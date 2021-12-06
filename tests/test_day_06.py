from src.day06.day06 import State, simulate


def test_state_parse():
    input = "3,4,3,1,2\n"

    assert State.parse(input) == State(current=[3, 4, 3, 1, 2])


def test_get_zeros():
    current = [3, 4, 0, 1, 4, 0, 3, 1, 7, 0]

    # Want the indices of every 0
    want = [2, 5, 9]

    state = State(current=current)
    assert state.get_zeros() == want


def test_next():
    current = [3, 4, 3, 1, 2]

    state = State(current=current)

    assert state.next() == [2, 3, 2, 0, 1]


def test_advance():
    current = [3, 4, 3, 1, 2]

    state = State(current=current)
    state.advance()

    assert state.current == [2, 3, 2, 0, 1]


def test_next_series_example():

    start = [3, 4, 3, 1, 2]

    # The intermediate states from the example
    want = [
        [2, 3, 2, 0, 1],
        [1, 2, 1, 6, 0, 8],
        [0, 1, 0, 5, 6, 7, 8],
        [6, 0, 6, 4, 5, 6, 7, 8, 8],
        [5, 6, 5, 3, 4, 5, 6, 7, 7, 8],
        [4, 5, 4, 2, 3, 4, 5, 6, 6, 7],
        [3, 4, 3, 1, 2, 3, 4, 5, 5, 6],
        [2, 3, 2, 0, 1, 2, 3, 4, 4, 5],
        [1, 2, 1, 6, 0, 1, 2, 3, 3, 4, 8],
        [0, 1, 0, 5, 6, 0, 1, 2, 2, 3, 7, 8],
        [6, 0, 6, 4, 5, 6, 0, 1, 1, 2, 6, 7, 8, 8, 8],
        [5, 6, 5, 3, 4, 5, 6, 0, 0, 1, 5, 6, 7, 7, 7, 8, 8],
        [4, 5, 4, 2, 3, 4, 5, 6, 6, 0, 4, 5, 6, 6, 6, 7, 7, 8, 8],
        [3, 4, 3, 1, 2, 3, 4, 5, 5, 6, 3, 4, 5, 5, 5, 6, 6, 7, 7, 8],
        [2, 3, 2, 0, 1, 2, 3, 4, 4, 5, 2, 3, 4, 4, 4, 5, 5, 6, 6, 7],
        [1, 2, 1, 6, 0, 1, 2, 3, 3, 4, 1, 2, 3, 3, 3, 4, 4, 5, 5, 6, 8],
        [0, 1, 0, 5, 6, 0, 1, 2, 2, 3, 0, 1, 2, 2, 2, 3, 3, 4, 4, 5, 7, 8],
        [6, 0, 6, 4, 5, 6, 0, 1, 1, 2, 6, 0, 1, 1, 1, 2, 2, 3, 3, 4, 6, 7, 8, 8, 8, 8],
    ]

    # Start at the beginning, the next state should be the next
    # thing in want
    state = State(start)
    for i, item in enumerate(want):
        state.advance()
        assert state.current == item


def test_simulate_example_part1():
    start = [3, 4, 3, 1, 2]

    assert simulate(start, 18) == 26
    assert simulate(start, 80) == 5934
