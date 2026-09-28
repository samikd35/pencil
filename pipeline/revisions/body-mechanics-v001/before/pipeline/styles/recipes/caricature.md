# Exaggerated caricature

Exaggerated features and body proportions that make identities readable.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[Ronaldo](https://dribbble.com/shots/27278756-Ronaldo) — Artwork: Fraser Davidson / Cub Studio.

A complete football figure uses exaggerated forearms, shoulders and a large foreground boot while keeping the face, kit and pose in a unified drawing style. The source artwork contains no headline overlay.

- Exaggerate a few distinctive body and facial shapes deliberately instead of enlarging every feature.
- Maintain one coherent outline, color and shading treatment across head, limbs, shirt and shorts.
- Use open hand silhouettes, a strong action pose and clear overlap order around bent limbs.

Its large foreground boot is an authored foreshortened pose, not evidence that our existing rig can freely rotate. Match the caricature finish; plan any such pose as authored artwork.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use an angular enlarged head, stronger hair silhouette, enlarged nose and distinctive jaw. Preserve the coordinated outline thickness across the whole figure.
- Surface: Native emission colors and clean outlines; no texture dependency.
- Presentation: Use the current film’s authored shot layout and timing.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "caricature", "finish": "flat", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style caricature --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

Before detailed animation, apply the [demanding-motion review](../construction.md#demanding-motion-before-detailed-animation) using the current production’s strongest action. Check bent limbs, silhouettes, contacts and continuous joins in motion; a still or small gesture cannot establish suitability for running or jumping.

## Limits and evidence

Each likeness needs designed features and a pose test; foreshortening needs authored artwork. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/caricature.png) · [Catalogue](../gallery.html)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/caricature/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/caricature/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/caricature/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/caricature/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion has not been visually reviewed for this preset.
