# Toon 3D and drawn-face hybrids for Samtoons

Research: 23 September 2026. Bounded method study; no assets, scenes, pipeline code, software or dependencies changed. Read against [benchmark v003](../../benchmark-v003.md) and [the previous Blender Python study](../python-animation-practice-v001.md).

**Finding:** A simple 3D body with an authored caricature head/face is a credible alternative when turns, connected limbs and football contact dominate. It does not make good likeness or acting automatic. The strongest production evidence is a carefully designed 3D pipeline with considerable artistic control; the most direct drawn-face evidence is a creator's smaller demonstration. Neither establishes that Codex can already deliver the Samtoons benchmark.

## Three useful primary examples

### 1. Wing It! — strongest production evidence for 3D made to read as 2D

Blender Studio explicitly describes a **full 3D pipeline with extras**, rendered in EEVEE. Its shading lead says that design, flexible deformation and animation must agree; perspective changes can break the illusion. They suppressed many shadows, used simplified shadow proxies where needed, and built custom outlines. Some outline/silhouette defects still required corrections on individual frames. This is unusually relevant evidence against assuming that a toon shader finishes the problem. [Simon Thommes, *Shading and Rendering of Wing It!*, 5 October 2023](https://studio.blender.org/blog/shading-and-rendering-of-wing-it/).

The character treatment derives outline, rim and simplified shading information from the silhouette and camera. Surface normals alone were insufficient for the desired appearance. The team also advanced its noise pattern with the held animation to avoid texture swimming. These are deliberate aesthetic choices, not properties inherent in a 3D model. [Thommes, *Cartoon Character Shading with Geometry Nodes*, 21 November 2023](https://studio.blender.org/blog/cartoon-character-shading-with-geometry-nodes/).

The character rigger separately documents mouth construction using UV-space deformation, curves deforming flat geometry, and CloudRig. This supports faces that remain highly graphic within a 3D production; it is **not** evidence that the film simply attached Grease Pencil drawings to conventional heads. [Demeter Dzadik, *Rigging With Geometry Nodes on Wing It!*, Blender Conference 2023](https://conference.blender.org/2023/presentations/1909/).

**Suitability:** Best production reference for expressive 3D with a 2D result. Its entire technical system is too large a starting point for one Samtoons proof. Transfer the controlled silhouettes, flexible facial shapes and selective shadows first. This last recommendation is our inference, not the production's prescription.

### 2. LaurenLArtist's hybrid demonstration — closest documented split of body and face

The original creator states that the visuals were made in Blender, with a new Grease Pencil face drawn on geometry for each face frame, while everything else was rigged and animated conventionally. The creator chose this to draw extreme expressions without building a complex facial rig. These statements belong to the original poster, LaurenLArtist; other commenters' descriptions of their own methods are not evidence about this demonstration. [Original demonstration and creator explanation, 13 December 2021](https://www.reddit.com/r/blender/comments/rfk76h/2d3d_hybrid_animation_using_grease_pencil_and/).

**Suitability:** Most direct evidence for a rigged-body/drawn-face experiment. It exchanges facial-rig setup for drawing work. The account does not establish likeness preservation, multi-angle reuse, football mechanics, current API compatibility or production throughput. It is evidence of a documented method, not a validated Samtoons production system.

### 3. Lightning Boy Studio's character workflow — concrete model-to-toon construction

The studio's own walkthrough covers concept/T-pose preparation, simple face modeling, outlines, light control, UVs, texture painting and material adjustments. Its chapter list also includes correcting disappearing outlines. The demonstration uses Blender 2.91 and the studio's Lightning Boy Shader 2.0. [*Toon Shaded Character Guide, from Modeling to Final Shading*, 9 February 2021](https://www.youtube.com/watch?v=spz6bpGYJZQ).

**Suitability:** Useful for understanding the modeling and look-development decisions needed before a toon character becomes usable. This research inspected the published description and documented chapters, not the entire video or supplied files. It does not verify the product in Blender 5.2, recommend purchasing it, or prove the shader transfers likeness automatically. Start with Blender's built-in tools for the experiment.

## Ranked routes for this specific need

This ranking is a research inference from the requirements and documented mechanisms, not measured production performance. It can change after the same representative shot is tested.

| Rank | Route | What it buys | Main cost and failure mode |
| --- | --- | --- | --- |
| **1 — test first** | Simple rigged 3D body and head mass; authored facial shapes/drawings; sparse drawn accents | Body depth, coherent overlap and reusable foot/hand targets, while retaining graphic faces and the option to replace an extreme expression | Likeness still needs deliberate head/hair proportions and views. Drawings attached to a surface do not automatically stay appealing through turns; profiles and expression changes must be authored. |
| **2 — if varied views recur** | Fully modeled caricature with a small facial rig, rendered with restrained toon shading | Most reusable camera coverage and environment integration once a recurring player is built well | Greatest initial likeness/topology/face-rig work. Ordinary 3D facial anatomy or volume-preserving deformation can be unappealing in a deliberately distorted caricature. Shot corrections remain legitimate. |
| **3 — retain where it fits** | Existing 2D construction plus purpose-specific replacement views and poses | Closest control over the drawn design; low setup when an action is largely in one view | A single drawing stretched through every turn lacks the missing silhouette and overlap information. More deformation controls cannot invent those views. This is a limitation of that construction, not of all vector or Grease Pencil animation. |

The routes can share a 3D pitch, room or prop layout. Choosing 2D actors does not require flat or inconsistent environments; choosing 3D actors does not supply appealing environment design. Blender's own hybrid storyboard practice combines drawings with 3D spaces to establish scale and spatial relationships. [Studio storyboard workflow](https://studio.blender.org/tools/artist-guide/pre-production/storyboard).

## What 3D helps, and what still needs decisions

- **Connected limbs:** Weighted mesh deformation and segmented B-Bones offer continuous geometry rather than detached limb pieces. B-Bones follow curved segments; increasing segment count increases calculation cost. A connected mesh can still crease, collapse or intersect. Armature Preserve Volume reduces a common joint-volume loss, but its documented extreme-rotation discontinuity makes it a control to test, not a universal fix. [Blender 5.2 B-Bones](https://docs.blender.org/manual/th/5.2/animation/armatures/bones/properties/bendy_bones.html), [Blender 5.2 Armature modifier](https://docs.blender.org/manual/id/5.2/modeling/modifiers/deform/armature.html).
- **Football contact:** The previous study already establishes IK targets. The useful change is that body, ball, feet and floor can occupy one coherent space. The artist still decides support intervals, weight transfer, impact, overlap and recovery. A planted target can coexist with a weightless-looking performance. This is our inference; no researched source demonstrates our required football shot.
- **Lines:** Current Line Art derives selected edge types and visible contours from a camera, supports occlusion choices, and can be baked. Several modifier instances can repeat costly scene-occlusion work. These controls support automation, but provide no guarantee of stable appealing line topology across a turn or near-contact. Test the actual encoded motion, including wrist/sleeve, boot/ball and cheek/nose overlaps. [Blender 5.2 Line Art manual](https://docs.blender.org/manual/id/5.2/grease_pencil/modifiers/generate/line_art.html).
- **Shadows:** A minimal EEVEE Shader to RGB/Color Ramp setup is a documented way to obtain toon bands, but the manual warns about interactions with some shading effects, noise and render passes. Use a simple, controlled light setup initially; decide the desired floor contact independently from decorative facial shading. Do not copy Wing It's 2023 renderer internals on the assumption that they are a present-day recipe. [Blender 5.2 Shader to RGB manual](https://docs.blender.org/manual/id/5.2/render/shader_nodes/color/shader_to_rgb.html).
- **Python/Codex:** Existing documented APIs can construct and key Blender data; the prior note covers that foundation. Wing It's shader article additionally describes script-driven shot properties, providing a concrete example of automation supporting look control. Neither source claims automatic character design or acting. Keep the experiment editable and inspect the generated result. Automating a wrong pose or head shape makes it repeatable, not correct. [Prior local evidence and compatibility limits](../python-animation-practice-v001.md), [Wing It character-shading controls](https://studio.blender.org/blog/cartoon-character-shading-with-geometry-nodes/).

## Smallest discriminating experiment

**One already-approved player, one ball, a simple pitch patch and one 4–6 second technical acting/contact beat.** This is a proposed isolated method test, not a new fictional football incident or a production revision.

1. **Before animation, prove the identity.** Show front, three-quarter and near-profile head/body poses in the intended vertical framing. Preserve the selected hair, facial proportions, kit and silhouette. Use the same player design for comparison with the current 2D route. If the 3D head mass already loses the caricature, fix or reject that construction before adding controls.
2. **Use one short connected action:** notice an incoming ball, shift onto the support foot, control/pass it, settle, then look toward an off-screen person with a changed attitude. This tests gaze/body agreement, bent elbows and knees, a boot/ball contact, weight transfer and recovery. Reuse this timing and staging for a comparison route; do not make one candidate more entertaining to hide construction weaknesses.
3. **Render the same animation from the planned three-quarter view and one short alternate view.** First use flat colors and restrained shadow/line treatment. Only the face variant needs to differ when comparing authored drawn features against a small 3D facial setup. Do not build both full character systems in advance.
4. **Judge likeness, motion and cost together:** normal-speed intention; consecutive contact and turn frames; native-size silhouette/line crops; number of unique drawings, per-view fixes and surface corrections; and wall-clock setup/correction time. A still render or a freely spinning model cannot establish this result.

**Decision rule:** Continue with the hybrid if it improves continuity and contact while retaining recognizable faces with manageable view corrections. Prefer more 3D facial construction only when repeated changes of view make the drawn-face repairs the larger burden. Retain purpose-built 2D poses when they reach the required performance more directly. None of these decisions requires a new renderer, production framework, full cast, universal rig or paid shader first.

## Evidence limits

This note is a primary-source documentation review. It does not claim continuous playback analysis of these examples, a new rendered Samtoons test, benchmark parity, or runtime validation. Some official pages could only be read through their indexed text; several official manual results used localized URLs with the relevant content in English. Access-restricted production downloads were not obtained. Historical setups are identified by their actual versions. Later local v004–v006 work was built and rendered with Blender 5.2.0; the newly proposed techniques have not been runtime-tested in this study.

Nothing here establishes the production method of 442oons or the user-supplied Neymar/Messi Short. Their observed performance remains useful independently of software attribution.
