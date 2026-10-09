
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB = Path(__file__).resolve().parent / "kyc_reviews.sqlite3"

STATUSES = (
    "Needs follow-up",
    "Awaiting customer",
    "Resolved friction"
)

def connect():
    db = sqlite3.connect(str(DB), timeout=10)
    db.execute("""
        CREATE TABLE IF NOT EXISTS review_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT NOT NULL,
            status TEXT NOT NULL,
            note TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    db.commit()
    return db

def add_review(case_id, status, note):
    if not case_id or status not in STATUSES:
        raise ValueError("Invalid case or review status")

    note = str(note).strip()
    if not 1 <= len(note) <= 500:
        raise ValueError("Note must contain 1-500 characters")

    timestamp = datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    )

    with connect() as db:
        db.execute(
            """INSERT INTO review_events
               (case_id, status, note, created_at)
               VALUES (?, ?, ?, ?)""",
            (case_id, status, note, timestamp)
        )

def history(case_id=None):
    with connect() as db:
        db.row_factory = sqlite3.Row
        if case_id is None:
            rows = db.execute(
                "SELECT * FROM review_events ORDER BY id DESC"
            ).fetchall()
        else:
            rows = db.execute(
                """SELECT * FROM review_events
                   WHERE case_id=?
                   ORDER BY id DESC""",
                (case_id,)
            ).fetchall()
    return [dict(row) for row in rows]

def current_status(case_id):
    rows = history(case_id)
    return rows[0]["status"] if rows else "Not reviewed"
