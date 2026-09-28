# S12 — A founding member

13-second staging candidate, 1280×720, 24 fps. The phone lowers, the scarf is revealed, Valencia retrieves the membership card, and the fan becomes defensive. The two original dialogue lines are present. This is an intermediate scene review, not final-film or sound acceptance.

- `membership-review.mp4`: combined picture and actual dialogue, with quiet paper foley.
- `membership.blend`: native scene, arm drawings, facial controls, camera, captions and authoritative audio strip.
- `grip-review.jpg`, `scene-review.jpg`: crops from the actual encoded movie, not separate beauty renders.
- `verification.json`, `native-verification.json`: actual technical checks and review limits.
- `render-selection.json`, `audio/`: shot-local mix plan, resolved cues, stems and premaster. Full-film S12 still starts at frame 3109 in production.json.

## Construction and observed correction

The first source-contour arm warp pulled neighboring scarf/shirt pixels and tore the torso when the wrist moved. A local weighting adjustment failed to resolve the whole region. That arm/body binding chain and its dependent shape-key animation were discarded. `rejected-warp-construction.blend` and the failed probes retain the evidence.

The replacement removes the moving arm from the source body extraction and draws the arm explicitly through its intended poses. A swept contour stays connected through the elbow; the fan's shoulder belongs to one sweater silhouette. The returning forearm crosses above the scarf, while the polo cuff occludes the bare upper arm. The hand and prop share a rigid attachment. These are bounded projected drawings for these gestures, not a universal skeleton or a physics solver. Independent source faces, room and dialogue are retained.

All new line strokes are flattened in depth: a bevelled 3D line was previously piercing the foreground neck despite its nominal rear layer. Eyebrows and mouth backings were cleaned separately. The archive is already open when established, so no drawer moves without a hand on it.

## Review and limits

Inspected the phone grip through frames 20,31,43 and retrieval through 99,108,118,124,138, then wider scene/insert/reaction frames from the encoded video. The prior torso holes and stretched scarf are absent in those samples. The hands remain fixed grips, with small source-edge fringes and a small source remnant at the inner polo cuff; these are not represented as final polish. The card insert uses the same fan's face with tears and an invented FIRST MEMBER · 2020 support-group card, not a historical membership claim.

Normal-speed creative acceptance and listening to the new voice remain a user checkpoint. The agent has not heard the dialogue and does not infer vocal performance quality from RMS mouth timing or audio-stream checks. The opening laugh is visually mimed; no separate snort take has been added. S03 still needs the matching scarf-edge continuity detail at assembly. The existing S07 rejection is not cleared by this scene.

## Reproduction

Source owners: `scripts/prepare_membership_v001.py` and `scripts/build_membership_v001.py`, relative to the video root. New art, contours and voice metadata are under `assets/membership-v001/` and `assets/voices-s12-v001/`. Do not overwrite a delivered version; select a fresh output directory before rebuilding.

1. Run the extraction script with the existing `.runtime/vector-art` dependencies and `.runtime/qwen-voice/.venv/bin/python`.
2. In visible Blender load the builder module and call `setup()`, `actors()`, `animate()`. Preserve other scenes.
3. Build `render-selection.json` with the shared `pipeline/audio.py build ... --out .../audio`, then `finish()` writes the isolated scene library. This preserves the user's other open native work.
4. Run `check_native.py` with Blender `--background membership.blend --python-exit-code 1 --python check_native.py`. It checks the saved scene and saves it as a normal project opening directly on S12.
5. Render with `scripts/render_staging_scene.py -- S12 S003_S12_Membership_v001 membership`, then run `check_preview.py` with the existing PIL runtime. Rendering selects the saved S12 scene explicitly and reuses the premaster.

Do not substitute parameter alignment or a connected polygon assertion for visual review of a new action.
