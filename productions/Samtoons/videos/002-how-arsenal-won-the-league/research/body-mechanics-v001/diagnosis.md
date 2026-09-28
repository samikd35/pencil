# Why the movement failed — Samtoons 002

17 September 2026. Status: investigation completed; animation remains rejected. This supersedes the previous angle-tuning approach, not the approved artwork or script.

## Root cause

I treated a rig as a motion system. It was only a mechanism for moving a drawing. I prescribed root travel, hip bob, feet and arms separately, then tried to make the results convincing by changing amplitudes and timing. No reference-based sequence of complete poses defined how support, propulsion, airborne motion and recovery connected. Surface fixes addressed visible damage without supplying that missing performance.

A second problem compounded it: the fixed drawing and its planar deformation were asked to imply depth, arm gestures and limb overlap that were never designed as poses. A frontal cartoon **can** run; the benchmark does. The limitation is expecting arbitrary flat rotations of our particular neutral painting to invent the necessary poses automatically. A more complex 3D rig or a physics simulation is not a prerequisite and would not automatically fix this.

The review method then rewarded the wrong evidence: unchanged vertex/bone hashes, aligned endpoints and planted toes. Those are useful engineering checks. They do not establish believable movement. I described local corrections as improvements before establishing an improved performance.

## Evidence from the actual implementation

| Finding | Evidence | Consequence |
| --- | --- | --- |
| Motion authored as independent functions | `scripts/build_bruno_action_v006.py`: separate runfoot, hip cosine, arm cosine and jump equations; inherited from layered and earlier intense-motion approaches | No complete authored action poses or causal sequence controls their relationships |
| Incorrect neutral knee | Saved v006 at frame 192: left knee differs from original rest by **0.1503603 local units**, about **0.0451 world units** at scale 0.3 | Both knees were forced onto the same IK branch; even returning to neutral changes the original pose |
| Contact tests pass despite bad performance | Prior evaluated planted-toe drift is only **1.19e-7 world units** across 234 consecutive contact samples | Contact alone cannot validate locomotion or a rig adaptation |
| Gravity setting is not driving the keys | Saved scene gravity is -9.81; keyed hip flight measures approximately **-4.32 world units/s²**, and body objects have no rigid-body simulation | The checkbox is not a physical controller. The arc is authored; its style/scale must be intentional |
| Hip is used as a mass proxy without a mass model | Pose generation translates hip/torso; no whole-body COM is evaluated | The measured hip acceleration is diagnostic, not proof of physical COM accuracy or a universal pass/fail value |
| Rendering cleanup cannot supply performance | Transparent-face trimming and depth offsets clean some overlaps, while hands/arms still read as gestures and the run remains rejected | Stop treating material/deformation polish as the next motion solution |

[Captured native audit](audit.json), [expected failing audit log](audit.log), [geometry correction check](geometry-check.json). The audit reads the saved native scene; it does not alter it.

### Reproducible defect and bounded correction

Run from the workspace:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background productions/Samtoons/videos/002-how-arsenal-won-the-league/artifacts/bruno-action-v006/bruno-action-v006.blend --python-exit-code 1 --python productions/Samtoons/videos/002-how-arsenal-won-the-league/research/body-mechanics-v001/audit.py
```

Expected result: nonzero exit with `REPRODUCED: supposedly neutral pose changes original knee bend`. It takes seconds and catches a concrete contributing defect; it cannot reproduce the whole artistic judgment automatically.

The shared `pipeline/pose_geometry.py` uses an explicit pole instead of one bend sign for every limb. It rejects unreachable/ambiguous targets. `python3 productions/Samtoons/videos/002-how-arsenal-won-the-league/research/body-mechanics-v001/check_geometry.py` applies it to the captured native rest positions: both neutral errors are below 1e-15, and a compressed pose retains both segment lengths. `python3 pipeline/pose_geometry.py` exercises both bend directions and invalid targets. **This corrects a geometric primitive; it has not repaired or approved the rejected movie.** Historical builders and renders are retained unchanged.

## References actually revisited

Read the adopted Bayern benchmark and study. Inspected consecutive thumbnail sheets `all-04.jpg` and `all-05.jpg` (source frames 240–399, about 8.00–13.30 seconds), and native stills F432, F648 and F1711. The running interval shows distinct spread/passing/recovery silhouettes, alternating arms, bent trailing legs and rapid travel; the native contact images show action-specific poses and clear response. These are frame observations, not a new normal-speed playback review or knowledge of the creator's rig. Their frontal/three-quarter staging disproves any claim that sideways travel universally requires a side-view drawing.

[First-party animation, physics and rigging research](../../../../../../research/body-mechanics-primary-sources-v001.md) supplies the corrective method. Wayne Gilbert emphasizes causes and lead/follow; Jason Martinsen starts with reference and whole-body blocking before breakdowns and curves. Physics establishes causal constraints, not a compulsory realistic style. The embedded teaching videos have not been watched in this investigation.

## The replacement authoring method

Use the shared [motion-planning guide](../../../../../../pipeline/motion-planning.md), now linked from the production skill, construction guide and relevant recipes:

1. Pick and inspect the exact action interval and view. Keep the benchmark's exaggerated comedy and the accepted character finish.
2. Write support/contact, release, travel, impact and recovery together in the existing shot plan. Choose timing and scale consistently.
3. Build complete readable poses first. Calibrate neutral geometry and bend direction; include pelvis/chest/head relationships. Do not add arm sine waves to an independently completed leg cycle.
4. Check whether the original art supports each pose. Use matching hand/limb or whole-pose drawings where needed; no pasted replacement head, generic weaker body or loss of kit/shoes.
5. Add breakdowns, interpolation and overlap only after the pose sequence explains the action. Verify contact, reach and trajectory, then evaluate the actual movement at playback speed.

This applies to kicks, turns, lifts, falls, interactions and mechanisms through their own causal sequence. Abstract graphics use their intended timing rules rather than forced human physics. No new approval gate, physics engine or all-purpose procedural motion framework was added.

## Current decision and next concrete proof

All current Bruno motion candidates remain rejected/unapproved. v005 is the user's pictured rejection; v006 is an additional internally rejected attempt, not a user-approved improvement. The visual baseline is retained. Full-film animation and Gyökeres adaptation do not advance on these tests.

The next proof must be rebuilt from a small set of complete reference-informed running and jump poses in the intended view, with ground-contact and trajectory overlays available for inspection. It remains the same eight-second diagnostic and existing staging checkpoint. A rough internal proxy may establish mechanics, but the user-facing test must return to the complete accepted character finish. The outstanding work is that replacement performance and its motion review—not another angle adjustment to the retired cycle.
