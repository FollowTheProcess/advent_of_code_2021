"""
--- Day 10: Syntax Scoring ---

You ask the submarine to determine the best route out of the deep-sea cave, but it only replies:

Syntax error in navigation subsystem on line: all of them
All of them?! The damage is worse than you thought. You bring up a copy of the navigation subsystem (your puzzle input).

The navigation subsystem syntax is made of several lines containing chunks. There are one or more chunks on each line,
and chunks contain zero or more other chunks. Adjacent chunks are not separated by any delimiter;
if one chunk stops, the next chunk (if any) can immediately start.

Every chunk must open and close with one of four legal pairs of matching characters:

If a chunk opens with (, it must close with ).
If a chunk opens with [, it must close with ].
If a chunk opens with {, it must close with }.
If a chunk opens with <, it must close with >.

So, () is a legal chunk that contains no other chunks, as is [].

More complex but valid chunks include ([]), {()()()}, <([{}])>, [<>({}){}[([])<>]], and even (((((((((()))))))))).

Some lines are incomplete, but others are corrupted. Find and discard the corrupted lines first.

A corrupted line is one where a chunk closes with the wrong character - that is, where the characters
it opens and closes with do not form one of the four legal pairs listed above.

Examples of corrupted chunks include (], {()()()>, (((()))}, and <([]){()}[{}]). Such a chunk can appear anywhere
within a line, and its presence causes the whole line to be considered corrupted.

For example, consider the following navigation subsystem:

[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]

Some of the lines aren't corrupted, just incomplete; you can ignore these lines for now.

The remaining five lines are corrupted:

{([(<{}[<>[]}>{[]{[(<()> - Expected ], but found } instead.
[[<[([]))<([[{}[[()]]] - Expected ], but found ) instead.
[{[{({}]{}}([{[{{{}}([] - Expected ), but found ] instead.
[<(<(<(<{}))><([]([]() - Expected >, but found ) instead.
<{([([[(<>()){}]>(<<{{ - Expected ], but found > instead.

Stop at the first incorrect closing character on each corrupted line.

Did you know that syntax checkers actually have contests to see who can get the high score for syntax errors
in a file? It's true! To calculate the syntax error score for a line,
take the first illegal character on the line and look it up in the following table:

): 3 points.
]: 57 points.
}: 1197 points.
>: 25137 points.

In the above example, an illegal ) was found twice (2*3 = 6 points), an illegal ] was found once (57 points),
an illegal } was found once (1197 points), and an illegal > was found once (25137 points).

So, the total syntax error score for this file is 6+57+1197+25137 = 26397 points!

Find the first illegal character in each corrupted line of the navigation subsystem.

What is the total syntax error score for those errors?

--- Part Two ---

Now, discard the corrupted lines. The remaining lines are incomplete.

Incomplete lines don't have any incorrect characters - instead, they're missing some closing characters at the
end of the line. To repair the navigation subsystem, you just need to figure out the sequence of closing
characters that complete all open chunks in the line.

You can only use closing characters (), ], }, or >), and you must add them in the correct order so that only legal
pairs are formed and all chunks end up closed.

In the example above, there are five incomplete lines:

[({(<(())[]>[[{[]{<()<>> - Complete by adding }}]])})].
[(()[<>])]({[<{<<[]>>( - Complete by adding )}>]}).
(((({<>}<{<{<>}{[]{[]{} - Complete by adding }}>}>)))).
{<[[]]>}<{[{[{[]{()[[[] - Complete by adding ]]}}]}]}>.
<{([{{}}[<[[[<>{}]]]>[]] - Complete by adding ])}>.

Did you know that autocomplete tools also have contests? It's true! The score is determined by considering the
completion string character-by-character. Start with a total score of 0. Then, for each character,
multiply the total score by 5 and then increase the total score by the point value given for the
character in the following table:

): 1 point.
]: 2 points.
}: 3 points.
>: 4 points.

So, the last completion string above - ])}> - would be scored as follows:

Start with a total score of 0.
Multiply the total score by 5 to get 0, then add the value of ] (2) to get a new total score of 2.
Multiply the total score by 5 to get 10, then add the value of ) (1) to get a new total score of 11.
Multiply the total score by 5 to get 55, then add the value of } (3) to get a new total score of 58.
Multiply the total score by 5 to get 290, then add the value of > (4) to get a new total score of 294.
The five lines' completion strings have total scores as follows:

}}]])})] - 288957 total points.
)}>]}) - 5566 total points.
}}>}>)))) - 1480781 total points.
]]}}]}]}> - 995444 total points.
])}> - 294 total points.
Autocomplete tools are an odd bunch: the winner is found by sorting all of the scores and then taking the middle score.
(There will always be an odd number of scores to consider.) In this example,
the middle score is 288957 because there are the same number of scores smaller and larger than it.

Find the completion string for each incomplete line, score the completion strings, and sort the scores.

What is the middle score?
"""


