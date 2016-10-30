#from utils import get_tree
import scipy.optimize as opt
import numpy
import unittest




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
