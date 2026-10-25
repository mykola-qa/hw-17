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
| OTA-1 boot banner | pass | reboot countdown 3-2-1; `fw v2.1.0`; `running v2.1.0 from ota_0`; `ready. state 1 NORMAL`; `last reset: software reboot` |
| WF-3 no auto-connect | pass | boot prints `known network 'lol_slow'. Type 'reconnect'` and does not connect |
| AU-1 profile after reboot | pass | boot prints `profile 'test_user' registered` |
| AC-1 E002 without Wi-Fi | pass | after reboot, `login`, `lamp status`, `relay status`, and `lamp scene load 3` return E002 |
| LM-1 off after reboot | pass | after login, beacon is off while color blue, 37%, and breathe remain |
| LM-7 settings after reboot | pass | scene 3 loads `(0,0,255)` 37% breathe |
| RL-2 persistence | pass | relay stays closed, auto on, cycles 124 |
| OTA-6 / OTA-7 beta update | pass | 2.1.0 on ota_0 downloads v2.3.0 to ota_1 in 3 s; self-check passes; running v2.3.0 from ota_1 |
| OTA-10 after 2.3.0 boot | pass | beacon off with blue, 37%, breathe saved; `lamp on` shows that pattern and the LED is blue; relay closed, auto on, cycles 124; health 30 s; calibration +0.0 cm, filter off, alarm on |
| LM-5 timer on 2.3.0 | pass | `auto-off in 10 s`; lamp off about 10 s later. BUG-001 does not reproduce |
| DS-7 on 2.3.0 | fail BUG-002 | continuous readings stay near 50 cm and then return many E701 no-echo lines. Not a new regression |
| GD-1 guard status | partial | disarmed, zone 50 cm, last distance -1.0 cm |
| GD-1 arm and disarm | pass | countdown reaches ARMED after 10 s; PIN 1234 disarms from ARMED |
| GD-2 intrusion | pass | hand at 11.5 cm raises INTRUSION and a 15 s disarm warning; PIN 1234 disarms from INTRUSION. The relay click was `[VALVE] OPEN (distance alarm)` because relay auto was still on |
| GD-3 alarm | pass | after 15 s without a PIN, GENERAL ALARM opens the valve as a critical alert and raises NORMAL to VERBOSE; PIN 1234 disarms the alarm and closes the valve. After disarm the LED blinks green and blue; the red/blue alarm color was not observed |
| AL-2 alert list | pass | 18 alerts, all unacknowledged; #18 is CRITICAL `GENERAL ALARM` |
| AL-3 / AL-4 acknowledge and clear | pass | `alert ack 18` acknowledges the critical alert; `alert ack all` acknowledges the other 17; `alert clear` leaves no alerts |
| OTA-3 / OTA-4 on 2.3.0 | pass | `ota check` reports running newer than stable; `ota update beta` prints `already up to date` and does not reboot |
| OTA-1 / OTA-2 on 2.3.0 | pass | `version` shows v2.3.0, partition ota_1 at 0x1a0000, valid; `ota status` shows previous v2.1.0 in ota_0 |
| OTA-5 blocked downgrade | pass | `ota install 2.1.0` returns E408 and does not reboot |
| OTA-5 forced downgrade | pass | `ota install 2.1.0 force` installs 2.1.0 on ota_0 in 9 s; self-check passes |
| OTA-10 after downgrade | pass | login works; beacon off, blue, 37%, breathe; relay closed, auto off, cycles 130; health 30 s; calibration +0.0 cm, filter off, alarm off |
| OTA-8 broken rollback | pass | v2.9.0-broken fails self-check and rolls back to v2.1.0 on ota_0; `version` is valid; `ota rollback` returns E417 |
| OTA-9 bad images | pass | garbage returns E406; truncated and corrupted return E412; `version` stays v2.1.0 valid |
| OTA-11 E418 | pass | `ota url ftp://...` returns `E418 url must start with http:// or https://` |
| OTA-9 drop | partial | server drops at 49%; device returns E410 after 40% and does not reboot |
| OTA-9 recovery after drop | pass | the following `ota update beta` installs v2.3.0 in 47 s under `--slow 20` and passes self-check. `disconnect` was not sent |
| OTA-12 server default | pass | server returns to the GitHub fw7 URL; `ota check` shows current 2.3.0, stable 2.1.0, beta 2.3.0, running newer than stable |
| GD-4 wrong PIN | pass | attempts 1/3 and 2/3 return E803; the third raises GENERAL ALARM, opens the relay, and moves NORMAL to VERBOSE. PIN 1234 disarms it and the relay clicks closed |
| K4 on 2.3.0 | pass | a short press acknowledges alert #3; a 1.5 s hold raises PANIC, opens the relay, and PIN 1234 closes it |
| GD-5 PIN change | pass | `guard pin 1234 5678` and `guard pin 5678 1234` both print `PIN changed`. The PIN is back to 1234. `guard log` keeps the last 10 events. Logout prints `stays ARMED after logout`, and `guard status` is still ARMED after the next login |
| WF-3 disconnect | pass | `disconnect` drops the link; `reconnect` joins `lol_slow` and gets 192.168.50.188 again |
| DS-3 calibrate | fail BUG-003 | `distance calibrate 20` sets offset +0.2 cm from a 19.8 cm measurement. `distance calibrate reset` returns E706, and stats still show calibration +0.2 cm |
| DS-6 no echo on 2.3.0 | pass | after several real echoes, one `distance` returns `E701 sonar: no echo` |
| DS-1 single distance | pass | single readings followed the hand, including 9.1 cm, 29.5 cm, and 138.3 cm |
| K3 press and second press | pass | 30 s pinging starts and then stops |
| K4 on 2.1.0 | pass | `E099 K4: perimeter watch is planned in v2.3.0` |
