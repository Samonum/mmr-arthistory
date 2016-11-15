# Code structure
All code is in the `/app` folder.

# Running the webapp
Make virtualenv, install requirements, then tell flask which app to use `export FLASK_APP=app`, then `flask run`, and don't forget to set `export PYTHONPATH=./` as the flask CLI script is not in the same folder.

# Installing on production server
Go to directory of git repo.

On Ubuntu, install all necessary packages first: `sudo apt install circus nginx python-pip chaussette mongodb python-opencv`

Disable mongodb service (we run it ourselves): `systemctl disable mongodb`

(Probably I forgot some dependencies that I had already installed on the dev server)

Then install required python packages: `pip install -r requirements.txt`

Enable swap if numpy does not compile.

Make dirs: `mkdir log && mkdir mongodb`

Upload paintings. Set proper permissions.

Then symlink `circus.service` into `/etc/systemd/system/circus.service` and do `systemctl --system daemon-reload`.
