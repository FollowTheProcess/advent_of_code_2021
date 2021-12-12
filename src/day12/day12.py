r"""
--- Day 12: Passage Pathing ---

With your submarine's subterranean subsystems subsisting suboptimally, the only way you're getting out
of this cave anytime soon is by finding a path yourself.
Not just a path - the only way to know if you've found the best path is to find all of them.

Fortunately, the sensors are still mostly working, and so you build a rough map of the remaining caves
(your puzzle input). For example:

start-A
start-b
A-c
A-b
b-d
A-end
b-end

This is a list of how all of the caves are connected. You start in the cave named start,
and your destination is the cave named end.
An entry like b-d means that cave b is connected to cave d - that is, you can move between them.

So, the above cave system looks roughly like this:

    start
    /   \
c--A-----b--d
    \   /
     end

Your goal is to find the number of distinct paths that start at start, end at end, and don't visit small caves
more than once. There are two types of caves: big caves (written in uppercase, like A)
and small caves (written in lowercase, like b).
It would be a waste of time to visit any small cave more than once, but big caves are large enough
that it might be worth visiting them multiple times.
So, all paths you find should visit small caves at most once, and can visit big caves any number of times.

Given these rules, there are 10 paths through this example cave system:

start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end
(Each line in the above list corresponds to a single path; the caves visited by that path are listed
in the order they are visited and separated by commas.)

Note that in this cave system, cave d is never visited by any path: to do so, cave b would need to be visited
twice (once on the way to cave d and a second time when returning from cave d),
and since cave b is small, this is not allowed.

Here is a slightly larger example:

dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc

The 19 paths through it are as follows:

start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end

Finally, this even larger example has 226 paths through it:

fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW

How many paths through this cave system are there that visit small caves at most once?

--- Part Two ---

After reviewing the available paths, you realize you might have time to visit a single small cave twice.
Specifically, big caves can be visited any number of times, a single small cave can be visited at most twice,
and the remaining small caves can be visited at most once.
However, the caves named start and end can only be visited exactly once each: once you leave the start cave,
you may not return to it, and once you reach the end cave, the path must end immediately.

Now, the 36 possible paths through the first example above are:

start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,end
start,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,end
start,b,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end

The slightly larger example above now has 103 paths through it, and the even larger
example now has 3509 paths through it.

Given these new rules, how many paths through this cave system are there?
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Graph:
    # Map of a node to all of it's direct connected nodes
    graph: defaultdict[str, set[str]]

    @classmethod
    def parse(cls, text: str) -> Graph:
        """
        Parse a graph from the puzzle input
        """
        connections = text.strip().splitlines()
        froms = [con.split("-")[0] for con in connections]
        tos = [con.split("-")[1] for con in connections]

        mapping: defaultdict[str, set[str]] = defaultdict(set[str])

        for cave1, cave2 in zip(froms, tos):
            mapping[cave1].add(cave2)
            mapping[cave2].add(cave1)

        return Graph(graph=mapping)

    def nodes(self) -> set[str]:
        """
        Get all the nodes in the `Graph`.
        """
        return {key for key in self.graph.keys()}

    def paths(self, start: str, end: str) -> list[list[str]]:
        """
        Find all paths from `start` to `end` in the graph,
        visiting "small" nodes only once and "large" nodes
        any number of times.
        """
        # If either start or end not in the graph, error out
        if start not in self.nodes():
            raise ValueError(f"Starting node: {start} not in the graph")

        if end not in self.nodes():
            raise ValueError(f"Ending node: {end} not in the graph")

        paths: list[list[str]] = []
        front = [[start]]

        while front:
            path = front.pop()
            cave = path[-1]

            if cave == end:
                paths.append(path)
            else:
                for next in self.graph[cave]:
                    if next not in path or next.isupper():
                        front.append(path + [next])

        return paths

    def paths_part2(self, start: str, end: str) -> list[list[str]]:
        """
        Same as `paths` but with the new part 2 constraints.
        """
        # If either start or end not in the graph, error out
        if start not in self.nodes():
            raise ValueError(f"Starting node: {start} not in the graph")

        if end not in self.nodes():
            raise ValueError(f"Ending node: {end} not in the graph")

        paths: list[list[str]] = []
        lowers = {
            cave for cave in self.graph if cave.islower() and cave not in (start, end)
        }
        front = [[start]]

        while front:
            path = front.pop()

            cave = path[-1]

            if cave == end:
                paths.append(path)
            else:
                for next in self.graph[cave]:
                    small_repeats = [cave for cave in lowers if path.count(cave) > 1]
                    if (
                        next.isupper()
                        or (not small_repeats and next != start)
                        or (next not in path)
                    ):
                        front.append(path + [next])

        return paths


if __name__ == "__main__":
    HERE = Path(__file__).parent.resolve()
    INPUT = HERE / "day12.txt"

    with open(INPUT) as f:
        input_text = f.read()

    graph = Graph.parse(input_text)

    print(f"Part 1: {len(graph.paths('start', 'end'))}")
    print()
    print(f"Part 2: {len(graph.paths_part2('start', 'end'))}")
