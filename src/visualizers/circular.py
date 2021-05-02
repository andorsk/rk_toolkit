from visualizer import RKModelVisualizer
import matplotlib.pyplot as plt
import numpy as np
from typing import List
from ..model import Node

class CircularVisualizerSpec():
    '''
    These are specs for the circular visualiation
    They define how close the clsuters are to the
    centroid, the size of the centroid bubble,
    alpha, etc.

    You can compute these dynamically or
    use static fields
    '''

    def __init__(self,
                 center_color='#000000',
                 center_size=300,
                 distance_from_center=10,
                 alpha=.5):
        self.center_color = center_color
        self.center_size = center_size
        self.distance_from_center = distance_from_center
        self.alpha = alpha

class CircularVisualizer(RKModelVisualizer):
    '''
    Cicular Visualizer  visualizes an RKModel
    by plotting clusters and measures in a circular
    pattern in 3D space

    It assumes the RKModel is at least in 3d
    '''

    def __init__(self, spec: CircularVisualizerSpec = None,
                 *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.method = "circular"
        if spec is None:
            spec = CircularVisualizerSpec()
        self.spec = spec

    def build(self, model: RKModel):
        _plot_cluster_centroid(model) # plot the centroid
        placed_nodes = _plot_clusters(model) # plot the clusters
        _plot_links(model, placed_nodes) # plot the links

    def _plot_clusters(self, model):
        '''
        Plots a first level child of an rkmodel

        The first level child is positioned in a cicular
        pattern, incrementing rads through the position in the list.

        The entire RKModel must be built out so the spacing can be
        determined between clusters.
        '''
        nclusters = len(model.hgraph.get_level(1))
        angle_width= 2*np.pi / (nclusters)
        for i in range(nclusters):
            rads = angle_width/(self.ncount() + 1)
            _plot_cluster(model.hgraph.get_parent(i))

    def _plot_links(self, model: RKmodel, placed_nodes: List[Node]):
        pass

    def _plot_cluster(self, cluster, start_angle, end_angle, center):
        angle_v = (end_angle - start_angle) / (len(cluster.nodes()) + 1)
        for i in range(len(cluster.nodes())):
            dangle = start_angle + (angle_v * i)
            center + [0, np.cos(dangle), np.sin(dangle)]

    def _plot_cluster_centroid(self, model):
        pos = self.model.location
        self.ax.scatter(pos[0], pos[1], pos[2],
                        c=self.spec.center_color,
                        s=self.spec.center_size,
                        alpha = self.spec.alpha)

