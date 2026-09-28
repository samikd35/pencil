# Doodle / sketch

Expressive ink contours and deliberately sparse detail.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[Simon’s Cat — Cat Man Do featured artwork](https://simonscat.com/watch) — Simon’s Cat · Simon Tofield / Simon’s Cat Ltd..

The official Watch page’s large, clean artwork shows expressive line drawing with readable paw-to-cloth contact. It is more useful at menu scale than a four-panel comic strip or the small YouTube thumbnail. The small creator badge is preserved.

- Use economical, lively contours with controlled irregularity and consistent visual weight.
- Make gaze, mouth and body posture communicate the action without color or extra facial detail.
- Keep the hand or paw contact legible and preserve open white space around the active silhouette.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use one filled torso/hips shape, driven sleeve and shorts subcurves, a modest native head, solid hair and a simple collar/pocket.
- Surface: Use cream fills, sparse ink, fixed offset contour echoes and body-local hatch strokes. Do not randomize every frame.
- Presentation: Use the current film’s authored shot layout and timing.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "human", "finish": "doodle", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style doodle --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

## Limits and evidence

The benchmark uses fixed line irregularity; animated line boil and additional character anatomy need a proof. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/doodle.png) · [Catalogue](../gallery.html)

References: [Primary source](https://docs.toonboom.com/help/harmony-25/premium/reference/node/filter/animate-pencil-line-texture-node.html)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/doodle/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/doodle/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/doodle/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/doodle/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion has not been visually reviewed for this preset.
