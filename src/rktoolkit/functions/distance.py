import scipy as sp
import numpy as np


def jaccard(s1, s2): # two sets
    '''

    The Jaccard similarity index measures the similarity between two sets of
    data. It can range from 0 to 1. The higher the number, the more similar the
    two sets of data.

    If a list is given, it converts it into a set.

    :param s1: Data Set 1
    :type s1: set
    :param s2: Data Set 2
    :type s2: set
    :return: Topological Distance 
    :rtype: float
    '''
    if isinstance(s1, list):
        s1 = set(s1)
    if isinstance(s2, list):
        s2 = set(s2)

    intersect = s1 & s2
    jin = len(intersect)  / (len(s1) + len(s2) - len(intersect))
    return 1-jin

def mahalanobis(x=None, data=None, cov=None):
    '''
    Value Distance Funtion
    
    :param x: vector or matrix of data with, say, p columns, defaults to None
    :type x: ndarray, optional
    :param data: ndarray of the distribution from which Value distance of each observation of x is to be computed, defaults to None
    :type data: ndarray, optional
    :param cov: covariance matrix (p x p) of the distribution. If None, will be computed from data.
    :type cov: ndarray, optional
    :return: Value/Magnitudinal distance.
    :rtype: ndarray
    '''
    x_minus_mu = x - np.mean(data)
    if not cov:
        cov = np.cov(data.values.T)
    inv_covmat = np.linalg.inv(cov)

    left_term = np.dot(x_minus_mu, inv_covmat)
    mahal = np.dot(left_term, x_minus_mu.T)
    return mahal.diagonal()
