@echo off
echo ========================================
echo CRM Amlak - Setup Script
echo ========================================
echo.

echo [1/4] Checking Python...
python --version
if errorlevel 1 (
    echo Python not found. Please install Python 3.11+
    exit /b 1
)

echo [2/4] Checking Node.js...
node --version
if errorlevel 1 (
    echo Node.js not found. Please install Node.js 18+
    exit /b 1
)

echo.
echo [3/4] Setting up Backend...
cd backend

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Installing dependencies...
call .venv\Scripts\activate.bat
pip install -r requirements.txt

if not exist .env (
    echo Creating .env file...
    copy .env.example .env
)

echo Running migrations...
python manage.py migrate

echo Seeding data...
python manage.py seed_data

cd ..

echo.
echo [4/4] Setting up Frontend...
cd frontend

echo Installing dependencies...
call npm install

cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the backend:
echo   cd backend
echo   .venv\Scripts\activate
echo   python manage.py runserver
echo.
echo To start the frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Default credentials:
echo   Username: admin
echo   Password: admin123456
echo.
pause
