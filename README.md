# Code structure
All code is in the `/app` folder.

# Running the webapp
Make virtualenv, install requirements, then tell flask which app to use `export FLASK_APP=app`, then `flask run`, and don't forget to set `export PYTHONPATH=./` as the flask CLI script is not in the same folder.

# Installing on production server
On Ubuntu, install all necessary packages first.

Make dirs.

Then symlink `circus.service` into `/etc/systemd/system/circus.service` and do `systemctl --system daemon-reload`.
