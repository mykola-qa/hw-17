from __future__ import annotations

import pytest
from drivers.sentry_uart import SentryUart

from tests.helpers import assert_error, assert_has, assert_not_error

pytestmark = pytest.mark.common


@pytest.mark.parametrize("state", ["1", "2", "3", "NORMAL", "DEBUG", "VERBOSE"])
def test_state_accepts_documented_values(logged_in_dut: SentryUart, state: str) -> None:
    output = logged_in_dut.command(f"state {state}")
    assert_not_error(output, "E301")


def test_state_rejects_invalid_value(logged_in_dut: SentryUart) -> None:
    assert_error(logged_in_dut.command("state 0"), "E301")
    assert_error(logged_in_dut.command("state 5"), "E301")


@pytest.mark.parametrize(
    ("value", "error"),
    [("-1", "E504"), ("0", None), ("100", None), ("101", "E504")],
)
def test_lamp_brightness_boundaries(
    logged_in_dut: SentryUart, value: str, error: str | None
) -> None:
    output = logged_in_dut.command(f"lamp brightness {value}")
    if error:
        assert_error(output, error)
    else:
        assert_not_error(output, "E504")


@pytest.mark.parametrize(
    ("rgb", "error"),
    [
        ("-1 0 0", "E502"),
        ("0 0 0", None),
        ("255 255 255", None),
        ("256 0 0", "E502"),
    ],
)
def test_lamp_rgb_boundaries(
    logged_in_dut: SentryUart, rgb: str, error: str | None
) -> None:
    output = logged_in_dut.command(f"lamp color {rgb}")
    assert_error(output, error) if error else assert_not_error(output, "E502")


def test_lamp_modes_and_invalid_mode(logged_in_dut: SentryUart) -> None:
    for mode in ("solid", "blink", "breathe", "rainbow"):
        assert_not_error(logged_in_dut.command(f"lamp mode {mode}"), "E505")
    assert_error(logged_in_dut.command("lamp mode invalid"), "E505")


@pytest.mark.parametrize(
    ("seconds", "error"),
    [("-1", "E506"), ("1", None), ("3600", None), ("3601", "E506")],
)
def test_lamp_timer_boundaries(
    logged_in_dut: SentryUart, seconds: str, error: str | None
) -> None:
    logged_in_dut.command("lamp on")
    output = logged_in_dut.command(f"lamp timer {seconds}")
    if error:
        assert_error(output, error)
    else:
        assert_not_error(output, "E506")
    logged_in_dut.command("lamp timer 0")


@pytest.mark.parametrize("milliseconds", ["99", "10001"])
def test_relay_pulse_rejects_outside_boundaries(
    logged_in_dut: SentryUart, milliseconds: str
) -> None:
    assert_error(logged_in_dut.command(f"relay pulse {milliseconds}"), "E603")


@pytest.mark.parametrize(
    ("on_s", "off_s", "valid"),
    [("1", "2", False), ("2", "2", True), ("3600", "3600", True), ("3601", "2", False)],
)
def test_relay_schedule_boundaries(
    logged_in_dut: SentryUart, on_s: str, off_s: str, valid: bool
) -> None:
    output = logged_in_dut.command(f"relay schedule {on_s} {off_s}")
    if valid:
        assert_not_error(output, "E606")
        logged_in_dut.command("relay schedule off")
    else:
        assert_error(output, "E606")


@pytest.mark.parametrize(
    ("count", "error"),
    [("0", "E704"), ("1", None), ("20", None), ("21", "E704")],
)
def test_distance_count_boundaries(
    logged_in_dut: SentryUart, count: str, error: str | None
) -> None:
    output = logged_in_dut.command(f"distance {count}", timeout=20)
    if error:
        assert_error(output, error)
    else:
        assert_not_error(output, "E704")


@pytest.mark.parametrize(
    ("interval", "error"),
    [("99", "E705"), ("100", None), ("5000", None), ("5001", "E705")],
)
def test_distance_log_interval_boundaries(
    logged_in_dut: SentryUart, interval: str, error: str | None
) -> None:
    output = logged_in_dut.command(f"distance log {interval}")
    if error:
        assert_error(output, error)
    else:
        assert_not_error(output, "E705")
        logged_in_dut.command("distance stop")


@pytest.mark.parametrize(
    ("threshold", "error"),
    [("4", "E708"), ("5", None), ("300", None), ("301", "E708")],
)
def test_distance_alarm_boundaries(
    logged_in_dut: SentryUart, threshold: str, error: str | None
) -> None:
    output = logged_in_dut.command(f"distance alarm {threshold}")
    assert_error(output, error) if error else assert_not_error(output, "E708")
    logged_in_dut.command("distance alarm off")


@pytest.mark.parametrize(
    ("interval", "error"),
    [("9", "E902"), ("10", None), ("300", None), ("301", "E902")],
)
def test_health_interval_boundaries(
    logged_in_dut: SentryUart, interval: str, error: str | None
) -> None:
    output = logged_in_dut.command(f"health interval {interval}")
    assert_error(output, error) if error else assert_not_error(output, "E902")
    logged_in_dut.command("health interval 30")


def test_network_status_commands(logged_in_dut: SentryUart) -> None:
    assert_has(logged_in_dut.command("net"), "IP", "MAC")
    assert_not_error(logged_in_dut.command("ping", timeout=15), "E105")
    assert_not_error(logged_in_dut.command("time"), "E121")


def test_reboot_returns_to_normal_and_keeps_account(
    logged_in_dut: SentryUart, credentials: tuple[str, str]
) -> None:
    logged_in_dut.command("state 3")
    boot = logged_in_dut.reboot()
    assert_has(boot, "ready. state 1 NORMAL")
    logged_in_dut.ensure_login(*credentials)
    assert_has(logged_in_dut.command("whoami"), credentials[0])