from pathlib import Path

# Map of every opening token to it's closer
PAIRS = {"(": ")", "[": "]", "{": "}", "<": ">"}

# Map of the closing tokens to their syntax error score
SYNTAX_SCORES = {")": 3, "]": 57, "}": 1197, ">": 25137}

# Map of the closing tokens to their autocomplete score
COMPLETION_SCORES = {")": 1, "]": 2, "}": 3, ">": 4}


def first_illegal_character(text: str) -> str | None:
    """
    Finds and returns the first illegal character in `text`
    returning None if there no illegal characters.
    """
    stack: list[str] = []

    for char in text:
        if char in PAIRS:
            # If the character is an opening token, push it onto the stack
            stack.append(char)
        else:
            # If the character is a closing token and the stack is empty
            # or if it's not the closing token for what's at the top of the
            # stack, return the character
            if not stack or PAIRS[stack.pop()] != char:
                return char

    return None


def calculate_syntax_score(line: str) -> int:
    """
    Calculates the syntax error score for a line.
    """
    if illegal := first_illegal_character(line):
        return SYNTAX_SCORES[illegal]

    return 0


def complete(line: str) -> list[str]:
    """
    Figures out what tokens you need to complete the line
    and returns them in a list of the right order
    """
    if char := first_illegal_character(line):
        raise ValueError(
            f"Illegal character {char!r} found at index {line.index(char)}"
        )

    # Similar process to before
    stack: list[str] = []
    for char in line:
        if char in PAIRS:
            # If it's an opening token, push it onto the stack
            stack.append(char)
        else:
            # Must be a closing token, if it's not the closing token
            # to whatever is at stack top, we've done something wrong
            if char != PAIRS[stack.pop()]:
                raise ValueError(
                    f"Incorrect closing token: got {char!r}, expected"
                    f" {PAIRS[stack.pop()]}"
                )

    # Flip the stack around and get the closing token for each
    return [PAIRS[char] for char in reversed(stack)]


def calculate_completion_score(completion: list[str]) -> int:
    """
    Calculates the completion score for a line of completions.
    """
    score = 0
    for char in completion:
        score *= 5
        score += COMPLETION_SCORES[char]

    return score


def get_middle(lines: list[str]) -> int:
    """
    Gets the middle completion score.
    """
    scores = [
        calculate_completion_score(complete(line))
        for line in lines
        if first_illegal_character(line) is None
    ]

    # Puzzle says there is always an odd number of scores
    if len(scores) % 2 != 1:
        raise ValueError("Got an even number of scores!")

    return sorted(scores)[len(scores) // 2]


if __name__ == "__main__":
    HERE = Path(__file__).parent.resolve()
    INPUT = HERE / "day10.txt"

    with open(INPUT) as f:
        lines = f.read().strip().splitlines()

        print(f"Part 1: {sum(calculate_syntax_score(line) for line in lines)}")
        print()
        print(f"Part 2: {get_middle(lines)}")
