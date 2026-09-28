# Animated collage look

Coordinated patterned cutouts across the whole character.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Build this treatment

- Character: Use one filled torso/hips shape, driven sleeve and shorts subcurves, a modest native head, solid hair and a simple collar/pocket.
- Surface: Use coordinated Wave-to-ColorRamp print patterns across face, clothing and hair. Native original patterns avoid mismatched pasted artwork; prepare real cutouts separately when requested.
- Presentation: Use the current film’s authored shot layout and timing.

## Executable recipe

`build_samples.py:apply_style` consumes `{"design": "human", "finish": "collage", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style collage --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then load `resolve` and these settings in its own builder. Copy the mechanism, not the benchmark's story or fixed timeline. Adjust proportions, palette, eyes, hair and outfit to the current brief; new identity artwork needs its own review.

## Limits and evidence

The sample uses original procedural patterns; imported photography needs preparation and source records. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[Sample image](../samples/collage.png) · [Catalogue](../gallery.html)

References: [Primary source](https://www.domestika.org/en/courses/333-animated-collage-with-adobe-after-effects)

Verified sample evidence: [Native project](../../../experiments/009_style_gallery/artifacts/gallery-v002/collage/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v002/collage/checks.json). A representative motion proof is now reviewed; see below.

## Motion-proof lesson

Character remains connected and the body-local printed scrap stays attached. Wave patterns stretch visibly on bending limbs. Treat these as stylized patterns; use solid or low-contrast limb fills and body-local prints when texture stability matters.

[Actual review](../../../experiments/009_style_gallery/proofs/workflow-v001/collage/animatic-v001/review.md) · [Encoded proof](../../../experiments/009_style_gallery/proofs/workflow-v001/collage/animatic-v001/animatic-with-sound.mp4) · [Successive-frame evidence](../../../experiments/009_style_gallery/proofs/workflow-v001/collage/animatic-v001/release-successive-frames.png). This is a limited benchmark, not a blanket promise for every action.
