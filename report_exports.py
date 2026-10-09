
import io
from datetime import datetime, timezone
from xml.sax.saxutils import escape

import xlsxwriter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)


def report_details(name, result, status, events):
    return {
        "customer": name,
        "score": result["score"],
        "priority": result["priority"],
        "status": status,
        "reason_codes": result["reason_codes"],
        "actions": result["recommended_actions"],
        "evidence": result["evidence"],
        "history": events,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(timespec="seconds")
    }


def build_excel(data):
    output = io.BytesIO()
    book = xlsxwriter.Workbook(
        output, {"in_memory": True}
    )

    header = book.add_format({
        "bold": True,
        "bg_color": "#13263C",
        "font_color": "#FFFFFF",
        "border": 0
    })
    title = book.add_format({
        "bold": True,
        "font_size": 16,
        "font_color": "#13263C"
    })
    normal = book.add_format({
        "text_wrap": True,
        "valign": "top"
    })

    def sheet_with_headers(name, labels):
        sheet = book.add_worksheet(name)
        sheet.freeze_panes(1, 0)
        sheet.set_column(0, 0, 27, normal)
        sheet.set_column(1, 5, 43, normal)
        sheet.write_row(0, 0, labels, header)
        sheet.autofilter(0, 0, 0, len(labels) - 1)
        return sheet

    summary = book.add_worksheet("Case Summary")
    summary.set_column("A:A", 28)
    summary.set_column("B:B", 57, normal)
    summary.write("A1", "KYC DNA X - Case Report", title)

    fields = [
        ("Customer", data["customer"]),
        ("Friction Score", data["score"]),
        ("Support Priority", data["priority"]),
        ("Review Status", data["status"]),
        ("Generated UTC", data["timestamp"]),
        ("Data Classification", "Synthetic demonstration"),
        ("Decision Scope", "Onboarding support only"),
        ("Reason Codes", ", ".join(data["reason_codes"]))
    ]
    for i, (key, value) in enumerate(fields, 2):
        summary.write(i, 0, key, header)
        summary.write(i, 1, value, normal)

    evidence = sheet_with_headers(
        "Evidence Ledger",
        ["Signal", "Recorded Value", "Raw Points"]
    )
    for i, item in enumerate(data["evidence"], 1):
        evidence.write_row(i, 0, [
            item["Signal"],
            item["Recorded value"],
            item["Raw points"]
        ])

    actions = sheet_with_headers(
        "Recommendations", ["Step", "Suggested Action"]
    )
    for i, action in enumerate(data["actions"], 1):
        actions.write_row(i, 0, [i, action])

    audit = sheet_with_headers(
        "Audit History",
        ["Event ID", "Customer", "Status", "Note", "UTC Timestamp"]
    )
    for i, event in enumerate(data["history"], 1):
        audit.write_row(i, 0, [
            event["id"],
            event["case_id"],
            event["status"],
            event["note"],
            event["created_at"]
        ])

    book.close()
    return output.getvalue()


def build_pdf(data):
    output = io.BytesIO()
    doc = SimpleDocTemplate(
        output, pagesize=A4,
        leftMargin=36, rightMargin=36,
        topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()
    story = []

    def paragraph(value, style="Normal"):
        return Paragraph(
            escape(str(value)),
            styles[style]
        )

    story.append(
        paragraph("KYC DNA X - Case Investigation", "Title")
    )
    story.append(Spacer(1, 12))
    story.append(paragraph(
        "Synthetic demonstration | Not a KYC approval or fraud decision"
    ))
    story.append(Spacer(1, 14))

    summary = [
        ["Field", "Value"],
        ["Customer", str(data["customer"])],
        ["Friction Score", str(data["score"]) + "/100"],
        ["Support Priority", str(data["priority"])],
        ["Review Status", str(data["status"])],
        ["Generated UTC", str(data["timestamp"])]
    ]

    def add_table(rows, widths):
        table = Table([
            [paragraph(cell) for cell in row]
            for row in rows
        ], colWidths=widths, repeatRows=1, hAlign="LEFT")
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCEAF3")),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8)
        ]))
        story.append(table)

    add_table(summary, [150, 350])
    story.append(Spacer(1, 18))
    story.append(paragraph("Evidence Ledger", "Heading2"))

    evidence_rows = [["Signal", "Recorded Value", "Points"]]
    for item in data["evidence"]:
        evidence_rows.append([
            item["Signal"],
            item["Recorded value"],
            str(item["Raw points"])
        ])
    add_table(evidence_rows, [150, 290, 60])

    story.append(Spacer(1, 18))
    story.append(paragraph("Reason Codes", "Heading2"))
    story.append(paragraph(
        ", ".join(data["reason_codes"]) or "None"
    ))

    story.append(Spacer(1, 12))
    story.append(paragraph("Recommended Actions", "Heading2"))
    for i, action in enumerate(data["actions"], 1):
        story.append(paragraph(f"{i}. {action}"))
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 12))
    story.append(paragraph("Review Audit History", "Heading2"))
    if data["history"]:
        for event in data["history"]:
            story.append(paragraph(
                f'{event["created_at"]} | '
                f'{event["status"]} | '
                f'{event["note"]}'
            ))
            story.append(Spacer(1, 6))
    else:
        story.append(paragraph("No recorded review actions."))

    doc.build(story)
    return output.getvalue()
