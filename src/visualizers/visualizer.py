from ..models import RKModel
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d import Axes3D
import uuid

class RKModelVisualizer():

    def __init__(self, ax=None, fig=None):

        if fig is None:
            fig = plt.figure(dpi=100)

        if ax is None:
            ax = Axes3D(fig)

        if not isinstance(ax, Axes3D):
            raise ValueError("RKModel renders in 3d. Please Make sure to specify a 3d subplot")

        self.fig = fig
        self.ax = ax
        self.id = str(uuid.uuid4())
        self.method = "unspecified"

    def build(self, model: RKmodel):
        raise ValueError("Not implemented!")

    def render(self):
        self.fig.show()


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)
