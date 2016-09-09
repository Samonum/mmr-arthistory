from flask import Blueprint

showoffapp = Blueprint('showoffapp', __name__)
trainingapp = Blueprint('trainingapp', __name__)

from .routes import *
