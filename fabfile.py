#
# File that automates local and remote updating
#

from fabric.api import env, lcd, cd, local, run, prefix, shell_env

def serve(port=None):
    with shell_env(FLASK_APP='app', PYTHONPATH='./', FLASK_DEBUG='True'):
        if port:
            local("flask run --port "+port)
        else:
            local("flask run")
