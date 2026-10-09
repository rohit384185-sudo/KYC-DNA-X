from customer_data import CUSTOMERS
import streamlit as st
import io
from contextlib import redirect_stdout
from kyc_engine import analyze_upload_friction, calculate_friction_score

st.set_page_config(
    page_title="KYC DNA",
    page_icon="???",
    layout="wide"
)

st.markdown(
    '''
    <style>
    .stApp {
        background:
          radial-gradient(circle at 85% 5%, #192e40 0%, transparent 32%),
          #080d19;
        color: #edf5ff;
    }
    .block-container {
        padding-top: 5rem;
        max-width: 1350px;
    }
    .kyc-hero {
        padding: 28px 32px;
        border: 1px solid #22465b;
        border-radius: 20px;
        background: linear-gradient(120deg, #10283a, #111126 75%);
        box-shadow: 0 12px 36px #0005;
        margin-bottom: 22px;
    }
    .kyc-eyebrow {
        color: #3ee7d0;
        font-weight: 700;
        letter-spacing: 2px;
        font-size: 12px;
    }
    .kyc-hero h1 {
        color: #ffffff;
        font-size: 44px;
        margin: 8px 0;
        font-weight: 800;
    }
    .kyc-hero p {
        color: #aab9d3;
    }
    

/* KYC DNA X HERO TOP SPACING FIX */
.kyc-hero {
    padding-top: 34px !important;
}
.kyc-eyebrow {
    line-height: 1.5 !important;
    margin-top: 0 !important;
    display: block;
}

/* KYC DNA X COMPACT HERO */
.kyc-hero {
    padding-top: 20px !important;
    padding-bottom: 20px !important;
    min-height: auto !important;
}
.kyc-hero h1 {
    font-size: 34px !important;
    line-height: 1.15 !important;
    margin: 8px 0 !important;
}
.kyc-hero p {
    margin: 6px 0 !important;
}
</style>
<div class="kyc-hero">
  <div class="kyc-eyebrow">IDENTITY INTELLIGENCE PLATFORM</div>
  <h1>KYC DNA X</h1>
  <p>Detect friction. Explain decisions. Protect onboarding.</p>
</div>
    ''',
    unsafe_allow_html=True
)
st.caption("Identity Friction Intelligence | Portfolio Prototype")


