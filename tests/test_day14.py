from src.day14.day14 import count_chars, get_polymer_template, parse_pair_instructions

RAW = """NNCB

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
CN -> C"""


def test_get_polymer_template():
    assert get_polymer_template(RAW) == "NNCB"


def test_parse_pair_instructions():
    pairs = parse_pair_instructions(RAW)

    assert pairs == {
        "CH": "B",
        "HH": "N",
        "CB": "H",
        "NH": "C",
        "HB": "C",
        "HC": "B",
        "HN": "C",
        "NN": "C",
        "BH": "H",
        "NC": "B",
        "NB": "B",
        "BN": "B",
        "BB": "N",
        "BC": "B",
        "CC": "N",
        "CN": "C",
    }


def test_example_part1():
    template = get_polymer_template(RAW)
    instructions = parse_pair_instructions(RAW)

    assert count_chars(template, instructions, 10) == 1588


def test_example_part2():
    template = get_polymer_template(RAW)
    instructions = parse_pair_instructions(RAW)

    assert count_chars(template, instructions, 40) == 2188189693529
