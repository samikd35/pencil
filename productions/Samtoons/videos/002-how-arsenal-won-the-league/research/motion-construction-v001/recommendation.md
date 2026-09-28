# Samtoons motion construction: findings and recommended direction

17 September 2026. Scope: inspect the exact episode 001 delivery specified by the user, diagnose episode 002’s jump test, and choose a practical route toward the adopted benchmarks. This is an investigation and proposed construction change, not a passed animation proof.

**Recommendation: keep simple joint controls; build a coherent, layered cartoon body designed for animation, and use replacement drawings for extreme poses. Preserve recognizable heads, hair, expressions and kit identity. Stop treating the entire approved illustration as one surface that must stretch into every action.**

## What video 001 actually used

The exact input was [samtoons-final-1080p.mp4](../../../001-manchester-derby-2026-09-13/artifacts/delivery-v001/samtoons-final-1080p.mp4), together with its delivered `samtoons-final.blend`, edit list and authoring scripts. I inspected three one-second overview sheets from that MP4, selected full-size delivery/action frames, and the native file read-only. This was not a new normal-speed audiovisual review of the whole movie.

“Stickman based” described its simple head/shoulder/elbow/wrist/hip/knee/ankle **controls**. The delivered main characters used textured 2D meshes deformed by bones. The native inventory found 51 armature-skinned object appearances across the 17 selected shot scenes, with no Grease Pencil objects in those scenes; this is not a count of distinct people or all visible instances. In the kick/reaction scene, the sampled bodies have 9,709 vertices, 14 weight groups and Preserve Volume enabled. [Inventory](delivery-native-inventory.json).

Earlier staging did use native curve limbs and polygon bodies with replaceable faces. The later selected A treatment used full-body illustrated surfaces. Therefore, saying that the delivered film avoided deformation through pure stick figures would be inaccurate.

Useful implementation evidence:

- [build_option_a.py](../../../001-manchester-derby-2026-09-13/scripts/build_option_a.py): editable joint targets, constrained bones, continuous artwork, separate eyes/brows/mouth controls.
- [repair_cast.py](../../../001-manchester-derby-2026-09-13/scripts/repair_cast.py): measured arm silhouettes, garment boundaries and character-specific binding; authored seated/reclining treatments.
- [build_action_staging.py](../../../001-manchester-derby-2026-09-13/scripts/build_action_staging.py): earlier native shapes/curves, driven socks, attached boots and face substitutions. Useful mechanisms, not a finished universal character kit.
- [Earlier audit](../../../001-manchester-derby-2026-09-13/research/animatic-audit-v001/audit-and-repair-plan.md): rejected patch limbs, residual source arms, mismatched colors and weak timing. This describes the earlier failed animatic, not an assertion that every defect persisted into delivery.

What deserves reuse: simple controls, fitted construction, coherent drawing style, independent facial acting, visible contacts and shot-specific posing. What should not be inherited: the assumption that one approved standing drawing supports every action or view.

## Why the new jump failed

1. **The controls were simple; the surface was not.** Gyökeres began as a fully shaded, open-arm illustration containing connected shirt, arms and legs. Rotating its arms pulls nearby artwork unless those surfaces are correctly separated or fitted.
2. **The initial weighting was too generic.** Distance to every bone let moving arms/legs influence shirt regions. Subsequent rectangular masks merely moved the distortion to their boundaries. Increasing grid density to 33,166 vertices did not fix the anatomical assignment.
3. **Invisible geometry also folded.** The full rectangular mesh retained transparent areas. Trimming those faces removed the inspected black overlap artifacts, but did not solve the body construction.
4. **The test exposed a missing pose range.** Large raises, crouches and landings require appropriate shoulder, pelvis and overlap shapes. The shrug had never validated these.
5. **Motion design needs a separate pass.** Uniform eased keys do not create convincing acceleration, flight or landing weight. An in-place, symmetrical jump does not establish the film’s side-view chase performance.

The final diagnostic iteration still shows pointed/flared underarms at its high jump. It also contains a set-scaling regression that displaced the number from its flag shirt. **It is failed evidence, not a review-ready film asset.** The attempted weight revisions are preserved; further local threshold adjustments are not the recommended route. The first film’s Preserve Volume setting is another difference to test, but cannot repair wrong part assignment or create missing drawings.

## Best practical approach

Use a **hybrid 2D puppet** in Blender: simple controls, purpose-built cartoon parts, and a few drawn pose replacements. This is a recommendation for our implementation; the benchmark movies do not reveal their creators’ exact rigs or software.

- Build torso/pelvis, upper/lower limbs, hands and boots as coherent flat shapes with controlled outlines. Use the same joint targets throughout. Keep sleeve, cuff, sock and boot attachments derived from their actual limb controls.
- Design overlap under sleeves, shorts and cuffs. Hide internal seam outlines; inspect the full external silhouette. Avoid circular joint patches and roughly cropped scraps over the existing body—the first film already exposed that failure.
- Retain the approved facial identity. Use properly registered face/hand drawings and independent brows, eyes and mouth acting. Any detached head needs a continuous neck-to-collar join, not a pasted portrait.
- Keep kit lettering on the torso instead of letting an arm deform it. Simplify folds and shading, while retaining the colors, crest/number and other recognizable details appropriate to the framing.
- Use a small number of views required by the actual shot. A side/three-quarter run requires suitable artwork; rotating a flat frontal drawing does not produce it.
- Add a replacement drawing or corrective shape for an extreme shoulder lift, compressed landing, crossed arm or foreshortened kick when the ordinary parts cannot make a clean silhouette. Do not force every pose through the base rig.

