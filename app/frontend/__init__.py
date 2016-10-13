from flask import Blueprint

showoffapp = Blueprint('showoffapp', __name__)
trainingapp = Blueprint('trainingapp', __name__)
api = Blueprint('api', __name__)

from .routes import *
