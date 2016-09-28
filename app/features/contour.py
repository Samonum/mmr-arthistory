import unittest
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

def CalContour(image):
    """
    Function that returns the contours detected within in the image.

    Takes an image, using Canny edge detection to get all edges of it and store
    the edge-image

    Uses the edge-version image and calls findContours() function to calculate all
    contours of the edge-version image

    Returns the length of all contours in the image

    Coded by An Li
    """
    #Use Canny edge detection to find all edges
    edges = cv2.Canny(image, 100, 200)

    #Create the edge-version image and save it
    plt.subplot(111), plt.imshow(edges, cmap = 'gray')
    plt.xticks([]), plt.yticks([])
    plt.savefig('test\Cannyedge.png', transparent = True, bbox_inches = 'tight')

    #Load the edge-version image and convert it from RGB to GRAY
    img1 = cv2.imread('test\Cannyedge.png')
    img2 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    #Use findContours() to find all contours
    ret,thresh = cv2.threshold(img2,127,255,0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #return the length of all contours
    return len(contours)

################################################################################
# TESTS
################################################################################

# The unittest module provides nice utilities for testing
# Check out docs at https://docs.python.org/3/library/unittest.html !!!
class TestContourFeatures(unittest.TestCase):

    def test_contour(self):
        """Should output the length of the contours"""
        thispath = os.path.dirname(__file__)
        impath = os.path.join("test", "opencv-logo.png")
        img = cv2.imread(os.path.join(thispath, impath))
        count = CalContour(img)
        print(count)

# This if statement gets executed when you run this file, so > python color.py
if __name__ == '__main__':
    # It's a convenient way of running unittests!
    unittest.main()
