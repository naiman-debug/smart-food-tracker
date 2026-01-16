@echo off
setlocal enabledelayedexpansion

REM ============================================
REM Smart Food Tracker - Simple Startup Script
REM Auto-installs frontend dependencies if needed
REM ============================================

chcp 65001 >nul 2>&1

REM Color definitions
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "CYAN=[96m"
set "RESET=[0m"

echo.
echo ============================================
echo   Smart Food Tracker - Quick Start
REM ============================================
echo.

REM ============================================
REM Step 1: Check Environment
REM ============================================
echo %BLUE%[1/4] Checking environment...%RESET%

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%ERROR: Python not found%RESET%
    echo.
    echo Please install Python 3.8+ from:
    echo   https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo %GREEN%  OK: Python is installed%RESET%

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%ERROR: Node.js not found%RESET%
    echo.
    echo Please install Node.js from:
    echo   https://nodejs.org/
    echo.
    pause
    exit /b 1
)
echo %GREEN%  OK: Node.js is installed%RESET%

REM Check backend directory
if not exist "%~dp0backend" (
    echo %RED%ERROR: Backend directory not found%RESET%
    pause
    exit /b 1
)
echo %GREEN%  OK: Backend directory exists%RESET%

REM Check frontend directory
if not exist "%~dp0frontend" (
    echo %RED%ERROR: Frontend directory not found%RESET%
    pause
    exit /b 1
)
echo %GREEN%  OK: Frontend directory exists%RESET%

echo.

REM ============================================
REM Step 2: Check Port Availability
REM ============================================
echo %BLUE%[2/4] Checking port availability...%RESET%

REM Check port 8000
netstat -ano | findstr ":8000" | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo %YELLOW%WARNING: Port 8000 is already in use%RESET%
    echo %YELLOW%  Backend service may fail to start%RESET%
) else (
    echo %GREEN%  OK: Port 8000 is available%RESET%
)

REM Check port 5173
netstat -ano | findstr ":5173" | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo %YELLOW%WARNING: Port 5173 is already in use%RESET%
    echo %YELLOW%  Frontend service may fail to start%RESET%
) else (
    echo %GREEN%  OK: Port 5173 is available%RESET%
)

echo.

REM ============================================
REM Step 3: Get Local IP Address
REM ============================================
echo %BLUE%[3/4] Getting local IP address...%RESET%

set "LOCAL_IP=127.0.0.1"
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        set "LOCAL_IP=%%b"
    )
)
echo %GREEN%  OK: Local IP is %LOCAL_IP%%RESET%

echo.

REM ============================================
REM Step 4: Start Services
REM ============================================
echo %BLUE%[4/4] Starting services...%RESET%
echo.

REM Start backend service
echo Starting backend service on port 8000...
cd /d "%~dp0backend"

REM Check if database exists and create tables if needed
if not exist "smart_food.db" (
    echo %YELLOW%Database not found, creating tables...%RESET%
    python create_tables.py
    if %errorlevel% neq 0 (
        echo %YELLOW%WARNING: Table creation had issues, trying to continue...%RESET%
    )
    echo %YELLOW%Please run init_extended_database.py to import food data%RESET%
    echo.
)

REM Check if .env exists
if not exist ".env" (
    echo %YELLOW%WARNING: .env file not found%RESET%
    echo %YELLOW%  Creating default .env...%RESET%
    (
        echo # GLM API Key (Required)
        echo GLM_API_KEY=your_glm_api_key_here
        echo.
        echo # Environment Mode
        echo ENV_MODE=production
    ) > .env
    echo %YELLOW%  Please edit .env and add your GLM_API_KEY%RESET%
    echo.
)

start "SmartFood-Backend" /min cmd /c "title SmartFood-Backend && chcp 65001 >nul && cd /d "%~dp0backend" && echo ============================================ && echo   Backend Service Starting... && echo ============================================ && echo. && echo API: http://localhost:8000 && echo API Docs: http://localhost:8000/docs && echo. && uvicorn app.main:app --host 0.0.0.0 --port 8000 && pause"

timeout /t 3 /nobreak >nul

echo %GREEN%  Backend service started in new window%RESET%

REM Generate IP config file
echo Generating IP configuration for mobile access...
cd /d "%~dp0backend"
python get_local_ip.py
if %errorlevel% neq 0 (
    echo %YELLOW%WARNING: IP config generation failed, will use WebRTC fallback%RESET%
)

REM Start frontend service
echo Starting frontend service on port 5173...
cd /d "%~dp0frontend"

REM Check if node_modules exists, install if needed
if not exist "node_modules" (
    echo %YELLOW%Frontend dependencies not found, installing...%RESET%
    echo.
    echo This may take a few minutes, please wait...
    echo.

    REM Try standard npm install
    call npm install
    if %errorlevel% neq 0 (
        echo.
        echo %RED%ERROR: npm install failed%RESET%
        echo.
        echo %YELLOW%Possible solutions:%RESET%
        echo   1. Check your internet connection
        echo   2. Try using Taobao mirror:
        echo      npm install --registry=https://registry.npmmirror.com
        echo   3. Or manually install:
        echo      cd frontend
        echo      npm install
        echo.
        pause
        exit /b 1
    )

    echo.
    echo %GREEN%OK: Frontend dependencies installed successfully%RESET%
    echo.
) else (
    echo %GREEN%OK: Frontend dependencies already installed%RESET%
    echo.
)

start "SmartFood-Frontend" /min cmd /c "title SmartFood-Frontend && chcp 65001 >nul && cd /d "%~dp0frontend" && echo ============================================ && echo   Frontend Service Starting... && echo ============================================ && echo. && echo Web App: http://localhost:5173 && echo Mobile:  http://%LOCAL_IP%:5173 && echo. && npm run dev -- --host 0.0.0.0 && pause"

timeout /t 2 /nobreak >nul

echo %GREEN%  Frontend service started in new window%RESET%

echo.
echo ============================================
echo   All Services Started Successfully!
echo ============================================
echo.
echo %GREEN%Access URLs:%RESET%
echo.
echo   Computer Browser:
echo     %CYAN%http://localhost:5173%RESET%
echo.
echo   Mobile Browser (same WiFi):
echo     %CYAN%http://%LOCAL_IP%:5173%RESET%
echo.
echo   API Documentation:
echo     %CYAN%http://localhost:8000/docs%RESET%
echo.
echo %YELLOW%Notes:%RESET%
echo   - Two command windows have opened
echo   - Don't close them while using the app
echo   - To stop: Close the windows or press Ctrl+C
echo.
echo %CYAN%For help, see: MANUAL_INSTALL_GUIDE.md%RESET%
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul

start http://localhost:5173

echo.
pause
