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

---

## Version 2 - Advanced Product Intelligence

### Product Intelligence Lab
- Reproducible what-if simulation of upload assistance and error resolution
- Baseline vs hypothetical support-priority comparison
- Root-cause analysis across onboarding stages and upload-error categories
- Operational metrics: error rates, repeat uploads, missing requirements and extra attempts

### Reviewer Operations & SLA
- Fictional case assignment to demonstration reviewers
- Configurable 24, 48 and 72-hour SLA windows
- Case aging, overdue detection and resolve/reopen lifecycle
- SQLite operational events with UTC timestamps
- Manager, Reviewer and Viewer role demonstrations

### Evidence-Grounded Case Copilot
- Rule-based generation of case-support summaries
- Editable draft and regenerate controls
- Human approval and revision workflow
- Saved summary decisions and audit events

### Important Limitations
- This prototype uses synthetic records only.
- Case Copilot is deterministic; no actual LLM is connected.
- Support-priority scores are not fraud scores or KYC decisions.
- Role selection is a UI demonstration, not authenticated authorization.
- Local SQLite is persistent on the developer machine but is not guaranteed durable on Streamlit Community Cloud.
- Multi-user production operation requires real identity verification, server-enforced permissions and managed persistent storage.
- Simulated friction improvements are hypothetical, not observed customer outcomes.

### Running Version 2
Install requirements and launch:

    python -m pip install -r requirements.txt
    python -m streamlit run app.py

Launch the application and select Product Intelligence, Reviewer Operations or Case Copilot in the sidebar.

