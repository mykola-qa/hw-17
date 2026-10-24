# HW-17: SENTRY SWM-2 acceptance tests

Acceptance test repository for the SENTRY SWM-2 hydroacoustic watch module on an ESP32-S3. The DUT (Device Under Test) starts on firmware 2.1.0 from `sentry_fw7_v2.1.0_merged.bin`. Firmware 2.3.0 is installed later with `ota update beta`. Requirements are in the PRD (Product Requirements Document). Pass and fail are judged only against that document.

The hand-in is this git repository. Open the report first. Passwords in the logs are replaced with `***`.

## Start here

| Path | What it contains |
|---|---|
| [REPORT.md](REPORT.md) | Checklist copy, bug reports, bug matrix, security notes, and the release conclusion |
| [CHECKLIST.md](CHECKLIST.md) | Running pass/fail record for firmware 2.1.0 and 2.3.0 |
| [logs/](logs/) | UART evidence for OTA transitions and bug reproductions |
| [qa/README.md](qa/README.md) | Pytest setup and run order on the Raspberry Pi 5 |
| [PRD.md](PRD.md) | Firmware behavior under test |
| [HW-17.md](HW-17.md) | Original task text |
| [FLASH.md](FLASH.md) | How to flash firmware 2.1.0 |
| [WIRING.md](WIRING.md) | Pin table and bench wiring. Supply is 3.3 V only |
| [tools/README.md](tools/README.md) | Local OTA server used for download-failure cases |

## What is in this repository

`qa/` is the UART pytest harness: smoke, shared limits, version-specific checks, and selected OTA cases. Buttons, LED color, the relay diode, sonar distance, and a real Wi-Fi interruption are bench checks. Their results go into `REPORT.md` next to the automated results. `traceability.md` inside `qa/` maps each PRD item to an automated, mixed, or manual check.

Two findings are already written in the report: BUG-001, the lamp timer log says milliseconds, and BUG-002, continuous sonar stays near 50 cm. Both are confirmed on 2.1.0 and are still open on 2.3.0.
