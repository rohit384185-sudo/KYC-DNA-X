
from collections import Counter, defaultdict
from hashlib import sha256

import plotly.graph_objects as go
import streamlit as st

from analytics_data import load_cases
from kyc_engine import calculate_friction_score


def band(score):
    if score >= 60:
        return "High"
    if score >= 30:
        return "Medium"
    return "Low"


def selected_for_change(case_id, percentage, salt):
    if not 0 <= percentage <= 100:
        raise ValueError("Percentage must be 0-100")
    if percentage == 100:
        return True
    if percentage == 0:
        return False
    token = f"{salt}:{case_id}".encode("utf-8")
    number = int.from_bytes(
        sha256(token).digest()[:8], "big"
    )
    return number % 100 < percentage


def simulate_intervention(
    rows, retry_reduction=1, retry_coverage=50,
    error_resolution=25
):
    if not 0 <= retry_reduction <= 5:
        raise ValueError("Invalid retry reduction")

    baseline = Counter()
    improved = Counter()
    before_scores = []
    after_scores = []
    changes = 0

    for row in rows:
        case_id = row["case_id"]
        missing = int(row["missing_requirements"])
        attempts = int(row["upload_attempts"])
        error = str(row["error"])

        before = calculate_friction_score(
            missing, attempts, error
        )

        adjusted_attempts = attempts
        if selected_for_change(
            case_id, retry_coverage, "retry"
        ):
            adjusted_attempts = max(
                1 if attempts >= 1 else 0,
                attempts - retry_reduction
            )

        adjusted_error = error
        if error != "None" and selected_for_change(
            case_id, error_resolution, "error"
        ):
            adjusted_error = "None"

        after = calculate_friction_score(
            missing, adjusted_attempts, adjusted_error
        )

        baseline[band(before)] += 1
        improved[band(after)] += 1
        before_scores.append(before)
        after_scores.append(after)

        if before != after:
            changes += 1

    size = len(rows)

    return {
        "total": size,
        "baseline": dict(baseline),
        "improved": dict(improved),
        "baseline_average": (
            round(sum(before_scores) / size, 1)
            if size else 0
        ),
        "improved_average": (
            round(sum(after_scores) / size, 1)
            if size else 0
        ),
        "cases_improved": changes
    }


def root_causes(rows):
    by_stage = defaultdict(
        lambda: {
            "cases": 0,
            "with_errors": 0,
            "missing": 0,
            "repeat_uploads": 0
        }
    )
    errors = Counter()
    missing_counts = Counter()

    for row in rows:
        stage = str(row["stage"])
        attempts = int(row["upload_attempts"])
        missing = int(row["missing_requirements"])
        error = str(row["error"])

        item = by_stage[stage]
        item["cases"] += 1
        item["with_errors"] += int(error != "None")
        item["missing"] += int(missing > 0)
        item["repeat_uploads"] += int(attempts > 1)

        missing_counts[missing] += 1

        if error != "None":
            errors[error] += 1

    return {
        "stages": [
            {
                "Stage": stage,
                "Cases": item["cases"],
                "Error cases": item["with_errors"],
                "Missing requirement cases": item["missing"],
                "Repeat upload cases": item["repeat_uploads"],
                "Error rate %": round(
                    100 * item["with_errors"]
                    / item["cases"], 1
                )
            }
            for stage, item in sorted(by_stage.items())
        ],
        "errors": dict(errors),
        "missing_counts": dict(missing_counts)
    }


def success_metrics(rows):
    size = len(rows)
    errors = sum(
        str(r["error"]) != "None" for r in rows
    )
    repeated = sum(
        int(r["upload_attempts"]) > 1 for r in rows
    )
    missing = sum(
        int(r["missing_requirements"]) > 0
        for r in rows
    )
    extra = sum(
        max(int(r["upload_attempts"]) - 1, 0)
        for r in rows
    )

    def percent(number):
        return round(number / size * 100, 1) if size else 0

    return {
        "cases": size,
        "error_cases": errors,
        "error_rate": percent(errors),
        "repeat_cases": repeated,
        "repeat_rate": percent(repeated),
        "missing_cases": missing,
        "missing_rate": percent(missing),
        "extra_attempts": extra,
        "extra_attempts_per_case": (
            round(extra / size, 2) if size else 0
        )
    }


def chart_bar(labels, series, title):
    fig = go.Figure()
    colors = ["#38bdf8", "#2dd4bf", "#fb7185"]
    for i, (name, values) in enumerate(series):
        fig.add_trace(go.Bar(
            name=name,
            x=labels,
            y=values,
            marker_color=colors[i % len(colors)],
            text=values,
            textposition="outside"
        ))

    max_value = max(
        [1] + [
            value
            for _, values in series
            for value in values
        ]
    )
    fig.update_layout(
        title=title,
        barmode="group",
        yaxis=dict(range=[0, max_value * 1.23]),
        height=365,
        margin=dict(l=25, r=15, t=65, b=45),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0"
    )
    return fig


