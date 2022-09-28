from .graph import *
from .pipeline import RKPipeline
from ..functions.filters import RangeFilter

from ..functions.linkers import SimpleChildLinker
from .graph import Graph, Vertex, Edge

def test_rk_pipeline():
    # TODO: functional tests that tests pipeline transforms
    # more robustly
    structural_graph = build_sample_graph()
    filters, linkers = make_linkers_and_filters(structural_graph)
    pipeline = RKPipeline(filters, linkers, structural_graph)

    # Check if valid node
    v = Vertex(id="vvv")
    assert pipeline.check_valid_node(v) == False

    v.value = 1
    assert pipeline.check_valid_node(v) == True

    model = pipeline.transform(structural_graph)
    pipeline.get_w()


def make_linkers_and_filters(graph, opts={}):
    '''
    Defaults all filters to be a range filter. And the linker to be a simple
    child linker.
    '''
    ENDL = " | "
    filters, linkers = {}, {}
    for k, v in graph.nodes.items():
        if 'value' in v and isinstance(v['value'], numbers.Number):
            if v["id"] in opts:
                print("Set {:s} from options".format(v["id"]), end=ENDL)
            else:
                print("Set {:s} to default".format(v["id"]), end=ENDL)
            minv, maxv = opts.get(v["id"][0], 0), opts.get(v["id"][1], 1)
            filters[k] = RangeFilter(min=minv, max=maxv)
    linkers['root'] = SimpleChildLinker()
    return filters, linkers

def build_sample_graph():
    '''build sample graph'''
    g = Graph()
    root = Vertex('root')
    a = Vertex('a')
    b = Vertex('a')
    root_a = Edge(a, b)
    root_b = Edge(a, b)

    g.add_vertex(root)
    g.add_vertex(a)
    g.add_vertex(b)
    g.add_edge(root_a)
    g.add_edge(root_b)
    return g
