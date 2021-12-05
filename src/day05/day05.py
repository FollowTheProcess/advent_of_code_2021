"""
--- Day 5: Hydrothermal Venture ---

Part 1
------

You come across a field of hydrothermal vents on the ocean floor!

These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents
(your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the
coordinates of one end the line segment and x2,y2 are the coordinates of the other end.

These line segments include the points at both ends. In other words:

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....

In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9.
Each position is shown as the number of lines which cover that point or . if no line covers that point.

The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines
0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap.

In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two lines overlap?

Part 2
------

Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture;
you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal,
vertical, or a diagonal line at exactly 45 degrees. In other words:

An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....
You still need to determine the number of points where at least two lines overlap. In the above example,
this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?
"""

from __future__ import annotations

import collections
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator


# Hash is needed so it works with collections.Counter
@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int

    @classmethod
    def parse(self, text: str) -> Point:
        """
        Parse a `Point` from the text coords
        e.g. "0,9"
        """
        parts = text.split(",")
        if len(parts) != 2:
            raise ValueError(f"Malformed point: {text!r}")

        return Point(x=int(parts[0]), y=int(parts[1]))


# Hash is needed so it works with collections.Counter
@dataclass(unsafe_hash=True)
class Line:
    start: Point
    end: Point

    @classmethod
    def parse(self, text: str) -> Line:
        """
        Parse a `Line` from the text representation
        e.g. "0,9 -> 5,9"
        """
        points = text.strip().split(" -> ")
        if len(points) != 2:
            raise ValueError(f"Malformed line: {text!r}")

        return Line(start=Point.parse(points[0]), end=Point.parse(points[1]))

    def is_horizontal(self) -> bool:
        return self.start.y == self.end.y

    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    def points_covered(self) -> Iterator[Point]:
        """
        Yields the points covered by the calling `Line`
        """
        if self.is_horizontal():
            low = min(self.start.x, self.end.x)
            high = max(self.start.x, self.end.x)

            for x in range(low, high + 1):
                yield Point(x, self.start.y)

        elif self.is_vertical():
            low = min(self.start.y, self.end.y)
            high = max(self.start.y, self.end.y)

            for y in range(low, high + 1):
                yield Point(self.start.x, y)

        else:
            # We have a diagonal line (45 degrees)
            # This one is hard!
            x_low = min(self.start.x, self.end.x)
            x_high = max(self.start.x, self.end.x)

            dx = self.end.x - self.start.x
            dy = self.end.y - self.start.y

            # If the line has a positive gradient it must be the +45 degrees case
            is_positive_gradient = dx * dy > 0

            # +1 to avoid the pesky off by one error that bugged me for ages!
            x = x_low
            y = self.start.y if x_low == self.start.x else self.end.y
            for i in range(x_high - x_low + 1):
                yield Point(x, y)
                x += 1
                y += 1 if is_positive_gradient else -1


def count(lines: Iterable[Line], diagonal: bool = False) -> int:
    counter = collections.Counter(
        point
        for line in lines
        if any([diagonal, line.is_horizontal(), line.is_vertical()])
        for point in line.points_covered()
    )

    return sum(count >= 2 for count in counter.values())


if __name__ == "__main__":
    HERE = Path(__file__).parent.resolve()
    INPUT = HERE / "day05.txt"

    with open(INPUT) as f:
        input_text = f.read()

    items = [line for line in input_text.splitlines()]
    assert len(items) == 500

    lines = [Line.parse(item) for item in items]

    print(f"Part 1: {count(lines)}")
    print()
    print(f"Part 2: {count(lines, diagonal=True)}")
