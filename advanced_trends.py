
from collections import defaultdict
from datetime import date, datetime
import csv
import io

import plotly.graph_objects as go
import streamlit as st


def aggregate_trends(rows, frequency="Daily"):
    if frequency not in ("Daily", "Weekly"):
        raise ValueError("Unsupported frequency")

    buckets = defaultdict(lambda: {"cases": 0, "errors": 0})

    for row in rows:
        day = date.fromisoformat(str(row["case_date"]))

        if frequency == "Weekly":
            day = day.fromordinal(day.toordinal() - day.weekday())

        key = day.isoformat()
        buckets[key]["cases"] += 1

        if str(row["error"]).strip().lower() not in ("none", ""):
            buckets[key]["errors"] += 1

    return [
        {
            "period": key,
            "cases": buckets[key]["cases"],
            "errors": buckets[key]["errors"]
        }
        for key in sorted(buckets)
    ]


def export_csv(data):
    buffer = io.StringIO()
    writer = csv.DictWriter(
        buffer, fieldnames=["period", "cases", "errors"]
    )
    writer.writeheader()
    writer.writerows(data)
    return buffer.getvalue().encode("utf-8")


def render_trend_intelligence(rows):
    st.divider()
    st.subheader("Temporal Friction Intelligence")
    st.caption(
        "Date-based trends from synthetic case records. "
        "Reflects existing stage and error filters. "
        "Not a conversion funnel or a forecast."
    )

    frequency = st.selectbox(
        "Trend Grouping",
        ["Daily", "Weekly"],
        key="kyc_trend_frequency"
    )

    try:
        trends = aggregate_trends(rows, frequency)
    except (ValueError, KeyError, TypeError) as exc:
        st.error(f"Unable to calculate trends: {exc}")
        return

    if not trends:
        st.info("No case records match the current filters.")
        return

    total = sum(item["cases"] for item in trends)
    errors = sum(item["errors"] for item in trends)
    peak = max(trends, key=lambda item: item["cases"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Filtered Cases", total)
    c2.metric("Cases With Errors", errors)
    c3.metric("Recorded Error Share", f"{errors / total:.1%}")
    c4.metric("Busiest Period", peak["period"])

    periods = [item["period"] for item in trends]
    volumes = [item["cases"] for item in trends]
    failures = [item["errors"] for item in trends]

    a, b = st.columns(2)

    with a:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=periods, y=volumes,
            mode="lines+markers",
            name="Recorded cases",
            line=dict(color="#2dd4bf", width=3),
            hovertemplate="%{x}: %{y} cases<extra></extra>"
        ))
        fig.update_layout(
            title=f"{frequency} Case Volume",
            xaxis_title="Case date / period",
            yaxis_title="Recorded cases",
            height=350,
            margin=dict(l=20, r=20, t=60, b=60),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0"
        )
        st.plotly_chart(fig, use_container_width=True)

    with b:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=periods, y=failures,
            name="Cases with recorded errors",
            marker_color="#fb7185",
            hovertemplate="%{x}: %{y} errors<extra></extra>"
        ))
        fig.update_layout(
            title=f"{frequency} Upload Error Trend",
            xaxis_title="Case date / period",
            yaxis_title="Cases with errors",
            height=350,
            margin=dict(l=20, r=20, t=60, b=60),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        "Download Trend Summary (CSV)",
        data=export_csv(trends),
        file_name="kyc_dna_trend_summary.csv",
        mime="text/csv",
        key="kyc_trend_export"
    )
