# Acting and construction research

Research date: 2026-09-22. Scope: evidence for addressing the reported fixed three-quarter facing, small repetitive gestures and weak reactions. This is direction research, not a review or certification of the rendered film. Recommendations below are production inferences; source findings and their limits are separated explicitly.

## 1. Plan the thought, pose and audience attention

**Primary source:** John Lasseter, *Principles of Traditional Animation Applied to 3D Computer Animation*, SIGGRAPH 1987, sections 2.4, 2.6, 2.10 and 3. [Full paper](https://www.cs.utexas.edu/~fussell/courses/cs384g-fall2013/projects/animator/lasseter.pdf).

**Supported claims:** Staging makes the idea clear and directs attention; competing simultaneous actions can obscure it. Pose-to-pose planning concentrates on acting poses and timing before inbetweens. The paper cautions that automatic interpolation may produce bad paths/intersections. Secondary action must remain subordinate. Expressions changing during a major body move can be missed. Connected thought processes distinguish character acting from unrelated motion.

**Application:** For each important beat, draw the initial attitude, the noticed event and the resulting attitude before animating. Give the reaction a different silhouette, line of action and facing where motivated. Stage the face change before or after the largest move. Let the other character hold or quiet down during the important reaction. Check transitions, not only endpoints.

**Limit:** These are artistic principles and examples, not measured proof that more poses or larger motion always improves a shot. A deliberate hold can be the strongest acting choice.

## 2. Make looking and understanding visible

**Primary practitioner source:** Dana Boadway-Masson, *Facial Animation 101*, Animation Mentor. [Article](https://www.animationmentor.com/blog/facial-animation-101/).

**Supported claims:** Gaze must read correctly from the shot camera, even if its target requires adjustment. Eye darts can be overused; the pauses between them must allow a sense of focus. Eyes/brows generally react before the rest of the face and body; simultaneous large body changes can hide facial changes.

**Application:** Name the actual target of every important look: ball, opponent, teammate or result. Build a readable look, moment of comprehension, then bodily response. Reserve shifts in gaze for new information or changing intent. Judge the eyes at delivery size; moving pupils alone is insufficient if the head artwork still reads as looking elsewhere.

**Limit:** The suggested order is an acting rule of thumb, not a universal physiological law or a fixed frame-offset prescription.

## 3. Separate eye attention from head orientation

**Primary research:** Matthew K. X. J. Pan et al., *Realistic and Interactive Robot Gaze*, Disney Research / collaborators. [Paper](https://la.disneyresearch.com/wp-content/uploads/root.pdf), sections IV-C, IV-D.2 and V-A.

**Supported claims:** Their glance behavior differs from full engagement; in turn-to-glance/engage transitions the eyes reach their target before the slower head. Primary attention can suppress background eye behavior. The paper acknowledges limited emotional range and dependence on interaction distance/duration.

**Application:** Distinguish a suspicious sideways glance from turning to confront someone. For a major discovery, let the eyes acquire the target, turn the head, and involve shoulders/body only as the intention warrants. Avoid a perpetual default camera-facing head while the body supposedly addresses another player.

**Limit:** This is an animatronic gaze system, not a controlled test of 2D comedy. Borrow the attention distinction and timing idea; do not import its robot architecture or random saccade timings.

## 4. Ground the change of pose

**Primary practitioner source:** Brian Mendenhall, *7 Things All Animators Need to Start (or Stop) Doing Right Now*, Animation Mentor. [Article](https://www.animationmentor.com/blog/7-things-all-animators-need-to-start-or-stop-doing-right-now/), points 4–6.

**Supported claims:** For ordinary walking, the planted foot should not slide or lift before support transfers. Lifting a weight-bearing leg requires a preceding transfer of weight. Foot roll can express loading/unloading.

**Application:** Mark which foot carries weight at the start and end of an acting change. If a character pivots to another player, keep the support contact fixed, rotate/roll it intentionally or show a small replacement step. For a shove, kick or prop contact, author the meeting point and resulting movement together rather than hoping independently animated parts coincide.

**Limit:** The contact extension to football interactions is our inference. These walking rules do not prohibit airborne phases in running, hopping or exaggerated comedy. The article's broader exhortation to move every part is not adopted as a requirement for this limited-animation style.

## 5. Change drawings when transformations cannot express the action

**Official production-tool source:** Toon Boom, *About Swapping Drawings*. [Documentation](https://docs.toonboom.com/help/game-studio-24/game-asset-editor/cut-out-animation/about-swap-drawing.html).

**Supported claims:** Cut-out animation commonly uses multiple drawings on a layer. Mouth changes can be difficult with transformations/deformations alone; alternate hand drawings permit poses and rotations without individually animating fingers.

**Application:** Keep the simple body. Add only the shot-required replacements: a genuine profile head, a rear/turned-away head if visible, an appropriate reaching hand, or a compressed impact pose. Use those intentionally during turns; scaling or rotating a single three-quarter face cannot supply its missing profile information.

**Limit:** The head-profile recommendation is a construction inference, not a claim that this documentation prescribes our head design. No complete 360-degree rig or exhaustive expression library is justified before the shots demand it.

## 6. Single-drawing motion transfer has real orientation/contact ceilings

**Primary research:** Harrison Jesse Smith, Nicky He and Yuting Ye, *Animating Childlike Drawings with 2.5D Character Rigs*, 2025 preprint. [Paper](https://arxiv.org/html/2502.17866v1), sections 5.3–5.4 and 7.

**Supported claims:** The authors distinguish their view-dependent system from the earlier 2D Animated Drawings method, including orientation cues such as foot direction. Their own method still struggles with actions pointing toward the camera and certain projection-dependent motions. They explicitly report unrealistic external-object interactions and possible foot sliding from projection or camera movement. Its input assumptions include bipedal, approximately vertical figures without overlapping parts.

**Application:** Use automatic deformation for moves it actually supports. For a turn, inspect face, nose, feet, limb ordering and overlap together. For a kick, handshake, shove or camera-directed reach, prefer a deliberately authored pose/contact correction when retargeting fails. Testing a walking skeleton does not establish expressive acting or reliable interaction.

**Limit:** This research concerns childlike drawings, not our specific caricature rig. It neither proves our renderer has these exact bugs nor proves that adopting the paper's more complex method would solve the film.

## Smallest useful next proof

Production inference from the sources: choose one existing two-character exchange and render its full cause-and-reaction beat. It should demonstrate a motivated change in gaze/facing, an unmistakable attitude change, readable contact/weight transfer where present, and a pause that lets the reaction register. Assess it once silently at phone size and once with sound. Check intermediate frames for head/body contradictions and sliding. Only build additional drawings or controls when this specific beat exposes their absence. This is a proposed proof, not a passed check or authorization to revise the production.
