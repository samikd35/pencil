# Paper-cutout look

Layered cut-paper shapes, tactile texture and readable overlaps.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[The Old Red Rooster — rooster on the barn](https://sundstedt.co.uk/blog/portfolio/the-old-red-rooster-animated-music-video/) — The Old Red Rooster · Anders Sundstedt / Sundstedt Animation.

The close, readable rooster shows separate feather shapes, painted texture and shallow layered scenery. The studio explicitly describes digitally illustrated paper-cutout styling, so the target is the paper appearance and art direction, not a requirement to photograph physical paper.

- Build a readable character from layered cut shapes, with feather or clothing detail following the form.
- Use restrained painted texture and shallow edge shadows consistently across character and scenery.
- Keep feet visibly on the supporting surface and use warm/cool color contrast to separate the character from the set.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use one filled torso/hips shape, driven sleeve and shorts subcurves, a modest native head, solid hair and a simple collar/pocket.
- Surface: Use subdued procedural paper grain and small offset duplicates behind head shapes only; body parts share one outline to prevent shadow seams. Shadows are graphic offsets, not a simulated lighting system.
- Presentation: Use the current film’s authored shot layout and timing.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "human", "finish": "paper", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style paper-cutout --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

## Limits and evidence

Elastic limbs remain continuous; rigid hinged cutout limbs need a separate variant. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/paper-cutout.png) · [Catalogue](../gallery.html)

References: [Primary source](https://www.adobe.com/uk/creativecloud/animation/discover/cut-out-animation.html)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/paper-cutout/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/paper-cutout/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/paper-cutout/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/paper-cutout/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion references below predate the hand-layer correction; this guide revision is still-only evidence.

## Motion-proof lesson

Removing separate body-part shadows eliminated the waist seam. Paper backing is scene decoration; the character moves off it during the benchmark. Continuous limbs and native head stay connected.

[Actual review](../../../experiments/009_style_gallery/proofs/workflow-v001/paper-cutout/animatic-v001/review.md) · [Encoded proof](../../../experiments/009_style_gallery/proofs/workflow-v001/paper-cutout/animatic-v001/animatic-with-sound.mp4) · [Successive-frame evidence](../../../experiments/009_style_gallery/proofs/workflow-v001/paper-cutout/animatic-v001/release-successive-frames.png). This is a limited benchmark, not a blanket promise for every action.
