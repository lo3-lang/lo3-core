#!/usr/bin/env python3
# Copyright (c) 2026 seesee010
# Master test runner: Rust unit tests + C unit test (test_parsing) + syntax tests.

import os
import shutil
import subprocess
import sys

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT   = os.path.dirname(SCRIPT_DIR)
BUILD_DIR   = os.path.join(REPO_ROOT, "build_test")
RUST_DIR    = os.path.join(SCRIPT_DIR, "unit", "rust")
SYNTAX_RUNNER = os.path.join(SCRIPT_DIR, "syntax", "run_syntax_tests.py")


def section(title):
    print(f"\n{'='*60}\n  {title}\n{'='*60}")


def run(cmd, **kwargs):
    print(f"  $ {' '.join(cmd)}")
    return subprocess.run(cmd, **kwargs)


def run_rust_unit_tests():
    section("UNIT TESTS — Rust (var / global / control-flow / execute / warnings)")

    if shutil.which("cargo") is None:
        print("  cargo not found — SKIPPING Rust unit tests")
        return "SKIP (cargo not found)"

    r = run(["cargo", "test"], cwd=RUST_DIR)
    return "PASS" if r.returncode == 0 else "FAIL"


def run_c_unit_tests():
    section("UNIT TESTS — C/Unity (test_parsing)")

    missing = [tool for tool in ("cmake", "ctest") if shutil.which(tool) is None]
    if missing:
        print(f"  {'/'.join(missing)} not found — SKIPPING C unit tests")
        return f"SKIP ({'/'.join(missing)} not found)"

    r = run(["cmake", "-B", BUILD_DIR, "-S", REPO_ROOT, "-DCMAKE_BUILD_TYPE=Debug"])
    if r.returncode != 0:
        print("ERROR: cmake configure failed")
        return "FAIL"

    r = run(["cmake", "--build", BUILD_DIR, "--parallel"])
    if r.returncode != 0:
        print("ERROR: cmake build failed")
        return "FAIL"

    r = run(["ctest", "--output-on-failure", "--test-dir", BUILD_DIR])
    return "PASS" if r.returncode == 0 else "FAIL"


def run_syntax_tests():
    section("SYNTAX TESTS")
    r = subprocess.run([sys.executable, SYNTAX_RUNNER])
    return "PASS" if r.returncode == 0 else "FAIL"


def main():
    syntax_status = run_syntax_tests()
    c_status      = run_c_unit_tests()
    rust_status   = run_rust_unit_tests()

    section("SUMMARY")
    print(f"  Syntax tests:        {syntax_status}")
    print(f"  Unit tests (C):      {c_status}")
    print(f"  Unit tests (Rust):   {rust_status}")
    print()

    if "FAIL" in (syntax_status, c_status, rust_status):
        print("Some tests FAILED.")
        return 1
    print("All tests passed (skipped stages excluded).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
