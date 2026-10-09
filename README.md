# KYC DNA X

**Identity Friction Intelligence | Interactive FinTech Portfolio Prototype**

KYC DNA X is a Streamlit-based product prototype that demonstrates
how a financial-services team could investigate onboarding friction,
prioritize customer assistance and document human review activity.

**All records are synthetic. This is not a real identity verification,
fraud detection, compliance or KYC approval system.**

## Product problem

Customers may experience repeated uploads, missing documents,
unsupported file types and unclear next steps during onboarding.
These operational problems can create avoidable customer effort.

This prototype provides an explainable view of those friction signals
and a structured workflow for suggesting customer support actions.

## Functional workspaces

| Workspace | What it demonstrates |
| --- | --- |
| Executive Dashboard | Operational KPIs, priority distribution, review snapshot |
| Advanced Analytics | Interactive filters, chart customization, daily/weekly trends, CSV downloads |
| Human Review Queue | Review statuses, notes and timestamped SQLite audit events |
| AI Intelligence | Rule-based scenario simulator, 500-case cohort analysis, nine policy tests |
| Case Investigation | Explainable scores, evidence ledger, reason codes, recommendations, JSON/Excel/PDF exports |

## Demonstration dataset

- 500 fictional case records in `synthetic_kyc_cases.csv`
- 3 separate fictional customers in `customer_data.py`
- 5 onboarding stages
- Generated case dates, missing requirements, attempt counts and errors

The 500-case analytical dataset and the three-customer manual
review queue are intentionally separate. Results must not be
interpreted as measured industry performance.

## Explainable scoring

The friction score is calculated as:

```text
min(
    100,
    missing_requirements * 20
    + max(upload_attempts - 1, 0) * 10
    + (15 if recorded_error else 0)
)
```

The configured support-priority bands are:

- Low: 0-29
- Medium: 30-59
- High: 60-100

These are illustrative product rules, not validated risk thresholds.

## Run locally

Use a supported Python version with package wheels available
for your operating system.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

## Regression check

```bash
python test_kyc.py
```

The application also includes nine rule-conformance evaluation
scenarios displayed within the AI Intelligence workspace.

These checks do **not** measure real-world AI accuracy,
fraud-detection performance, precision or recall.

## Report exports

Case Investigation supports:

- JSON: structured technical evidence
- Excel: Case Summary, Evidence Ledger, Recommendations, Audit History
- PDF: readable case investigation summary

## Architecture

- Python and Streamlit: application and interactive interface
- Plotly: data visualizations
- CSV: synthetic operational dataset
- SQLite: demonstration human-review event history
- XlsxWriter and ReportLab: case report generation

## Deployment limitations

This is a demonstration application without user authentication,
role-based access controls or production data governance.

The SQLite review history is stored locally. On ephemeral hosting,
database changes may disappear when the app restarts or redeploys.
Different public users may also share the same demonstration state.

Use fictional data only. A production solution would require
secure authentication, authorization, persistent managed storage,
audit controls, privacy review, compliance assessment and testing.

## Suggested product roadmap

1. Connect anonymized operational events from an approved source.
2. Implement authenticated reviewer roles and case ownership.
3. Add secure, persistent workflow storage and review controls.
4. Validate support-priority rules with observed operational outcomes.
5. Conduct accessibility, performance and privacy testing.

## Portfolio focus

This project demonstrates product problem framing,
explainable rule design, data analytics, investigation workflows,
human-in-the-loop operations, evaluation and technical prototyping.
