#!/usr/bin/env python3
from pydantic import BaseModel
from enum import Enum
from typing import List, Optional
import uuid

# Edge types for edges
class EdgeType(Enum):
    UNDIRECTED=1
    DIRECTED=2

'''
A graph edge links nodes together
using the nodeid.
'''
class Edge(BaseModel):
    from_id: str
    to_id: str
    edge_type: EdgeType
    weight: Optional[float] = EdgeType.UNDIRECTED
    attributes: Optional[dict] = None

'''
A node represents a distinct object in a graph
'''
class Node(BaseModel):
    id: Optional[str] = str(uuid.uuid4())
    name: Optional[str] = None,
    value: Optional[float] = None
    attributes: Optional[dict] = {}

'''
A subclass of node that speiciflcally is used
in DAG creation. It has a couple features a normal
node doesn't have, such as checking boundary conditions
and an executing function for data transformation
'''
class TransformNode(Node):

    def getInputSchema(self) -> dict:
        return

    def getOutputSchema(self) -> dict:
        return

    def transform(self, X): # the model transform function
        pass

'''
The underlying graph model is a relationship
of nodes and edges
'''
class GraphModel(BaseModel):

    nodes: Optional[Node] = []
    edges: Optional[Edge] = []

    def add_node(self, node: Node):
        self.nodes.append(node)
        self._ids.add(node.id)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

'''
A Hierarchical Graph
is a subset of the general graph in which
all elements are directed.
'''
class HierarchicalGraph(GraphModel):

    def add_edge(self, edge:Edge):
        if edge.edge_type != EdgeType.DIRECTED:
            raise ValueError("Edge type needs to be directed in heirarchial graph")

    def validate(self) -> bool:
        '''
        validates the graph is valid.
        for a graph to be valid, all edges must be
        direcected edges
        '''
        for e in self.edges:
            if e.edge_type != EdgeType.DIRECTED:
                return False
        return True


'''
Graph masks are similar to numpy masks.
They represent a masking of graph elements
and are ultimately what the filter functions
are generating.
'''
class GraphMask(BaseModel):
    nodeMasks: List[bool]
    edgeMasks: List[bool]
    graph: GraphModel


class RKModel(BaseModel):
    '''
    An RK-Model is the core data-structure that can be manifested in an
    RK-Diagram or interpreted.

    RK-Models are different from most models due to a number of important
    features:

    - HierarchicalGraph(h) => a heierarchical graph of features. Which features
    have a directional relationship with eachother
    - Mask (mask) =>  A graph mask. Represents a masking function on top of
    the Hierarchical Graph
    - Links => Links just edges. They can be computed with a Linkage Function
    - Locatoin => A global position for reference. When plotting an rkmodel against
    other rk-models, this positions the rk-models relative to eachtother
    '''
    def __init__(self,
                 mask: GraphMask = None,
                 h: HierarchicalGraph = None,
                 links:List[Edge] = None,
                 location: List[float] = None):
        self.mask = mask
        self.h = h
        self.links = links
        self.location = location

    def complete(self) -> bool:
        if self.mask is None or self.h is None \
           or self.links is None or self.location is None:
            return False
        return True
