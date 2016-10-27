from flask import render_template
from . import showoffapp, trainingapp, api
from ..utils import get_tree, dist
import random
from flask import json, send_file, request
import os
import random
from tinydb import TinyDB, where
import datetime
import logging

logging.basicConfig(filename='log.txt', level=logging.DEBUG)
logger = logging.getLogger(__name__)

db = TinyDB(os.path.join(os.getcwd(), 'results.json'))

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
        return {'compare_by': 'color', 'msg': "Compare the two paintings based on color."}
    else:
        return {'compare_by': 'texture', 'msg': "Compare the two paintings based on texture."}

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
    # prune for important information, avoid sending whole thing over the wire
    out = []
    copylistdict(tree, out, 'titel', 'afbeelding')
    return json.dumps(out)

@api.route("/get_random_painting")
def get_random_painting():
    tree = get_tree()
    i = random.randint(0, len(tree)-1)
    # Remove features as they are not json serializable
    # Add index for easy retrieval later
    return json.dumps(dict(((k,v) for (k,v) in tree[i].items() if k != 'features'),
                    **compare_by(), index=i))

@api.route("/schilderijen/<int:n>.jpg")
def get_painting_img(n):
    path = os.path.join(os.getcwd(), 'data', 'schilderijen', str(n)+'.jpg')
    return send_file(path)

@api.route("/get_similar_painting", methods=["POST"])
def get_similar_painting():
    j = request.get_json()
    # Get index that we added at get_random_painting()
    j['index']
    # TODO: Calculate distance to all other paintings
    j['compare_by']
    # TODO: Sort and return best n

    # TODO: pick one feature from feature dict

    # TODO: Also return random painting every once in a while for spread

    # TODO: Add distance to json obj for later analysis
    return get_random_painting()

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
    db.insert(dict(j, timestamp=timestamp.isoformat()))
    return json.dumps({'msg': "Vote received!"})
