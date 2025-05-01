#!/bin/bash

# remove all __pycache__ directories excluding those under .venv, run in background
# sudo find . -name '__pycache__' -exec rm -rf {} \; &

# set default port to 8080 if APP_PORT is not provided
PORT=${APP_PORT:-8080}

# Add current directory to PYTHONPATH
export PYTHONPATH=$(pwd):$PYTHONPATH

# execute the main.py file with the specified port
python3 app/main.py --port "$PORT"

# wait for all background jobs to finish
wait
