# Plan coherent motion before interpolating controls

Use this technique guide for consequential movement in any production. It expands the existing staging/motion review; it creates no extra user checkpoint. Preserve accepted artwork and completed films. A simpler construction reduces drawing complexity, not the need to design convincing movement.

## Choose construction for the shot

Record the construction choice and its action/view limit in the existing shot plan. A successful technique is an option with demonstrated scope, not a replacement for every other technique.

- Use native articulated drawings/layers for gestures, reaches and other movement whose silhouette and clothing joins the rig can support.
- Use a fitted illustrated skin for bounded movement that preserves its artwork and required view. Do not extrapolate a small gesture into unsupported extreme bends.
- Use matched drawings, corrective shapes or a hybrid when the required expression, gesture, view, pose or overlap exceeds the rig's range. Replacements can serve quiet acting as well as intense action; their timing and transitions still need authorship.

Whichever construction is chosen, author the performance between meaningful poses: timing, trajectories, support, overlap and recovery. Pose swaps, camera movement, mouth pulses and moving props do not by themselves fulfill a requested character performance. Preserve intentional holds; do not add arbitrary motion to make every frame different. Verify the actual sequence before describing shots as animated.

For dialogue, volume-driven deformation of one painted mouth is not lip sync. Use separately controllable mouth artwork/geometry with speech closures and vowel shapes timed to the chosen recording. Author body gestures from phrase intent and stress, with independent joints, preparation and recovery; generic coupled arm angles and torso sway do not establish acting. Review speech and body together at normal speed before claiming the dialogue shot works.


## Authoring passes

Use these passes within the existing shot work, iterating when a later finding requires an earlier change. They are not new approval gates.

| Pass | Author and inspect |
|---|---|
| Rough layout and treatment | Focus, silhouettes, scale, coverage, screen direction, depth and intended palette/shading. Test visual cause and response before final assets. |
| Meaningful key poses | Starting attitude, noticed event, response and ending attitude. Design the complete pose and purposeful holds before interpolation. |
| Breakdowns and contact | Trajectories, support, reachable joints, arcs, acceleration, force transfer and overlap; add drawings/correctives where deformation fails. |
| Face/body and editorial timing | Attention and expression changes, gesture accents, anticipation/recovery and cuts against actual sound. Offset parts deliberately rather than moving all controls together. |
| Secondary action | Relevant listeners, eyes, clothing, props and effects, subordinate to the focus. No mandatory constant sway or synchronized blink cycle. |
| Cleanup and final look | Surface continuity, contours, masks, layer order, pops, contacts, shadows and color/shot continuity. Recheck the surrounding edit. |

Codex chooses and revises the performance. Python can set explicit native drawings/keys, controls, exposure, curve handles, camera/material choices and previews; it does not obtain acting from an automatic curve. Use constant holds, linear travel or shaped easing only where they implement intended timing. More in-betweens and uniformly eased transitions are not a default quality improvement.

For ordinary dialogue, determine who notices what, where they look, what they want and how their attitude changes. Author the listener as well as the speaker when their response matters. Coordinate brows/lids/gaze and mouth shape with the chosen view; avoid stacking animated features over conflicting painted ones. Supply closures and vowel shapes for selected speech, but judge expression and articulation separately. A head need not turn continually: an intentional small gaze/lid change can carry the thought.

Give hands a task and suitable palm/back/edge view, grip and contact. For walk-in dialogue, design support transfer, passing feet and a settled speaking stance in the actual 2D projection; sliding a frontal rest drawing sideways is not walking. Preserve purposeful holds and vary the response by scene intention, not by randomizing controls. The following mechanics sequence applies when physical action is needed.

## Work from cause to pose to curve

1. **Study the intended action and view.** Use an actual performance reference for mechanics and the production's selected animation for exaggeration and timing. Record the exact interval and what was actually inspected. Written tutorial advice or a single still is not a substitute for examining movement. Invented actions still need an intentional cause and response.
2. **Write the causal sequence in the existing shot plan.** Identify support/contact, release, travel, impact and recovery as applicable. State what initiates movement, what leads, what follows and what stops it. Choose screen direction, character facing, scale and timing together. Identify deliberate impossible behavior as an artistic choice rather than an accidental contradiction.
3. **Block complete body/object states.** Design the meaningful poses together: feet/hands, pelvis, chest, head and limbs. Give them readable silhouettes and a line of action from the delivery view. A run needs support, passing, push-off and flight; a jump needs preparation, extension, flight, contact and absorption. These are action examples, not a universal pose count. A proxy can help internally, but the actual finished character must demonstrate that its artwork supports these poses.
4. **Connect poses through support and travel.** Establish contact anchors and the body's path before polishing limb swings. Use IK to satisfy chosen geometry, not to invent balance or performance. Specify bend directions in the intended view. Calibrate a neutral pose against the original drawing; then test extreme poses. Reject unreachable targets instead of silently clamping or stretching them to fit incompatible plans.
5. **Add breakdowns and spacing.** Show how force passes through the body: extension before release, continued body descent after landing, then recovery. Author chest/head/limb overlap where appropriate. Only now interpolate and refine arcs. Sinusoids and easing functions may implement a designed cycle; independent periodic curves are not an action plan. Frame count does not establish quality.
6. **Review cause, motion and surface separately.** Check normal-speed movement for intention, weight and timing; inspect contact transitions, silhouettes and garment/limb overlaps frame by frame. Use actual evaluated geometry as well as control points. Compare with the chosen reference and accepted baseline under comparable framing. Record unreviewed playback honestly.

