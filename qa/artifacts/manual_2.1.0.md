# Manual session — firmware 2.1.0

DUT (Device Under Test): ESP32-S3, `/dev/ttyACM0`, account `test_user`.

| Check | Result | Evidence |
|---|---|---|
| WF-1 connect | pass | IP 192.168.50.188, internet OK, NTP synced, network saved |
| AU-1 register | pass | profile `test_user` registered |
| AU-2 login | pass | operator `test_user` on watch |
| AU-4 whoami | pass | `user: test_user, access: user` |
| LM-1 lamp on | pass | solid, 50%, white `(255,255,255)`; LED white |
| LM-1 lamp off | pass | `[BEACON] off`; LED turned to the green state indicator |
| LM-1 lamp on again | pass | white beacon returned |
| LM-2 red | pass | `(255,0,0)`; LED red |
| LM-7 status while red | pass | ON, red, 50%, solid, timer off; LED still red |
| LM-2 green | pass | `(0,255,0)`; LED green |
| LM-2 blue | pass | `(0,0,255)`; LED blue |
| LM-2 yellow | pass | `(255,180,0)`; LED yellow |
| LM-2 purple | pass | `(160,0,255)`; LED purple |
| LM-2 cyan | pass | `(0,255,255)`; LED cyan |
| LM-2 orange | pass | `(255,80,0)`; LED orange |
| LM-4 blink | pass | `[BEACON] mode: blink`; LED blinks |
| LM-4 breathe | pass | `[BEACON] mode: breathe`; LED breathes |
| LM-4 rainbow | pass | `[BEACON] mode: rainbow`; color cycle visible |
| LM-3 brightness 10 | pass | `[BEACON] brightness: 10%`; LED visibly dimmer during rainbow |
| LM-3 brightness 100 | pass | `[BEACON] brightness: 100%`; LED visibly brighter |
| LM-3 brightness 0 | pass, visual ambiguous | `[BEACON] brightness: 0%`; LED dark, on and off cannot be distinguished by eye |
| LM-7 status at 0% | pass | ON, color `(255,80,0)`, brightness 0%, mode rainbow, timer off |
| LM-3 brightness restored to 50 | pass | `[BEACON] brightness: 50%`; LED lit again |
| LM-5 timer 10 | fail BUG-001 | log says `auto-off in 10 ms`, but the lamp turns off after 10 s; repeated 2/2; LED then green |
| LM-1 repeated on | pass | `W510 lamp already on` |
| LM-6 scene 1 | pass | saved red 80% solid; blue blink changed back to red solid, confirmed by eye |
| LM-6 scenes 2–4 | pass | scene 2 restored red 80% solid; empty scene 3 returned E509; scene 4 returned E508 |
| RL-1 on/off/toggle | pass | `[VALVE] OPEN`, `CLOSED`, `OPEN`; click each time; relay LED followed the state |
| RL-1 repeated on | pass | `W601 relay already on` |
| RL-2 status | pass | `closed, auto off, cycles 12` |
| RL-3 pulse 1000 | pass | OPEN to CLOSED in about 1020 ms; clicks and about 1 s delay |
| RL-3 pulse 100 and 10000 | pass | about 120 ms and 10020 ms; user confirmed the timings |
| RL-1 rate limit | pass | third rapid toggle returned `E602 relay switching too fast (max 2 per second)` |
| DS-6 collision threshold | pass | 22.0 cm and 17.7 cm show the 20 cm edge |
| DS-6 hysteresis | pass | 9.1 cm warns once; 12.9 cm does not repeat it; after 29.5 cm, 17.3 cm warns again |
| K1 short | pass | short press toggles the beacon off and on |
| K1 hold | pass | long press cycles red, green, blue, yellow, purple, cyan |
| K2 short | pass | valve OPEN and later CLOSED |
| K2 hold | pass | 1 s pulse, OPEN to CLOSED in about 1020 ms |
| K1+K2 | pass | `W303 already in 1 NORMAL` |
| K2+K3 | pass | NORMAL to DEBUG |
| K3+K4 | pass | DEBUG to VERBOSE |
| K4+K1 | pass | VERBOSE to EMERGENCY; module locked |
| ST-3 blocked command | pass | `lamp on` returns E005; driver temperature rises 31.7 C to 40.6 C |
| ST-3 allowed status | pass | status shows v2.1.0 and state 4 EMERGENCY |
| ST-4 reboot | pass | software reboot returns to `ready. state 1 NORMAL`; account and saved network remain |
| WF-3 reconnect | pass | reconnect joins `lol_slow`, gets an IP, and confirms internet |
| ST-2 command guard | pass | `state 4` from NORMAL returns E302 |
| AU-3 logout | pass | beacon off, valve closed with a click; LED returned to the green NORMAL indicator; both status commands return E003 |
| Aliases | pass | `beacon on`, `valve open/close`, `sonar` 138.3 cm, and `telemetry now` all work |
| DS-4 alarm | pass | 37.6 cm raises the 50 cm alarm; 136.6 cm clears it |
| HL-1 interval | pass | telemetry numbers 8 through 14 arrive every 30 s |
| DS-7 continuous sonar | fail BUG-002 | with and without the median filter, continuous readings stay near 50 cm; the diode keeps blinking at the same rate regardless of hand position |
| RL-4 schedule 2 2 | pass | on and off intervals are about 2000 ms; `schedule stopped`; relay clicked |
| RL-5 relay auto | pass | 29.5 cm raised the proximity alarm and opened the valve; the relay clicked |
| RL-6 relay health | pass | seal 110 / 100000 cycles, wear 0.11% (good); solenoid OK, 45 mOhm |
| RL-7 logout during schedule | pass | schedule was cycling every 2 s; logout printed `[VALVE] CLOSED (logout)`; the relay did not keep clicking |
| DS-5 stats and history | pass | 662 measurements, 1 error, min 3.8 cm, max 138.3 cm, avg 43.2 cm; filter off, alarm on; history lists 10 entries |
| HL-3 health commands | pass | auto on at 30 s; `health now` prints a report; `health off` and `health on` are accepted |
| System status | pass | `status` shows v2.1.0 on ota_0, NORMAL, `lol_slow`, `test_user`, valve closed; `sysinfo`, `temp`, and `uptime` respond |
| DS-1 single distance | pass | single readings followed the hand, including 9.1 cm, 29.5 cm, and 138.3 cm |
| K3 press and second press | pass | 30 s pinging starts and then stops |
| K4 on 2.1.0 | pass | `E099 K4: perimeter watch is planned in v2.3.0` |
