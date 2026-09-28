# Whiteboard / chalkboard look

Minimal line drawing on a clean board.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Build this treatment

- Character: Use a narrow spine and thin continuous limbs. Keep the circular face and simple features; use gesture and timing for expression.
- Surface: Use thin black strokes, a pure white native board and diagram labels/arrows. The current preset demonstrates drawing appearance, without a reveal pass.
- Presentation: Use the current film’s authored shot layout and timing.

## Executable recipe

`build_samples.py:apply_style` consumes `{"design": "stick", "finish": "whiteboard", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style whiteboard --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then load `resolve` and these settings in its own builder. Copy the mechanism, not the benchmark's story or fixed timeline. Adjust proportions, palette, eyes, hair and outfit to the current brief; new identity artwork needs its own review.

## Limits and evidence

This sample establishes whiteboard appearance; drawing reveal and chalk grain are optional untested additions. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[Sample image](../samples/whiteboard.png) · [Catalogue](../gallery.html)

References: [Primary source](https://www.adobe.com/creativecloud/video/discover/whiteboard-animation.html)

Verified sample evidence: [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/whiteboard/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/whiteboard/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/whiteboard/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/whiteboard/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion has not been visually reviewed for this preset.
