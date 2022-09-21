'''
Localization functions

Must implement the LocalizationFunction interface
'''
import numpy as np
from ..models.functions import LocalizationFunction
from typing import Optional
from pydantic import PrivateAttr

class NDMaxLocalizationFunction(LocalizationFunction):
    '''
    Localization function that localizes a N x D matrix around the maximum of the matrix.
    '''

    def __init__(self):
        super().__init__()

    def predict(self, X):
        '''
        Predicts and localizes a given N x D matrix around the maximum of the matrix.

        :param X: Matrix to be localized. Should be in N x D dimensions.
        :type X: ndarray
        :return: Localized values for the matrix X
        :rtype: tuple[int], int
        '''
        pos = np.argmax(X[2])
        i1=int(X[2].argmax()/len(X[2])),
        i2 = int(X[2].argmax() % len(X[2]))
        return X[0][i1], X[1][i2]

class IterableLocalizationFunction(LocalizationFunction):
    '''_
    An Iterable localization function that localizes a N x D matrix around the max. The class can be initialized with parameters to determine which dimensions 
    should be iterated around.
    '''

    _iterateX: bool = PrivateAttr()
    _iterateY: bool = PrivateAttr()
    _iterateZ: bool = PrivateAttr()

    _xcount: int = PrivateAttr()
    _ycount: int = PrivateAttr()
    _zcount: int = PrivateAttr()

    def __init__(self, iterateX=True, iterateY=True, iterateZ=True):
        super().__init__()
        self._iterateX = iterateX
        self._iterateY = iterateY
        self._iterateZ = iterateZ
        self._xcount = -1
        self._ycount = -1
        self._zcount = -1

    def localize(self, X):
        '''
        Localizes  the matrix X around the max iteratively. 

        :param X: Matrix X to be localized.
        :type X: ndarray
        :return: Localized X,Y and Z values
        :rtype: int,int,int
        '''
        if self._iterateX:
            self._xcount += 1
        if self._iterateY:
            self._ycount += 1
        if self._iterateZ:
            self._zcount += 1

        return self._xcount, self._ycount, self._zcount
