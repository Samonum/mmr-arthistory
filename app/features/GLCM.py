import unittest
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from scipy.misc import imread
from skimage.feature import greycomatrix, greycoprops

def GLCMFeatures(image):
    """
    Function that calculate the gray level co-occurrence matrix of an image.

    Coded by An Li
    """
    GrayImg = rgb2gray(image)
    glcms = greycomatrix(GrayImg, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4], levels=4)
    results = greycoprops(glcms, 'contrast')
    results = np.concatenate((results, greycoprops(glcms, 'dissimilarity')))
    results = np.concatenate((results, greycoprops(glcms, 'homogeneity')))
    results = np.concatenate((results, greycoprops(glcms, 'energy')))
    results = np.concatenate((results, greycoprops(glcms, 'correlation')))
    return results

################################################################################
# TESTS
################################################################################

# The unittest module provides nice utilities for testing
# Check out docs at https://docs.python.org/3/library/unittest.html !!!
class TestGLCMFeatures(unittest.TestCase):

    def test_GLCMFeatures(self):
        """Should output the designated features of GCLM"""
        thispath = os.path.dirname(__file__)
        impath = os.path.join("test", "lady.png")
        img = cv2.imread(os.path.join(thispath, impath))
        features = GLCMFeatures(img)
        print(features)

# This if statement gets executed when you run this file, so > python color.py
if __name__ == '__main__':
    # It's a convenient way of running unittests!
    unittest.main()
