# Database Setup Script for CRM Amlak
# Run this script to set up PostgreSQL database

Write-Host "=== CRM Amlak Database Setup ===" -ForegroundColor Green
Write-Host ""

# Check if PostgreSQL is running
Write-Host "Checking PostgreSQL service..." -ForegroundColor Yellow

try {
    $pgService = Get-Service -Name "postgresql*" -ErrorAction Stop
    Write-Host "PostgreSQL service found: $($pgService.Name)" -ForegroundColor Green

    if ($pgService.Status -ne "Running") {
        Write-Host "Starting PostgreSQL service..." -ForegroundColor Yellow
        Start-Service -Name $pgService.Name
        Write-Host "PostgreSQL service started." -ForegroundColor Green
    } else {
        Write-Host "PostgreSQL service is already running." -ForegroundColor Green
    }
} catch {
    Write-Host "PostgreSQL service not found. Please install PostgreSQL first." -ForegroundColor Red
    Write-Host "Download from: https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
    exit 1
}

# Create database
Write-Host ""
Write-Host "Creating database..." -ForegroundColor Yellow

$env:PGPASSWORD = "postgres"

# Try to create database
$createDbResult = & psql -U postgres -h localhost -c "CREATE DATABASE crm_amlak ENCODING 'UTF8';" 2>&1

if ($createDbResult -match "already exists") {
    Write-Host "Database 'crm_amlak' already exists." -ForegroundColor Yellow
} elseif ($LASTEXITCODE -eq 0) {
    Write-Host "Database 'crm_amlak' created successfully." -ForegroundColor Green
} else {
    Write-Host "Error creating database: $createDbResult" -ForegroundColor Red
    Write-Host "Please create the database manually:" -ForegroundColor Yellow
    Write-Host "  psql -U postgres -c `"CREATE DATABASE crm_amlak ENCODING 'UTF8';`"" -ForegroundColor Yellow
}

# Run migrations
Write-Host ""
Write-Host "Running migrations..." -ForegroundColor Yellow

Set-Location "backend"
& ".venv/Scripts/python.exe" manage.py migrate

if ($LASTEXITCODE -eq 0) {
    Write-Host "Migrations completed successfully." -ForegroundColor Green
} else {
    Write-Host "Migration failed." -ForegroundColor Red
    exit 1
}

# Seed data
Write-Host ""
Write-Host "Seeding data..." -ForegroundColor Yellow

& ".venv/Scripts/python.exe" manage.py seed_data

if ($LASTEXITCODE -eq 0) {
    Write-Host "Seed data completed successfully." -ForegroundColor Green
} else {
    Write-Host "Seed data failed." -ForegroundColor Red
    exit 1
}

Set-Location ".."

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run the backend server with:" -ForegroundColor Yellow
Write-Host "  cd backend" -ForegroundColor Cyan
Write-Host "  .venv\Scripts\python.exe manage.py runserver" -ForegroundColor Cyan
Write-Host ""
