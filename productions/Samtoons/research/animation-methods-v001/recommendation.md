# Choosing a better animation method for Samtoons

**Decision update — 23 September 2026:** The user rejected both implemented comparison options and selected the existing v006 2D puppet for improvement. This document remains a historical proposal. The current direction and diagnosis are in [the v006 audit](../puppet-v006-audit/README.md).

23 September 2026 — research and proposed experiments, **not an adopted production change**.

## Recommendation

Test a **simple three-dimensional caricature body with deliberately drawn facial shapes and a controlled 2D finish**, against a **proper 2D rig with replacement drawings**. Use the same short performance and likeness target. Keep 3D-assisted Grease Pencil drawing as the fallback when the 3D result loses the graphic appeal.

This is a recommendation to test competing representations, not a claim that 3D is inherently better or that any method guarantees benchmark quality. We have demonstrated connected controls locally; we have not yet demonstrated the required combination of likeness, appealing deformation, expressive acting and economical revision.

## What actually went wrong here

The latest reconstruction changed the skeleton and motion but retained artwork extracted from a particular posed illustration. That was an incomplete reconstruction of the animation asset.

- [The tracing script](../../videos/003-barca-emergency-meeting/scripts/trace_call_reference_v003.py) starts with `call-pose.png`, separates regions using masks, and extracts the existing grip and bent forearm. The source contains one solution to silhouette, overlap and shading.
- [The art construction](../../videos/003-barca-emergency-meeting/scripts/build_call_performance_v004.py) gives entire hand and forearm regions a single controlling bone. It reconstructs upper sleeves and blends some joins, but does not supply alternate finger/grip silhouettes or unseen views.
- [The new foundation](../../videos/003-barca-emergency-meeting/scripts/build_call_performance_v006.py) genuinely builds and animates a new connected skeleton before attaching that artwork. The unchanged-motion checks verify that attachment preserves the skeleton. They cannot verify that the visible sleeve, wrist and hand form an appealing pose.

The [v006 hand crops](../../videos/003-barca-emergency-meeting/artifacts/staging-v001/call-performance-v006/focused-hands.png) make the mismatch visible: the same drawn grip travels with the prop while sleeve/cuff contours change around it. The current asset has a narrower useful range than the motion controls. That architectural limitation is established by the code; the exact contribution of weights, contour construction and depth ordering to each bad frame still needs a controlled test.

A line skeleton has no thickness, clothing, finger silhouette or hidden surface to maintain. Its clean movement therefore cannot certify a finished character. The missing foundation is **a character designed to perform the required poses**, plus authored timing and acting. More bones alone cannot supply this.

## What the benchmarks require

The existing [benchmark analysis](../../benchmark-v003.md) and [Bayern frame study](../reference-bayern-v001/analysis.md) remain the visual target. This research also inspected the native [prop/microphone pose](../reference-bayern-v001/details/frame-3192.png) alongside our weak hand crops. The benchmark uses simple readable limb shapes, clear grips and strong facial attitude. Its strength is not constant motion or anatomical realism.

We have not established the software or rig used by those benchmark creators. The methods below are ways to pursue the observed result, not claims about how 442oons constructed it.

## The three serious alternatives

| Method | How it works | Why it could fit | Work it does not remove |
| --- | --- | --- | --- |
| **1. A 2D rig with replacement drawings** | Deform an arm within its useful range. Switch to an authored hand, arm, head or body drawing when the silhouette or view needs to change. Use a few transitional drawings where necessary. | Closest to the selected flat caricature look; strong control of exaggerated expressions and poses. | Someone must design the missing views and shapes. A larger library of the same neutral pose is not a solution. |
| **2. Simple 3D characters rendered to look drawn** | Give the body, head, hands and clothes actual volume. Animate a rig; add graphic facial shapes/drawings, outlines and restrained shading. | Most promising new test for repeated turns, connected surfaces, prop contact and shared camera space through Python. | Appealing modeling, likeness across views, joint deformation and the drawn finish. A generic 3D human with a cartoon shader will not meet the target. |
| **3. 3D-assisted 2D drawing** | Animate simple 3D forms for perspective, weight and contact. Use them to guide authored Grease Pencil key drawings, changing silhouettes and expressions freely. | Preserves drawn exaggeration while reducing guesswork about hands, foreshortening, scale and camera movement. | Drawing and cleanup remain substantial. Automatically tracing the 3D result is not equivalent to designing good animation. |

### Evidence for 2D rigs with drawing changes

Toon Boom's own teaching explicitly includes drawing substitutions as part of cut-out animation. Its rigging documentation separately explains that a hand may need to follow an arm deformer without being distorted by it. These are complementary tools: deformation for continuous motion, different drawings for different shapes. [Drawing substitutions](https://learn.toonboom.com/modules/layout-and-posing/topic/about-swapping-drawings1?c=32), [attaching drawings to deformers](https://docs.toonboom.com/help/harmony-21/premium/deformation/about-rigging-with-deformers.html).

Mercury Filmworks' account of *The Duke's Game* describes action-specific construction, responsive deformers, rough drawings for finding the performance, and 3D environments where useful. It also describes reusing rendered views of 3D props inside the 2D setup. The transferable lesson is to build for the actual performance and keep the animator's controls manageable. This is evidence from Harmony, not proof of identical Blender features. [Production interview](https://www.toonboom.com/making-of-the-dukes-game-part-2-rigging-animation-comp).

