import scipy as sp
import numpy as np

def jaccard(s1, s2): # two sets
    '''
    Jaccard distance measures the dissimilarity between data sets and is
    obtained by subtracting the Jaccard similarity coefficient from 1. For
    binary variables, Jaccard distance is equivalent to the Tanimoto
    coefficient.

    :param s1: Data Set 1
    :type s1: set
    :param s2: Data Set 2
    :type s2: set
    :return: Jaccard distance 
    :rtype: float
    '''
    intersect = s1 & s2
    jin = len(intersect)  / (len(s1) + len(s2) - len(intersect))
    return 1-jin

def mahalanobis(x=None, data=None, cov=None):
    '''
    Compute the Mahalanobis Distance between each row of X and the data
    
    :param x: vector or matrix of data with, say, p columns, defaults to None
    :type x: ndarray, optional
    :param data: ndarray of the distribution from which Mahalanobis distance of each observation of x is to be computed, defaults to None
    :type data: ndarray, optional
    :param cov: covariance matrix (p x p) of the distribution. If None, will be computed from data.
    :type cov: ndarray, optional
    :return: Mahalanobis distance.
    :rtype: ndarray
    '''
    x_minus_mu = x - np.mean(data)
    if not cov:
        cov = np.cov(data.values.T)
    inv_covmat = sp.linalg.inv(cov)
    left_term = np.dot(x_minus_mu, inv_covmat)
    mahal = np.dot(left_term, x_minus_mu.T)
    return mahal.diagonal()
