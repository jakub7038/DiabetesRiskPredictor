#!/bin/bash
set -e

# Backend
cd backend
venv/bin/python app.py &
BACKEND_PID=$!

# Frontend
cd ../frontend
npm run dev

wait $BACKEND_PID