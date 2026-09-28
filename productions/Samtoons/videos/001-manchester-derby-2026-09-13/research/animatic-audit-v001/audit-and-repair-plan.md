# Full animatic rejection: diagnosis and repair plan

15 September 2026. **Audit and proposed repair only. No animation, voices or movie have been revised.**

The criticism is justified. The full film does not maintain the construction quality of the approved excerpts. The expansion reused the controls but replaced the new characters' visible arm construction with inadequately fitted patches, reused weak action patterns, and filled fixed scene lengths with too little performance. Inspection was insufficient, and the previous claim that the new limbs were fixed exceeded the evidence. These are production and review failures for which the assistant is responsible. Blender, the stickman foundation and the user's chosen duration did not require these shortcuts.

## Evidence and coverage

Audited export: [animatic.mp4](../../artifacts/animatic-v001/animatic.mp4), SHA-256 `ee23aa2df0791ac7376807b9a9cffe4d000946f26fdc1f1318848424a1ad5008`. Native scene: [combined-animatic-v006.blend](../../artifacts/animatic-v001/combined-animatic-v006.blend). All 12 supplied screenshots were compared with the movie.

- Decoded all **3,600 frames**; presentation timestamps advance uniformly by approximately 1/24 second. Native scenes and encoded file both specify 24 fps, with a 150-second duration. [Extraction and timestamp results](extraction.json).
- Visually inspected the whole film at one-second intervals: 150 images across six overview sheets.
- Visually inspected **308 consecutive frames across ten targeted windows** covering new arm motion, both United strikes, Haaland's finish, Martínez's protest, Lammens' save, Maguire's header, and two approved-action comparisons. [Evidence browser](evidence.html) includes every sheet and the unchanged movie.
- Read the builders, finalization patches and prior checks; inspected the saved native camera keys, cast geometry and orientation. [Native inspection](native-inspection.json).

This is a targeted frame-by-frame diagnosis, **not a claim that every one of the 3,600 frames was individually visually cleared**. Small distant details sometimes require the supplied enlarged screenshots. No new listening judgment is claimed. The findings below are sufficient to reject the construction and explain the repeated failures; repaired action windows will require complete consecutive-frame review and normal-speed playback.

## Why the good bodies and bad bodies differ

The old and new actors share a simple joint-control foundation. The difference is how the visible drawing follows it.

The earlier actors retain a continuous illustrated surface, with shoulder and hip weighting adapted through earlier reviews. Bruno and Mbeumo in the newly assembled late-chance conversation look coherent because they reuse those suitable assets. This is evidence that reusable character construction can work outside its original excerpt; approval did not belong only to three fixed video clips.

The new cast was cropped from two four-person sheets. Different proportions and limb silhouettes were fed into the old builder, then assigned new approximate distance-based weights. After that still failed, the new characters' raster forearms were partially deleted and replaced with generic curve arms, polygon hands and circular covers. The saved file contains **24 actor instances with this added arm construction**. This construction change was propagated before its visible result met the accepted standard.

| Root cause | Source evidence | Visible consequence |
|---|---|---|
| Incompatible assumptions carried into new art | `build_option_a.py`, lines 112–153, uses image landmarks and fixed pixel-region thresholds; `build_full_animatic.py`, lines 12–22 and 51–74, rescales and overrides weights with generic proximity/torso rules. | An attractive neutral drawing does not retain its painted silhouette when stretched around different joints. Normalizing coordinates does not normalize anatomy or garment edges. |
| Patching symptoms instead of preparing suitable limbs | `finalize_animatic.py`, lines 92–119, deletes mesh faces within rough geometric regions, then adds curve forearms and polygon hands. Lines 141–152 add upper arms and joint discs. | Original arm fragments survive beside replacement limbs; shirt and sleeve contours expose gaps; round caps read as mechanical joints; thick black bars and generic hands clash with the painted body. |
| Appearance inferred from scene names | `finalize_animatic.py`, lines 105 and 141–143, chooses color using strings such as “Rashford” and “Mainoo”. `build_full_animatic.py`, line 213, calls those players “Corner 0” and “Corner 1”. | Dark-headed players acquire pale arms in the corner scene. Character identity must come from the character asset, not the instance label. |
| Kick poses lack a coordinated body action | `build_full_animatic.py`, line 139, assigns the same angle to thigh, calf and foot for both shots; `build_dramatic_actions.py`, lines 71–76, rotates each segment from its rest vector. | A straight leg swings like a lever; pelvis and supporting leg barely participate. Shorts/thigh artwork folds and stretches around the hip. The body does not convincingly load, strike and recover. |
| Ball placement solves one moment only | `build_full_animatic.py`, lines 140–146, takes the toe position at frame 57 and parks the ball there from frame 1. | The ball appears beside the planted foot during the windup. A later toe-position match cannot establish a convincing approach, boot-surface contact or release path. |
| Flat artwork viewed from an unsuitable direction | `build_option_a.py`, line 119, assigns an initial facing orientation; the finished saved Mainoo scene has its background defender approximately **71.5° away from face-on at the opening camera**. | Fernández appears almost edge-on; layer thickness and rectangular pieces become visible. A 3D camera does not create missing character views. |
| Review tested the wrong property | `finalize_animatic.py`, lines 156–171, samples four frames per new actor, checking wrist/palm control alignment; the parry check addresses an already-approved action. | Zero endpoint error was reported while visible sleeves, elbows, hips and skin still failed. The check never established continuous silhouettes, absence of duplicate art, plausible footwork or energetic performance. |

