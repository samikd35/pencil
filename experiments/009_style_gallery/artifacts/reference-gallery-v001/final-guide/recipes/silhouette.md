# Silhouette / shadow

Dark cut silhouettes, negative space and graphic scenery.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[Princes et princesses — queen with hourglass](https://www.gebekafilms.com/fiches-films/princes-et-princesses/) — Princes et princesses · Michel Ocelot / Gebeka Films.

A sharply readable profile, crown, bent arms and held hourglass show how a black silhouette can carry character and action. Fine ornamental scenery and a luminous magenta background set an ambitious finish target while preserving simple articulated posing.

- Make identity readable through profile, crown and posture before adding any internal detail.
- Protect negative-space gaps around arms, torso and the held prop so contact remains clear.
- Use strong foreground/background value contrast; keep decorative cutwork from merging into the acting silhouette.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use one filled torso/hips shape, driven sleeve and shorts subcurves, a modest native head, solid hair and a simple collar/pocket.
- Surface: Use the same dark fill for head, body and limbs and omit internal facial details. Review every limb overlap against a light background.
- Presentation: Use the current film’s authored shot layout and timing.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "human", "finish": "silhouette", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style silhouette --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

## Limits and evidence

Overlapping limbs lose detail; stage poses with negative space. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/silhouette.png) · [Catalogue](../gallery.html)

References: [Primary source](https://www.bfi.org.uk/sight-and-sound/features/scissors-make-films-lotte-reiniger-creating-her-magical-animations)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/silhouette/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/silhouette/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/silhouette/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/silhouette/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion has not been visually reviewed for this preset.
