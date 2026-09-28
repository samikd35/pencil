# Plan coherent motion before interpolating controls

Use this technique guide for consequential movement in any production. It expands the existing staging/motion review; it creates no extra user checkpoint. Preserve accepted artwork and completed films. A simpler construction reduces drawing complexity, not the need to design convincing movement.

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
