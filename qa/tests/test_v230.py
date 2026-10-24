from __future__ import annotations

import pytest
from drivers.sentry_uart import SentryUart

from tests.helpers import assert_error, assert_has, assert_not_error

pytestmark = [pytest.mark.v230, pytest.mark.usefixtures("firmware_only")]


@pytest.mark.parametrize(
    ("zone", "error"),
    [("9", "E808"), ("10", None), ("200", None), ("201", "E808")],
)
def test_guard_zone_boundaries(
    logged_in_dut: SentryUart, zone: str, error: str | None
) -> None:
    output = logged_in_dut.command(f"guard zone {zone}")
    assert_error(output, error) if error else assert_not_error(output, "E808")
    logged_in_dut.command("guard zone 50")


@pytest.mark.parametrize("pin", ["123", "12345", "abcd"])
def test_guard_pin_format_validation(logged_in_dut: SentryUart, pin: str) -> None:
    assert_error(logged_in_dut.command(f"guard pin 1234 {pin}"), "E804")


def test_guard_status_is_available(logged_in_dut: SentryUart) -> None:
    assert_has(logged_in_dut.command("guard status"), "guard", "zone")


@pytest.mark.parametrize("level", ["info", "warning", "critical"])
def test_alert_create_acknowledge_and_clear(
    logged_in_dut: SentryUart, level: str
) -> None:
    created = logged_in_dut.command(f"alert test {level}")
    assert_has(created, level)
    assert_not_error(logged_in_dut.command("alert ack"), "E851")
    listed = logged_in_dut.command("alert list")
    assert_has(listed, level)
    logged_in_dut.command("alert ack all")
    assert_not_error(logged_in_dut.command("alert clear"), "E855")


def test_invalid_alert_level(logged_in_dut: SentryUart) -> None:
    assert_error(logged_in_dut.command("alert test invalid"), "E854")
