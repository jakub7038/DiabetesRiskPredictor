@echo off

cd backend
start "" venv\Scripts\python.exe app.py

cd ..\frontend
npm run dev