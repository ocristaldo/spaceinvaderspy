Quick Start — macOS (zsh)

This project includes `workon.sh`, a small helper script to create and enter a virtual environment, install dependencies, and optionally run tests. Use it as the recommended way to prepare your environment on macOS (zsh). You can also use it as a template for Linux or adapt it for Windows.

1) Make the script executable (one-time)

```bash
chmod +x ./workon.sh
```

2) Prepare the environment and open a shell

```bash
# Create a .venv if missing, install dependencies from requirements.txt and open an interactive shell
./workon.sh

# Skip installing requirements
./workon.sh --no-install

# Run pytest after installing and then open a shell
./workon.sh --test

# Use an existing venv located at ./spaceinvaders
./workon.sh --use-existing
```

What the script does
- Creates `.venv/` using the system `python3` if it doesn't exist.
- Activates the virtualenv in a new interactive shell.
- Upgrades `pip`, `setuptools`, and `wheel`.
- Installs packages from `requirements.txt` (unless `--no-install`).
- Optionally runs `pytest` (when `--test` is passed).

Notes for Linux
- The same script works on most Linux distributions with `zsh` installed. If you use `bash`, either run it with `bash ./workon.sh` or adapt the shebang to `#!/usr/bin/env bash` and change `exec "$SHELL" -i` to start an interactive bash shell if necessary.

Notes for Windows
- For Windows (PowerShell) you'll want a separate `workon.ps1` script. The basic steps are:
  - python -m venv .venv
  - .\.venv\Scripts\Activate.ps1
  - python -m pip install -r requirements.txt
  - (optional) python -m pytest

Security / personal files
- The repo `.gitignore` should exclude local virtualenv directories (e.g., `.venv/`, `spaceinvaders/`), `__pycache__/`, `*.pyc`, `.DS_Store`, and other editor-specific files. If any environment-specific files are already tracked (for example `spaceinvaders/pyvenv.cfg`) remove them from git history or untrack them before pushing.

If you'd like, I can:
- Add a short section to the `README.md` linking to this file, or
- Update the project's `.gitignore` and remove tracked local environment files from git history.

