from .graph import *
from .pipeline import RKPipeline
from ..functions.localization_functions import IterableLocalizationFunction
from ..functions.linkage_functions import SimpleLinkageFunction
from ..functions.filters import StaticFilter

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def test_rk_pipeline():

    root = TreeNode(parent=None, id="root", name="test")
    hgraph = HierarchicalTransformGraph(root=root)
    measures = TreeNode(parent=root, name="measures", id="measures")
    m1 = TreeTransformNode(name="m1", id="m1", parent=measures,
                           attributes={'color':'green'}, transformf=lambda X: X[0]) # we are computing using exsting measures. So we just pass the column
    m2 = TreeTransformNode(name="m2", id="m2", parent=measures,
                           attributes={'color':'green'}, transformf=lambda X: X[1]) # we are computing using exsting measures. So we just pass the column
    m3 = TreeTransformNode(name="m3", id="m3", parent=measures,
                           attributes={'color':'green'}, transformf=lambda X: X[2]) # we are computing using exsting measures. So we just pass the column

    [hgraph.add_node(n) for n in [measures, m1, m2, m3]]
    pipeline = RKPipeline(
        preprocess_nodes = [TreeTransformNode()],
        localization_algorithm = IterableLocalizationFunction(),
        linkage_function = SimpleLinkageFunction(threshold=-1),
        filter_functions = {
            'm1': StaticFilter(max=3), #passes
            'm2': StaticFilter(min=0, max=1) #fails
        },
        hfe=hgraph
    )

    sample_data = [1,2,3]
    rkmodel = pipeline.transform(sample_data)
    rkmodel.name = "p1"

    sample_data = [50,-.5, 30]
    rkmodel2 = pipeline.transform(sample_data)
    rkmodel2.name = "p2"

    from rktoolkit.visualizers.circular import CircularVisualizer, CircularVisualizerSpec

    ax = None
    spec = CircularVisualizerSpec(add_node_labels=True)

    for r in [ rkmodel2, rkmodel]:
        visualizer = CircularVisualizer(spec=spec, ax=ax)
        if ax is None:
            ax = visualizer.ax
        visualizer.build([r])

    visualizer.ax.set_title("Test Render")
    visualizer.ax.set_xlabel("X label")
    visualizer.ax.set_ylabel("Y label")
    visualizer.ax.set_zlabel("Z label")
    visualizer.render()
