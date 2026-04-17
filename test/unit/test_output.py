"""
Unit Tests — Output: correctness and ordering of the #o command.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from common import TestRunner, run_lo3, stdout_eq, stdout_lines


def run(r: TestRunner) -> None:

    # --- Basic output ---

    prog = "#n _a $0\n#= _a $1\n#o %a $0\n#0 $0 $0\n"
    out, err, code = run_lo3(prog)
    r.check("Output a single number",
            code == 0 and stdout_eq(out, "1"), f"out={out!r}")

    prog = "#n _s $3\n#= _s _hello\n#o %s $0\n#0 $0 $0\n"
    out, err, code = run_lo3(prog)
    r.check("Output a string value",
            code == 0 and stdout_eq(out, "hello"), f"out={out!r}")

    # --- Output ordering ---

    prog = (
        "#n _a $0\n#n _b $0\n"
        "#= _a $1\n#= _b $2\n"
        "#o %a $0\n#o %b $0\n"
        "#0 $0 $0\n"
    )
    out, err, code = run_lo3(prog)
    r.check("Two outputs in declared order [1, 2]",
            code == 0 and stdout_lines(out) == ["1", "2"], f"out={out!r}")

    prog = (
        "#n _a $0\n#n _b $0\n#n _c $0\n"
        "#= _a $10\n#= _b $20\n#= _c $30\n"
        "#o %c $0\n#o %a $0\n#o %b $0\n"
        "#0 $0 $0\n"
    )
    out, err, code = run_lo3(prog)
    r.check("Output order follows #o sequence, not declaration order [30, 10, 20]",
            code == 0 and stdout_lines(out) == ["30", "10", "20"], f"out={out!r}")

    # --- Output after arithmetic ---

    prog = (
        "#n _x $0\n"
        "#= _x $8\n#+ _x $2\n"
        "#o %x $0\n#0 $0 $0\n"
    )
    out, err, code = run_lo3(prog)
    r.check("Output after addition shows updated value (10)",
            code == 0 and stdout_eq(out, "10"), f"out={out!r}")

    prog = (
        "#n _x $0\n#= _x $5\n"
        "#o %x $0\n"
        "#+ _x $5\n"
        "#o %x $0\n"
        "#0 $0 $0\n"
    )
    out, err, code = run_lo3(prog)
    r.check("Output before and after add shows both snapshots [5, 10]",
            code == 0 and stdout_lines(out) == ["5", "10"], f"out={out!r}")

    # --- Output after reassignment ---

    prog = (
        "#n _a $0\n#= _a $1\n"
        "#o %a $0\n"
        "#= _a $99\n"
        "#o %a $0\n"
        "#0 $0 $0\n"
    )
    out, err, code = run_lo3(prog)
    r.check("Output before and after reassignment [1, 99]",
            code == 0 and stdout_lines(out) == ["1", "99"], f"out={out!r}")

    # --- No spurious extra output ---

    prog = "#n _a $0\n#= _a $7\n#o %a $0\n#0 $0 $0\n"
    out, err, code = run_lo3(prog)
    r.check("Exactly one output line for a single #o",
            code == 0 and len(stdout_lines(out)) == 1, f"out={out!r}")
