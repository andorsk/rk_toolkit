# Maintainer: andor@henosisknot.com
# Main graph class
from networkx.classes.digraph import DiGraph
import networkx as nx
import copy
import numbers
from ..functions.distance import jaccard, mahalanobis
from pydantic import BaseModel, PrivateAttr
from enum import Enum
from typing import List, Optional, Callable, Any
import uuid
from copy import deepcopy, copy

class NodeMask():
    '''
    A graph mask is a mask over an existing structural graph. It essentially provides an overlay representation, which can be used to filter out particular nodes and edges.    Typically,a mask over a node, should also mask child-nodes associated with it. A node mask represents a masking structure that when applied to a structural graph S, reduces the number of nodes into a subgraph S. Node masks in the R-K Model are binary operators, which when set to true, filter a node and its direct children. To derive the node masks, we produce a set of filters Fn(G), which takes in a graph and returns a mask.
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
    Excerpt from initial paper:
    https://arxiv.org/pdf/2201.06923.pdf

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
            super().add_edges_from([e.to_dict()])
        else:
            raise ValueError("Expected a Edge Type")

    def get_children(self, node_id, recursive=False):
        '''
        Get the children nodes of the given node.

        :param node_id: ID of the node whose children needs to be found
        :type node_id: str
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

        return nx.is_directed_acyclic_graph(self)

    def sort(self, *args, **kwargs):
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

    def get_signature(f) -> str:
        '''
        Determine which distance functions to be used

        :param f: Distance function to be used.
        :type f: Any
        :return: Signature of the distance function to be used
        :rtype: str
        '''
        match f.__name__:
            case "mahalonobis":
                return "mag"
            case "jaccard":
                return "top"

class Edge():
    '''
    For an undirected graph, an unordered pair of nodes that specify a line joining these two nodes are said to form an edge which represents a relationship or dependence between any two nodes. For a directed graph, the edge is an ordered pair of nodes. The terms "arc," "branch," "line," "link," and "1-simplex" are sometimes used to describe an Edge in Graph Theory.    

    https://mathworld.wolfram.com/GraphEdge.html#:~:text=For%20an%20undirected%20graph%2C%20an,e.g.%2C%20Skiena%201990%2C%20p.

    TODO: Consider moving this to pydantic.
    '''

    def __init__(self, u, v, w=1, type=None, attributes={}):
        self.u = u
        self.v = v
        self.w = w
        self.type = type
        self.attributes = attributes

    def to_dict(self):
        ''' returns a tuple of the

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
    "Vertex" is a synonym for a node of a graph, i.e., one of the points on which the graph is defined and which may be connected by graph edges. The terms "point," "junction," and 0-simplex are also used to describe a Vertex in Graph Theory.

    See
    https://mathworld.wolfram.com/GraphVertex.html#:~:text=%22Vertex%22%20is%20a%20synonym%20for,80).
    for more information

    NOT threadsafe implementation

    TODO: Consider moving this to pydantic.
    '''
    def __init__(self, id: str, value=None, attributes={}):
        self.value = value
        self.id = id
        self.attributes = attributes
        self._disallowed_keys = set('id', 'value')

    def add_attribute(k: str, v: Any, unsafe=True):
        '''
        adds an attributes

        toggle unsafe to allow keys to be overridden
        that already exist
        '''

        if k in self._disallowed_keys:
            raise ValueError("key {} is not allowed".format(k))

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

'''
Older Stuff
TODO: figure out how much is still used and remove bad components
'''
# Edge types for edges
class EdgeType(Enum):
    UNDIRECTED=1
    DIRECTED=2

class Node(BaseModel):
    '''
    A node represents a distinct object in a graph that has magnitude but no direction and accounts for the quantitative value of a particular property of a variable. A special class  of nodes are used in the creation of DAGs (Directed Acyclic Graphs) which have a few unique features beyond that of a normal node, such as checking boundary conditions and an executing function for data transformation which are of interest in the case of building R-K Models.
    '''
    id: Optional[str] = None
    name: Optional[str] = None,
    value: Optional[float] = None
    attributes: Optional[dict] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.id is None:
            self.id = str(uuid.uuid4())

class TreeNode(Node):
    parent: Optional[Node] = None
    children: Optional[List[Node]] = []
    is_root: Optional[bool] = False

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

class GraphModel(BaseModel):
    '''
    The underlying graph model is a relationship
    of nodes and edges
    '''
    nodes: Optional[Node] = []
