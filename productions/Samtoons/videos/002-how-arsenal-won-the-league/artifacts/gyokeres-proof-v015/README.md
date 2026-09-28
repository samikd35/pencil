# Gyökeres complete-character review — v015

**Selected candidate:** `gyokeres-proof-v015-review2.mp4`, with editable `gyokeres-proof-v015-review2.blend`. User review pending. The first internal movie retains an inherited neutral-pose lean and is superseded.

## Coverage

- 0–2.7 s: source-fitted rig walk and stop.
- 2.7–6 s: connected sleeve/arm bend and dialogue, “Then why am I here?” Existing approved take begins at 3.5 s, with native mouth geometry timed within its actual words.
- 6–14 s: complete matching run/jump drawings, using Bruno v003’s exposure schedule, separate camera travel and support registration. Start and settled positions are recalculated for Gyökeres’s drawing.

## What was retained and what changed

Video 1 supplies the continuous complete-character mesh, fitted bone controls and semantic binding method. Bruno v003 supplies the accepted extreme-action construction and temporal strategy. The original whole Gyökeres drawing provides his head, neck, clothes, limbs and shoes together. There is no separate replacement head surface. New complete run/jump drawings use that identity; they have not inherited Bruno’s creative approval.

The v012 adaptation simultaneously changed rest proportions and retargeted existing motion. The v013/v014 attempts then changed facial construction independently of the body. Both approaches lost qualities the user had already required. They are rejected evidence, not approved foundations.

The present proof exposed additional construction faults before review: silhouette triangulation made narrow triangles vulnerable at abrupt weight boundaries; a regular UV grid with weights smoothed within the source silhouette removed the detected folds. Copying Bruno’s resting travel offsets also sheared the new character’s legs at rest; fitting those offsets to the new source fixes that while retaining the action timings and images.

## Checks and limits

The rendered movie is 336 frames, 14 seconds, 1280×720, 24 fps, with the existing voice take at normal speed. `deformation-check.json` covers every rig frame and visible source-surface triangles, rather than invisible transparent grid corners. Zero detected inversions is a construction check, **not** a claim of benchmark-quality acting. Some local compression/stretch remains; inspect clothing and joints in playback.

`action-check.json` checks registered support anchors and single-pose visibility. Those anchors do not establish anatomical realism or validate all visible boot geometry. Complete-pose substitutions remain drawings exposed on twos; ordinary motion uses the rig. Facial acting is limited to this short line and two blinks, not a general dialogue proof. No full turns or other characters were tested. Sound effects/music are omitted from this isolated motion test; the film’s approved sound direction remains unchanged.

Render samples and the encoded file were inspected; QuickTime playback was opened. No assistant listening acceptance or user approval is claimed. Judge recognition, head-to-toe coherence, clothing, contacts, energy, lips and eyes together before proceeding with the cast.

## Reproduction

In visible Blender, load `scripts/build_gyokeres_proof_v015.py` as a namespace and call `setup()`, `rig()`, `animate_rig()`, `action()`, `regular_surface()`, `facial()`, `fit_action_rest()`, then save the scene. Existing scenes are guarded against replacement. The two inspected reusable sources are Video 1 `build_option_a.py` / `repair_cast.py`, and this film’s `revise_pose_action_v003.py`.

Run `scripts/check_gyokeres_proof_v015.py` against the saved native scene. `scripts/render_gyokeres_proof_v015.py` streams the bounded proof through ffmpeg and refuses to overwrite its output. Keep this candidate separate from the rejected first batch until the combined qualities are accepted.
