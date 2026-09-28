# Character Asset prototype

> PROTOTYPE — throw away after the Character Asset question is answered.

## Question

Can an approved Character Model Sheet become a reusable, part-structured
Grease Pencil Character Asset with stable identity, useful controls, and only
the alternate drawings required by the v1 reference Shot?

## Result

The Creator approved continuing with
[`simple-character-model-sheet.png`](../../../data/references/larry/model_sheet/simple-character-model-sheet.png).
The front view supplies the editable cutout and the right-profile view supplies
the minimum orientation alternate. A small remaining joint imperfection is an
accepted prototype limitation, not a claim of perfect deformation.

The technical run currently detects two views, creates 11 front-view semantic
parts and 16 named controls, and imports native Grease Pencil objects. Each arm
is traced once as a continuous drawing and bent with a two-bone Grease Pencil
armature instead of rotating independently traced cutouts. The review artifact
shows a -20 / 0 / +20 degree elbow sweep. Automated checks confirmed only
structure and movement; the Creator supplied the recorded visual approval.

The joint design is the applied test for the research gate recorded in
[`docs/research/character-joint-deformation.md`](../../../docs/research/character-joint-deformation.md).

## Source and preparation

The reference is the downloaded CC0 Kenney Toon Characters image at
[`kenney-male-person-idle.png`](../../../data/references/larry/source/kenney-male-person-idle.png); its
source and licence are recorded in
[`kenney-toon-character-source.md`](../../../data/references/larry/source/kenney-toon-character-source.md).

The raw generated two-view artwork is retained at
[`simple-character-model-sheet-input.png`](../../../data/references/larry/model_sheet/simple-character-model-sheet-input.png).
On every run, the preparation step removes only pale, low-chroma background
pixels connected to the outside canvas, writes alpha 0 there and alpha 255
inside the figures, flattens the artwork to 15 visible colors, and verifies the
two figure components. This preserves enclosed white details such as the eyes
and shirt and makes the successful alpha technique reusable.

## Final generation prompt

The downloaded cartoon was used as the character reference for exactly two
matching full-body drawings: a straight front view and an exact right-facing
profile. Both use a neutral A-pose, separated arms and legs, a clearly visible
nose, simple one-thumb mitten hands, thick dark outlines, and flat colors with
no logos, props, text, extra poses, lighting, texture, or shadows.

## Run

From the repository root:

```sh
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/prototype_character_asset.py
```

Generated Blender, render, vector, and validation artifacts are written under
the ignored `artifacts/experiment_002_hybrid_character_motion/` directory.

## Rejected animation-ready v2 wave proof

V2 is negative evidence, not an animation-ready asset. It rotates one
contaminated whole-arm SVG around a pivot 140.6 pixels from the annotated
attachment, supplies no real shoulder/elbow/wrist chain, and adds zero hidden
art pixels. The Creator rejected its visible result.

Run:

```sh
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/prototype_character_asset_v2.py
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/test_character_asset_v2.py
```

The first command can reproduce the rejected artifact. The second locks the
causal rejection evidence; it no longer grants a pass.

## Rejected quality-first v3 wave candidate

V3 preserves the approved full artwork as one Grease Pencil deformation
domain instead of cutting at the shoulder. It uses separate shoulder, elbow,
and wrist bones, localized continuous weights, a pinned cuff correction, real
hidden shoulder artwork, a 33-pose dense sweep, genuine wrist and retiming
edits, and a linked second-scene reuse proof.

The Creator rejected the render because foreign/background-looking shapes
remain visible around the moving arm and hand. The root cause is semantic, not
frame rate: v3 imports the full character as one object and assigns weights by
a coordinate polygon. That polygon overlaps hair, ear, head, and negative-space
boundaries, so the rig cannot prove that every moved stroke belongs to the arm.
The connected-component check only proves that pixels touch; it does not prove
correct ownership, silhouette, or occlusion.

Run:

```sh
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/prototype_character_asset_v3.py
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/test_motion_representation_quality.py artifacts/experiment_002_hybrid_character_motion/character_asset/animation-ready-v3/validation.json
```

The automatic gate rejects invalid representation, controls, hidden artwork,
motion range, dense-sweep structure, non-local revisions, failed reuse, and any
result without explicit Creator visual approval. V3 is intentionally red.

## V4 drawing-led wave — static semantic gate

V4 reuses the approved pose drawings but never interpolates their full-body
pixels. One three-quarter rest drawing supplies the immutable fixed character.
Each state uses committed semantic masks for hand, forearm, and sleeve ownership;
runtime coordinate and color inference is forbidden. A separate hidden shoulder
underlap sits behind the immutable head, and the fixed head/hair occluder is
always composited in front.

The static gate rejects any arm-owned pixel inside the fixed head, any changed
source-arm pixel, any missing source foreground inside the shoulder corridor,
any undeclared foreground pixel, or any disconnected character state. More
importantly, it compares every RGBA pixel outside the union of the four approved
arm modules with the canonical drawing. This locks the head, torso, hips, legs,
other arm, and background as one rule instead of protecting them piecemeal.

Run:

```sh
./.venv/bin/python \
  experiments/002_hybrid_character_motion/character_asset/prototype_character_asset_v4.py
```

The ignored `artifacts/experiment_002_hybrid_character_motion/character_asset/animation-ready-v4-static/` directory contains the four
static composites, semantic parts, ownership passes, a full review sheet, a 4x
shoulder sheet, a full-body lock map, and the validation manifest.

## V4 drawing-exposure timing proof

