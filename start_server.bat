@echo off
echo ========================================================
echo   Starting PrioritiQ Enterprise Decision Engine
echo ========================================================
echo.

echo [1/3] Verifying and seeding database if required...
python -m backend.database.seed

echo.
echo [2/3] Launching FastAPI Backend on http://127.0.0.1:8000 ...
start "PrioritiQ Backend" cmd /k "python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"

echo.
echo [3/3] Launching Vite Frontend on http://localhost:5173 ...
cd frontend
start "PrioritiQ Frontend" cmd /k "npm run dev"

echo.
echo ========================================================
echo   PrioritiQ is launching!
echo   - Backend API Docs: http://127.0.0.1:8000/docs
echo   - Web Console:      http://localhost:5173
echo ========================================================
