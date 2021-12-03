from src.day03.day03 import (
    Binary,
    CountResult,
    get_co2_rating,
    get_epsilon_rate,
    get_gamma_rate,
    get_life_support_rating,
    get_oxygen_rating,
    get_power_consumption,
    most_and_least_common_bits,
)

# The example binaries are 5 digits long
TEST_LEN = 5


def test_binary_from_item():
    item = "11001"
    b = Binary.from_item(item)

    assert b.raw == item


def test_binary_to_bin():
    b = Binary("11001")

    assert b.to_bin() == "0b11001"


def test_binary_to_int():
    b = Binary("11001")

    assert b.to_int() == 25


def test_binary_bit():
    b = Binary("11001")

    assert b.bit(0) == 1
    assert b.bit(1) == 1
    assert b.bit(2) == 0
    assert b.bit(3) == 0
    assert b.bit(4) == 1


def test_most_and_least_common_bits():
    bins = [
        Binary("00100"),
        Binary("11110"),
        Binary("10110"),
        Binary("10111"),
        Binary("10101"),
        Binary("01111"),
        Binary("00111"),
        Binary("11100"),
        Binary("10000"),
        Binary("11001"),
        Binary("00010"),
        Binary("01010"),
    ]

    assert most_and_least_common_bits(bins, bit=0) == (
        CountResult(digit=1, count=7),
        CountResult(digit=0, count=5),
    )
    assert most_and_least_common_bits(bins, bit=1) == (
        CountResult(digit=0, count=7),
        CountResult(digit=1, count=5),
    )


def test_binary_from_list():
    lst = [0, 0, 1, 0, 0]
    assert Binary.from_list(lst) == Binary("00100")


def test_get_gamma_rate_example():
    example_binaries = [
        Binary("00100"),
        Binary("11110"),
        Binary("10110"),
        Binary("10111"),
        Binary("10101"),
        Binary("01111"),
        Binary("00111"),
        Binary("11100"),
        Binary("10000"),
        Binary("11001"),
        Binary("00010"),
        Binary("01010"),
    ]

    answer = 22

    assert get_gamma_rate(example_binaries, TEST_LEN) == answer


def test_get_epsilon_rate_example():
    example_binaries = [
        Binary("00100"),
        Binary("11110"),
        Binary("10110"),
        Binary("10111"),
        Binary("10101"),
        Binary("01111"),
        Binary("00111"),
        Binary("11100"),
        Binary("10000"),
        Binary("11001"),
        Binary("00010"),
        Binary("01010"),
    ]

    answer = 9

    assert get_epsilon_rate(example_binaries, TEST_LEN) == answer


def test_get_power_consumption_example():
    example_binaries = [
        Binary("00100"),
        Binary("11110"),
        Binary("10110"),
        Binary("10111"),
        Binary("10101"),
        Binary("01111"),
        Binary("00111"),
        Binary("11100"),
        Binary("10000"),
        Binary("11001"),
        Binary("00010"),
        Binary("01010"),
    ]

    answer = 198

    assert get_power_consumption(example_binaries, TEST_LEN) == answer


def test_get_oxygen_rating_example():
    example_binaries = [
        Binary("00100"),
        Binary("11110"),
        Binary("10110"),
        Binary("10111"),
        Binary("10101"),
        Binary("01111"),
        Binary("00111"),
        Binary("11100"),
        Binary("10000"),
        Binary("11001"),
        Binary("00010"),
        Binary("01010"),
    ]

    answer = 23

    assert get_oxygen_rating(example_binaries, TEST_LEN) == answer


def test_get_co2_rating_example():
    example_binaries = [
        Binary("00100"),
        Binary("11110"),
        Binary("10110"),
        Binary("10111"),
        Binary("10101"),
        Binary("01111"),
        Binary("00111"),
        Binary("11100"),
        Binary("10000"),
        Binary("11001"),
        Binary("00010"),
        Binary("01010"),
    ]

    answer = 10

    assert get_co2_rating(example_binaries, TEST_LEN) == answer


def test_get_life_support_rating_example():
    example_binaries = [
        Binary("00100"),
        Binary("11110"),
        Binary("10110"),
        Binary("10111"),
        Binary("10101"),
        Binary("01111"),
        Binary("00111"),
        Binary("11100"),
        Binary("10000"),
        Binary("11001"),
        Binary("00010"),
        Binary("01010"),
    ]

    answer = 230

    assert get_life_support_rating(example_binaries, TEST_LEN) == answer
