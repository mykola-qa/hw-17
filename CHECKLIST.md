# HW-17 checklist

This file stays in the git repository that is the hand-in. Record the result for every row on both firmware versions. `pass` and `fail BUG-xxx` are finished results. `partial` means only part of the row was run. `pending` means that part was not run. `skipped` means the check was left out on purpose. `n/a` means the PRD does not require that behavior on this version. An `E099` response on 2.1.0 for Guard, Alert center, or K4 is the expected result, not a bug.

## 1. Bring-up

| Check | PRD | 2.1.0 | 2.3.0 |
|---|---|---|---|
| Flash 2.1.0, boot shows `fw v2.1.0` and `ready. state 1 NORMAL` | OTA-1 | pass | n/a |
| `connect`: scan, saved network, IP, internet, NTP | WF-1 | pass | pass: `connect` lists networks. `reconnect` gets an IP, internet, and NTP |
| Empty SSID returns E111 | WF-1 | pass | pass |
| Password shorter than 8 characters returns E112 | WF-1 | pass | pass |
| `register`, then login and `whoami` show `access: user` | AU-1, AU-2, AU-4 | pass | pass |

## 2. Wi-Fi and account

| Check | PRD | 2.1.0 | 2.3.0 |
|---|---|---|---|
| Wrong password E101, missing network E102, remaining documented connect errors | WF-2 | partial: E101 for a wrong password and E102 for a missing network. E103, E104, E105, W106, W107, and E108 were not run | partial: W106, NTP sync failed on the phone hotspot. E101 and E102 were not repeated |
| `reconnect`, `disconnect`, `forget`; no automatic connect at boot | WF-3 | partial: no automatic connect; `reconnect` passes | pass: `forget` clears the saved network and `reconnect` returns E113. `disconnect` and `reconnect` already passed. Boot does not connect by itself |
| `scan`, `net`, `ping`, `time`; `ping` also accepts a host | WF-4 | pass | pass |
| Link loss prints W110 and makes 3 reconnect attempts | WF-5 | pending | x fail BUG-008: W110 and retry 1/3 only. The link stayed down. A later `reconnect` succeeds after the hotspot is back |
| Second `register` returns E202; bad login E204; bad password E205; login `debug` returns E203 | AU-1 | partial: a second `register` returns E202. After logout, `login debug` returns E209. E203, E204, and E205 were not reached because a profile already exists | pass: with no profile, short login returns E204, a 5-character password returns E205, and `debug` returns E203. A second `register` returns E202 |
| Account remains after reboot and OTA | AU-1, OTA-10 | partial: login works after reboot and after OTA; Guard not checked | partial: login works after OTA onto 2.3.0 |
| Three bad logins lock the account for 30 s | AU-2 | pass: attempts 1/3, 2/3, 3/3, then E210 for 30 s. A login during the lock returns E207 | pass: attempts 1/3, 2/3, 3/3, then E210 for 30 s. A login during the lock returns E207 |
| `logout` turns the lamp and relay off and stops measurements | AU-3 | pass | partial: logout ends the session and `lamp status` returns E003. The lamp, relay, and measurements were already off |
| `passwd` persists through logout, reboot, and OTA | AU-5 | partial: a new password survives logout and the old one returns E209. Reboot and OTA were not repeated | partial: a 5-character new password returns E205. A password change was not repeated on 2.3.0 |
| `sudo` with a wrong password returns E213 | AU-6 | pass | pass |

## 3. Access and states

| Check | PRD | 2.1.0 | 2.3.0 |
|---|---|---|---|
| `help` lists the 2.1.0 menu and its `[wifi]`, `[login]`, and `[debug]` marks | AC-1 | pass | pass: the header lists all three marks. Guard, alert, `watch`, and `cic` are present |
| Unmarked commands work without login; `[wifi]` without Wi-Fi returns E002; `[login]` without a session returns E003 | AC-1 | pass | pass: `version`, `status`, and `sysinfo` work with no login. `net` without Wi-Fi returns E002. `lamp status` after logout returns E003 |
| Unknown command E001; first-word case does not matter; non-Latin text returns W006 | AC-2 | pass: `LAMP status` works, `привіт` returns W006, `test` returns E001 | pass: `LAMP status` works and non-Latin text returns W006. E001 passed in pytest |
| States 1, 2, 3 and their names; invalid state rejected | ST-1 | pass | pass |
| EMERGENCY is accepted only from VERBOSE, including the button pair | ST-2 | pass | pending |
| EMERGENCY allows only the documented commands; other commands return E005; buttons return E005 | ST-3 | partial: `lamp on` returns E005; `status` and `reboot` are allowed | pending |
| Current-state warning W303; logout returns to NORMAL; reboot returns to NORMAL | ST-4 | partial: W303 and reboot to NORMAL pass | partial: logout from VERBOSE returns to NORMAL; reboot returns to NORMAL and the account can log in |

