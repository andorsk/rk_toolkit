# graph test
from .graph import Graph, Vertex, Edge
import pytest

def make_graph_components():
    root = Vertex(id="root")
    A = Vertex("a")
    B = Vertex("b")
    C = Vertex("c")

    A_B = Edge(A, B)
    A_C = Edge(A, C)
    root_A = Edge(root, A)
    return [root, A, B, C], [A_B, A_C, root_A]


def test_node_masks():
    pass

def test_graph():
    comp = make_graph_components()
    g = Graph()
    for n in comp[0]:
        g.add_vertex(n)

    assert len(g.nodes) == 4

    with pytest.raises(ValueError):
        g.add_vertex("bad")

    # no edges yet. not connected
    with pytest.raises(ValueError):
        g.validate()

    for e in comp[1]:
        g.add_edge(e)

    assert len(g.nodes) == 4
    assert len(g.edges) == 3

    with pytest.raises(ValueError):
        g.add_edge("bad")

    assert g.is_dag() == True
    assert g.is_connected() == True
    assert g.validate() == True

def test_edge():
    attrs = {
        "a": 1,
        "b": 2,
    }

    e = Edge(u="a", v="b", w=1, type="mytype", attributes=attrs)
    assert e.to_dict()[0] == "a"
    assert e.to_dict()[1] == "b"
    assert e.to_dict()[2].get("a") == 1

def test_vertex():
    a = Vertex(id="a")
    a.add_attribute("attr1", 1)
    with pytest.raises(ValueError):
        a.add_attribute("id", "bad")
    assert a.to_dict().get("id", None) == "a"
