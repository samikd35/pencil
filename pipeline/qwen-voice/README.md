# Local directed voice generation

The runtime is stored at `~/Models/qwen-voice`, outside the Pencil project, so it remains available to other local work. It uses MLX Audio 0.5.4 and Qwen3-TTS-12Hz-1.7B-VoiceDesign bf16 on Apple Silicon. The pinned model plus speech tokenizer is 4,520,194,992 bytes. The source revision and LFS hashes are in model-source.json. Do not move partially downloaded weights into place: the runtime's download_remaining.py verifies size and SHA-256 before renaming them.

Create a new WAV with an explicit acting direction:

```sh
python3 pipeline/qwen_voice.py \
  --text 'Ref! Ref!' \
  --direction 'A young adult male shouting furiously across a football pitch. Two explosive projected calls; comic outrage, strong vocal attack. Clean dry recording.' \
  --out productions/Samtoons/videos/001-manchester-derby-2026-09-13/assets/voices-v002/bruno-local.wav
```

Run from the Pencil workspace. The helper selects the shared virtual environment automatically and loads the local model directory. Other projects can use `~/Models/qwen-voice/.venv/bin/python` and the models under `~/Models/qwen-voice/`. The helper refuses to overwrite takes and records the direction, seed, model source, waveform hash, elapsed time and peak MLX memory. Review the actual performance; instructions and technical assertions do not establish emotional quality. VoiceDesign can vary timbre between generations: repeated descriptions are not a guarantee of a fixed character voice. Cache chosen takes; resolve recurring voice identity with auditioned conditioning before generating a full cast of new lines.

Model: https://huggingface.co/mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16 (Apache-2.0, derived from Qwen).
Runtime: https://github.com/Blaizzy/mlx-audio (MIT).
No paid API or account is required for local generation. The initial voices-v002 scene contains separately identified official hosted-demo takes, not local generations.

## Verified on this laptop

Offline generation passed on macOS 26.2, M4/24GB: a 1.36-second test, 68.51-second cold load, 5.89-second generation, about5.3GiB peak MLX allocation. See the Samtoons voices-v002/local-setup.json for exact measurements and limitations. The CLI loads a model per invocation; keep one loaded model session when a future batch of lines justifies that optimization. Current outputs are cached, not regenerated for retiming.

Installation used Python 3.13.5 and `uv pip install` into the shared runtime's `.venv`. `requirements-lock.txt` records installed versions. Network streaming of the MLX Metal wheel timed out; the retained official wheel was downloaded separately and checked against metal-wheel-source.json, then passed as a local wheel to `uv pip install` with `UV_HTTP_TIMEOUT=300` and the runtime's persistent pip-cache. Large model files were downloaded in resumable ranges and verified against the published hashes in model-source.json.
