@echo off
echo ==========================================
echo    ECOSENSE — STARTING PROJECT
echo ==========================================

:: Start Backend in a new window
echo [1/2] Launching Backend (FastAPI)...
start cmd /k "python -m uvicorn backend.main:app --reload --port 8000"

:: Wait a bit for backend to initialize
timeout /t 3 /nobreak > nul

:: Start Frontend in a new window
echo [2/2] Launching Frontend (React/Vite)...
cd frontend
start cmd /k "npm run dev"

echo ==========================================
echo    ECOSENSE IS NOW RUNNING!
echo    Frontend: http://localhost:5173
echo    Backend: http://localhost:8000
echo ==========================================
pause
