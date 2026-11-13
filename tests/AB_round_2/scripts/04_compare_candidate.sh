#!/usr/bin/env bash
set -euo pipefail
# Usage: bash scripts/04_compare_candidate.sh path/to/front_registered_1254.png results/B_img2cad
cd "$(dirname "$0")/.."
[ $# -eq 2 ] || { echo "Usage: $0 front_aligned.png result_dir"; exit 2; }
python evaluate.py --reference reference/FRONT.png --candidate "$1" --out "$2"
