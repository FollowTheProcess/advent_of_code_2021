"""
--- Day 14: Extended Polymerization ---

The incredible pressures at this depth are starting to put a strain on your submarine.
The submarine has polymerization equipment that would produce suitable materials to reinforce the submarine,
and the nearby volcanically-active caves should even have the necessary input elements in sufficient quantities.

The submarine manual contains instructions for finding the optimal polymer formula; specifically, it offers a polymer
template and a list of pair insertion rules (your puzzle input).

You just need to work out what polymer would result after repeating the pair insertion process a few times.

For example:

NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C

The first line is the polymer template - this is the starting point of the process.

The following section defines the pair insertion rules. A rule like AB -> C means that when elements
A and B are immediately adjacent, element C should be inserted between them.

These insertions all happen simultaneously.

So, starting with the polymer template NNCB, the first step simultaneously considers all three pairs:

The first pair (NN) matches the rule NN -> C, so element C is inserted between the first N and the second N.
The second pair (NC) matches the rule NC -> B, so element B is inserted between the N and the C.
The third pair (CB) matches the rule CB -> H, so element H is inserted between the C and the B.

Note that these pairs overlap: the second element of one pair is the first element of the next pair.
Also, because all pairs are considered simultaneously, inserted elements are not considered
to be part of a pair until the next step.

After the first step of this process, the polymer becomes NCNBCHB.

Here are the results of a few steps using the above rules:

Template:     NNCB
After step 1: NCNBCHB
After step 2: NBCCNBBBCBHCB
After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB

This polymer grows quickly. After step 5, it has length 97; After step 10, it has length 3073. After step 10,
B occurs 1749 times, C occurs 298 times, H occurs 161 times, and N occurs 865 times;
taking the quantity of the most common element (B, 1749) and subtracting the quantity of the least
common element (H, 161) produces 1749 - 161 = 1588.

Apply 10 steps of pair insertion to the polymer template and find the most and least common elements in the result.

What do you get if you take the quantity of the most common element and subtract the
quantity of the least common element?

--- Part Two ---

The resulting polymer isn't nearly strong enough to reinforce the submarine.
You'll need to run more steps of the pair insertion process; a total of 40 steps should do it.

In the above example, the most common element is B (occurring 2192039569602 times) and the least common
element is H (occurring 3849876073 times); subtracting these produces 2188189693529.

Apply 40 steps of pair insertion to the polymer template and find the most and least common elements in the result.

What do you get if you take the quantity of the most common element and subtract the quantity
of the least common element?
"""


from pathlib import Path

# Note: "This polymer grows quickly" is sus
# Part 2 will probably need 100 steps or something so don't
# do it how you think


def get_polymer_template(text: str) -> str:
    """
    Gets the polymer template sequence from the first
    line of `text`.
    """
    return text.strip().splitlines()[0]


def parse_pair_instructions(text: str) -> dict[str, str]:
    """
    Parses the pair instructions from `text` and returns
    them as a dictionary of the pair to look for mapped
    to the value needed to put between them.
    """
    pairs = text.strip().split("\n\n")[-1].splitlines()

    keys = [pair.split(" -> ")[0] for pair in pairs]
    vals = [pair.split(" -> ")[1] for pair in pairs]

    return {k: v for k, v in zip(keys, vals)}


def count_chars(template: str, instructions: dict[str, str], n: int) -> int:
    """
    Counts the characters in the would-be string after `n` steps and
    returns the highest count (most common) - lowest count (least common).

    Args:
        template (str): The polymer template e.g. "NNCB"
        instructions (dict[str, str]): The pair instructions as a dictionary
            e.g. {"CH": "B"} etc.
        n (int): Number of steps.

    Returns:
        int: Most common count - Least common count
    """
    # We don't actually care about the string, just the quantity of pairs
    # if we see a pair, we inject a new letter into the middle according
    # to the instructions, therefore every one of those 2 character pairs becomes 3 characters
    # and 2 new pairs are created
    # e.g. if we see 'CH' and the instruction is CH -> B
    # we create the 3 character sequence: 'CBH'
    # and 2 new pairs: 'CB' and 'BH'

    pair_counts = {pair: template.count(pair) for pair in instructions}
    char_counts = {char: template.count(char) for char in instructions.values()}

    for i in range(n):
        # Take a copy to prevent modifying while iterating
        for pair, value in pair_counts.copy().items():
            # Found the pair e.g. 'CH' which we're going to replace
            # with whatever the instruction says so this pair now occurs
            # 'value' less times (because we replace them all)
            pair_counts[pair] -= value

            # Form the new pair based on the first character of the old
            # and whatever the instructions tell us to put next
            # and increase their count
            pair_counts[pair[0] + instructions[pair]] += value

            # Same for the new pair formed by the now middle
            # replacement character and the last character of the old pair
            pair_counts[instructions[pair] + pair[1]] += value

            # Bump the character counts
            char_counts[instructions[pair]] += value

    answer = max(char_counts.values()) - min(char_counts.values())
    return answer


if __name__ == "__main__":
    HERE = Path(__file__).parent.resolve()
    INPUT = HERE / "day14.txt"

    with open(INPUT) as f:
        input_text = f.read()

    template = get_polymer_template(input_text)
    instructions = parse_pair_instructions(input_text)

    print(f"Part 1: {count_chars(template, instructions, 10)}")
    print()
    print(f"Part 2: {count_chars(template, instructions, 40)}")
