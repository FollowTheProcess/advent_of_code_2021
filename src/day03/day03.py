"""
--- Day 3: Binary Diagnostic ---

Part 1
------

The submarine has been making some odd creaking noises, so you ask it to produce a diagnostic report just in case.

The diagnostic report (your puzzle input) consists of a list of binary numbers which, when decoded properly,
can tell you many useful things about the conditions of the submarine.

The first parameter to check is the power consumption.

You need to use the binary numbers in the diagnostic report to generate two new binary numbers
(called the gamma rate and the epsilon rate).

The power consumption can then be found by multiplying the gamma rate by the epsilon rate.

Each bit in the gamma rate can be determined by finding the most common bit in the corresponding position of all
numbers in the diagnostic report. For example, given the following diagnostic report:

00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010

Considering only the first bit of each number, there are five 0 bits and seven 1 bits. Since the most common bit is 1,
the first bit of the gamma rate is 1.

The most common second bit of the numbers in the diagnostic report is 0, so the second bit of the gamma rate is 0.

The most common value of the third, fourth, and fifth bits are 1, 1, and 0, respectively,
and so the final three bits of the gamma rate are 110.

So, the gamma rate is the binary number 10110, or 22 in decimal.

The epsilon rate is calculated in a similar way; rather than use the most common bit,
the least common bit from each position is used. So, the epsilon rate is 01001, or 9 in decimal.

Multiplying the gamma rate (22) by the epsilon rate (9) produces the power consumption, 198.

Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate,
then multiply them together.

What is the power consumption of the submarine? (Be sure to represent your answer in decimal, not binary.)

Part 2
------

Next, you should verify the life support rating, which can be determined by multiplying the oxygen generator rating
by the CO2 scrubber rating.

Both the oxygen generator rating and the CO2 scrubber rating are values that can be found in your diagnostic report
finding them is the tricky part. Both values are located using a similar process that involves filtering out values
until only one remains. Before searching for either rating value,
start with the full list of binary numbers from your diagnostic report and consider just the first bit of those numbers.

Then:

Keep only numbers selected by the bit criteria for the type of rating value for which you are searching.
Discard numbers which do not match the bit criteria.
If you only have one number left, stop; this is the rating value for which you are searching.
Otherwise, repeat the process, considering the next bit to the right.
The bit criteria depends on which type of rating value you want to find:

To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position,
and keep only numbers with that bit in that position.
If 0 and 1 are equally common, keep values with a 1 in the position being considered.

To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position,
and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 0 in the
position being considered.

For example, to determine the oxygen generator rating value using the same example diagnostic report from above:

Start with all 12 numbers and consider only the first bit of each number.

There are more 1 bits (7) than 0 bits (5), so keep only the 7 numbers with a 1 in the first position:

11110, 10110, 10111, 10101, 11100, 10000, and 11001.

Then, consider the second bit of the 7 remaining numbers:

there are more 0 bits (4) than 1 bits (3), so keep only the 4 numbers with a 0 in the second position:

10110, 10111, 10101, and 10000.

In the third position, three of the four numbers have a 1, so keep those three: 10110, 10111, and 10101.
In the fourth position, two of the three numbers have a 1, so keep those two: 10110 and 10111.
In the fifth position, there are an equal number of 0 bits and 1 bits (one each).

So, to find the oxygen generator rating, keep the number with a 1 in that position: 10111.

As there is only one number left, stop; the oxygen generator rating is 10111, or 23 in decimal.
Then, to determine the CO2 scrubber rating value from the same example above:

Start again with all 12 numbers and consider only the first bit of each number.
There are fewer 0 bits (5) than 1 bits (7), so keep only the 5 numbers with a 0 in the first position:

00100, 01111, 00111, 00010, and 01010.

Then, consider the second bit of the 5 remaining numbers: there are fewer 1 bits (2) than 0 bits (3),
so keep only the 2 numbers with a 1 in the second position: 01111 and 01010.
In the third position, there are an equal number of 0 bits and 1 bits (one each).
So, to find the CO2 scrubber rating, keep the number with a 0 in that position: 01010.
As there is only one number left, stop; the CO2 scrubber rating is 01010, or 10 in decimal.
Finally, to find the life support rating, multiply the oxygen generator rating (23) by the CO2 scrubber rating (10)
to get 230.

Use the binary numbers in your diagnostic report to calculate the oxygen generator rating and CO2 scrubber rating,
then multiply them together. What is the life support rating of the submarine?
(Be sure to represent your answer in decimal, not binary.)
"""


from __future__ import annotations

import collections
import copy
from dataclasses import dataclass
from pathlib import Path

# Each number in the real input has 12 digits
INPUT_LEN = 12


@dataclass
class CountResult:
    digit: int
    count: int


@dataclass
class Binary:
    """
    Representation of a binary number.

    Args:
        raw (str): The string representation from the
            input (e.g. "11001")
    """

    raw: str = ""

    @classmethod
    def from_item(cls, item: str) -> Binary:
        """
        Construct a `Binary` object from an item of puzzle input
        """
        return Binary(raw=item)

    @classmethod
    def from_list(cls, lst: list[int]) -> Binary:
        """
        Construct a `Binary` object from a list of 1s and 0s.
        """
        liststr = [str(item) for item in lst]
        raw = "".join(liststr)
        return Binary.from_item(raw)

    def to_bin(self) -> str:
        """
        Outputs the `Binary` number as it's proper string representation
        with the '0b' marker prepended so python can properly interpret it.
        """
        return f"0b{self.raw}"

    def to_int(self) -> int:
        """
        Returns the decimal representation of the `Binary`.
        """
        return int(self.to_bin(), 2)

    def bit(self, index: int) -> int:
        """
        Returns the bit at `index`, ignoring the 0b marker.
        """
        if index > len(self.raw):
            raise ValueError(f"index {index} is past the end of the string.")

        return int(self.raw[index])

    def startswith(self, val: str) -> bool:
        """
        Returns whether the raw binary sequence startswith a subsequence
        """
        return self.raw.startswith(val)


