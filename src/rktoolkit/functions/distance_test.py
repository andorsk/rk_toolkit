from .distance import jaccard, mahalanobis
import pandas as pd

vec0 = [0, 1, 2, 5, 6, 8, 9]
vec1 = [0, 2, 3, 4, 5, 7, 9]
vec2 = [0, 1, 2, 3, 4, 5]
vec3 = [6, 7, 8, 9, 10]
vec4 = ['cat', 'dog', 'hippo', 'monkey']
vec5 = ['monkey', 'rhino', 'ostrich', 'salmon']

def test_jaccard():
    assert jaccard(vec0, vec0) == 0
    assert jaccard(vec0, vec1) == 1-0.4
    assert jaccard(vec2, vec3) == 1
    assert jaccard(vec4, vec5) == .8571428571428572

def test_mahalanobis():
    pass

    # data and results here:
    # https://www.statology.org/mahalanobis-distance-python/

    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.mahalanobis.html
#    assert mahalanobis(x = pd.DataFrame([[1,0,0]]),
#                       data = pd.DataFrame([[1, 0, 0], [0, 1, 0], [0, 0, 1]])) == 1
