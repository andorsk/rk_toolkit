from ..models.graph import (
    Graph,
    Vertex,
    Edge
)

import numpy as np
import matplotlib
import matplotlib.cm as cm

class BaseOntologyTransform():
    '''
    This Class is used for cases in which an ontology is generated or provided for a particular application. It creates a transform for a given Ontology loaded from a JSON file with input given as a Python object. The JSON file contains hierarchical data. This class transforms the ontology into a Graph using the data from the dataframe of any particular data source or from results of the Hierarchical Transform Graph based on covariance parameters.  An empty graph is first created and the rest of vertices and edges are added using a private convert method.
    '''

    def __init__(self, mapping, lens="root", color_decay_rate=.1):
        self.mapping = mapping
        self.lens = lens
        self.cmap = matplotlib.cm.get_cmap('Spectral')
        self.color_decay_rate = color_decay_rate

    def transform(self, X):
        '''
        Transforms the ontology into a Graph using the data from the dataframe of GWTC.
        An empty graph is created and the rest of vertices and edges are added using a private convert method.

        :param X: Data to be transformed to graph
        :type X: Any
        :return: Graph transform for the given data.
        :rtype: Graph
        '''
        H = Graph()
        H.add_vertex(Vertex(self.lens))
        return self._convert(X, H, self.mapping, parent=self.lens, level=1)

    def _convert(self, X, H, hmap=None, parent=None, level=0, color=None, lens="root", no_self_refrence=True):
        count = 0
        for k, v in hmap.items():
            if level == 1:
                color = np.array(self.cmap(count/len(hmap.keys())))
            value = X[k] if k in X else None
            color[3] *= 1- self.color_decay_rate
            node = Vertex(id=k, attributes={"color": color}, value=value)
            H.add_vertex(node)
            if no_self_refrence and parent != k:
                H.add_edge(Edge(u=parent, v=k))
            self._convert(X, H, v, parent=k, level=level+1, color=color)
            count+=1
        return H

