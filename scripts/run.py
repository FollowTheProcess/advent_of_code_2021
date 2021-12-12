"""
Helper script to easily run a day's code.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

DAYS = {n for n in range(1, 26)}
ROOT = Path(__file__).parent.parent.resolve()
SRC = ROOT / "src"
PYTHON = os.fsdecode(ROOT / ".venv" / "bin" / "python")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run an advent of code file.")
    parser.add_argument("day", type=int, nargs=1, help="The day of AOC to run.")
    args: argparse.Namespace = parser.parse_args()
    day: int = args.day.pop()

    if day not in DAYS:
        raise ValueError(f"{day} is not a valid day.")

    day_str = f"day{day:02d}"

    file = SRC / day_str / f"{day_str}.py"

    if not file.exists():
        raise ValueError(f"You haven't done day {day} yet!")

    subprocess.run(
        args=[PYTHON, file], check=True, stdout=sys.stdout, stderr=sys.stderr
    )
