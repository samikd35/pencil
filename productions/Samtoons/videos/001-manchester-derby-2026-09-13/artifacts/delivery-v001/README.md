# Ten Men. Two Posts. No Points. — final render

Approved source: animatic-v004. User approved the full picture and sound and requested the high-quality render on 16 September 2026.

Native render: 1920×1080, 24 fps, 3,768 frames / 2:37. EEVEE, 64 temporal samples. All seventeen shots are rerendered from the approved Blender file; the preview is not enlarged. Shot timing, cameras, motion, text and selected sound remain as approved.

The final MP4 and editable `samtoons-final.blend` are the main deliverables. `mix-review.wav` is the exact approved lossless stereo mix. Separate stems remain in [the approved audio build](../animatic-v004/mix/stems/). `plan.json` retains paths to versioned local source audio, and the Blender file contains packed artwork and the mix.

Reproduce from the workspace root:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python productions/Samtoons/videos/001-manchester-derby-2026-09-13/scripts/render_full_animatic.py -- --final-v001
python3 productions/Samtoons/videos/001-manchester-derby-2026-09-13/scripts/finish_full_animatic.py --final-v001
```

The render helper refuses existing scene outputs. Preserve this delivered revision and use a new output directory for revisions. The input checkpoint hashes are verified before full rendering.

The film is authored football comedy/parody. Production provenance and factual-source notes remain internal; use the parody description when publishing. No publication has been requested or performed.

The exact full-resolution encoded movie still requires final delivery playback review. Approval of the earlier animatic is recorded separately.
