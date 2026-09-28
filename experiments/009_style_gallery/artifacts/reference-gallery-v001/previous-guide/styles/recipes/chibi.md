# Chibi / super-deformed

A very large head over a compact body.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Build this treatment

- Character: Use a head roughly as wide as the torso is tall, a shorter torso and lowered derived pelvis. Keep the clearance constraint active through crouches and stumbles.
- Surface: Native emission colors and clean outlines; no texture dependency.
- Presentation: Use the current film’s authored shot layout and timing.

## Executable recipe

`build_samples.py:apply_style` consumes `{"design": "chibi", "finish": "flat", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style chibi --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then load `resolve` and these settings in its own builder. Copy the mechanism, not the benchmark's story or fixed timeline. Adjust proportions, palette, eyes, hair and outfit to the current brief; new identity artwork needs its own review.

## Limits and evidence

Compact hips need foot-clearance constraints and action-specific reach tuning. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[Sample image](../samples/chibi.png) · [Catalogue](../gallery.html)

References: [Primary source](https://www.clipstudio.net/how-to-draw/archives/155423)

Verified sample evidence: [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/chibi/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/chibi/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/chibi/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/chibi/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. [Corrected hand motion proof and review](../../../experiments/009_style_gallery/artifacts/hand-layer-v006/chibi/review.md).

## Motion-proof lesson

Compact pelvis remains above the feet through push and recovery; native neck and waist remain connected. Long reaches intentionally stretch the arms. Raised arms briefly pass behind the enlarged head; new poses need the same overlap review.

[Actual review](../../../experiments/009_style_gallery/proofs/workflow-v001/chibi/animatic-v001/review.md) · [Encoded proof](../../../experiments/009_style_gallery/proofs/workflow-v001/chibi/animatic-v001/animatic-with-sound.mp4) · [Successive-frame evidence](../../../experiments/009_style_gallery/proofs/workflow-v001/chibi/animatic-v001/release-successive-frames.png). This is a limited benchmark, not a blanket promise for every action.
