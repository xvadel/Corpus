# =============================================================================
# Corpus - Windows Setup & Virtual Environment Initializer
# =============================================================================
# This script automates creating, activating, and installing dependencies
# into an isolated local Python virtual environment (venv).
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File infrastructure/setup/setup_venv.ps1
# =============================================================================

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Corpus - Local Development Environment Initializer" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Ensure script runs from project root (2 folders up from this script's directory)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir "../..")
Set-Location $ProjectRoot
Write-Host "Project root located at: $ProjectRoot" -ForegroundColor Gray

# 1. Check Python Version
Write-Host "`n[1/4] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Error "Python is not installed or not in your PATH. Please install Python 3.10+."
    Exit 1
}

# 2. Create Virtual Environment
$VenvPath = Join-Path $ProjectRoot "venv"
Write-Host "`n[2/4] Initializing isolated virtual environment..." -ForegroundColor Yellow
if (Test-Path $VenvPath) {
    Write-Host "Virtual environment folder already exists at: $VenvPath" -ForegroundColor Gray
} else {
    Write-Host "Creating venv..." -ForegroundColor Gray
    python -m venv venv
    Write-Host "Virtual environment successfully created." -ForegroundColor Green
}

# 3. Upgrade pip & Install Requirements in the Virtual Environment
Write-Host "`n[3/4] Installing backend dependencies from requirements.txt..." -ForegroundColor Yellow
$PipExe = Join-Path $VenvPath "Scripts\pip.exe"
if (-not (Test-Path $PipExe)) {
    Write-Error "Failed to locate pip.exe inside the virtual environment ($PipExe)."
    Exit 1
}

Write-Host "Upgrading pip..." -ForegroundColor Gray
Start-Process -FilePath $PipExe -ArgumentList "install", "--upgrade", "pip" -NoNewWindow -Wait

Write-Host "Installing requirements..." -ForegroundColor Gray
$ReqPath = Join-Path $ProjectRoot "requirements.txt"
Start-Process -FilePath $PipExe -ArgumentList "install", "-r", $ReqPath -NoNewWindow -Wait
Write-Host "Backend dependencies successfully installed." -ForegroundColor Green

# 4. Success Instructions
Write-Host "`n[4/4] Setup completed successfully!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "HOW TO ACTIVATE AND USE:" -ForegroundColor Cyan
Write-Host "1. Activate in PowerShell:" -ForegroundColor Yellow
Write-Host "   .\\venv\\Scripts\\Activate.ps1" -ForegroundColor Gray
Write-Host "2. Run development backend:" -ForegroundColor Yellow
Write-Host "   uvicorn backend.main:app --reload" -ForegroundColor Gray
Write-Host "3. To select this environment in VS Code / Cursor:" -ForegroundColor Yellow
Write-Host "   - Press 'Ctrl + Shift + P'" -ForegroundColor Gray
Write-Host "   - Type 'Python: Select Interpreter'" -ForegroundColor Gray
Write-Host "   - Click 'Enter interpreter path...' and select:" -ForegroundColor Gray
Write-Host "     $ProjectRoot\\venv\\Scripts\\python.exe" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Cyan
