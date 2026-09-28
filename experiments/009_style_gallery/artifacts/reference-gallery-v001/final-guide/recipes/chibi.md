# Chibi / super-deformed

Oversized heads, compact bodies and bold expressions.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[Chibi Tiny Tales — The Cheetah Girls: As Told By Chibi](https://disneynow.com/video/60136741-427a-4868-bd20-c831e708ae06/playlist/PL554083840) — Chibi Tiny Tales · Disney.

Four complete characters show the large-head/small-body construction clearly, with distinct hair, bright expressions, recognizable clothing and several readable hand gestures. The actual artwork is clean and title-free.

- Keep oversized heads and eyes balanced with compact bodies, short limbs and simple shoes.
- Use distinct hair masses, brows and mouth shapes so each character has a clear identity and emotion.
- Draw clean cuffs, continuous clothing joins and visible hand silhouettes in both raised and resting poses.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use a head roughly as wide as the torso is tall, a shorter torso and lowered derived pelvis. Keep the clearance constraint active through crouches and stumbles.
- Surface: Native emission colors and clean outlines; no texture dependency.
- Presentation: Use the current film’s authored shot layout and timing.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "chibi", "finish": "flat", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style chibi --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

## Limits and evidence

Compact hips need foot-clearance constraints and action-specific reach tuning. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/chibi.png) · [Catalogue](../gallery.html)

References: [Primary source](https://www.clipstudio.net/how-to-draw/archives/155423)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/chibi/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/chibi/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/chibi/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/chibi/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. [Corrected hand motion proof and review](../../../experiments/009_style_gallery/artifacts/hand-layer-v006/chibi/review.md).

## Motion-proof lesson

Compact pelvis remains above the feet through push and recovery; native neck and waist remain connected. Long reaches intentionally stretch the arms. Raised arms briefly pass behind the enlarged head; new poses need the same overlap review.

[Actual review](../../../experiments/009_style_gallery/proofs/workflow-v001/chibi/animatic-v001/review.md) · [Encoded proof](../../../experiments/009_style_gallery/proofs/workflow-v001/chibi/animatic-v001/animatic-with-sound.mp4) · [Successive-frame evidence](../../../experiments/009_style_gallery/proofs/workflow-v001/chibi/animatic-v001/release-successive-frames.png). This is a limited benchmark, not a blanket promise for every action.
