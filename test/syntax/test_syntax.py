"""
Syntax Tests — does the parser accept valid programs and reject invalid ones?
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from common import TestRunner, run_lo3, run_with_ext, stdout_eq


def run(r: TestRunner) -> None:

    # --- File validation ---

    out, err, code = run_lo3("#0 $0 $0\n")
    r.check("Minimal valid program (exit 0) is accepted",
            code == 0, f"exit={code} stderr={err!r}")

    out, err, code = run_with_ext("#0 $0 $0\n", ".txt")
    r.check("Wrong extension (.txt) is rejected",
            code != 0, f"exit={code}")

    out, err, code = run_with_ext("#0 $0 $0\n", ".lo")
    r.check("Wrong extension (.lo) is rejected",
            code != 0, f"exit={code}")

    # --- Comments and blank lines ---

    prog = "// comment\n#n _a $0\n#= _a $5\n#o %a $0\n#0 $0 $0\n"
    out, err, code = run_lo3(prog)
    r.check("Comment lines (//) are skipped",
            code == 0 and "5" in out, f"out={out!r}")

    prog = "\n\n#n _a $0\n\n#= _a $7\n\n#o %a $0\n\n#0 $0 $0\n"
    out, err, code = run_lo3(prog)
    r.check("Empty lines are skipped",
            code == 0 and "7" in out, f"out={out!r}")

    prog = (
        "// program start\n"
        "\n"
        "#n _x $0\n"
        "// set x\n"
        "#= _x $3\n"
        "\n"
        "#o %x $0\n"
        "#0 $0 $0\n"
    )
    out, err, code = run_lo3(prog)
    r.check("Mixed comments + empty lines do not disturb parsing",
            code == 0 and stdout_eq(out, "3"), f"out={out!r}")

    # --- Exit commands ---

    out, err, code = run_lo3("#0 $0 $0\n")
    r.check("#0 produces exit code 0", code == 0, f"exit={code}")

    out, err, code = run_lo3("#1 $0 $0\n")
    r.check("#1 produces exit code 1", code == 1, f"exit={code}")

    # --- Command sequence ---

    prog = (
        "#n _a $0\n"
        "#n _b $0\n"
        "#= _a $1\n"
        "#= _b $2\n"
        "#o %a $0\n"
        "#o %b $0\n"
        "#0 $0 $0\n"
    )
    out, err, code = run_lo3(prog)
    r.check("Multiple commands in sequence all execute",
            code == 0 and "1" in out and "2" in out, f"out={out!r}")

    # --- Free without crash ---

    prog = "#n _a $0\n#= _a $9\n#f _a $0\n#0 $0 $0\n"
    out, err, code = run_lo3(prog)
    r.check("#f (free) followed by exit does not crash",
            code == 0, f"exit={code} stderr={err!r}")
