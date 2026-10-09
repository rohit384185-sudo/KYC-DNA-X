import csv
from collections import Counter
from pathlib import Path


DATA_FILE = Path(__file__).with_name("synthetic_kyc_cases.csv")


def load_cases():
    with DATA_FILE.open(
        "r", encoding="utf-8", newline=""
    ) as file:
        rows = list(csv.DictReader(file))

    for row in rows:
        row["missing_requirements"] = int(
            row["missing_requirements"]
        )
        row["upload_attempts"] = int(
            row["upload_attempts"]
        )

    return rows


def calculate_overview(rows):
    total = len(rows)

    incomplete = sum(
        row["missing_requirements"] > 0
        for row in rows
    )

    extra_attempts = sum(
        max(row["upload_attempts"] - 1, 0)
        for row in rows
    )

    errors = Counter(
        row["error"]
        for row in rows
        if row["error"] != "None"
    )

    return {
        "total_cases": total,
        "incomplete_cases": incomplete,
        "extra_attempts": extra_attempts,
        "error_breakdown": dict(errors)
    }