## 4. Lamp

Physical color must match the log, not only the text.

| Check | PRD | 2.1.0 | 2.3.0 |
|---|---|---|---|
| `lamp on`, `lamp off`, repeated command W510; off after reboot and logout | LM-1 | pass | pending |
| Colors white, red, green, blue, yellow, purple, cyan | LM-2 | pass | pending |
| Color orange | LM-2 | pass | pending |
| RGB minimum 0, maximum 255, one below, one above | LM-2 | pass | pass |
| Unknown color E503 | LM-2 | pass | pass |
| Brightness 0, 100, -1, 101; brightness is visible in every mode. Boundary errors are automated | LM-3, LM-4 | pass | pass |
| Modes solid, blink, breathe, rainbow; invalid mode E505 is automated | LM-4 | pass | pass |
| Timer 1, 3600, 0, one below, one above; timer shown by `lamp status`. Boundary errors are automated | LM-5 | fail BUG-001 | pass |
| Scenes 1–3 save/load; bad number E508; empty scene E509 | LM-6 | pass | pending |
| `lamp status` matches the LED | LM-7 | pass: status stayed ON at 0% while the LED was dark | pending |
| LED priority while the beacon is off | LM-8 | partial: beacon off in NORMAL, the LED is green. EMERGENCY, OTA, sensor-error, and Guard priorities were not checked | partial: beacon off in NORMAL, the LED is green. The other priorities were not checked |
| Alias `beacon` performs the same action as `lamp` | LM | pass | pending |

## 5. Relay, sonar, health, buttons, system

| Check | PRD | 2.1.0 | 2.3.0 |
|---|---|---|---|
| Relay on/off/toggle, click, and diode; repeat command W601; rate limit E602 | RL-1 | pass | pending |
| Status, cycle counter, persistence | RL-2 | pass | pending |
| Pulse 100, 10000, 99, 10001 ms. Values 99 and 10001 are automated | RL-3 | x fail BUG-005: pulse 99 did not return E603 | x fail BUG-005: pulse 99 opened the valve |
| Schedule 2, 3600, one below, one above; `schedule off`. Boundary results are automated | RL-4 | pass | pass |
| `relay auto` switches at the sonar alarm | RL-5 | pass | pending |
| `relay health` wear and coil state | RL-6 | pass | pending |
| Logout stops relay pulse and schedule | RL-7 | pass | pending |
| Aliases `valve on/off` and `valve open/close` match `relay` | RL | pass | pending |
| One distance reading and counts 1, 20, 0, 21. Repeated counts are automated | DS-1 | x fail BUG-004: distance 20 returned E704 | x fail BUG-004: distance 20 returned E704 |
| Distance log intervals 100, 5000, 99, 5001 ms; stop and busy errors | DS-2 | pass | pass |
| Calibration 5, 300, and reset | DS-3 | x fail BUG-003: reset returned E706 and left calibration +3.1 cm | fail BUG-003 |
| Alarm 5, 300, one below, one above; approach and clear. Boundary errors are automated | DS-4 | pass | pass |
| Filter, stats, and last 10 history entries | DS-5 | pass | pending |
| Collision below 20 cm and again after moving beyond 25 cm; no-echo E701 | DS-6 | partial: threshold and 25 cm re-arm pass | partial: collision at 14.7 cm and 18.4 cm; one later reading returns E701. The 25 cm re-arm was not repeated |
| Diode blinks faster as the object approaches while the relay is on | DS-7 | fail BUG-002 | fail BUG-002 |
| Alias `sonar` performs the same action as `distance` | DS | pass | pending |
| `health`, `health now`, `health on/off`; interval 10, 300, 9, 301, and report timing. Boundary errors are automated | HL-1, HL-3 | x fail BUG-006: interval 300 returned E902 | pass |
| Alias `telemetry` performs the same action as `health` | HL | pass | pending |
| K1 short and 1.5 s hold | Buttons | pass | pending |
| K2 short and 1.5 s hold | Buttons | pass | pending |
| K3 starts and stops 30 s of measurements | Buttons | pass | pending |
| K4 on 2.1.0 returns E099; on 2.3.0 it acknowledges or raises panic | Buttons | pass: `E099` planned in v2.3.0 | pass |
| Button pairs select states 1–4 | Buttons, ST-2 | partial: NORMAL, DEBUG, and VERBOSE pass | pending |
| `help`, `status`, `sysinfo`, `temp`, `uptime`, reboot countdown and reset reason | System | pass | partial: `status`, `sysinfo`, `temp`, and `uptime` pass. Boot reports `last reset: software reboot`. The reboot countdown was not repeated |

