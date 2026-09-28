# Repetitive acting: source diagnosis and next-production proposal

Date: 2026-09-22. Scope: investigate and propose; no completed film, rig or pipeline code changed. Read with [benchmark audit](benchmark-audit-v001/report.md) and [primary-source research](acting-source-research.md).

## Conclusion

We overextended a fixed-view illustrated puppet into a general character-performance system. The reusable controls offer useful in-plane deformation, but much of the authored performance remains a variation of the same rest drawing. Fixed face orientation, limited expressive replacements, repeated gesture formulas and weak scene-level evaluation jointly explain the sameness. This is not a claim that the film contains no animation. It contains real articulated animation and action drawings; their range and direction are insufficient for many acting beats.

## Findings grounded in the implementation

The final delivery README records the actual hybrid: fitted illustrated meshes, native rigs/vector geometry, facial controls and matched action drawings. Calling it entirely native Grease Pencil would be false. Neither raster artwork nor Grease Pencil alone determines whether the result acts convincingly.

1. **Head tilt was serving in place of head orientation.** `scripts/reconstruct_defence_v021.py:117` builds the pose from rest landmarks. Its head position is the neck plus a rotated rest vector. `build_gyokeres_proof_v015.py:99` defines that rotation in the drawing's XY plane, retaining Z. This can tilt a face; it cannot construct the nose, far eye, ear and jaw changes of a turn. `build_final_v023.py:31–42` clones the accepted drawing and optionally mirrors its root. A mirrored three-quarter view is not a performed turn. The later `build_clarity_v024.py:16` explicitly imports the same pose/write/step helpers, so this is relevant to the delivered branch, not just an abandoned experiment.

2. **Much of the face is built into the source artwork.** `build_final_v023.py:87–102` adds mouth/teeth shapes and a blink deformation to the fitted head. That function does not supply an independent gaze target, brow acting system or alternate head views. The supporting-character coordinates differ, but the feature mechanism is shared. Other sequences may have additional controls; this diagnosis is bounded to the inspected paths, not a claim that no pupil movement exists anywhere.

3. **Some eye activity is procedural decoration.** `build_final_v023.py:58–63` schedules applicable blinks starting at frame 41, every 83 frames. Mouth articulation and blinking are useful, but neither describes what a character notices or thinks. The common schedule also risks synchronized, unrelated blinks. It is not evidence that every final actor visibly blinks on that schedule, since availability and later revisions matter.

4. **Pose authoring repeatedly returns to the same basis.** The shared pose function starts from rest for each evaluation and varies lean, down, arm angles, hands, head and shift. It is capable of useful movement but has no semantic representation of a thought, intention or interaction partner. Such meaning must be authored outside it. In `build_final_v023.py:295`, Saka and Gabriel are assigned the same celebration arm values and a sinusoidal head change. This is direct evidence of repeated choreography, not merely similar rendering. Reuse of controls was allowed to become reuse of acting.

5. **The ordinary foot mechanism is too limited to be treated as a general gait.** `reconstruct_defence_v021.py:127–132` places the knee along the hip-to-ankle segment plus a fixed lateral offset, while the step preserves the rest toe-to-ankle vector. It does not itself solve fixed segment lengths, heel/toe roll or a turn's changing foot view. Dedicated shots add corrections and separate run drawings, so it would be wrong to blame every gait on this helper. But it explains why simply raising an ankle and shifting a body can remain stiff or read as shuffling.

6. **Our written standards were ahead of execution.** `pipeline/styles/construction.md`, under “Character facing, faces and anatomy,” already requires separate body/head/gaze direction and matching views. The needed idea was not absent from the documentation. `check_cast_v021.py` verifies 14 bones and at least five moving controls above a numeric threshold, while correctly stating it does not establish artistic quality. Such a test can pass a puppet that barely acts. Earlier review practice did not consistently close the gap with complete-scene performance evidence.

These findings establish construction limits and repeated authoring choices. They do not prove that a single helper caused every visual defect, or that code review alone can determine comic timing.

## What the research supports

