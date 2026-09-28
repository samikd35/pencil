# Retro pixelated look

Crisp pixel clusters, compact palettes and readable silhouettes.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[Simpsons Pixels](https://www.ivandixon.com/) — Simpsons Pixels · Ivan Dixon and Paul Robertson.

The creators’ pixel animation uses deliberate block shapes, a limited palette and clear silhouettes, with a fully designed living-room environment. This is pixel design, not simply a blur or mosaic filter.

- Consistent, crisp square pixel edges with no smeared or antialiased contours.
- Recognizable character silhouettes and faces using economical clusters of color.
- Environment, props and figures share the same pixel scale and palette discipline.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use one filled torso/hips shape, driven sleeve and shorts subcurves, a modest native head, solid hair and a simple collar/pocket.
- Surface: Render the same native scene at 100×120 for the portrait (160×90 for the proof) and display with nearest-neighbour scaling. Keep important features several pixels wide.
- Presentation: Use the current film’s authored shot layout and timing.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "human", "finish": "pixel", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style pixelated --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

## Limits and evidence

Our tested mechanism is low-resolution rendering; deliberate pixel clusters and stable moving edges need design and frame review. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/pixelated.png) · [Catalogue](../gallery.html)

References: [Primary source](https://docs.blender.org/manual/en/latest/compositing/types/creative/pixelate.html)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/pixelated/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/pixelated/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/pixelated/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/pixelated/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion has not been visually reviewed for this preset.
