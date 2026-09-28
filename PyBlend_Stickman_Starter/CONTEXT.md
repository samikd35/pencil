# PyBlend

PyBlend is a reference-driven animation authoring context that bridges AI- and
code-assisted creation with editable Blender animation workflows.

## Language

**Animation Authoring System**:
The near-term PyBlend product: a system that turns visual references and creative direction into an editable Blender animation project and a preview render.
_Avoid_: One-click video generator, automatic movie generator

**Editable Animation Project**:
The primary authored result, preserving inspectable and adjustable drawings, controls, timing, staging, and scene structure rather than only rendered pixels.
_Avoid_: Output video, generated clip

**Movie-Creation North Star**:
The long-term goal of making complete animated stories substantially easier to create through an AI/code bridge into Blender and animation tooling.
_Avoid_: V1 scope, immediate product promise

**Input Envelope**:
The version-specific boundary defining which Creator inputs PyBlend requires, accepts, may infer through approval, or refuses before production.
_Avoid_: Permanent product limitation, best-effort guessing

**Shot**:
One uninterrupted camera view between two cuts and the primary unit PyBlend authors and validates. A Shot belongs to a Scene and contains its own staging, action, camera behavior, and timeline.
_Avoid_: Scene, movie, arbitrary clip

**Approved Shot**:
A Shot that has passed its required quality gates and is accepted as ready for use in a Scene while remaining editable and revisable.
_Avoid_: Finished movie, immutable final output

**Success Gate**:
An independent pass-or-fail condition an authored Shot must satisfy before approval, using automatic evidence for technical facts and Creator review for visual or acting judgments. Every required gate must pass.
_Avoid_: Overall quality score, averaged trade-off

**Gate Record**:
The retained evidence and explicit Creator pass-or-fail decision for one Success Gate, including the revision effort used to reach it.
_Avoid_: Implicit approval, conversational memory alone

**Shot Package**:
The deliverable for an Approved Shot, containing the editable Blender project, a reviewable render, a reproducibility manifest, and the approved supporting assets used to author it.
_Avoid_: Video export, `.blend` file alone

**Scene**:
A story section occurring within a coherent place and period, composed of one or more Shots.
_Avoid_: Shot, Blender scene

**Character Model Sheet**:
An approval artifact that establishes a character's consistent views, proportions, colors, important expressions, and other appearance decisions before animation. It may include clearly identified views inferred from incomplete references.
_Avoid_: Character Asset, raw reference image

**Character Asset**:
An approved, reusable animation-ready representation of a character, including its Grease Pencil artwork and the controls or alternate drawings needed to author Shots consistently.
_Avoid_: Character Model Sheet, per-shot character generation

**Semantic Part**:
A named piece of a Character Asset whose artwork, ownership, depth, controls, and allowed changes are explicit and stable across runs.
_Avoid_: Coordinate region, color guess, whole-image difference mask

**Motion Envelope**:
The independently declared image or scene region within which a named Semantic Part may change during a certified motion interval; every pixel outside it remains locked.
_Avoid_: Post-hoc difference mask, permission for unrelated body motion

**Drawing Exposure**:
A frame range that displays one approved drawing state without changing that drawing's geometry, equivalent to holding a drawing on the timeline.
_Avoid_: Smooth in-between, duplicated image file per frame

**Hidden Artwork**:
Authored surface that sits behind a foreground Semantic Part and prevents gaps when an attached moving part reveals an overlap.
_Avoid_: Background fill, visible seam patch, inferred connector pixels

**Correction Drawing**:
An approved local drawing substitution used where a bounded transform cannot preserve silhouette, volume, topology, or occlusion quality.
_Avoid_: Whole-character regeneration, untracked paint-over

**Alternate Drawing**:
An approved complete character drawing used when an action changes silhouette or topology beyond the safe range of local deformation and Correction Drawings. It must retain explicit pose ownership and compile to an editable representation.
_Avoid_: Unapproved full-character regeneration, anonymous frame replacement

**Style Guide**:
A compact visual approval artifact that fixes the palette, line treatment, shading, shape language, texture allowance, and character-to-environment relationship used by a PyBlend project.
_Avoid_: Text-only style prompt, brand guide

**Shot Plan**:
An approval artifact that decomposes a Scene into named Shots with intended action, framing, timing, dialogue cues, and continuity before detailed animation begins.
_Avoid_: Finished animation, unstructured story prompt

**Animatic**:
A timed preview assembled from storyboard images, rough camera changes, dialogue, and temporary sound to validate a Shot Plan before detailed animation.
_Avoid_: Final render, finished Shot

**Environment Asset**:
An approved, reusable layered 2.5D representation of a location, arranged to support limited depth, occlusion, parallax, and consistent reuse across Shots without claiming full 3D reconstruction.
_Avoid_: Flat background image, generated 3D set

**Motion Brief**:
The direction for how action should unfold within a Shot, combining required written intent with optional pose, video, timing, and audio references.
_Avoid_: Animation data, rig controls

**Pose Reference**:
Creator-supplied clean, style-matched character artwork that communicates a desired body pose for a Shot. Raw photographs and rough sketches must be cleaned outside PyBlend before submission.
_Avoid_: Generated Pose Drawing, motion-capture data

**Key Pose Plan**:
An approval artifact identifying the important character poses, acting beats, and their timing before rig motion and in-between drawings are produced.
_Avoid_: Motion Brief, finished animation

**Targeted Revision**:
A requested change limited to a named Shot element and time range, preserving unrelated approved work.
_Avoid_: Whole-shot regeneration, manual patch

**Lock**:
An explicit protection on an approved asset, pose, timing choice, camera choice, or other authored result that later revisions must preserve.
_Avoid_: Finalization, file permission

**Adopted Edit**:
A manual Blender change explicitly accepted as the new PyBlend-managed baseline for later revisions.
_Avoid_: Untracked scene mutation, automatic round-trip merge

**Creator**:
The primary PyBlend user: a solo, AI-comfortable storyteller who can direct work in ordinary language but is not expected to know Blender, rigging, or professional animation workflows.
_Avoid_: Blender expert, studio pipeline engineer, animator by default
