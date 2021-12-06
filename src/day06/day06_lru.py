"""
My first solution worked totally fine for part 1, but exploded my RAM on part 2!

So here I played around for ages using numpy and all sorts of crap to get it
to work without incinerating my laptop, all to no avail.

So I confess to a bit of cheating, I looked at the subreddit for some help.
In my head the cheating is fine because my logic was correct but my implementation
needed optimising 👀
"""

from functools import lru_cache
from pathlib import Path

TIMER_START = 6
NEW_FISH_TIMER = TIMER_START + 2


@lru_cache
def simulate(population: int, n: int, timer: int) -> int:
    """
    Recursively simulate population growth of the fish.

    Args:
        population (int): Starting population
        n (int): Number of days to simulate.
        timer (int): The reset timer of the fish
            initialised at 6 or 8 depending on whether
            it's newborn, and decremented on each round.

    Returns:
        int: The population of fish after `n` days
    """
    if n == 0:
        # It's the start
        return population
    if timer == 0:
        # A fish's timer has reached 0
        # create required new fish
        newborns = simulate(population, n - 1, NEW_FISH_TIMER)
        current = simulate(population, n - 1, TIMER_START)
        return current + newborns

    return simulate(population, n - 1, timer - 1)


if __name__ == "__main__":
    HERE = Path(__file__).parent.resolve()
    INPUT = HERE / "day06.txt"

    with open(INPUT) as f:
        line = f.readline()
        ages = [int(n) for n in line.split(",")]

    total = sum(simulate(1, 256, age) for age in ages)

    print(f"Part 2: {total}")
