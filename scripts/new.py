"""
Helper script that sets up a new days directories and files
and gets the puzzle input.

Expects a .env file in the project root with:
AOC_SESSION=<session_cookie>
"""

import argparse
import os
from datetime import datetime
from pathlib import Path

import httpx
from dotenv import load_dotenv

DAYS = {n for n in range(1, 26)}
URL = "https://adventofcode.com/2021"

ROOT = Path(__file__).parent.parent.resolve()


def get_input(day: int, path: Path, session: str) -> None:
    """
    Gets the puzzle input for `day` and saves
    it to `path`.

    This requires the unique `session` cookie.
    """
    input_url = f"{URL}/day/{day}/input"

    res = httpx.get(input_url, cookies={"session": session})
    res.raise_for_status()

    with open(path, mode="w", encoding="utf-8") as f:
        f.write(res.text)


def setup(root: Path, day: int, session: str) -> None:
    """
    Sets up an AOC `day` by creating the necessary
    directories and files as well as downloading
    and saving the input.

    `root` is the absolute path to the root
    of the aoc directory.
    """
    src = root / "src"
    tests = root / "tests"

    # Create a new folder called dayXX under src
    if day < 10:
        day_str = f"day0{day}"
    else:
        day_str = f"day{day}"

    day_x = src / day_str
    day_x.mkdir()

    init = day_x / "__init__.py"
    day_py = day_x / f"{day_str}.py"
    data = day_x / f"{day_str}.txt"

    for file in {init, day_py, data}:
        file.touch()

    # Create the test file
    day_x_test = tests / f"test_{day_str}.py"
    day_x_test.touch()

    get_input(day=day, path=data, session=session)


if __name__ == "__main__":
    load_dotenv(dotenv_path=ROOT / ".env")

    # Get the session cookie
    session = os.getenv("AOC_SESSION")
    if not session:
        raise ValueError("missing session cookie")

    parser = argparse.ArgumentParser(description="Set up an advent of code puzzle.")
    parser.add_argument("day", type=int, nargs=1, help="The day of AOC to set up for.")
    args: argparse.Namespace = parser.parse_args()
    day: int = args.day.pop()

    if day not in DAYS:
        raise ValueError(f"{day} is not a valid day")

    today = datetime.now().day
    if day > today:
        raise ValueError(
            f"{day} December hasn't happened yet, get your time machine out!"
        )

    print(f"Setting up for day: {day}")

    setup(root=ROOT, day=day, session=session)
