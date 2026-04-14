#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="${1:-${ROOT_DIR}/scripts/release_installer.env}"

log() {
  printf '[livescan-installer] %s\n' "$*"
}

fail() {
  printf '[livescan-installer][error] %s\n' "$*" >&2
  exit 1
}

if [[ -f "${CONFIG_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${CONFIG_FILE}"
  log "Loaded configuration from ${CONFIG_FILE}"
else
  log "Configuration file not found at ${CONFIG_FILE}; using defaults"
fi

PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-${ROOT_DIR}/.venv}"
INSTALL_MODE="${INSTALL_MODE:-editable}"
EXTRAS="${EXTRAS:-dev}"
PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
START_API="${START_API:-false}"
UPGRADE_PIP="${UPGRADE_PIP:-true}"

command -v "${PYTHON_BIN}" >/dev/null 2>&1 || fail "Python binary not found: ${PYTHON_BIN}"

log "Creating virtual environment at ${VENV_DIR}"
"${PYTHON_BIN}" -m venv "${VENV_DIR}"

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

if [[ "${UPGRADE_PIP}" == "true" ]]; then
  log "Upgrading pip/setuptools/wheel"
  pip install --upgrade pip setuptools wheel
fi

case "${INSTALL_MODE}" in
  editable)
    log "Installing LiveScan in editable mode with extras '${EXTRAS}'"
    pip install -e "${ROOT_DIR}[${EXTRAS}]"
    ;;
  release)
    log "Building a wheel and installing from dist/"
    pip install build
    python -m build "${ROOT_DIR}"
    latest_wheel="$(ls -t "${ROOT_DIR}"/dist/livescan-*.whl | head -n 1 || true)"
    [[ -n "${latest_wheel}" ]] || fail "No wheel file found under dist/"
    pip install "${latest_wheel}"
    ;;
  *)
    fail "Invalid INSTALL_MODE='${INSTALL_MODE}'. Supported values: editable, release"
    ;;
esac

log "Installation completed"
log "Activate with: source ${VENV_DIR}/bin/activate"

if [[ "${START_API}" == "true" ]]; then
  log "Starting API on ${HOST}:${PORT}"
  exec uvicorn livescan.api.main:app --host "${HOST}" --port "${PORT}"
fi
