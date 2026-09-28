# Animated collage look

Drawn characters mixed with photographic textures and cut-paper shapes.

Read [the shared construction guide](../construction.md) first. Use native curves/flat meshes on simple motion controls; this choice does not require a new armature or Grease Pencil backend.

## Visual quality target

[Charlie and Lola — leaf costume and drawn character designs](https://milkmonitor.me/the-charlie-and-lola-television) — Lauren Child / Milkmonitor Ltd. · Charlie and Lola.

A photographic leaf becomes a costume around an economical drawn face and limbs. This makes mixed-media collage unmistakable while preserving a coherent character and continuous limb connections.

- Photographic texture confined to a clear, deliberately cut silhouette.
- Hand-drawn faces, hair and limbs that retain one consistent visual scale.
- Clean overlaps and readable limb exits where the textured costume meets drawn body parts.

The reference is the design and finish target for the story's own artwork. Compare it with a native film frame at the existing staging checkpoint, then preserve those qualities through the required poses. The linked internal benchmark below documents reusable mechanics.

## Proven construction starting point

These notes describe the internal box-test construction. Adapt the mechanisms and design new artwork to the selected reference and story.

- Character: Use one filled torso/hips shape, driven sleeve and shorts subcurves, a modest native head, solid hair and a simple collar/pocket.
- Surface: Use coordinated Wave-to-ColorRamp print patterns across face, clothing and hair. Native original patterns avoid mismatched pasted artwork; prepare real cutouts separately when requested.
- Presentation: Use the current film’s authored shot layout and timing.

## Reproduce the internal benchmark

`build_samples.py:apply_style` consumes `{"design": "human", "finish": "collage", "presentation": "scene"}`. It reuses the named attachment/curve helpers listed in the shared guide. `patterned` owns surface treatments; `render_sample` owns portrait framing and pixel dimensions. The box benchmark can be reproduced with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --style collage --out NEW_OUTPUT_DIRECTORY
```

For a film, save this option with `pipeline/styles.py select`, then use `resolve` to load its pinned reference, quality targets and construction notes. Design the film's artwork and poses from that target and its own story. Review a finished representative frame beside the reference in the existing staging checkpoint, then check the design through movement.

## Limits and evidence

The benchmark uses procedural patterns; prepare authored cutouts with stable attachment and source records. New combinations or major proportion changes require a focused motion check. Use the catalogue's current evidence links for the exact build, all-frame connection check and any reviewed motion proof; the research source establishes the style, not rig compatibility.

[External quality reference](../samples/collage.png) · [Catalogue](../gallery.html)

References: [Primary source](https://www.domestika.org/en/courses/333-animated-collage-with-adobe-after-effects)

Internal construction evidence (different artwork from the menu reference): [Native guide pose](../../../experiments/009_style_gallery/artifacts/gallery-v003/collage/guide-pose.blend), [guide wrist/framing check](../../../experiments/009_style_gallery/artifacts/gallery-v003/collage/guide-checks.json), [motion benchmark](../../../experiments/009_style_gallery/artifacts/gallery-v003/collage/character.blend), [240-frame connection check](../../../experiments/009_style_gallery/artifacts/gallery-v003/collage/checks.json). The guide uses a separate open-arm still pose; the benchmark retains the original action. Motion references below predate the hand-layer correction; this guide revision is still-only evidence.

## Motion-proof lesson

Character remains connected and the body-local printed scrap stays attached. Wave patterns stretch visibly on bending limbs. Treat these as stylized patterns; use solid or low-contrast limb fills and body-local prints when texture stability matters.

[Actual review](../../../experiments/009_style_gallery/proofs/workflow-v001/collage/animatic-v001/review.md) · [Encoded proof](../../../experiments/009_style_gallery/proofs/workflow-v001/collage/animatic-v001/animatic-with-sound.mp4) · [Successive-frame evidence](../../../experiments/009_style_gallery/proofs/workflow-v001/collage/animatic-v001/release-successive-frames.png). This is a limited benchmark, not a blanket promise for every action.
