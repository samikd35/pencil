# Upright animal cartoon

Upright animal characters with distinctive shapes and markings.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[Bluey — Keepy Uppy episode artwork](https://www.bluey.tv/watch/season-1/keepy-uppy/) — Bluey · Ludo Studio / BBC Studios.

A clear upright animal character in a finished room shows how silhouette, ears, muzzle and flat fur patches create identity while hands perform one readable action. The continuous drawing language and controlled scene palette are suitable targets for a simple articulated native character.

- Use the same contour and fill language across head, muzzle, body and paws.
- Establish identity through ear shape, muzzle proportions and a small number of large fur markings.
- Show convincing paw-to-balloon contact and planted feet, with background detail subordinate to the action.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use a fox-colored head with triangular ears, contrasting muzzle and small dark nose on a two-legged clothed body. Ears attach to the head as fixed artwork.
- Surface: Native emission colors and clean outlines; no texture dependency.
- Presentation: Use the current film’s authored shot layout and timing.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "fox", "finish": "flat", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style animal-mascot --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

## Limits and evidence

Upright motion is demonstrated; quadrupeds and complex ear/tail acting need additional controls. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/animal-mascot.png) · [Catalogue](../gallery.html)

References: [Primary source](https://pages.adobe.com/character/en/puppet-maker)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/animal-mascot/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/animal-mascot/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/animal-mascot/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/animal-mascot/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion has not been visually reviewed for this preset.