After static approval, the next run vectorizes the approved semantic parts,
imports them as native Grease Pencil objects, and keys eight held-drawing
exposure ranges across 36 frames at 24 fps. The fixed-body and fixed-head
collections have no animation or deformation. Three isolated fixed renders
must have the same decoded-pixel hash, and each held arm state must have only
one decoded-pixel hash. Blender's compositor combines separate fixed-body, arm,
and front-head view layers in explicit depth order. An independently authored
motion-envelope mask—not a mask inferred from the rendered pose—requires every
pixel outside that envelope to match frame 1 in all 36 final Blender frames.
The validator also rejects empty character frames.

Run:

```sh
./.venv/bin/python \
  experiments/002_hybrid_character_motion/character_asset/prototype_character_asset_v4_motion.py
```

The ignored `artifacts/experiment_002_hybrid_character_motion/character_asset/animation-ready-v4-motion/` directory contains the native
Grease Pencil `.blend`, all 36 alpha renders, a white-background MP4 and GIF,
the exposure contact sheet, fixed-body diagnostic renders, vector sources, and
validation. This is a timing proof only; it deliberately does not pretend that
four held drawings are smooth in-between animation.

## V4 bounded editability proof

The off-timeline proof samples a semantically isolated forearm-and-hand interval
at 33 positions, saves a hand-only wrist edit, and retimes the first A/B exposure
boundary without changing drawing geometry. Locked pixels remain unchanged and
every sweep frame remains one connected character. This is a certified small
interval, not a claim that large silhouette changes can be rigged; those still
use approved drawing substitutions.

```sh
./.venv/bin/python \
  experiments/002_hybrid_character_motion/character_asset/prototype_character_asset_v4_editability.py
```

Its artifacts are under
`artifacts/experiment_002_hybrid_character_motion/character_asset/animation-ready-v4-editability/`.

## V5 semantic-topology correction

The motion audit invalidated V4 as an animation-ready source: its sleeve masks
owned fixed torso pixels, while the rest mask left 453 arm pixels in the fixed
layer. V5 preserves those files as negative evidence and rebuilds ownership
with explicit shoulder seams, a completed fixed torso underlap, one canonical
arm topology, bounded joint-control disks, and a mesh rasterizer that rejects
folds and internal alpha holes.

Run the complete candidate gate from the repository root:

```sh
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/prepare_semantic_ownership_v5.py
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/prototype_character_asset_v5.py
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/prototype_semantic_interval_v5.py
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/test_semantic_interval_v5.py
```

Generated review media and validation are under
`artifacts/experiment_002_hybrid_character_motion/character_asset/semantic-2_5d-v5/`.
The automatic gates pass, but the candidate remains pending Creator visual
review and does not resolve Ticket 04 yet.

## V6 graph-first restart from the original source

V6 restarts from the untouched 192 x 256 Kenney Larry image. It does not reuse
V2-V5 masks, meshes, or motion geometry. The first gate generates four clean
front-view pose candidates, locks both source hashes, verifies genuine alpha,
isolates the four figures, removes only 57 disconnected alpha specks, and
normalizes each pose around the stable trousers and ground line.

Run:

```sh
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/prepare_graph_motion_v6.py
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/test_graph_motion_v6_source.py
```

The review packet is written to
`artifacts/experiment_002_hybrid_character_motion/character_asset/graph-motion-v6/source-preparation/v6-key-pose-review.png`.
Its current state is `awaiting_creator_key_pose_review`. No segmentation,
stroke correspondence, TPS deformation, or Blender compilation may begin
until this pose intent is explicitly approved.

The Creator approved the identity and four-pose intent on 2026-09-04. Gate 2
then builds committed pose-specific ownership masks, one neutral fixed core, a
separate fixed head-front occluder, a bounded hidden shoulder underlap, and one
independent closed contour graph per arm pose:

```sh
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/prepare_semantic_graph_v6.py
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/test_semantic_graph_v6.py
```

The first Gate 2 run was rejected automatically because the breakdown mask
captured a disconnected ear fragment. Visual review then found orange torso
contamination and an oversized visible underlap. The corrected run removes
590-1,250 connected torso pixels per pose through an explicit seeded semantic
region and removes one disconnected 71-pixel fixed fragment. Every arm owner
is now one closed, hole-free surface with zero protected head-core pixels and
at least 355 hidden-overlap pixels. Graph correspondence is intentionally
`not_yet_established`, and TPS remains disabled pending Creator review.

Gate 2 was approved on 2026-09-04. Gate 3 uses ten named contour landmarks to
resample the compatible raised-arm poses into one persistent graph with
102 node IDs and 102 edge IDs. Eight shoulder-attachment edges close the fill
domain but are marked non-rendering. All three graphs have zero
self-intersections and reproduce their approved silhouettes at 0.988-0.991
IoU.

```sh
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/build_graph_correspondence_v6.py
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/test_graph_correspondence_v6.py
```

The Creator approved the raised-arm correspondence and an authored hand-turn
key. The hand-turn key has two interval-local parameterizations over the same
visible contour: one receives the neutral arm and the other enters the raised
sequence. This records the thumb visibility turn without reflecting the hand,
and the rendered key is identical at the parameterization switch.

Gate 4 renders the first 13-frame motion proof:

```sh
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/prototype_graph_motion_v6.py
./.venv/bin/python experiments/002_hybrid_character_motion/character_asset/test_graph_motion_v6.py
```

The proof uses minimum-jerk timing, TPS coarse motion from ten semantic
landmarks, and an exact target-contour correction over the 102-node graph.
Graph alpha and visible edges—not raster interpolation—own the silhouette.
All 13 frames are unique, retain at least 409 shoulder-overlap pixels, have no
graph self-intersections, and change zero pixels outside the motion envelope.
These are rejection filters only; Creator motion review is pending.
