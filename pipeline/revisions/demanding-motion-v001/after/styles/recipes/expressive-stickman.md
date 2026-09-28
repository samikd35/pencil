# Expressive stickman

Simple line figures with expressive poses and clear silhouettes.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[Animation vs. Water - #TeamWater](https://www.youtube.com/watch?v=d_uDE3cD_Xg) — Artwork: Alan Becker.

One large, clearly posed orange stick figure dominates a bright, uncluttered story setting. It stays legible at menu size and shows how much action a very simple body can communicate.

- Use an unmistakable line of action and clean negative space between limbs.
- Keep round heads, continuous limb thickness and smooth joins consistent across the figure.
- Separate the character from the environment with strong color contrast and a clear visual focal point.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use a narrow spine and thin continuous limbs. Keep the circular face and simple features; use gesture and timing for expression.
- Surface: Native emission colors and clean outlines; no texture dependency.
- Presentation: Use the current film’s authored shot layout and timing.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "stick", "finish": "flat", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style expressive-stickman --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

Before detailed animation, apply the [demanding-motion review](../construction.md#demanding-motion-before-detailed-animation) using the current production’s strongest action. Check bent limbs, silhouettes, contacts and continuous joins in motion; a still or small gesture cannot establish suitability for running or jumping.

## Limits and evidence

New props and actions still need contact checks. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/expressive-stickman.png) · [Catalogue](../gallery.html)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/expressive-stickman/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/expressive-stickman/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/expressive-stickman/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/expressive-stickman/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion has not been visually reviewed for this preset.
