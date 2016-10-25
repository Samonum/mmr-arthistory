#
# Utilities for handling painting data and more
#

import xml.etree.ElementTree as ET
import xmltodict
import sys
version = sys.version_info.major

if version == 2:
    import cPickle as pickle
else:
    import pickle

def get_tree(remember={}):
    # Memoize tree, using the fact that kwargs only get instantiated once
    if not remember.get('tree'):
        with open('./data/extracted.pickle', 'r') as f:
            remember['tree'] = pickle.load(f)
    return remember['tree']

def save_tree(tree):
    with open('./data/extracted.pickle', 'w') as f:
        pickle.dump(tree, f)

def get_tree_xml(remember={}):
    # Memoize tree, using the fact that kwargs only get instantiated once
    if not remember.get('tree'):
        with open('./data/extracted.xml', 'rb') as f:
            remember['tree'] = xmltodict.parse(f)['kunstwerken']['kunstwerk']
    return remember['tree']

def dist(vec1, vec2):
    "Calculate distance between two feature vectors"
    return 1
