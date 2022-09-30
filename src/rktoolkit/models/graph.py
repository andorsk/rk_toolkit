# Maintainer: andor@henosisknot.com
# Main graph class
from networkx.classes.digraph import DiGraph
import networkx as nx
import copy
import numbers
from ..functions.distance import jaccard, mahalanobis
from pydantic import BaseModel
from enum import Enum
from typing import List, Optional, Callable, Any
import uuid
from copy import deepcopy, copy

class NodeMask():
    '''
    A graph mask is a mask over an existing structural graph. It essentially
    provides an overlay representation, which can be used to filter out
    particular nodes and edges. Typically,a mask over a node, should also mask
    child-nodes associated with it. A node mask represents a masking structure
    that when applied to a structural graph S, reduces the number of nodes into
    a subgraph S. Node masks in the R-K Model are binary operators, which when
    set to true, filter a node and its direct children. To derive the node
    masks, we produce a set of filters Fn(G), which takes in a graph and returns
    a mask.
    '''

    def __init__(self, nmasks=[], emasks=[]):
        self._nmask = set(nmasks)
        self._emask = set(emasks)

    def get_nmasks(self, n):
        return self._nmask

    def get_emasks(self, n):
        return self._emask

    def fit(self, G):
        sgraph = self._nmask ^ set(list(G.nodes.keys()))
        mG = G.__class__()
        mG.add_nodes_from((n, G.nodes[n]) for n in sgraph)
        for e in list(G.edges):
            if e[0] in sgraph and e[1] in sgraph:
                mG.add_edges_from([e])

        edges = dict(mG.edges.items())
        for e in self._emask:
            if e in edges:
                mG.remove_edge(*e)
        return mG