#    edges: Optional[Edge] = []
    _nids: dict = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._nids = {}

    def add_node(self, node: Node):
        self.nodes.append(node)
        self._nids[node.id] = node

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def get_node_by_id(self, id: str) -> Node:
        if id not in self._nids:
            raise ValueError("Node ID: {} not in graph.".format(id))
        return self._nids[id]

class HierarchicalGraph(GraphModel):
    '''
    A Hierarchical Graph is a subset of the general graph in which all elements are directed and have a dependence relationship such as parent and child which is defined by a particular domain Ontology.

    '''
    root: TreeNode
    _level_ref: Optional[dict] = PrivateAttr()
    _node_ref: Optional[dict] = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._level_ref = None
        self._node_ref = None
        self.root.is_root = True

    def add_edge(self, edge:Edge):
        if edge.edge_type != EdgeType.DIRECTED:
            raise ValueError("Edge type needs to be directed in heirarchial graph")

    def add_node(self, node: TreeNode):
        if not isinstance(node, TreeNode):
            raise ValueError("Node must be a tree node")
        if node.parent is not None:
            node.parent.children.append(node)
        super().add_node(node)

    def _build_levels(self) -> (dict(), dict()):
        '''
        Inefficient method to build the levels of a graph
        based. Returns two dictionaries:
        1: A dictionary where dict[level] -> [list of nodes]
        2. A dictionary where dict[id] -> level
        TODO: Build a more efficient data structure to index levels
        '''
        levels, nmap = {}, {}
        def _build_level_from_parent(n, d, d1, c):
            if c not in d:
                d[c] = []
            d[c].append(n)
            d1[n.id] = c
            for child in n.children:
                _build_level_from_parent(child, d, d1, c+1)
        _build_level_from_parent(self.root, levels, nmap, 0)
        return levels, nmap

    def get_root(self) -> Node:
        return self.root

    def get_level(self, level, rebuild=True) -> List[Node]:
        if self._level_ref is None or rebuild:
            self._level_ref, self._node_ref = self._build_levels()
        return self._level_ref.get(level, [])

class HierarchicalTransformGraph(HierarchicalGraph):
    '''
    Heirarchical Transform Graph contains
    transform functions
    '''
    def __init__(self, **data):
        super().__init__(**data)

    def _transform(self, parent, X):
        for n in parent.children:
            if isinstance(n, TreeTransformNode):
                v = n.transform(X)
                n.value = v
            self._transform(n, X)

    def transform(self, X):
        self._transform(self.get_root(), X)
        return self


class HierarchicalGraph(GraphModel):
    '''
    A Hierarchical Graph is a subset of the general graph in which all elements are directed and have a dependence relationship such as parent and child which is defined by a particular domain Ontology.

    '''
    root: TreeNode
    _level_ref: Optional[dict] = PrivateAttr()
    _node_ref: Optional[dict] = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._level_ref = None
        self._node_ref = None
        self.root.is_root = True

    def add_edge(self, edge:Edge):
        if edge.edge_type != EdgeType.DIRECTED:
            raise ValueError("Edge type needs to be directed in heirarchial graph")

    def add_node(self, node: TreeNode):
        if not isinstance(node, TreeNode):
            raise ValueError("Node must be a tree node")
        if node.parent is not None:
            node.parent.children.append(node)
        super().add_node(node)

    def _build_levels(self) -> (dict(), dict()):
        '''
        Inefficient method to build the levels of a graph
        based. Returns two dictionaries:
        1: A dictionary where dict[level] -> [list of nodes]
        2. A dictionary where dict[id] -> level
        TODO: Build a more efficient data structure to index levels
        '''
        levels, nmap = {}, {}
        def _build_level_from_parent(n, d, d1, c):
            if c not in d:
                d[c] = []
            d[c].append(n)
            d1[n.id] = c
            for child in n.children:
                _build_level_from_parent(child, d, d1, c+1)
        _build_level_from_parent(self.root, levels, nmap, 0)
        return levels, nmap

    def get_root(self) -> Node:
        return self.root

    def get_level(self, level, rebuild=True) -> List[Node]:
        if self._level_ref is None or rebuild:
            self._level_ref, self._node_ref = self._build_levels()
        return self._level_ref.get(level, [])



class TreeTransformNode(TreeNode):

    transformf: Optional[Callable] = lambda x: x
    fitf: Optional[Callable] = lambda X,y: None

    def __init__(self, **data):
        super().__init__(**data)

    def transform(self, X):
        return self.transformf(X)

    def fit(self, X, y):
        self.fit(X,y)

class PipelineNode(TreeNode):
    '''
    defines a pipeline node
    '''
    def predict(self, X):
        pass

    def fit(self, X, y):
        pass

