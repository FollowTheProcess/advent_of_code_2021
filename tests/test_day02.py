from src.day02.day02 import Position

# Note: I've changed the implementation of Position in place for Part 2
# so the below will no longer work for part 1


def test_position_increments():
    # Start at 0
    p = Position()
    assert p.horizontal == 0
    assert p.depth == 0
    assert p.product() == 0

    p.forward(5)
    assert p.horizontal == 5
    assert p.depth == 0
    assert p.product() == 0

    p.up(2)
    assert p.horizontal == 5
    assert p.depth == 0
    assert p.aim == -2
    assert p.product() == 0

    p.down(5)
    assert p.horizontal == 5
    assert p.depth == 0
    assert p.aim == 3
    assert p.product() == 0

    p.forward(6)
    assert p.horizontal == 11
    assert p.depth == 18
    assert p.aim == 3
    assert p.product() == 198


def test_move():
    p = Position()

    p.move("forward 5")

    assert p.horizontal == 5
    assert p.depth == 0
    assert p.aim == 0
    assert p.product() == 0

    p.move("down 6")
    assert p.horizontal == 5
    assert p.depth == 0
    assert p.aim == 6
    assert p.product() == 0

    p.move("up 2")
    assert p.horizontal == 5
    assert p.depth == 0
    assert p.aim == 4
    assert p.product() == 0


def test_movements():
    p = Position()

    p.apply_movements(["down 4", "up 2", "forward 3", "down 1", "forward 5"])

    assert p.horizontal == 8
    assert p.depth == 21
    assert p.aim == 3
    assert p.product() == 168


def test_example_part2_solution():
    example_movements = [
        "forward 5",
        "down 5",
        "forward 8",
        "up 3",
        "down 8",
        "forward 2",
    ]

    answer_position = Position(horizontal=15, depth=60, aim=10)
    answer_product = 900

    p = Position()
    p.apply_movements(example_movements)

    assert p == answer_position
    assert p.product() == answer_product