class Graph(DiGraph):

    '''
    Excerpt from initial `paper <https://arxiv.org/pdf/2201.06923.pdf>`_ :

    It is important to note, that in the field of Graph Theory,
    the term "graph" does not refer to data charts, such as
    the likes of line graphs or bar graphs pertaining to the
    graphical visualization of data. Instead, it refers to a set
    of Vertices (V) (i.e., points or nodes) and Edges (E) (or
    lines) that connect the vertices. When any two vertices
    are joined by more than one edge, then such a graph is
    called a "Multi-graph". [11][86] A graph without any
    loops and with a maximum of one edge between any
    two vertices is called a simple graph. When each and
    every vertex of a graph is connected by an edge to every other vertex, then such a graph is called a complete
    graph. Moreover, it is important to note in the context
    of this paper, a direction is assigned to each edge of a
    graph to produce what is known as a Directed Graph
    or Digraph.[50] We shall be dealing with such Directed
    Graphs for the remaining part of this paper.

    NOT threadsafe

    TODO: Add more documentation around usage
    TODO: More tests coverage
    '''
    def __init__(self, id=None, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.id = id

    def add_vertex(self, n):
        '''
        Adds a vertex to the graph for the given node. Must be a vertex type to be added successfully.

        :param n: Node vertex to be added to the graph.
        :type n: Vertex
        :raises ValueError: Raises an error if the input is not of the Vertex Type
        '''
        if isinstance(n, Vertex):
            super().add_nodes_from([(n.id, n.to_dict())])
        else:
            raise ValueError("Expected a Vertex Type")

    def add_edge(self, e):
        '''
        Adds an edge to the graph for the given node. Must be an Edge type to be added successfully.

        :param e: Edge  node to be added to the graph.
        :type e: Edge
        :raises ValueError: Raises an error if the input is not of the Edge Type
        '''
        if isinstance(e, Edge):
            d = e.to_dict()
            u = d[0]
            v = d[1]
            if isinstance(u, Vertex):
                u = u.id
            if isinstance(v, Vertex):
                v = v.id
            super().add_edges_from([(u, v, d[2])])
        else:
            raise ValueError("Expected a Edge Type")

    def get_children(self, node_id, recursive=False):
        '''
        Get the children nodes of the given node.

        :param node_id: ID of the node whose children needs to be found
  dojjkkk      :type node_id: str
        :param recursive: Condition to choose if the child nodes be found recursively till leaf node, defaults to False
        :type recursive: bool, optional
        :return: Returns all nodes reachable from the given node ID.
        :rtype: set(recursive) OR list(non-recursive)
        '''
        if recursive:
            return nx.descendants(self, node_id)
        else:
            return list(self.successors(node_id))

    def validate(self):
        '''
        Validate if the graph is fully connected, if Yes, find the cycles and return True. Else raise exceptions

        :raises ValueError: Raises ValueError if graph is not connected
        :raises ValueError: Raises ValueError if it's not a DAG
        :raises e: Raises exception 'e' if cycles can not be found.
        :return: Returns True if fully connected.
        :rtype: bool
        '''
        try:
            if not self.is_connected():
                raise ValueError("Graph is not connected")
            if not self.is_dag():
                raise ValueError("Not a DAG")
            self._find_cycles()
        except Exception as e:
            raise e
        return True

    def is_connected(self):
        '''
        Check if Graph is connected

        :return: Returns True if the graph is connected, False otherwise. 
        :rtype: bool
        '''
        return nx.is_connected(self.to_undirected())

    def edge_distance(self, G, method="jaccard"):
        '''
        Calculate the edge distances using Jaccard method.

        :param G: Graph G whose edge distances to self should be calculated.
        :type G: Graph
        :param method: Method to use for finding edge distance, defaults to "jaccard"
        :type method: str, optional
        :raises ValueError: Raises ValueError when Unknown method is selected to compute distances
        :return: Jaccard distance for the given graph to self graph.
        :rtype: float
        '''
        if method == "jaccard":
            s1 = set(list(self.edges.keys()))
            s2 = set(list(G.edges.keys()))
            return jaccard(s1, s2)
        raise ValueError("Unknown method to compute distances")

    def node_distance(self, G, method="jaccard"):
        '''
        Calculate the node distances using Jaccard method.

        :param G: Graph G whose node distances to self should be calculated.
        :type G: Graph
        :param method: Method to use for finding node distance, defaults to "jaccard"
        :type method: str, optional
        :raises ValueError: Raises ValueError when Unknown method is selected to compute distances
        :return: Jaccard distance for the given graph to self graph.
        :rtype: float
        '''
        if method == "jaccard":
            s1 = set(list(self.nodes.keys()))
            s2 = set(list(G.nodes.keys()))
            return jaccard(s1, s2)
        raise ValueError("Unknown method to compute distances")

    def topological_distance(self, G, method="jaccard", weights=[.5,.5]):
        '''
        Calculate the topological distance using the edge and node distances generated for the given graph

        :param G: Graph whose topological distance should be found
        :type G: Graph
        :param method: Distance method used to find the edge and node distances, defaults to "jaccard"
        :type method: str, optional
        :param weights: Weights for the edges and nodes, defaults to [.5,.5]
        :type weights: list, optional
        :return: Topological distance for the graph
        :rtype: float
        '''
        ed = self.edge_distance(G, method)
        nd = self.node_distance(G, method)
        return sum([ed * weights[0], nd * weights[1]]) / 2

    def weighted_distance(self, G, topological_method="jaccard", value_method="cossine", key="value", weights=[.5, .5]):
        '''
        Computes a hybrid distance between a value and topological distance. Useful for comparing not only the actual value/ magnitudinal distance and similarity, but also the actual distinction in the topological shape of any two graphs.
        '''
        td = self.topological_distance(G, method=topological_method, weights=[.5, .5])
        vd = self.value_distance(G, method=value_method, key="value")
        logger.info("Got value distance {} and toplogical distance {}".format(td, vd))
        return ((vd + td) / 2)[0]

    def similarity(self, *args, **kwargs):
        '''
        Returns the similarity coefficient.

        :return: Similarity coefficient 
        :rtype: float
        '''
        #returns the inverse of the normalized distance.
        return 1- self.weighted_distance(*args, **kwargs)

    def value_distance(self, G, method="cossine", key="value", fillValue=0):
        '''
        Value distance compares the distance value of the
        nodes across the graph, using the method specified.

        For example, cossine distance will unravvel the nodes
        values into an array, and then use the cossine distance
        to give the final distance

        TODO: More methods
        TODO: Better explanatations of methods
        TODO: More tests on this
        '''
        a1 = self.get_value_dict(key=key)
        a2 = G.get_value_dict(key=key)
        isect = a1.keys() & a2.keys()
        # build array
        arr1 = []
        arr2 = []
        for i in isect:
            arr1.append(a1[i])
            arr2.append(a2[i])
        arr1 = np.array(arr1).reshape(1, -1)
        arr2 = np.array(arr2).reshape(1, -1)
        arr1 = arr1.astype(float)
        arr1[np.isnan(arr1)] = fillValue
        arr2 = arr2.astype(float)
        arr2[np.isnan(arr2)] = fillValue
        return 1 - cosine_similarity(arr1, arr2)

    def is_dag(self):
        '''
        Check if the graph is a Directed Acyclic Graph

        :return: Returns True if graph is a DAG, else False
        :rtype: bool
        '''
        return nx.is_directed_acyclic_graph(self)

    def sort(self, *args, **kwargs):
        '''
        Sort the graph in topological order. Uses the :code:`topological_sort()` method of NetworkX

        :return: Returns a list of nodes sorted in topological order
        :rtype: Generator[Any]
        '''
        return nx.topological_sort(self, *args, **kwargs)

    def get_value_dict(self, key="value"):
        return { n[0]: n[1].get(key, 0) for n in self.nodes.items()}

    def _find_cycles(self):
        try:
            nx.find_cycle(self, orientation=None)
        except nx.exception.NetworkXNoCycle:
            return True
        except Exception as e:
            raise e
        raise Exception("Cycle Detected! Invalid Graph.")

    @staticmethod
    def get_signature(f) -> str:
        '''
        Determine which distance functions to be used

        :param f: Distance function to be used.
        :type f: Any
        :return: Signature of the distance function to be used
        :rtype: str
        '''
        q = f.__qualname__
        if q == "mahalanobis":
                return "mag"
        if q == "jaccard":
                return "top"
        return None

class Edge():
    ''' For an undirected graph, an unordered pair of nodes that specify a line
    joining these two nodes are said to form an edge which represents a
    relationship or dependence between any two nodes. For a directed graph, the
    edge is an ordered pair of nodes. The terms "arc," "branch," "line," "link,"
    and "1-simplex" are sometimes used to describe an Edge in Graph Theory.
    
    Refer to this `article
    <https://mathworld.wolfram.com/GraphEdge.html#:~:text=For%20an%20undirected%20graph%2C%20an,e.g.%2C%20Skiena%201990%2C%20p>`_
    for more information on Graph Edge.

    TODO: Consider moving this to pydantic. '''

    def __init__(self, u, v, w=1, type=None, attributes={}):
        self.u = u
        self.v = v
        self.w = w
        self.type = type
        self.attributes = attributes

    def to_dict(self):
        ''' Returns a tuple of the Edge

        TODO: Fix. this should actually be called to_tuple and then
        TODO: Should also return promoted values

            to_dict should send back dictionary in the form of:
            {
                'u': a,
                'v': b,
                'attributes': c
            }
            
        '''
        return (self.u, self.v, self.attributes)

class Vertex():
    '''
    "Vertex" is a synonym for a node of a graph, i.e., one of the points on
    which the graph is defined and which may be connected by graph edges. The
    terms "point," "junction," and 0-simplex are also used to describe a Vertex
    in Graph Theory.

    See `Here
    <https://mathworld.wolfram.com/GraphVertex.html#:~:text=%22Vertex%22%20is%20a%20synonym%20for,80)>`_
    for more information.

    NOT threadsafe implementation

    TODO: Consider moving this to pydantic.
    '''
    def __init__(self, id: str, value=None, attributes={}):
        self.value = value
        self.id = id
        self.attributes = attributes
        self._disallowed_keys = set(['id', 'value'])

    def add_attribute(self, k: str, v: Any, unsafe=True):
        '''
        adds an attributes

        toggle unsafe to allow keys to be overridden
        that already exist
        '''

        if k in self._disallowed_keys:
            raise ValueError("key {} by attributes is not allowed".format(k))

        if not unsafe:
            if k in self.attributes:
                raise ValueError("Key {} already exists in attributes. Can't add".format(k))

        self.attributes[k] = v

    def to_dict(self):
        '''
        converts to dictionary
        merging attributes to promoted
        field and sending back
        '''
        return {
            "id": self.id,
            "value": self.value,
            **self.attributes
        }

