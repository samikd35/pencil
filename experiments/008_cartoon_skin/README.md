# Cartoon appearance on the working stickman controls

User-authorized exploration, 13 September 2026. The user clarified that the move back to stickman was driven by repeated deformation/attachment failures in more detailed characters, despite good static drawings. The aim is to keep the successful motion construction while testing fuller cartoon artwork.

Follow-on identity test: [the supplied character moves the box](ronny.md), applying the user's photograph to the same motion with reference-led head expressions and white number 7 football clothing.

User feedback rejected that identity test's detailed head/simple body mismatch and overlapping waist outlines. [Follow-up research](../../research/seamless-cartoon-from-stickman.md) led to the user-authorized [coherent character proof](coherent.md): a flat native face, simplified white kit, derived hip attachments and one visible torso/shorts boundary. It retains the original action and sound. This is the latest candidate for visual review; the earlier proofs remain preserved.

The subsequent [native Grease Pencil comparison](gp-comparison.md) keeps that exact design and action while replacing the visible character geometry with native GP strokes/fills. All 240 control frames and hand/foot contours match, and saved control/art edits pass. [Play curves versus GP](artifacts/gp-proof-v004/curves-vs-grease-pencil.mp4). It establishes a GP option for this tested construction, with fixed drawing topology and viewing-angle limits; user playback review remains pending.

## Three-player caricature test — 14 September 2026

The user identified the reference figures as Jude Bellingham, Kylian Mbappé and Vinícius Júnior and requested that cartoon treatment in the current curve/mesh workflow. This is a fictional box-action construction test, not a football incident or an approved channel character identity.

[Play the three tests](artifacts/trio-comparison-v001/three-player-motion-test.mp4) · [Native character lineup](artifacts/trio-comparison-v001/native-lineup.png) · [Delivery checks](artifacts/trio-comparison-v001/checks.json)

| Character | Editable Blender project | Individual 10-second clip |
|---|---|---|
| Jude Bellingham | [Tall body, grin](artifacts/trio-jude-v004/cartoon-skin.blend) | [Play](artifacts/trio-jude-v004/cartoon-with-sound.mp4) |
| Kylian Mbappé | [Long neck, profile, sash](artifacts/trio-mbappe-v003/cartoon-skin.blend) | [Play](artifacts/trio-mbappe-v003/cartoon-with-sound.mp4) |
| Vinícius Júnior | [Compact body, beard, red shoes](artifacts/trio-vini-v004/cartoon-skin.blend) | [Play](artifacts/trio-vini-v004/cartoon-with-sound.mp4) |

The head artwork is reconstructed from explicit whole-head domains in the supplied drawing, using the already installed VTracer library and native filled Blender Bezier curves. Heads have no image textures. Bodies, kit marks and sponsor lettering are native shapes. Derived shoulder, hip, neck and bend attachments adapt proportions while leaving the original 12 animated controls, hand/foot contours, box, timing and source sound intact. The torso and shorts still use the live combined silhouette. This is a focused reconstruction of the selected drawing, not automatic segmentation of a complete character into an inferred rig.

The compact body needs a minimum pelvis height relative to the feet during the lean/hop; globally scaling pelvis height hid a shoe. Neck tubes sit behind the shirt/collar, and the jaw overlaps the neck. Shoulder stripes remain inside the shirt. Earlier candidates and source assets are preserved; only the versions linked above are the current trial.

Each saved/reopened character passes all 240 source-controller comparisons, endpoint checks, unchanged projected hand/foot geometry and a temporary hand edit. Native poses and exported motion sheets are reviewed separately from these checks. Each individual movie preserves decoded original audio. The compilation presents three successive 10-second executions, rather than a three-person interaction.

**Limits:** each reference-angle head moves as a unit. Expressions, blinking, lip sync and head turns have not been implemented. Limbs remain elastic and simple; tiny shoes and mittens retain the proven contact shapes. Likeness and style acceptance remain the user's review. This trial does not establish arbitrary anatomical movement or a universal character rig.

Build with `build_trio.py -- --character jude --out <fresh-revision>` through Blender, substituting `mbappe` or `vini`. Render the saved file with the existing `build_skin.py -- --out <revision> --render`. `finish_trio.py` packages the three selected revisions with the unchanged original sound. The builder includes an SVG-parser self-check and reuses existing controller, curve-section and verification helpers. The final vector inputs are in `assets/trio-v003/`; regenerate into a fresh asset revision using `prepare_trio.py` with the existing PyBlend virtual environment.

## Earlier result — proof-v002

[Play the comparison](artifacts/proof-v002/stickman-to-cartoon.mp4) · [Cartoon alone](artifacts/proof-v002/cartoon-with-sound.mp4) · [Editable Blender scene](artifacts/proof-v002/cartoon-skin.blend) · [Still comparison](artifacts/proof-v002/comparison.png)

The 10-second small proof adds a full coral shirt, continuous colored sleeves and blue trouser legs. The original face, mittens, shoes, action, camera, box, effects and sound are retained. This is a mechanism/staging candidate for review, not a selected channel identity or accepted final film.

