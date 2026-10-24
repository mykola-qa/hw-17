from generate_report import build_report


def test_report_contains_failure_and_required_sections() -> None:
    report = build_report(
        {
            "created_utc": "2026-10-24T00:00:00+00:00",
            "expected_version": "2.3.0",
            "results": [
                {
                    "test": "tests/test_smoke.py::test_status",
                    "result": "failed",
                    "details": "expected NORMAL",
                }
            ],
        }
    )
    assert "BUG-001" in report
    assert "Bug matrix" in report
    assert "Security findings" in report
    assert "Conclusion" in report
