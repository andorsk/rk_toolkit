import copy
import numbers
from .graph import Edge, NodeMask

class RKModel():
    
    def __init__(self, G, mask, edges):
        self.G = G
        self.mask = mask
        self.edges = edges

    def get(self):
        '''
        Get the Graph for RKModel

        :return: Returns the graphmask for the RKModel
        :rtype: GraphMask
        '''
        gC = copy.deepcopy(self.G)
        for k,v in self.edges.items():
            gC.add_edge(Edge(*k, attributes=v))
        return NodeMask(nmasks=self.mask).fit(gC)
