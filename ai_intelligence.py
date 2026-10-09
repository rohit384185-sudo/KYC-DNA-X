
import csv
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from case_evidence import build_case_evidence
from kyc_engine import calculate_friction_score

DATA_FILE = (
    Path(__file__).resolve().parent
    / "synthetic_kyc_cases.csv"
)

ERROR_OPTIONS = [
    "None",
    "File too large",
    "Unreadable document",
    "Upload timeout",
    "Unsupported format"
]


def priority_for_score(score):
    if score >= 60:
        return "High support priority"
    if score >= 30:
        return "Medium support priority"
    return "Low support priority"


def simulate(missing_count, attempts, error):
    customer = {
        "missing": [
            f"Requirement {i + 1}"
            for i in range(missing_count)
        ],
        "attempts": attempts,
        "error": error
    }

    return build_case_evidence(
        "Interactive synthetic scenario",
        customer
    )


def cohort_summary():
    counts = {"Low": 0, "Medium": 0, "High": 0}
    scores = []

    with DATA_FILE.open(
        newline="", encoding="utf-8-sig"
    ) as handle:
        rows = list(csv.DictReader(handle))

    for row in rows:
        score = calculate_friction_score(
            int(row["missing_requirements"]),
            int(row["upload_attempts"]),
            row["error"]
        )

        scores.append(score)

        if score >= 60:
            counts["High"] += 1
        elif score >= 30:
            counts["Medium"] += 1
        else:
            counts["Low"] += 1

    return {
        "total": len(rows),
        "counts": counts,
        "average": (
            round(sum(scores) / len(scores), 1)
            if scores else 0
        ),
        "capped": sum(x == 100 for x in scores)
    }


TEST_CASES = [
    (0, 1, "None", 0, "Low"),
    (1, 1, "None", 20, "Low"),
    (2, 1, "None", 40, "Medium"),
    (0, 4, "None", 30, "Medium"),
    (0, 1, "File too large", 15, "Low"),
    (1, 4, "File too large", 65, "High"),
    (3, 0, "None", 60, "High"),
    (0, 7, "None", 60, "High"),
    (5, 9, "Upload timeout", 100, "High")
]


def run_evaluation():
    results = []

    for missing, attempts, error, expected, band in TEST_CASES:
        actual = calculate_friction_score(
            missing, attempts, error
        )

        actual_band = priority_for_score(
            actual
        ).split()[0]

        passed = (
            actual == expected
            and actual_band == band
        )

        results.append({
            "Missing": missing,
            "Attempts": attempts,
            "Error": error,
            "Expected score": expected,
            "Actual score": actual,
            "Expected priority": band,
            "Actual priority": actual_band,
            "Passed": passed
        })

    return results


def render_ai_intelligence():
    st.title("AI Intelligence & Evaluation Lab")

    st.caption(
        "Explainable rule-based decision support using "
        "synthetic onboarding data. No trained AI model, "
        "fraud assessment or KYC approval decisions."
    )

    st.subheader("Interactive Scenario Simulator")

    c1, c2, c3 = st.columns(3)

    with c1:
        missing = st.slider(
            "Missing requirements",
            min_value=0,
            max_value=5,
            value=1,
            key="ai_missing"
        )

    with c2:
        attempts = st.slider(
            "Upload attempts",
            min_value=0,
            max_value=9,
            value=4,
            key="ai_attempts"
        )

    with c3:
        error = st.selectbox(
            "Upload error",
            ERROR_OPTIONS,
            index=1,
            key="ai_error"
        )

    result = simulate(missing, attempts, error)

    a, b, c = st.columns(3)

    a.metric(
        "Calculated Friction",
        f'{result["score"]}/100'
    )

    b.metric(
        "Reason Codes",
        len(result["reason_codes"])
    )

    c.metric(
        "Raw Rule Points",
        result["raw_points"]
    )

    if result["score"] >= 60:
        st.warning(result["priority"])
    else:
        st.info(result["priority"])

    st.markdown("#### Why this result?")

    st.dataframe(
        result["evidence"],
        hide_index=True,
        use_container_width=True
    )

    st.markdown("#### Triggered Reason Codes")

    if result["reason_codes"]:
        st.code(
            " | ".join(result["reason_codes"]),
            language=None
        )
    else:
        st.success(
            "No friction reason codes triggered."
        )

    st.markdown("#### Recommended Actions")

    for index, action in enumerate(
        result["recommended_actions"], 1
    ):
        st.write(f"{index}. {action}")

    st.divider()

    st.subheader("Synthetic Cohort Intelligence")

    cohort = cohort_summary()

    x, y, z = st.columns(3)

    x.metric("Synthetic Cases", cohort["total"])
    y.metric("Average Friction", cohort["average"])
    z.metric(
        "Scores Capped at 100",
        cohort["capped"]
    )

    labels = ["Low", "Medium", "High"]

    values = [
        cohort["counts"][label]
        for label in labels
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
        title="Support Priority Distribution",
        yaxis_title="Synthetic cases",
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        margin=dict(
            l=20,
            r=20,
            t=65,
            b=40
        )
    )

    st.plotly_chart(
        figure,
        use_container_width=True
    )

    st.caption(
        "Priority bands: Low 0-29, Medium 30-59, "
        "High 60-100. Counts are recalculated "
        "from 500 synthetic CSV records."
    )

    st.divider()

    st.subheader(
        "Evaluation & Policy Regression Lab"
    )

    results = run_evaluation()

    passed = sum(
        item["Passed"]
        for item in results
    )

    total = len(results)

    st.metric(
        "Policy Tests Passed",
        f"{passed}/{total}"
    )

    if passed == total:
        st.success(
            "All predefined policy regression "
            "scenarios passed."
        )
    else:
        st.error(
            "Some policy scenarios failed. "
            "Review the results below."
        )

    st.dataframe(
        results,
        hide_index=True,
        use_container_width=True
    )

    st.caption(
        "This is deterministic rule-conformance testing, "
        "not a model accuracy, precision or recall claim. "
        "Real-world validation would require independent "
        "outcomes, representative data and governance."
    )
