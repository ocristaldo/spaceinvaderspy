#!/usr/bin/env zsh
#
# spaceinvaders.sh - virtualenv helper + launcher
# ------------------------------------------------
# Usage:
#   ./spaceinvaders.sh              # ensure env ready and launch the game
#   ./spaceinvaders.sh test         # run pytest (after ensuring env)
#   ./spaceinvaders.sh shell        # open an interactive shell with the env active
#   ./spaceinvaders.sh --force-reinstall   # force reinstall of requirements
#   ./spaceinvaders.sh --no-install        # skip dependency installation
#
# Behavior highlights:
#   * Creates .venv automatically if no virtualenv is active.
#   * Never creates or reinstalls requirements if you're already inside a venv.
#   * Remembers the last installed requirements hash to avoid redundant pip installs.
#   * Respects SPACEINVADERS_WINDOW_SCALE when launching the game.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname -- "$0")" && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"
REQ_FILE="$PROJECT_ROOT/requirements.txt"
REQ_HASH_FILE="$VENV_DIR/.requirements.sha256"
DEFAULT_PY_CMDS=("python3" "python")
CUSTOM_PYTHON="${SPACEINVADERS_PYTHON:-}"

if [[ -n "${SPACEINVADERS_PYTEST_ARGS:-}" ]]; then
  PYTEST_ARGS=("${(@s/ /)SPACEINVADERS_PYTEST_ARGS}")
else
  PYTEST_ARGS=("-q")
fi

ACTION="play"
INSTALL=true
FORCE_INSTALL=false

print_step() {
  echo "[spaceinvaders] $1"
}

find_command_in_path() {
  for cmd in "$@"; do
    local resolved
    resolved="$(command -v "$cmd" 2>/dev/null || true)"
    if [[ -n "$resolved" ]]; then
      echo "$resolved"
      return 0
    fi
  done
  return 1
}

resolve_venv_exec() {
  local env_dir="$1"
  shift
  for rel in "$@"; do
    local candidate="$env_dir/bin/$rel"
    if [[ -x "$candidate" ]]; then
      echo "$candidate"
      return 0
    fi
  done
  return 1
}

usage() {
  cat <<'EOF'
Usage: ./spaceinvaders.sh [action] [options]

Actions (pick one):
  play            Ensure env + requirements (if needed) and launch the game (default)
  test            Run pytest -q
  shell           Open an interactive shell with the managed virtualenv activated

Options:
  --no-install        Do not install/update requirements even if env is new
  --force-reinstall   Force reinstall of requirements (ignores hash cache)
  -h, --help          Show this help

Examples:
  ./spaceinvaders.sh
  ./spaceinvaders.sh test
  ./spaceinvaders.sh shell
EOF
}

for arg in "$@"; do
  case "$arg" in
    play|run|--play)
      ACTION="play"
      ACTION_SELECTED=true
      ;;
    test|--test)
      ACTION="test"
      ACTION_SELECTED=true
      ;;
    shell|--shell)
      ACTION="shell"
      ACTION_SELECTED=true
      ;;
    --no-install)
      INSTALL=false
      ;;
    --force-reinstall|--reinstall)
      FORCE_INSTALL=true
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $arg" >&2
      usage
      exit 2
      ;;
  esac
done

# Environment / command variables
ACTIVE_ENV="${VIRTUAL_ENV:-}"
USING_EXTERNAL_ENV=false
ACTIVE_PYTHON=""
SYSTEM_PYTHON=""
NEW_ENV_CREATED=false

detect_system_python() {
  if [[ -n "$CUSTOM_PYTHON" ]]; then
    if [[ -x "$CUSTOM_PYTHON" ]]; then
      SYSTEM_PYTHON="$CUSTOM_PYTHON"
      return
    elif command -v "$CUSTOM_PYTHON" >/dev/null 2>&1; then
      SYSTEM_PYTHON="$(command -v "$CUSTOM_PYTHON")"
      return
    else
      echo "[spaceinvaders] error: SPACEINVADERS_PYTHON '$CUSTOM_PYTHON' not found." >&2
      exit 1
    fi
  fi
  for cmd in "${DEFAULT_PY_CMDS[@]}"; do
    if command -v "$cmd" >/dev/null 2>&1; then
      SYSTEM_PYTHON="$cmd"
      return
    fi
  done

  echo "[spaceinvaders] error: Python 3 is required but was not found on PATH." >&2
  exit 1
}

