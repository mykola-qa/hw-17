from __future__ import annotations

import pytest
from drivers.sentry_uart import SentryUart

from tests.helpers import assert_error

pytestmark = [pytest.mark.v210, pytest.mark.usefixtures("firmware_only")]


@pytest.mark.parametrize(
    "command",
    ["guard status", "guard arm", "alert list", "alert test info"],
)
def test_future_features_report_planned(
    logged_in_dut: SentryUart, command: str
) -> None:
    assert_error(logged_in_dut.command(command), "E099")
