#
# File that automates local and remote updating
#

from fabric.api import env, lcd, cd, local, run, prefix, shell_env

def serve():
    with shell_env(FLASK_APP='app', PYTHONPATH='./', FLASK_DEBUG='True'):
        local("flask run")
