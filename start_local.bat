@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

REM ============================================
REM Smart Food Tracker - Local Startup Script v2.0
REM Enhanced with better error handling and recovery
REM ============================================

echo.
echo ============================================
echo    Smart Food Tracker - Local Launcher
echo ============================================
echo.

REM Color definitions (using ANSI escape codes)
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "CYAN=[96m"
set "RESET=[0m"
set "BOLD=[1m"

REM ============================================
REM Step 1: Check Python Environment
REM ============================================
echo %BLUE%[1/7] Checking Python environment...%RESET%

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%ERROR: Python not found%RESET%
    echo.
    echo Please install Python 3.8+ from:
    echo   https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYTHON_VERSION=%%v
echo %GREEN%  OK: Python %PYTHON_VERSION%%RESET%
echo.

REM ============================================
REM Step 2: Check Node.js Environment
REM ============================================
echo %BLUE%[2/7] Checking Node.js environment...%RESET%

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%ERROR: Node.js not found%RESET%
    echo.
    echo Please install Node.js 16+ from:
    echo   https://nodejs.org/
    pause
    exit /b 1
)

for /f "tokens=1" %%v in ('node --version 2^>^&1') do set NODE_VERSION=%%v
echo %GREEN%  OK: Node.js %NODE_VERSION%%RESET%
echo.

REM ============================================
REM Step 3: Install Backend Dependencies
REM ============================================
echo %BLUE%[3/7] Checking backend dependencies...%RESET%
echo.

cd /d "%~dp0backend"

REM Check if .env exists, create if not
if not exist ".env" (
    echo %YELLOW%Creating .env configuration file...%RESET%
    (
        echo # GLM API Key (Required)
        echo GLM_API_KEY=your_glm_api_key_here
        echo.
        echo # Environment Mode
        echo ENV_MODE=production
    ) > .env
    echo %YELLOW%  Please edit backend\.env and add your GLM_API_KEY%RESET%
    echo.
)

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo %RED%ERROR: requirements.txt not found in backend folder%RESET%
    pause
    exit /b 1
)

REM Try to verify dependencies are installed
echo Verifying installed packages...
python -c "import fastapi; import uvicorn; import sqlalchemy" >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%Dependencies missing or incomplete, installing...%RESET%
    echo.

    REM Upgrade pip first
    echo Upgrading pip...
    python -m pip install --upgrade pip >nul 2>&1

    REM Install dependencies
    echo Installing from requirements.txt...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo %YELLOW%Retrying with alternative method...%RESET%
        python -m pip install --no-cache-dir -r requirements.txt
    )

    if %errorlevel% neq 0 (
        echo %RED%ERROR: Failed to install dependencies%RESET%
        echo.
        echo %YELLOW%Manual installation steps:%RESET%
        echo   1. Open Command Prompt as Administrator
        echo   2. Run: cd backend
        echo   3. Run: python -m pip install -r requirements.txt
        echo.
        echo If you encounter encoding errors, try:
        echo   chcp 65001
        echo   python -m pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
) else (
    echo %GREEN%  OK: Dependencies already installed%RESET%
)
echo.

REM ============================================
REM Step 4: Initialize Database
REM ============================================
echo %BLUE%[4/7] Initializing database...%RESET%
echo.

REM Check if database needs initialization
if not exist "smart_food.db" (
    echo Database not found, creating tables...
    python create_tables.py
    if %errorlevel% neq 0 (
        echo %YELLOW%WARNING: Table creation had issues, continuing...%RESET%
    )

    echo Importing food data (105 foods)...
    python init_extended_database.py
    if %errorlevel% neq 0 (
        echo %YELLOW%WARNING: Data import had issues. You can import later manually.%RESET%
        echo   Run: python init_extended_database.py
    )
) else (
    echo %GREEN%  OK: Database already exists%RESET%
    echo %YELLOW%  To re-import data, delete smart_food.db and restart%RESET%
)
echo.

REM ============================================
REM Step 5: Start Backend Service
REM ============================================
echo %BLUE%[5/7] Starting backend service (port 8000)...%RESET%
echo.

REM Check if port 8000 is already in use
netstat -ano | findstr ":8000" | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo %YELLOW%WARNING: Port 8000 is already in use%RESET%
    echo %YELLOW%  Attempting to use existing backend...%RESET%
) else (
    start "SmartFood-Backend" /min cmd /c "title SmartFood-Backend && chcp 65001 >nul && cd /d "%~dp0backend" && echo ============================================ && echo   Backend Service Starting... && echo ============================================ && echo. && echo API: http://localhost:8000 && echo API Docs: http://localhost:8000/docs && echo. && uvicorn app.main:app --host 0.0.0.0 --port 8000 && pause"
    echo %GREEN%  Backend starting in new window%RESET%
)

timeout /t 3 /nobreak >nul

REM ============================================
REM Step 6: Generate IP Configuration
REM ============================================
echo %BLUE%[6/7] Generating IP configuration...%RESET%

python get_local_ip.py >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%  WARNING: IP config generation skipped (will use WebRTC)%RESET%
) else (
    echo %GREEN%  OK: IP configuration generated%RESET%
)
echo.

REM ============================================
REM Step 7: Start Frontend Service
REM ============================================
echo %BLUE%[7/7] Starting frontend service (port 5173)...%RESET%
echo.

cd /d "%~dp0frontend"

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing npm packages...
    echo This may take a few minutes...
    echo.

    call npm install
    if %errorlevel% neq 0 (
        echo.
        echo %RED%ERROR: npm install failed%RESET%
        echo.
        echo %YELLOW%Possible solutions:%RESET%
        echo   1. Check your internet connection
        echo   2. Try using Taobao mirror:
        echo      npm install --registry=https://registry.npmmirror.com
        echo   3. Clear npm cache:
        echo      npm cache clean --force
        echo.
        pause
        exit /b 1
    )
)

REM Check if port 5173 is already in use
netstat -ano | findstr ":5173" | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo %YELLOW%WARNING: Port 5173 is already in use%RESET%
    echo %YELLOW%  Frontend may already be running%RESET%
) else (
    start "SmartFood-Frontend" /min cmd /c "title SmartFood-Frontend && chcp 65001 >nul && cd /d "%~dp0frontend" && echo ============================================ && echo   Frontend Service Starting... && echo ============================================ && echo. && echo Web App: http://localhost:5173 && echo. && npm run dev -- --host 0.0.0.0 && pause"
    echo %GREEN%  Frontend starting in new window%RESET%
)

echo.
echo ============================================
echo    Startup Complete!
echo ============================================
echo.
echo %GREEN%Services Status:%RESET%
echo   Backend:  %GREEN%Running%RESET% on http://localhost:8000
echo   Frontend: %GREEN%Running%RESET% on http://localhost:5173
echo.
echo %GREEN%Access URLs:%RESET%
echo.
echo   Computer Browser:
echo     %CYAN%http://localhost:5173%RESET%
echo.
echo   API Documentation:
echo     %CYAN%http://localhost:8000/docs%RESET%
echo.
echo %YELLOW%Troubleshooting:%RESET%
echo   - If pages don't load, check the backend/frontend windows
echo   - If you see "connection refused", the services may still be starting
echo   - Wait 10-15 seconds for services to fully initialize
echo.
echo %CYAN%For testing guide, see: MOBILE_TEST_PLAN_TEMPLATE.md%RESET%
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul

start http://localhost:5173

echo.
echo Press any key to close this window (services will continue running)...
pause >nul
