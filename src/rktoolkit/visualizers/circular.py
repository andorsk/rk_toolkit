from .visualizer import RKModelVisualizer, RKDiagram
import matplotlib.pyplot as plt
import numpy as np
from typing import List
from ..models.graph import Node, GraphMask
from ..models.rkmodel import RKModel
import copy
import logging

'''

Cicular Visualizer Makes an almost "Mandlebot" like visualization
of the RKModel.

How it works: based on the center, and relative number of children nodes,
it expands outward using a circular pattern. As the expansion continues,
children birth more children in circular patterns.

The distance and sizes of of the node between each parent -> child in the visualization
decreases each iteration.

You can override any particular value using the attributes of a node.
'''
class CircularVisualizerSpec():
    '''
    These are specs for the circular visualiation
    They define how close the clsuters are to the
    centroid, the size of the centroid bubble,
    alpha, etc.

    You can compute these dynamically or
    use static fields. Initialization specs are::

    :param center_color: Color for center in unicode, defaults to '#000000'
    :type center_color: str 
    :param center_size:  Size of the center node, defaults to 300
    :type center_size: int
    :param distance_from_center: Distance of nodes from center, defaults to 10.
    :type distance_from_center: int
    :param cluster_size: Size of the cluster, defaults to 10.
    :type cluster_size: int
    :param add_node_labels: To check if nodes need to be labelled or not,defaults to False.
    :type add_node_labels: bool
    :param alpha: Alpha index value, defaults to .5.
    :type alpha: float   
    '''

    def __init__(self,
                 center_color='#000000',
                 center_size=300,
                 distance_from_center=10,
                 cluster_size=10,
                 add_node_labels = False,
                 alpha=.5):
        self.center_color = center_color
        self.center_size = center_size
        self.distance_from_center = distance_from_center
        self.alpha = alpha
        self.cluster_size = cluster_size
        self.add_node_labels = add_node_labels

class CircularVisualizer(RKModelVisualizer):
    '''
    Cicular Visualizer  visualizes an RKModel
    by plotting clusters and measures in a circular
    pattern in 3D space

    It assumes the RKModel is at least in 3d
    TODO: Visualizer only gives locations and specs.
    RK-Diagram Renderer renders the specs
    '''
    def __init__(self, spec: CircularVisualizerSpec = None,
                 *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.method = "circular"
        if spec is None:
            spec = CircularVisualizerSpec()
        self.spec = spec
        self.positions = {}

    def _build(self, model: List[RKModel]):
        '''
        Builds a Visualization of the RKModel.

        :param model: RKModel(s) to be visualized.
        :type model: List[RKModel]
        :raises e: If RKModel is unable to be created, returns an exception.
        :return: An RKDiagram visualization .
        :rtype: RKDiagram
        '''
        try:
            self._plot_cluster_centroid(model) # plot the centroid
            placed_nodes = self._plot_clusters(model) # plot the clusters
            links = self._plot_links(model, model.mask) # plot the links
            return RKDiagram(rkmodel=model, placed_nodes=placed_nodes,
                                links=links)
        except Exception as e:
            print("Failed to create model")
            raise e

    def _register_node(self, node, pos):
        '''
        Register the nodes' positions for plotting.
        '''
        self.positions[node.id] = pos

    def _get_node_position(self, node) -> []:
        '''
        Get the position of the node to be used for plotting

        :param node: The node whose position is needed.
        :type node: Any
        :return: Position of the node
        :rtype: List
        '''
        return self.positions.get(node.id, None)

    def _plot_children(self, parent, mask=None, level=1):
        '''Plots a first level child of an rkmodel

        The first level child is positioned in a cicular
        pattern, incrementing rads through the position in the list.

        The entire RKModel must be built out so the spacing can be
        determined between clusters.Plots a first level child of an rkmodel

        The first level child is positioned in a cicular
        pattern, incrementing rads through the position in the list.

        The entire RKModel must be built out so the spacing can be
        determined between clusters.

        :param parent: Parent node (Starting node) from where the children should be plotted.
        :type parent: Any
        :param mask: Any child nodes to be masked, defaults to None
        :type mask: GraphMask, optional
        :param level: Child nodes level, defaults to 1
        :type level: int, optional
        :raises ValueError: Raises a ValueError if Parent node's position hasn't been placed i.e, not in positions list.
        '''
        children_unmasked = parent.children
        children_masked = []
        for i, l in enumerate(children_unmasked):
            if mask is None or not mask.node_is_masked(l.id):
                children_masked.append(l)

        # TODO: Add mask
        if children_masked is None or len(children_masked) == 0:
            return

        angle_width= 2 * np.pi / (len(children_masked))
        for i, node in enumerate(children_masked):
            if node.parent.id not in self.positions:
                raise ValueError("parent id must have been placed.\
                Something is wrong.")

            pos = copy.copy(self._get_node_position(node.parent))
            dangle = (i * angle_width)
            dist = self.spec.distance_from_center / level
            offset = [0, np.cos(dangle) * dist, np.sin(dangle) * dist]
            pos = [pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2]]
            self.ax.plot([pos[0]], [pos[1]], [pos[2]],
                         marker='o', markersize=node.attributes.get('size', 10) / level,
                         color=node.attributes.get("color", "blue"))
            if self.spec.add_node_labels:
                self.ax.text(pos[0], pos[1], z=pos[2], s= node.id)
            self._register_node(node, pos)
            self._plot_children(node, mask, level+1)

    def _plot_links(self, model: RKModel, mask: GraphMask = None):
        '''
        Plots the links between the nodesplots the links between the nodes

        :param model: The RKModel for which links need to be plotted for the nodes.
        :type model: RKModel
        :param mask: Nodes that are/need to be masked, defaults to None
        :type mask: GraphMask, optional
        :raises ValueError: Raises ValueError if no links are provided in the RKModel.
        '''
        if model.links is None:
            raise ValueError("No links provided")

        links = model.links

        for l in links:

            if mask is not None and mask.edge_is_masked(l.id):
                # skipped masked edges
                continue

            if l.from_id not in self.positions:
                logging.warning("Warning. {} not in registered positions.\
                Skipping".format(l.from_id))
                continue

            if l.to_id not in self.positions:
                logging.warning("Warning. {} not in registered positions.\
                Skipping".format(l.from_id))
                continue

            fr = self.positions[l.from_id]
            to = self.positions[l.to_id]
            x = np.array((fr[0], to[0]))
            y = np.array((fr[1], to[1]))
            z = np.array((fr[2], to[2]))
            self.ax.plot(x, y, z, c='black', alpha=0.5)

    def _plot_clusters(self, model):
        '''
        Plot the clusters of the RKModel

        :param model: The RKModel whose clusters need to be plotted.
        :type model: RKModel
        '''
        self._plot_children(model.hgraph.get_root(), model.mask)

    def _plot_cluster_centroid(self, model):
        '''
        Plot the centroid of the clusters of RKModel

        :param model: The RKModel whose centroid needs to be plotted
        :type model: RKModel
        :raises ValueError: Raises ValueError if no model position is available for centroid.
        '''
        pos = model.location
        if pos == None or len(pos) < 3:
            raise ValueError("No model position")
        self._register_node(model.hgraph.get_root(), pos)
        self.ax.plot([pos[0]], [pos[1]], [pos[2]],
                     marker='o',
                     markersize=10,
                     color=self.spec.center_color,
                     alpha = self.spec.alpha)

        if self.spec.add_node_labels:
                self.ax.text(pos[0], pos[1], z=pos[2], s=model.name)
