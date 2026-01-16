@echo off
chcp 65001 >nul 2>&1

REM ============================================
REM Smart Food Tracker - Quick Start (Simplified)
REM For users who prefer manual control or troubleshooting
REM ============================================

echo.
echo ============================================
echo    Smart Food Tracker - Quick Start
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)
echo [OK] Python found

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js 16+
    pause
    exit /b 1
)
echo [OK] Node.js found

echo.
echo ============================================
echo    Services Starting...
echo ============================================
echo.

REM Start Backend
echo Starting backend on port 8000...
cd /d "%~dp0backend"

REM Quick dependency check
python -c "import fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing backend dependencies...
    python -m pip install -q fastapi uvicorn sqlalchemy pydantic python-dotenv httpx
)

start "SmartFood-Backend" cmd /k "uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo Backend starting...

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start Frontend
echo Starting frontend on port 5173...
cd /d "%~dp0frontend"

REM Quick dependency check
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install --silent
)

start "SmartFood-Frontend" cmd /k "npm run dev -- --host 0.0.0.0"
echo Frontend starting...

echo.
echo ============================================
echo    Done! Services started in background.
echo ============================================
echo.
echo Access the app at: http://localhost:5173
echo API docs at: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause >nul