- [Lasseter, SIGGRAPH 1987](https://www.cs.utexas.edu/~fussell/courses/cs384g-fall2013/projects/animator/lasseter.pdf) discusses staging, pose-to-pose work, timing and connected thought in character acting. Our application: decide the meaningful attitudes and timing before interpolating controls.
- [Animation Mentor: Facial Animation 101](https://www.animationmentor.com/blog/facial-animation-101/) emphasizes visible thought changes, focused gaze and readable facial/body timing. Our application: separate noticing, understanding and responding; blinking and lip sync are not a substitute.
- [Toon Boom: About Swapping Drawings](https://learn.toonboom.com/modules/layout-and-posing/topic/about-swapping-drawings1?c=32) explicitly describes cut-out animation as more than moving parts, with new drawings used during a scene. Our application: author the few head/body/hand replacements demanded by the shot, rather than forcing every pose through one drawing.
- [Animating Childlike Drawings with 2.5D Character Rigs, 2025](https://arxiv.org/html/2502.17866v1) discusses remaining problems with camera-directed actions, external contacts and projection-related foot sliding. This is a different system, not evidence that adopting it fixes ours. It supports caution about promising arbitrary motion from a single drawing.
- The companion research note also covers a Disney gaze paper and Animation Mentor's contact/weight-transfer advice, including the limits of applying those sources to our comedy style.

## Proposed method for the next production

### 1. Plan performances before building the asset list

For each consequential shot, use a short entry in the existing shot plan: starting attitude, event noticed, gaze target, resulting attitude, body/head facing, and required contact. Example: Gyökeres enters confident, notices the shirted flag, stops, looks back at Arteta, then asks why he was signed. Arteta can hold still smugly while Gyökeres changes. Do not make everybody move constantly.

### 2. Keep the accepted identity; expand only the views the shot needs

Build coordinated alternate drawings for genuine facing changes, not unrelated replacement heads. Match skull landmarks, proportions, neck/collar, line weight, colour and clothing. For a turn affecting shoulders, provide the relevant torso/overlap change too. Add transition drawings if a direct swap pops. Preserve fitted deformation for movements it handles well; use replacement drawings for view or silhouette changes it cannot express. Native editable drawing layers in Blender remain a suitable direction; do not promise that converting a fixed image to strokes supplies missing poses.

Separate mouth articulation from facial expression, and eye focus from head orientation. At minimum, the chosen shot must have the expressions and gaze directions needed for its thought change. Do not build a speculative full-360 rig or exhaustive asset library.

### 3. Block distinct poses and reactions before smoothing

Establish the starting attitude, information-taking moment, and changed attitude with shot-specific timing. The important difference may be a small eye change or weight shift, not an extreme action. Check silhouettes, eye lines and the meaning of holds. Then add transitions and overlap. Do not increase all amplitudes or add random breathing/sway to conceal weak acting.

### 4. Author football contact as one event

For each kick, header, challenge or pivot, designate the support foot, contact moment, affected participant and recovery. Author ball and character together. Replace the simplistic knee projection where the shot needs segment-length constraints and a controlled bend direction; add deliberate foot roll or a new foot view when appropriate. A geometric test should detect sliding/reach faults, but the camera must still show the event clearly. No specific solver change is validated by this research yet.

### 5. Prove ordinary acting as well as extreme action

Use the existing staging review; do not add another approval bureaucracy. Before propagating a new cast, inspect a short complete two-character exchange showing a motivated look/turn, emotional change, reply and listening reaction. Include one simple planted step or prop contact. Compare it with the existing baseline in the same framing and duration, first silently, then with sound. Keep the established action proof for demanding running/kicking; passing it does not cover dialogue acting.

Acceptance evidence must identify actual readable changes and limitations, not just count moving controls. Inspect normal-speed playback for performance, then intermediate frames for construction. If full playback/listening did not occur, leave those aspects unreviewed. No new proof has been rendered or passed in this investigation.

### 6. Adopt tested improvements, not promises

Save the resulting successful views, controls and example performance as reusable assets after the proof. Reuse construction and contact mechanisms, but author emotional timing for the new scene. Preserve the old baseline, and compare likeness, joins, timing, contact and readability together after changes. The existing guides already contain many of these requirements; the immediate need is demonstrated execution and honest review, not a longer generic checklist.

## Historical illustrative experiment — not a next-production requirement

An approximately 8–12 second interaction using the accepted Arteta and Gyökeres identity: Gyökeres notices something outside his original facing direction, pivots with a grounded step, recognizes the insult, turns to Arteta and responds; Arteta gives a small confident reaction. Duration follows the performance, not a quota. Keep the old version beside it. This directly tests the fixed-facing and minimal-reaction failure; another isolated jump cannot do so.

Research and diagnosis are complete. Implementation remains proposed; the completed movie is untouched.

## Scope clarification — 2026-09-22

The user clarified that the next production may contain entirely different characters. The Arteta/Gyökeres example above is illustrative only and must not determine the next cast or require a remake. Select a representative excerpt from the next production after its concept is chosen. See [cast-independent supplemental reference study](../../../research/reference-ijvy-v001/analysis.md).
