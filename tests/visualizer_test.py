from rktoolkit.visualizers.circular import CircularVisualizer, CircularVisualizerSpec
from rktoolkit.models.graph import RKModel, HierarchicalGraph, TreeNode

def test_rkmodel_visualizer_circular(): # Tests an rkmodel visaulizer: Circular pattern

    measures = TreeNode(parent=None)

    hgraph = HierarchicalGraph(root=measures)
    mass = TreeNode(name="mass_measures", parent=measures, attributes={'size': 5})
    m1 = TreeNode(name="mass1", parent=mass, attributes={'color':'green'})
    m2 = TreeNode(name="mass2", parent=mass, attributes={'color': 'orange'})

    spin = TreeNode(name="spin_measures", parent=measures, attributes={'size': 5})
    s1 = TreeNode(name="spin1", parent=spin, attributes={'color':'pink'})
    s2 = TreeNode(name="spin2", parent=spin, attributes={'color': 'yellow'})
    s3 = TreeNode(name="spin3", parent=spin, attributes={'color': 'green'})
    s4 = TreeNode(name="spin4", parent=spin, attributes={'color': 'red'})

    lin = TreeNode(name="lin_measures", parent=measures, attributes={'size': 5})
    l1 = TreeNode(name="lin1", parent=lin, attributes={'color':'pink'})
    l2 = TreeNode(name="lin2", parent=lin, attributes={'color': 'yellow'})

    h1 = TreeNode(name="h1", parent=measures, attributes={'size': 5})
    h2 = TreeNode(name="h2", parent=h1, attributes={'color':'pink'})
    h3 = TreeNode(name="h3", parent=h1, attributes={'color': 'yellow'})

    [hgraph.add_node(n) for n in [measures, mass, m1, m2, spin, s1, s2, s3, s4, l1, l2, lin, h1, h2, h3]]

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
