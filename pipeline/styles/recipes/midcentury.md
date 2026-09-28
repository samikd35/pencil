# Midcentury / UPA-inspired

Graphic proportions, playful shapes and economical color.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[Toot, Whistle, Plunk and Boom (1953) — musicians](https://d23.com/this-day/toot-whistle-plunk-and-boom-wins-oscar-for-best-short-subjectcartoon/) — Toot, Whistle, Plunk and Boom (1953) · Disney / D23.

An unmistakable midcentury modernist animation scene: elongated angular musicians, delicate economical lines, flat pink/purple shapes and playful abstract instruments. D23 explicitly describes this Disney film as using the UPA style; it is not itself a UPA production.

- Playful exaggerated silhouettes built from long angular limbs and bold flat head and costume shapes.
- Economical fine contour and decorative lines over a restrained, harmonious pink-purple palette.
- Characters, instruments and scenery share stylized geometry and deliberate negative space.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use a trapezoid torso, asymmetric angular head and muted teal/coral palette. Add sparse offset geometric scenery; author readable held poses when needed.
- Surface: Native emission colors and clean outlines; no texture dependency.
- Presentation: Use the current film’s authored shot layout and timing.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "angular", "finish": "flat", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style midcentury --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

## Limits and evidence

The visual treatment alone does not reproduce UPA movement or redraws. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/midcentury.png) · [Catalogue](../gallery.html)

References: [Primary source](https://www.moma.org/docs/press_archives/1959/releases/MOMA_1955_0074_57.pdf)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/midcentury/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/midcentury/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/midcentury/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/midcentury/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion has not been visually reviewed for this preset.
