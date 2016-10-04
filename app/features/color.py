import unittest
import cv2
import math
import os
import numpy

################################################################################
# FUNCTIONS
################################################################################
class ColorFeatureExtracter:
    _histogram = 0;
    _opencvimg = 0;
    _hlsimg = 0;
    
    def __init__(self, opencvimage):
        self._opencvimg = opencvimage
    
    def getHlsHistogram(self):
        """
        Generates a histogram based on the given HLS image.
        The histogram contains 20 bins for different hue values and 1 bin for greyscale.
        """
        if self._histogram:
            return self._histogram
        hlsimg = self.getHlsImage()
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
        self._histogram = histogram
        return histogram
    
    def getHlsImage(self):
        if not self._hlsimg:
            self._hlsimg = cv2.cvtColor(self._opencvimg, cv2.COLOR_BGR2HLS)
        return self._hlsimg
    
    def getHueCount(self):
        #Algorithm parameters
        noiseThreshold = .05

        histogram = self.getHlsHistogram()
        maxColor = max(histogram)
        return len([x for x in histogram if x > maxColor * noiseThreshold])
    
    def getMostCommonColor(self):
        histogram = getHlsHistogram()
        return histogram.index(max(histogram))

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
        colorextr = ColorFeatureExtracter(img)
        count = colorextr.getHueCount()
        self.assertEqual(count, 4)
        # ... and then evaluate the output

# This if statement gets executed when you run this file, so > python color.py
if __name__ == '__main__':
    # It's a convenient way of running unittests!
    unittest.main()
