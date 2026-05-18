#!/bin/bash
set -e

echo "Starting fullstack application..."

# Start backend in the background
echo "Starting backend..."
cd /app/backend
python -m gunicorn --bind 0.0.0.0:5000 --timeout 60 app:app &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend..."
cd /app/frontend
npm start &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
