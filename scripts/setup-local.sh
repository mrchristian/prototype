#!/usr/bin/env bash
set -euo pipefail

echo "Setting up local environment for prototype-open-museum..."

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required but was not found in PATH." >&2
  exit 1
fi

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python -m ipykernel install --user --name prototype-open-museum --display-name "Python (.venv) prototype-open-museum"

if ! command -v quarto >/dev/null 2>&1; then
  echo "Quarto CLI not found. Attempting installation..."

  if command -v brew >/dev/null 2>&1; then
    brew install --cask quarto
  elif command -v apt-get >/dev/null 2>&1; then
    curl -fsSL -o /tmp/quarto.deb https://github.com/quarto-dev/quarto-cli/releases/latest/download/quarto-linux-amd64.deb
    sudo apt-get update
    sudo apt-get install -y /tmp/quarto.deb
    rm -f /tmp/quarto.deb
  else
    echo "WARNING: No supported package manager found for automatic Quarto install (brew/apt-get)." >&2
    echo "Install Quarto from https://quarto.org/docs/get-started/ and re-run this script." >&2
  fi

  if command -v quarto >/dev/null 2>&1; then
    quarto --version
  else
    echo "WARNING: Quarto still not available in PATH. You may need to restart your terminal after installation." >&2
  fi
else
  quarto --version
fi

echo "Setup complete."
echo "Activate your environment with: source .venv/bin/activate"
