"""Small UART client for the SENTRY SWM-2 command console."""

from __future__ import annotations

import logging
import os
import re
import time
from collections.abc import Iterable
from pathlib import Path

import serial
from serial.tools import list_ports

BAUD = 115200
POLL_S = 0.1
QUIET_S = 0.75
DEFAULT_TIMEOUT_S = 8.0
BOOT_TIMEOUT_S = 45.0

ANSI_RE = re.compile(
    r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07\x1b]*(?:\x07|\x1b\\)|[@-Z\\-_])"
)
CTRL_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")
VERSION_RE = re.compile(r"\bfw v(\d+\.\d+\.\d+)\b", re.IGNORECASE)
SECRET_COMMANDS = {"login", "register", "passwd", "sudo"}
KNOWN_VIDS = {0x10C4, 0x1A86, 0x0403, 0x303A}

logger = logging.getLogger(__name__)


class UartError(RuntimeError):
    """UART transport or protocol failure."""


def load_env(path: Path) -> None:
    """Load a simple KEY=VALUE file without overriding the process environment."""
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip("\"'")
        if key.strip() and value:
            os.environ.setdefault(key.strip(), value)


def clean_text(value: bytes | str) -> str:
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    return CTRL_RE.sub("", ANSI_RE.sub("", value)).replace("\r", "").strip()


def redact_command(command: str) -> str:
    parts = command.strip().split()
    if not parts:
        return "<Enter>"
    if parts[0].lower() in SECRET_COMMANDS:
        return f"{parts[0]} <redacted>"
    if parts[:2] == ["connect", "password"]:
        return "connect password <redacted>"
    return command


def redact_text(text: str) -> str:
    """Redact configured credentials while preserving text used by assertions."""
    redacted = text
    for key in ("SENTRY_PASSWORD", "WIFI_PASSWORD", "SENTRY_GUARD_PIN"):
        secret = os.getenv(key, "")
        if secret:
            redacted = redacted.replace(secret, "***")
    return redacted


def find_port(explicit: str | None = None) -> str:
    if explicit:
        return explicit
    ports = list(list_ports.comports())
    known = [port for port in ports if port.vid in KNOWN_VIDS]
    candidates = known or ports
    if not candidates:
        raise UartError("No serial ports found; set SENTRY_PORT explicitly.")
    if len(candidates) != 1:
        names = ", ".join(port.device for port in candidates)
        raise UartError(f"Multiple serial ports found ({names}); set SENTRY_PORT.")
    return candidates[0].device


