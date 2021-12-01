"""
As the submarine drops below the surface of the ocean, it automatically performs a sonar sweep of the nearby sea floor.
On a small screen, the sonar sweep report (your puzzle input) appears:
each line is a measurement of the sea floor depth as the sweep looks further and further away from the submarine.

For example, suppose you had the following report:

199
200
208
210
200
207
240
269
260
263

This report indicates that, scanning outward from the submarine, the sonar sweep found depths of 199, 200, 208, 210
and so on.

The first order of business is to figure out how quickly the depth increases, just so you know what you're dealing with
- you never know if the keys will get carried into deeper water by an ocean current or a fish or something.

To do this, count the number of times a depth measurement increases from the previous measurement.
(There is no measurement before the first measurement.) In the example above, the changes are as follows:

199 (N/A - no previous measurement)
200 (increased)
208 (increased)
210 (increased)
200 (decreased)
207 (increased)
240 (increased)
269 (increased)
260 (decreased)
263 (increased)

In this example, there are 7 measurements that are larger than the previous measurement.

How many measurements are larger than the previous measurement?
"""

from pathlib import Path


def number_of_increases(readings: list[int]) -> int:
    """
    Returns the number of times a reading in `readings` has increased
    relative to the previous value.

    Args:
        readings (list[int]): The list of readings.

    Returns:
        int: Number of increases.
    """
    # Subtract each element from the one before it
    diff = [readings[i] - readings[i - 1] for i in range(1, len(readings))]

    # Now we return the number of positive diffs
    positives = [item for item in diff if item > 0]
    return len(positives)


if __name__ == "__main__":
    HERE = Path(__file__).parent.resolve()
    INPUT = HERE / "day1.txt"

    with open(INPUT) as f:
        readings_text = f.read()

    # My puzzle input has 2000 lines, let's make sure we haven't missed any
    # and cast them to integers
    readings = [int(reading) for reading in readings_text.splitlines()]
    assert len(readings) == 2000

    # Get my actual answer
    print(number_of_increases(readings))
