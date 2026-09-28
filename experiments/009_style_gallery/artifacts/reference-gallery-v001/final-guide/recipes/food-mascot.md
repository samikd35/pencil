# Object / food mascot

Food or objects with faces, simple limbs and clear personalities.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[The World of Suki-Ya — food mascot ensemble](https://www.ziqun-ak.com/sukiya) — The World of Suki-Ya · Poh Zi Qun (AK) / Big 3 Media.

The character designer’s published artwork shows a coordinated ensemble of lively food mascots with distinct ingredient silhouettes, tiny faces and simple limbs. The central mascot’s bowl and spoon gestures provide clear prop-contact examples. The project page also describes six animated skits, making this a useful art-direction target for animated food characters.

- Keep each ingredient recognizable through its outer shape, with facial features integrated into the same illustration.
- Use consistent rounded limb shapes and simple hands; stage active gestures clearly and show a convincing grip on props.
- Unify the cast with warm brown contours, controlled flat colors and restrained surface details that describe the ingredient.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use one rounded toast silhouette and a lighter toasted interior. Place facial features directly on the body and attach simple arms and legs to that shape.
- Surface: Native emission colors and clean outlines; no texture dependency.
- Presentation: Use the current film’s authored shot layout and timing.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "toast", "finish": "flat", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style food-mascot --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

## Limits and evidence

Different object silhouettes need their own anchors and reach/ground-clearance checks. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/food-mascot.png) · [Catalogue](../gallery.html)

References: [Primary source](https://pages.adobe.com/character/en/puppet-maker)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/food-mascot/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/food-mascot/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/food-mascot/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/food-mascot/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion references below predate the hand-layer correction; this guide revision is still-only evidence.

## Motion-proof lesson

Face and body remain one toast shape; driven limbs stay attached through reaching and deep lean. This validates the toast biped only, not arbitrary object dimensions.

[Actual review](../../../experiments/009_style_gallery/proofs/workflow-v001/food-mascot/animatic-v001/review.md) · [Encoded proof](../../../experiments/009_style_gallery/proofs/workflow-v001/food-mascot/animatic-v001/animatic-with-sound.mp4) · [Successive-frame evidence](../../../experiments/009_style_gallery/proofs/workflow-v001/food-mascot/animatic-v001/release-successive-frames.png). This is a limited benchmark, not a blanket promise for every action.