The shared rig has 14 independently constrained bones, not an articulated bone-parent hierarchy. That alone is not a defect—the approved bodies use it too. The failure is treating its point controls and generic surface weights as if they guarantee anatomical behavior for every new drawing and action. Adding bones indiscriminately would not address the art preparation or acting decisions.

## Shot findings and recommended repairs

Times are positions in the current 150-second export. Frame numbers are global and one-based, with time `(frame−1)/24`.

| Film section / supplied image | Observed failure or retained strength | Repair direction |
|---|---|---|
| 0:00–0:08, Haaland/Maresca; image 4 | Forearm/sleeve remnants and mechanical joins, especially as Maresca raises the ENZO card. Consecutive F101–132 expose the same seams through the change. | Prepare coherent arm and sleeve surfaces for both characters. Use a specific greeting, recognition pause, card reveal and offended reaction. Compose a readable medium/insert rather than enlarging bad joints. |
| 0:08–0:22, Foden/Bruno/Oliver; image 1 | Coherent bodies and a clear physical relationship survive F240–271. Earlier user-reviewed action remains the best local construction reference. | Preserve the accepted kick/fall/recovery/red-card content. Keep the contact and ground visible; only change adjacent coverage if the new edit needs it. This is not blanket certification of every old frame. |
| 0:22–0:32, Foden exit | Body artwork is stronger, but the exit combines sliding root travel and small foot wiggles; the ground shadow is left behind in the overview. | Give the departure a short readable walk/angry stomp with matching foot plants and traveling shadow; put the fishing-rod reveal on a deliberate reaction beat. |
| 0:32–0:44, Rashford; image 5 | F805–838 show shorts/thigh distortion during an almost rigid leg swing. F874–905 show a forearm held away from the head: the intended temple/scratch performance does not happen. | Author actual preparation, planted support, knee/ankle action, contact and recovery. Then place fingertips at the temple and turn confidence into an embarrassed scratch; supply the necessary hand/pose drawings. |
| 0:44–0:56, Mainoo; image 6 | F1093–1126 repeat the same leg failure. Background Fernández is visibly edge-on. Ball and keeper response are not staged as a convincing sequence. | Reuse a corrected mechanism, author Mainoo's own action, fit the shorts/hip drawing, and give the defender an appropriate view. Show the rebound and possession outcome before the post's contract gag. |
| 0:56–1:07, goal; image 7 | F1435–1458 show Haaland swinging a leg while the others remain mostly upright spectators; overlapping players obscure their roles. | Block the deflection/interference/finish as coordinated action. Give the defender, attacker and keeper distinct positions, gaze and reactions. Use an establishing angle plus readable finish and flag reaction. |
| 1:07–1:16, VAR | Nine seconds largely on a checklist; stamp appears without an acted decision. | Keep the concise factual distinction, but make the skipped check and approval an observable comic action, then cut when its meaning is clear. |
| 1:16–1:25, protest; image 8 | F1825–1856 show Martínez's old arm fragment beside his raised replacement arm. Everyone largely faces the audience. | Clean shoulder-to-hand construction; point toward Fernández with body and gaze, then cut to the subject/reaction. Make the complaint scroll readable without dominating the whole shot. |
| 1:25–1:32, Lammens; image 9 | F2080–2111 show a small tilted-body lift with glove fragments. Fernández does not perform a visible strike in this builder. | Animate the shooter too. Give the keeper anticipation, push-off, reaching glove, deflection and landing. Inspect contact through the glove surface, not only a finger control. |
| 1:32–1:41, Maguire; image 10 | F2268–2291 show a small whole-body hop among motionless players, weak header emphasis, and pale arms on Mainoo/Rashford. | Fix identity/material assignment. Stage preparation, competition for the ball, head contact and miss. Use a brief heroic reveal followed by an embarrassed reaction; keep other players responsive to the ball. |
| 1:41–1:53, Bruno/Mbeumo and parry; image 2 | Reused bodies stay coherent. The parry has a visibly stronger body arc than the new Lammens shot. | Retain these assets and the accepted parry. Tighten unnecessary lead-in or hold only after reviewing the complete pacing. |
| 1:53–1:58, keeper/Haaland; image 11 | Good keeper surface beside bad Haaland arms. The wolf joke is mostly two triangle ears, with little behavioral payoff. | Preserve keeper construction, fix Haaland, and make the transformation/reaction an acted joke. Do not spend five seconds on a nearly unchanged pair. |
| 1:58–2:10, celebration; image 12 | Maresca stands in front of a rectangular “lounger” instead of relaxing on it. Twelve seconds contain sparse gestures and widely spaced short lines. | Make a genuine seated/reclining pose and hand-held cup, then let the mistaken name interrupt that relaxed state. Plan the camera to show the posture and then the offended reaction. |
| 2:10–2:21, apology; image 3 | Letter handover and connected bodies are substantially clearer; F3236–3267 retain coherent elbows/shoulders during sobbing. | Preserve approved performance and three approved recordings. An insert or reaction composition can help the letter/response, but need not rebuild the working body. |
| 2:21–2:30, flood/fishing | Flat water and nearly stationary fishing pose; abrupt change of setting does little to connect tears to the flood. | Show the expanding consequence, then pull back to reveal Foden enjoying it. Give the float and his response a short setup/payoff, then end. |

