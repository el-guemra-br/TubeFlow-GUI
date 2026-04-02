param(
    [switch]$RunAfterSetup
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "[setup] $Message" -ForegroundColor Cyan
}

function Resolve-PythonCommand {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        return "py -3"
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return "python"
    }
    throw "Python 3 was not found. Install Python 3.x and run this script again."
}

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $projectRoot

Write-Step "Starting TubeFlow-GUI setup..."

$pythonCmd = Resolve-PythonCommand
$venvPath = Join-Path $projectRoot ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"
$requirementsFile = Join-Path $projectRoot "requirements.txt"

if (-not (Test-Path $venvPython)) {
    Write-Step "Creating virtual environment at .venv"
    Invoke-Expression "$pythonCmd -m venv .venv"
} else {
    Write-Step "Virtual environment already exists"
}

Write-Step "Upgrading pip in virtual environment"
& $venvPython -m pip install --upgrade pip

if (Test-Path $requirementsFile) {
    Write-Step "Installing dependencies from requirements.txt"
    & $venvPython -m pip install -r $requirementsFile
} else {
    Write-Step "requirements.txt not found, installing yt-dlp directly"
    & $venvPython -m pip install yt-dlp
}

Write-Step "Validating yt-dlp import"
& $venvPython -c "import yt_dlp; print('yt-dlp version:', yt_dlp.version.__version__)"

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host "[setup] WARNING: ffmpeg not found in PATH. MP3 conversion/high-quality merges may fail." -ForegroundColor Yellow
    Write-Host "[setup] Download ffmpeg from https://ffmpeg.org/download.html and add it to PATH." -ForegroundColor Yellow
} else {
    Write-Step "ffmpeg detected in PATH"
}

Write-Host ""
Write-Host "Setup complete." -ForegroundColor Green
Write-Host "To run the app:" -ForegroundColor Green
Write-Host "  .\.venv\Scripts\python.exe .\TubeFlow-GUI.py" -ForegroundColor Green

if ($RunAfterSetup) {
    Write-Step "Launching TubeFlow GUI"
    & $venvPython ".\TubeFlow-GUI.py"
}
