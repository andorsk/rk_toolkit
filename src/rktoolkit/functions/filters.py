class RangeFilter():
    '''
    Range Filter class to create a filter between the given ranges.
    '''
    def __init__(self, min:float=0, max:float=1):
        self.min = min
        self.max = max

    def get_knobs(self):
        '''Get knobs to be used for the filter range.

        :return: Min and max ranges.
        :rtype: dict
        '''
        return {
            "min": self.min,
            "max": self.max
        }

    def set_knob(self, knb, v):
        '''Set Knobs to given values.

        :param knb: The knob to be adjusted, can be either min or max.
        :type knb: str
        :param v: Value of the knob to be adjusted to.
        :type v: int
        :raises ValueError: Need the `knob` argument to be only min or max,else the error will be raised.
        '''
        if knb == "min":
            self.min = v
        elif knb == "max":
            self.max = v
        else:
            raise ValueError("No knob {}".format(knb))

    def filter(self, node):
        '''
        Filter method to filter the node according to the range.

        :param node: Node to be filtered
        :type node: Any
        :return: Returns true if filtered else false.
        :rtype: bool
        '''
        if not "value" in node or node["value"] is None:
            print("Warning: No value present for {}. Could not filter".format(node))
            return False

        return not (node["value"] > self.min and node["value"] <= self.max)

class FilterAll():
    '''
    Filter for all knobs. To be used when all needs to be filtered.
    '''
    def get_knobs(self):
        pass

    def set_knob(self, knb, v):
        pass

    def filter(self, node):
        return False


class FilterNone():
    '''
    Filter for No filters. To be used when nothing needs to be filtered.
    '''
    def get_knobs(self):
        pass

    def set_knob(self, knb, v):
        pass

    def filter(self, node):
        return True