## Why it feels slow

There is no evidence of an encoding frame-rate mismatch: 3,600 frames / 24 fps = 150 seconds, with uniform timestamps. The renderer supplies one authored frame for each encoded frame. The user's browser playback setting was not inspected; the film's authored pacing already explains the complaint.

Measured from scene keys:

- Each United post shot waits **2.33 seconds before contact** (local F57), then takes **1.125 seconds from strike to post** (F57→84). Both get identical 12-second scene slots despite different jokes. These ball paths are explicitly LINEAR; their sluggishness is not caused by Bezier easing.
- Maguire's incoming ball takes **1.83 seconds** from F30→74; the main body returns at F98, while the scene continues to F216. Later captions/camera changes do not provide a new physical performance.
- The VAR stamp arrives at F111 and the scene lasts to F216: about **4.38 seconds afterward**, with the completed graphic largely unchanged.
- The 12-second celebration has short speech starts at F57, F106 and F184—approximately **2.04 and 3.25 seconds apart**—with little intervening acting.
- `smooth_actor` applies the same auto-clamped Bezier treatment to all control keys. This makes transitions continuous, but does not design acceleration, weight or comic contrast. Other ball paths use the general key helper; their acceleration must be reviewed individually.
- Many background actors receive the same neutral pose at first and last frame plus a blink. Missing anticipation, tracking gaze and reaction remove energy even while the main object moves.

**More drawings must improve the path and pose—not extend the same movement over more time.** At the same 24 fps we can have a quick strike, a readable impact, a short settling motion and a deliberate reaction pause. Do not globally speed up the whole film: that would also damage dialogue, the accepted sob and purposeful deadpan timing.

Retain the requested **2:30–3:00 range** by spending time on actual setup, physical business and escalating reactions. Do not pad to the lower bound with idle holds. Redistribute time between beats only after the revised action/camera cut plays at normal speed. Proposed timing experiments, not rules: test a 4–8-frame final kick swing, a shorter ball flight appropriate to the staged distance, and 6–12 frames for registering a reversal before the reaction. The final values must come from the shot and its sound, not a universal template.

## Camera research and application