st.markdown("""
<style>


/* KYC DNA X PLOTLY GLASS PANELS */
[data-testid="stPlotlyChart"] {
    background: linear-gradient(
        145deg,
        rgba(21, 42, 64, 0.70),
        rgba(10, 20, 36, 0.85)
    );
    border: 1px solid rgba(69, 135, 166, 0.30);
    border-radius: 18px;
    padding: 12px;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.15);
    overflow: hidden;
}

.chart-card {
    background: linear-gradient(180deg, rgba(16,29,53,0.92), rgba(10,20,38,0.92));
    border: 1px solid rgba(61, 187, 255, 0.18);
    border-radius: 18px;
    padding: 18px 18px 8px 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.18);
    margin-bottom: 18px;
}
.chart-card-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #f3f7ff;
    margin-bottom: 6px;
}
.chart-card-caption {
    font-size: 0.90rem;
    color: #9bb0c7;
    margin-bottom: 12px;
}

.premium-kpi {
    background: linear-gradient(145deg, #152a40, #101729);
    border: 1px solid #29465e;
    border-radius: 18px;
    padding: 25px 22px;
    min-height: 150px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.22);
}
.kpi-label {
    color: #9eb5c9;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.1px;
}
.kpi-value {
    color: #f1f7ff;
    font-size: 42px;
    font-weight: 800;
    margin-top: 10px;
}
.kpi-note {
    color: #47dbc8;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## KYC DNA X")
st.sidebar.caption("IDENTITY FRICTION INTELLIGENCE")

st.markdown("""
<style>
/* KYC DNA X PREMIUM SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0e2034 0%, #0a1424 100%);
    border-right: 1px solid #26465b;
}
[data-testid="stSidebar"] h2 {
    color: #f3faff;
    font-weight: 800;
    letter-spacing: 0.5px;
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #91aabd;
}
[data-testid="stSidebar"] [role="radiogroup"] label {
    border-radius: 11px;
    padding: 11px 12px;
    transition: background 0.2s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: #17344a;
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(90deg, #164449, #173047);
    border: 1px solid #2dd4bf66;
}
[data-testid="stSidebar"] input[type="radio"] {
    accent-color: #2dd4bf;
}
</style>
""", unsafe_allow_html=True)


st.sidebar.divider()

selected_page = st.sidebar.radio(
    "WORKSPACE",
    [
        "Executive Dashboard",
        "Advanced Analytics",
        "Human Review Queue",
        "AI Intelligence",
        "Case Investigation"
    ],
    key="kyc_sidebar_navigation"
)

st.sidebar.divider()
st.sidebar.caption("Portfolio Prototype | Synthetic Data")


if selected_page == "Executive Dashboard":

    from analytics_data import load_cases, calculate_overview

    executive_cases = load_cases()
    executive_report = calculate_overview(executive_cases)

    recorded_errors = sum(
        executive_report["error_breakdown"].values()
    )

    st.subheader("Executive Command Center")
    st.caption(
        "Portfolio Prototype | 500 Synthetic KYC Cases | "
        "Operational Friction Metrics"
    )

    executive_metrics = [
        (
            "TOTAL CASES",
            executive_report["total_cases"],
            "Synthetic onboarding records"
        ),
        (
            "MISSING REQUIREMENTS",
            executive_report["incomplete_cases"],
            "Cases with missing items"
        ),
        (
            "EXTRA UPLOAD ATTEMPTS",
            executive_report["extra_attempts"],
            "Additional customer effort"
        ),
        (
            "RECORDED UPLOAD ERRORS",
            recorded_errors,
            "Cases with recorded errors"
        )
    ]

    executive_columns = st.columns(4)

    for column, (label, value, note) in zip(
        executive_columns, executive_metrics
    ):
        with column:
            st.markdown(
                f"""
                <div class="premium-kpi">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value:,}</div>
                    <div class="kpi-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()


    with st.expander("3-Customer Demonstration", expanded=False):
        st.subheader("Intelligence Overview")
        st.caption("Portfolio Demo | Synthetic Customer Data")

        overview_customers = CUSTOMERS

        total_cases = len(overview_customers)
        incomplete = sum(
            len(case["missing"]) > 0
            for case in overview_customers.values()
        )
        extra_attempts = sum(
            max(case["attempts"] - 1, 0)
            for case in overview_customers.values()
        )

        k1, k2, k3 = st.columns(3)

        with k1:
            st.markdown(
                f"""
                <div class="premium-kpi">
                  <div class="kpi-label">TOTAL CASES</div>
                  <div class="kpi-value">{total_cases}</div>
                  <div class="kpi-note">Synthetic customer records</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with k2:
            st.markdown(
                f"""
                <div class="premium-kpi">
                  <div class="kpi-label">INCOMPLETE CASES</div>
                  <div class="kpi-value">{incomplete}</div>
                  <div class="kpi-note">Action required</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with k3:
            st.markdown(
                f"""
                <div class="premium-kpi">
                  <div class="kpi-label">EXTRA UPLOAD ATTEMPTS</div>
                  <div class="kpi-value">{extra_attempts}</div>
                  <div class="kpi-note">Repeated customer effort</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        import plotly.graph_objects as go

        names = list(CUSTOMERS.keys())
        scores = [
            calculate_friction_score(
                len(case["missing"]),
                case["attempts"],
                case["error"]
            )
            for case in CUSTOMERS.values()
        ]

        fig = go.Figure(
            go.Bar(
                x=names,
                y=scores,
                marker_color=["#2dd4bf", "#8b5cf6", "#38bdf8"],
                text=scores,
                textposition="outside",
                hovertemplate="%{x}: %{y}/100<extra></extra>"
            )
        )

        fig.update_layout(
            title="Customer Friction Score Comparison",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            yaxis=dict(range=[0, 110], title="Friction Score"),
            xaxis=dict(title="Customer"),
            height=380
        )

        chart_left, chart_right = st.columns(2)
        with chart_left:
            st.plotly_chart(fig, use_container_width=True)

        action_required = sum(
            len(case["missing"]) > 0
            for case in CUSTOMERS.values()
        )
        review_pending = len(CUSTOMERS) - action_required

        status_fig = go.Figure(
            go.Pie(
                labels=[
                    "Action Required",
                    "Human Verification Pending"
                ],
                values=[action_required, review_pending],
                hole=0.65,
                marker=dict(colors=["#fb7185", "#2dd4bf"]),
                textinfo="label+percent",
                hovertemplate="%{label}: %{value} cases<extra></extra>"
            )
        )

        status_fig.update_layout(
            title="Case Status Distribution",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            height=400,
            showlegend=True
        )

        with chart_right:
            st.plotly_chart(status_fig, use_container_width=True)






    from executive_snapshot import render_executive_snapshot
    render_executive_snapshot()


if selected_page == "Advanced Analytics":
    import plotly.graph_objects as go

    st.divider()
    st.subheader("500-Case Synthetic Analytics")
    st.caption(
        "Generated portfolio dataset | Separate from the 3-customer investigation demo"
    )

    from analytics_data import load_cases, calculate_overview

    all_synthetic_cases = load_cases()

    stage_options = [
        "All Stages",
        "Registration",
        "PAN Verification",
        "Address Verification",
        "Bank Verification",
        "Human Review"
    ]

    selected_stage = st.selectbox(
        "Filter by Onboarding Stage",
        stage_options,
        key="synthetic_stage_filter"
    )

    if selected_stage == "All Stages":
        synthetic_cases = all_synthetic_cases
    else:
        synthetic_cases = [
            case for case in all_synthetic_cases
            if case["stage"] == selected_stage
        ]

    error_options = [
        "All Errors",
        "None",
        "File too large",
        "Unsupported format",
        "Unreadable document",
        "Upload timeout"
    ]

    selected_error = st.selectbox(
        "Filter by Upload Error",
        error_options,
        key="synthetic_error_filter"
    )

    if selected_error != "All Errors":
        synthetic_cases = [
            case for case in synthetic_cases
            if case["error"] == selected_error
        ]

    st.caption(
        f"Showing {len(synthetic_cases)} of "
        f"{len(all_synthetic_cases)} synthetic cases"
    )

    synthetic_report = calculate_overview(synthetic_cases)

    s1, s2, s3 = st.columns(3)

    synthetic_metrics = [
        (s1, "SYNTHETIC CASES", synthetic_report["total_cases"],
         "Generated test records"),
        (s2, "MISSING REQUIREMENTS",
         synthetic_report["incomplete_cases"],
         "Cases requiring document action"),
        (s3, "EXTRA UPLOAD ATTEMPTS",
         synthetic_report["extra_attempts"],
         "Additional upload effort"),
    ]

    for column, label, value, note in synthetic_metrics:
        with column:
            st.markdown(
                f"""
                <div class="premium-kpi">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value:,}</div>
                    <div class="kpi-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True
            )



    analytics_top_left, analytics_top_right = st.columns([2, 3])
    with analytics_top_left:
        st.markdown("### Document Requirements Intelligence")
        st.caption(
            "Filtered synthetic cases grouped by missing requirements. "
            "No KYC approval or rejection is inferred."
        )

        missing_cases = synthetic_report["incomplete_cases"]
        no_missing_cases = (
            synthetic_report["total_cases"] - missing_cases
        )

        requirements_chart_type = st.selectbox(
            "Choose Document Requirements Chart Type",
            ["Donut", "Pie", "Horizontal Bar"],
            key="requirements_chart_type"
        )

        if synthetic_report["total_cases"] == 0:
            st.info("No cases match the selected filters.")
        else:
            req_labels = [
                "Missing requirements",
                "No missing requirements"
            ]
            req_values = [
                missing_cases,
                no_missing_cases
            ]

            if requirements_chart_type == "Horizontal Bar":
                requirement_fig = go.Figure(
                    go.Bar(
                        x=req_values,
                        y=req_labels,
                        orientation="h",
                        marker_color=["#fb7185", "#2dd4bf"],
                        text=req_values,
                        textposition="outside",
                cliponaxis=False,
                        hovertemplate="%{y}: %{x} cases<extra></extra>"
                    )
                )
                requirement_fig.update_layout(
                    xaxis=dict(
                title="Number of cases",
                range=[0, max(req_values) * 1.22 if req_values else 1]
            ),
                    yaxis=dict(autorange="reversed"),
                    margin=dict(l=10, r=45, t=45, b=45)
                )
            else:
                requirement_fig = go.Figure(
                    go.Pie(
                        labels=req_labels,
                        values=req_values,
                        hole=0.63 if requirements_chart_type == "Donut" else 0,
                        marker=dict(colors=["#fb7185", "#2dd4bf"]),
                        textinfo="percent",
                        hovertemplate="%{label}: %{value} cases<extra></extra>"
                    )
                )
                requirement_fig.update_layout(
                    legend=dict(
                        orientation="h",
                        x=0.5,
                        xanchor="center",
                        y=-0.12
                    ),
                    margin=dict(l=10, r=10, t=45, b=50)
                )

            requirement_fig.update_layout(
                title="Synthetic Document Requirements Distribution",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                height=330
            )

            st.plotly_chart(
                requirement_fig,
                use_container_width=True
            )

    with analytics_top_right:
        st.markdown("### Upload Error Intelligence")
        st.caption(
            "Error counts from 500 fictional records; not real bank performance."
        )

        error_counts = synthetic_report["error_breakdown"]
        ordered_errors = sorted(
            error_counts.items(),
            key=lambda item: item[1],
            reverse=True
        )

        error_names = [item[0] for item in ordered_errors]
        error_values = [item[1] for item in ordered_errors]

        error_chart_type = st.selectbox(
            "Choose Upload Error Chart Type",
            ["Horizontal Bar", "Pie", "Donut"],
            key="upload_error_chart_type"
        )

        if error_chart_type == "Horizontal Bar":
            error_fig = go.Figure(
                go.Bar(
                    x=error_values,
                    y=error_names,
                    orientation="h",
                    marker_color="#2dd4bf",
                    text=error_values,
                    textposition="outside",
                    hovertemplate="%{y}: %{x} cases<extra></extra>"
                )
            )

            error_fig.update_layout(
                title="Synthetic Upload Error Breakdown",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                xaxis=dict(title="Number of cases"),
                yaxis=dict(autorange="reversed"),
                height=350,
                margin=dict(l=20, r=45, t=65, b=45)
            )

        else:
            error_fig = go.Figure(
                go.Pie(
                    labels=error_names,
                    values=error_values,
                    hole=0.62 if error_chart_type == "Donut" else 0,
                    marker=dict(
                        colors=[
                            "#2dd4bf", "#38bdf8",
                            "#8b5cf6", "#fb7185"
                        ]
                    ),
                    textinfo="percent",
                    hovertemplate=(
                        "%{label}: %{value} cases<extra></extra>"
                    )
                )
            )

            error_fig.update_layout(
                title="Synthetic Upload Error Breakdown",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                height=350,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    y=-0.12,
                    x=0.5,
                    xanchor="center"
                ),
                margin=dict(l=15, r=15, t=65, b=60)
            )

        st.plotly_chart(error_fig, use_container_width=True)



    st.markdown("### Onboarding Stage Intelligence")
    st.caption(
        "Distribution of recorded stages across synthetic cases. "
        "Not a conversion funnel or completion rate."
    )

    from collections import Counter

    stage_counts = Counter(
        row["stage"] for row in synthetic_cases
    )

    stage_order = [
        "Registration",
        "PAN Verification",
        "Address Verification",
        "Bank Verification",
        "Human Review"
    ]

    stage_names = stage_order
    stage_values = [stage_counts.get(name, 0) for name in stage_names]

    stage_chart_type = st.selectbox(
        "Choose Onboarding Stage Chart Type",
        ["Vertical Bar", "Horizontal Bar", "Pie", "Donut"],
        key="stage_chart_type"
    )

    if stage_chart_type == "Vertical Bar":
        stage_fig = go.Figure(
            go.Bar(
                x=stage_names,
                y=stage_values,
                marker_color=[
                    "#2dd4bf",
                    "#38bdf8",
                    "#8b5cf6",
                    "#fb7185",
                    "#fbbf24"
                ],
                text=stage_values,
                textposition="outside",
                hovertemplate="%{x}: %{y} cases<extra></extra>"
            )
        )

        stage_fig.update_layout(
            title="Synthetic Onboarding Stage Distribution",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            xaxis=dict(title="Recorded onboarding stage"),
            yaxis=dict(title="Number of cases"),
            height=420,
            margin=dict(l=20, r=20, t=65, b=60)
        )

    elif stage_chart_type == "Horizontal Bar":
        stage_fig = go.Figure(
            go.Bar(
                x=stage_values,
                y=stage_names,
                orientation="h",
                marker_color=[
                    "#2dd4bf",
                    "#38bdf8",
                    "#8b5cf6",
                    "#fb7185",
                    "#fbbf24"
                ],
                text=stage_values,
                textposition="outside",
                hovertemplate="%{y}: %{x} cases<extra></extra>"
            )
        )

        stage_fig.update_layout(
            title="Synthetic Onboarding Stage Distribution",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            xaxis=dict(title="Number of cases"),
            yaxis=dict(title="Recorded onboarding stage", autorange="reversed"),
            height=420,
            margin=dict(l=20, r=45, t=65, b=45)
        )

    elif stage_chart_type == "Pie":
        stage_fig = go.Figure(
            go.Pie(
                labels=stage_names,
                values=stage_values,
                hole=0,
                marker=dict(
                    colors=[
                        "#2dd4bf",
                        "#38bdf8",
                        "#8b5cf6",
                        "#fb7185",
                        "#fbbf24"
                    ]
                ),
                textinfo="percent",
                hovertemplate="%{label}: %{value} cases (%{percent})<extra></extra>"
            )
        )

        stage_fig.update_layout(
            title="Synthetic Onboarding Stage Distribution",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            height=420,
            margin=dict(l=20, r=20, t=65, b=20),
            legend=dict(orientation="h", y=-0.1)
        )

    else:
        stage_fig = go.Figure(
            go.Pie(
                labels=stage_names,
                values=stage_values,
                hole=0.55,
                marker=dict(
                    colors=[
                        "#2dd4bf",
                        "#38bdf8",
                        "#8b5cf6",
                        "#fb7185",
                        "#fbbf24"
                    ]
                ),
                textinfo="percent",
                hovertemplate="%{label}: %{value} cases (%{percent})<extra></extra>"
            )
        )

        stage_fig.update_layout(
            title="Synthetic Onboarding Stage Distribution",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            height=420,
            margin=dict(l=20, r=20, t=65, b=20),
            legend=dict(orientation="h", y=-0.1)
        )

    st.plotly_chart(stage_fig, use_container_width=True)


    st.divider()

    from advanced_trends import render_trend_intelligence
    render_trend_intelligence(synthetic_cases)

    st.divider()
    st.subheader("Case Explorer")
    st.caption(
        "Search fictional case IDs within your selected stage and error filters."
    )

    case_query = st.text_input(
        "Search by Case ID",
        placeholder="Example: KYC-0001",
        key="synthetic_case_search"
    ).strip().casefold()

    visible_cases = [
        case for case in synthetic_cases
        if case_query in case["case_id"].casefold()
    ]

    st.caption(
        f"Displaying {len(visible_cases)} of "
        f"{len(synthetic_cases)} filtered cases"
    )

    st.dataframe(
        visible_cases,
        use_container_width=True,
        hide_index=True,
        column_order=[
            "case_id",
            "stage",
            "missing_requirements",
            "upload_attempts",
            "error",
            "case_date"
        ]
    )


    import csv
    import io

    export_buffer = io.StringIO()

    export_columns = [
        "case_id",
        "stage",
        "missing_requirements",
        "upload_attempts",
        "error",
        "case_date"
    ]

    export_writer = csv.DictWriter(
        export_buffer,
        fieldnames=export_columns
    )

    export_writer.writeheader()
    export_writer.writerows(visible_cases)

    st.download_button(
        label="Download Visible Cases (CSV)",
        data=export_buffer.getvalue().encode("utf-8-sig"),
        file_name="kyc_dna_filtered_cases.csv",
        mime="text/csv",
        disabled=len(visible_cases) == 0,
        key="synthetic_case_csv_export"
    )

    st.caption(
        "Export includes only currently visible synthetic cases "
        "after stage, error, and Case ID filters."
    )

if selected_page == "Case Investigation":


    customers = CUSTOMERS

    name = st.selectbox("Select Customer", list(customers.keys()))
    customer = customers[name]

    col1, col2 = st.columns(2)
    col1.metric("Missing Requirements", len(customer["missing"]))
    col2.metric("Upload Attempts", customer["attempts"])


    extra_attempts = max(customer["attempts"] - 1, 0)
    st.metric("Extra Upload Attempts", extra_attempts)


    friction_score = calculate_friction_score(
        len(customer["missing"]),
        customer["attempts"],
        customer["error"]
    )
    st.metric("Friction Severity Score", f"{friction_score}/100")

    st.subheader("Case Analysis")

    if customer["missing"]:
        st.warning("Action Required")
        st.write("Missing:", ", ".join(customer["missing"]))
    else:
        st.success("Requirements recorded; human verification pending")

    st.caption("Synthetic data only. No KYC approvals are issued.")


    st.subheader("Central Engine Result")

    output = io.StringIO()

    with redirect_stdout(output):
        analyze_upload_friction(
            customer["attempts"],
            customer["error"]
        )

    st.code(output.getvalue())


    st.divider()
    st.subheader("Explainable Friction Intelligence")
    st.caption(
        "Rule-based customer-friction analysis. "
        "Not a fraud score or identity verification decision."
    )

    missing_total = len(customer["missing"])
    attempt_total = customer["attempts"]
    recorded_error = customer["error"]

    missing_points = missing_total * 20
    retry_points = max(attempt_total - 1, 0) * 10
    error_points = 15 if recorded_error != "None" else 0

    raw_score = missing_points + retry_points + error_points
    final_score = min(100, raw_score)

    st.markdown("#### Friction Score Breakdown")

    breakdown = [
        ("Missing requirements", missing_points),
        ("Additional upload attempts", retry_points),
        ("Recorded upload error", error_points)
    ]

    for reason, points in breakdown:
        st.write(f"{reason}: **+{points} points**")

    st.progress(final_score / 100)
    st.caption(
        f"Total rule points: {raw_score} | "
        f"Customer friction score: {final_score}/100 "
        "(capped at 100)"
    )

    st.markdown("#### Recommended Next Actions")

    recommendations = []

    if missing_total > 0:
        recommendations.append(
            "Request the outstanding documents: "
            + ", ".join(customer["missing"])
        )

    if recorded_error == "File too large":
        recommendations.append(
            "Show approved file-size and compression instructions."
        )
    elif recorded_error == "Unreadable document":
        recommendations.append(
            "Ask for a clearer document scan or photograph."
        )
    elif recorded_error == "Upload timeout":
        recommendations.append(
            "Offer retry guidance and investigate connectivity."
        )
    elif recorded_error == "Unsupported format":
        recommendations.append(
            "Show accepted file formats and conversion guidance."
        )
    elif recorded_error != "None":
        recommendations.append(
            "Investigate the recorded upload error."
        )

    if attempt_total >= 3:
        recommendations.append(
            "Offer human support due to repeated upload attempts."
        )

    if not recommendations:
        recommendations.append(
            "No friction action identified by current rules. "
            "Continue normal human verification."
        )

    for item in recommendations:
        st.markdown("- " + item)

    st.markdown("#### Human Review Guidance")

    if attempt_total >= 3 or final_score >= 60:
        st.warning(
            "Human assistance recommended due to onboarding friction. "
            "This does not determine KYC approval."
        )
    else:
        st.info(
            "Follow the normal verification workflow. "
            "A human reviewer remains responsible for decisions."
        )


    st.divider()

    from case_evidence import render_case_evidence
    render_case_evidence(name, CUSTOMERS[name])

    st.divider()
    st.subheader("Human Review Actions")
    st.caption(
        "Synthetic onboarding support only. "
        "Not a KYC approval or rejection."
    )

    from review_store import (
        add_review, history, current_status, STATUSES
    )

    st.info("Current status: " + current_status(name))

    with st.form("human_review_form"):
        review_status = st.selectbox(
            "Review Status",
            list(STATUSES),
            key="kyc_review_status"
        )
        review_note = st.text_area(
            "Review Note",
            max_chars=500
        )
        submitted = st.form_submit_button(
            "Save Review Action"
        )

    if submitted:
        try:
            add_review(name, review_status, review_note)
            st.success("Review action saved successfully.")
        except ValueError as error:
            st.error(str(error))

    st.markdown("#### Case Audit History")
    events = history(name)

    if events:
        st.dataframe(
            events,
            hide_index=True,
            use_container_width=True
        )
    else:
        st.caption("No review actions recorded yet.")


if selected_page == "Human Review Queue":
    from review_store import history, current_status

    st.subheader("Human Review Queue")
    st.caption(
        "Three synthetic demonstration customers. "
        "Review status refers to onboarding support only."
    )

    queue = []

    for case_name, record in CUSTOMERS.items():
        queue.append({
            "Customer": case_name,
            "Missing items": len(record["missing"]),
            "Upload attempts": record["attempts"],
            "Friction score": calculate_friction_score(
                len(record["missing"]),
                record["attempts"],
                record["error"]
            ),
            "Review status": current_status(case_name)
        })

    st.dataframe(
        queue,
        hide_index=True,
        use_container_width=True
    )

    st.subheader("Review Audit Log")
    audit = history()

    if audit:
        st.dataframe(
            audit,
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No review actions saved yet.")


if selected_page == "AI Intelligence":
    from ai_intelligence import render_ai_intelligence
    render_ai_intelligence()

