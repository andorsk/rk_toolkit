from ..models.functions import LinkageFunction
from ..models.graph import HierarchicalGraph, Edge
import logging
import numpy as np
import itertools

class SimpleLinkageFunction():
    '''
    A greedy linkage function
    '''
    def __init__(self, threshold):
        self.threshold = threshold

    def _recursive_link(self, parent, links = []):
        # make links between children
        # simple method: O(n^2)
        # better waays to do this and reduct to O(n(log(n)))
        for p in itertools.permutations(parent.children):
            p1, p2 = p[0], p[1]
            d = np.linalg.norm(p1.value - p2.value)
            if d < self.threshold and p2.value < p1.value:
                links.append(Edge(from_id=parent.id, to_id=parent.id),
                             weight=d, attributes={
                                 'delta': d,
                             })

        # Make links between children -> parent
        for c in parent.children:
            if parent.value is None:
                logging.warning("No value set. Skipping node for linkage function")
                continue

            d = np.linalg.norm(parent.value - c.value)

            if d < self.threshold and c.value < parent.value:
                links.append(Edge(from_id=parent.id, to_id=parent.id),
                             weight=d, attributes={
                                 'delta': d,
                             })
            return self._recursive_link(c, links)

        return links

    def predict(self, X: HierarchicalGraph):
        return self._link(X.get_root(), [])
