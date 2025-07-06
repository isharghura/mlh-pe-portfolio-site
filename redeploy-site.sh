#!/bin/bash

PROJECT_DIR="/root/mlh-pe-portfolio-site"

echo "Killing all tmux sessions"
tmux kill-server

echo "Changing directory to proj folder"
cd "${PROJECT_DIR}"

echo "fetching latest changes from github"
git fetch && git reset origin/main --hard

echo "activating virtual env"
source python3-virtualenv/bin/activate

echo "installing requirements"
pip install -r requirements.txt

echo "starting tmux session"
COMMAND_TO_RUN="
cd '${PROJECT_DIR}' &&
source python3-virtualenv/bin/activate &&
export FLASK_APP=app.py &&
export FLASK_ENV=production &&
exec flask run --host=0.0.0.0 --port=5000
"
              
tmux new-session -d -s flask-site "bash -c \"${COMMAND_TO_RUN}\""

echo "deployment complete, flask server is running"
