# Textured storybook

Soft colors, expressive drawn figures and painterly texture.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[We’re Going on a Bear Hunt — ident artwork](https://www.lupusfilms.com/commercialsandidents/were-going-on-a-bear-hunt-ident) — We’re Going on a Bear Hunt · Lupus Films.

This studio artwork puts expressive drawn people into a complete, textured landscape. It shows the intended finish at scene scale, including atmosphere and staging, rather than only a textured character.

- Visible pencil and watercolor-like grain that remains consistent across figures and scenery.
- Soft, harmonious color and value separation between the figures, foreground and distant landscape.
- Readable running poses and integrated ground contact inside a complete illustrated composition.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use one filled torso/hips shape, driven sleeve and shorts subcurves, a modest native head, solid hair and a simple collar/pocket.
- Surface: Use a soft palette and low-contrast Noise-to-ColorRamp emission materials across the character. Check grain deformation before using stronger texture.
- Presentation: Use the current film’s authored shot layout and timing.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "human", "finish": "storybook", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style storybook --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

## Limits and evidence

Designed textures and backgrounds need art direction; check their stability through bends and contacts. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/storybook.png) · [Catalogue](../gallery.html)

References: [Primary source](https://moho.lostmarble.com/pages/features)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/storybook/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/storybook/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/storybook/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/storybook/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion has not been visually reviewed for this preset.
