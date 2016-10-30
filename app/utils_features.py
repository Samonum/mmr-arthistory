#
# Utilities for features, like distance calcs
#

from features.color import ColorFeatureExtracter
import random
import cv2

colorfeats = (
    'HsvHist',
    'BIC',
    'ColorBitmap',
)
texturefeats = (
    'EHD',
    'GF',
    'GLCM',
)

def get_random_feature(category):
    if category == 'color':
        return random.choice(colorfeats)
    elif category == 'texture':
        return random.choice(texturefeats)
    else:
        raise Warning("Unknown feature category")

def dist(featname, a, b):
    "Returns distance between feature vectors a and b"
    if featname in ('HsvHist', 'BIC', 'EHD', 'GF', 'GLCM'):
        return cv2.compareHist(a, b, 3)
    elif featname in ('ColorBitmap'):
        return ColorFeatureExtracter.CompareColorBitmap(a,b)
    else:
        raise Warning("Feature name >{}< not recognized".format(featname))

if __name__ == '__main__':
    # Test stuff
    import cPickle as pickle
    from utils import get_tree
    e = get_tree()

    i,j = 50,180
    for featname, val1 in e[i]['features'].items():
        val2 = e[j]['features'][featname]
        d = dist(featname, val1, val2)
        print("Comparing {featname} feature, distance between {i} and {j} is {d:.2f}".format(
        featname=featname, i=i, j=j, d=d))
