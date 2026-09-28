# Native Grease Pencil comparison

User-authorized same-design comparison, 14 September 2026. **Result: native Grease Pencil carries this character and box action while retaining live motion controls.** This is a small review candidate, with no new likeness or full-cast claim.

[Play the side-by-side comparison](artifacts/gp-proof-v004/curves-vs-grease-pencil.mp4) · [GP alone](artifacts/gp-proof-v004/grease-pencil-with-sound.mp4) · [Native GP scene](artifacts/gp-proof-v004/cartoon-skin.blend) · [Comparison still](artifacts/gp-proof-v004/comparison.png)

The left side is coherent-proof-v003, the previously delivered curve/mesh character. The right side replaces all 48 visible character parts with native GP strokes and fills. Design, proportions, camera, 240-frame action, stage, effects and decoded sound remain the same. Similar appearance is the intended result of isolating the drawing representation.

## What was measured

| Check | Curves/meshes | Native GP |
|---|---|---|
| Original 12 motion controls | Reference | Identical on all 240 frames |
| Projected hand/shoe contours | Reference | Zero measured difference on all frames |
| Limb centreline samples | Reference Bezier evaluation | Maximum difference 0.0000901 scene units, about 0.00481 pixel at 640px |
| Hand-control edit after saving/reopening | Passed | Passed |
| Hair-point and limb-width edits after saving/reopening | Passed | Passed |
| Native editable character geometry | Curves, meshes and digit text | 48 GP objects, with native stroke/fill points |
| Body playback | Existing native controls/drivers | Native point drivers referencing only the controls; no body-frame bake or custom playback handler |
| Sound | Original selected sound | Decoded audio hash matches |
| Movie | 10 seconds, 24 fps | 10 seconds, 24 fps; full decode passes |

Evidence: [GP geometry](artifacts/gp-proof-v004/checks.json), [GP saved edits](artifacts/gp-proof-v004/editability-checks.json), [curve/mesh saved edits](artifacts/gp-proof-v004/curve-editability-checks.json), [encoded movies](artifacts/gp-proof-v004/video-checks.json). The diagnostic edited scenes are separate files and intentionally alter the action; the main comparison scene retains the original action.

The recorded final-frame log times were 72.357 seconds for the existing curve/mesh render and 64.534 seconds for the GP render. These are single sequential runs, not a controlled performance benchmark. The GP scene is 1,927,013 bytes versus 1,701,484 bytes for the source; both retain archived artwork, so this does not measure geometry-format overhead in isolation. The GP conversion/build took 1.41 seconds after loading existing design and motion; that excludes agent authoring/debugging effort and is not a fresh-character production estimate.

## Visual findings and limits

Agent inspection covered native standing, deep push and raised-arm poses, the side-by-side push frame, and the [24-frame encoded motion sheet](artifacts/gp-proof-v004/motion-sheet.png). The silhouette, expressions and waist construction remain close in those samples. Small stroke-edge/rasterization differences are visible. No new per-pose artwork repair was made for this conversion. Full subjective playback/listening and user acceptance remain pending; encoded checks and sampled stills cannot supply that judgment.

Three candidate builds stopped during verification: the first compared against source geometry that no longer evaluated after archiving; the second checked GP parts excluded from the active measurement layer; the third exposed subpixel point-driver differences near integer values. The corrected check captures source geometry while active, evaluates every GP layer during measurement, and records the observed interior-point tolerance while keeping endpoint and contact checks stricter. All failed candidates remain preserved.

This proves a control-driven native GP implementation for the tested view and action. It does not test automatic weights or establish arbitrary anatomical deformation, head turns, crossed-arm depth changes, new costumes, or stronger likeness. The same torso/shorts compositor remains in use; replacing it with native GP masking was deliberately not another variable in this comparison.

The current driven drawings use fixed layer/frame/point addressing. Direct shape edits to undriven artwork and stroke-radius changes work. Adding/deleting/reordering points or driven layers requires rebinding their animation; driven limb positions are edited through the existing controls. A freely redrawn, multi-view actor would require a separate construction test. These limits belong to this implementation, not to GP as a whole.

**Decision supported:** keep the native GP candidate available for further character work. This experiment establishes that we can change the drawing representation without losing this motion. It does not establish a visual-quality advantage or justify replacing every existing film.

## Reproduce

Run from the workspace root using a fresh output name:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python experiments/008_cartoon_skin/build_gp.py -- --out gp-proof-v005
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python experiments/008_cartoon_skin/build_skin.py -- --out gp-proof-v005 --render
python3 experiments/008_cartoon_skin/finish_gp.py gp-proof-v005
```

These commands reproduce the native scene, all-frame geometry/live-hand checks and comparison movies. The separate matched hair/width/saved-hand diagnostic files were additional MCP checks performed for this report.

The actual build and saved-edit checks ran through the installed Blender MCP in an isolated background Blender 5.2 instance. The initial connector was disconnected and its CLI launcher lacked the executable path; starting the already installed MCP add-on in the known Blender executable restored the connection. No add-on installation, system configuration change or existing GUI scene change was needed. Rendering used the existing background Blender helper. The geometry/material construction reuses native GP mechanisms documented in `Dawn_Training/production_scripts/RESEARCH.md`; no image tracing or new art generation was involved.
