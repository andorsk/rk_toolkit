from ..models.rkmodel import RKModel
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d import Axes3D
import uuid
from copy import copy, deepcopy

class RKModelVisualizer():
    
    '''
    A user-interface built on top of a particular R-K Pipeline to render each output of the pipeline in sequence along with manual customization options to toggle the lens, range-filters, linkage functions and other boundary conditions necessary to render specific R-K Diagrams from their corresponding R-K Models.

    '''
    def __init__(self, ax=None, fig=None):

        if fig is None:
            fig = plt.figure(dpi=100)

        if ax is None:
            ax = Axes3D(fig)

        if not isinstance(ax, Axes3D):
            raise ValueError("R-K Model renders in 3d. Please Make sure to specify a 3d subplot")

        self.fig = fig
        self.ax = ax
        self.id = str(uuid.uuid4())
        self.method = "unspecified"

    def build(self, models: RKModel):
        '''
        Method to build the visualization for the R-K Model.

        :param models: R-K Model whose R-K Diagram needs to built.
        :type models: RKModel
        '''
        self._build(models[0])

    def render(self):
        '''
        Method to render a R-K Diagram. Utilizes the :code:`pyplot.show()` method.
        '''
        plt.show(block=True)


class Arrow3D(FancyArrowPatch):
    '''
    Builds arrows in 3D. Uses matplotlib's :code:`FancyArrowPatch` class to draw the 3D arrows. 
    '''
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        '''
        Implements the :code:`FancyArrowPatch`'s draw method to draw the arrows. 

        :param renderer: Renderer used for the arrows used by FancyArrowPatch to plot.
        :type renderer: RendererBase
        '''
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

class RKDiagram():
    
    def __init__(self, rkmodel: RKModel, placed_nodes, links):
        self.rkmodel = rkmodel
        self.placed_nodes = placed_nodes
        self.links = links

    def render(self):
        # render specs here are done
        plt.show()
