import csv
import random
from datetime import date, timedelta

random.seed(42)

stages = [
    "Registration",
    "PAN Verification",
    "Address Verification",
    "Bank Verification",
    "Human Review"
]

errors = [
    "None",
    "File too large",
    "Unsupported format",
    "Unreadable document",
    "Upload timeout"
]

rows = []

for i in range(1, 501):
    stage = random.choice(stages)
    error = random.choices(
        errors,
        weights=[55, 15, 10, 10, 10],
        k=1
    )[0]

    attempts = random.randint(1, 5)
    if error == "None":
        attempts = random.randint(0, 2)

    missing = random.randint(0, 3)

    rows.append({
        "case_id": f"KYC-{i:04d}",
        "stage": stage,
        "missing_requirements": missing,
        "upload_attempts": attempts,
        "error": error,
        "case_date": (
            date(2026, 9, 1)
            + timedelta(days=random.randint(0, 38))
        ).isoformat()
    })

with open("synthetic_kyc_cases.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("SUCCESS: 500 synthetic KYC cases generated.")
print("File: synthetic_kyc_cases.csv")
