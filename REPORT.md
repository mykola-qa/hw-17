# SENTRY SWM-2 acceptance report

## 1. Checklist

The running checklist is [CHECKLIST.md](CHECKLIST.md). Copy its final tables here before sharing the repository link.

## 2. Bug reports

### BUG-001: Lamp timer log says milliseconds

- Version found: 2.1.0. Fixed on 2.3.0: the log says `auto-off in 10 s`, and the lamp turns off about 10 s later.
- Severity: Minor. Priority: Low.
- Preconditions: logged in, lamp ON.
- Steps: `lamp timer 10`.
- Expected: PRD LM-5, the log says `auto-off in 10 s`.
- Actual: the log says `auto-off in 10 ms`. The lamp still turns off after 10 seconds.
- Evidence: boot timestamps `1556847` to `1566847` are 10000 ms apart. The same 10-second interval occurred on the first run. The LED then showed the green NORMAL indicator.
- Reproducibility: 2/2.

### BUG-002: Continuous sonar stays near 50 cm

- Version found: 2.1.0. Reproduced on 2.3.0. Continuous readings again stay near 50.4–51.5 cm, with occasional other values and bursts of E701. A single reading in the same session was 131.9 cm.
- Severity: Major. Priority: High.
- Preconditions: logged in, valve open, hand moved in front of the sonar.
- Steps: `distance log 500`. Repeat with `distance filter off`.
- Expected: PRD DS-2 and DS-7, the distance follows the hand and the diode blinks faster as the hand approaches.
- Actual: readings stay near 50.2–51.0 cm with rare other values. The diode keeps blinking, and its rate does not change when the hand moves. `distance filter off` does not change this. Earlier single `distance` readings did follow the hand, from 9 cm to 138 cm.
- Evidence: `logs/manual_2.1.0_uart.txt` and the continuous-mode session.
- Reproducibility: 2/2 in continuous mode.

### BUG-003: `distance calibrate reset` is rejected

- Version found: 2.3.0. Reproduced on 2.1.0.
- Severity: Minor. Priority: Medium.
- Preconditions: logged in.
- Steps: `distance calibrate 20`, then `distance calibrate reset`.
- Expected: PRD DS-3, `distance calibrate reset` clears the offset.
- Actual: both versions return `E706 usage: distance calibrate <ref 5-300 cm>`. On 2.3.0, `distance stats` afterward still shows `calibration +0.2 cm`. On 2.1.0, calibration reports `measured 16.9 cm, offset +3.1 cm`. After E706, one reading still reports `calibration +3.1 cm`.
- Evidence: `logs/ota_server_default.txt` and `logs/manual_2.1.0_uart.txt`.
- Reproducibility: 1/1 on each version.

### BUG-004: `distance 20` is rejected

- Version found: 2.3.0. Reproduced on 2.1.0.
- Severity: Minor. Priority: Medium.
- Preconditions: logged in.
- Steps: `distance 20`.
- Expected: PRD DS-1, counts 1 through 20 are accepted and averaged. `21` returns E704.
- Actual: `distance 20` returns `E704 count must be 1-20`. On 2.3.0, `distance 1` printed `[SONAR] avg 130.7 cm`, and `distance 0` and `distance 21` returned E704.
- Evidence: `logs/pytest_2.3.0.txt` and `logs/pytest_2.1.0_summary.txt`, `test_distance_count_boundaries[20-None]`.
- Reproducibility: 1/1.

### BUG-005: `relay pulse 99` is not rejected

- Version found: 2.3.0. Reproduced on 2.1.0.
- Severity: Minor. Priority: Medium.
- Preconditions: logged in, relay off.
- Steps: `relay pulse 99`.
- Expected: PRD RL-3, a pulse below 100 ms returns `E603 pulse must be 100-10000 ms`.
- Actual: on 2.3.0, `relay pulse 99` prints `[VALVE] OPEN (pulse)` and `[VALVE] CLOSED (pulse end)` about 110 ms later. E603 is absent. `relay pulse 10001` returns `E603 pulse must be 100-10000 ms`. The 2.1.0 run fails the same assertion.
- Evidence: `logs/pytest_2.3.0.txt` and `logs/pytest_2.1.0_summary.txt`, `test_relay_pulse_rejects_outside_boundaries[99]`.
- Reproducibility: 1/1 on each version.

### BUG-006: `health interval 300` is rejected on 2.1.0

