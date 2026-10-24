"""Fixtures, safety gates, and lightweight evidence output for HW-17."""

from __future__ import annotations

import json
import logging
import os
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from drivers.sentry_uart import SentryUart, find_port, load_env

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
RESULTS: list[dict[str, Any]] = []
logger = logging.getLogger(__name__)

load_env(Path(os.environ.get("HW17_ENV", ROOT / "env" / ".env")))


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-destructive",
        action="store_true",
        default=False,
        help="allow tests that replace firmware or persistent state",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    allow = (
        config.getoption("--run-destructive")
        or os.getenv("RUN_DESTRUCTIVE", "0") == "1"
    )
    skip = pytest.mark.skip(
        reason="destructive test; pass --run-destructive after reading its docstring"
    )
    if not allow:
        for item in items:
            if item.get_closest_marker("destructive"):
                item.add_marker(skip)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[Any]):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" and not (report.when == "setup" and report.skipped):
        return
    markers = sorted(marker.name for marker in item.iter_markers())
    RESULTS.append(
        {
            "test": item.nodeid,
            "result": report.outcome,
            "duration_s": round(report.duration, 3),
            "markers": markers,
            "details": str(report.longrepr) if report.failed else "",
        }
    )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> None:
    logger.info("=== START %s ===", item.nodeid)


@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item: pytest.Item) -> None:
    logger.info("=== END %s ===", item.nodeid)


def pytest_sessionfinish(
    session: pytest.Session, exitstatus: int | pytest.ExitCode
) -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    payload = {
        "created_utc": datetime.now(UTC).isoformat(),
        "expected_version": os.getenv("SENTRY_VERSION", ""),
        "exit_status": int(exitstatus),
        "results": RESULTS,
    }
    (ARTIFACTS / "results.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )


@pytest.fixture(scope="session")
def expected_version() -> str:
    value = os.getenv("SENTRY_VERSION", "").strip()
    if value not in {"2.1.0", "2.3.0"}:
        pytest.fail("Set SENTRY_VERSION=2.1.0 or 2.3.0 in .env.")
    return value


@pytest.fixture(scope="session")
def credentials() -> tuple[str, str]:
    username = os.getenv("SENTRY_USER", "").strip()
    password = os.getenv("SENTRY_PASSWORD", "")
    if not username or not password:
        pytest.fail("Set SENTRY_USER and SENTRY_PASSWORD in .env.")
    return username, password


@pytest.fixture(scope="session")
def dut(expected_version: str) -> Iterator[SentryUart]:
    port = find_port(os.getenv("SENTRY_PORT"))
    client = SentryUart(port)
    client.open()
    actual = client.version()
    if actual != expected_version:
        client.close()
        pytest.fail(f"DUT version is {actual}, but SENTRY_VERSION={expected_version}.")
    try:
        yield client
    finally:
        client.close()


@pytest.fixture
def logged_in_dut(
    dut: SentryUart, credentials: tuple[str, str]
) -> Iterator[SentryUart]:
    dut.ensure_login(*credentials)
    dut.command("state 1")
    yield dut
    # Best-effort safe logical baseline; physical behavior is checked manually.
    dut.command("distance stop")
    dut.command("relay schedule off")
    dut.command("relay off")
    dut.command("lamp off")
    dut.command("state 1")


@pytest.fixture
def firmware_only(request: pytest.FixtureRequest, expected_version: str) -> str:
    required = None
    if request.node.get_closest_marker("v210"):
        required = "2.1.0"
    elif request.node.get_closest_marker("v230"):
        required = "2.3.0"
    if required and expected_version != required:
        pytest.skip(f"requires firmware {required}")
    return expected_version