class SentryUart:
    def __init__(self, port: str, timeout: float = POLL_S):
        self.port = port
        self.timeout = timeout
        self.serial: serial.Serial | None = None

    def open(self) -> None:
        try:
            self.serial = serial.Serial(
                self.port,
                BAUD,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.timeout,
            )
        except (OSError, serial.SerialException) as exc:
            raise UartError(f"Cannot open {self.port}: {exc}") from exc
        self.drain(1.0)

    def close(self) -> None:
        if self.serial is not None:
            try:
                self.serial.close()
            except (OSError, serial.SerialException):
                pass
        self.serial = None

    def command(
        self,
        text: str,
        *,
        timeout: float = DEFAULT_TIMEOUT_S,
        until: Iterable[str] = (),
    ) -> str:
        self.drain(0.3)
        logger.info("TX %s", redact_command(text))
        self._write(text)
        output = self._read_response(timeout, tuple(until))
        logger.debug("RX block\n%s", redact_text(output))
        return output

    def wait_for(self, *patterns: str, timeout: float) -> str:
        """Read until one requested substring appears, preserving the evidence."""
        if not patterns:
            raise ValueError("At least one pattern is required")
        deadline = time.monotonic() + timeout
        chunks: list[str] = []
        while time.monotonic() < deadline:
            chunk = self._read_available()
            if chunk:
                chunks.append(chunk)
                blob = clean_text("".join(chunks))
                if any(pattern in blob for pattern in patterns):
                    logger.debug("RX wait block\n%s", redact_text(blob))
                    return blob
            else:
                time.sleep(POLL_S)
        blob = clean_text("".join(chunks))
        raise TimeoutError(
            f"Timed out waiting for {patterns}; received: {redact_text(blob[-500:])}"
        )

    def reboot(self) -> str:
        return self.run_rebooting(
            "reboot", "ready. state 1 NORMAL", timeout=BOOT_TIMEOUT_S
        )

    def run_rebooting(self, text: str, *patterns: str, timeout: float) -> str:
        """Run a command that may temporarily remove the native USB UART."""
        if not patterns:
            raise ValueError("At least one completion pattern is required")
        self.drain(0.2)
        logger.info("TX %s", redact_command(text))
        self._write(text)
        deadline = time.monotonic() + timeout
        chunks: list[str] = []
        while time.monotonic() < deadline:
            try:
                chunk = self._read_available()
            except UartError:
                self.close()
                self._reconnect(deadline)
                continue
            if chunk:
                chunks.append(chunk)
                blob = clean_text("".join(chunks))
                if any(pattern in blob for pattern in patterns):
                    logger.debug("RX reboot block\n%s", redact_text(blob))
                    return blob
            else:
                time.sleep(POLL_S)
        blob = clean_text("".join(chunks))
        raise TimeoutError(
            f"Timed out waiting for {patterns}; received: {redact_text(blob[-1000:])}"
        )

    def version(self) -> str:
        output = self.command("version")
        match = VERSION_RE.search(output)
        if not match:
            raise AssertionError(f"Cannot parse firmware version from: {output}")
        return match.group(1)

    def ensure_login(self, username: str, password: str) -> str:
        output = self.command("whoami")
        if "user:" in output.lower():
            return output
        reconnect = self.command(
            "reconnect",
            timeout=20,
            until=(
                "connected to",
                "W114",
                "E113",
                "E101",
                "E102",
                "E104",
                "E105",
                "E108",
            ),
        )
        if "E113" in reconnect:
            raise AssertionError("No saved Wi-Fi network; complete connect manually.")
        output = self.command(f"login {username} {password}", timeout=20)
        if "E" in output and "[AUTH]" not in output:
            raise AssertionError(f"Login failed: {redact_text(output)}")
        return output

    def drain(self, duration: float) -> str:
        deadline = time.monotonic() + duration
        chunks: list[str] = []
        while time.monotonic() < deadline:
            chunk = self._read_available()
            if chunk:
                chunks.append(chunk)
            else:
                time.sleep(POLL_S)
        return clean_text("".join(chunks))

    def _read_response(self, timeout: float, until: tuple[str, ...]) -> str:
        deadline = time.monotonic() + timeout
        last_data = time.monotonic()
        saw_data = False
        chunks: list[str] = []
        matched = not until
        while time.monotonic() < deadline:
            chunk = self._read_available()
            if chunk:
                saw_data = True
                last_data = time.monotonic()
                chunks.append(chunk)
                blob = clean_text("".join(chunks))
                if until and any(item in blob for item in until):
                    matched = True
                continue
            if saw_data and matched and time.monotonic() - last_data >= QUIET_S:
                break
            time.sleep(POLL_S)
        output = clean_text("".join(chunks))
        if until and not matched:
            raise TimeoutError(
                f"{redact_command(' '.join(until))} not seen: "
                f"{redact_text(output[-500:])}"
            )
        return output

    def _write(self, text: str) -> None:
        serial_port = self._require_open()
        try:
            serial_port.write((text + "\r\n").encode())
            serial_port.flush()
        except (OSError, serial.SerialException) as exc:
            raise UartError(f"Write failed on {self.port}: {exc}") from exc

    def _reconnect(self, deadline: float) -> None:
        last_error: Exception | None = None
        while time.monotonic() < deadline:
            try:
                self.serial = serial.Serial(
                    self.port,
                    BAUD,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=self.timeout,
                )
                logger.info("Reopened %s after reboot", self.port)
                return
            except (OSError, serial.SerialException) as exc:
                last_error = exc
                time.sleep(0.2)
        raise UartError(f"Cannot reopen {self.port}: {last_error}")

    def _read_available(self) -> str:
        serial_port = self._require_open()
        try:
            data = serial_port.read(serial_port.in_waiting or 1)
        except (OSError, serial.SerialException) as exc:
            raise UartError(f"Read failed on {self.port}: {exc}") from exc
        return data.decode("utf-8", errors="replace") if data else ""

    def _require_open(self) -> serial.Serial:
        if self.serial is None or not self.serial.is_open:
            raise UartError(f"Serial port {self.port} is not open")
        return self.serial
