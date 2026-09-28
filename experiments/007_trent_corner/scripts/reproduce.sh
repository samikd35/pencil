#!/bin/zsh
set -euo pipefail
cd "$(dirname "$0")/../../.."
revision="${1:-film-v002}"
case "$revision" in ''|*[!a-zA-Z0-9_-]*) print -u2 'Use a revision name containing letters, numbers, underscores or hyphens.'; exit 1;; esac
export PENCIL_REVISION="$revision"
production='experiments/007_trent_corner'
output="$production/artifacts/$revision"
[[ ! -e "$output" ]] || { print -u2 "Output already exists: $output"; exit 1; }
mkdir -p "$output/stills"
blender='/Applications/Blender.app/Contents/MacOS/Blender'
python='/Applications/Blender.app/Contents/Resources/5.2/python/bin/python3.13'
"$blender" --background --factory-startup --python-exit-code 1 --python "$production/scripts/build_film.py" > "$output/build.log" 2>&1
"$python" "$production/scripts/select_sound.py"
python3 pipeline/audio.py build "$production/production.json" --out "$output/audio-v002"
python3 "$production/scripts/finish_delivery.py" --audio-only
"$blender" --background --factory-startup --python-exit-code 1 --python "$production/scripts/verify_project.py" > "$output/verify.log" 2>&1
"$blender" --background --factory-startup --python-exit-code 1 --python "$production/scripts/render_film.py" > "$output/render.log" 2>&1
python3 "$production/scripts/finish_delivery.py"
