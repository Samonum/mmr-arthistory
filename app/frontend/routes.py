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

db = TinyDB(os.path.join(os.getcwd(), 'results.json'))

@showoffapp.route("/")
def index():
    return "Showing off our single-page app"

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

@api.route("/get_random_painting")
def get_random_painting():
    tree = get_tree()
    i = random.randint(0, len(tree)-1)
    # Add index for easy retrieval later
    return json.dumps(dict(**tree[i], **compare_by(), index=i))

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
    return get_random_painting()

@api.route("/vote", methods=["POST"])
def vote():
    j = request.get_json()
    # Process vote and send to db
    compare_by = j['mainimg']['compare_by']
    mainimgindex = j['mainimg']['index']
    similarimgindex = j['similarimg']['index']
    votevalue = j['votevalue']
    timestamp = datetime.datetime.now()
    logging.info("\n\nAt {:%Y-%m-%d %H:%M} images #{} and #{} were compared by {} and given value {}\n\n"
    .format(timestamp, mainimgindex, similarimgindex, compare_by, votevalue))
    db.insert(dict(j, timestamp=timestamp.isoformat()))
    return json.dumps({'msg': "Vote received!"})
