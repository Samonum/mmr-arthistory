from __future__ import division
import unittest
import cv2
import math
import os
import numpy

################################################################################
# FUNCTIONS
################################################################################
        
                
class ColorFeatureExtracter:
    _hsvHistogram = 0
    _bicHistogram = 0
    _opencvimg = 0
    _hsvimg = 0
    _rgbHistogram = 0
    _rgbAvrg = 0
    _rgbStd = 0
    _bitmap = 0
    
    def __init__(self, opencvimage):
        self._opencvimg = opencvimage
    
    #THE method to call for All your colour related features!
    def ComputeFeatures(self):
        res = {}
        res['ColorBitmap'] = self.ColorBitmap()
        res['HsvHist']      = self.HsvHistogram()
        res['BIC']          = self.BICHistogram()
        return res
    
    #THE method to call for All your colour related comparisons
    @staticmethod
    def CompareFeatures(features1, features2):
        res = {}
        for key in features1:
            if(key == "HsvHist"):
                res[key] = cv2.compareHist(features1[key], features2[key], 3)
            if(key == "BIC"):
                res[key] = cv2.compareHist(features1[key], features2[key], 3)
            if(key == "ColorBitmap"):
                res[key] = ColorFeatureExtracter.CompareColorBitmap(features1[key], features2[key])
        return res
     
    @staticmethod
    def CompareColorBitmap(map1, map2):
        res = numpy.linalg.norm(map1['sd'] - map2['sd'])/128
        res += numpy.linalg.norm(map1['avrg'] - map2['avrg'])/256
        res += numpy.sum(map1['bitmap'] != map2['bitmap'])/map1['bitmap'].size
        res /= 3
        return res
        
    
    def HsvHistogram(self):
        """
        Generates a histogram based on the given HSV image.
        The histogram contains 20 bins for different hue values and 8 bins for greyscale.
        """
        if self._hsvHistogram:
            return self._hsvHistogram
        hsvimg = self.HsvImage()
        #Note that in OpenCV hsv uses the ranges [0,179], [0,255] and [0,255] respectively
        histogram = numpy.zeros(28, dtype=numpy.float32)
        [width, height, depth] = hsvimg.shape
        for y in xrange(height):
            for x in xrange(width):
                    histogram[self.HsvBin(hsvimg[x][y])] += 1
                    
        histogram /= width*height
        
        sHistogram = numpy.zeros(28, dtype=numpy.float32)
        sHistogram[0] = 0.25 * histogram[20] +  0.5 * histogram[0] +  0.25 * histogram[1]
        sHistogram[20] = 0.5 * histogram[20] +  0.25 * histogram[0] +  0.25 * histogram[19]
        
        for i in xrange(1, 19):
            sHistogram[i] = 0.25 * histogram[i-1] +  0.5 * histogram[i] +  0.25 * histogram[i+1]
        
        self._hsvHistogram = sHistogram
        return sHistogram
        
    def HsvBin(self, pixel):
        if pixel[1] > 255-.8*pixel[2]:
            return pixel[0] // 9
        return 20+pixel[2]//32
        
        
        
    def BICHistogram(self):
        """
        Generates a histogram based on the given HSV image.
        The histogram contains 20 bins for different hue values and 8 bins for greyscale.
        """
        if not self._bicHistogram is 0:
            return self._bicHistogram
        hsvimg = self.HsvImage()
        #Note that in OpenCV hsv uses the ranges [0,179], [0,255] and [0,255] respectively
        histogram = numpy.zeros(56, dtype=numpy.float32)
        [width, height, depth] = hsvimg.shape
        swidth = width-1
        sheight = height-1
        for y in xrange(height):
            for x in xrange(width):
                index = self.HsvBin(hsvimg[x][y])
                if index != self.HsvBin(hsvimg[min(x+1, swidth)][min(y+1, sheight)]) or index != self.HsvBin(hsvimg[min(x+1, swidth)][max(y-1, 0)]) or index != self.HsvBin(hsvimg[max(x-1, 0)][min(y+1, sheight)]) or index != self.HsvBin(hsvimg[min(x-1, 0)][min(y-1, 0)]):
                    histogram[28+index] += 1
                else:
                    histogram[index] += 1
        histogram /= width*height
        print(histogram)
        sHistogram = numpy.zeros(56, dtype=numpy.float32)
        sHistogram[0] = 0.25 * histogram[20] +  0.5 * histogram[0] +  0.25 * histogram[1]
        sHistogram[20] = 0.5 * histogram[20] +  0.25 * histogram[0] +  0.25 * histogram[19]
        
        for i in xrange(1, 19):
            sHistogram[i] = 0.25 * histogram[i-1] +  0.5 * histogram[i] +  0.25 * histogram[i+1]
        
        sHistogram[28] = 0.25 * histogram[48] +  0.5 * histogram[28] +  0.25 * histogram[29]
        sHistogram[48] = 0.5 * histogram[48] +  0.25 * histogram[28] +  0.25 * histogram[47]
        
        for i in xrange(29, 47):
            sHistogram[i] = 0.25 * histogram[i-1] +  0.5 * histogram[i] +  0.25 * histogram[i+1]
        self._bicHistogram = sHistogram
        return sHistogram
    
    def HsvImage(self):
        if self._hsvimg is 0:
            self._hsvimg = cv2.cvtColor(self._opencvimg, cv2.COLOR_BGR2HSV)
        return self._hsvimg
        
    def RgbHistogram(self):
        """
        Generates a RGB histogram based on the given image.
        """
        if not self._rgbHistogram is 0:
            return self._rgbHistogram
        [width, height, depth] = self._opencvimg.shape
        histogram = numpy.zeros(48, dtype=numpy.float32)
        
        for y in xrange(height):
            for x in xrange(width):
                for i in xrange(depth):
                    histogram[i*16+self._opencvimg.item(x, y, i)//16] += 1
        histogram /= width*height
        self._rgbHistogram = histogram
        return self._rgbHistogram
    
    def RgbAverages(self):
        if not self._rgbAvrg is 0:
            return self._rgbAvrg
        flatrgb = self._opencvimg.reshape(-1, self._opencvimg.shape[-1])
        total = numpy.sum(flatrgb, axis=0)
        self._rgbAvrg = total / (flatrgb.shape[0])
        return self._rgbAvrg
        
    def RgbStandardDeviation(self):
        if not self._rgbStd is 0:
            return self._rgbStd
        flatrgb = self._opencvimg.reshape(-1, self._opencvimg.shape[-1])
        rgbAvrg = self.RgbAverages()
        rgbStd = flatrgb - rgbAvrg
        rgbStd = numpy.abs(rgbStd)
        
        rgbStd = numpy.sum(rgbStd, axis=0)
        rgbStd /= (flatrgb.shape[0])
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
        impath2 = os.path.join("test", "lady.png")
        
        img = cv2.imread(os.path.join(thispath, impath))
        img2 =  cv2.imread(os.path.join(thispath, impath2))
        colorextr = ColorFeatureExtracter(img)
        colorextr2 = ColorFeatureExtracter(img2)
        print(colorextr.CompareFeatures(colorextr2.ComputeFeatures(),colorextr.ComputeFeatures()))
        # ... and then evaluate the output

# This if statement gets executed when you run this file, so > python color.py
if __name__ == '__main__':
    # It's a convenient way of running unittests!
    unittest.main()
