
from .graph import (
    Graph,
    Vertex,
    Edge,
    NodeMask
)

from .rkmodel import RKModel

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


def testRKModel():
    g = build_sample_graph()
    assert len(g.nodes) == 3
    m = RKModel(g, ['b'], g.edges)
    assert len(m.get().nodes) == 2
