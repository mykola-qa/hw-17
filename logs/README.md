# Evidence logs

Save one text file here for every OTA transition and every bug reproduction. Replace the Wi-Fi password with `***`.

Required OTA evidence:

- `ota_2.1.0_to_2.3.0.txt`
- `ota_update_already_current.txt`
- `ota_install_2.1.0_blocked.txt`
- `ota_install_2.1.0_force.txt`
- `ota_broken_rollback.txt`
- `ota_drop.txt`
- `ota_slow_wifi_off.txt`
- `ota_garbage.txt`
- `ota_truncated.txt`
- `ota_corrupted.txt`
- `ota_server_default.txt`
- `pytest_2.3.0.txt` — `pytest -m "not ota"` on 2.3.0. Failed cases are marked `x FAIL` in the file.
- `pytest_2.3.0_summary.txt` — same run with `-v --tb=short`. Every test is listed PASSED, FAILED, or SKIPPED, and each failure includes the DUT (Device Under Test) text.
- `pytest_2.1.0_summary.txt` — `pytest -m "not ota and not v230" -v --tb=short` on 2.1.0.
