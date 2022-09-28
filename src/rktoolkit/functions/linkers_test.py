from .linkers import SimpleChildLinker

from ..models.graph import (
    Graph,
    Vertex,
    Edge
)

def build_sample_graph():
    '''build sample graph'''
    g = Graph()
    root = Vertex('root')
    a = Vertex('a', value=1)
    b = Vertex('b', value=2)
    root_a = Edge(root, a)
    root_b = Edge(root, b)

    g.add_vertex(root)
    g.add_vertex(a)
    g.add_vertex(b)
    g.add_edge(root_a)
    g.add_edge(root_b)
    return g

def testSimpleChildLinker():

    linker = SimpleChildLinker(1)
    assert linker.theta == 1

    linker.set_knob("theta", 2)
    assert linker.theta == 2

    g = build_sample_graph()
    assert len(g.edges) == 2

    g2 = linker.link(g)
    assert len(g2.edges) == 3

    linker.set_knob("theta", .1)
    g2 = linker.link(g)
    assert len(g2.edges) == 2

    assert linker.get_knobs().get("theta", None) == .1

