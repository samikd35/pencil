# Supplied character moves the box

User request: “lets this guy move the Box”, with `/Users/samikd/Desktop/Ronny.jpg`.

This is a fictional character-identity experiment on the existing Heavy Box movement. It is not a claim that the photographed person performed this event. It retains the established simple cartoon body construction rather than attempting anatomical deformation of the photograph.

Latest export: `artifacts/ronny-proof-v003/`, **rejected by the user for head/body style mismatch and the waist join**. It remains a preserved technical experiment, not an accepted character design. The requested follow-up is [research on a coherent cartoon construction](../../research/seamless-cartoon-from-stickman.md).

- [Play the character test](artifacts/ronny-proof-v003/ronny-moves-the-box.mp4)
- [Compare with the original stickman](artifacts/ronny-proof-v003/stickman-to-cartoon.mp4)
- [Packed editable Blender scene](artifacts/ronny-proof-v003/cartoon-skin.blend)
- [Native pose](artifacts/ronny-proof-v003/pose-118.png)
- [Geometry and motion checks](artifacts/ronny-proof-v003/checks.json)
- [Encoded-video checks](artifacts/ronny-proof-v003/video-checks.json)

## Identity and construction

The supplied photo guides the cropped dark hairstyle, facial structure and white Portugal number 7 kit. Native clothing includes white long sleeves, simplified red/green shirt print and badge, a dark captain's armband, white shorts and dark collar. The photograph does not show the full lower legs and footwear: white socks and dark shoes are authored choices. Logos and textile patterns are simplified.

Four matching head illustrations were made with the **built-in imagegen tool**, using the photo as a reference: neutral, effort, surprise and skeptical. [Exact generation prompt](assets/ronny-v001/heads.prompt.txt), [generated head sheet](assets/ronny-v001/heads.png), [preserved reference](assets/ronny-v001/reference.jpg). The requested transparent output arrived as RGB with a checker backdrop. The original pixels are retained; the existing whole-head silhouette mesh technique excludes the exterior backdrop. This involves no arm/torso segmentation or head deformation. The packed scene contains the sheet and its UV-mapped native silhouettes.

The body reuses the live curve controls from the cartoon proof. Shorts, socks and armband are exact continuous sections of those curves, with live source-coordinate drivers. Shirt number and accents are separate native objects. Hands and shoes keep their exact projected geometry. Expression selection follows the existing effort/surprise/reaction timing. The original Heavy Box soundtrack is carried through unchanged.

This remains native Blender curves/meshes with whole-head illustration replacements, not a Grease Pencil armature. The body controls, costume geometry, expression timing and materials are editable; detailed facial pixels are editable through the packed source image rather than individual facial strokes.

## Checks and review scope

The reopened saved project preserves every frame of the original 12 controls, the projected hand/shoe geometry and the source project hash. Both fill and outline curves stay connected to their endpoints. Clothing section endpoints are checked against their original curve locations on all 240 frames. A hand-control edit in the saved project moves the sleeve with it. Exactly one head is visible on every frame.

Native pose review covered the opening, forceful push and raised-arm recovery. The first build hit a stale-object-reference error in verification after reopening; its scene and exact source are retained as v001. V002 then exposed sock/skin surfaces at identical depth, causing striped z-fighting. V003 moves the sock surface forward without changing the motion. Earlier versions remain available.

Full subjective playback/listening and user acceptance are not claimed. Perceived likeness, expression replacement smoothness and the desired balance of detailed head versus simple body remain playback-review judgments. The small 640×360, 10-second proof is not a new final channel identity.

## Reproduce

Choose a fresh revision name; existing outputs are preserved:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python experiments/008_cartoon_skin/build_ronny.py -- --out ronny-proof-v004
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python experiments/008_cartoon_skin/build_skin.py -- --out ronny-proof-v004 --render
python3 experiments/008_cartoon_skin/finish_proof.py ronny-proof-v004
```

The character build reuses the named helper definitions in `build_skin.py` without executing its authoring side effects. The original character proof, source film, image-generation prompt and generated asset remain required inputs for reproduction. The saved `.blend` packs its head artwork, font and soundtrack for opening independently.
