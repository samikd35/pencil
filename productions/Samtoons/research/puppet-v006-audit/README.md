# v006 audit: preserve the caricature, improve the moving drawing

23 September 2026. **Selected baseline:** [the existing ten-second v006 call](../../videos/003-barca-emergency-meeting/artifacts/staging-v001/call-performance-v006/call-review.mp4). Both independent experiments are **rejected by the user**. They are preserved as evidence, not production alternatives. The v006 native scene has been reopened in Blender; its saved artwork, animation and audio remain unchanged.

## Conclusion

Keep the existing 2D characters and their recognizable design. Improve how the intended performance, joint geometry and artwork cooperate. The evidence does **not** support rebuilding the cast again, switching character medium, or installing a new deformation solver first.

The central limitation is that our animation asset does not fully describe the shapes required by its controls. A connected skeleton describes joint positions and directions. It does not describe the outside and inside contours of a thick sleeve, a wrist entering a cuff, or a changed grip. We currently approximate those independently and then test mainly the skeleton.

There is also a concrete code problem: a wrist-angle safeguard silently changes the intended performance. Fixing that alone exposes a second, visible construction problem. This is a chain of causes, not one magical missing Blender feature.

## What was actually inspected

- The selected source image, tracing/masking code, v004 artwork construction, v005 binding, v006 motion and attachment, current checker and encoder.
- Exact encoded weak-region frames **38, 146, 150, 154, 206, 210, 214 and 215**, plus source-art wrist/forearm crops. [Müller](evidence/muller-weak-poses.png), [Pérez](evidence/perez-weak-poses.png).
- All **240 saved poses** for wrist directions, bone attachment and wrist-strip measurements.
- Two isolated pose tests changing only the requested hand orientation, with the production file left untouched. [Pérez, frame 150](evidence/perez-clamp-ablation.png), [Müller, frame 215](evidence/muller-clamp-ablation.png).
- Original papers and official production/tool documentation, summarized with limitations in [papers.md](papers.md).

These are diagnostic checks and visual samples. They are not a new finished animation, normal-speed acting approval, audio audition or benchmark-quality certification.

## Concrete findings

### 1. The pose code changes the hand direction without reporting it

`build_call_performance_v006.py:pose()` independently authors wrist position and hand rotation, solves the elbow, then clamps the angle between forearm and a vertical hand-bone proxy to ±40°. The prop is attached to that hand, so it also changes direction.

| Saved actor | Frames at the limit | Greatest difference from requested hand direction |
| --- | ---: | ---: |
| Müller | 91 / 240 | 32.42° at frame 228 |
| Pérez | 61 / 240 | 37.24° at frame 151 |

Pérez's frame 151 requests 67° in drawing coordinates and delivers 29.76°. Bone attachment error remains zero. The old check accepts wrist angles below 42.01°, so it passes precisely because the clamp has already altered the requested pose. [Measured output](pose-audit.json).

A clamp is not inherently wrong; **silently overriding an authored pose and treating a limit pass as successful execution is the problem**. The source's hand bone is defined as an arbitrary vertical 75-pixel segment, so this number should not be presented as a measured anatomical wrist limit either.

### 2. Simply deleting that clamp is visibly insufficient

The diagnostic restores the requested rotation while retaining the same skeleton positions, hand drawing, sleeve and bindings. Pérez's hand changes direction, but his cuff/skin transition becomes a sharp stretched wedge. Müller's transition also changes its silhouette. These tests are **not selected fixes**.

The first implementation must fit the intended hand/cuff silhouette and a feasible arm pose together. It must not conceal the problem by reducing the gesture or freezing the hand. If an authored pose cannot be supported by the current drawing, report the missing construction instead of silently replacing the performance.

### 3. Most of the arm artwork is rigid, despite the broad description “deformable puppet”

In `build_call_performance_v004.py:region_weights()`, every point in a forearm region receives 100% forearm influence; the grip receives 100% hand influence. `articulated_sleeves()` combines a newly constructed upper sleeve with a forearm extracted from the posed image. That is legitimate cutout construction within a useful range, but it does not author a different elbow silhouette or cuff opening.

`build_call_performance_v005.py:bound_wrist()` constructs a 13-row bridge between two registered edges, with interpolated forearm/hand weights and Preserve Volume. Its fills, shadow and outline ribbons share those weights. This helps attachment; it still has no authored target for how the inside and outside wrist contour should look at a strong bend.

