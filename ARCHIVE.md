# Pencil GitHub archive

This repository preserves authored code, production records, reusable assets,
selected native Blender projects, and selected finished or review media. It is
not a byte-for-byte copy of the original Pencil folder.

## Included

- Shared pipeline, production profiles, scripts, research, briefs, plans, and journals.
- Reusable assets outside `artifacts/`.
- Small authored records inside `artifacts/` (for example READMEs, edit maps,
  manifests, subtitles, checks, and source notes).
- Selected editable `.blend` files and delivery/review media from completed
  experiments and Samtoons productions. Large selected files use Git LFS.

## Local-only or omitted

- `.runtime/` weights, virtual environments, package caches, and local tools.
  The Qwen voice runtime was moved to `~/Models/qwen-voice` and is not in GitHub.
  `pipeline/qwen_voice.py` uses that shared location.
- Blender backup files, logs, caches, temporary renders, and superseded
  preview media. Some historical project records still point to these files.

## Known gaps in the original folder

- Arsenal's records name `artifacts/hand-repair-v025/hand-repair-v025.blend`
  and `artifacts/delivery-v027/sources/remaining.blend`; neither file exists
  locally. The original editable delivery package is also absent.
- Some available Arsenal `.blend` files already refer to missing preview audio.
  The delivered video and available source scenes are preserved, but a complete
  editable reconstruction of that film is not verified.
- Some Barcelona staging scenes use the macOS Arial Bold font. Reopening on a
  different system may substitute it.

Before deleting the local folder, confirm that every wanted file is present in
a fresh clone with `git lfs pull`. The Qwen runtime is already outside Pencil.
