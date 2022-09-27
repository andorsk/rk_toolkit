from .filters import RangeFilter, FilterAll, FilterNone

def testFilters():
    '''
    test filters
    '''
    filters = make_filter_tests()
    for f in filters:
        for c in f.cases:
            assert f.filter.filter({'value': c[0]}) == c[1]

def testRangeFilterRemap():
    test = make_filter_tests()[0]
    for c in test.cases:
        assert test.filter.filter({'value': c[0]}) == c[1]
    test.filter.set_knob("min", -1)
    assert test.filter.filter({'value': 0}) == False


class FilterTests():
    '''
    Filter test
    '''
    def __init__(self, f, cases=[], name=""):
        self._filter = f
        self.cases = cases

    def name(self):
        if self.name == "":
            return self._filter.__name__
        else:
            return self.name

    @property
    def filter(self):
        return self._filter

def make_filter_tests() :
    return [
        FilterTests(
            RangeFilter(min=0, max=1),
            [(0, True) , (1, False), (.5, False), (2, True)],
            "RangeFilter-01-Test"
        ),
        FilterTests(
            FilterAll(),
            [(0, False) , (1, False), (.5, False), (2, False)],
            'Filter-All-01'
        ),
        FilterTests(
            FilterNone(),
            [(0, True) , (1, True), (.5, True), (2, True)],
            'Filter-None-Test-01'
        )
    ]
