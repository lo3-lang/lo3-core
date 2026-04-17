"""
Unit Tests — Variables: creation, assignment, reassignment, free, strings.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from common import TestRunner, run_lo3, stdout_eq, stdout_lines


def run(r: TestRunner) -> None:

    # --- Number variables ---

    prog = "#n _a $0\n#= _a $42\n#o %a $0\n#0 $0 $0\n"
    out, err, code = run_lo3(prog)
    r.check("Create number variable and output it (42)",
            code == 0 and stdout_eq(out, "42"), f"out={out!r}")

    prog = "#n _z $0\n#= _z $0\n#o %z $0\n#0 $0 $0\n"
    out, err, code = run_lo3(prog)
    r.check("Assign value 0 and output it",
            code == 0 and stdout_eq(out, "0"), f"out={out!r}")

    prog = "#n _a $0\n#= _a $1\n#= _a $99\n#o %a $0\n#0 $0 $0\n"
    out, err, code = run_lo3(prog)
    r.check("Reassignment overwrites previous value (→ 99)",
            code == 0 and stdout_eq(out, "99"), f"out={out!r}")

    prog = "#n _x $0\n#= _x $1000000\n#o %x $0\n#0 $0 $0\n"
    out, err, code = run_lo3(prog)
    r.check("Large number (1 000 000) is stored correctly",
            code == 0 and stdout_eq(out, "1000000"), f"out={out!r}")

    # --- String variables ---

    prog = "#n _msg $3\n#= _msg _hello\n#o %msg $0\n#0 $0 $0\n"
    out, err, code = run_lo3(prog)
    r.check("String variable stores and prints 'hello'",
            code == 0 and stdout_eq(out, "hello"), f"out={out!r}")

    prog = "#n _s $3\n#= _s _lo3\n#o %s $0\n#0 $0 $0\n"
    out, err, code = run_lo3(prog)
    r.check("String variable with value 'lo3'",
            code == 0 and stdout_eq(out, "lo3"), f"out={out!r}")

    # --- Multiple independent variables ---

    prog = (
        "#n _a $0\n#n _b $0\n"
        "#= _a $10\n#= _b $20\n"
        "#o %a $0\n#o %b $0\n"
        "#0 $0 $0\n"
    )
    out, err, code = run_lo3(prog)
    r.check("Two number variables are independent [10, 20]",
            code == 0 and stdout_lines(out) == ["10", "20"], f"out={out!r}")

    prog = (
        "#n _a $0\n#n _b $0\n#n _c $0\n"
        "#= _a $1\n#= _b $2\n#= _c $3\n"
        "#o %a $0\n#o %b $0\n#o %c $0\n"
        "#0 $0 $0\n"
    )
    out, err, code = run_lo3(prog)
    r.check("Three variables each hold their own value [1, 2, 3]",
            code == 0 and stdout_lines(out) == ["1", "2", "3"], f"out={out!r}")

    # --- Assign from variable to variable ---

    prog = (
        "#n _a $0\n#n _b $0\n"
        "#= _a $55\n"
        "#= _b %a\n"
        "#o %b $0\n"
        "#0 $0 $0\n"
    )
    out, err, code = run_lo3(prog)
    r.check("Assign from variable to variable (b = a = 55)",
            code == 0 and stdout_eq(out, "55"), f"out={out!r}")

    # --- Free ---

    prog = "#n _a $0\n#= _a $1\n#f _a $0\n#0 $0 $0\n"
    out, err, code = run_lo3(prog)
    r.check("Free a variable does not crash",
            code == 0, f"exit={code} stderr={err!r}")

    prog = (
        "#n _a $0\n#n _b $0\n"
        "#= _a $5\n#= _b $6\n"
        "#f _a $0\n"
        "#o %b $0\n"
        "#0 $0 $0\n"
    )
    out, err, code = run_lo3(prog)
    r.check("Freeing one variable leaves other variables intact",
            code == 0 and stdout_eq(out, "6"), f"out={out!r}")
