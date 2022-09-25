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
        '''_summary_

        :param knb: Knob value
        :type knb: str
        :param v: Value for theta
        :type v: int
        :raises ValueError: If knob isn't theta raises Valu  error
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

class SimpleLinkageFunction(LinkageFunction):
    '''
    A greedy and quick linkage function implementing `LinkageFunction`. Takes O(n^2) time and can be improved.
    '''
    def __init__(self, threshold=-1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threshold = threshold

    def _recursive_link(self, parent, links = []):
        # make links between children
        # simple method: O(n^2)
        # better waays to do this and reduct to O(n(log(n)))
        if len(parent.children) > 1:
            for p in itertools.permutations(parent.children):
                p1, p2 = p[0], p[1]
                if p1.value is None or p2.value is None:
                    continue

                d = np.linalg.norm(p1.value - p2.value)
                if (self.threshold < 0 or d < self.threshold) and p2.value <= p1.value:
                    links.append(Edge(from_id=p2.id, to_id=p1.id,
                                weight=d, attributes={
                                    'delta': d,
                                }))

        # Make links between children -> parent
        for c in parent.children:
            if parent.is_root:
                 links.append(Edge(from_id=c.id, to_id=parent.id,
                             weight=1, attributes={}))
                 self._recursive_link(c, links)

            if parent.value is None:
                continue

            d = np.linalg.norm(parent.value - c.value)
            if (self.threshold < 0 or d < self.threshold) and c.value <= parent.value:
                links.append(Edge(from_id=c.id, to_id=parent.id,
                             weight=d, attributes={
                                 'delta': d,
                             }))

            return self._recursive_link(c, links)

        return links

    def link(self, X: HierarchicalGraph):
        '''
        Simple recursive link method to add nodes to Graph.

        :param X: Graph to be linked, needs to be Hierarchical to implement the linking without issues.
        :type X: HierarchicalGraph
        :return: Returns a linked Hierarchical Graph after recursion is finished
        :rtype: HierarchicalGraph
        '''
        return self._recursive_link(X.get_root(), [])
