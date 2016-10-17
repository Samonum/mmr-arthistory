import unittest
import cv2
import numpy as np
import os
def CalNonBlackPixels(image):
    """
    Function that returns the ratio of non-black pixels in an image.

    This fuction is used to analyze the complexity of an image. After detecting
    all edges in the image, we get an image that consists of black pixels and
    non-black pixels(white, gray or something approximates to them), we call it
    egde-version image.

    We use the edge-version image and scan all pixels to find non-black pixels(
    B >= 125, G >= 125 and R >= 125).

    Coded by An Li
    """
    #Set the threshold of three color channels to filter black pixels
    pvalue = 125
    #The counter of non-black pixels that are found during scanning
    count = 0
    #Get rows and columns of the pixel array
    rows, cols, channels = image.shape

    #The iteration for finding non-black pixels
    for i in range(rows):
        for j in range(cols):
            #Access each channel of a pixel
            k1 = image.item(i,j,0)
            k2 = image.item(i,j,1)
            k3 = image.item(i,j,2)
            #If we find a non-black pixel then increase the counter
            if k1 >= pvalue and k2 >= pvalue and k3 >= pvalue:
                count += 1

    #Get the number of all pixels, img.size returns the total number of channels
    #so we need to divide 3
    size = image.size/3.000
    #Calculate the ratio of non-black pixels and show it in the form of percentage
    NonBlackRatio = (count/size)*100

    #return the ratio of non-black pixels
    return NonBlackRatio

################################################################################
# TESTS
################################################################################

# The unittest module provides nice utilities for testing
# Check out docs at https://docs.python.org/3/library/unittest.html !!!
class TestNonBlackPixelFeatures(unittest.TestCase):

    def test_NonBlackPixels(self):
        """Should output the ratio of non-black pixels"""
        thispath = os.path.dirname(__file__)
        impath = os.path.join("test", "lady.png")
        img = cv2.imread(os.path.join(thispath, impath))
        ratio = CalNonBlackPixels(img)
        print("The ratio of non-black region is %.2f%%" % ratio)

# This if statement gets executed when you run this file, so > python color.py
if __name__ == '__main__':
    # It's a convenient way of running unittests!
    unittest.main()
