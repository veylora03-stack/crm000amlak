Set-Location "$PSScriptRoot\backend"
Write-Host "🚀 Starting Backend on http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "📚 API Docs: http://127.0.0.1:8000/api/docs/" -ForegroundColor Yellow
Write-Host "👤 Admin login: admin / admin123456" -ForegroundColor Cyan
Write-Host ""
& ".venv\Scripts\python.exe" manage.py runserver 0.0.0.0:8000
