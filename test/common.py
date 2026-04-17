"""
Shared helpers used by both unit/ and syntax/ test modules.
"""
import os
import sys
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent
BIN  = ROOT / "bin" / ("lo3.exe" if sys.platform == "win32" else "lo3")

_COLOR = sys.platform != "win32" or os.environ.get("TERM") == "xterm"
GREEN  = "\033[92m" if _COLOR else ""
RED    = "\033[91m" if _COLOR else ""
YELLOW = "\033[93m" if _COLOR else ""
BOLD   = "\033[1m"  if _COLOR else ""
DIM    = "\033[2m"  if _COLOR else ""
RESET  = "\033[0m"  if _COLOR else ""


class TestRunner:
    def __init__(self, suite_name: str):
        self.suite_name = suite_name
        self.passed = 0
        self.failed = 0
        self._failures: list[tuple[str, str]] = []

    @property
    def total(self) -> int:
        return self.passed + self.failed

    def check(self, name: str, condition: bool, detail: str = "") -> None:
        if condition:
            self.passed += 1
            print(f"  {GREEN}[PASS]{RESET} {name}")
        else:
            self.failed += 1
            self._failures.append((name, detail))
            suffix = f"  {DIM}→  {YELLOW}{detail}{RESET}" if detail else ""
            print(f"  {RED}[FAIL]{RESET} {name}{suffix}")

    def print_failures(self) -> None:
        for name, detail in self._failures:
            print(f"    {RED}✗{RESET} {name}")
            if detail:
                print(f"      {DIM}{detail}{RESET}")


def run_lo3(program: str, input_data: str = "") -> tuple[str, str, int]:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".lo3", delete=False, encoding="utf-8"
    ) as f:
        f.write(program)
        path = f.name
    try:
        result = subprocess.run(
            [str(BIN), path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout, result.stderr, result.returncode
    finally:
        os.unlink(path)


def run_with_ext(program: str, ext: str) -> tuple[str, str, int]:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=ext, delete=False, encoding="utf-8"
    ) as f:
        f.write(program)
        path = f.name
    try:
        result = subprocess.run(
            [str(BIN), path],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout, result.stderr, result.returncode
    finally:
        os.unlink(path)


def stdout_eq(stdout: str, expected: str) -> bool:
    return stdout.strip().replace("\r\n", "\n") == expected


def stdout_lines(stdout: str) -> list[str]:
    return stdout.strip().replace("\r\n", "\n").splitlines()
