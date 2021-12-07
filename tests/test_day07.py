from src.day07.day07 import find_cheapest_fuel_use, find_cheapest_fuel_use_part2


def test_example_part1():
    positions = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]

    assert find_cheapest_fuel_use(positions) == 37


def test_example_part2():
    positions = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]

    assert find_cheapest_fuel_use_part2(positions) == 168
