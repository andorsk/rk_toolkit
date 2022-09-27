import numpy as np
from .localizers import NDMaxLocalizationFunction
from .linkers import  SimpleLinkageFunction
from ..models.graph import TreeNode, HierarchicalGraph

'''

TODO: Clean tests
Some tests are old.
Some tests are not relevant anymore
Add tests to other functions
'''
def test_NDLocalizationFunction():
    '''
    TODO: remove this. not required
    '''
    ll = NDMaxLocalizationFunction()
    x = np.linspace(0,100,100)
    y = np.linspace(101, 200, 100)
    xx, yy = np.meshgrid(x, y, sparse=True)
    z = np.sin(xx**2 + yy**2) / (xx**2 + yy**2)
    l = ll.predict((x,y,z))
    x1 = np.where(x==l[0])[0][0]
    y2 = np.where(y==l[1])[0][0]
    assert z.max() == z[x1, y2]

def test_simple_linkage_function():
    pass
