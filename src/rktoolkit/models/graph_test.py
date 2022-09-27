# graph test
from .graph import Graph, Vertex, Edge
import pytest


root = Vertex(id="root")
A = Vertex(id="a")
B = Vertex(id="b")
A_B = Edge(u=A, v=B)

def test_node_masks():
    pass

def test_graph():
    '''
    Graph Tests
    '''
    g = Graph(id="theid")
    g.add_vertex(A)
    g.add_vertex(B)

    with pytest.raises(ValueError):
        g.add_vertex("bad")

    g.add_edge(A_B)
    with pytest.raises(ValueError):
        g.add_edge("bad")


    print(g.sort())
    assert g.validate() == True
    assert g.is_dag() == True

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
