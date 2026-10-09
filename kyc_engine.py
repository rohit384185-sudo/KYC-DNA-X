def analyze_upload_friction(attempts, error):
    if error == "File too large":
        print("Friction: DOCUMENT SIZE ERROR")
        print("Action: Show approved file-size instructions")

        if attempts >= 3:
            print("Escalation: OFFER HUMAN SUPPORT")
    elif error in ("None", "", None):
        print("Friction: NO UPLOAD ERROR RECORDED")
        print("Action: Check onboarding stage and customer feedback")
    else:
        print("Friction: UNCLASSIFIED UPLOAD ERROR")
        print("Action: Investigate recorded error")


if __name__ == "__main__":
    print("KYC DNA - Demo")
    analyze_upload_friction(4, "File too large")


def calculate_friction_score(missing_count, attempts, error):
    if type(missing_count) is not int or type(attempts) is not int:
        raise ValueError("Counts must be integers")

    if missing_count < 0 or attempts < 0:
        raise ValueError("Counts cannot be negative")

    extra_attempts = max(attempts - 1, 0)
    score = (
        missing_count * 20
        + extra_attempts * 10
        + (15 if error != "None" else 0)
    )
    return min(score, 100)
