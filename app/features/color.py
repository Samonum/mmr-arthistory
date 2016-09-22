import unittest
import cv2
import math
import os
import numpy

################################################################################
# FUNCTIONS
################################################################################
def generateHlsHistogram(hlsimg):
    """
    Generates a histogram based on the given HLS image.
    The histogram contains 20 bins for different hue values and 1 bin for greyscale.
    """
    #Algorithm parameters
    #Note that in OpenCV hls uses the ranges [0,179], [0,255] and [0,255] respectively
    saturationThreshold = (int)(.2 * 255)
    minLightness = (int)(.15 * 255)
    maxLightness = (int)(.95 * 255)
    
    
    histogram = [0] * 21
    [width, height, depth] = hlsimg.shape
    
    for y in range(0, height):
        for x in range(0, width):
            #If not greyscale
            if hlsimg.item(x, y, 2) > saturationThreshold or minLightness < hlsimg.item(x, y, 1) < maxLightness:
                histogram[hlsimg.item(x, y, 0) // 9] += 1
            #Else
            else:
                histogram[20] += 1
    return histogram


def huefeatures(image):
    """
    Function that returns the amount of different colours detected within the image.

    Takes a OpenCV image
    Returns the number of different colours

    Feature from: 'The Design of High-Level Features for Photo Quality Assessment' by Y.Ke et al. (2006)

    Coded by Sam
    """
    #Algorithm parameters
    noiseThreshold = .05

    #Convert image
    hlsimg = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    histogram = generateHlsHistogram(hlsimg)

    #Return the number of colours that pass the threshold (threshold relative to max count)
    maxColor = max(histogram)
    return [len([x for x in histogram if x > maxColor * noiseThreshold]),(histogram.index(maxColor)*9)+10, maxColor]


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
        count = huefeatures(img)[0]
        self.assertEqual(count, 4)
        # ... and then evaluate the output

# This if statement gets executed when you run this file, so > python color.py
if __name__ == '__main__':
    # It's a convenient way of running unittests!
    unittest.main()