The audit found **no wrist-strip triangle flips** across 240 frames. Row-width extrema remain essentially stable: approximately 56.61–71.00 source pixels for Müller and 56.04–72.00 for Pérez. This rules out that particular collapse symptom in this shot, not all bad deformation. It weakens the case for adding more subdivisions or a different weight solver as the first remedy. [Measurements](wrist-measurements.json).

### 4. The source is a good likeness reference, but incomplete animation construction

`trace_call_reference_v003.py` extracts a particular bent arm and fixed grip from `call-pose.png`. It uses palette thresholds, manually selected polygons and horizontal hand cuts. Those are image-specific construction decisions, not a reusable understanding of anatomy.

The source provides the successful appearance we should retain. It does not show every hidden cuff edge, open hand, palm/back orientation, arm straightening or new head view. A more detailed prompt for one whole illustration cannot supply all those states. Nor can tracing recover an occluded contour from absent pixels.

### 5. The review was checking necessary conditions as if they were sufficient

Connected bones, normalized weights, no crossings and identical motion before/after dressing are valuable. They do not measure silhouette appeal, grip readability, cuff shape, acting or likeness. Existing review notes correctly mention limitations, but the implementation kept accumulating corrections without a test that compared intended and delivered posing.

The new orientation audit deliberately fails on v006. It identifies one reproducible issue, not every visual defect. Other visual problems still need source/pose comparison rather than invented numerical thresholds.

## Stage-by-stage changes

| Stage | Retain | Change and proof required |
| --- | --- | --- |
| Script → action | Existing dialogue, joke, timing and character relationships | State the intended silhouette, gaze, grip direction and contact at each important beat. Pose controls must deliver that intention or flag a conflict. |
| Identity references | Current likeness, hair, proportions, kit and office treatment | Distinguish identity reference from construction artwork. Request only missing action/view drawings; compare against the existing design before import. |
| Artwork preparation | Successful visible source contours | Complete hidden sleeve/cuff/torso areas; register wrist, palm axis, cuff edges and prop contact. Give each visible outline a clear owner. Keep interior cut edges out of visible ink. |
| Conversion | Native editable mesh/curve artwork already working in Blender | Verify rest-pose silhouette, holes, palette and contour order against the source before binding. Use semantic part masks, not transferable skin-colour thresholds. Any converter change must preserve the current likeness. |
| Binding | Connected skeleton and explicit part ownership | Use rigid binding where intentional; deform only the required continuous regions. Fit joint topology and contour tangents to the actual art. Evaluate skin, ink and shading together. |
| Joint correction | Existing arm targets and expressive amplitude | Add a small pose-driven correction for the cuff/wrist bend. A different palm/back view or grip needs suitable replacement art, not more stretch. Test both approach and recovery. |
| Motion/contact | Existing body/head/eye performance and shared hand–prop attachment | Audit requested versus evaluated pose. Resolve conflicts through appropriate shoulder/elbow/wrist coordination and matched artwork. Do not remove limits blindly. Pickup/release requires explicit contact transitions. |
| Head/face | Working brows, gaze, blinks and mouth changes | Current head movement is largely in-plane tilt; it is not a demonstrated three-dimensional head turn. Add matched views only when the shot calls for them, with anchored features and transitions. |
| Environment/camera | 2D characters; current office geography | 2D, layered 2.5D or stylized 3D sets are compatible. Keep real spatial scale/contact and design camera angles around available character views. A 3D room will not repair a puppet. |
| Review/reuse | Weak-region-first review and exact encoded output checks | Compare baseline and candidate at identical frames, then normal speed. Promote a fix only if likeness, gesture, contour, contact and timing all survive. Retest a new action; do not infer arbitrary-pose capability. |

## Research applied to this specific failure

