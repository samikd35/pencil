# Whiteboard / chalkboard look

Marker drawings, expressive diagrams and brief handwritten labels.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[RSA Animate: Changing Education Paradigms](https://www.youtube.com/watch?v=zDZFcDGpL4U) — RSA Animate · Royal Society of Arts / Cognitive.

The official RSA upload uses confident marker drawings, small expressive people, handwritten explanations and one accent color. Text is part of this visual treatment, not thumbnail decoration to reproduce.

- Confident dark contour lines on a clean white field, with readable small faces and hands.
- One restrained accent color that groups ideas and directs attention.
- Characters, diagrams and short labels arranged with clear spacing and an obvious reading order.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use a narrow spine and thin continuous limbs. Keep the circular face and simple features; use gesture and timing for expression.
- Surface: Use thin black strokes, a pure white native board and diagram labels/arrows. The current preset demonstrates drawing appearance, without a reveal pass.
- Presentation: Use the current film’s authored shot layout and timing.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "stick", "finish": "whiteboard", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style whiteboard --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

## Limits and evidence

The benchmark establishes board-like drawing; progressive reveal and chalk grain need authored additions. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/whiteboard.png) · [Catalogue](../gallery.html)

References: [Primary source](https://www.adobe.com/creativecloud/video/discover/whiteboard-animation.html)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/whiteboard/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/whiteboard/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/whiteboard/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/whiteboard/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion has not been visually reviewed for this preset.
