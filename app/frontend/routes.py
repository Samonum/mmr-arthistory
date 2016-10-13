from flask import render_template
from . import showoffapp, trainingapp, api
from ..utils import get_tree, dist
import random
from flask import json, send_file, request
import os

@showoffapp.route("/")
def index():
    return "Showing off our single-page app"

@trainingapp.route("/")
def train():
    return render_template("train.html")

################################################################################
# API
################################################################################

@api.route("/get_random_painting")
def get_random_painting():
    tree = get_tree()
    i = random.randint(0, len(tree)-1)
    # Add index for easy retrieval later
    return json.dumps(dict(tree[i], index=i))

@api.route("/schilderijen/<int:n>.jpg")
def get_painting_img(n):
    path = os.path.join(os.getcwd(), 'data', 'schilderijen', str(n)+'.jpg')
    return send_file(path)

@api.route("/get_similar_painting", methods=["POST"])
def get_similar_painting():
    # Get index that we added at get_random_painting()
    j = request.get_json()
    j['index']
    # Calculate distance to all other paintings
    # Sort and return best n
    return get_random_painting()
