$ErrorActionPreference = "Stop"

Write-Host "Setting up local environment for prototype-open-museum..."

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python is required but was not found in PATH."
}

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe -m ipykernel install --user --name prototype-open-museum --display-name "Python (.venv) prototype-open-museum"

if (-not (Get-Command quarto -ErrorAction SilentlyContinue)) {
    Write-Host "Quarto CLI not found. Attempting installation..."

    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install --id Quarto.Quarto -e --accept-source-agreements --accept-package-agreements
    }
    elseif (Get-Command choco -ErrorAction SilentlyContinue) {
        choco install quarto -y
    }
    else {
        Write-Warning "No supported package manager found for automatic Quarto install (winget/choco)."
        Write-Warning "Install Quarto from https://quarto.org/docs/get-started/ and re-run this script."
    }

    if (-not (Get-Command quarto -ErrorAction SilentlyContinue)) {
        Write-Warning "Quarto still not available in PATH. You may need to restart your terminal after installation."
    } else {
        quarto --version
    }
} else {
    quarto --version
}

Write-Host "Setup complete."
Write-Host "Activate your environment with: .\.venv\Scripts\Activate.ps1"
