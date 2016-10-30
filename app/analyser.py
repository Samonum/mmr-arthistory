#from utils import get_tree
import scipy.optimize as opt
import numpy
import unittest
import json
import os


import utils

from features import color
#from features import EHD, GF, GLCM

def analyse_features():
    resultPath = os.path.join(os.getcwd(), os.path.join('data','results.json'))
    resultFile = open(resultPath, 'r')
    resultArray = json.load(resultFile)
    
    cUserRating = []
    cImg1 = []
    cImg2 = []
    
    tUserRating = []
    tImg1 = []
    tImg2 = []
    
    for item in resultArray:
        if item['mainimg']['compare_by'] == 'color':
            cUserRating.append(item['votevalue'])
            cImg1.append(item['mainimg']['index'])
            cImg1.append(item['similarimg']['index'])
        else:
            tUserRating.append(item['votevalue'])
            tImg1.append(item['mainimg']['index'])
            tImg1.append(item['similarimg']['index'])
    
    print utils.get_tree()
    return 0

analyse_features();

def linear_regression(x, y):
    """
    Given two matching data sets caculates the closest fitting line
    using the least squares method and the correlation coefficient.
    Returns: coefficients of the line, correlation coefficient
    """
    def f(x, a, b):
        return a+b*x
    yay, _ = opt.curve_fit(f, x, y)
    covar = numpy.cov(x,y)
    
    stdev = numpy.sqrt(numpy.diag(covar))
    return yay,(covar[0][1]/(stdev[0]*stdev[1]))


################################################################################
# TESTS
################################################################################

# The unittest module provides nice utilities for testing
# Check out docs at https://docs.python.org/3/library/unittest.html !!!
class TestColorFeatures(unittest.TestCase):

    def test_lin_reg(self):
        """Should output correct hue count, for the given image 4"""
        
        x = range(0,40000)
        y = range(10,80010,2)
        print linear_regression(x, y)
        # ... and then evaluate the output

# This if statement gets executed when you run this file, so > python color.py
if __name__ == '__main__':
    # It's a convenient way of running unittests!
    unittest.main()
