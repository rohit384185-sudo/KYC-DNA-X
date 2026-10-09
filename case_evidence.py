
import json
from datetime import datetime, timezone

import streamlit as st

from kyc_engine import calculate_friction_score
from review_store import current_status


def build_case_evidence(name, customer):
    missing = list(customer["missing"])
    attempts = int(customer["attempts"])
    error = str(customer["error"])

    missing_points = len(missing) * 20
    retry_points = max(attempts - 1, 0) * 10
    error_points = 0 if error == "None" else 15

    score = calculate_friction_score(
        len(missing), attempts, error
    )

    codes = []
    actions = []

    if missing:
        codes.append("DOCUMENT_GAP")
        actions.append(
            "Request outstanding documents: "
            + ", ".join(missing)
        )

    if attempts >= 3:
        codes.append("REPEATED_UPLOAD_ATTEMPTS")
        actions.append(
            "Offer assisted upload and troubleshooting."
        )

    error_guidance = {
        "File too large": (
            "FILE_SIZE_ERROR",
            "Provide file-size and compression guidance."
        ),
        "Unreadable document": (
            "UNREADABLE_DOCUMENT",
            "Request a clearer document image."
        ),
        "Upload timeout": (
            "UPLOAD_TIMEOUT",
            "Offer connection and upload retry guidance."
        ),
        "Unsupported format": (
            "UNSUPPORTED_FILE_FORMAT",
            "Show accepted file-format instructions."
        )
    }

    if error in error_guidance:
        code, action = error_guidance[error]
        codes.append(code)
        actions.append(action)
    elif error != "None":
        codes.append("OTHER_UPLOAD_ERROR")
        actions.append("Investigate the recorded upload error.")

    if score >= 60:
        priority = "High support priority"
        codes.append("HIGH_FRICTION")
        actions.append(
            "Prioritize human onboarding assistance."
        )
    elif score >= 30:
        priority = "Medium support priority"
    else:
        priority = "Low support priority"

    if not actions:
        actions.append(
            "No immediate friction intervention indicated."
        )

    evidence = [
        {
            "Signal": "Missing requirements",
            "Recorded value": ", ".join(missing) if missing else "None",
            "Raw points": missing_points
        },
        {
            "Signal": "Upload attempts",
            "Recorded value": str(attempts),
            "Raw points": retry_points
        },
        {
            "Signal": "Upload error",
            "Recorded value": error,
            "Raw points": error_points
        }
    ]

    return {
        "case": name,
        "score": score,
        "raw_points": sum(
            item["Raw points"] for item in evidence
        ),
        "score_cap": 100,
        "priority": priority,
        "reason_codes": codes,
        "recommended_actions": actions,
        "evidence": evidence
    }


def render_case_evidence(name, customer):
    result = build_case_evidence(name, customer)

    st.divider()
    st.subheader("Case Investigation 2.0")
    st.caption(
        "Explainable evidence from fictional onboarding records. "
        "Support priority is not a fraud or KYC decision."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Friction Score", f'{result["score"]}/100')
    c2.metric("Evidence Signals", len(result["evidence"]))
    c3.metric("Reason Codes", len(result["reason_codes"]))

    st.markdown("#### Structured Evidence Ledger")
    st.dataframe(
        result["evidence"],
        hide_index=True,
        use_container_width=True
    )

    st.markdown("#### Support Priority")
    if result["score"] >= 60:
        st.warning(result["priority"])
    else:
        st.info(result["priority"])

    st.markdown("#### Reason Codes")
    if result["reason_codes"]:
        st.code(
            " | ".join(result["reason_codes"]),
            language=None
        )
    else:
        st.success("No friction reason codes triggered.")

    st.markdown("#### Suggested Resolution Plan")
    for index, action in enumerate(
        result["recommended_actions"], start=1
    ):
        st.write(f"{index}. {action}")

    report = dict(result)
    report["review_status"] = current_status(name)
    report["generated_at_utc"] = datetime.now(
        timezone.utc
    ).isoformat(timespec="seconds")
    report["data_classification"] = "Synthetic demo data"
    report["decision_scope"] = (
        "Onboarding friction assistance only"
    )

    st.download_button(
        "Download Case Evidence Report (JSON)",
        data=json.dumps(report, indent=2),
        file_name=f"kyc_case_{name.lower()}_evidence.json",
        mime="application/json",
        key=f"case_evidence_export_{name}"
    )


    from report_exports import (
        report_details, build_excel, build_pdf
    )
    from review_store import history

    report_data = report_details(
        name, result, current_status(name), history(name)
    )

    export_left, export_right = st.columns(2)

    with export_left:
        st.download_button(
            "Export Case Report - Excel",
            data=build_excel(report_data),
            file_name=f"kyc_case_{name.lower()}.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            key=f"excel_case_export_{name}"
        )

    with export_right:
        st.download_button(
            "Export Case Report - PDF",
            data=build_pdf(report_data),
            file_name=f"kyc_case_{name.lower()}.pdf",
            mime="application/pdf",
            key=f"pdf_case_export_{name}"
        )

