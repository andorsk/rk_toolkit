'''
Example filters
'''
class StaticFilter():
    '''
    This static filter takes simple boundary conditions,
    a min and max, and provides a filter function over it
    '''
    def __init__(self, min=None, max=None):
        self._min = min
        self._max = max

    def filter(self, val):
        if val is None:
            return True
        if self._min is not None and val < self._min:
            return False
        if self._max is not None and val > self._max:
            return False
        return True
