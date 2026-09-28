# Coherent motion before deformation polish

Research date: 2026-09-17. Scope: a general production method prompted by Samtoons 002's rejected run/jump tests. This is primary-source research and a proposed application, **not an inspection verdict on the current scripts**. Tutorial webpages and documentation were read; embedded demonstration videos were not watched.

## What needs to change

**Research synthesis:** character motion should be authored as a coordinated sequence of intention, support, force, travel and recovery. Good drawings, connected joints, valid limb lengths and smooth curves are separate achievements; they do not establish convincing movement. Increasing an arm's amplitude or adjusting one knee cannot repair a missing whole-body action plan.

Wayne Gilbert's first-party Animation Mentor article specifically teaches analyzing the causes of movement, deciding what leads and follows, and designing breakdowns that explain the transition. He permits exaggeration while requiring consistent forces. This supports changing the authoring order, rather than abandoning the successful artwork. [Gilbert: body mechanics](https://www.animationmentor.com/blog/animation-tips-tricks-what-makes-or-breaks-a-good-body-mechanics-shot/)

## Evidence that constrains the solution

**Run:** Jason Martinsen teaches starting from reference, blocking stride/down/passing/push-off poses, then adding breakdowns and overlap before polishing. His run includes intervals with neither foot grounded. These are coordinated body states, not independent oscillations. The article does not prescribe a universal cycle duration or amplitude. [Martinsen: dynamic run cycles](https://www.animationmentor.com/blog/animating-dynamic-run-cycles/)

**Jump:** Martinsen's jump teaching distinguishes preparation, extension/takeoff, airborne action, contact, compression and recovery. Legs can lead and trail rather than moving identically; hips, torso and head have deliberate offsets. This is an example to analyze, not a requirement that every jump use the same crouch or hero landing. [Martinsen: jump and land](https://www.animationmentor.com/blog/tutorial-animate-a-jump-and-land/)

**Flight:** after release, an unpowered projectile with negligible air resistance follows constant horizontal velocity and gravitational vertical acceleration: `x = x0 + vx*t`, `y = y0 + vy*t - g*t²/2`. Its apex is a moment of zero vertical velocity, not an arbitrary hover. These assumptions exclude powered flight, collisions and deliberate cartoon exceptions. [OpenStax: projectile motion](https://openstax.org/books/physics/pages/5-3-projectile-motion)

**Whole-body mass:** internal movements can relocate limbs while net external forces govern the system's center-of-mass trajectory. Moving arms in midair does not independently accelerate the entire character forward. A pelvis/root control is only an approximation of center of mass, especially with an oversized head or moving limbs. [OpenStax: center of mass](https://openstax.org/books/university-physics-volume-1/pages/9-6-center-of-mass)

**Landing:** momentum must change through impulse. Increasing the time over which the ground stops a falling person reduces average impact force; bent knees illustrate this. Therefore an animation's contact, continued body descent, compression and recovery should belong to one event. A generic easing function is not evidence of impact absorption. [OpenStax: impulse](https://openstax.org/books/college-physics/pages/8-2-impulse)

**IK:** Blender describes inverse kinematics as rotating a bone chain to reach a target; poles guide bend orientation, and stretch optionally changes length. Consequently, successful target reaching is a geometric result, not proof of balance, propulsion or readable action. [Blender: IK constraint](https://docs.blender.org/manual/id/5.0/animation/constraints/tracking/ik_solver.html)

## Proposed production method

The following is our application of the evidence, not a quoted studio standard:

1. **Choose the action and view before programming motion.** Gather an actual performance reference plus the selected animation benchmark. Annotate contact/release frames, direction, major poses and timing. Record what was actually viewed. Reference can inform a fictional gag without limiting its exaggeration.
2. **Make a short causal plan.** For each phase state what supports the subject, what initiates movement, where it travels, and what stops or redirects it. Draw the trajectory and contact sequence together. Set one shot scale and time basis; do not tune gravity, jump height and duration independently.
3. **Block complete poses.** Pose feet/hands, pelvis, chest, head and limbs together at the meaningful events. Review their silhouettes from the delivery camera. Use a simple proxy to solve mechanics if helpful, but transfer back to the approved complete character early enough to reveal view and deformation limits.
4. **Solve transitions around contacts.** A stationary, non-sliding contact stays stationary in world space while the body moves over it; foot roll changes the contact point. Mark intentional slips, rolls or moving surfaces explicitly. Design takeoff and landing velocity changes through the relevant support interval. Do not clamp unreachable endpoints silently or stretch limbs merely to make conflicting trajectories fit.
5. **Add overlap after the action reads.** Use curves to refine spacing and limb arcs between designed states. A periodic function can interpolate a proven cycle; it should not invent the performance. Keep facial detail and secondary motion subordinate to the action.
6. **Review motion and construction separately.** Inspect native-speed playback, slowed transitions and consecutive frames. Compare the same demanding action against the baseline and benchmark. Preserve accepted artwork while revising motion; document any necessary view-specific drawing change.

## Applying it beyond this jump

These are planning prompts, not mandatory human physics for every production:

| Action | Causal questions before interpolation |
| --- | --- |
| Walk/run | Which foot supports each interval? Where are transfer and flight? Does travel agree with stride spacing? |
| Kick | Which leg supports the body? When does the striking foot meet the ball? What continues after impact? |
| Lift/push | Where is the load? When does grip/contact establish? How do body and object respond together? |
| Turn | What initiates rotation? Is it a planted pivot, stepping turn or airborne turn? How does rotation stop? |
| Interactions | Who supplies the force? Do both subjects share the same contact point and event timing? |
| Props/non-character motion | What drives, constrains or collides with the object? For abstract graphics, what timing/spacing rule makes the transition intentional? |

## Respect the drawing's capabilities

Toon Boom explicitly uses drawing substitutions for mouths and hands because transformations/deformation alone can be impractical. Its rigging guidance also separates hand positioning from unwanted deformation. This supports preserving a good drawing while supplying specific alternate poses when needed. [Drawing substitutions](https://docs.toonboom.com/help/harmony-20/advanced/cut-out-animation/about-swap-drawing.html), [Rigging deformers](https://docs.toonboom.com/help/harmony-24/advanced/deformation/about-rigging-with-deformers.html)

**Inference for our planar artwork:** rotating a painted frontal limb in its image plane cannot automatically supply an unseen side, convincing foreshortening or the correct overlap order. When the shot requires those, use a matching view/pose drawing or a suitable layered construction. Do not disguise the limitation with stronger warping. Alternatives cost drawing/setup time; limiting staging costs action range. Neither requires replacing the whole character. Toon Boom's production interview recommends studying the storyboard and building only required capabilities, with consistent turnarounds. [Matt Watts: rig design and scope](https://www.toonboom.com/training-punk-rig)

## Checks and their limits

Measure contact drift, ground penetration, limb reach, trajectory continuity and unexpected velocity jumps on the **evaluated scene**, with shot-specific tolerances. Visualize paths of the root, feet, hands and head; Blender already provides motion paths for object origins and bone joints. [Blender: motion paths](https://docs.blender.org/manual/en/latest/animation/motion_paths.html)

These checks can expose contradictions. They cannot certify appeal, perceived weight, recognizability, comedic timing or benchmark quality. A mathematically smooth path can still look wrong; a deliberate smear or impossible hold can work. Log justified stylistic exceptions and require visual review. A reusable lesson is the diagnosed cause, supported correction and demonstrated result—not merely a new version number or passing geometry check.
