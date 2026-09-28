# S08 — separate binding version

Second construction of the same 10-second Pérez–Müller passage. The scene, likeness, dialogue, captions and authored timing are retained. v004 remains the comparison baseline; the user did not accept its remaining hand defects.

## What changed

Each character now has one connected, eight-bone body skeleton. Elbows and wrists inherit their parent bones, and the face inherits the head. The caricature surfaces use that same armature. Wrist skin, shading and outline share weights; there are no separately keyed wrist patches or independent joint objects in the saved scene. Local gaze, blinking, brows and mouth controls remain editable.

This is native Blender vector mesh/curve artwork with armature binding, not Grease Pencil. The builder reuses v004's drawing and performance helpers, creates a separate scene, and replaces their binding. In Pose Mode, the stick display exposes the connected foundation.

## Checked

- All 240 frames pass the scoped evaluated surface, joint continuity and wrist checks. Maximum pose-transfer error: 0.0013 source pixels.
- Inspected enlarged hand joins at frames 139, 192 and 214, then consecutive encoded Pérez frames 135–143 and Müller frames 209–217. No open wrist gap or abrupt joint jump was observed in those samples. Small contour and grip-design imperfections remain; binding does not redraw them.
- The saved-file render matches live frame 139 exactly. The complete 1280×720, 24 fps export decodes successfully.
- The exported AAC audio bitstream matches v004 exactly. No voice model, take, timing or mix was regenerated. No new listening assessment is claimed.

## Files and scope

`call-review.mp4` is the picture/sound comparison; `call-performance.blend` is editable. `binding-check.json`, `call-performance-checks.json` and `export-check.json` record technical checks. The enlarged review images record the inspected regions.

This proves binding for the existing three-quarter views and call gestures. New angles, extreme poses and different grips still need suitable drawings and validation. It is not full-film or benchmark-quality acceptance.
