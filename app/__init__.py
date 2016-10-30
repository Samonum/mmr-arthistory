import sys
version = sys.version_info.major

# Avoid importing files incompatible with python 2 when just using python 2 to
# calculate features with opencv. (routes.py is incompatible)
if version == 3:
    from flask import Flask, send_file, json

    app = Flask(__name__)

    # Log route for debugging
    @app.route('/log')
    def sendlog():
        import os
        logpath = os.path.join(os.getcwd(), 'log.txt')
        return send_file(logpath)

    @app.route('/results')
    def sendresults():
        from .frontend.routes import db
        return json.dumps(db.all())

    from app.frontend import showoffapp, trainingapp, api
    app.register_blueprint(showoffapp, url_prefix="/show")
    app.register_blueprint(trainingapp, url_prefix="/")
    app.register_blueprint(api, url_prefix="/api")



    # register database Blueprint
