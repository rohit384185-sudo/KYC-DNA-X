
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

import streamlit as st

from customer_data import CUSTOMERS
from case_evidence import build_case_evidence
from review_store import DB

ROLES = ("Manager", "Reviewer", "Viewer")
ACTORS = ("Demo Reviewer A", "Demo Reviewer B")
DECISIONS = ("Approve", "Request revision")


def now_utc():
    return datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    )


@contextmanager
def database(path=None):
    db = sqlite3.connect(
        str(path if path is not None else DB),
        timeout=10
    )
    db.row_factory = sqlite3.Row

    try:
        db.execute("""
            CREATE TABLE IF NOT EXISTS copilot_drafts (
                case_id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                status TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                reviewed_by TEXT
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS copilot_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT NOT NULL,
                actor TEXT NOT NULL,
                role TEXT NOT NULL,
                action TEXT NOT NULL,
                note TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        db.commit()
        yield db
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def create_grounded_draft(name):
    if name not in CUSTOMERS:
        raise ValueError("Unknown demonstration customer.")

    evidence = build_case_evidence(
        name, CUSTOMERS[name]
    )

    record = CUSTOMERS[name]
    missing = (
        ", ".join(record["missing"])
        if record["missing"] else "None recorded"
    )

    codes = (
        ", ".join(evidence["reason_codes"])
        if evidence["reason_codes"]
        else "No friction reason codes"
    )

    actions = "\n".join(
        f"{index}. {action}"
        for index, action in enumerate(
            evidence["recommended_actions"], 1
        )
    )

    return (
        f"CASE SUPPORT SUMMARY - {name}\n"
        f"Data source: Fictional demonstration record\n"
        f"Friction score: {evidence['score']}/100\n"
        f"Support priority: {evidence['priority']}\n"
        f"Missing requirements: {missing}\n"
        f"Upload attempts: {record['attempts']}\n"
        f"Recorded upload error: {record['error']}\n"
        f"Reason codes: {codes}\n\n"
        f"Recommended support actions:\n{actions}\n\n"
        "Human reviewer must verify this draft before use. "
        "This does not establish identity authenticity, "
        "fraud risk, or KYC approval."
    )


def validate_actor(actor, role):
    if actor not in ACTORS or role not in ROLES:
        raise ValueError("Invalid demo identity or role.")


def get_draft(case_id, path=None):
    with database(path) as db:
        row = db.execute(
            "SELECT * FROM copilot_drafts WHERE case_id=?",
            (case_id,)
        ).fetchone()
        return dict(row) if row else None


def save_draft(case_id, content, actor, role,
               note, path=None):
    validate_actor(actor, role)

    if role == "Viewer":
        raise PermissionError("Demo Viewer is read-only.")

    if case_id not in CUSTOMERS:
        raise ValueError("Unknown case.")

    content = str(content).strip()
    note = str(note).strip()

    if not 20 <= len(content) <= 6000:
        raise ValueError(
            "Draft must contain 20-6000 characters."
        )
    if not 1 <= len(note) <= 500:
        raise ValueError(
            "Audit note must contain 1-500 characters."
        )

    timestamp = now_utc()

    with database(path) as db:
        db.execute("""
            INSERT INTO copilot_drafts
                (case_id, content, status,
                 updated_at, reviewed_by)
            VALUES (?, ?, 'Draft', ?, NULL)
            ON CONFLICT(case_id) DO UPDATE SET
                content=excluded.content,
                status='Draft',
                updated_at=excluded.updated_at,
                reviewed_by=NULL
        """, (case_id, content, timestamp))

        db.execute("""
            INSERT INTO copilot_audit
                (case_id,actor,role,action,note,timestamp)
            VALUES (?, ?, ?, 'Draft saved', ?, ?)
        """, (
            case_id, actor, role,
            note, timestamp
        ))


def review_draft(case_id, decision, actor, role,
                 note, path=None):
    validate_actor(actor, role)

    if role != "Manager":
        raise PermissionError(
            "Only demo Manager can review a draft."
        )

    if decision not in DECISIONS:
        raise ValueError("Invalid review decision.")

    note = str(note).strip()
    if not 1 <= len(note) <= 500:
        raise ValueError(
            "Review note must contain 1-500 characters."
        )

    with database(path) as db:
        current = db.execute("""
            SELECT status FROM copilot_drafts
            WHERE case_id=?
        """, (case_id,)).fetchone()

        if not current:
            raise ValueError("Save a draft first.")

        if current["status"] != "Draft":
            raise ValueError(
                "Only a Draft can be reviewed. "
                "Save a new draft to start another review."
            )

        new_status = (
            "Approved summary"
            if decision == "Approve"
            else "Revision requested"
        )

        timestamp = now_utc()

        db.execute("""
            UPDATE copilot_drafts
            SET status=?, reviewed_by=?, updated_at=?
            WHERE case_id=?
        """, (
            new_status, actor, timestamp, case_id
        ))

        db.execute("""
            INSERT INTO copilot_audit
                (case_id,actor,role,action,note,timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            case_id, actor, role,
            new_status, note, timestamp
        ))


