# Rubber-hose cartoon

Elastic curved limbs, bold eyes and rounded gloves.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[The Cuphead Show! — Cuphead and King Dice on stage](https://lighthousestudios.ie/work/the-cuphead-show) — The Cuphead Show! · Netflix / Lighthouse Studios / Studio MDHR.

Two complete figures, an open glove gesture and a bent microphone arm make the rounded construction and theatrical pose language immediately clear. The coordinated heads, bodies and textured background demonstrate a finished scene.

- Use flowing limb arcs, rounded shoes and readable glove silhouettes with visible thumbs.
- Keep head, face, torso and clothing in one coherent line and shape language.
- Stage the gesture clearly against a quieter background, with controlled shading and ground contact.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use rounded glove fills, pie-cut pupils, a dark outfit and curved limbs. Keep limb width consistent and avoid angular elbow seams.
- Surface: Native emission colors and clean outlines; no texture dependency.
- Presentation: Use the current film’s authored shot layout and timing.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "hose", "finish": "flat", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style rubber-hose --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

## Limits and evidence

Vintage redraws, smears and extreme squash need extra artwork. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/rubber-hose.png) · [Catalogue](../gallery.html)

References: [Primary source](https://www.adobe.com/uk/creativecloud/animation/discover/rubber-hose-animation.html)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/rubber-hose/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/rubber-hose/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/rubber-hose/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/rubber-hose/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion has not been visually reviewed for this preset.
