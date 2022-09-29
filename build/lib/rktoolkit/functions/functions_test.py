import numpy as np
from .localizers import NDMaxLocalizationFunction
from ..models.graph import Edge, Vertex
from typing import List

def test_NDLocalizationFunction():
    ll = NDMaxLocalizationFunction()
    x = np.linspace(0,100,100)
    y = np.linspace(101, 200, 100)
    xx, yy = np.meshgrid(x, y, sparse=True)
    z = np.sin(xx**2 + yy**2) / (xx**2 + yy**2)
    l = ll.predict((x,y,z))
    x1 = np.where(x==l[0])[0][0]
    y2 = np.where(y==l[1])[0][0]
    assert z.max() == z[x1, y2]

def testLinkageAbstraction():

    class GoodTestClass():

        def predict(self, nodes: List[Vertex]) -> List[Edge]: # given a graph the edges
            return []

    class BadTestClass():

        def bad(self):
            return None

    #TODO: Test interface
