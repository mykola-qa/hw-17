from __future__ import annotations

import pytest
from drivers.sentry_uart import SentryUart

from tests.helpers import assert_error, assert_has

pytestmark = pytest.mark.smoke


def test_version_matches_configuration(dut: SentryUart, expected_version: str) -> None:
    assert dut.version() == expected_version


def test_help_exposes_required_command_groups(dut: SentryUart) -> None:
    output = dut.command("help")
    assert_has(output, "state", "connect", "login", "ota", "lamp", "relay")
    assert_has(output, "distance", "health", "reboot")


def test_status_reports_core_state(dut: SentryUart, expected_version: str) -> None:
    output = dut.command("status")
    assert_has(output, expected_version, "NORMAL", "link")


def test_unknown_command_has_documented_error(dut: SentryUart) -> None:
    assert_error(dut.command("definitely_not_a_sentry_command"), "E001")


def test_login_access_gate_and_recovery(
    dut: SentryUart, credentials: tuple[str, str]
) -> None:
    dut.command("logout")
    assert_error(dut.command("lamp status"), "E003")
    output = dut.ensure_login(*credentials)
    assert_has(output, "login")
