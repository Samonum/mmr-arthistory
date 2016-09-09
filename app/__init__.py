from flask import Flask

app = Flask(__name__)

from app.frontend import showoffapp, trainingapp
app.register_blueprint(showoffapp, url_prefix="/showoff")
app.register_blueprint(trainingapp, url_prefix="/")



# register database Blueprint
