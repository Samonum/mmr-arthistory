#
# Utilities for handling painting data and more
#

import xml.etree.ElementTree as ET
import xmltodict
import sys
from features import color
import cv2
import unittest
version = sys.version_info.major

if version == 2:
    import cPickle as pickle
else:
    import pickle

def get_tree(remember={}):
    # Memoize tree, using the fact that kwargs only get instantiated once
    if not remember.get('tree'):
        with open('./data/extracted.pickle', 'r') as f:
            if version == 2:
                remember['tree'] = pickle.load(f)
            else:
                remember['tree'] = pickle.load(f, encoding='latin1')
    return remember['tree']

def save_tree(tree):
    with open('./data/extracted.pickle', 'wb') as f:
        pickle.dump(tree, f)

def get_tree_xml(remember={}):
    # Memoize tree, using the fact that kwargs only get instantiated once
    if not remember.get('tree'):
        with open('./data/extracted.xml', 'rb') as f:
            remember['tree'] = xmltodict.parse(f)['kunstwerken']['kunstwerk']
    return remember['tree']

def dist(img1, img2):
    """Calculate distance between two feature vectors, given their index"""
    t = get_tree()
    comp = color.ColorFeatureExtracter.CompareFeatures(t[img1]['features'],t[img2]['features'])
    comp['EHD'] = cv2.compareHist(t[img1]['features']['EHD'], t[img2]['features']['EHD'],3)
    comp['GF'] =  cv2.compareHist(t[img1]['features']['GF'], t[img2]['features']['GF'],3)
    comp['GLCM'] =  cv2.compareHist(t[img1]['features']['GLCM'], t[img2]['features']['GLCM'],3)
    #weights from analyser
    return 0.4606 * (0.06253 + comp['HsvHist'] * 0.4211) + 0.4870 * (0.1255 + comp['ColorBitmap'] * 0.1805) + 0.4337 * (0.08637 + comp['BIC'] * 0.4337) + 0.1430 * (0.08163 + comp['EHD'] * 0.06479) + 0.3064 * (0.04185 + comp['GF'] * 0.1200) + 0.2211 * (0.02248 + comp['GLCM'] * 0.03979)

class TestColorFeatures(unittest.TestCase):

    def test_dist(self):
        """Should output correct hue count, for the given image 4"""
        print dist(1,1)
        print dist(1,4)
        
        # ... and then evaluate the output

# This if statement gets executed when you run this file, so > python color.py
if __name__ == '__main__':
    # It's a convenient way of running unittests!
    unittest.main()
