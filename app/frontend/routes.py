from flask import render_template
from . import showoffapp, trainingapp, api
from ..utils import get_tree
import random
from flask import json, send_file, request
import os
import random
import datetime
import logging
from ..utils_features import dist, get_random_feature
from ..utils import dist as utils_dist
from time import clock as c
from pymongo import MongoClient
db = MongoClient().resultdb.results

logging.basicConfig(filename='log.txt', level=logging.DEBUG)
logger = logging.getLogger(__name__)

@showoffapp.route("/")
def index():
    return render_template("show.html")

@trainingapp.route("/")
def train():
    return render_template("train.html")

################################################################################
# API
################################################################################

def compare_by():
    if random.randint(0,1):
        return {'compare_by': 'color',
                'feature': get_random_feature('color'),
                'msg': "Compare the two paintings based on <span>color</span>."}
    else:
        return {'compare_by': 'texture',
                'feature': get_random_feature('texture'),
                'msg': "Compare the two paintings based on <span>texture</span>."}

def copylistdict(a, b, *names):
    "Copy names from list of dicts a to list of dicts b"
    keyerrs = {}
    for i in a:
        add = {}
        for n in names:
            try:
                add[n] = i[n]
            except KeyError as e:
                if keyerrs.get(n): keyerrs[n] += 1
                else: keyerrs[n] = 1
        b.append(add)
    print("\nKeyerrors: " + str(keyerrs) + "\n")

@api.route("/get_all_paintings")
def get_all_paintings():
    tree = get_tree()
    for i, p in enumerate(tree):
        p['index'] = i
    # prune for important information, avoid sending whole thing over the wire
    out = []
    copylistdict(tree, out, 'titel', 'afbeelding', 'index')
    return json.dumps(out)

@api.route("/get_random_painting")
def get_random_painting():
    tree = get_tree()
    i = random.randint(0, len(tree)-1)
    # Remove features as they are not json serializable
    # Add index for easy retrieval later
    out = dict(((k,v) for (k,v) in tree[i].items() if k != 'features'),
                      index=i)
    for k,v in compare_by().items():
        out.update({k:v})
    return json.dumps(out)

# @api.route("/schilderijen/<int:n>.jpg")
# def get_painting_img(n):
#     path = os.path.join(os.getcwd(), 'data', 'schilderijen', str(n)+'.jpg')
#     return send_file(path)

@api.route("/get_similar_painting", methods=["POST"])
def get_similar_painting():
    # Return random painting every once in a while for spread
    js = request.get_json()
    t = get_tree()
    feature = js['feature']
    # Get index that we added at get_random_painting()
    mainimgindex = js['index']
    # Calculate distance to all other paintings
    distlist = [None] * len(t)
    feat1 = t[mainimgindex]['features'][feature]
    t1 = c()
    for i, img in enumerate(t):
        feat2 = img['features'][feature]
        d = dist(feature, feat1, feat2)
        distlist[i] = d
        # Distance to itself is 0 of course
        if mainimgindex==i: distlist[i] = float('inf')
    t2 = c()
    # Return best or random for spread
    mindist = min(distlist)
    similarimgindex = distlist.index(mindist)
    selectrandom = True if random.random() < .2 else False
    if selectrandom:
        logger.info("get_similar_painting is getting random painting for spread")
        similarimgindex = random.randint(0,len(distlist)-1)
    logger.info("Calculated distance from painting #{index} for feature {feature} to all other paintings in {time:.4f}s, chose #{similarimgindex}"
    .format(index=mainimgindex, time=t2-t1, feature=feature, similarimgindex=similarimgindex))
    # Add distance to json obj for later analysis
    return json.dumps(dict(((k,v) for (k,v) in t[similarimgindex].items() if k != 'features'),
                      dist=mindist, feature=feature, index=similarimgindex, random=selectrandom))

@api.route("/get_similar_paintings/<int:n>", methods=["POST"])
def get_similar_paintings(n):
    # Return random painting every once in a while for spread
    js = request.get_json()
    t = get_tree()
    # Get index that we added at get_random_painting()
    mainimgindex = js['index']
    # Calculate distance to all other paintings
    distlist = [None] * len(t)
    t1 = c()
    for i, img in enumerate(t):
        distlist[i] = utils_dist(js['index'], i)
        # Distance to itself is 0 of course
        if mainimgindex==i: distlist[i] = float('inf')
    t2 = c()
    # Return best n
    similarimgindexes = sorted(enumerate(distlist), key=lambda x: x[1])[:n]
    time = t2-t1
    logger.info("Calculated distance from painting #{} to all other paintings in {:.4f}s, chose #{}"
    .format(mainimgindex, time, similarimgindexes))
    # Add distance to json obj for later analysis
    return json.dumps(list(dict((k,v) for (k,v) in t[similarimgindex].items()
                                  if k != 'features')
                      for similarimgindex, _ in similarimgindexes))

@api.route("/vote", methods=["POST"])
def vote():
    j = request.get_json()
    # Process vote and send to db
    compare_by = j['mainimg']['compare_by']
    mainimgindex = j['mainimg']['index']
    similarimgindex = j['similarimg']['index']
    votevalue = j['votevalue']
    sessionhash = j['sessionhash']
    timestamp = datetime.datetime.now()
    logger.info("\n\nAt {:%Y-%m-%d %H:%M} images #{} and #{} were compared by {} and given value {} during session {}\n\n"
    .format(timestamp, mainimgindex, similarimgindex, compare_by, votevalue, sessionhash))
    db.insert_one(dict(j, timestamp=timestamp.isoformat()))
    return json.dumps({'msg': "Vote received!"})
