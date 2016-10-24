import unittest
import numpy as np
import cv2
import os
from scipy.spatial import distance
from SimpleCV import Image, np, EdgeHistogramFeatureExtractor

def EHDFeatures(image):
    """
    Function that calculate the edge histogram of an image.

    Coded by An Li
    """

    img1 = Image(image)

    edgeFeats = EdgeHistogramFeatureExtractor(bins=16)

    results = np.array(edgeFeats.extract(img1), dtype = np.float32)

    return results

#Call this fucntion to measure the similarity of two feature vectors of EHD
def compareEHDFeatures(image1, image2):
    feature1 = EHDFeatures(image1)
    feature2 = EHDFeatures(image2)
    return cv2.compareHist(feature1, feature2, 3)


################################################################################
# TESTS
################################################################################

# The unittest module provides nice utilities for testing
# Check out docs at https://docs.python.org/3/library/unittest.html !!!
class TestEHDFeatures(unittest.TestCase):

    def test_EHDFeatures(self):
        """Should output the designated features of EHD"""
        thispath = os.path.dirname(__file__)
        impath1 = os.path.join("test", "740.jpg")
        img1 = cv2.imread(os.path.join(thispath, impath1))
        impath2 = os.path.join("test", "741.jpg")
        img2 = cv2.imread(os.path.join(thispath, impath2))
        print compareEHDFeatures(img1, img2)

# This if statement gets executed when you run this file, so > python color.py
if __name__ == '__main__':
    # It's a convenient way of running unittests!
    unittest.main()
