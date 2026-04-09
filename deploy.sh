#!/bin/zsh

set -a && source .env && set +a

rsync -az --exclude 'venv' --exclude '.git' --exclude '__pycache__' . "${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_DIR}"

ssh "${DEPLOY_USER}@${DEPLOY_HOST}" "cd ${DEPLOY_DIR}; docker-compose up -d --build"