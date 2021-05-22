from .graph import *
from .pipeline import RKPipeline
from ..functions.localization_functions import IterableLocalizationFunction
from ..functions.linkage_functions import SimpleLinkageFunction
from ..functions.filters import StaticFilter

def test_rk_pipeline():

    measures = TreeNode(parent=None)
    hgraph = HierarchicalTransformGraph(root=measures)

    m1 = TreeTransformNode(name="m1", id="m1", parent=measures,
                           attributes={'color':'green'}, predictf=lambda X: X[:,0]) # we are computing using exsting measures. So we just pass the column
    m2 = TreeTransformNode(name="m2", id="m2", parent=measures,
                           attributes={'color':'green'}, predictf=lambda X: X[:,1]) # we are computing using exsting measures. So we just pass the column
    m3 = TreeTransformNode(name="m3", id="m3", parent=measures,
                           attributes={'color':'green'}, predictf=lambda X: X[:,2]) # we are computing using exsting measures. So we just pass the column

    [hgraph.add_node(n) for n in [m1, m2, m3]]

    pipeline = RKPipeline(
        preprocess_nodes = [TreeTransformNode()],
        localization_algorithm = IterableLocalizationFunction(),
        linkage_function = SimpleLinkageFunction(threshold=-1),
        filter_functions = {
            'm1': StaticFilter(max=2)
        },
        hfe=hgraph
    )

    sample_data = [1,2,3]
    rkmodel = pipeline.transform(sample_data)
    print(rkmodel)
