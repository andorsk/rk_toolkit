from .graph import *
from .pipeline import RKPipeline
from ..functions.localizers import IterableLocalizationFunction
from ..functions.linkers import SimpleLinkageFunction
from ..functions.filters import RangeFilter

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from .graph import Graph, Vertex, Edge

'''
TODO: update tests to work with new core
'''
def test_rk_pipeline():

    filtermap = {}
    linkage_map = {}
    structural_graph = {}

    pipeline = RKPipeline(filtermap, linkage_map, structural_graph)

    # Check if valid node
    v = Vertex(id="vvv")
    assert pipeline.check_valid_node(v) == False

    v.add_attribute("value", 1 )
    assert pipeline.check_valid_node(v) == True

    model = pipeline.transform(structural_graph)

    # test remapping
    # test get_w
