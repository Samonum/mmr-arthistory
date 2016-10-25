#
# Utilities for handling painting data and more
#

import xml.etree.ElementTree as ET
import xmltodict
import json

def get_tree(remember={}):
    # Memoize tree, using the fact that kwargs only get instantiated once
    if not remember.get('tree'):
        with open('./data/extracted.json', 'r') as f:
            remember['tree'] = json.load(f)
    return remember['tree']

def save_tree(tree):
    with open('./data/extracted.json', 'w') as f:
        json.dump(tree, f)

def get_tree_xml(remember={}):
    # Memoize tree, using the fact that kwargs only get instantiated once
    if not remember.get('tree'):
        with open('./data/extracted.xml', 'rb') as f:
            remember['tree'] = xmltodict.parse(f)['kunstwerken']['kunstwerk']
    return remember['tree']

def dist(vec1, vec2):
    "Calculate distance between two feature vectors"
    return 1
