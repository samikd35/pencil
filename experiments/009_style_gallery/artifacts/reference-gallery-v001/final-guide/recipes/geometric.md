# Geometric character

Characters built from circles, blocks and simple geometric silhouettes.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[Duggee — arms wide character artwork](https://www.heyduggee.com/characters/duggee/) — Hey Duggee · Studio AKA / BBC Studios.

An uncluttered complete character makes the circular, rounded-rectangle and triangular shape vocabulary explicit. Both hands, cuffs and feet remain visible in the open-arm pose.

- Build a distinctive silhouette from a few deliberate geometric masses.
- Keep flat fills and crisp boundaries consistent, with a restrained family of accent colors.
- Make hands, facial features and clothing symbols large enough to read at small viewing sizes.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use polygonal body and rectangular head with small eyes. Place attachments inside the filled shapes so they remain hidden in bends.
- Surface: Native emission colors and clean outlines; no texture dependency.
- Presentation: Use the current film’s authored shot layout and timing.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "geometric", "finish": "flat", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style geometric --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

## Limits and evidence

Sharp shapes still need overlap and pivot checks. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/geometric.png) · [Catalogue](../gallery.html)

References: [Primary source](https://pages.adobe.com/character/en/puppet-maker)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/geometric/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/geometric/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/geometric/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/geometric/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion has not been visually reviewed for this preset.
