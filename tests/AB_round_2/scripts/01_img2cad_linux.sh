#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v uv >/dev/null || { echo 'Install uv: https://docs.astral.sh/uv/'; exit 2; }
uv venv --python 3.13 .venv-img2cad
uv pip install --python .venv-img2cad/bin/python 'img2cad==0.15.0'
.venv-img2cad/bin/img2cad doctor
echo 'Next: run an image-capable coding agent with img2cad_job/AGENT_INSTRUCTIONS.md'
