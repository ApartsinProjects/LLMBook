# LLMBook publishing pipeline - PowerShell wrapper
#
# Usage:
#   .\publish.ps1                 # default: build + validate
#   .\publish.ps1 -Quick          # fast iteration mode
#   .\publish.ps1 -ValidateOnly   # skip rebuild
#   .\publish.ps1 -Clean          # wipe output then build
#   .\publish.ps1 -RegenSpine     # re-walk source tree first
#   .\publish.ps1 -NoEpubcheck    # skip Java epubcheck

[CmdletBinding()]
param(
    [switch]$Quick,
    [switch]$ValidateOnly,
    [switch]$Clean,
    [switch]$RegenSpine,
    [switch]$NoEpubcheck,
    [string]$Python = "C:\Python314\python.exe"
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PublishPy = Join-Path $ScriptDir "publish.py"

if (-not (Test-Path $Python)) {
    Write-Host "Python not found at $Python" -ForegroundColor Red
    Write-Host "Override with -Python <path>" -ForegroundColor Yellow
    exit 3
}

if (-not (Test-Path $PublishPy)) {
    Write-Host "Cannot find publish.py at $PublishPy" -ForegroundColor Red
    exit 3
}

$args = @()
if ($Quick)         { $args += "--quick" }
if ($ValidateOnly)  { $args += "--validate-only" }
if ($Clean)         { $args += "--clean" }
if ($RegenSpine)    { $args += "--regen-spine" }
if ($NoEpubcheck)   { $args += "--no-epubcheck" }

& $Python $PublishPy @args
exit $LASTEXITCODE
