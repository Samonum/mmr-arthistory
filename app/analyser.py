#from utils import get_tree
import scipy.optimize as opt
import numpy
import unittest
import json
import os
import cv2
import matplotlib.pyplot as plt


import utils

from features import color
#from features import EHD, GF, GLCM

def linear_regression(x, y):
    """
    Given two matching data sets caculates the closest fitting line
    using the least squares method and the correlation coefficient.
    Returns: coefficients of the line, correlation coefficient
    """
    def f(x, a, b):
        return a+b*x
    yay, _ = opt.curve_fit(f, x, y)
    covar = numpy.cov(x,y)
    
    stdev = numpy.sqrt(numpy.diag(covar))
    return yay,(covar[0][1]/(stdev[0]*stdev[1]))

def analyse_features():
    resultPath = os.path.join(os.getcwd(), os.path.join('data','results.json'))
    resultFile = open(resultPath, 'r')
    resultArray = json.load(resultFile)
    
    cUserRating = []
    hsvHist = []
    bitmap = []
    bic = []
    hsvHistu = []
    bitmapu = []
    bicu = []
    
    
    t = utils.get_tree()
    
    
    EHD = []
    GF = []
    GLCM = []
    EHDu = []
    GFu = []
    GLCMu = []
    
    i = 0
    c = 0
    hash = 0
    for item in resultArray:
        i += 1
        c *= hash == item['sessionhash']
        hash = item['sessionhash']
        c += item['votevalue'] == "0"
        if c == 30:
            break
    
    resultArray = resultArray[i:]
    
    hash = {}
    for item in resultArray:
        try:
            hash[item['sessionhash']] +=1
        except KeyError:
            hash[item['sessionhash']] = 1
        
    print hash
    print len(hash)
    for item in resultArray:
        if item['votevalue'] == "0" or hash[item['sessionhash']] < 30:# or not item['similarimg']['random']:
            continue
        img1 = int(item['mainimg']['index'])
        img2 = int(item['similarimg']['index'])
        if item['similarimg']['random']:
            if item['mainimg']['compare_by'] == 'color':
                hsvHistu.append(1-(float(item['votevalue'])-1)/4)
                bitmapu.append(1-(float(item['votevalue'])-1)/4)
                bicu.append(1-(float(item['votevalue'])-1)/4)
                comp = color.ColorFeatureExtracter.CompareFeatures(t[img1]['features'],t[img2]['features'])
                hsvHist.append(comp['HsvHist'])
                bitmap.append(comp['ColorBitmap'])
                bic.append(comp['BIC'])
            else:
                EHDu.append(1-(float(item['votevalue'])-1)/4)
                EHD.append(cv2.compareHist(t[img1]['features']['EHD'], t[img2]['features']['EHD'],3))
                GFu.append(1-(float(item['votevalue'])-1)/4)
                GF.append(cv2.compareHist(t[img1]['features']['GF'], t[img2]['features']['GF'], 3))
                GLCMu.append(1-(float(item['votevalue'])-1)/4)
                GLCM.append(cv2.compareHist(t[img1]['features']['GLCM'], t[img2]['features']['GLCM'],3))
        else:
            if(item['mainimg']['feature'] == 'HsvHist'):
                comp = color.ColorFeatureExtracter.CompareFeatures(t[img1]['features'],t[img2]['features'])
                hsvHist.append(comp['HsvHist'])
                hsvHistu.append(1-(float(item['votevalue'])-1)/4)
            if(item['mainimg']['feature'] == 'ColorBitmap'):
                comp = color.ColorFeatureExtracter.CompareFeatures(t[img1]['features'],t[img2]['features'])
                bitmap.append(comp['ColorBitmap'])
                bitmapu.append(1-(float(item['votevalue'])-1)/4)
            if(item['mainimg']['feature'] == 'BIC'):
                comp = color.ColorFeatureExtracter.CompareFeatures(t[img1]['features'],t[img2]['features'])
                bic.append(comp['BIC'])
                bicu.append(1-(float(item['votevalue'])-1)/4)
            if(item['mainimg']['feature'] == 'EHD'):
                EHD.append(cv2.compareHist(t[img1]['features']['EHD'], t[img2]['features']['EHD'],3))
                EHDu.append(1-(float(item['votevalue'])-1)/4)
            if(item['mainimg']['feature'] == 'GF'):
                GF.append(cv2.compareHist(t[img1]['features']['GF'], t[img2]['features']['GF'], 3))
                GFu.append(1-(float(item['votevalue'])-1)/4)
            if(item['mainimg']['feature'] == 'GLCM'):
                GLCM.append(cv2.compareHist(t[img1]['features']['GLCM'], t[img2]['features']['GLCM'],3))
                GLCMu.append(1-(float(item['votevalue'])-1)/4)
            
    plt.plot(hsvHistu,hsvHist, 'or')
    #plt.show()
    print 'HsvHist'
    print linear_regression(hsvHistu,hsvHist)
    print "Bitmap"
    print linear_regression(bitmapu,bitmap)
    print "BIC"
    print linear_regression(bicu,bic)
    #print tUserRating
    #print EHD
    print "EHD"
    print linear_regression(EHDu,EHD)
    print "GF"
    print linear_regression(GFu,GF)
    print "GLCM"
    print linear_regression(GLCMu,GLCM)
    return 


################################################################################
# TESTS
################################################################################

# The unittest module provides nice utilities for testing
# Check out docs at https://docs.python.org/3/library/unittest.html !!!
class TestColorFeatures(unittest.TestCase):

    def test_lin_reg(self):
        """Should output correct hue count, for the given image 4"""
        
        x = range(0,40000)
        y = range(10,80010,2)

        analyse_features();
        print linear_regression(x, y)
        # ... and then evaluate the output

# This if statement gets executed when you run this file, so > python color.py
if __name__ == '__main__':
    # It's a convenient way of running unittests!
    unittest.main()
