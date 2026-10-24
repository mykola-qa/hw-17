"""Generate a reviewable REPORT.md draft from the latest pytest results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def build_report(data: dict) -> str:
    version = data.get("expected_version") or "UNKNOWN"
    results = data.get("results", [])
    lines = [
        "# SENTRY SWM-2 acceptance report",
        "",
        f"Generated from UART run: `{data.get('created_utc', 'unknown')}`",
        f"Configured firmware: `{version}`",
        "",
        "## 1. Checklist",
        "",
        "Automated UART results:",
        "",
    ]
    for result in results:
        outcome = str(result.get("result", "unknown")).upper()
        lines.append(f"- [{outcome}] `{result.get('test', '')}`")
    if not results:
        lines.append("- No pytest results found.")

    failures = [item for item in results if item.get("result") == "failed"]
    lines.extend(
        [
            "",
            "Manual results must be added from `traceability.md`: buttons, LEDs,",
            "relay sound, measured distance, Wi-Fi interruption, and physical OTA",
            "behavior.",
            "",
            "## 2. Bug reports",
            "",
        ]
    )
    if failures:
        for index, failure in enumerate(failures, start=1):
            lines.extend(
                [
                    f"### BUG-{index:03d}: {failure.get('test', '')}",
                    "",
                    f"- Version: {version}",
                    "- Severity / priority: TODO",
                    "- Preconditions: TODO",
                    "- Steps: rerun the failing pytest node",
                    "- Expected: behavior required by the linked PRD item",
                    f"- Actual: `{failure.get('details', '').strip()}`",
                    "- Evidence: `artifacts/logs/pytest.log`",
                    "- Reproducibility: TODO/3",
                    "",
                ]
            )
    else:
        lines.append("No UART failures in this run. Add manually discovered bugs here.")

    lines.extend(
        [
            "",
            "## 3. Bug matrix",
            "",
            "- Add each bug and mark occurrence in 2.1.0 and 2.3.0.",
            "- Mark regressions explicitly.",
            "",
            "## 4. Security findings",
            "",
            "Exploratory hidden-command testing was excluded from this submission.",
            "",
            "## 5. Conclusion",
            "",
            "TODO: Decide whether 2.3.0 can move from beta to stable after both",
            "automated UART and manual physical checks are complete.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results",
        type=Path,
        default=ROOT / "artifacts" / "results.json",
    )
    parser.add_argument("--output", type=Path, default=ROOT / "REPORT.draft.md")
    args = parser.parse_args()
    data = json.loads(args.results.read_text(encoding="utf-8"))
    args.output.write_text(build_report(data), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
