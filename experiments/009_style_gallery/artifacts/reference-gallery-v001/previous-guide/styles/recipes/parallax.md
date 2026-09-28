# Layered 2.5D / parallax

Flat character among separated foreground and background layers.

This card demonstrates an environment treatment. It can be adapted to other character styles, including stickman, caricature, chibi and mascots. Keep the chosen character's construction and add layered staging; review the combination in the actual shot. The current selector records one preset, so additional environment choices belong in the film brief and authored scene. New camera angles are not supplied by this treatment.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Build this treatment

- Character: Use one filled torso/hips shape, driven sleeve and shorts subcurves, a modest native head, solid hair and a simple collar/pocket.
- Surface: Native emission colors and clean outlines; no texture dependency.
- Presentation: Place native foreground/background shapes on separate planes and key their horizontal movement at different rates (.7 versus .15/.2 in the benchmark). Orthographic Z separation alone does not create parallax.

## Executable recipe

`build_samples.py:apply_style` consumes `{"design": "human", "finish": "flat", "presentation": "parallax"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style parallax --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then load `resolve` and these settings in its own builder. Copy the mechanism, not the benchmark's story or fixed timeline. Adjust proportions, palette, eyes, hair and outfit to the current brief; new identity artwork needs its own review.

## Limits and evidence

Depth comes from layered motion; it does not create new character viewing angles. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[Sample image](../samples/parallax.png) · [Catalogue](../gallery.html)

References: [Primary source](https://helpx.adobe.com/animate/desktop/using/layer-depth.html)

Verified sample evidence: [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/parallax/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/parallax/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/parallax/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/parallax/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion references below predate the hand-layer correction; this guide revision is still-only evidence.

## Motion-proof lesson

Foreground and background trees move at different rates while the character and box retain source motion. Staging remains readable. Camera perspective and new character views are not established.

[Actual review](../../../experiments/009_style_gallery/proofs/workflow-v001/parallax/animatic-v001/review.md) · [Encoded proof](../../../experiments/009_style_gallery/proofs/workflow-v001/parallax/animatic-v001/animatic-with-sound.mp4) · [Successive-frame evidence](../../../experiments/009_style_gallery/proofs/workflow-v001/parallax/animatic-v001/release-successive-frames.png). This is a limited benchmark, not a blanket promise for every action.
