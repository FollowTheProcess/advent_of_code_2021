import pytest

from src.day10.day10 import (
    calculate_syntax_score,
    complete,
    first_illegal_character,
    get_middle,
)

RAW = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


@pytest.mark.parametrize(
    "line, char",
    [
        ("{([(<{}[<>[]}>{[]{[(<()>", "}"),
        ("[[<[([]))<([[{}[[()]]]", ")"),
        ("[{[{({}]{}}([{[{{{}}([]", "]"),
        ("[<(<(<(<{}))><([]([]()", ")"),
        ("<{([([[(<>()){}]>(<<{{", ">"),
    ],
)
def test_get_first_illegal_character(line: str, char: str):

    assert first_illegal_character(line) == char


def test_score_example_part1():
    lines = RAW.strip().splitlines()

    assert sum(calculate_syntax_score(line) for line in lines) == 26397


@pytest.mark.parametrize(
    "line, completion",
    [
        ("[({(<(())[]>[[{[]{<()<>>", "}}]])})]"),
        ("[(()[<>])]({[<{<<[]>>(", ")}>]})"),
        ("(((({<>}<{<{<>}{[]{[]{}", "}}>}>))))"),
        ("{<[[]]>}<{[{[{[]{()[[[]", "]]}}]}]}>"),
        ("<{([{{}}[<[[[<>{}]]]>[]]", "])}>"),
    ],
)
def test_complete(line: str, completion: str):
    assert complete(line) == list(completion)


def test_score_example_part2():
    lines = RAW.strip().splitlines()

    assert get_middle(lines) == 288957
