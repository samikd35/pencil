# Video 003 — development, not a completed staging checkpoint

Current draft: [audiovisual script](../../script-v001.md), 3:28 working duration budget (S07 extended by one second). Source brief remains unchanged. Pérez and Müller are the user's selected Madrid/Bayern characters; all dialogue is fictional. Other club delegates and the final goalkeeper remain original fictional characters.

## What exists

- [S07 Flick/assistant continuous-clothing revision](coaching-performance-v002/README.md): [15-second review](coaching-performance-v002/coaching-review.mp4). v001 was rejected for discontinuous shoulders/hips; v002 retains the scene performance and supplies joined garment outlines. Creative acceptance is pending.

- [S06 standing-pose revision](football-performance-v002/README.md): [13-second review](football-performance-v002/football-review.mp4), [native scene](football-performance-v002/football-performance.blend). Full marking/pass/reception/finish sequence with six characters, speaker-labelled line and contact sounds. Numerical contact checks and focused frame inspection are recorded; final performance/sound approval remains pending.

- Selected [S08 call baseline](call-performance-v006/README.md): a ten-second native Pérez–Müller performance candidate. [Play v006](call-performance-v006/call-review.mp4). User selected it after rejecting both independent experiments. Remaining hand/cuff defects are deferred by the user on 23 September; this selection is not final quality approval. Earlier revisions remain historical evidence.

- Eight [rough native layouts](layouts-v002/layouts.blend), authored in the visible Blender instance. They show broad composition and role placement. The generic figures are **storyboard placeholders**, not selected character designs, rigs or finished animation.
- [Call-scene treatment](../../assets/treatment-v001/call-caricature.png), generated with the built-in image tool using Video 001's finish and identity references. [Exact prompts and inspection](../../assets/treatment-prompts-v001.md). First result was too textured; the revised reference simplifies it. This is reference artwork, not a native performance.
- [Native training set](training-set-v001/training-set.blend), with actual dimensional pitch/goal/marking geometry and separate cameras. [Wide preview](training-set-v001/wide-final.png), [finish angle](training-set-v001/finish-refined.png), [full plan](training-set-v001/plan-full.png), [checks](training-set-v001/native-check.json).

The user clarified that recognizable caricatures and high-quality, believable environments are both required. This applies to every cast member and location. These draft assets do not establish that the benchmark has been reached.

## Actual inspection and limits

Static previews of all eight rough layouts were inspected. They establish a losing-score reveal, the same room's opening/ending geography, a proposed unmarked channel and a readable call location. They still use symbolic figures: S01 does not yet draw the planned kneeling/hugging; S04 does not yet show the complete seated acting; S07's clipboard needs natural hand placement; S08's rough portrait spills below its call border; S16's rough pointing arm faces away from the offered chair. These are unfinished layouts, not cleared performance poses. Final construction must follow the written action and revised staging, rather than fit these placeholder bodies.

The generated call treatment was inspected for likeness, opposed eyelines and pen/frame grips. It provides a visual direction candidate; it supplies no evidence of head turns, expressive transitions, connected moving joints or lipsync. The small photographic decoration in the background is not a selected production asset.

The training set was viewed from wide and finish cameras. An uncovered ground gap beneath distant scenery was corrected in both the builder and native scene. The goal check measures the clear inner width/height, rather than tube-centre spacing. Saving, reopening and rendering the wide view produced identical decoded pixels. The diagnostic overhead camera was subsequently widened to show the full field. These checks establish geometry/persistence, not final scenic polish or animation quality. Landscaping and architectural shapes remain rough; final color/light integration must be reviewed with the characters.

At the initial layout review, no audio or finished character performance existed. Since then, two local call voice candidates and the S08 native performance were generated. The current call report distinguishes actual frame inspection and numerical checks from unperformed normal-speed playback/listening. No checkpoint is passed. The rough layout figures remain placeholders, not final designs; label them clearly when showing them.

## Source ownership and next work

`scripts/build_layouts_v001.py` owns the rough boards. `scripts/build_training_set_v001.py` owns the training environment, using inspected Video 001 surface/curve mechanisms without importing its full builder or live state. Native snapshots preserve the current inspection state; author later changes in the responsible builder or explicitly change ownership before file-only corrections.

`scripts/build_call_performance_v006.py` owns the selected S08 skeleton and action; the v004/v005 and tracing helpers supply its artwork and binding. See the [audit](../../../../research/puppet-v006-audit/README.md) for the dependency chain and remaining defects. No v007 hand repair is currently scheduled.

## Revised next-scene plan · 23 September 2026

The user asked to stop the repeated single-hand repair loop and move to new scenes. This supersedes the audit's proposed immediate v007 repair. Preserve v006, existing references, voices and models. Both rejected experiments remain rejected. The next scene choice below follows the existing S06–S07 production plan.

1. **S06 — complete football action first.** Build the approximately 13-second sequence: defenders crowd Raphinha → he notices unmarked Yamal → Pedri passes → Yamal receives, plants and finishes → defenders react late. Reuse the dimensional training set. Keep recognizable drawn characters, coherent perspective and left-to-right attack. Deliver one playable scene and its editable Blender source.
2. **Prepare only what that action needs.** Block the whole sequence, camera and ball path before detailed binding. Use the required contact and extreme poses to identify artwork needs: planted/striking feet, bent knees, torso rotation and Raphinha's pointing hand. Preserve likeness from selected references; supply matched local drawings where the action changes the visible surface. Check hidden joint coverage and attached outlines before rendering. Do not copy the call builder's silent wrist-angle override or assume one posed image covers every movement.
3. **Bound the internal review.** First watch the complete scene for readable action, timing and acting. Then inspect the weakest contact/deformation intervals, followed by one coordinated correction pass and a regression check. A broken contact, disconnected limb, visible clipping or unreadable action remains a blocker for that shot. If unresolved after that pass, keep it explicitly unfinished and continue independent scenes; do not launch another open-ended rig experiment. Minor finish notes enter one consolidated cleanup list. This is a limit on repeated iteration, not permission to call defective work finished.
4. **S07 — Flick and the assistant.** Follow with the complete conversational beat: pleased assistant, Flick's calm answer, listener reaction, watch check and ball roll. Preserve full lines and pauses. Reuse existing audio when applicable; new dialogue still needs the existing sound process and voice runtime. Review restrained acting and hand/ball release in the scene's context.
5. **Assemble the passage and continue production.** Join rough S05 context, S06, S07 and the selected S08 excerpt to assess transitions and pace. Keep S04 ensemble coverage on the staging list. Present meaningful scene progress through the existing staging checkpoint, then continue the remaining shots. Collect recurring construction defects for a shared repair only when multiple actual uses establish the need.

**Deferred:** Pérez/Müller grip and cuff polish, broader solver experiments and additional general research. Reopen only if they block a new shot or during the consolidated cleanup before final approval. Their technical audit remains useful evidence, not the active deliverable.

**Progress:** S06 stance v002 and S07 continuous-clothing v002 are review candidates. Screen motion/quality takes priority over convenient manual editing, as explicitly directed by the user. Benchmark parity is not established. Next: passage assembly and the existing staging review; keep unresolved finish in the consolidated list.


## S12 membership candidate — 2026-09-24

[Preview and native delivery](membership-v001/README.md) now cover the next 13-second scene. S11 reveal/reaction timing was accepted before this work. S12 is pending timing/voice review, with exact review and technical limits recorded beside the artifact. S07 remains rejected. Next after the S12 checkpoint: S13; preserve the S03 scarf-edge continuity task for assembly.
