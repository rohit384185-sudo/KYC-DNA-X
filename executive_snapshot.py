
import plotly.graph_objects as go
import streamlit as st

from ai_intelligence import cohort_summary
from customer_data import CUSTOMERS
from review_store import current_status


def build_snapshot():
    cohort = cohort_summary()
    total = cohort["total"]

    if total == 0:
        high_share = 0.0
    else:
        high_share = round(
            cohort["counts"]["High"] / total * 100, 1
        )

    reviews = [
        {
            "Customer": name,
            "Review status": current_status(name),
            "Missing requirements": len(record["missing"]),
            "Upload attempts": record["attempts"]
        }
        for name, record in CUSTOMERS.items()
    ]

    return {
        "total": total,
        "high_priority": cohort["counts"]["High"],
        "high_share": high_share,
        "average_friction": cohort["average"],
        "capped_scores": cohort["capped"],
        "distribution": cohort["counts"],
        "reviews": reviews,
        "open_reviews": sum(
            r["Review status"] in (
                "Needs follow-up",
                "Awaiting customer"
            )
            for r in reviews
        )
    }


def render_executive_snapshot():
    snapshot = build_snapshot()

    st.divider()
    st.subheader("Executive Intelligence Snapshot")
    st.caption(
        "Support prioritization calculated from synthetic "
        "case records. The human-review demonstration "
        "below uses three separate fictional customers."
    )

    a, b, c, d = st.columns(4)

    a.metric(
        "High-Priority Cases",
        snapshot["high_priority"]
    )
    b.metric(
        "High-Priority Share",
        f'{snapshot["high_share"]}%'
    )
    c.metric(
        "Average Friction",
        f'{snapshot["average_friction"]}/100'
    )
    d.metric(
        "Capped Scores",
        snapshot["capped_scores"]
    )

    left, right = st.columns([3, 2])

    with left:
        st.markdown("#### Support Priority Breakdown")

        labels = ["Low", "Medium", "High"]
        values = [
            snapshot["distribution"][key]
            for key in labels
        ]

        figure = go.Figure(
            go.Bar(
                x=labels,
                y=values,
                text=values,
                textposition="outside",
                marker_color=[
                    "#2dd4bf",
                    "#fbbf24",
                    "#fb7185"
                ]
            )
        )

        figure.update_layout(
            height=335,
            yaxis_title="Synthetic cases",
            xaxis_title="Support priority",
            yaxis=dict(
                range=[0, max(values + [1]) * 1.20]
            ),
            showlegend=False,
            margin=dict(l=25, r=20, t=35, b=45),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0"
        )

        st.plotly_chart(
            figure,
            use_container_width=True
        )

    with right:
        st.markdown("#### Operational Interpretation")
        st.write(
            f'{snapshot["high_priority"]} of '
            f'{snapshot["total"]} synthetic records '
            "fall in the high support-priority band."
        )
        st.write(
            "These categories describe potential "
            "onboarding assistance needs, not "
            "fraud or identity-verification outcomes."
        )
        st.info(
            "Suggested product action: prioritize "
            "upload guidance and human support "
            "for high-friction journeys."
        )

    st.markdown("#### Human Review Snapshot")
    st.caption(
        "Separate three-customer demo review queue; "
        "not a subset linked to the 500-case CSV."
    )

    st.dataframe(
        snapshot["reviews"],
        hide_index=True,
        use_container_width=True
    )

    st.caption(
        f'Open follow-up / awaiting-customer statuses: '
        f'{snapshot["open_reviews"]}. '
        "Manage these records in Human Review Queue."
    )
