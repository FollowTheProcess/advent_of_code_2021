from aoc.day1.day1 import number_of_increases


def test_day1():

    example_readings = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    example_answer = 7

    assert number_of_increases(example_readings) == example_answer
