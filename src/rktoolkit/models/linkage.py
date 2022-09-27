from typing import List
from .graph import Edge
from .graph import Node

class LinkageSpec():
    pass

class LinkageFunction():
    '''
    A linkage function takes in a list of nodes and returns a list of appropriate edges that defines the linkage between those nodes. The math behind the linkage function is defined as follows: If G = (V,E) is an undirected graph without multiple edges or loops. Let n = \|V \| and e = \|E\|. The linkage of G is defined to be the maximum min-degree of any of the subgraphs of G (the min-degree of a subgraph is the least degree of any of its vertices; the degree of a vertex is taken relative
    to the subgraph). The width of G is defined to be the minimum, over all linear orderings of the vertices of G, of the maximum, with respect to any vertex v, of the number of vertices connected with v and preceding it in the linear ordering. It has also been mathematically proven in Topology that the width of a graph is equal to its linkage.

    An example of a linker function is provided in the diagram below in the exact way it is applied in an R-K Model. The same linker functions are applied to two different graphs, providing directed edges across leafs.

    '''
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'link') and callable(subclass.link)

    def link(self, nodes: List[Node]) -> List[Edge]: # given a graph the edges
        return []
