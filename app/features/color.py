import unittest
import cv2
import math
import os

################################################################################
# FUNCTIONS
################################################################################
def huecount(image):
    """
    Function that returns the amount of different colours detected within the image.

    Takes a OpenCV image
    Returns the number of different colours

    Feature from: 'The Design of High-Level Features for Photo Quality Assessment' by Y.Ke et al. (2006)

    Coded by Sam
    """
    #Algorithm parameters
    #Note that in OpenCV HSV uses the ranges [0,179], [0,255] and [0,255] respectively
    saturationThreshold = .2 * 255
    minValue = .15 * 255
    maxValue = .95 * 255
    noiseThreshold = .05

    #Convert image
    hsvimg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    histogram = [0] * 21

    #Loop over all pixels
    for row in hsvimg:
        for hsvpx in row:
            #If not greyscale
            if hsvpx[1] > saturationThreshold or minValue < hsvpx[2] < maxValue:
                histogram[hsvpx[0] // 9] += 1
            #Else
            else:
                histogram[20] += 1

    #Return the number of colours that pass the threshold (threshold relative to max count)
    maxColor = max(histogram)
    return len([x for x in histogram if x > maxColor * noiseThreshold])


################################################################################
# TESTS
################################################################################

# The unittest module provides nice utilities for testing
# Check out docs at https://docs.python.org/3/library/unittest.html !!!
class TestColorFeatures(unittest.TestCase):

    def test_hue(self):
        """Should output correct hue count, for the given image 4"""
        thispath = os.path.dirname(__file__)
        impath = os.path.join("test", "opencv-logo.png")
        img = cv2.imread(os.path.join(thispath, impath))
        count = huecount(img)
        self.assertEqual(count, 4)
        # ... and then evaluate the output

# This if statement gets executed when you run this file, so > python color.py
if __name__ == '__main__':
    # It's a convenient way of running unittests!
    unittest.main()
