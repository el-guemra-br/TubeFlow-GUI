param(
    [switch]$RunAfterSetup
)

$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$setupScript = Join-Path $projectRoot "scripts\setup.ps1"

if (-not (Test-Path $setupScript)) {
    throw "Cannot find scripts/setup.ps1."
}

& $setupScript -RunAfterSetup:$RunAfterSetup