See the [primary-source camera research](../camera-planning-audit-v001.md) for definitions, sources and proposed coverage. Shot size, angle, movement and cuts are separate decisions. Columbia distinguishes a [zoom](https://filmglossary.ccnmtl.columbia.edu/term/zoom-shot/) from a [dolly move](https://filmglossary.ccnmtl.columbia.edu/term/dolly-dolly-shot/); Adobe recommends planning [tracking movement around its narrative purpose](https://www.adobe.com/creativecloud/video/production/cinematography/camera-shots-and-angles/tracking-shot.html).

The current film uses hard camera changes and a generic 0.16-unit push over the final 72 frames of most new scenes. That repeated three-second drift is not a substitute for directing attention. In some scenes the late-added position keys also sit beside existing rotation cuts; location and rotation need a joint review to avoid an unintended move between different compositions.

The proposed vocabulary is deliberately small:

- **Wide/three-quarter action view:** establish the ball, plant foot, opponent, keeper and goal.
- **Short pan or track:** follow a run or ball when it improves the read; stop or cut before motion obscures decisive contact.
- **Detail insert:** boot/ball, glove, card or apology letter when that detail carries meaning.
- **Reaction close-up or occasional snap zoom:** show realization, outrage or embarrassment at the payoff.
- **Locked two-shot:** give a dry exchange space when the acting carries it.
- **Pull-back/reveal:** expose the scale of the tears and then the fishing callback.

Maintain coherent screen direction through the action, following the [180-degree continuity convention](https://filmglossary.ccnmtl.columbia.edu/term/180-degree-rule/) unless a deliberate change is re-established. A [multiplane scene](https://helpcentre.toonboom.com/hc/en-ca/articles/51906223976339-What-is-a-multiplane) gives flat drawings depth/parallax; it does not create their unseen sides. For a new angle, author the necessary side/three-quarter view or shot-specific drawing. Orbiting the current front-facing art would magnify its weaknesses.

## Repair order and concrete acceptance criteria

1. **Retain the good foundation.** Archive this rejection with its evidence. Keep the accepted designs, scenes and recordings. Reopen new cast construction, new action, pacing and camera coverage. No new style selection or unrelated pilot is needed.
2. **Plan the repaired shots together.** For every consequential shot, specify viewer focus, action phases, opening/ending framing, size/angle, move or deliberate hold, screen direction, needed drawings, and the cut/contact/sound trigger. Use the existing audiovisual script and named events.
3. **Correct one actual demanding film shot first: Rashford's strike and reaction.** Keep the simple controls. Prepare a coherent body/limb surface with matched outline, fill, sleeve overlap and pelvis shape. Use individually fitted weights and corrective drawings where bending demands them. Replace an unsuitable body drawing rather than repeatedly cutting scraps off it. Finish the actual kick and temple-to-scratch action from its planned cameras. This is the first repaired production shot, not a separate pilot.
4. **Carry the established method across the new cast.** Adapt proportions and colors per character asset; check each character's required reach, bend and view. Do not copy numerical weights blindly. Reuse the corrected kick mechanism for Mainoo while authoring distinct timing and acting; then address Haaland, Lammens, Maguire, Martínez and Maresca's required performances. Check background instances as well as named leads.
5. **Retime the full film with motivated coverage.** Fast action, legible contact, recovery, reaction and intentional pauses should contrast. Retain 150–180 seconds through meaningful content. Reposition selected sound events and preserve approved takes rather than regenerating them because the timeline moved.
6. **Internal picture review before the next combined checkpoint.** Inspect every frame of changed contact, bend and turn windows at sufficient size, plus all scene/cut boundaries. Check sleeve→upper arm→elbow→wrist→hand, pelvis→thigh→knee→boot, no residual original limbs, matching skin/kit, planted feet, ball trajectories, prop handoffs, shadows and view compatibility. Evaluate the complete passage at 1× speed and with sound. Record exact coverage and any unreviewed qualities.
7. **Present the repaired complete animatic, then render at full quality only after acceptance.** Numeric checks support this review; they cannot overrule an ugly silhouette or unreadable action. Visible joint failures are blockers, not deferred polish.

The same checks apply to new shots even when an earlier excerpt was approved. A suitable control rig is reusable; proof of one pose is not proof of every cast member or camera angle.

## Workflow correction

The existing benchmark already forbids limbs separating and requires purposeful cuts. The process failure was not simply a missing document: those requirements were not applied consistently during expansion. The shared skill and construction guide now make three points explicit: camera is planned alongside action/sound; expansion to new cast requires reviewing its changed surface construction through the demanded poses; endpoint checks cannot clear visible seams or action timing. These are internal reviews within existing checkpoints, not a new permission ladder. The concrete repairs above remain proposed until authorized.
