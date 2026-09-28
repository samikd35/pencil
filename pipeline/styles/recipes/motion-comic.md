# Motion-comic presentation

Cinematic illustrated poses with selective animation and panel-like staging.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[Sigma Origin Story — illustrated key image](https://www.youtube.com/watch?v=onplsJSdp4A) — Sigma Origin Story · Blizzard Entertainment.

A polished cinematic illustrated frame with a strong central figure, readable hands, controlled light and layered debris. It represents illustrated-film / motion-comic presentation, not proof that our rig reproduces its full anatomy or animation.

- One strong focal pose with readable face and hands against a controlled background.
- Deliberate shape-based shadows and highlights that support volume without muddying the silhouette.
- Foreground and background elements composed to create depth while keeping the story action clear.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use one filled torso/hips shape, driven sleeve and shorts subcurves, a modest native head, solid hair and a simple collar/pocket.
- Surface: Native emission colors and clean outlines; no texture dependency.
- Presentation: Add native panel borders, a caption and an action word. In a film, author panel changes and selective holds; the sample alone only establishes the layout.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "human", "finish": "flat", "presentation": "comic"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style motion-comic --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

## Limits and evidence

Rich illustration, pose replacements and panel timing are authored per shot; a still cannot establish their movement. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/motion-comic.png) · [Catalogue](../gallery.html)

References: [Primary source](https://www.realmotioncomics.com/)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/motion-comic/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/motion-comic/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/motion-comic/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/motion-comic/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion has not been visually reviewed for this preset.
