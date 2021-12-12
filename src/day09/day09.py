"""
--- Day 9: Smoke Basin ---

Part 1
------

These caves seem to be lava tubes. Parts are even still volcanically active; small
hydrothermal vents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid it and
be that much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678

Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the
lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of its adjacent locations.
Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner
of the map have three or two adjacent locations, respectively.
(Diagonal locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0),
one is in the third row (a 5), and one is in the bottom row (also a 5).
All other locations on the heightmap have some lower adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example,
the risk levels of the low points are 2, 1, 6, and 6.
The sum of the risk levels of all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap.

What is the sum of the risk levels of all low points on your heightmap?

Part 2
------

Next, you need to find the largest basins so you know what areas are most important to avoid.

A basin is all locations that eventually flow downward to a single low point.
Therefore, every low point has a basin, although some basins are very small.
Locations of height 9 do not count as being in any basin, and all other locations will
always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the low point.

The example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678
The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678
The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
Find the three largest basins and multiply their sizes together. In the above example, this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?
"""

from __future__ import annotations

from dataclasses import dataclass
from math import prod
from pathlib import Path


@dataclass
class Map:
    squares: list[list[int]]

    @property
    def max_rows(self) -> int:
        return len(self.squares)

    @property
    def max_cols(self) -> int:
        return len(self.squares[0])

    def get(self, point: Point) -> int:
        """
        Gets the value stored at `point`.
        """
        if not point.is_in(self):
            raise ValueError(f"Requested point: {point} not in map")

        return self.squares[point.row][point.col]

    @classmethod
    def parse(cls, raw: str) -> Map:
        """
        Parse a `Map` from raw text.
        """
        lines = raw.strip().splitlines()
        squares: list[list[int]] = []

        for line in lines:
            row = [int(n) for n in list(line) if n.isdigit()]
            squares.append(row)

        return Map(squares)

    def get_lowpoints(self) -> list[Point]:
        """
        Iterates through the map and returns all the lowpoints.
        """
        lows: list[Point] = []
        for y, row in enumerate(self.squares):
            for x, col in enumerate(row):
                point = Point(y, x)
                if point.is_lowpoint(self):
                    lows.append(point)

        return lows

    def get_basins(self) -> list[list[Point]]:
        """
        Iterates through the map and returns a list of
        all the basins (defined as a list of `Point` that make up
        the basin).
        """
        # A basin always begins at the low points
        # Iterate through each low point's neighbours, if their value
        # is higher, we're going "uphill" and are therefore still in
        # the basin
        basins: list[list[Point]] = []
        for low in self.get_lowpoints():
            # basin is the basin we're currently in, initialised
            # with the starting low point
            basin: list[Point] = [low]

            # to fill is our constantly changing list of other points in
            # the basin, when this is empty, we've found every point in the
            # basin
            to_fill: list[Point] = [low]

            while len(to_fill) > 0:
                # While there's still stuff in to_fill, pop it off
                # and follow the neighbours
                point = to_fill.pop()
                for neighbour in point.get_neighbours(self):
                    # If the neighbour is bigger, not 9, and not
                    # already in the basin (no duplicates allowed)
                    if (
                        neighbour.value(self) > point.value(self)
                        and neighbour.value(self) != 9
                        and neighbour not in basin
                    ):
                        to_fill.append(neighbour)
                        basin.append(neighbour)

            basins.append(basin)

        return basins


@dataclass(eq=True, order=True)
class Point:
    row: int
    col: int

    def is_in(self, map: Map) -> bool:
        """
        Returns True if the point is inside the `Map`
        else False.
        """
        # Conditions to be out of the map
        conditions = [
            self.row < 0,
            self.row >= map.max_rows,
            self.col < 0,
            self.col >= map.max_cols,
        ]

        return not any(condition for condition in conditions)

    def get_neighbours(self, map: Map) -> list[Point]:
        """
        Gets all adjacent points to the current `Point`.

        Points that are outside of `map` will be ignored, hence
        why we must pass in the `map`.
        """
        potentials = [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]

        return [potential for potential in potentials if potential.is_in(map)]

    def value(self, map: Map) -> int:
        """
        Returns the value stored at the current point
        in `map`.
        """
        return map.get(self)

    def is_lowpoint(self, map: Map) -> bool:
        """
        Returns True if the current point is lower
        than all of it's neighbours, else False.
        """
        neighbours = self.get_neighbours(map)
        return all(self.value(map) < neighbour.value(map) for neighbour in neighbours)

    def risk_level(self, map: Map) -> int:
        """
        Calculates and returns the risk level of a point,
        defined as 1 + it's height (the value stored at that point in the `map`)
        """
        return self.value(map) + 1


if __name__ == "__main__":
    HERE = Path(__file__).parent.resolve()
    INPUT = HERE / "day09.txt"

    with open(INPUT) as f:
        raw = f.read()

    map = Map.parse(raw)

    sizes = [len(basin) for basin in map.get_basins()]
    largest_3_basins = sorted(sizes, reverse=True)[:3]

    print(f"Part 1: {sum(point.risk_level(map) for point in map.get_lowpoints())}")
    print()
    print(f"Part 2: {prod(largest_3_basins)}")
