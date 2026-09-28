#!/bin/zsh
set -euo pipefail
cd "$(dirname "$0")/../../.."
BLENDER=/Applications/Blender.app/Contents/MacOS/Blender
BLENDER_PY=/Applications/Blender.app/Contents/Resources/5.2/python/bin/python3.13
FILM=experiments/007_trent_corner
export PENCIL_REVISION="film-v002-rebuild-$(date +%Y%m%d-%H%M%S)"
OUT="$FILM/artifacts/$PENCIL_REVISION"
# Each reproduction gets a fresh version; the delivered movie and mix are preserved.
"$BLENDER" --background --factory-startup --python-exit-code 1 --python "$FILM/scripts/build_advanced.py"
"$BLENDER_PY" "$FILM/scripts/sound_advanced.py"
python3 pipeline/audio.py build "$FILM/production.json" --out "$OUT/audio-v001"
python3 "$FILM/scripts/finish_advanced.py" --audio-only
"$BLENDER" --background --factory-startup --python-exit-code 1 --python "$FILM/scripts/verify_advanced.py"
"$BLENDER" --background --factory-startup --python-exit-code 1 --python "$FILM/scripts/render_advanced.py"
python3 "$FILM/scripts/finish_advanced.py"
