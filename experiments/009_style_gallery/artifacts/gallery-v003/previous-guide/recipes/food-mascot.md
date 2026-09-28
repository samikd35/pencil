# Object / food mascot

A toast character with expressive eyes and simple limbs.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Build this treatment

- Character: Use one rounded toast silhouette and a lighter toasted interior. Place facial features directly on the body and attach simple arms and legs to that shape.
- Surface: Native emission colors and clean outlines; no texture dependency.
- Presentation: Use the current film’s authored shot layout and timing.

## Executable recipe

`build_samples.py:apply_style` consumes `{"design": "toast", "finish": "flat", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style food-mascot --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then load `resolve` and these settings in its own builder. Copy the mechanism, not the benchmark's story or fixed timeline. Adjust proportions, palette, eyes, hair and outfit to the current brief; new identity artwork needs its own review.

## Limits and evidence

Other objects need their own outline and attachment positions. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[Sample image](../samples/food-mascot.png) · [Catalogue](../gallery.html)

References: [Primary source](https://pages.adobe.com/character/en/puppet-maker)

Verified sample evidence: [Native project](../../../experiments/009_style_gallery/artifacts/gallery-v001/food-mascot/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v001/food-mascot/checks.json). A representative motion proof is now reviewed; see below.

## Motion-proof lesson

Face and body remain one toast shape; driven limbs stay attached through reaching and deep lean. This validates the toast biped only, not arbitrary object dimensions.

[Actual review](../../../experiments/009_style_gallery/proofs/workflow-v001/food-mascot/animatic-v001/review.md) · [Encoded proof](../../../experiments/009_style_gallery/proofs/workflow-v001/food-mascot/animatic-v001/animatic-with-sound.mp4) · [Successive-frame evidence](../../../experiments/009_style_gallery/proofs/workflow-v001/food-mascot/animatic-v001/release-successive-frames.png). This is a limited benchmark, not a blanket promise for every action.
