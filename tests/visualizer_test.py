from rk_toolkit.visualizers import CircularVisualizer, CircularVisualizerSpec
from rk_toolkit.models import RKModel

def test_rkmodel_visualizer_circular(): # Tests an rkmodel visaulizer: Circular pattern
    model = RKModel()
    spec = CircularVisualizerSpec()
    visualizer = CircularVisualizer(spec=spec)
    visualizer.build(model)
    visualizer.render()
