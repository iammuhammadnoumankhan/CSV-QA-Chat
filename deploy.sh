#!/bin/bash


# Check the status of the repository
echo "Checking Git status..."
git status

# Pull the latest changes from the remote repository
echo "Pulling the latest changes..."
git pull origin main || { echo "Failed to pull changes"; exit 1; }

echo "Successfully pulled the latest changes."

# Restart FastAPI application
echo "Restarting FastAPI application..."

# If you're using uvicorn, you might need to stop it first.
# You can use pkill or kill command if you know the process ID.
pkill -f "python run.py"  # This will kill any running instances of run.py

# Start FastAPI application again using run.py
nohup python3 run.py --host 0.0.0.0 --port 8000 --workers 4 --timeout 600 &

echo "FastAPI application restarted successfully."