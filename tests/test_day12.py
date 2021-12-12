from collections import defaultdict

from src.day12.day12 import Graph


def test_graph_parse():
    text = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

    want = Graph(
        graph=defaultdict(
            set[str],
            {
                "start": {"A", "b"},
                "A": {"start", "b", "end", "c"},
                "b": {"start", "end", "d", "A"},
                "c": {"A"},
                "d": {"b"},
                "end": {"A", "b"},
            },
        )
    )

    assert Graph.parse(text) == want


def test_graph_nodes():
    text = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

    g = Graph.parse(text)

    assert g.nodes() == {"start", "A", "b", "c", "d", "end"}


def test_graph_paths():
    text = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

    want = [
        ["start", "A", "b", "A", "c", "A", "end"],
        ["start", "A", "b", "A", "end"],
        ["start", "A", "b", "end"],
        ["start", "A", "c", "A", "b", "A", "end"],
        ["start", "A", "c", "A", "b", "end"],
        ["start", "A", "c", "A", "end"],
        ["start", "A", "end"],
        ["start", "b", "A", "c", "A", "end"],
        ["start", "b", "A", "end"],
        ["start", "b", "end"],
    ]

    g = Graph.parse(text)

    # Sorted to prevent the test failing just because things
    # are out of order
    assert sorted(g.paths("start", "end")) == sorted(want)
    assert len(g.paths("start", "end")) == 10


def test_graph_paths_larger_example():
    text = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

    g = Graph.parse(text)

    assert len(g.paths("start", "end")) == 19


def test_graph_paths_largest_example():
    text = """fs-end
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
start-RW"""

    g = Graph.parse(text)

    assert len(g.paths("start", "end")) == 226


def test_graph_paths_part2():
    text = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

    g = Graph.parse(text)

    assert len(g.paths_part2("start", "end")) == 36


def test_graph_paths_part2_larger_example():
    text = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

    g = Graph.parse(text)

    assert len(g.paths_part2("start", "end")) == 103


def test_graph_paths_part2_largest_example():
    text = """fs-end
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
start-RW"""

    g = Graph.parse(text)

    assert len(g.paths_part2("start", "end")) == 3509
