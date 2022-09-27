from .graph import *
from .pipeline import RKPipeline
from ..functions.localizers import IterableLocalizationFunction
from ..functions.linkers import SimpleLinkageFunction
from ..functions.filters import RangeFilter

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

'''
TODO: update tests to work with new core
'''
def test_rk_pipeline():

    filtermap = {}
    linkage_map = {}
    structural_graph = {}

    pipeline = RKPipeline(filtermap, linkage_map, structural_graph)