## 6. OTA

| Check | PRD | 2.1.0 | 2.3.0 |
|---|---|---|---|
| `version`, `ota`, `ota status`, `ota check` | OTA-1, OTA-2, OTA-3 | partial: `ota check` shows current 2.1.0, stable 2.1.0, beta 2.3.0 | pass |
| `ota update` on the version already running downloads nothing | OTA-4 | x fail BUG-007: same version was downloaded, reinstalled, and the device rebooted | pass |
| `ota update beta` goes 2.1.0 to 2.3.0, then self-check passes | OTA-6, OTA-7 | pass | n/a |
| Wi-Fi, account, lamp, relay, sonar, health, and Guard settings survive OTA | OTA-10 | pass: network, account, lamp, scene 3, relay, sonar, and health survive. Guard had no saved settings on 2.1.0 | pass: downgrade keeps login, lamp, relay, health, calibration +0.0, filter off, and alarm off. Guard was still at its default zone |
| `ota install 2.1.0` without force returns E408 | OTA-5 | n/a | pass |
| `ota install 2.1.0 force` installs and passes self-check | OTA-5 | n/a | pass |
| `ota broken` fails self-check and rolls back | OTA-8 | pass | pending |
| `ota rollback` boots the other partition; E416 when absent, E417 when invalid | OTA-8 | pass: E417, previous image is invalid. E416 was not reached | pending |
| `--drop-at` returns E410; device stays usable and the next OTA works | OTA-9 | pass | pending |
| `--slow` plus Wi-Fi removed during download; device recovers | OTA-9 | partial: a 47 s download completed because `disconnect` was not sent | pending |
| `garbage.bin`, `truncated.bin`, `corrupted.bin`; device stays usable after each one | OTA-9, OTA-11 | pass | pending |
| `ota url` rejects a non-http(s) link with E418 | OTA-11 | pass | pending |
| Final `ota server default` restores the GitHub server | OTA-12 | n/a | pass |

## 7. Firmware 2.3.0 additions

| Check | PRD | 2.1.0 | 2.3.0 |
|---|---|---|---|
| `guard`, `alert`, and their aliases `watch` and `cic` return E099 | GD, AL | pass | n/a |
| Guard arming, zone 10, 200, 9, 201, intrusion, and alarm. Zone bounds are automated | GD-1, GD-2, GD-3 | n/a | pass |
| Correct and wrong PIN, including the third-attempt alarm | GD-4 | n/a | pass |
| PIN change and guard log; logout does not disarm | GD-5 | n/a | pass |
| Alert list, acknowledge by id, acknowledge all, clear, and invalid level. Invalid level is automated | AL-1–AL-4 | n/a | pass |
| CRITICAL alert turns the relay on and raises NORMAL or DEBUG to VERBOSE | AL-5 | n/a | pass: from NORMAL the relay opens and the state becomes VERBOSE |

## 8. Security bonus

Hidden commands are optional. Leave this section empty unless a finding is actually tested.

| Check | PRD | 2.1.0 | 2.3.0 |
|---|---|---|---|
| Hidden commands and secrets | HW-17 bonus | skipped | skipped |