def render_product_intelligence():
    st.title("Product Intelligence Lab")
    st.caption(
        "Synthetic operational analytics and hypothetical "
        "improvement scenarios. Not observed business impact "
        "or real KYC decision-making."
    )

    rows = load_cases()

    st.subheader("1. Friction Reduction Simulator")
    st.write(
        "What-if analysis: agar upload journey improve ho, "
        "to existing rule-based friction scores par kya "
        "effect padega?"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        retry_reduction = st.slider(
            "Attempts reduced per selected case",
            0, 5, 1,
            key="v2_retry_reduction"
        )
    with col2:
        retry_coverage = st.slider(
            "Cases receiving retry assistance (%)",
            0, 100, 50,
            key="v2_retry_coverage"
        )
    with col3:
        error_resolution = st.slider(
            "Recorded errors resolved (%)",
            0, 100, 25,
            key="v2_error_resolution"
        )

    scenario = simulate_intervention(
        rows, retry_reduction, retry_coverage,
        error_resolution
    )

    a, b, c, d = st.columns(4)
    a.metric(
        "Baseline Average",
        f'{scenario["baseline_average"]}/100'
    )
    b.metric(
        "Simulated Average",
        f'{scenario["improved_average"]}/100'
    )
    c.metric(
        "Score Improvement",
        round(
            scenario["baseline_average"]
            - scenario["improved_average"], 1
        )
    )
    d.metric(
        "Cases with Lower Scores",
        scenario["cases_improved"]
    )

    labels = ["Low", "Medium", "High"]
    before = [
        scenario["baseline"].get(label, 0)
        for label in labels
    ]
    after = [
        scenario["improved"].get(label, 0)
        for label in labels
    ]

    st.plotly_chart(
        chart_bar(
            labels,
            [
                ("Baseline", before),
                ("Simulated", after)
            ],
            "Support Priority ? Before vs What-If"
        ),
        use_container_width=True
    )
    st.caption(
        "Changes are selected deterministically for a "
        "reproducible illustration, not randomly or from "
        "observed intervention outcomes. 100% means all "
        "eligible cases receive that hypothetical change. "
        "This is not a predicted completion-rate uplift."
    )

    st.divider()
    st.subheader("2. Root-Cause & Cohort Comparison")

    analysis = root_causes(rows)
    stage_rows = analysis["stages"]

    st.dataframe(
        stage_rows,
        hide_index=True,
        use_container_width=True
    )

    left, right = st.columns(2)

    with left:
        error_names = sorted(analysis["errors"])
        st.plotly_chart(
            chart_bar(
                error_names,
                [(
                    "Recorded errors",
                    [
                        analysis["errors"][name]
                        for name in error_names
                    ]
                )],
                "Upload Error Categories"
            ),
            use_container_width=True
        )

    with right:
        stages = [item["Stage"] for item in stage_rows]
        st.plotly_chart(
            chart_bar(
                stages,
                [(
                    "Error cases",
                    [
                        item["Error cases"]
                        for item in stage_rows
                    ]
                )],
                "Upload Errors by Onboarding Stage"
            ),
            use_container_width=True
        )

    st.caption(
        "The 500-case CSV records missing requirement "
        "counts, not document names. Document-type root "
        "cause analysis needs an enriched dataset; "
        "we do not invent document labels."
    )

    st.divider()
    st.subheader("3. Product Success Metrics")

    metrics = success_metrics(rows)

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Error Rate", f'{metrics["error_rate"]}%')
    p2.metric(
        "Repeat Upload Rate",
        f'{metrics["repeat_rate"]}%'
    )
    p3.metric(
        "Missing Requirement Rate",
        f'{metrics["missing_rate"]}%'
    )
    p4.metric(
        "Extra Attempts / Case",
        metrics["extra_attempts_per_case"]
    )

    st.markdown("#### Outcome Measurement Framework")
    st.dataframe(
        [
            {
                "Metric": "Onboarding completion rate",
                "Required evidence": (
                    "Completed/failed status for every case"
                ),
                "Current availability": "Not recorded"
            },
            {
                "Metric": "Time to resolution",
                "Required evidence": (
                    "Created and resolved timestamps"
                ),
                "Current availability": "Not recorded"
            },
            {
                "Metric": "Human support workload",
                "Required evidence": (
                    "Assignments, actions, closure events"
                ),
                "Current availability": (
                    "Partial three-customer demo history"
                )
            }
        ],
        hide_index=True,
        use_container_width=True
    )

    st.info(
        "Current KPIs are descriptive synthetic data. "
        "Business outcome metrics will become measurable "
        "once their lifecycle events are captured."
    )
