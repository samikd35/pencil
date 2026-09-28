# S08 call reconstruction — review candidate

[Ten-second movie](call-review.mp4) · [Editable Blender file](call-performance.blend) · [Construction checks](construction-check.json) · [Export/rebuild comparison](export-check.json)

This revises Pérez and Müller's existing call performance. The recognized likeness, separate eyes/brows/mouth controls, boast → question → uneasy reaction and picture-lowering beats remain. The character artwork is native colored mesh geometry traced from the selected drawing, with source-fitted armatures and keyed corrections. It is **not Grease Pencil**, a photographic head or a textured character plane.

## Established causes and repairs

| Failure | Cause found | Repair in this candidate |
|---|---|---|
| Scarf/neck pulled apart with the picture | Spatial weights gave overlapping prop/arm/torso artwork the wrong anatomical ownership | Separate grip/prop/forearm surfaces; torso has only head/torso weights; complete hidden garment and scarf coverage |
| Folded, plank-like sleeves | Smoothed sleeve envelopes self-intersected even at valid joint positions | Complete overlapping upper-arm drawings and source-traced foreground forearms; test evaluated boundaries |
| Sudden elbow reversal | The pole crossed the moving shoulder–wrist axis | Carry the authored bend side with the axis using `pipeline/pose_geometry.py:transported_pole` |
| Excessive wrist bend while lowering the picture | Independent prop tilt and wrist travel demanded an implausible combined pose | Reblock wrist travel and register grip/prop to the whole arm; this drawing uses a bounded 42° wrist range |
| Frame/pen outlines crossed fingers | Converted stroke bevels protruded in depth through foreground artwork | Flatten converted ink geometry; preserve explicit grip/prop layer order |
| Paper fringe and disconnected cuff edge | Loose source masks retained foreign pixels; a closed wrist edge rotated away from the sleeve | Isolate actual skin/ink, cut the hand at an open registered boundary, connect it to the evaluated cuff with native keyed geometry |

Earlier failures are retained in `../call-performance-v003/rejected-binding.blend`, `rejected-sleeve-construction.blend`, `rejected-sleeve-builder.py` and `failed-contour-check.json`. The failed sleeve check reproduced intersections on six diagnostic frames. These were failed constructions, not successful stages or accepted review outputs.

## Review starts with the defects

The latest user instruction is adopted: prioritize the weakest image and changed region, then its movement; briefly check the wider frame for regressions. Do not repeatedly review stable scenery at the expense of a faulty hand.

- **Müller grip/cuff:** enlarged crops at frames 163, 181, 192, 205, 214 and 240; [sequence](focused-review/muller-grip-sequence.png). Checked the lowering transition, frame occlusion and hand-to-sleeve silhouette. No open wrist gap or prop-outline penetration was observed in these crops. Slight line-width/paint variation remains visible at enlarged diagnostic scale.
- **Pérez grip/cuff:** frames 115, 127, 139, 151, 175 and 193; [sequence](focused-review/perez-grip-sequence.png). The wrist meets the cuff through the pen gesture without the former separated cap. The small drawn shadow transition is still simplified.
- **Encoded consecutive frames:** [Müller 209–217](focused-review/muller-encoded-neighbours.png), [Pérez 135–143](focused-review/perez-encoded-neighbours.png). No new tear or grip pop was observed in these intervals. Crop bounds and source frame numbers are in [crops.json](focused-review/crops.json).
- **Brief regression checks:** complete frame 214 for framing, arm/scarf overlap and monitor containment; changed eyelids at frames 74 and 102 for closed eyes and glasses alignment. [Eyelid crops](focused-review/eyelid-regression.png).

These are actual static/consecutive-frame inspections. The agent did **not** listen to the soundtrack or establish normal-speed comic timing by watching the full clip. The cached voice candidates are retained for user playback; no voice model was removed or replaced.

## Technical evidence

All 240 frames pass the evaluated sleeve/wrist contour, body triangle orientation and wrist-range checks. Five constructed surfaces are tested; the maximum elbow step is 12.009 source pixels and wrist angle 42.001° including numerical rounding. Source limb-length error is below 0.000023 pixels. These numbers establish the tested geometry, not artistic approval.

Fresh-process rendering of the saved file matches the live frame 139 exactly. A clean build from `scripts/build_call_performance_v004.py` matches live frames 139 and 214 exactly. The rebuilt check file is retained under `rebuild-check/`. No live Python frame handler is required for playback. The export is 1280×720, 24 fps, 240 frames / 10 seconds, H.264 with a 48 kHz AAC track; complete FFmpeg decoding reports no errors.

## Ownership and limits

The maintained builder and `scripts/trace_call_reference_v003.py` own construction; `assets/reference-redraw-v003/call-pose.png` and the registered contour JSONs are inputs. The saved `.blend` is the exact reviewed/rendered snapshot. `render-inputs.json` binds its source hashes. Rerender using `scripts/render_call_review_v001.py -- --revision v004`; run `scripts/check_call_construction.py` inside Blender for the geometry check.

This proves a bounded call gesture in the selected three-quarter views. It does not demonstrate a profile turn, a new grip, running, football contact or arbitrary extreme deformation. Those actions need suitable complete drawings/correctives and targeted review. The next production work remains the S04 ensemble and S06–S07 physical-action passages, followed by the existing combined staging/sound and animatic decisions. No full-film checkpoint or benchmark parity is claimed.

Professional-method research and source links are in [reference-drawing-v001.md](../../../research/reference-drawing-v001.md). The reusable changes are surface ownership, complete hidden artwork, stable bend direction, registered wrist boundaries and focused defect review—not these actors' coordinates or one universal animation.
