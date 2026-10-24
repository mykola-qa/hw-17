# HW-17 checklist

This file stays in the git repository that is the hand-in. Record the result for every row on both firmware versions. `pass` and `fail BUG-xxx` are the report values. `pending` means not run yet. `n/a` means the PRD does not require that behavior on this version. An `E099` response on 2.1.0 for Guard, Alert center, or K4 is the expected result, not a bug.

Confirmed 2.1.0 results are already filled. Everything else is still open. Repeat every 2.1.0 row on 2.3.0 after the beta update.

## 1. Bring-up

| Check | PRD | 2.1.0 | 2.3.0 |
|---|---|---|---|
| Flash 2.1.0, boot shows `fw v2.1.0` and `ready. state 1 NORMAL` | OTA-1 | pending | n/a |
| `connect`: scan, saved network, IP, internet, NTP | WF-1 | pass | pending |
| Empty SSID returns E111 | WF-1 | pending | pending |
| Password shorter than 8 characters returns E112 | WF-1 | pending | pending |
| `register`, then login and `whoami` show `access: user` | AU-1, AU-2, AU-4 | pass | pending |

## 2. Wi-Fi and account

| Check | PRD | 2.1.0 | 2.3.0 |
|---|---|---|---|
| Wrong password E101, missing network E102, remaining documented connect errors | WF-2 | pending | pending |
| `reconnect`, `disconnect`, `forget`; no automatic connect at boot | WF-3 | partial: no automatic connect; `reconnect` passes | pending |
| `scan`, `net`, `ping`, `time`; `ping` also accepts a host | WF-4 | pending | pending |
| Link loss prints W110 and makes 3 reconnect attempts | WF-5 | pending | pending |
| Second `register` returns E202; bad login E204; bad password E205; login `debug` returns E203 | AU-1 | pending | pending |
| Account remains after reboot and OTA | AU-1, OTA-10 | pending | pending |
| Three bad logins lock the account for 30 s | AU-2 | pending | pending |
| `logout` turns the lamp and relay off and stops measurements | AU-3 | pass | pending |
| `passwd` persists through logout, reboot, and OTA | AU-5 | pending | pending |
| `sudo` with a wrong password returns E213 | AU-6 | pending | pending |

## 3. Access and states

| Check | PRD | 2.1.0 | 2.3.0 |
|---|---|---|---|
| `help` lists the 2.1.0 menu and its `[wifi]`, `[login]`, and `[debug]` marks | AC-1 | pass | pending |
| Unmarked commands work without login; `[wifi]` without Wi-Fi returns E002; `[login]` without a session returns E003 | AC-1 | partial: `lamp status` and `relay status` return E003 after logout | pending |
| Unknown command E001; first-word case does not matter; non-Latin text returns W006 | AC-2 | pending | pending |
| States 1, 2, 3 and their names; invalid state rejected | ST-1 | pending | pending |
| EMERGENCY is accepted only from VERBOSE, including the button pair | ST-2 | pass | pending |
| EMERGENCY allows only the documented commands; other commands return E005; buttons return E005 | ST-3 | partial: `lamp on` returns E005; `status` and `reboot` are allowed | pending |
| Current-state warning W303; logout returns to NORMAL; reboot returns to NORMAL | ST-4 | partial: W303 and reboot to NORMAL pass | pending |

## 4. Lamp

Physical color must match the log, not only the text.

| Check | PRD | 2.1.0 | 2.3.0 |
|---|---|---|---|
| `lamp on`, `lamp off`, repeated command W510; off after reboot and logout | LM-1 | partial: on/off and W510 pass | pending |
| Colors white, red, green, blue, yellow, purple, cyan | LM-2 | pass | pending |
| Color orange | LM-2 | pass | pending |
| RGB minimum 0, maximum 255, one below, one above | LM-2 | pending | pending |
| Unknown color E503 | LM-2 | pending | pending |
| Brightness 0, 100, -1, 101; brightness is visible in every mode. Boundary errors are automated | LM-3, LM-4 | pass | pending |
| Modes solid, blink, breathe, rainbow; invalid mode E505 is automated | LM-4 | pass | pending |
| Timer 1, 3600, 0, one below, one above; timer shown by `lamp status`. Boundary errors are automated | LM-5 | fail BUG-001 | pending |
| Scenes 1–3 save/load; bad number E508; empty scene E509 | LM-6 | pass | pending |
| `lamp status` matches the LED | LM-7 | pass: status stayed ON at 0% while the LED was dark | pending |
| LED priority while the beacon is off | LM-8 | pending | pending |
| Alias `beacon` performs the same action as `lamp` | LM | pass | pending |

## 5. Relay, sonar, health, buttons, system

