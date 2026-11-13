#!/usr/bin/env bash
set -euo pipefail
# Linux + Python 3.12 + internet + OPENAI_API_KEY + OPENAI_MODEL_ID are required.
cd "$(dirname "$0")/.."
: "${OPENAI_API_KEY:?Set OPENAI_API_KEY in your shell, never in this file}"
: "${OPENAI_MODEL_ID:?Set OPENAI_MODEL_ID in your shell}"
command -v python3.12 >/dev/null || { echo 'Python 3.12 required'; exit 2; }
mkdir -p vendor results/A_agentic
if [ ! -d vendor/agentic-cad/.git ]; then git clone https://github.com/dancher00/agentic-cad.git vendor/agentic-cad; fi
python3.12 -m venv vendor/agentic-cad/.venv
. vendor/agentic-cad/.venv/bin/activate
pip install -r vendor/agentic-cad/constraints/cpu-py312.txt
pip install --no-deps -e vendor/agentic-cad
agentic-cad reconstruct inputs/four_views \
 --prompt "$(cat agentic_job/PROMPT.txt)" \
 --reconstruction gpt --provider openai --model "$OPENAI_MODEL_ID" \
 --max-repairs 3 --timeout 900 --output results/A_agentic/gpt_first
