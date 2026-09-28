# Temporal jitter diagnosis — pose action v002

User review: running/jumping mechanics now work and no construction inconsistency was reported, but the picture vibrates between frames. Preserve the accepted action direction. Overall motion proof remains pending because temporal smoothness was rejected.

## Confirmed cause

The body root is also each drawing's silhouette-area centre. In `build_pose_action_v001.py`, `grounded()` reconstructs this root from a fixed plant and each drawing's different foot offset. Each support drawing and its root are held for two frames, then replaced abruptly. Thus the root is a discontinuous contact/drawing-placement value, not an independently authored travel path.

`revise_pose_action_v002.py` follows that same value every frame with `camera_x += (root_x-camera_x)*0.35`. The camera moves on frames when the complete body is held. It then accelerates after the next drawing/root jump. Filtering attenuates the pulses but does not remove their source. This mixes held character positions with continuously following camera motion.

Read-only evaluation of the actual saved scene, steady-run frames 29–100, measured:

- Root advancement: 0 to 0.536 world units per frame (0 to 122.5 image pixels under a stationary camera).
- Background advancement: 31.0 to 63.0 pixels per frame, caused by the tracking camera's repeated speed changes.
- Projected character root: −41.0 to +59.5 pixels per frame. This is the perceived backward/forward oscillation, not intentional root acting.
- All 192 encoded frame timestamps are spaced at 1/24 second within timestamp rounding. Missing/irregular encoded timestamps do not explain this reproducible native-scene fault. Display-specific playback effects were not tested.

An especially direct pair is frames 29→30: the identical whole drawing remains at the identical world position, but the camera shifts its entire screen image left by 36.35 pixels. Frames 31→32 repeat that effect by 32.93 pixels. This observation needs no subjective inference about anatomy.

## Isolation and remaining limits

The orthographic projection permits exact counterfactual isolation without altering the scene. A frozen camera removes all background movement, but leaves character world steps ranging 0–122.5 pixels. Constant-speed tracking removes background speed pulses, but leaves character root steps −48.4 to +74.1 pixels. Therefore a camera-only smoothing patch is insufficient. No replacement movie is claimed from these calculations.

The jump uses longer held drawings followed by immediate whole-silhouette substitutions. Its ballistic root can be continuous while internal landmarks change abruptly. This is a separate, visible construction/exposure limitation; the root measurements do not quantify head/pelvis registration or prove its share of the user's perception. Check those landmarks when authoring breakdowns. Do not change the now-accepted action poses indiscriminately.

## Correction at the right level

Separate planned world travel, local pose/contact offsets and camera framing. Track the intended travel path, not a centre recomputed from changing opaque pixels. Establish deliberate exposure cadence for pose, translation and camera together. For the requested smooth result, add registered transition drawings or controlled local deformation where needed to carry the body forward while a support foot stays planted. Simply smoothing the entire rigid drawing creates foot sliding. Two-frame drawing exposure itself is not an error; the incompatible travel/camera sampling is the demonstrated fault.

Verify character landmarks and stationary background landmarks separately across consecutive frames, alongside world foot contacts. Compare camera held versus tracking and view the actual encoded playback at normal speed. Do not promote a numerical pass as smoothness acceptance.

## Reproduce

From the workspace, run:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b productions/Samtoons/videos/002-how-arsenal-won-the-league/artifacts/pose-action-v002/pose-action-v002.blend --python-exit-code 1 --python productions/Samtoons/videos/002-how-arsenal-won-the-league/research/temporal-jitter-v001/audit.py
```

This writes `audit.json` and `frames.json`, then intentionally fails on the reproduced >80-pixel steady-run root step. That threshold is a detector for this known artifact, not a universal animation quality limit. Actual run: exit 1, `REPRODUCED: root advances abruptly by >80 px/frame during steady run`. Preserve v002; no scene edits were made in this diagnosis.
