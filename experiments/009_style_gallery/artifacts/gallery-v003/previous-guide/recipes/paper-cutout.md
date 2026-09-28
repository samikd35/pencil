# Paper-cutout look

Layered colored shapes with offset paper shadows.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Build this treatment

- Character: Use one filled torso/hips shape, driven sleeve and shorts subcurves, a modest native head, solid hair and a simple collar/pocket.
- Surface: Use subdued procedural paper grain and small offset duplicates behind head shapes only; body parts share one outline to prevent shadow seams. Shadows are graphic offsets, not a simulated lighting system.
- Presentation: Use the current film’s authored shot layout and timing.

## Executable recipe

`build_samples.py:apply_style` consumes `{"design": "human", "finish": "paper", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style paper-cutout --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then load `resolve` and these settings in its own builder. Copy the mechanism, not the benchmark's story or fixed timeline. Adjust proportions, palette, eyes, hair and outfit to the current brief; new identity artwork needs its own review.

## Limits and evidence

Elastic limbs remain continuous; rigid hinged cutout limbs need a separate variant. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[Sample image](../samples/paper-cutout.png) · [Catalogue](../gallery.html)

References: [Primary source](https://www.adobe.com/uk/creativecloud/animation/discover/cut-out-animation.html)

Verified sample evidence: [Native project](../../../experiments/009_style_gallery/artifacts/gallery-v002/paper-cutout/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v002/paper-cutout/checks.json). A representative motion proof is now reviewed; see below.

## Motion-proof lesson

Removing separate body-part shadows eliminated the waist seam. Paper backing is scene decoration; the character moves off it during the benchmark. Continuous limbs and native head stay connected.

[Actual review](../../../experiments/009_style_gallery/proofs/workflow-v001/paper-cutout/animatic-v001/review.md) · [Encoded proof](../../../experiments/009_style_gallery/proofs/workflow-v001/paper-cutout/animatic-v001/animatic-with-sound.mp4) · [Successive-frame evidence](../../../experiments/009_style_gallery/proofs/workflow-v001/paper-cutout/animatic-v001/release-successive-frames.png). This is a limited benchmark, not a blanket promise for every action.
