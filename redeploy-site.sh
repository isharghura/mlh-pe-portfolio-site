#!/bin/bash
set -e

PROJECT_DIR="/root/mlh-pe-portfolio-site"

echo "killing all tmux sessions"
tmux kill-server || true

echo "changing directory to project folder"
cd "${PROJECT_DIR}"

echo "fetching latest changes from GitHub"
git fetch && git reset origin/main --hard

echo "activating virtual environment"
source python3-virtualenv/bin/activate

echo "installing requirements"
pip install -r requirements.txt

echo "start tmux session"

tmux new-session -d -s flask-site "bash -c \"
cd '${PROJECT_DIR}' && \
source python3-virtualenv/bin/activate && \
export FLASK_APP=app.py && \
export FLASK_ENV=production && \
while true; do flask run --host=0.0.0.0 --port=5000; sleep 1; done
\""

echo "tmux session created. Attach with: tmux attach -t flask-site"
echo "Deployment complete"
