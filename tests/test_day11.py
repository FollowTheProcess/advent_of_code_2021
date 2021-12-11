import numpy as np

from src.day11.day11 import Grid, Point

RAW = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


def test_parse():
    want = np.array(
        [
            [5, 4, 8, 3, 1, 4, 3, 2, 2, 3],
            [2, 7, 4, 5, 8, 5, 4, 7, 1, 1],
            [5, 2, 6, 4, 5, 5, 6, 1, 7, 3],
            [6, 1, 4, 1, 3, 3, 6, 1, 4, 6],
            [6, 3, 5, 7, 3, 8, 5, 4, 7, 8],
            [4, 1, 6, 7, 5, 2, 4, 6, 4, 5],
            [2, 1, 7, 6, 8, 4, 1, 7, 2, 1],
            [6, 8, 8, 2, 8, 8, 1, 1, 3, 4],
            [4, 8, 4, 6, 8, 4, 8, 5, 5, 4],
            [5, 2, 8, 3, 7, 5, 1, 5, 2, 6],
        ]
    )

    grid = Grid.parse(RAW)

    assert np.array_equal(grid.array, want)


def test_get_neighbours():
    grid = Grid.parse(RAW)

    # Pick a point, in this case a 6
    point = Point(row=2, col=2)

    want = [
        Point(1, 2),
        Point(3, 2),
        Point(2, 1),
        Point(2, 3),
        Point(1, 1),
        Point(1, 3),
        Point(3, 1),
        Point(3, 3),
    ]

    assert point.get_neighbours(grid) == want

    # Now pick one near an edge
    edge = Point(0, 0)

    want = [
        Point(1, 0),
        Point(0, 1),
        Point(1, 1),
    ]

    assert edge.get_neighbours(grid) == want

    # Now we'll do bottom right
    max_edge = Point(9, 9)

    want = [
        Point(8, 9),
        Point(9, 8),
        Point(8, 8),
    ]

    assert max_edge.get_neighbours(grid) == want


def test_increment():
    grid = Grid.parse(RAW)

    want = Grid(
        array=np.array(
            [
                [6, 5, 9, 4, 2, 5, 4, 3, 3, 4],
                [3, 8, 5, 6, 9, 6, 5, 8, 2, 2],
                [6, 3, 7, 5, 6, 6, 7, 2, 8, 4],
                [7, 2, 5, 2, 4, 4, 7, 2, 5, 7],
                [7, 4, 6, 8, 4, 9, 6, 5, 8, 9],
                [5, 2, 7, 8, 6, 3, 5, 7, 5, 6],
                [3, 2, 8, 7, 9, 5, 2, 8, 3, 2],
                [7, 9, 9, 3, 9, 9, 2, 2, 4, 5],
                [5, 9, 5, 7, 9, 5, 9, 6, 6, 5],
                [6, 3, 9, 4, 8, 6, 2, 6, 3, 7],
            ],
            dtype=np.int32,
        )
    )

    # Bump the grid
    grid.increment()

    assert np.array_equal(grid.array, want.array)


def test_get():
    grid = Grid(
        array=np.array(
            [
                [6, 5, 9, 4, 2, 5, 4, 3, 3, 4],
                [3, 8, 5, 6, 9, 6, 5, 8, 2, 2],
                [6, 3, 7, 5, 6, 6, 7, 2, 8, 4],
                [7, 2, 5, 2, 4, 4, 7, 2, 5, 7],
                [7, 4, 6, 8, 4, 9, 6, 5, 8, 9],
                [5, 2, 7, 8, 6, 3, 5, 7, 5, 6],
                [3, 2, 8, 7, 9, 5, 2, 8, 3, 2],
                [7, 9, 9, 3, 9, 9, 2, 2, 4, 5],
                [5, 9, 5, 7, 9, 5, 9, 6, 6, 5],
                [6, 3, 9, 4, 8, 6, 2, 6, 3, 7],
            ],
            dtype=np.int32,
        )
    )

    assert grid.get(Point(0, 0)) == 6
    assert grid.get(Point(3, 8)) == 5
    assert grid.get(Point(8, 6)) == 9
    assert grid.get(Point(9, 9)) == 7


def test_set():
    grid = Grid(
        array=np.array(
            [
                [6, 5, 9, 4, 2, 5, 4, 3, 3, 4],
                [3, 8, 5, 6, 9, 6, 5, 8, 2, 2],
                [6, 3, 7, 5, 6, 6, 7, 2, 8, 4],
                [7, 2, 5, 2, 4, 4, 7, 2, 5, 7],
                [7, 4, 6, 8, 4, 9, 6, 5, 8, 9],
                [5, 2, 7, 8, 6, 3, 5, 7, 5, 6],
                [3, 2, 8, 7, 9, 5, 2, 8, 3, 2],
                [7, 9, 9, 3, 9, 9, 2, 2, 4, 5],
                [5, 9, 5, 7, 9, 5, 9, 6, 6, 5],
                [6, 3, 9, 4, 8, 6, 2, 6, 3, 7],
            ],
            dtype=np.int32,
        )
    )

    grid.set(Point(0, 0), 7)
    grid.set(Point(3, 8), 9)
    grid.set(Point(8, 6), 2)
    grid.set(Point(9, 9), 0)

    assert grid.get(Point(0, 0)) == 7
    assert grid.get(Point(3, 8)) == 9
    assert grid.get(Point(8, 6)) == 2
    assert grid.get(Point(9, 9)) == 0


def test_example_part1():
    grid = Grid.parse(RAW)

    assert sum(grid.step() for _ in range(100)) == 1656


def test_example_part2():
    grid = Grid.parse(RAW)

    assert grid.sync_point() == 195