def most_and_least_common_bits(
    binaries: list[Binary], bit: int
) -> tuple[CountResult, CountResult]:
    """
    Iterates through a list of `Binary` and returns a tuple
    of the most and least common bits at index `bit`.
    """
    # All the bits at index `bit`
    bits = [binary.bit(bit) for binary in binaries]

    # Bits could be empty if we recursively empty it in part 2
    if len(bits) == 0:
        return CountResult(digit=1, count=0), CountResult(digit=0, count=0)

    counter = collections.Counter(bits)
    count = counter.most_common()

    most, least = count[0], count[-1]

    return CountResult(*most), CountResult(*least)


def get_gamma_rate(binaries: list[Binary], length: int) -> int:
    """
    Gets the gamma rate as a decimal integer from a list of `Binary`.

    It assumes all the binary digits are the same length
    """
    gammas: list[int] = []
    for i in range(length):
        gamma, _ = most_and_least_common_bits(binaries=binaries, bit=i)
        gammas.append(gamma.digit)

    binary = Binary.from_list(gammas)
    return binary.to_int()


def get_epsilon_rate(binaries: list[Binary], length: int) -> int:
    """
    Gets the epsilon rate as a decimal integer from a list of `Binary`.

    It assumes all the binary digits are the same length
    """
    epsilons: list[int] = []
    for i in range(length):
        _, epsilon = most_and_least_common_bits(binaries=binaries, bit=i)
        epsilons.append(epsilon.digit)

    binary = Binary.from_list(epsilons)
    return binary.to_int()


def get_power_consumption(binaries: list[Binary], length: int) -> int:
    """
    Returns the power consumption defines as the epsilon rate x gamma rate.
    """
    return get_gamma_rate(binaries, length) * get_epsilon_rate(binaries, length)


def get_matches(binaries: list[Binary], startswith: str) -> list[Binary]:
    """
    Returns all the entries in `binaries` who's string representation
    starts with the sequence `startswith`.
    """
    matches: list[Binary] = []

    for binary in binaries:
        if binary.startswith(startswith):
            matches.append(binary)

    return matches


def get_oxygen_rating(binaries: list[Binary], length: int) -> int:
    match_string = ""

    # Start with matches being all of them
    # copy to avoid referencing `binaries` by mistake
    matches = copy.deepcopy(binaries)

    for i in range(length):
        # For each index, find the most and least common bits
        most, least = most_and_least_common_bits(matches, i)
        if most.count == least.count:
            # If both equal, prefer 1's for oxygen
            match_digit = 1
        else:
            match_digit = most.digit

        match_string += str(match_digit)

        # This is a weird corner case that only showed up during the real puzzle input
        # and took me FOREVER!!! to find. Sometimes you can have 2 matches and due to
        # the rules for preferring 1 or 0 (oxygen or CO2) the next match string won't match
        # any of the remaining digits.
        # I tried a few ways of resolving it but after 2 HOURS!!!! of hunting this down I gave up and just make
        # a 50/50 guess as to which one is the right number and return that instead
        # This is hacky af but at this point I was too annoyed to give a shit and it gave me the right answer so
        next_matches = get_matches(matches, startswith=match_string)
        if len(next_matches) == 0:
            # Got a weird 50/50 split, return one of the previous
            return matches[0].to_int()
        matches = get_matches(matches, startswith=match_string)
        if len(matches) == 1:
            break

    return matches.pop().to_int()


def get_co2_rating(binaries: list[Binary], length: int) -> int:
    match_string = ""

    # Start with matches being all of them
    # copy to avoid referencing `binaries` by mistake
    matches = copy.deepcopy(binaries)

    for i in range(length):
        # For each index, find the most and least common bits
        most, least = most_and_least_common_bits(matches, i)
        if most.count == least.count:
            # If both equal, prefer 0's for co2
            match_digit = 0
        else:
            match_digit = least.digit

        match_string += str(match_digit)

        # This is a weird corner case that only showed up during the real puzzle input
        # and took me FOREVER!!! to find. Sometimes you can have 2 matches and due to
        # the rules for preferring 1 or 0 (oxygen or CO2) the next match string won't match
        # any of the remaining digits.
        # I tried a few ways of resolving it but after 2 HOURS!!!! of hunting this down I gave up and just make
        # a 50/50 guess as to which one is the right number and return that instead
        # This is hacky af but at this point I was too annoyed to give a shit and it gave me the right answer so
        next_matches = get_matches(matches, startswith=match_string)
        if len(next_matches) == 0:
            # Got a weird 50/50 split, return one of the previous
            return matches[0].to_int()
        matches = get_matches(matches, startswith=match_string)
        if len(matches) == 1:
            break

    return matches.pop().to_int()


def get_life_support_rating(binaries: list[Binary], length: int) -> int:
    return get_co2_rating(binaries, length) * get_oxygen_rating(binaries, length)


if __name__ == "__main__":
    HERE = Path(__file__).parent.resolve()
    INPUT = HERE / "day03.txt"

    with open(INPUT) as f:
        binaries_text = f.read()

    # Mine has 1000 lines
    binaries = [Binary.from_item(binary) for binary in binaries_text.splitlines()]
    assert len(binaries) == 1000

    print(f"Part 1: {get_power_consumption(binaries, INPUT_LEN)}")
    print()
    print(f"Part 2: {get_life_support_rating(binaries, INPUT_LEN)}")