| Check | PRD | 2.1.0 | 2.3.0 |
|---|---|---|---|
| Relay on/off/toggle, click, and diode; repeat command W601; rate limit E602 | RL-1 | pass | pending |
| Status, cycle counter, persistence | RL-2 | partial: closed, auto off, cycles 12 | pending |
| Pulse 100, 10000, 99, 10001 ms. Values 99 and 10001 are automated | RL-3 | pass | pending |
| Schedule 2, 3600, one below, one above; `schedule off`. Boundary results are automated | RL-4 | pass | pending |
| `relay auto` switches at the sonar alarm | RL-5 | pass | pending |
| `relay health` wear and coil state | RL-6 | pass | pending |
| Logout stops relay pulse and schedule | RL-7 | pass | pending |
| Aliases `valve on/off` and `valve open/close` match `relay` | RL | pass | pending |
| One distance reading and counts 1, 20, 0, 21. Repeated counts are automated | DS-1 | pass | pending |
| Distance log intervals 100, 5000, 99, 5001 ms; stop and busy errors | DS-2 | pending | pending |
| Calibration 5, 300, and reset | DS-3 | pending | pending |
| Alarm 5, 300, one below, one above; approach and clear. Boundary errors are automated | DS-4 | pass | pending |
| Filter, stats, and last 10 history entries | DS-5 | pass | pending |
| Collision below 20 cm and again after moving beyond 25 cm; no-echo E701 | DS-6 | partial: threshold and 25 cm re-arm pass | pending |
| Diode blinks faster as the object approaches while the relay is on | DS-7 | fail BUG-002 | pending |
| Alias `sonar` performs the same action as `distance` | DS | pass | pending |
| `health`, `health now`, `health on/off`; interval 10, 300, 9, 301, and report timing. Boundary errors are automated | HL-1, HL-3 | pass | pending |
| Alias `telemetry` performs the same action as `health` | HL | pass | pending |
| K1 short and 1.5 s hold | Buttons | pass | pending |
| K2 short and 1.5 s hold | Buttons | pass | pending |
| K3 starts and stops 30 s of measurements | Buttons | pass | pending |
| K4 on 2.1.0 returns E099; on 2.3.0 it acknowledges or raises panic | Buttons | pass: `E099` planned in v2.3.0 | pending |
| Button pairs select states 1–4 | Buttons, ST-2 | partial: NORMAL, DEBUG, and VERBOSE pass | pending |
| `help`, `status`, `sysinfo`, `temp`, `uptime`, reboot countdown and reset reason | System | pass | pending |

## 6. OTA

| Check | PRD | 2.1.0 | 2.3.0 |
|---|---|---|---|
| `version`, `ota`, `ota status`, `ota check` | OTA-1, OTA-2, OTA-3 | pending | pending |
| `ota update` on the version already running downloads nothing | OTA-4 | pending | pending |
| `ota update beta` goes 2.1.0 to 2.3.0, then self-check passes | OTA-6, OTA-7 | pending | n/a |
| Wi-Fi, account, lamp, relay, sonar, health, and Guard settings survive OTA | OTA-10 | pending | pending |
| `ota install 2.1.0` without force returns E408 | OTA-5 | n/a | pending |
| `ota install 2.1.0 force` installs and passes self-check | OTA-5 | n/a | pending |
| `ota broken` fails self-check and rolls back | OTA-8 | pending | pending |
| `ota rollback` boots the other partition; E416 when absent, E417 when invalid | OTA-8 | pending | pending |
| `--drop-at` returns E410; device stays usable and the next OTA works | OTA-9 | pending | pending |
| `--slow` plus Wi-Fi removed during download; device recovers | OTA-9 | pending | pending |
| `garbage.bin`, `truncated.bin`, `corrupted.bin`; device stays usable after each one | OTA-9, OTA-11 | pending | pending |
| `ota url` rejects a non-http(s) link with E418 | OTA-11 | pending | pending |
| Final `ota server default` restores the GitHub server | OTA-12 | pending | pending |

## 7. Firmware 2.3.0 additions

| Check | PRD | 2.1.0 | 2.3.0 |
|---|---|---|---|
| `guard`, `alert`, and their aliases `watch` and `cic` return E099 | GD, AL | pending | n/a |
| Guard arming, zone 10, 200, 9, 201, intrusion, and alarm | GD-1, GD-2, GD-3 | n/a | pending |
| Correct and wrong PIN, including the third-attempt alarm | GD-4 | n/a | pending |
| PIN change and guard log; logout does not disarm | GD-5 | n/a | pending |
| Alert list, acknowledge by id, acknowledge all, clear, and invalid level | AL-1–AL-4 | n/a | pending |
| CRITICAL alert turns the relay on and raises NORMAL or DEBUG to VERBOSE | AL-5 | n/a | pending |

## 8. Security bonus

Hidden commands are optional. Leave this section empty unless a finding is actually tested.

| Check | PRD | 2.1.0 | 2.3.0 |
|---|---|---|---|
| Hidden commands and secrets | HW-17 bonus | skipped | skipped |
