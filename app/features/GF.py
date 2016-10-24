import numpy as np
import os
import cv2
import unittest
import skimage
from scipy.spatial import distance
from skimage.filters import gabor_kernel
from scipy import ndimage as nd

"""
Function that calculate the Gabor filter features of an image.

Coded by An Li
"""
class GaborFeatures():
    def __init__(self):
        # prepare filter bank kernels
        self.kernels = []
        for theta in range(4):
            theta = theta / 4. * np.pi
            for sigma in (1, 3):
                for frequency in (0.05, 0.25):
                    kernel = np.real(
                        gabor_kernel(
                            frequency, theta=theta,
                            sigma_x=sigma, sigma_y=sigma))
                    self.kernels.append(kernel)

    def feats_gabor(self, data3d):
        """
        Compute features based on Gabor filters.
        """
        fv = self.__compute_gabor_feats(
            data3d[:, :, 0], self.kernels).reshape(-1)
        return fv.astype(np.float32)

    def __compute_gabor_feats(self, image, kernels):
        feats = np.zeros((len(kernels), 2), dtype=np.double)
        for k, kernel in enumerate(kernels):
            filtered = nd.convolve(image, kernel, mode='wrap')
            feats[k, 0] = filtered.mean()
            feats[k, 1] = filtered.var()
        return feats

    #Call this fucntion to measure the similarity of two feature vectors of GF
    def compareGFFeatures(self, img1, img2):
        feature1 = self.feats_gabor(img1)
        feature2 = self.feats_gabor(img2)
        return cv2.compareHist(feature1, feature2, 3)

################################################################################
# TESTS
################################################################################

# The unittest module provides nice utilities for testing
# Check out docs at https://docs.python.org/3/library/unittest.html !!!
class TestGFFeatures(unittest.TestCase):

    def test_GFFeatures(self):
        """Should output the designated features of GF"""
        thispath = os.path.dirname(__file__)
        impath1 = os.path.join("test", "737.jpg")
        img1 = cv2.imread(os.path.join(thispath, impath1))
        impath2 = os.path.join("test", "740.jpg")
        img2 = cv2.imread(os.path.join(thispath, impath2))
        gf = GaborFeatures()
        results = gf.compareGFFeatures(img1, img2)
        print results

# This if statement gets executed when you run this file, so > python color.py
if __name__ == '__main__':
    # It's a convenient way of running unittests!
    unittest.main()