This order follows [Wayne Gilbert's causal body-mechanics approach](https://www.animationmentor.com/blog/animation-tips-tricks-what-makes-or-breaks-a-good-body-mechanics-shot/) and [Jason Martinsen's reference, blocking and breakdown workflow](https://www.animationmentor.com/blog/animating-dynamic-run-cycles/). These are principles to adapt, not a required software or visual style.

## Physical consistency without compulsory realism

- A stationary contact remains fixed in world space. A rolling foot changes its contact point; an intentional slide or moving platform has a different constraint. Do not label a moving foot planted to make a check pass.
- Dynamic balance differs from standing balance. A runner can move outside the current support region because momentum and the next contact matter; do not require the center of mass to stay above a planted foot throughout every action.
- For unpowered flight under constant gravity, use one consistent trajectory model: `x=x0+vx*t`, `y=y0+vy*t-g*t²/2`. For equal-height endpoints, `H=g*T²/8`. Choose scale and two independent quantities; do not tune height, duration and gravity independently. Different landing heights require the general equation. Cartoon exceptions remain available when intentional and readable. [Projectile motion](https://openstax.org/books/physics/pages/5-3-projectile-motion)
- Track a justified center-of-mass estimate when doing physical checks; a hip/root is only a proxy, especially with a large head. Limb motion can change posture in the air without independently accelerating the whole body's center of mass. [Center of mass](https://openstax.org/books/university-physics-volume-1/pages/9-6-center-of-mass)
- Landings, kicks, collisions and catches transfer momentum through contact. Design absorption and follow-through with that contact. An abrupt velocity change may be an impact; an unexplained midair change needs a cause. [Impulse](https://openstax.org/books/college-physics/pages/8-2-impulse)

Keyed Blender controls follow their authored curves. A scene's gravity checkbox does not make those authored controls behave as a simulated body. Use simulation only if it serves the shot; it will not supply good posing, intention or comedy automatically.

## Construction has to support the poses

A frontal cartoon can perform stylized action, but moving a flat painted limb cannot automatically reveal its unseen side, change its hand gesture or supply correct foreshortening. When a necessary pose exceeds the drawing, use a coherent matching pose/view substitution or suitable parts, preserving face/body finish, clothes and shoes. Do not fit a detailed head onto a weaker generic body or reduce the intended action to protect an unsuitable rig. [Toon Boom drawing substitutions](https://docs.toonboom.com/help/harmony-20/advanced/cut-out-animation/about-swap-drawing.html)

For simple planar chains, [pose_geometry.py](pose_geometry.py) supplies a fixed-length two-bone solve with an explicit pole and invalid-target errors. Its self-check and the [captured Bruno calibration check](../productions/Samtoons/videos/002-how-arsenal-won-the-league/research/body-mechanics-v001/check_geometry.py) verify geometry only. It is not a walk/run generator, a balance solver or approval of a finished rig.

## Apply the same method to other actions

| Action | Resolve before polishing |
| --- | --- |
| Walk/run | Support transfer, stride distance versus travel, passing and flight, coordinated arms/chest/pelvis |
| Kick/throw | Support, wind-up, contact or release, transfer to the ball, follow-through |
| Lift/push/carry | Load and grip, body/object contact, effort, release and recovery |
| Turn/fall | Initiation, pivot or flight, rotation, impact and settling |
| Two interacting subjects | Shared contact and event timing; both subjects' responses |
| Mechanism/prop | Driver, constraints, collisions and the resulting motion |
| Abstract graphic | Intended timing and spacing rule; do not impose human anatomy or gravity |

If repeated curve tweaks fail, stop adding amplitude, frames or smoothing. Return to the reference, causal plan, complete poses and construction limits. Keep the failed result, reproduce specific defects, and adopt only corrections supported by evidence. Technical passes cannot replace normal-speed creative review.

Evidence: [primary-source research](../research/body-mechanics-primary-sources-v001.md) and [Samtoons 002 diagnosis](../productions/Samtoons/videos/002-how-arsenal-won-the-league/research/body-mechanics-v001/diagnosis.md).

## Separate travel, pose exposure and camera tracking

For pose substitutions, do not derive the camera target directly from a changing drawing's opaque-pixel centre or discontinuous contact-placement root. Keep planned world travel, local pose/contact offsets and camera framing distinct. Choose drawing, translation and camera cadence together. A drawing held on twos can work; a continuously chasing camera can turn held world poses into unintended screen-space oscillation. Smoothing the camera alone does not repair discontinuous character travel, and smoothing a rigid planted drawing can create foot sliding. Use registered breakdown drawings or suitable local deformation when continuous travel requires it.

Inspect successive screen-space character landmarks and stationary background landmarks as well as world-space contacts. Separate camera-induced pulses from pose changes and check encoded frame timestamps. The [Samtoons jitter diagnosis](../productions/Samtoons/videos/002-how-arsenal-won-the-league/research/temporal-jitter-v001/diagnosis.md) demonstrates this failure; the later v003 acceptance and scoped evidence are recorded below.

## Reusable whole-character action proof

Samtoons 002's [eight-second pose action proof](../productions/Samtoons/videos/002-how-arsenal-won-the-league/artifacts/pose-action-v003/README.md) is a useful construction example for illustrated action. The user positively reviewed its complete-character running/jumping and asked to preserve this method for future projects. This does not prescribe football artwork, an eight-second duration, or this action for every production.

1. Start from the accepted **whole character**: face, body proportions, clothing, footwear and outline finish. Supply matching complete action drawings where the original neutral art cannot deform convincingly. Preserve original deliveries; derived drawings need their own inspection.
2. Author coordinated silhouettes for the actual demanding movement, including opposite stride halves and preparation, release, impact and recovery. Confirm the two stride halves really exchange arm/leg roles. Use the smallest representative playable excerpt before detailed animation.
3. Keep pose selection/exposure, body travel, support constraints and camera editable separately. Native drawing substitutions may use a single keyed selector; they are not automatically a freely deformable skeletal rig.
4. Register a stable anatomical landmark across drawings. Track an authored travel path rather than the changing silhouette's pixel centre. Match camera cadence to that travel. Where rigid drawings would slide a planted foot, use bounded local deformation or authored breakdown drawings; preserve the upper-body artwork and inspect the actual correction.
5. Test the failed property: screen-space body oscillation, background speed pulses and evaluated contact geometry. Test both the old failing scene and the revised scene. Numerical checks locate implementation faults; normal-speed playback determines whether the action is pleasing.
6. Preserve user-approved action and artwork when fixing temporal faults. Record acceptance by aspect so a camera defect does not cause a needless character redesign.

Evidence: v002's action direction received positive user feedback, with a requested temporal correction. v003 keeps the same pose images/exposures and adds registered horizontal travel, independent tracking and keyed lower-body compensation. The steady-run regression fails v002 and passes v003; the user subsequently accepted v003 as almost perfect and better than video001. New character/action adaptations still require review. This fixed-view method requires new drawings for unseen angles, extreme action or silhouettes that exceed the small deformation range. Do not blindly propagate this film's landmark coordinates, mesh dimensions, stride speed or corrective amount.

When layering native corrective shape keys, explicitly initialize each correction from the same Basis coordinates. A newly added key may otherwise inherit another correction's geometry, coupling axes or controls. Evaluate the actual deformed contact vertices in the demanding-motion check; target coordinates alone missed this during the Samtoons chase adaptation.


When replacing a pose library on a reused control, reset the selector property’s hard and soft limits to the new drawing count. Blender can clamp keyed values to inherited limits even when the F-curves contain the requested indices. Evaluate every intended pose index and visible drawing across both stride halves; checking only travel/contact targets misses an unvisited drawing. Samtoons002’s CP03 Pep adaptation reproduced a four-pose limit suppressing indices 4 and 5; resetting the range to 0–5 restored all 96 intended frame selections. See the [saved-scene regression](../productions/Samtoons/videos/002-how-arsenal-won-the-league/scripts/check_pep_shot_v001.py) and [captured selector check](../productions/Samtoons/videos/002-how-arsenal-won-the-league/artifacts/animation-v001/CP03_pep/selector-check.json). This fixes that adaptation’s selector, not the earlier rejected chase’s artistic gait.
