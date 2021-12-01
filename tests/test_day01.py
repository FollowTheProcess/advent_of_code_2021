from src.day01.day01 import number_of_grouped_increases, number_of_increases


def test_part1():

    example_readings = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    example_answer = 7

    assert number_of_increases(example_readings) == example_answer


def test_part2():

    example_readings = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    example_answer = 5

    assert number_of_grouped_increases(example_readings) == example_answer
