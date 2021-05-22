'''
Localization functions

Must implement the LocalizationFunction interface
'''
import numpy as np
from ..models.functions import LocalizationFunction

class NDMaxLocalizationFunction(LocalizationFunction):

    def __init__(self):
        super().__init__()

    def predict(self, X):
        '''
        given a matrix NxD. Localizes around the max of the matrix
        '''
        pos = np.argmax(X[2])
        i1=int(X[2].argmax()/len(X[2])),
        i2 = int(X[2].argmax() % len(X[2]))
        return X[0][i1], X[1][i2]

class IterableLocalizationFunction(LocalizationFunction):

    def __init__(self, iterateX=True, iterateY=True):
        super().__init__()
        self.iterateX = iterateX
        self.iterateY = iterateY
        self._xcount = -1
        self._ycount = -1
        self.counter

    def predict(self, X):
        '''
        given a matrix NxD. Localizes around the max of the matrix
        '''
        if self.iterateX:
            self._xcount += 1
        if self.iterateY:
            self._ycount += 1
        return self._xcount, self.y_count
