#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 -m venv .venv || true
source .venv/bin/activate
pip install -r tools/requirements.txt >/dev/null
python3 tools/specgen.py configs/spec.yaml
echo "[apply_spec] Done."