All 12 existing controls have identical transforms on all 240 frames after reopening the candidate. Both outline and fill curves follow the hand/foot endpoints; maximum measured endpoint discrepancy is below 0.00000007 scene units. The projected hand/shoe geometry is exactly unchanged on all frames. A temporary hand-control edit in the saved scene moves the sleeve endpoint with the hand. The original Blender file hash is unchanged. Both exported movies decode completely and their decoded audio matches the original. See [geometry checks](artifacts/proof-v002/checks.json) and [encoded checks](artifacts/proof-v002/video-checks.json).

Visual inspection covered 12 native poses and the 24-frame [exported motion sheet](artifacts/proof-v002/motion-sheet.png). Those samples show a fuller simple-cartoon silhouette with attached hands and feet through the deep push and raised-arm recovery. Full subjective playback/listening and user acceptance have not been performed. Thick, flexible limbs and shoulder/head occlusion remain visible style choices; this does not prove arbitrary anatomical movement, another viewing angle, or a Grease Pencil rig.

The first build saved its scene and passed controller checks but stopped while rendering samples because Python retained a scene reference invalidated by reopening the file. The next revision refreshes that reference. This was a build-script failure, not a deformation failure; the earlier candidate is retained as `proof-v001`.

## First question

Can the existing Heavy Box movement carry continuous filled arms, trouser legs and a wider clothed torso, without changing its hand/foot/body controls or losing wrist/ankle attachments?

Use the preserved `001_heavy_box/artifacts/finish-v002/` as the input. Compare exactly the same 240 frames from the same camera. Keep the existing face, mittens, shoes, props, motion and soundtrack. This is a low-resolution mechanism/staging proof, not a new film, channel identity, or a final-quality export. No new sound selection is needed.

The first treatment is a simple rubber-hose cartoon: coral long sleeves and shirt, blue trousers, rounded shoes and the existing expressive head. Continuous limb shapes follow the existing curves; hands and feet follow the same endpoint controls. The shirt covers the shoulder and hip roots. Details belong to named body parts rather than being recovered from a flattened character image.

## Why this tests a different construction

The working Heavy Box source uses native Blender curves and flat meshes with control-driven curve endpoints. It is not a Grease Pencil armature. Preserve that representation for this proof and label it accurately. A Grease Pencil-specific implementation would be a separate comparison, using the same control locations to construct its drawing contours; do not claim that this proof validates it.

The historical `PyBlend_Stickman_Starter/experiments/002_hybrid_character_motion/character_asset/README.md` records incorrect arm ownership, shoulder gaps and contamination of head/torso artwork in prior attempts. Those are representation/attachment failures, not evidence that detailed 2D characters cannot animate. Blender's [Grease Pencil armature documentation](https://docs.blender.org/manual/en/5.0/grease_pencil/modifiers/deform/armature.html) describes vertex-group and envelope influence; selecting the correct strokes remains an authored responsibility.

## Evidence required

- Exact equality of all existing controller transforms across 240 frames, compared again after reopening the saved candidate.
- Live endpoint correspondence for all four limbs, valid drivers, and preserved projected hand/shoe geometry.
- An edit to a hand control makes both the filled sleeve and hand follow it in the saved project.
- Native pose samples and a playable before/after comparison, especially during the deepest bend and fast recovery.
- Keep visual judgment separate from numerical checks. Thick shapes may overlap even when their endpoints are connected.

No automatic weighting, image segmentation, new universal rig, or change to previous films is needed for this test. The known limit is elastic, approximately constant-width limbs and a fixed view; rigid anatomy, foreshortening, finger turns and detailed clothing folds are not established.

## Run

From the workspace root:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python experiments/008_cartoon_skin/build_skin.py -- --out proof-v001
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python experiments/008_cartoon_skin/build_skin.py -- --out proof-v001 --render
python3 experiments/008_cartoon_skin/finish_proof.py proof-v001
```

The build refuses an existing output directory. Rendering opens the saved candidate and refuses an existing movie. Records use the existing production journal helper. Review the small comparison before choosing a more developed character treatment.

Choose a fresh revision name when reproducing; `proof-v001` and `proof-v002` already exist. The source snapshots accompanying proof-v002 are evidence copies; run the scripts from this experiment directory as shown above.

## What the next visual step could change

The proven boundary is the control graph: body, head, hands, feet and bend controls. Fuller artwork can be built with explicit ownership around those controls. For this sample, each sleeve/leg is a continuous curve, so there is no elbow/knee drawing seam to split. The endpoint is shared with its mitten/shoe, and the torso covers limb roots.

- A more distinctive simple cartoon could change the head/hair, torso silhouette, colors and clothing accents while retaining this movement method.
- A more human-shaped cartoon would additionally need tapered contours and a narrower allowed stretch range; the current rubber-hose motion alone does not preserve realistic limb lengths.
- Hand turns, crossed limbs and large silhouette changes may need authored drawing replacements or explicit layer changes. Do not return to guessing body-part ownership from a flattened image.

These are proposed follow-on experiments, not completed capabilities. Keep new examples small and compare their actual motion before expanding a character's detail.
