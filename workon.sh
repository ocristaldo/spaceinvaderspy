#!/usr/bin/env zsh
# workon.sh - prepare and enter this project's virtualenv
#
# Usage:
#   ./workon.sh                   # create .venv if missing, install requirements, open an interactive shell
#   ./workon.sh --use-existing    # use existing venv at ./spaceinvaders if present
#   ./workon.sh --no-install      # don't install requirements
#   ./workon.sh --test            # run pytest after installing (installs pytest if missing)
#
# This script is written for zsh on macOS. It will create a venv, activate it, upgrade pip,
# optionally install requirements from requirements.txt, optionally run tests, then open an
# interactive shell with the venv active.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname -- "$0")" && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"
ALT_VENV_DIR="$PROJECT_ROOT/spaceinvaders"
PYTHON_CMD="python3"
REQ_FILE="$PROJECT_ROOT/requirements.txt"

INSTALL=true
RUN_TESTS=false
USE_EXISTING=false

print_info() {
  echo "[workon] $1"
}

for arg in "$@"; do
  case "$arg" in
    --no-install) INSTALL=false ;;
    --test) RUN_TESTS=true ;;
    --use-existing) USE_EXISTING=true ;;
    --help|-h) echo "Usage: $0 [--use-existing] [--no-install] [--test]"; exit 0 ;;
    *) echo "Unknown option: $arg"; echo "Usage: $0 [--use-existing] [--no-install] [--test]"; exit 2 ;;
  esac
done

if ! command -v "$PYTHON_CMD" >/dev/null 2>&1; then
  echo "[workon] error: $PYTHON_CMD not found. Install Python 3 and try again." >&2
  exit 1
fi

if [[ "$USE_EXISTING" == true ]]; then
  if [[ -d "$ALT_VENV_DIR" && -f "$ALT_VENV_DIR/bin/activate" ]]; then
    VENV_DIR="$ALT_VENV_DIR"
    print_info "Using existing venv at $VENV_DIR"
  else
    echo "[workon] --use-existing requested but $ALT_VENV_DIR not found or invalid" >&2
    exit 1
  fi
fi

if [[ ! -d "$VENV_DIR" ]]; then
  print_info "Creating virtual environment at $VENV_DIR"
  "$PYTHON_CMD" -m venv "$VENV_DIR"
  print_info "Virtual environment created"
fi

ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"
if [[ ! -f "$ACTIVATE_SCRIPT" ]]; then
  echo "[workon] activation script not found at $ACTIVATE_SCRIPT" >&2
  exit 1
fi

print_info "Activating virtual environment"
# Source the activate script in this process so child shells inherit the environment.
source "$ACTIVATE_SCRIPT"

print_info "Upgrading pip, setuptools, wheel"
pip install --upgrade pip setuptools wheel

if [[ "$INSTALL" == true ]]; then
  if [[ -f "$REQ_FILE" ]]; then
    print_info "Installing dependencies from requirements.txt"
    pip install -r "$REQ_FILE"
  else
    print_info "No requirements.txt found at $REQ_FILE — skipping pip install"
  fi
else
  print_info "Skipping dependency installation (--no-install)"
fi

if [[ "$RUN_TESTS" == true ]]; then
  if ! command -v pytest >/dev/null 2>&1; then
    print_info "pytest not found in venv — installing pytest"
    pip install pytest
  fi
  print_info "Running tests (pytest -q)"
  # Run tests from project root
  (cd "$PROJECT_ROOT" && pytest -q)
fi

print_info "Environment is ready. Dropping into an interactive shell with the venv active."
cd "$PROJECT_ROOT"
exec "$SHELL" -i
