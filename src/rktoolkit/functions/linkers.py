from ..models.functions import LinkageFunction
from ..models.graph import HierarchicalGraph, Edge
import logging
import numpy as np
import itertools
from typing import Optional
import copy
import numbers

class SimpleChildLinker():
    '''
    A simple leaf-linker function is provided in the R-K Toolkit which can be used to build a specific R-K model based on the choice of lens and application. The simple leaf linker compares only the leafs of a graph tree, and provides an edge E in the case the euclidean distance is less than the specified threshold. Thus a Leaf Linker function compares the distances between values with ϵ < θ, and links the leafs of the final clusters based upon the set threshold.
    '''

    def __init__(self, theta=1):
        self.theta = theta

    def get_knobs(self):
        '''
        Get the knobs to link.

        :return: Knob
        :rtype: dict
        '''
        return {"theta": self.theta}

    def set_knob(self, knb, v):
        '''
        Set the knobs for linking.

        :param knb: Knob value
        :type knb: str
        :param v: Value for theta
        :type v: int
        :raises ValueError: If knob isn't theta raises Value  error
        '''
        if knb == "theta":
            self.theta = v
        else:
            raise ValueError("No knob {}".format(knb))

    def check_valid_node(self, node) -> bool:
        '''
        Checks if node contains value or not 

        :param node: Node to be checked for validity
        :type node: Any
        :return: Returns  true if Node is valid, else false
        :rtype: bool
        '''
        if "value" not in node:
            return False
        if not isinstance(node["value"], numbers.Number):
            return False
        return True

    def link(self, G):
        '''
        Links the nodes of the given Graph by creating a copy of the graph  and adding nodes to it based on criteria

        :param G: Graph to be linked.
        :type G: Graph
        :return: A linked graph with all child nodes linked.
        :rtype: Graph
        '''
        gC = copy.deepcopy(G)
        for n in G.nodes:
            for p in itertools.combinations(G.get_children(n), 2):
                if len(p) < 2:
                    continue
                if not self.check_valid_node(G.nodes[p[0]]) or not self.check_valid_node(G.nodes[p[1]]):
                    continue
                u_v, v_v = G.nodes[p[0]]["value"], G.nodes[p[1]]["value"]
                d = np.linalg.norm(u_v - v_v)
                if d < self.theta:
                    fn = 0 if u_v < v_v else 1
                    tn = 1 ^ fn
                    gC.add_edge(Edge(u=p[fn], v=p[tn], attributes={"edge_distance": d}))
        return gC

