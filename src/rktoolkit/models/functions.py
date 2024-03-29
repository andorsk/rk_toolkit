from typing import List
from .graph import Vertex, Edge

'''
Function abstractions
'''
class LocalizationFunction():

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'localize') and callable(subclass.localize))

    def localize(self, X) -> [float]:
        '''
        Predicts the localized position

        :param X: Matrix X to be localized
        :type X: Any
        :return: Returns a list of float
        :rtype: [float]
        '''
        return

    def fit(self):
        '''
        Fits the data
        '''
        pass

class LinkageFunction():
    '''
    A linkage function takes in a list of nodes and returns a list of
    appropriate edges that defines the linkage between those nodes. The math
    behind the linkage function is defined as follows: If G = (V,E) is an
    undirected graph without multiple edges or loops. Let n = \|V \| and e =
    \|E\|. The linkage of G is defined to be the maximum min-degree of any of
    the subgraphs of G (the min-degree of a subgraph is the least degree of any
    of its vertices; the degree of a vertex is taken relative to the subgraph).
    The width of G is defined to be the minimum, over all linear orderings of
    the vertices of G, of the maximum, with respect to any vertex v, of the
    number of vertices connected with v and preceding it in the linear ordering.
    It has also been mathematically proven in Topology that the width of a graph
    is equal to its linkage.

    An example of a linker function is provided in the diagram below in the
    exact way it is applied in an R-K Model. The same linker functions are
    applied to two different graphs, providing directed edges across leafs.
    '''
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'predict') and callable(subclass.link))

    def predict(self, nodes: List[Vertex]) -> List[Edge]: # given a graph the edges
        return []

class FilterFunction():

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'filter') and callable(subclass.filter))

    def filter(self, X) -> bool:
        '''
        Predicts the localized position

        :param X: Matrix X to be localized
        :type X: Any
        :return: Returns a bool
        :rtype: bool
        '''
        return

    def fit(self):
        '''
        Fits the data
        '''
        pass
