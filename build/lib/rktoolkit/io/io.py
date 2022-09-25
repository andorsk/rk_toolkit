import abc
from collections.abc import Sequence
from typing import List
from ..models.rkmodel import RKModel

class RKModelWriter(metaclass=abc.ABCMeta):
    '''
    Datastore Interface

    Writes a RK-model. The classmethod hook is used to write the RK-Model using the given parameter.
    '''
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'write') and callable(subclass.write)

    def write(self, model: RKModel) -> bool: # returns whether success or failure on write
        '''
        Writes the RK-model. Returns whether success or failure on  write. 
        :param model: RK-Model to be written
        :type model: RKModel
        '''
        pass

class RKModelReader(metaclass=abc.ABCMeta):
    '''
    RK Model Reader Interface
    Must implement the following interfaces. The classmethod hook will read the RK-model based. 
    '''
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'read') and callable(subclass.read) and \
            hasattr(subclass, 'next') and callable(subclass.next) and  \
            hasattr(subclass, 'close') and callable(subclass.close) and  \
            hasattr(subclass, 'readAll') and callable(subclass.readAll)

    def read(self) -> RKModel:
        '''
        Reads from the RK-Model.
        '''
        pass

    def next(self) -> RKModel:
        '''
        Reads next line if exists.
        '''
        pass

    def close(self):
        '''
        Close the reader
        '''
        pass

    def readAll(self) -> List[RKModel]:
        '''
        Reads the RK-Models and returns a list of them.
        '''
        pass
