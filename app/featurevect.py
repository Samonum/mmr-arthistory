#
# Calculates feature vector for all paintings, stores it in extracted.json
#

import cv2
from features import color
from utils import get_tree, save_tree
import os
import time

c = time.clock

testlimit = 1

if __name__ == '__main__':
    t = get_tree()

    for painting in t[:testlimit]:
        painting['features'] = {}
        fn = painting['afbeelding']

        # Always run from repo root dir
        path = os.path.abspath(os.path.join('.', 'data', *fn.split('/')))
        print("Getting painting {}".format(path))
        cvim = cv2.imread(path)
        cfe = color.ColorFeatureExtracter(cvim)

        t1 = c()
        cfe.ComputeFeatures()
        t2 = c()
        print("Extracting color features took {:.6f}s".format(t2-t1))

        # Save tree with feature vects
        # save_tree(t)
