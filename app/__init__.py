import sys
version = sys.version_info.major

# Avoid importing files incompatible with python 2 when just using python 2 to
# calculate features with opencv. (routes.py is incompatible)
# if version == 3:
from flask import Flask, send_file, json, render_template

app = Flask(__name__)

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

# Log route for debugging
@app.route('/log')
def sendlog():
    import os
    logpath = os.path.join(os.getcwd(), 'log.txt')
    return send_file(logpath)

@app.route('/results')
def sendresults():
    from .frontend.routes import db
    out = [item for item in db.find()]
    for item in out:
        item['_id'] = str(item['_id'])
    return json.dumps(out)

from app.frontend import showoffapp, trainingapp, api
app.register_blueprint(showoffapp, url_prefix="/show")
app.register_blueprint(trainingapp, url_prefix="/train")
app.register_blueprint(api, url_prefix="/api")
