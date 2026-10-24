from __future__ import annotations

import logging

import drivers.sentry_uart as uart


class FakeSerial:
    def __init__(self, responses: dict[str, str]):
        self.responses = responses
        self.buffer = bytearray()
        self.is_open = True

    @property
    def in_waiting(self) -> int:
        return len(self.buffer)

    def write(self, data: bytes) -> int:
        command = data.decode().strip()
        self.buffer.extend(self.responses.get(command, "").encode())
        return len(data)

    def flush(self) -> None:
        pass

    def read(self, count: int) -> bytes:
        if not self.buffer:
            return b""
        data = bytes(self.buffer[:count])
        del self.buffer[:count]
        return data

    def close(self) -> None:
        self.is_open = False


def make_client(monkeypatch, responses: dict[str, str]) -> uart.SentryUart:
    monkeypatch.setattr(uart, "QUIET_S", 0)
    client = uart.SentryUart("FAKE")
    client.serial = FakeSerial(responses)  # type: ignore[assignment]
    monkeypatch.setattr(client, "drain", lambda _duration: "")
    return client


def test_clean_text_removes_terminal_noise() -> None:
    assert uart.clean_text(b"\x1b[31mready\r\n\x00") == "ready"


def test_redact_command_hides_credentials() -> None:
    assert uart.redact_command("login nick secret") == "login <redacted>"
    assert uart.redact_command("sudo secret") == "sudo <redacted>"
    assert uart.redact_command("version") == "version"


def test_redact_text_uses_environment(monkeypatch) -> None:
    monkeypatch.setenv("SENTRY_PASSWORD", "very-secret")
    assert uart.redact_text("echo very-secret") == "echo ***"


def test_command_and_version_parser(monkeypatch) -> None:
    client = make_client(
        monkeypatch,
        {"version": "version\r\nSENTRY SWM-2 sonar watch module, fw v2.1.0\r\n"},
    )
    assert client.version() == "2.1.0"


def test_password_is_absent_from_debug_log(monkeypatch, caplog) -> None:
    monkeypatch.setenv("SENTRY_PASSWORD", "very-secret")
    client = make_client(
        monkeypatch,
        {
            "login nick very-secret": "login nick very-secret\r\n[AUTH] login successful\r\n"
        },
    )
    caplog.set_level(logging.DEBUG)
    client.command("login nick very-secret")
    assert "very-secret" not in caplog.text
    assert "***" in caplog.text
