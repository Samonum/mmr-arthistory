import unittest
import cv2
import numpy as np
import os
from scipy.spatial import distance
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from scipy.misc import imread
from skimage.feature import greycomatrix, greycoprops
def GLCMFeatures(image):
    """
    Function that calculate the gray level co-occurrence matrix of an image.

    Coded by An Li
    """

    GrayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    glcms = greycomatrix(GrayImg, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256, normed=True)
    results = greycoprops(glcms, 'contrast')
    results = np.concatenate((results, greycoprops(glcms, 'dissimilarity')))
    results = np.concatenate((results, greycoprops(glcms, 'homogeneity')))
    results = np.concatenate((results, greycoprops(glcms, 'energy')))
    results = np.concatenate((results, greycoprops(glcms, 'correlation')))
    results = results.flatten()
    return results

#Call this fucntion to measure the similarity of two feature vectors of EHD
def compareGLCMFeatures(image1, image2):
    feature1 = GLCMFeatures(image1)
    feature2 = GLCMFeatures(image2)
    return distance.braycurtis(feature1, feature2)


################################################################################
# TESTS
################################################################################

# The unittest module provides nice utilities for testing
# Check out docs at https://docs.python.org/3/library/unittest.html !!!
class TestGLCMFeatures(unittest.TestCase):

    def test_GLCMFeatures(self):
        """Should output the designated features of GCLM"""
        thispath = os.path.dirname(__file__)
        impath1 = os.path.join("test", "740.jpg")
        img1 = cv2.imread(os.path.join(thispath, impath1))
        impath2 = os.path.join("test", "741.jpg")
        img2 = cv2.imread(os.path.join(thispath, impath2))
        print compareGLCMFeatures(img1, img2)



# This if statement gets executed when you run this file, so > python color.py
if __name__ == '__main__':
    # It's a convenient way of running unittests!
    unittest.main()
