from src.day05.day05 import Line, Point, count


def test_point_parse():
    example = "0,9"

    assert Point.parse(example) == Point(x=0, y=9)


def test_line_parse():
    example = "0,9 -> 5,9"

    assert Line.parse(example) == Line(start=Point(0, 9), end=Point(5, 9))


def test_points_covered():
    line = Line(start=Point(0, 9), end=Point(5, 9))

    covered = [
        Point(0, 9),
        Point(1, 9),
        Point(2, 9),
        Point(3, 9),
        Point(4, 9),
        Point(5, 9),
    ]

    for i, point in enumerate(line.points_covered()):
        assert point == covered[i]


def test_example_part_1():
    input = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

    lines = [Line.parse(item) for item in input.splitlines()]

    assert count(lines) == 5


def test_example_part_2():
    input = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

    lines = [Line.parse(item) for item in input.splitlines()]

    assert count(lines, diagonal=True) == 12
