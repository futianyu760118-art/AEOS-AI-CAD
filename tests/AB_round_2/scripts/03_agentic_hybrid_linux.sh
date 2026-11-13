#!/usr/bin/env bash
set -euo pipefail
# Run only after official CUDA/DA3/SAM2/COLMAP setup and model-weight installation.
cd "$(dirname "$0")/.."
: "${OPENAI_API_KEY:?OPENAI_API_KEY must be set outside scripts}"
: "${OPENAI_MODEL_ID:?OPENAI_MODEL_ID must be set outside scripts}"
[ -f vendor/agentic-cad/.venv/bin/activate ] || { echo 'Run 02_agentic_cpu_linux.sh first'; exit 2; }
. vendor/agentic-cad/.venv/bin/activate
python - <<'PY'
import torch
if not torch.cuda.is_available():
    raise SystemExit('GPU CUDA unavailable: hybrid run aborted')
PY
agentic-cad reconstruct inputs/four_views \
 --prompt "$(cat agentic_job/PROMPT.txt)" \
 --reconstruction hybrid --provider openai --model "$OPENAI_MODEL_ID" \
 --max-repairs 3 --timeout 900 --max-output-tokens 32768 \
 --output results/A_agentic/hybrid_first
