# HW-17 acceptance tests

UART pytest suite for the SENTRY SWM-2 final acceptance run on Raspberry Pi 5.
The submission checklist is [`../CHECKLIST.md`](../CHECKLIST.md). Report sections are in
[`../REPORT.md`](../REPORT.md), and OTA evidence goes in [`../logs/`](../logs/).
Automated checks cover commands, boundaries, both firmware versions, persistence,
and OTA. Bench observations — buttons, LED, diode, relay, distance, and Wi-Fi
interruption — are recorded with the UART evidence in the final report.

## Prepare on Raspberry Pi 5

Tests run on the Pi. Keep the complete `hw_17` directory, because OTA tests use
`tools/ota_server.py` beside `qa/`.

```bash
cd ~/hw_17/qa
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp env/env.example env/.env
nano env/.env
pytest tests_unit
```

Edit `env/.env`, then flash firmware 2.1.0 and run `connect`,
`register <login> <password>`, and `login <login> <password>` once from a
serial terminal. Passwords are redacted from test commands and logs.

If UART access is denied:

```bash
sudo usermod -aG dialout "$USER"
```

Log out and back in after changing the group. This DUT (Device Under Test) uses
`SENTRY_PORT=/dev/ttyACM0`. Close serial terminals before flashing or pytest;
only one process may own the port.

## Flash 2.1.0

With the virtual environment active and the serial terminal closed:

```bash
cd ~/hw_17
python -m esptool --chip esp32s3 --port /dev/ttyACM0 erase-flash
python -m esptool --chip esp32s3 --port /dev/ttyACM0 -b 460800 write-flash 0x0 sentry_fw7_v2.1.0_merged.bin
```

`erase-flash` is required. Open a terminal at 115200 8N1, press RESET, and
confirm `fw v2.1.0` plus `ready. state 1 NORMAL (patrol)`. Firmware 2.3.0 is
installed later with `ota update beta`, not with esptool.

## Recommended run order

Every run verifies that the real firmware matches `SENTRY_VERSION` from
`env/.env`.

```bash
# Fast readiness check
pytest -m smoke

# Common UART behavior and limits
pytest -m common

# Version-specific checks
pytest -m v210                    # with SENTRY_VERSION=2.1.0
pytest -m v230                    # with SENTRY_VERSION=2.3.0
```

Do not run the entire OTA module blindly. OTA tests are stateful and must be
called by node ID after checking their docstrings and current firmware:

```bash
pytest -m ota -k check
pytest tests/test_ota.py::test_update_beta --run-destructive
```

After updating, change `SENTRY_VERSION` in `env/.env` before the next pytest
process. Test logs are in `artifacts/logs/pytest.log`; compact machine-readable
results are in `artifacts/results.json`.

Generate a starting report after each meaningful run:

```bash
python generate_report.py
```

This writes `REPORT.draft.md`. Merge results from both versions and your manual
checks into the final `REPORT.md`; do not submit the draft without reviewing it.

## Local OTA server

Use a second Pi terminal:

```bash
cd hw_17/tools
python3 ota_server.py --download          # once
python3 ota_server.py                     # normal mode
```

For error cases, stop the server and restart exactly one mode:

```bash
python3 ota_server.py --drop-at 50
python3 ota_server.py --slow 20
```

The OTA server runs in its own terminal, so the active failure mode stays
explicit. Verify the displayed LAN IP, set
`OTA_BASE_URL`, and make sure the ESP32 and Pi use the same Wi-Fi network.
Always finish with `ota server default`.

## Bench checks

Record K1-K4, LED and diode appearance, relay actuation, HC-SR04 distance,
Wi-Fi interruption, and visible behavior across reboot and OTA in the report
next to the automated results.

## Recovery

- Wrong version: fix `SENTRY_VERSION`; never bypass the version gate.
- Port busy: close the serial monitor and rerun.
- Login fails after reboot: run `reconnect` in a terminal, then rerun.
- OTA server unreachable: open `http://<PI-IP>:8000/fw7/stable.txt` from
  another device on the same LAN and check the Pi firewall.
- Interrupted run: return the DUT to NORMAL, stop distance logging/schedules,
  and run `pytest -m smoke` before continuing.

The hand-in is the git repository link. Before sharing it, put the reviewed
results in `REPORT.md` and the required evidence in `logs/`, and replace every
password with `***`.
