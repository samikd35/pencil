# Doodle / sketch

Loose ink lines and restrained hatching on paper.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Build this treatment

- Character: Use one filled torso/hips shape, driven sleeve and shorts subcurves, a modest native head, solid hair and a simple collar/pocket.
- Surface: Use cream fills, sparse ink, fixed offset contour echoes and body-local hatch strokes. Do not randomize every frame.
- Presentation: Use the current film’s authored shot layout and timing.

## Executable recipe

`build_samples.py:apply_style` consumes `{"design": "human", "finish": "doodle", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style doodle --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then load `resolve` and these settings in its own builder. Copy the mechanism, not the benchmark's story or fixed timeline. Adjust proportions, palette, eyes, hair and outfit to the current brief; new identity artwork needs its own review.

## Limits and evidence

The sample has fixed line irregularity; temporal line boil is not implemented. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[Sample image](../samples/doodle.png) · [Catalogue](../gallery.html)

References: [Primary source](https://docs.toonboom.com/help/harmony-25/premium/reference/node/filter/animate-pencil-line-texture-node.html)

Verified sample evidence: [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/doodle/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/doodle/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/doodle/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/doodle/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion has not been visually reviewed for this preset.
