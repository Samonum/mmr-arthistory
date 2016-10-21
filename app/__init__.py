from flask import Flask

app = Flask(__name__)

from app.frontend import showoffapp, trainingapp, api
app.register_blueprint(showoffapp, url_prefix="/showoff")
app.register_blueprint(trainingapp, url_prefix="/")
app.register_blueprint(api, url_prefix="/api")



# register database Blueprint
