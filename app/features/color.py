import unittest
import cv2
import math
import os
import numpy

################################################################################
# FUNCTIONS
################################################################################
        
                
class ColorFeatureExtracter:
    _hlsHistogram = 0
    _opencvimg = 0
    _hlsimg = 0
    _rgbHistogram = 0
    _rgbAvrg = 0
    _rgbStd = 0
    _bitmap = 0
    
    def __init__(self, opencvimage):
        self._opencvimg = opencvimage
    
    #THE method to call for All your colour related features!
    def ComputeFeatures(self):
        res = {}
        res['ColorBitmap']  = self.ColorBitmap()
        res['RgbHist']      = self.RgbHistogram()
        return res
    
    #THE method to call for All your colour related comparisons
    @staticmethod
    def CompareFeatures(features1, features2):
        res = {}
        for key in features1:
            if(key == "RgbHist"):
                res[key] = cv2.compareHist(features1[key], features2[key], 3)
            if(key == "ColorBitmap"):
                res[key] = ColorFeatureExtracter.CompareColorBitmap(features1[key], features2[key])
        return res
     
    @staticmethod
    def CompareColorBitmap(map1, map2):
        res = numpy.linalg.norm(map1['sd'] - map2['sd'])
        res += numpy.linalg.norm(map1['avrg'] - map2['avrg'])
        res += numpy.sum(map1['bitmap'] != map2['bitmap'])/map1['bitmap'].shape[0]
        res /= 3
        return res
        
    
    #depricated
    def HlsHistogram(self):
        """
        Generates a histogram based on the given HLS image.
        The histogram contains 20 bins for different hue values and 1 bin for greyscale.
        """
        if self._hlsHistogram:
            return self._hlsHistogram
        hlsimg = self.HlsImage()
        #Algorithm parameters
        #Note that in OpenCV hls uses the ranges [0,179], [0,255] and [0,255] respectively
        saturationThreshold = (int)(.2 * 255)
        minLightness = (int)(.15 * 255)
        maxLightness = (int)(.95 * 255)
        
        
        histogram = [0] * 21
        [width, height, depth] = hlsimg.shape
        
        for y in range(height):
            for x in range(width):
                #If not greyscale
                if hlsimg.item(x, y, 2) > saturationThreshold or minLightness < hlsimg.item(x, y, 1) < maxLightness:
                    histogram[hlsimg.item(x, y, 0) // 9] += 1
                #Else
                else:
                    histogram[20] += 1
        
        self._hlsHistogram = histogram
        return histogram
    
    def HlsImage(self):
        if not self._hlsimg:
            self._hlsimg = cv2.cvtColor(self._opencvimg, cv2.COLOR_BGR2HLS)
        return self._hlsimg
        
    #depricated
    def HueCount(self):
        #Algorithm parameters
        noiseThreshold = .05

        histogram = self.HlsHistogram()
        maxColor = max(histogram)
        return len([x for x in histogram if x > maxColor * noiseThreshold])
        
    #depricated
    def MostCommonColor(self):
        histogram = HlsHistogram()
        return histogram.index(max(histogram))
        
    def RgbHistogram(self):
        """
        Generates a RGB histogram based on the given image.
        """
        if not self._rgbHistogram is 0:
            return self._rgbHistogram
        [width, height, depth] = self._opencvimg.shape
        histogram = [[0]*16,[0]*16, [0]*16]
        
        for y in range(0, height):
            for x in range(0, width):
                for i in range(0, depth):
                    histogram[i][self._opencvimg.item(x, y, i)//16] += 1
        histogram = list(map(lambda rgb: list(map(lambda x: x/(width*height), rgb)), histogram))
        self._rgbHistogram = numpy.asarray(histogram, dtype=numpy.float32)
        return self._rgbHistogram
    
    def RgbAverages(self):
        if not self._rgbAvrg is 0:
            return self._rgbAvrg
        flatrgb = self._opencvimg.reshape(-1, self._opencvimg.shape[-1])
        total = numpy.sum(flatrgb, axis=0)
        self._rgbAvrg = total / (flatrgb.shape[0]*256)
        return self._rgbAvrg
        
    def RgbStandardDeviation(self):
        if not self._rgbStd is 0:
            return self._rgbStd
        flatrgb = self._opencvimg.reshape(-1, self._opencvimg.shape[-1])
        rgbAvrg = self.RgbAverages()
        rgbStd = flatrgb - rgbAvrg
        rgbStd *= rgbStd
        rgbStd /= (flatrgb.shape[0] *128)
        rgbStd = numpy.sum(rgbStd, axis=0)
        numpy.sqrt(rgbStd, rgbStd)
        self._rgbStd = rgbStd
        return self._rgbStd
        
    def BitMap(self):
        if not self._bitmap is 0:
            return self._bitmap
        bitmapScaled = cv2.resize(self._opencvimg, (10,10))
        globAvrg = self.RgbAverages()
        bitmap = numpy.empty((10,10,3))
        bitmap = numpy.greater_equal(bitmapScaled, globAvrg)
        self._bitmap = bitmap
        return bitmap
    
    def ColorBitmap(self):
        return {'bitmap': self.BitMap(), 'sd':self.RgbStandardDeviation(), 'avrg': self.RgbAverages()}
        
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
        
        print(colorextr.CompareFeatures(colorextr.ComputeFeatures(),colorextr.ComputeFeatures()))
        # ... and then evaluate the output

# This if statement gets executed when you run this file, so > python color.py
if __name__ == '__main__':
    # It's a convenient way of running unittests!
    unittest.main()