def get_audit(case_id, path=None):
    with database(path) as db:
        rows = db.execute("""
            SELECT actor,role,action,note,timestamp
            FROM copilot_audit
            WHERE case_id=?
            ORDER BY id DESC
        """, (case_id,)).fetchall()

        return [dict(row) for row in rows]


def render_case_copilot():
    st.title("Case Copilot & Human Approval")

    st.caption(
        "Evidence-grounded draft assistant using "
        "transparent rules. No generative AI model "
        "is connected. All records are fictional."
    )

    first, second, third = st.columns(3)

    with first:
        name = st.selectbox(
            "Customer", list(CUSTOMERS),
            key="copilot_customer"
        )

    with second:
        role = st.selectbox(
            "Demo Role", ROLES,
            key="copilot_role"
        )

    with third:
        actor = st.selectbox(
            "Demo Actor", ACTORS,
            key="copilot_actor"
        )

    proposed = create_grounded_draft(name)
    existing = get_draft(name)

    st.subheader("Evidence-Grounded Summary")

    if existing:
        st.info(
            "Saved status: "
            + existing["status"]
        )
        default_text = existing["content"]
    else:
        st.caption(
            "No saved draft. Showing generated proposal."
        )
        default_text = proposed

    draft_key = f"copilot_editable_{name}"

    if draft_key not in st.session_state:
        st.session_state[draft_key] = default_text

    if st.button(
        "Generate / Regenerate Summary",
        key=f"copilot_generate_{name}"
    ):
        st.session_state[draft_key] = proposed
        st.success(
            "Fresh evidence-grounded summary generated. "
            "Review and save the draft below."
        )

    with st.form(
        f"copilot_draft_form_{name}"
    ):
        draft = st.text_area(
            "Editable case summary",
            key=draft_key,
            height=330,
            max_chars=6000
        )

        draft_note = st.text_input(
            "Audit note for draft changes",
            value="Evidence-grounded support summary"
        )

        save = st.form_submit_button(
            "Save / Update Draft"
        )

    if save:
        try:
            save_draft(
                name, draft, actor, role, draft_note
            )
            st.success("Draft saved.")
            st.rerun()

        except (ValueError, PermissionError) as exc:
            st.error(str(exc))

    st.divider()
    st.subheader("Human Review Decision")

    st.caption(
        "Summary approval is NOT customer KYC approval."
    )

    with st.form(
        f"copilot_review_form_{name}"
    ):
        decision = st.selectbox(
            "Decision", DECISIONS
        )

        review_note = st.text_input(
            "Reviewer justification",
            value=""
        )

        submit = st.form_submit_button(
            "Record Review Decision"
        )

    if submit:
        try:
            review_draft(
                name, decision, actor, role,
                review_note
            )
            st.success("Review decision recorded.")
            st.rerun()

        except (ValueError, PermissionError) as exc:
            st.error(str(exc))

    st.subheader("Case Copilot Audit History")

    events = get_audit(name)

    if events:
        st.dataframe(
            events, hide_index=True,
            use_container_width=True
        )
    else:
        st.caption(
            "No saved draft or review events yet."
        )

    st.warning(
        "Role selection is a demonstration, not "
        "verified authentication. Do not enter "
        "real customer or confidential information."
    )
