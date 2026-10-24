# SENTRY SWM-2 acceptance report

## 1. Checklist

The running checklist is [CHECKLIST.md](CHECKLIST.md). Copy its final tables here before sharing the repository link.

## 2. Bug reports

### BUG-001: Lamp timer log says milliseconds

- Version found: 2.1.0. Not yet checked on 2.3.0.
- Severity: Minor. Priority: Low.
- Preconditions: logged in, lamp ON.
- Steps: `lamp timer 10`.
- Expected: PRD LM-5, the log says `auto-off in 10 s`.
- Actual: the log says `auto-off in 10 ms`. The lamp still turns off after 10 seconds.
- Evidence: boot timestamps `1556847` to `1566847` are 10000 ms apart. The same 10-second interval occurred on the first run. The LED then showed the green NORMAL indicator.
- Reproducibility: 2/2.

### BUG-002: Continuous sonar stays near 50 cm

- Version found: 2.1.0. Not yet checked on 2.3.0.
- Severity: Major. Priority: High.
- Preconditions: logged in, valve open, hand moved in front of the sonar.
- Steps: `distance log 500`. Repeat with `distance filter off`.
- Expected: PRD DS-2 and DS-7, the distance follows the hand and the diode blinks faster as the hand approaches.
- Actual: readings stay near 50.2–51.0 cm with rare other values. The diode keeps blinking, and its rate does not change when the hand moves. `distance filter off` does not change this. Earlier single `distance` readings did follow the hand, from 9 cm to 138 cm.
- Evidence: `logs/manual_2.1.0_uart.txt` and the continuous-mode session.
- Reproducibility: 2/2 in continuous mode.

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
| BUG-001 lamp timer log says `ms` | fail | not tested | no |
| BUG-002 continuous sonar sticks near 50 cm | fail | not tested | no |

## 4. Security findings

Hidden-command exploration was not run.

## 5. Conclusion

Pending. Decide whether 2.3.0 can move from beta to stable only after both checklist columns are complete.