For Blender, the proposed implementation would use drawing exposures or keyed object visibility, native deformation where suitable, and explicitly authored transitions. Blender documents stroke interpolation, but that operation is not an anatomy, acting or missing-view generator. [Blender 5.2 animation tools](https://docs.blender.org/manual/it/5.2/grease_pencil/animation/tools.html).

### Evidence for volume with a drawn finish

Blender Studio's *Wing It!* demonstrates a deliberately designed 3D production with a 2D appearance. It also reports frame-specific silhouette corrections, so it is evidence of potential, not automatic polish. [Production account](https://studio.blender.org/blog/shading-and-rendering-of-wing-it/).

The proposed Samtoons version is smaller: a continuous simple body, a head and hair silhouette shaped for the identity, controlled hand poses, and authored graphic facial features. Large turns must change the visible facial arrangement; sliding one flat face across a head would repeat our current mistake. A fully modeled face is an alternative if drawing changes become more work than the facial rig.

In *House of Chores*, Blender Studio combined 3D forms, projected Grease Pencil lines, painted color, rigged elements and drawn animation. A perspective-heavy waterwheel used 3D with Line Art. The trumpeter used drawn animation. This supports choosing a method per element within one Blender film. Our proposed character draw-over workflow is an adaptation, not a claim that the example already solves football caricatures. [Production breakdown](https://studio.blender.org/blog/house-of-chores-testing-grease-pencil-30/).

See [the detailed 3D/hybrid study](toon-3d-sources.md) for construction, shading and current-version caveats.

## What newer research adds

Two directions deserve attention after the controlled Blender comparison:

- **DrawingSpinUp:** builds a 3D proxy from a drawing and restores a drawn appearance after animation. It is relevant evidence that a drawing can become more than a flat puppet. Its published subjects and evaluation do not establish the likeness, expressive fingers and exact contacts required here. [Authors' paper and examples](https://lordliang.github.io/DrawingSpinUp/).
- **ToonComposer:** uses reference art and sketch guidance to generate colored inbetween video. It may help finish a short authored movement, but the documented output is raster video, not a controllable Blender character. [Official project](https://github.com/TencentARC/ToonComposer).

The [paper survey](papers-and-assistance.md) also assesses Monster Mash, Animated Drawings, AniClipart, LiveSketch, ToonCrafter, AniDoc and related work. The full DrawingSpinUp and ToonComposer implementations have substantial runtime requirements and no verified local Mac route in this study. No models were downloaded or installed. They are candidates for isolated assistance, not dependencies for the next proof.

Image generation can help create a coherent design and the specific missing pose/view references. The output still needs consistent proportions, hidden-part construction and deliberate conversion into editable assets. Tracing a pleasing illustration only reproduces what is visible in it; it does not create the missing character structure.

## What Codex should do differently

Work from **the intended performance to the required artwork**, rather than generate a finished neutral picture and then invent motions it might tolerate.

1. Establish the action, attitude, key poses, contact moments and framing.
2. Choose the simplest representation that can actually express those poses. Identify which parts deform, which drawings change, and which forms need depth.
3. Build and inspect those important poses with the recognizable design attached. A successful naked skeleton is only an intermediate check.
4. Use Python for consistent dimensions, scene construction, keys, constraints, drawing switches, cameras, rendering and repeatable checks. Author the timing, expressions and silhouettes; do not expect interpolation to decide them.
5. Evaluate the moving result at normal speed, then inspect the weak transitions closely. Keep technical continuity checks separate from visual acceptance.

This is a change in representation and authoring decisions, not a request to add another generic framework. A capable rig can still perform badly; a beautiful still can still be impossible to animate economically.

## The smallest useful experiment

**One familiar caricature, one 4–6 second action, two constructions.** Keep identity, framing, staging, timing and any reused audio identical. The character is a test subject, not a restriction on future casts.

The action should require an open hand to reach for a prop, close around it, lift it across the body, turn the wrist, and settle while the head changes view and reacts. It directly tests the failure we have, and prevents a fixed grip from passing merely because it rotates smoothly.

**Candidate A:** purpose-built 2D arm/hand/head drawings with controlled deformation and replacements. **Candidate B:** a simple 3D body/head with authored caricature features and a drawn finish. Reuse that 3D blockout for a Grease Pencil draw-over only if B's motion works but the appearance does not.

Start by checking likeness in the few views the action needs. Then inspect the reach, deepest bend, wrist turn, overlap change and settle, including neighboring frames. Compare normal-speed acting, connected silhouettes, readable grip, facial identity and outline stability. Record actual construction and correction time. Request one change to the action to see whether either method really supports economical revision.

Only the stronger result proceeds to a second, short football contact test with a planted support foot, kick and recovery in the intended pitch setting. Passing a seated conversation does not validate full-body sport.

Reject a candidate if it passes only by shrinking the movement, hiding the hands or simplifying away the likeness. If neither looks good, do not scale it across a cast. Reduce the uncertain part and test again, rather than produce another complete film with the same limitation.

The environment can already use coherent 3D layout with drawn materials regardless of the character route. Use real spatial relationships for pitch markings, goals, furniture, floor contact and cameras; preserve Samtoons' caricature art direction in the finish. This is our proposed application, not an assertion that a particular shader makes an environment world-class.

## Evidence and completion limits

This work inspected the local construction, selected weak crops and an existing native benchmark frame, and researched primary production accounts, manuals and original papers/repositories. It did not replay every benchmark frame, identify their source software, run the research models, or build these new comparison characters. Current Blender 5.2 has already built/rendered the existing v004–v006 work; the newly proposed techniques remain untested in this project.

No production assets, voice models, audio, existing film, or pipeline rules were changed. Better construction should reduce recurring defects and revision cost. It cannot honestly promise world-class output without artistic work or eliminate review for new actions.
