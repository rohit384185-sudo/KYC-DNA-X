import io
from contextlib import redirect_stdout
from kyc_engine import analyze_upload_friction, calculate_friction_score


def get_result(attempts, error):
    output = io.StringIO()

    with redirect_stdout(output):
        analyze_upload_friction(attempts, error)

    return output.getvalue()


result1 = get_result(4, "File too large")
assert "DOCUMENT SIZE ERROR" in result1
assert "OFFER HUMAN SUPPORT" in result1
print("TEST 1 PASSED: Repeated upload failure")


result2 = get_result(1, "File too large")
assert "DOCUMENT SIZE ERROR" in result2
assert "OFFER HUMAN SUPPORT" not in result2
print("TEST 2 PASSED: First upload failure")


result3 = get_result(2, "Unknown error")
assert "UNCLASSIFIED UPLOAD ERROR" in result3
print("TEST 3 PASSED: Unclassified error")

result4 = get_result(0, "None")
assert "NO UPLOAD ERROR RECORDED" in result4
assert "Check onboarding stage" in result4
print("TEST 4 PASSED: No recorded error")



try:
    calculate_friction_score(1, -2, "None")
    raise AssertionError("Negative attempts were accepted")
except ValueError as error:
    assert "Counts cannot be negative" in str(error)

print("TEST 5 PASSED: Negative input rejected")

print("ALL 5 TESTS PASSED")
