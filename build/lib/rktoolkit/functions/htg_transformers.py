from ..models.graph import HierarchicalTransformGraph, TreeNode, TreeTransformNode, Graph, Vertex, Edge
import pandas as pd
import matplotlib
import numpy as np

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

    def _convert(self, X, H, hmap=None, parent=None, level=0, color=None, lens="root"):
        count = 0
        for k, v in hmap.items():
            if level == 1:
                color = np.array(self.cmap(count/len(hmap.keys())))
            value = X[k] if k in X else None
            color[3] *= 1- self.color_decay_rate
            node = Vertex(id=k, attributes={"color": color}, value=value)
            H.add_vertex(node)
            H.add_edge(Edge(u=parent, v=k))
            self._convert(X, H, v, parent=k, level=level+1, color=color)
            count+=1
        return H

class CorrelationHTGGenerator():
    '''
    This Class is used to create a Correlation and covariance based Hierarchical Transform Graph(HTG) using a given data frame for pre determining dependence and interrelationships between various column variables residing in the master-dataset which could consist of columns and dimensions from different data sources/streams representing the same event or entity. Transforms a given graph into a Correlated HTG with built-in covariance parameters which determine interdependence between dependent and independent variables. In this case an empty HTG is created first and then nodes are added to it based on the correlation factor between different dimensions of the master-dataset.  
    '''
    def __init__(self, threshold=.7):
        self.threshold = threshold
        self._corr = None

    def fit(self, X,y):
        pass

    def transform(self, X):
        '''
        Transforms a given graph into a Correlated HTG. Empty HTG is created and then nodes are added to it based on the correlation factor.

        :param X: Input data to be used for creating the transform. Will be converted into a correlated dataframe.
        :type X: Any
        :return: A correlated Hierarchical Transform Graph.
        :rtype: HierarchicalTransformGraph
        '''

        cdf = pd.DataFrame(X).corr().abs()
        measures = TreeNode(parent=None, id='measures')
        H = HierarchicalTransformGraph(root=measures)

        nodes = []
        for i,v in cdf.iterrows():

            parent = TreeNode(name="{}_measure".format(i), id="{}_measure".format(i),
                    parent=measures)
            j = i

            nodes.append(parent)

            n_id = "{}_{}".format(i,i)
            n1 = TreeTransformNode(name=n_id, id=n_id, parent=parent,
                                   transformf=lambda X: X[i])
            nodes.append(n1)

            while j < len(v) - 1:

                if j == i:
                    j+=1
                    continue

                if v[j] > self.threshold:
                    n_id = "{}_{}".format(i,j)
                    n1 = TreeTransformNode(name=n_id, id=n_id, parent=parent,
                                           transformf=lambda X: X[j])
                    nodes.append(n1)
                j+=1
        [H.add_node(n) for n in nodes]
        return H
