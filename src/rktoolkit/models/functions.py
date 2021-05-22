from .graph import HierarchicalGraph, Edge
from typing import List

'''
Function abstractions
'''

class LocalizationFunction():

    def __init__(self):
        pass

    def predict(self, X) -> [float]:
        '''
        Predicts the localized position
        Returns a list of float
        '''
        pass

    def fit(self):
        '''
        Fits the data
        '''
        pass

class LinkageFunction():

    def __init__(self):
        pass

    def predict(self, X: HierarchicalGraph) -> List[Edge]:
        pass

    def fit(self, X: HierarchicalGraph):
        pass
