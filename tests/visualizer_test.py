from rktoolkit.visualizers.circular import CircularVisualizer, CircularVisualizerSpec
from rktoolkit.models.graph import RKModel, HierarchicalGraph, TreeNode

def test_rkmodel_visualizer_circular(): # Tests an rkmodel visaulizer: Circular pattern

    measures = TreeNode(parent=None)

    hgraph = HierarchicalGraph(root=measures)
    mass = TreeNode(name="mass_measures", parent=measures)
    m1 = TreeNode(name="mass1", parent=mass)
    m2 = TreeNode(name="mass2", parent=mass)

    [hgraph.add_node(n) for n in [measures, mass, m1, m2]]

    model = RKModel(
        location=[100.0, 100.0, 100.0],
        hgraph=hgraph
    )

    spec = CircularVisualizerSpec()
    visualizer = CircularVisualizer(spec=spec)
    visualizer.build(model)
    visualizer.render()


if __name__ == "__main__":
    test_rkmodel_visualizer_circular()
