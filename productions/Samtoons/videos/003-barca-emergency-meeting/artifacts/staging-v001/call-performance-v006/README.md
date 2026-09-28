# S08 — new stickman-first performance

This is a separate 10-second reconstruction of the Pérez–Müller call. v005 only rebound the previous movement and did not satisfy the request for fresh animation. v006 creates a connected skeleton, authors new motion, and saves that foundation before attaching the selected caricature artwork.

Watch `call-review.mp4` for the dressed scene, `stickman-review.mp4` for the body foundation, or `binding-comparison.mp4` for both in synchronization. All three retain the exact existing audio bitstream.

## Construction and performance

- New bone hierarchy and new body/head movement: Müller anticipates and lifts the picture, settles through his boast, then reacts and lowers it. Pérez listens, gestures with the pen during his question, then settles. His other hand retains desk contact.
- The existing vector drawings, environment, dialogue, captions and audio-aligned mouth cues are reused. Gaze, blinking and brows have newly authored timing. The old pose and animate functions are never called.
- The original foundation armatures remain in the bound scene. Every evaluated bone matrix across all 240 frames is identical before and after artwork attachment. Wrists have shared armature weights, without separately animated connector patches.
- Native mesh/curve artwork, not Grease Pencil or character image planes. The selected drawing controls proportions; the new performance is in `movement-beats.json` and `scripts/build_call_performance_v006.py`.

## Verification and review

All 240 frames pass the scoped construction checks. Maximum joint-target error is 0.0014 source pixels. Saved-file frame 151 matches the live render exactly. All three movies fully decode at 24 fps with 240 frames; the main scene is 1280×720. Audio is bitstream-identical to v004, with no voice generation or mixing changes.

Inspected the hand/cuff joins at frames 38, 150 and 215, consecutive encoded Pérez frames 146–154 and Müller frames 206–214, and wider entry/gesture/recovery frames. No open joint gap or abrupt jump was observed in those samples. Small contour/grip drawing imperfections remain. Normal-speed acting and sound are supplied for user playback; no new listening assessment or creative acceptance is claimed.

This proof covers the current view, held grips and seated/standing call actions. Müller's resting right arm remains part of the torso artwork in this shot; independent movement there needs separate artwork. New head views, grips or extreme poses still need appropriate drawings and validation. This is not a universal deformation solution or full-film approval.

## Reproduction

In a clean visible Blender session, load `scripts/build_call_performance_v006.py` into a Python namespace and call `build()`. It saves `stickman-foundation.blend` before `call-performance.blend`. The existing renderer supports `--revision v006`, adding `--foundation` for the foundation file. Run `check_call_construction.py` against the saved dressed scene. The builder owns this revision; preserve these files when revising.

`foundation-check.json`, `binding-check.json`, `call-performance-checks.json` and `export-check.json` record the actual technical checks. Earlier versions remain intact.
