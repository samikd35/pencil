# Textured storybook

Soft colors and subtle procedural painted grain.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Build this treatment

- Character: Use one filled torso/hips shape, driven sleeve and shorts subcurves, a modest native head, solid hair and a simple collar/pocket.
- Surface: Use a soft palette and low-contrast Noise-to-ColorRamp emission materials across the character. Check grain deformation before using stronger texture.
- Presentation: Use the current film’s authored shot layout and timing.

## Executable recipe

`build_samples.py:apply_style` consumes `{"design": "human", "finish": "storybook", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style storybook --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then load `resolve` and these settings in its own builder. Copy the mechanism, not the benchmark's story or fixed timeline. Adjust proportions, palette, eyes, hair and outfit to the current brief; new identity artwork needs its own review.

## Limits and evidence

Paint appearance only; inspect texture deformation and seams for new poses. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[Sample image](../samples/storybook.png) · [Catalogue](../gallery.html)

References: [Primary source](https://moho.lostmarble.com/pages/features)

Verified sample evidence: [Native project](../../../experiments/009_style_gallery/artifacts/gallery-v001/storybook/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v001/storybook/checks.json). Motion not yet reviewed for this new preset.
