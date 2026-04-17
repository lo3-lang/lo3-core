#!/usr/bin/env python3
"""
lo3-lang test runner
====================
Discovers and runs all suites under unit/ and syntax/, then prints a summary.

Usage:
    python test/run_tests.py

Requires the binary to be built first:
    cmake -S . -B build && cmake --build build
"""
import sys
import importlib.util
from pathlib import Path

TEST_ROOT = Path(__file__).parent
sys.path.insert(0, str(TEST_ROOT))

from common import BIN, BOLD, GREEN, RED, YELLOW, RESET, DIM, TestRunner


# ---------------------------------------------------------------------------
# Suite discovery
# ---------------------------------------------------------------------------
GROUPS: dict[str, Path] = {
    "Syntax": TEST_ROOT / "syntax",
    "Unit":   TEST_ROOT / "unit",
}


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def discover(folder: Path) -> list[tuple[str, object]]:
    """Return [(display_name, module), ...] for every test_*.py in folder."""
    if not folder.exists():
        return []
    return [
        (path.stem.replace("test_", "").replace("_", " ").title(), load_module(path))
        for path in sorted(folder.glob("test_*.py"))
    ]


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------
def bar(char: str = "─", w: int = 56) -> str:
    return char * w


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    if not BIN.exists():
        print(f"{RED}ERROR:{RESET} binary not found at {BIN}")
        print("Build first:  cmake -S . -B build && cmake --build build")
        return 1

    print(f"\n{BOLD}lo3-lang test suite{RESET}  {DIM}({BIN}){RESET}")

    all_runners: list[TestRunner] = []

    for group_name, folder in GROUPS.items():
        suites = discover(folder)
        if not suites:
            continue

        print(f"\n{BOLD}{bar('═')}{RESET}")
        print(f"{BOLD}  {group_name} Tests{RESET}")
        print(f"{BOLD}{bar('═')}{RESET}")

        for suite_label, module in suites:
            r = TestRunner(f"{group_name} › {suite_label}")
            print(f"\n{BOLD}  {suite_label}{RESET}")
            print(f"  {bar('·', 52)}")
            module.run(r)
            all_runners.append(r)

    # --- Summary ---
    total_passed = sum(r.passed for r in all_runners)
    total_failed = sum(r.failed for r in all_runners)
    grand_total  = total_passed + total_failed

    print(f"\n{BOLD}{bar('═')}{RESET}")
    print(f"{BOLD}  SUMMARY{RESET}")
    print(f"{BOLD}{bar('═')}{RESET}\n")

    for r in all_runners:
        icon    = f"{GREEN}✓{RESET}" if r.failed == 0 else f"{RED}✗{RESET}"
        detail  = f"{r.passed}/{r.total}"
        padding = " " * max(1, 36 - len(r.suite_name))
        print(f"  {icon}  {r.suite_name}{padding}{DIM}{detail}{RESET}")

    print(f"\n  {bar('─', 52)}")

    if total_failed == 0:
        verdict = f"{GREEN}{BOLD}{total_passed}/{grand_total} passed — all good!{RESET}"
    else:
        verdict = (
            f"{RED}{BOLD}{total_failed} failed{RESET}  "
            f"{DIM}({total_passed}/{grand_total} passed){RESET}"
        )
    print(f"\n  {verdict}")

    if total_failed:
        print(f"\n{BOLD}  Failed tests:{RESET}")
        for r in all_runners:
            if r.failed:
                print(f"\n  {YELLOW}{r.suite_name}{RESET}")
                r.print_failures()

    print(f"\n{BOLD}{bar('═')}{RESET}\n")
    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
