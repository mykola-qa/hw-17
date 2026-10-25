# HW-17: SENTRY SWM-2 acceptance tests

Acceptance test repository for the SENTRY SWM-2 hydroacoustic watch module on an ESP32-S3. The DUT (Device Under Test) starts on firmware 2.1.0 from `sentry_fw7_v2.1.0_merged.bin`. Firmware 2.3.0 is installed later with `ota update beta`. Requirements are in the PRD (Product Requirements Document). Pass and fail are judged only against that document.

The hand-in is this git repository. Open the report first. Passwords in the logs are replaced with `***`.

## Start here

| Path | What it contains |
|---|---|
| [REPORT.md](REPORT.md) | Checklist copy, bug reports, bug matrix, security notes, and the release conclusion |
| [CHECKLIST.md](CHECKLIST.md) | Running pass/fail record for firmware 2.1.0 and 2.3.0 |
| [logs/](logs/) | UART evidence, plus `pytest_2.1.0_summary.txt` and `pytest_2.3.0_summary.txt` |
| [qa/README.md](qa/README.md) | Pytest setup and run order on the Raspberry Pi 5 |
| [PRD.md](PRD.md) | Firmware behavior under test |
| [HW-17.md](HW-17.md) | Original task text |
| [FLASH.md](FLASH.md) | How to flash firmware 2.1.0 |
| [WIRING.md](WIRING.md) | Pin table and bench wiring. Supply is 3.3 V only |
| [tools/README.md](tools/README.md) | Local OTA server used for download-failure cases |

## Pytest results

Firmware 2.1.0, `pytest -m "not ota and not v230"`: 3 failed, 50 passed, 22 deselected, 11:05. The failures are `relay pulse 99`, `distance 20`, and `health interval 300`. The log is [logs/pytest_2.1.0_summary.txt](logs/pytest_2.1.0_summary.txt).

Firmware 2.3.0, `pytest -m "not ota"`: 2 failed, 59 passed, 4 skipped, 10 deselected, 13:15. The failures are `relay pulse 99` and `distance 20`. The log is [logs/pytest_2.3.0_summary.txt](logs/pytest_2.3.0_summary.txt).

## What is in this repository

`qa/` is the UART pytest harness: smoke, shared limits, version-specific checks, and selected OTA cases. Buttons, LED color, the relay diode, sonar distance, and a real Wi-Fi interruption are bench checks. Their results go into `REPORT.md` next to the automated results. `traceability.md` inside `qa/` maps each PRD item to an automated, mixed, or manual check.