setup_environment() {
  if [[ -n "$ACTIVE_ENV" ]]; then
    if [[ "$ACTIVE_ENV" == "$VENV_DIR" ]]; then
      print_step "Managed virtualenv already active; reusing it."
      ACTIVE_PYTHON="$(resolve_venv_exec "$ACTIVE_ENV" python3 python)"
      if [[ -z "$ACTIVE_PYTHON" ]]; then
        echo "[spaceinvaders] error: could not find python executable inside $ACTIVE_ENV" >&2
        exit 1
      fi
      USING_EXTERNAL_ENV=false
      return
    fi
    USING_EXTERNAL_ENV=true
    ACTIVE_PYTHON="$(resolve_venv_exec "$ACTIVE_ENV" python3 python)"
    if [[ -z "$ACTIVE_PYTHON" ]]; then
      ACTIVE_PYTHON="$(find_command_in_path "${DEFAULT_PY_CMDS[@]}")"
    fi
    if [[ -z "$ACTIVE_PYTHON" ]]; then
      echo "[spaceinvaders] error: could not find python interpreter in active virtualenv." >&2
      exit 1
    fi
    print_step "Detected active virtualenv ($ACTIVE_ENV); skipping creation and install."
    return
  fi

  detect_system_python

  if [[ ! -d "$VENV_DIR" ]]; then
    print_step "Creating virtual environment at $VENV_DIR"
    "$SYSTEM_PYTHON" -m venv "$VENV_DIR"
    NEW_ENV_CREATED=true
  fi

  ACTIVE_ENV="$VENV_DIR"
  ACTIVE_PYTHON="$(resolve_venv_exec "$ACTIVE_ENV" python3 python)"
  if [[ -z "$ACTIVE_PYTHON" ]]; then
    echo "[spaceinvaders] error: could not find python executable inside $ACTIVE_ENV" >&2
    exit 1
  fi

  if [[ ! -x "$ACTIVE_PYTHON" ]]; then
    echo "[spaceinvaders] error: expected python executable at $ACTIVE_PYTHON" >&2
    exit 1
  fi

  if [[ "$NEW_ENV_CREATED" == true ]]; then
    print_step "Upgrading pip/setuptools/wheel (first-time setup)"
    "$ACTIVE_PYTHON" -m pip install --upgrade pip setuptools wheel
  fi
}

compute_requirements_hash() {
  if [[ ! -f "$REQ_FILE" ]]; then
    echo ""
    return
  fi
  REQ_PATH="$REQ_FILE" "$ACTIVE_PYTHON" <<'PY'
import hashlib, os, pathlib
path = pathlib.Path(os.environ["REQ_PATH"])
data = path.read_bytes() if path.exists() else b""
print(hashlib.sha256(data).hexdigest())
PY
}

install_requirements_if_needed() {
  if [[ "$INSTALL" == false ]]; then
    print_step "Skipping dependency installation (--no-install)"
    return
  fi

  if [[ "$USING_EXTERNAL_ENV" == true ]]; then
    print_step "Virtualenv already active; assuming requirements satisfied."
    return
  fi

  if [[ ! -f "$REQ_FILE" ]]; then
    print_step "requirements.txt not found; nothing to install."
    return
  fi

  local desired_hash current_hash
  desired_hash="$(compute_requirements_hash)"
  current_hash=""
  if [[ -f "$REQ_HASH_FILE" ]]; then
    current_hash="$(< "$REQ_HASH_FILE")"
  fi

  if [[ "$FORCE_INSTALL" == true || "$desired_hash" != "$current_hash" ]]; then
    print_step "Installing dependencies from requirements.txt"
    "$ACTIVE_PYTHON" -m pip install -r "$REQ_FILE"
    if [[ -n "$desired_hash" ]]; then
      echo "$desired_hash" > "$REQ_HASH_FILE"
    fi
  else
    print_step "Dependencies already up-to-date (hash unchanged)."
  fi
}

launch_game() {
  print_step "Launching Space Invaders"
  cd "$PROJECT_ROOT"
  exec "$ACTIVE_PYTHON" -m src.main
}

run_tests() {
  local args="${PYTEST_ARGS[*]}"
  print_step "Running pytest ${args}"
  cd "$PROJECT_ROOT"
  exec "$ACTIVE_PYTHON" -m pytest "${PYTEST_ARGS[@]}"
}

open_shell() {
  local shell_bin="${SHELL:-/bin/zsh}"
  cd "$PROJECT_ROOT"
  if [[ "$USING_EXTERNAL_ENV" == true ]]; then
    print_step "Using already active virtualenv ($ACTIVE_ENV). Opening shell."
    exec "$shell_bin" -i
  fi

  print_step "Activating managed virtualenv at $ACTIVE_ENV"
  export VIRTUAL_ENV="$ACTIVE_ENV"
  export PATH="$ACTIVE_ENV/bin:$PATH"
  exec "$shell_bin" -i
}

main() {
  setup_environment
  install_requirements_if_needed

  case "$ACTION" in
    play)
      launch_game
      ;;
    test)
      run_tests
      ;;
    shell)
      open_shell
      ;;
    *)
      echo "[spaceinvaders] Unknown action: $ACTION" >&2
      exit 2
      ;;
  esac
}

main
