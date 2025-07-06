#!/bin/bash

echo "Killing all tmux sessions"
tmux kill-server

echo "Changing directory to proj folder"
cd mlh-pe-portfolio-site

echo "fetching latest changes from github"
git fetch && git reset origin/main --hard

echo "activating virtual env"
source python3-virtualenv/bin/activate

echo "installing requirements"
pip install -r requirements.txt

echo "starting tmux session"
tmux new-session -d -s flask-site
cd /root/mlh-pe-portfolio-site
source python3-virtualenv/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=production
flask run --host=0.0.0.0 --port=5000

echo "deployment complete, flask server is running"
