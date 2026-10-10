
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone

import streamlit as st
from customer_data import CUSTOMERS
from review_store import DB, current_status

REVIEWERS = ("Demo Reviewer A", "Demo Reviewer B")
ROLES = ("Manager", "Reviewer", "Viewer")
SLA_HOURS = (24, 48, 72)

def utc_now():
    return datetime.now(timezone.utc)

def timestamp(value):
    return value.isoformat(timespec="seconds")

@contextmanager
def database(path=None):
    db = sqlite3.connect(
        str(path if path is not None else DB),
        timeout=10
    )
    db.row_factory = sqlite3.Row
    try:
        db.execute("""
            CREATE TABLE IF NOT EXISTS ops_tasks (
                case_id TEXT PRIMARY KEY,
                assignee TEXT NOT NULL,
                state TEXT NOT NULL,
                opened_at TEXT NOT NULL,
                due_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                resolved_at TEXT
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS ops_events (
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

def validate_note(note):
    note = str(note).strip()
    if not 1 <= len(note) <= 500:
        raise ValueError("Note must be 1-500 characters.")
    return note

def assign_case(case_id, assignee, hours, actor, role,
                note, path=None, now=None):
    if role != "Manager":
        raise PermissionError("Demo Manager role required.")
    if case_id not in CUSTOMERS:
        raise ValueError("Unknown demo case.")
    if assignee not in REVIEWERS or hours not in SLA_HOURS:
        raise ValueError("Invalid assignment settings.")
    note = validate_note(note)
    now = now or utc_now()
    due = now + timedelta(hours=hours)

    with database(path) as db:
        old = db.execute(
            "SELECT state FROM ops_tasks WHERE case_id=?",
            (case_id,)
        ).fetchone()
        if old and old["state"] == "Resolved":
            raise ValueError("Reopen resolved case first.")

        if old:
            db.execute("""
                UPDATE ops_tasks SET assignee=?, due_at=?,
                    updated_at=? WHERE case_id=?
            """, (
                assignee, timestamp(due),
                timestamp(now), case_id
            ))
            action = "Reassigned"
        else:
            db.execute("""
                INSERT INTO ops_tasks
                (case_id,assignee,state,opened_at,due_at,
                 updated_at,resolved_at)
                VALUES (?,?,'Assigned',?,?,?,NULL)
            """, (
                case_id, assignee, timestamp(now),
                timestamp(due), timestamp(now)
            ))
            action = "Assigned"

        db.execute("""
            INSERT INTO ops_events
            (case_id,actor,role,action,note,timestamp)
            VALUES (?,?,?,?,?,?)
        """, (
            case_id, actor, role, action,
            note, timestamp(now)
        ))

def transition_case(case_id, action, actor, role,
                    note, path=None, now=None):
    if action not in ("Resolve", "Reopen"):
        raise ValueError("Invalid action.")
    if role not in ROLES or role == "Viewer":
        raise PermissionError("Demo Viewer is read-only.")
    note = validate_note(note)
    now = now or utc_now()

    with database(path) as db:
        row = db.execute(
            "SELECT * FROM ops_tasks WHERE case_id=?",
            (case_id,)
        ).fetchone()
        if row is None:
            raise ValueError("Assign this case first.")

        if action == "Resolve":
            if row["state"] != "Assigned":
                raise ValueError("Case already resolved.")
            if role != "Manager" and actor != row["assignee"]:
                raise PermissionError(
                    "Reviewer can resolve only assigned case."
                )
            db.execute("""
                UPDATE ops_tasks
                SET state='Resolved',resolved_at=?,updated_at=?
                WHERE case_id=?
            """, (timestamp(now), timestamp(now), case_id))
        else:
            if role != "Manager":
                raise PermissionError("Manager role required.")
            if row["state"] != "Resolved":
                raise ValueError("Case must be resolved.")
            due = now + timedelta(hours=24)
            db.execute("""
                UPDATE ops_tasks
                SET state='Assigned',opened_at=?,due_at=?,
                    resolved_at=NULL,updated_at=?
                WHERE case_id=?
            """, (
                timestamp(now), timestamp(due),
                timestamp(now), case_id
            ))

        db.execute("""
            INSERT INTO ops_events
            (case_id,actor,role,action,note,timestamp)
            VALUES (?,?,?,?,?,?)
        """, (
            case_id, actor, role, action,
            note, timestamp(now)
        ))

def read_tasks(path=None, now=None):
    now = now or utc_now()
    with database(path) as db:
        records = [
            dict(row) for row in db.execute(
                "SELECT * FROM ops_tasks ORDER BY case_id"
            ).fetchall()
        ]

    items = []
    for row in records:
        opened = datetime.fromisoformat(row["opened_at"])
        due = datetime.fromisoformat(row["due_at"])
        active = row["state"] == "Assigned"
        age = max(0, (now - opened).total_seconds() / 3600)
        remaining = (due - now).total_seconds() / 3600

        items.append({
            "Case": row["case_id"],
            "Assignee": row["assignee"],
            "State": row["state"],
            "Age (hours)": round(age, 1),
            "SLA remaining (hours)": (
                round(remaining, 1) if active else None
            ),
            "SLA status": (
                "Overdue" if active and remaining < 0
                else "On track" if active else "Closed"
            ),
            "Due UTC": row["due_at"],
            "Resolved UTC": row["resolved_at"] or "-"
        })
    return items

def read_events(path=None):
    with database(path) as db:
        records = db.execute("""
            SELECT case_id,actor,role,action,note,timestamp
            FROM ops_events ORDER BY id DESC
        """).fetchall()
        return [dict(row) for row in records]

def render_reviewer_operations():
    st.title("Reviewer Operations & SLA")
    st.caption(
        "Fictional demo workflow. Role selector is NOT "
        "authentication; SQLite is local and cloud storage "
        "may be temporary."
    )

    left, right = st.columns(2)
    with left:
        role = st.selectbox(
            "Demonstration Role", ROLES,
            key="v2_ops_role"
        )
    with right:
        actor = st.selectbox(
            "Demonstration Actor", REVIEWERS,
            key="v2_ops_actor"
        )

    tasks = read_tasks()
    opened = sum(x["State"] == "Assigned" for x in tasks)
    overdue = sum(
        x["SLA status"] == "Overdue" for x in tasks
    )
    resolved = sum(x["State"] == "Resolved" for x in tasks)

    a, b, c, d = st.columns(4)
    a.metric("Open", opened)
    b.metric("Overdue", overdue)
    c.metric("Resolved", resolved)
    d.metric("Unassigned", len(CUSTOMERS) - len(tasks))

    st.subheader("Case Assignment & Aging")
    if tasks:
        st.dataframe(
            tasks, hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No assignments yet.")

    st.caption(
        "SLA starts when a case is first assigned. "
        "Reassignment updates the deadline. "
        "Reopening creates a new 24-hour SLA."
    )

    st.divider()
    st.subheader("Operational Actions")

    with st.form("v2_ops_form"):
        case_id = st.selectbox(
            "Customer", list(CUSTOMERS),
            key="v2_ops_case"
        )
        st.caption(
            "Existing review status: "
            + current_status(case_id)
        )
        assignee = st.selectbox(
            "Assignee", REVIEWERS,
            key="v2_ops_assignee"
        )
        hours = st.selectbox(
            "SLA hours", SLA_HOURS,
            key="v2_ops_sla"
        )
        action = st.selectbox(
            "Action",
            ("Assign / Reassign", "Resolve", "Reopen"),
            key="v2_ops_action"
        )
        note = st.text_area(
            "Required note", max_chars=500,
            key="v2_ops_note"
        )
        submit = st.form_submit_button("Save Action")

    if submit:
        try:
            if action == "Assign / Reassign":
                assign_case(
                    case_id, assignee, hours,
                    actor, role, note
                )
            else:
                transition_case(
                    case_id, action, actor, role, note
                )
            st.success("Action saved to local SQLite.")
            st.rerun()
        except (PermissionError, ValueError) as exc:
            st.error(str(exc))

    st.subheader("Operational Audit Log")
    events = read_events()
    if events:
        st.dataframe(
            events, hide_index=True,
            use_container_width=True
        )
    else:
        st.caption("No events recorded yet.")

    st.warning(
        "Role selection is a simulation, not secure access "
        "control. Do not enter real customer data."
    )
