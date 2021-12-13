"""
--- Day 13: Transparent Origami ---

You reach another volcanically active part of the cave. It would be nice if you could do some kind of thermal
imaging so you could tell ahead of time which caves are too hot to safely enter.

Fortunately, the submarine seems to be equipped with a thermal camera! When you activate it, you are greeted with:

Congratulations on your purchase! To activate this infrared thermal imaging
camera system, please enter the code found on page 1 of the manual.
Apparently, the Elves have never used this feature. To your surprise, you manage to find the manual; as you go
to open it, page 1 falls out. It's a large sheet of transparent paper!
The transparent paper is marked with random dots and includes instructions on how to fold it up (your puzzle input).

For example:

6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5

The first section is a list of dots on the transparent paper. 0,0 represents the top-left coordinate.
The first value, x, increases to the right. The second value, y, increases downward.
So, the coordinate 3,0 is to the right of 0,0, and the coordinate 0,7 is below 0,0.
The coordinates in this example form the following pattern,
where # is a dot on the paper and . is an empty, unmarked position:

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Then, there is a list of fold instructions. Each instruction indicates a line on the transparent paper and
wants you to fold the paper up (for horizontal y=... lines) or left (for vertical x=... lines).
In this example, the first fold instruction is fold along y=7, which designates the line formed by all of
the positions where y is 7 (marked here with -):

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
-----------
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Because this is a horizontal line, fold the bottom half up. Some of the dots might end up overlapping after the
fold is complete, but dots will never appear exactly on a fold line. The result of doing this fold looks like this:

#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........

Now, only 17 dots are visible.

Notice, for example, the two dots in the bottom left corner before the transparent paper is folded; after
the fold is complete, those dots appear in the top left corner (at 0,0 and 0,1).
Because the paper is transparent, the dot just below them in the result (at 0,3) remains visible,
as it can be seen through the transparent paper.

Also notice that some dots can end up overlapping; in this case, the dots merge together and become a single dot.

The second fold instruction is fold along x=5, which indicates this line:

#.##.|#..#.
#...#|.....
.....|#...#
#...#|.....
.#.#.|#.###
.....|.....
.....|.....

Because this is a vertical line, fold left:

#####
#...#
#...#
#...#
#####
.....
.....

The instructions made a square!

The transparent paper is pretty big, so for now, focus on just completing the first fold.
After the first fold in the example above, 17 dots are visible - dots that end up overlapping
after the fold is completed count as a single dot.

How many dots are visible after completing just the first fold instruction on your transparent paper?

--- Part Two ---

Finish folding the transparent paper according to the instructions.
The manual says the code is always eight capital letters.

What code do you use to activate the infrared thermal imaging camera system?
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from pprint import pprint


@dataclass
class Fold:
    axis: str
    line: int

    @classmethod
    def parse(cls, text: str) -> Fold:
        """
        Parse a single fold instruction from text.

        >>> f = Fold.parse("fold along y=7")
        >>> f
        Fold(axis='y', line=7)

        >>> f = Fold.parse("fold along x=5")
        >>> f
        Fold(axis='x', line=5)
        """
        if not text.startswith("fold along"):
            raise ValueError(f"Invalid fold instruction: {text!r}")

        text = text.replace("fold along ", "").strip()
        return Fold(axis=text.split("=")[0], line=int(text.split("=")[1]))


@dataclass
class Point:
    row: int
    col: int

    @classmethod
    def parse(cls, text: str) -> Point:
        """
        Parse a `Point` from it's text representation of (x,y)
        where x is horizontal (column) and y is vertical (row)

        >>> p = Point.parse("6,10")
        >>> p
        Point(row=10, col=6)
        """
        parts = text.strip().split(",")
        if len(parts) != 2:
            raise ValueError(f"Unparseable point: {text!r}")

        return Point(row=int(parts[1]), col=int(parts[0]))


@dataclass
class Paper:
    """
    Representation of the piece of paper.

    Args:
        array (list[list[str]]): The n x n matrix representing
            all the coordinates of the paper, each element will
            either be a # representing a "dot" or a . representing
            an empty slot
    """

    array: list[list[str]]

    @classmethod
    def parse_points(cls, text: str) -> Paper:
        """
        Parse the input text into a `Paper` object.
        """
        points = [Point.parse(n) for n in text.strip().split("\n\n")[0].splitlines()]

        max_col = max([point.col for point in points]) + 1
        max_row = max([point.row for point in points]) + 1

        # Construct the array, initialising everything as an empty '.'
        array = [["." for i in range(max_col)] for i in range(max_row)]

        # Populate all the dots
        for point in points:
            array[point.row][point.col] = "#"

        return Paper(array)

    @staticmethod
    def parse_fold_instructions(text: str) -> list[Fold]:
        """
        Parses all the fold instructions from the input
        and returns them.
        """
        return [Fold.parse(n) for n in text.strip().split("\n\n")[1].splitlines()]

    def get(self, point: Point) -> str:
        """
        Gets the value stored at `point`.
        """
        return self.array[point.row][point.col]

    def set(self, point: Point, value: str) -> None:
        """
        Sets the value at `point` to `value`.
        """
        self.array[point.row][point.col] = value

    def get_row(self, row: int) -> list[str]:
        """
        Get a row by index.
        """
        return self.array[row]

    def get_col(self, col: int) -> list[str]:
        """
        Get a column by index.
        """
        return [row[col] for row in self.array]

    def show(self) -> None:
        """
        Pretty prints the paper.
        """
        pprint(self)

    def move(self, frm: Point, to: Point) -> None:
        """
        Moves whatever is at `frm` to `to` and replaces
        `frm` with a "."
        """
        from_value = self.get(frm)
        self.set(to, from_value)
        self.set(frm, ".")

    def count_dots(self) -> int:
        """
        Counts the number of dots ('#') present
        on the paper.
        """
        count = 0
        for i, row in enumerate(self.array):
            for j, col in enumerate(row):
                if self.get(Point(i, j)) == "#":
                    count += 1

        return count

    def _fold_vertical(self, line: int) -> None:
        """
        Specialised method for a vertical fold.
        """
        # e.g. fold along y=7
        # Loop through everything below the 7th row
        # hit the first '#' at row 10, col 1
        # folding vertically so column stays the same
        # 10 - 7 = 3 so it needs to be moved -3 above the fold line

        start_row = line
        for i, row in enumerate(self.array[line:]):
            current_row = start_row + i
            start_col = 0
            for j, point in enumerate(row):
                current_col = start_col + j
                # Keep track of where we currently are
                at = Point(current_row, current_col)

                if self.get(at) == "#":
                    delta_y = current_row - line
                    to = Point(line - delta_y, current_col)
                    # Move the dot
                    self.move(at, to)

        # We're now at the end of the bottom edge and should have moved everything
        # We can cut off everything below the fold line (including the fold line itself)
        self.array = self.array[:line]

    def _fold_horizontal(self, line: int) -> None:
        """
        Specialised method for a horizontal fold.
        """
        # e.g. fold along x=5
        # Loop through everything right of the 5th column
        # hit the first '#' at row 0, col 6
        # folding horizontally so row stays the same
        # 6 - 5 = 1 so it needs to be moved -1 left of the fold line

        start_col = line
        start_row = 0
        for i, row in enumerate(self.array):
            current_row = start_row + i
            for j, col in enumerate(row[line:]):
                current_col = start_col + j
                # Keep track of where we currently are
                at = Point(current_row, current_col)

                if self.get(at) == "#":
                    delta_x = current_col - line
                    to = Point(current_row, line - delta_x)
                    # Move the dot
                    self.move(at, to)

        # We're now at the end of the right half and should have moved everything
        # can cut off everything right of the fold line (including itself)
        new = [row[:line] for row in self.array]
        self.array = new

    def fold(self, fold: Fold) -> None:
        """
        Perform the fold specified by `Fold` on the
        piece of paper.
        """
        if fold.axis == "y":
            self._fold_vertical(fold.line)
        elif fold.axis == "x":
            self._fold_horizontal(fold.line)
        else:
            raise ValueError(f"Unsupported fold axis: {fold.axis!r}")

    def apply_folds(self, folds: list[Fold]) -> None:
        """
        Perform a series of folds in order.
        """
        for fold in folds:
            self.fold(fold)


if __name__ == "__main__":
    HERE = Path(__file__).parent.resolve()
    INPUT = HERE / "day13.txt"

    with open(INPUT) as f:
        input_text = f.read()

    paper = Paper.parse_points(input_text)
    folds = Paper.parse_fold_instructions(input_text)

    # Apply the first fold
    paper.fold(folds[0])
    print(f"Part 1: {paper.count_dots()}")
    print()

    # Apply the remaining folds
    paper.apply_folds(folds[1:])
    for row in paper.array:
        print(row)
