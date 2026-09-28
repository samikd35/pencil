# Flat vector cartoon

Crisp shapes, controlled color and clean graphic detail.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[Loneliness — Managing facts and feelings](https://kurzgesagt.org/projects/loneliness) — Artwork: Kurzgesagt – In a Nutshell.

The clean character montage shows coordinated heads and bodies, different proportions and clear hand-to-prop relationships using economical flat shapes. Saturated color grouping keeps the image readable without heavy outlines.

- Build a coherent silhouette from economical flat shapes with clean, continuous edges.
- Use a controlled palette and value separation so hands, faces and props remain readable.
- Preserve character-specific hair, proportions and expressions while simplifying small detail.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use one filled torso/hips shape, driven sleeve and shorts subcurves, a modest native head, solid hair and a simple collar/pocket.
- Surface: Native emission colors and clean outlines; no texture dependency.
- Presentation: Use the current film’s authored shot layout and timing.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "human", "finish": "flat", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style flat-vector --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

## Limits and evidence

Turns and foreshortening need authored views. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/flat-vector.png) · [Catalogue](../gallery.html)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/flat-vector/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/flat-vector/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/flat-vector/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/flat-vector/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion has not been visually reviewed for this preset.
