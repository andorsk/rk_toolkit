from pydantic import BaseModel
from .graph import (
    HierarchicalTransformGraph,
    TreeTransformNode,
    GraphMask,
    RKModel
)
from .functions import *
from typing import List, Optional, Callable
from ..functions.localization_functions import IterableLocalizationFunction
from ..functions.linkage_functions import SimpleLinkageFunction

class RKPipeline(BaseModel):
    '''
    RK Pipeline Builder
    '''
    preprocess_nodes: Optional[List[TreeTransformNode]] = []
    localization_algorithm: Optional[LocalizationFunction] = IterableLocalizationFunction()
    hfe:HierarchicalTransformGraph
    filter_functions: dict
    linkage_function: Optional[LinkageFunction] = SimpleLinkageFunction(threshold=-1)

    class Config:
        arbitrary_types_allowed = True

    def fit(self, X, y):
        for n in self.preprocess_nodes:
            n.fit(X,y)

    def transform(self, X):

        # Step 1: run through preprocess nodes
        for node in self.preprocess_nodes:
            X = node.transform(X)

        # Step 2: localize data
        loc = self.localization_algorithm.localize(X)

        # Step 3: Run through heirarhcial transform graph
        hgraph = self.hfe.transform(X)

        # Step 4: Run through Filter Functions
        gm = GraphMask()
        for k, f in self.filter_functions.items():
            # get the filter function node
            n1 = hgraph.get_node_by_id(k)
            if n1 is None:
                raise ValueError("You've mapped a filter function \
                to a non-existant correspondence. Make sure to link \
                the filter function to an id fomr the hfe")
            ns = f.filter(n1.value)
            if ns:
                gm.mask_node(n1)

        # Step 5: Build links
        links = self.linkage_function.link(hgraph)
        return RKModel(
            mask = gm,
            hgraph = hgraph,
            links = links,
            location = loc
        )