**Pose-space correction is the most immediately relevant principle.** It supplies an artist-defined shape for a pose rather than asking weights to invent it. Blender supports shape keys and pose-driven activation. This is a proposed local repair, not a proven v006 result. [Lewis, Cordner & Fong](https://scribblethink.org/Work/PSD/PSD.pdf), [Blender driver examples](https://docs.blender.org/manual/nl/5.2/animation/drivers/workflow_examples.html).

**Topology-aware weights and ARAP are conditional tools.** BBW addresses how influence spreads through a constructed shape; ARAP resists triangle distortion. Neither supplies an unseen hand or correct cuff contour. The current rigid forearm/hand assignments and non-flipping wrist strip do not establish a need to install either first. [Bounded Biharmonic Weights](https://igl.ethz.ch/projects/bbw/bounded-biharmonic-weights-siggraph-2011-compressed-jacobson-et-al.pdf), [ARAP project](https://www-ui.is.s.u-tokyo.ac.jp/~takeo/research/rigid/index.html).

**Deforming shape, attached hand and alternate drawing are separate responsibilities.** Harmony documents that separation. Its controls are useful production evidence, not drop-in Blender code. Matched hand/arm drawings may extend this same puppet without redesigning its head or restarting either rejected experiment. See the official sources and 2.5D-view limitations in [papers.md](papers.md).

No research model, add-on or dependency was installed. No published system has been verified here as a one-step path from this reference to benchmark-quality animation.

## How to use Codex, the tools and models better

The useful division of work is **visual decisions with explicit targets, repeatable execution with code, and rendered feedback after each meaningful change**.

- Use image generation to propose a missing construction drawing in the established style. Inspect the actual output. Do not regenerate the whole character to repair a wrist, or assume a generated sheet has consistent anchors.
- Use Python/Blender for exact coordinate registration, rig transforms, contour construction, weights, authored corrections, drawing exposure, depth order, contact schedules and repeatable renders. More generated code does not automatically add artistic intent.
- Use the agent to inspect the source and weak rendered intervals, form a falsifiable explanation, change one cause and compare the result. The saved artifacts and measurements make the work resumable. OpenAI describes this tool–feedback loop; it does not establish animation expertise or guaranteed visual quality. [Official Codex workflow](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex).
- Judge likeness and silhouette through baseline/candidate comparisons, with explicit defect labels. Automated vision judgments can assist triage, but require calibration and cannot replace exact-frame and motion review. [Official image-evaluation guidance](https://developers.openai.com/cookbook/examples/multimodal/image_evals).
- Preserve one authoritative path for a changed component. v006 currently loads v005 → v004 → v002 through source-string rewriting; helper changes can affect later builds. The render manifest omits some of those dependencies. Before adopting a repair, pin/hash the actual helper chain and make the corrected component's ownership explicit. Do not turn this into a new generic framework.

The rejected experiments also show a process failure: they changed construction and lost the visual target simultaneously. They are not reliable evidence that all 2D rigs or all stylized 3D animation are inferior. The user has rejected those delivered options; the production direction remains the existing 2D puppet.

## Repair order and stopping conditions

1. **Selected baseline and diagnosis — done in this audit.** Preserve v006; record rejection; capture weak regions; reproduce the silent angle change and inspect the isolated consequence of restoring it.
2. **One integrated wrist/cuff repair in a new v007 candidate.** Preserve the current cast, environment, audio and full ten-second action. Calibrate palm/cuff attachment to the drawing, author the desired extreme pose, and implement the smallest local correction/pose adjustment that makes it possible. Do not silently change the intended grip or shrink the gesture. Establish explicit behavior when a requested pose lacks support.
3. **Review that correction across the action.** Start at Pérez 146–154 and Müller 206–215, then transitions into/out of corrected ranges. Check contour tangent, wrist thickness, cuff opening, finger/prop overlap, outline continuity and torso/scarf stability. The numerical orientation check and visual inspection must both be accounted for; revise an authored target explicitly if the art direction warrants it.
4. **Extend only the demonstrated construction.** Add the next genuinely different grip/view and a full-body football contact shot. Reuse the corrected mechanism, not the exact sampled motion. New drawings are work required by the action, not evidence that the whole pipeline must be rebuilt.
5. **Promote only verified improvements.** Keep the experiment in the current production until it survives the above. Document the proven range and remaining limits; then update reusable construction guidance. A newly implemented fix must not be described as universal.

This audit is complete; the v007 artwork/animation repair is **not implemented**. The next change is now a diagnosed component repair in the selected scene, rather than another replacement character experiment. Review should become cheaper and earlier; no honest process can eliminate it for every future pose.

## Reproduce the evidence

From the Pencil root:

```sh
PYTHONPATH=.runtime/vector-art ~/Models/qwen-voice/.venv/bin/python productions/Samtoons/research/puppet-v006-audit/capture_baseline.py
/Applications/Blender.app/Contents/MacOS/Blender -b productions/Samtoons/videos/003-barca-emergency-meeting/artifacts/staging-v001/call-performance-v006/call-performance.blend --python-exit-code 3 --python productions/Samtoons/research/puppet-v006-audit/audit_saved_scene.py -- --ablate
```

The second command deliberately exits **3** on the saved v006 orientation discrepancy and writes [pose-audit.json](pose-audit.json). Its optional isolated render changes are not saved to the native production. [audit.log](audit.log) contains the failure. The assertion detects this specific control discrepancy; it cannot certify that a green result has attractive anatomy.