- Version found: 2.1.0. Passes on 2.3.0.
- Severity: Minor. Priority: Medium.
- Preconditions: logged in.
- Steps: `health interval 300`.
- Expected: PRD HL-3, 10 and 300 are included. `301` returns E902.
- Actual: `health interval 300` returns `E902 interval must be 10-300 s`. The message includes 300, and the command still rejects it.
- Evidence: `logs/pytest_2.1.0_summary.txt`, `test_health_interval_boundaries[300-None]`.
- Reproducibility: 1/1.

### BUG-007: `ota update` reinstalls the running stable version

- Version found: 2.1.0. On 2.3.0, `ota update beta` correctly prints `already up to date`. `ota update` while already on the stable version was not repeated there.
- Severity: Minor. Priority: Medium.
- Preconditions: logged in, running v2.1.0, stable channel is v2.1.0.
- Steps: `ota update`.
- Expected: PRD OTA-4, `[OTA] already up to date`. Nothing is downloaded and the device does not reboot.
- Actual: the device downloads v2.1.0 again, prints `W409 same version v2.1.0 - reinstalling`, reboots, and passes self-check from `ota_1`. Wi-Fi credentials and the account are still present after reboot.
- Evidence: `logs/ota_update_already_current.txt`.
- Reproducibility: 1/1.

### BUG-008: link loss stops after one reconnect attempt

- Version found: 2.3.0. Not yet checked on 2.1.0.
- Severity: Minor. Priority: Medium.
- Preconditions: logged in, connected to a phone hotspot, then the hotspot is switched off.
- Steps: turn the hotspot off and watch the console.
- Expected: PRD WF-5, `W110 wifi connection lost` and 3 automatic reconnect attempts.
- Actual: `W110 wifi connection lost (reason 1)` and `retry 1/3`. The first attempt fails authentication. `retry 2/3` and `retry 3/3` are not printed. About 80 s later, `status` still shows `link: buoy link down (known: Xiaomi 14T Pro)`. The login session stays open.
- Evidence: `logs/ota_2.1.0_to_2.3.0.txt`.
- Reproducibility: 1/1.

No other bugs recorded yet. For each new bug add:

- ID and title
- Version found, and whether the other version reproduces it
- Severity and priority
- Preconditions and steps
- Expected result with the PRD item
- Actual result
- Evidence: log excerpt, photo, or video
- Reproducibility, for example 3/3

## 3. Bug matrix

| Bug | 2.1.0 | 2.3.0 | Regression |
|---|---|---|---|
| BUG-001 lamp timer log says `ms` | fail | pass | no |
| BUG-002 continuous sonar sticks near 50 cm | fail | fail | no |
| BUG-003 `distance calibrate reset` rejected | fail | fail | no |
| BUG-004 `distance 20` returns E704 | fail | fail | no |
| BUG-005 `relay pulse 99` is not rejected | fail | fail | no |
| BUG-006 `health interval 300` returns E902 | fail | pass | no |
| BUG-007 `ota update` reinstalls the same stable version | fail | pass | no |
| BUG-008 link loss stops after one reconnect attempt | not tested | fail | no |

## 4. Security findings

Hidden-command exploration was not run.

## 5. Conclusion

Do not move 2.3.0 from beta to stable.

2.3.0 fixes the lamp-timer unit text (BUG-001) and the health-interval upper bound (BUG-006). Guard, the alert center, and K4 work. An update from 2.1.0 passes self-check, and Wi-Fi plus the account can survive it.

The beta still fails checks that 2.1.0 also fails. Continuous sonar stays near 50 cm (BUG-002). `distance calibrate reset` is rejected and the offset remains (BUG-003). `distance 20` is rejected (BUG-004). `relay pulse 99` is accepted (BUG-005). On 2.3.0, loss of the access point prints `W110` and only one of the three required reconnect attempts (BUG-008).

Hidden-command exploration was not run. Lamp color, relay clicks, and buttons were checked on 2.1.0 and were not repeated by eye on 2.3.0. `E203`, `E204`, and `E205` were checked on 2.3.0 only.

Product decision: do not mark 2.3.0 stable. A unit that needs Guard, alerts, or K4 may move from 2.1.0 to this beta. The timer text and the health-interval bound are fixed, and those features work. The sonar reading that sticks near 50 cm is already wrong on 2.1.0, so staying on 2.1.0 does not protect the fleet. The reason to hold the stable label is the link loss: after `W110` the buoy tries to reconnect once and then stays down. A device whose job is to stay on the network should not ship that as the release image.
