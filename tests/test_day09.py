from math import prod

import pytest

from src.day09.day09 import Map, Point

DEMO_MAP = [
    [2, 1, 9, 9, 9, 4, 3, 2, 1, 0],
    [3, 9, 8, 7, 8, 9, 4, 9, 2, 1],
    [9, 8, 5, 6, 7, 8, 9, 8, 9, 2],
    [8, 7, 6, 7, 8, 9, 6, 7, 8, 9],
    [9, 8, 9, 9, 9, 6, 5, 6, 7, 8],
]

RAW_MAP = """2199943210
3987894921
9856789892
8767896789
9899965678"""


def test_map_parse():
    assert Map.parse(RAW_MAP) == Map(DEMO_MAP)


def test_map_properties():
    map = Map(DEMO_MAP)

    assert map.max_rows == 5
    assert map.max_cols == 10


@pytest.mark.parametrize(
    "point, value",
    [
        (Point(0, 0), 2),
        (Point(0, 5), 4),
        (Point(2, 4), 7),
        (Point(4, 9), 8),
    ],
)
def test_map_get(point: Point, value: int):
    map = Map(DEMO_MAP)

    assert map.get(point) == value


def test_map_get_lowpoints():
    map = Map(DEMO_MAP)

    assert map.get_lowpoints() == [Point(0, 1), Point(0, 9), Point(2, 2), Point(4, 6)]


def test_point_is_in():
    map = Map(DEMO_MAP)

    assert Point(2, 4).is_in(map) is True
    assert Point(99, 99).is_in(map) is False

    # Let's do a close one
    assert Point(0, 10).is_in(map) is False
    assert Point(5, 3).is_in(map) is False


def test_point_get_neighbours():
    map = Map(DEMO_MAP)

    point = Point(1, 2)

    want = [
        Point(0, 2),
        Point(2, 2),
        Point(1, 1),
        Point(1, 3),
    ]

    assert point.get_neighbours(map) == want

    # Let's do one on the edge
    point = Point(0, 0)

    want = [
        Point(1, 0),
        Point(0, 1),
    ]

    assert point.get_neighbours(map) == want


@pytest.mark.parametrize(
    "point, value",
    [
        (Point(0, 0), 2),
        (Point(0, 4), 9),
        (Point(3, 7), 7),
        (Point(4, 9), 8),
        (Point(1, 2), 8),
    ],
)
def test_point_value(point: Point, value: int):
    map = Map(DEMO_MAP)

    assert point.value(map) == value


def test_point_is_lowpoint():
    map = Map(DEMO_MAP)

    # Use the given low points from the example
    low1 = Point(0, 1)
    low2 = Point(0, 9)
    low3 = Point(2, 2)
    low4 = Point(4, 6)

    lows = [low1, low2, low3, low4]

    for low in lows:
        assert low.is_lowpoint(map) is True

    # Check some non low points
    assert Point(1, 1).is_lowpoint(map) is False
    assert Point(3, 8).is_lowpoint(map) is False


def test_point_risklevel():
    map = Map(DEMO_MAP)

    low1 = Point(0, 1)
    low2 = Point(0, 9)
    low3 = Point(2, 2)
    low4 = Point(4, 6)

    assert low1.risk_level(map) == 2
    assert low2.risk_level(map) == 1
    assert low3.risk_level(map) == 6
    assert low4.risk_level(map) == 6


def test_example_part_1():
    map = Map(DEMO_MAP)

    assert sum(point.risk_level(map) for point in map.get_lowpoints()) == 15


def test_get_basins():
    map = Map(DEMO_MAP)

    basins = map.get_basins()

    # Top left basin
    assert basins[0] == [
        Point(0, 1),
        Point(0, 0),
        Point(1, 0),
    ]
    # Top right basin
    assert basins[1] == [
        Point(row=0, col=9),
        Point(row=1, col=9),
        Point(row=0, col=8),
        Point(row=1, col=8),
        Point(row=0, col=7),
        Point(row=0, col=6),
        Point(row=1, col=6),
        Point(row=0, col=5),
        Point(row=2, col=9),
    ]

    # Middle basin
    assert basins[2] == [
        Point(row=2, col=2),
        Point(row=1, col=2),
        Point(row=3, col=2),
        Point(row=2, col=1),
        Point(row=2, col=3),
        Point(row=1, col=3),
        Point(row=3, col=3),
        Point(row=2, col=4),
        Point(row=1, col=4),
        Point(row=3, col=4),
        Point(row=2, col=5),
        Point(row=3, col=1),
        Point(row=4, col=1),
        Point(row=3, col=0),
    ]

    # Bottom right basin
    assert basins[3] == [
        Point(row=4, col=6),
        Point(row=3, col=6),
        Point(row=4, col=5),
        Point(row=4, col=7),
        Point(row=3, col=7),
        Point(row=4, col=8),
        Point(row=3, col=8),
        Point(row=4, col=9),
        Point(row=2, col=7),
    ]


def test_example_part2():
    map = Map(DEMO_MAP)

    basins = map.get_basins()
    lengths = [len(basin) for basin in basins]
    largest_3 = sorted(lengths, reverse=True)[:3]

    assert prod(largest_3) == 1134