Layered movable parts and separate animation controls are established cut-out practice. [Toon Boom’s rigging guide](https://docs.toonboom.com/help/harmony-24/essentials/getting-started/character-building.html). Replacement drawings should retain compatible line style, part separation and pivot registration. [Toon Boom’s substitution guidance](https://helpcentre.toonboom.com/hc/en-ca/articles/41014001536275-How-do-I-add-a-substitution-drawing-while-animating-a-rig). Mixing cut-out and drawn animation is also documented as a way to improve selected scenes. [Workflow reference](https://learn.toonboom.com/modules/animation-workflow/topic/cut-out-animation-workflow).

These sources support the method, not a promise that our unbuilt version already meets the benchmark.

## Options and compromises

| Option | Gain | Cost or limitation | Decision |
|---|---|---|---|
| Keep reweighting the whole illustration | Retains the exact painted surface | Fragile at large bends; difficult part overlap; repeated character-specific repairs | Limit to modest motion already demonstrated; stop using it as the default intense-action solution |
| Bare line-stick bodies with recognizable heads | Least surface complexity; very clear poses | Significant visual reduction from the adopted football cartoon references | Possible only if deliberately chosen; not necessary to obtain simple controls |
| Designed flat parts + joint controls + selected replacement drawings | Strong control, readable movement and recognizable cartoon finish | Upfront part/view construction; some poses need new drawings | **Recommended balance** |
| Draw the entire film frame by frame | Greatest pose and silhouette freedom | Much more drawing and consistency work across 4–5 minutes | Reserve for brief difficult actions or accents |
| Switch to Grease Pencil or a dedicated 2D application | Different drawing and rigging tools | Migration and a new proof; does not automatically solve anatomy or timing | Not justified as the first fix |

Grease Pencil can itself use bone weights, so switching to it is not an automatic escape from deformation problems. [Blender Armature documentation](https://docs.blender.org/manual/en/4.4/grease_pencil/modifiers/deform/armature.html) describes the mechanism; this is not a claim of Blender 5.2 API compatibility.

The practical compromises are **less painted body detail, a bounded set of authored views, and extra drawings for exceptional poses**. Keep likeness, clean contact, expressive action and the joke. Do not compromise those to keep one unsuitable image unchanged. Setup effort rises initially; later reuse is plausible but no time/cost savings have been measured.

## How to improve beyond video 001

The benchmark advantage is not simply more surface detail. Reference A’s running/offside and fall passages show distinct action silhouettes and consequences. Reference B’s ~69-second jump and ~75-second strike use clear limbs, readable contact and economical body shading. Its group reaction uses different gestures for different people. [Adopted benchmark](../../assets/benchmark-v002.md), [A study](../../../../research/reference-analysis.md), [B study](../../../../research/reference-bayern-v001/analysis.md).

For this film:

- **City chase:** readable alternating strides, stable foot contacts, body lean and a visibly steady grip on the podium. Give panicked Arsenal a different rhythm from calm Pep. Do not just slide a standing figure.
- **Corner into defence:** complete the football action, then animate players repositioning into the nine-player wall; Raya and Gyökeres retain their distinct roles.
- **Ridiculous winner:** author the body angle needed for the backside contact, ball reaction and recovery. Use a dedicated pose where necessary.
- **Ferguson:** keep silhouette acting legible, then change posture, hands, brows and mouth for the reveal/meltdown. A shaking whole card is insufficient.
- **Timing:** block strong poses first, then choose transitions, faster action and purposeful holds. Maintain separate control over body travel, feet, face and prop contact. More interpolated frames alone do not improve performance.

## Next concrete proof

Replace the failed construction test with one **eight-second full-body run → jump → land → recover** excerpt using Gyökeres’ recognizable identity and the proposed simpler body. Build only its required view and extreme poses first. Suggested allocation: 0–2 seconds a few accelerating strides; 2–3 seconds preparation/takeoff; 3–4 seconds flight; 4–5 seconds landing/compression; 5–8 seconds recovery and an expressive reaction. Adjust this during posing; do not stretch the jump to fill the allocation.

Review the clean silhouette and solid-color body before kit detail, then the same movement with finished face/kit treatment. This remains one existing staging checkpoint. Keep the whole body and contacts visible, compare with selected reference action, inspect every changed contact/bend interval at useful size, and review the encoded clip at normal speed. Check planted feet, hand/prop attachment, absence of residual limbs, consistent outlines and recognizable identity.

Do not propagate it across the cast or claim benchmark quality until that actual proof holds up. The current eight-second files establish why the old approach needs changing; they do not pass this requirement. The locked script and earlier completed film remain unchanged.


## Subsequent implementation feedback — 17 September 2026

The layered-body implementation was rejected: its head/body coherence, joint finish, clothes and shoes regressed from episode 001. Its proposed architecture is not an approved replacement. The current direction reuses the actual delivered Bruno asset and improves its movement before adapting Gyökeres. The user accepts this reused drawing/composition/construction as a baseline, but rejects the initial running and jumping. See the current brief and versioned Bruno action proofs; technical reuse is not proof of improved animation.
