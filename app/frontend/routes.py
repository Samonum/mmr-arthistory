from flask import render_template
from . import showoffapp, trainingapp

@showoffapp.route("/")
def index():
    return "Showing off our single-page app"

@trainingapp.route("/")
def train():
    return render_template("train.html")
