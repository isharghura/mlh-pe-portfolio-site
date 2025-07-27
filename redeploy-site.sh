#!/bin/bash
set -e

PROJECT_DIR="/root/mlh-pe-portfolio-site"

echo "Changing directory to project folder"
cd "${PROJECT_DIR}"

echo "Fetching latest changes from GitHub"
git fetch && git reset origin/main --hard

echo "Spinning down containers to prevent memory issues"
docker compose -f docker-compose.prod.yml down

echo "Building and starting containers"
docker compose -f docker-compose.prod.yml up -d --build

echo "Deployment complete"