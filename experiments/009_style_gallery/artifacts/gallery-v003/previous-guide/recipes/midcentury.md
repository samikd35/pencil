# Midcentury / UPA-inspired

Angular design, a restrained palette and playful graphic scenery.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Build this treatment

- Character: Use a trapezoid torso, asymmetric angular head and muted teal/coral palette. Add sparse offset geometric scenery; author readable held poses when needed.
- Surface: Native emission colors and clean outlines; no texture dependency.
- Presentation: Use the current film’s authored shot layout and timing.

## Executable recipe

`build_samples.py:apply_style` consumes `{"design": "angular", "finish": "flat", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style midcentury --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then load `resolve` and these settings in its own builder. Copy the mechanism, not the benchmark's story or fixed timeline. Adjust proportions, palette, eyes, hair and outfit to the current brief; new identity artwork needs its own review.

## Limits and evidence

The visual treatment alone does not reproduce UPA movement or redraws. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[Sample image](../samples/midcentury.png) · [Catalogue](../gallery.html)

References: [Primary source](https://www.moma.org/docs/press_archives/1959/releases/MOMA_1955_0074_57.pdf)

Verified sample evidence: [Native project](../../../experiments/009_style_gallery/artifacts/gallery-v001/midcentury/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v001/midcentury/checks.json). Motion not yet reviewed for this new preset.
