# HW-17 traceability

Legend:

- **UART automated** — asserted by pytest.
- **Mixed** — UART behavior is automated; physical or disruptive behavior is manual.
- **Manual** — checked on the bench and recorded in the report.

## Access, states, Wi-Fi, and account

- AC-1 — **UART automated (representative):** login gate and recovery in
  `test_smoke.py`; review all `help` access labels manually.
- AC-2 — **Mixed:** E001 is automated; case and non-Latin W006 are manual.
- ST-1, ST-4 — **UART automated:** states 1-3, aliases, invalid values, repeated
  transitions during the run, logout cleanup, and NORMAL after reboot.
- ST-2, ST-3 — **Manual:** EMERGENCY can heat/reboot the simulated driver and
  blocks the suite; execute as a controlled manual scenario.
- WF-1, WF-2 — **Manual:** interactive scan/SSID/password and network fault
  injection.
- WF-3 — **Mixed:** reconnect is used by fixtures; forget/disconnect and saved
  network behavior are manual.
- WF-4 — **UART automated:** `net`, default `ping`, and `time`.
- WF-5 — **Manual:** requires real Wi-Fi interruption.
- AU-1, AU-2, AU-5, AU-6 — **Manual:** registration, lockout, permanent password
  changes, and unknown sudo secret are unsafe suite prerequisites.
- AU-3, AU-4 — **UART automated:** logout/access gate and `whoami`.

## OTA

- OTA-1 to OTA-4 — **UART automated:** version/status/check and beta update.
- OTA-5 — **UART automated:** downgrade block and force downgrade are separate,
  explicitly destructive nodes.
- OTA-6, OTA-7 — **UART automated:** transition and self-check text are captured
  across the reboot.
- OTA-8 — **UART automated:** `ota broken` rollback is an explicit destructive
  node; manual rollback remains manual.
- OTA-9 — **Mixed:** drop, garbage, truncated, and corrupted-image outcomes are
  automated against a manually selected server mode. Slow download plus Wi-Fi
  removal is manual.
- OTA-10 — **Mixed:** account, lamp, relay-auto, and health persistence are
  asserted during beta update. Wi-Fi is exercised by reconnect; settings without
  a query command and Guard data are checked manually.
- OTA-11 — **UART automated:** local invalid-image URLs.
- OTA-12 — **UART automated:** custom server set/show/default.

## Lamp, relay, sonar, and telemetry

- LM-1 to LM-7 — **Mixed:** command parsing, RGB/brightness/mode/timer boundaries,
  status, and OTA-visible persistence are automated. Timer timing, scenes in
  detail, reboot/logout output state, and appearance are manual.
- LM-8 — **Manual:** LED priority is visual.
- RL-1 to RL-7 — **Mixed:** command/range checks and safe cleanup are automated.
  Relay click, diode, timing, wear counter, rapid switching, auto threshold, and
  logout/Guard physical behavior are manual.
- DS-1, DS-2, DS-4 — **Mixed:** count, interval, and alarm boundaries are
  automated; measurement correctness and threshold crossings are manual.
- DS-3, DS-5 to DS-7 — **Manual:** calibration, physical distance/history,
  collision hysteresis, no-echo behavior, and diode indication need a target or
  visual observation.
- HL-1 to HL-3 — **Mixed:** interval boundaries and health output are automated;
  report cadence and simulated warning conditions are manual.

## Firmware 2.3.0 and controls

- GD-1 to GD-5 — **Mixed:** status, zone boundaries, and PIN format are automated.
  Arming countdown, intrusion, alarm, wrong-PIN count, tamper, K4, relay, and LED
  behavior are manual.
- AL-1 to AL-4 — **UART automated:** create/list/acknowledge/clear and invalid
  levels; exact 20-entry retention and each ID variant are manual.
- AL-5 — **Mixed:** CRITICAL generation is automated; state/relay consequences
  are confirmed manually.
- Buttons section — **Manual:** no button stimulator is available.
- System section — **Mixed:** help/status/version/reboot are automated; detailed
  sysinfo fields and reset reasons are manual.
- Hidden commands/security bonus — **Excluded by user scope.**
