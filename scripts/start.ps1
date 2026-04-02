$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "[start] Virtual environment not found. Running setup first..." -ForegroundColor Yellow
    & (Join-Path $projectRoot "setup.ps1")
}

Write-Host "[start] Launching TubeFlow GUI..." -ForegroundColor Cyan
& $venvPython (Join-Path $projectRoot "TubeFlow-GUI.py")
