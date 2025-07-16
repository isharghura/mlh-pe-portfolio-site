#!/bin/bash
set -e

PROJECT_DIR="/root/mlh-pe-portfolio-site"

echo "Changing directory to project folder"
cd "${PROJECT_DIR}"

echo "Fetching latest changes from GitHub"
git fetch && git reset origin/main --hard

echo "Activating virtual environment"
source python3-virtualenv/bin/activate

echo "Installing requirements"
pip install -r requirements.txt

echo "Restarting myportfolio service"
sudo systemctl restart myportfolio

echo "Checking service status"
sudo systemctl status myportfolio --no-pager

echo "Deployment complete"
