from __future__ import annotations

import re

ERROR_RE = re.compile(r"\bE\d{3}\b")


def assert_has(output: str, *parts: str) -> None:
    missing = [part for part in parts if part.lower() not in output.lower()]
    assert not missing, f"missing {missing}; output was:\n{output}"


def assert_error(output: str, code: str) -> None:
    assert re.search(rf"\b{re.escape(code)}\b", output), (
        f"expected {code}; output was:\n{output}"
    )


def assert_not_error(output: str, code: str) -> None:
    assert not re.search(rf"\b{re.escape(code)}\b", output), (
        f"did not expect {code}; output was:\n{output}"
    )


def assert_ok(output: str) -> None:
    match = ERROR_RE.search(output)
    assert match is None, f"unexpected {match.group(0)}; output was:\n{output}"
