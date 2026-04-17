"""
Unit Tests — Arithmetic: addition, subtraction, multiplication with literals and variables.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from common import TestRunner, run_lo3, stdout_eq


def _prog(*ops: str, start: int = 0) -> str:
    """Build a program: create _x, set to start, apply ops, output, exit."""
    lines = ["#n _x $0", f"#= _x ${start}"] + list(ops) + ["#o %x $0", "#0 $0 $0"]
    return "\n".join(lines) + "\n"


def run(r: TestRunner) -> None:

    # --- Addition ---

    out, err, code = run_lo3(_prog("#+ _x $5", start=10))
    r.check("Addition: 10 + 5 = 15",
            code == 0 and stdout_eq(out, "15"), f"out={out!r}")

    out, err, code = run_lo3(_prog("#+ _x $0", start=7))
    r.check("Add zero: 7 + 0 = 7 (identity)",
            code == 0 and stdout_eq(out, "7"), f"out={out!r}")

    out, err, code = run_lo3(_prog("#+ _x $100", "#+ _x $200", start=0))
    r.check("Two additions: 0 + 100 + 200 = 300",
            code == 0 and stdout_eq(out, "300"), f"out={out!r}")

    # --- Subtraction ---

    out, err, code = run_lo3(_prog("#- _x $8", start=20))
    r.check("Subtraction: 20 - 8 = 12",
            code == 0 and stdout_eq(out, "12"), f"out={out!r}")

    out, err, code = run_lo3(_prog("#- _x $10", start=3))
    r.check("Subtraction with negative result: 3 - 10 = -7",
            code == 0 and stdout_eq(out, "-7"), f"out={out!r}")

    out, err, code = run_lo3(_prog("#- _x $0", start=5))
    r.check("Subtract zero: 5 - 0 = 5 (identity)",
            code == 0 and stdout_eq(out, "5"), f"out={out!r}")

    # --- Multiplication ---

    out, err, code = run_lo3(_prog("#* _x $7", start=6))
    r.check("Multiplication: 6 * 7 = 42",
            code == 0 and stdout_eq(out, "42"), f"out={out!r}")

    out, err, code = run_lo3(_prog("#* _x $0", start=99))
    r.check("Multiply by zero: 99 * 0 = 0",
            code == 0 and stdout_eq(out, "0"), f"out={out!r}")

    out, err, code = run_lo3(_prog("#* _x $1", start=42))
    r.check("Multiply by one: 42 * 1 = 42 (identity)",
            code == 0 and stdout_eq(out, "42"), f"out={out!r}")

    out, err, code = run_lo3(_prog("#* _x $3", "#* _x $4", start=2))
    r.check("Two multiplications: 2 * 3 * 4 = 24",
            code == 0 and stdout_eq(out, "24"), f"out={out!r}")

    # --- Mixed chains ---

    out, err, code = run_lo3(_prog("#+ _x $50", "#- _x $30", "#* _x $2", start=10))
    r.check("Mixed chain: (10 + 50 - 30) * 2 = 60",
            code == 0 and stdout_eq(out, "60"), f"out={out!r}")

    # --- Variable as operand ---

    prog = (
        "#n _a $0\n#n _b $0\n"
        "#= _a $10\n#= _b $5\n"
        "#+ _a %b\n"
        "#o %a $0\n#0 $0 $0\n"
    )
    out, err, code = run_lo3(prog)
    r.check("Add variable to variable: 10 + 5 = 15",
            code == 0 and stdout_eq(out, "15"), f"out={out!r}")

    prog = (
        "#n _a $0\n#n _b $0\n"
        "#= _a $30\n#= _b $12\n"
        "#- _a %b\n"
        "#o %a $0\n#0 $0 $0\n"
    )
    out, err, code = run_lo3(prog)
    r.check("Subtract variable from variable: 30 - 12 = 18",
            code == 0 and stdout_eq(out, "18"), f"out={out!r}")

    prog = (
        "#n _a $0\n#n _b $0\n"
        "#= _a $9\n#= _b $3\n"
        "#* _a %b\n"
        "#o %a $0\n#0 $0 $0\n"
    )
    out, err, code = run_lo3(prog)
    r.check("Multiply variable by variable: 9 * 3 = 27",
            code == 0 and stdout_eq(out, "27"), f"out={out!r}")
