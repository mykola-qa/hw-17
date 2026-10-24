from __future__ import annotations

import os

import pytest
from drivers.sentry_uart import SentryUart

from tests.helpers import assert_error, assert_has

pytestmark = pytest.mark.ota


def _base_url() -> str:
    value = os.getenv("OTA_BASE_URL", "").rstrip("/")
    if not value:
        pytest.fail("Set OTA_BASE_URL to the Pi ota_server.py address.")
    return value


def _assert_alive(dut: SentryUart, version: str) -> None:
    assert dut.version() == version
    assert_has(dut.command("status"), version)


def test_ota_status_and_check(logged_in_dut: SentryUart) -> None:
    assert_has(logged_in_dut.command("ota status"), "current", "ota_")
    assert_has(
        logged_in_dut.command("ota check", timeout=20, until=("beta",)),
        "stable",
        "beta",
    )


def test_custom_server_can_be_set_and_restored(
    logged_in_dut: SentryUart,
) -> None:
    server = f"{_base_url()}/fw7/"
    try:
        assert_has(logged_in_dut.command(f"ota server {server}"), server)
        assert_has(logged_in_dut.command("ota server"), server)
    finally:
        logged_in_dut.command("ota server default")


@pytest.mark.destructive
def test_update_beta(
    logged_in_dut: SentryUart,
    expected_version: str,
    credentials: tuple[str, str],
) -> None:
    """Run alone on 2.1.0; installs beta and checks UART-visible OTA-10 data."""
    if expected_version != "2.1.0":
        pytest.skip("beta transition starts on 2.1.0")
    logged_in_dut.command("lamp color blue")
    logged_in_dut.command("lamp brightness 37")
    logged_in_dut.command("lamp mode breathe")
    logged_in_dut.command("lamp scene save 1")
    logged_in_dut.command("relay auto on")
    logged_in_dut.command("health interval 47")
    output = logged_in_dut.run_rebooting(
        "ota update beta", "ready. state 1 NORMAL", timeout=240
    )
    assert_has(output, "success: v2.1.0 -> v2.3.0", "self-check passed")
    assert logged_in_dut.version() == "2.3.0"
    logged_in_dut.ensure_login(*credentials)
    lamp = logged_in_dut.command("lamp status")
    assert_has(lamp, "37%", "breathe")
    assert "(0,0,255)" in lamp.replace(" ", "")
    assert_has(logged_in_dut.command("relay status"), "auto", "on")
    assert_has(logged_in_dut.command("health"), "47")
    assert_has(logged_in_dut.command("whoami"), credentials[0])


def test_downgrade_without_force_is_blocked(
    logged_in_dut: SentryUart, expected_version: str
) -> None:
    if expected_version != "2.3.0":
        pytest.skip("downgrade protection is checked from 2.3.0")
    assert_error(logged_in_dut.command("ota install 2.1.0", timeout=20), "E408")
    _assert_alive(logged_in_dut, "2.3.0")


@pytest.mark.destructive
def test_forced_downgrade(logged_in_dut: SentryUart, expected_version: str) -> None:
    """Run alone on 2.3.0; installs 2.1.0 and reboots."""
    if expected_version != "2.3.0":
        pytest.skip("forced downgrade starts on 2.3.0")
    output = logged_in_dut.run_rebooting(
        "ota install 2.1.0 force", "ready. state 1 NORMAL", timeout=240
    )
    assert_has(output, "success: v2.3.0 -> v2.1.0", "self-check passed")
    assert logged_in_dut.version() == "2.1.0"


@pytest.mark.destructive
def test_broken_image_rolls_back(
    logged_in_dut: SentryUart, expected_version: str
) -> None:
    """Run alone; validates automatic rollback to the starting version."""
    output = logged_in_dut.run_rebooting(
        "ota broken", "ready. state 1 NORMAL", timeout=300
    )
    assert_has(output, "self-check FAILED", "Rolling back")
    _assert_alive(logged_in_dut, expected_version)


@pytest.mark.destructive
@pytest.mark.parametrize(
    ("filename", "accepted_errors"),
    [
        ("garbage.bin", ("E406",)),
        ("truncated.bin", ("E410", "E412")),
        ("corrupted.bin", ("E412",)),
    ],
)
def test_invalid_local_images_leave_firmware_usable(
    logged_in_dut: SentryUart,
    expected_version: str,
    filename: str,
    accepted_errors: tuple[str, ...],
) -> None:
    """Run with normal ota_server.py in a second terminal."""
    url = f"{_base_url()}/test/{filename}"
    output = logged_in_dut.command(
        f"ota url {url} force",
        timeout=120,
        until=accepted_errors,
    )
    assert any(code in output for code in accepted_errors), output
    _assert_alive(logged_in_dut, expected_version)


@pytest.mark.destructive
def test_dropped_download_leaves_firmware_usable(
    logged_in_dut: SentryUart, expected_version: str
) -> None:
    """Run only while ota_server.py --drop-at 50 is active."""
    version_path = f"v{expected_version}/sentry_fw7.bin"
    url = f"{_base_url()}/fw7/{version_path}"
    assert_error(
        logged_in_dut.command(
            f"ota url {url} force",
            timeout=120,
            until=("E410",),
        ),
        "E410",
    )
    _assert_alive(logged_in_dut, expected_version)
