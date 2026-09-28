# Cast coherence repair v011 — review candidate

The user rejected v010: the faces looked wrong, Gyökeres’s head/neck looked detached, and his shorts looked like separate garments. Arteta was an example; the requirement applies to **every character**. Video 1’s whole-character drawing is the local quality floor. Neither rig checks nor improved movement establish that floor.

## What caused the regression

- The v009 shared facial template and v010 approximate reconstruction discarded the selected illustration’s actual feature relationships. Adding hair stripes, cheek patches and stubble did not recover its likeness. The generic mouth/muzzle treatment compounded that mismatch.
- The neck was a fixed torso-local patch rather than a surface fitted between jaw and collar. Gyökeres also retained a filled white collar shape over the neck opening. A mirrored head requires the two attachment sides to be sorted in the torso’s space; failing to do that crossed Arteta’s replacement neck.
- The old hip patch, thigh-colored regions, duplicate shorts marks and separate contours did not constitute one coherent pair of shorts. Details added to those parts reinforced the split.

## Repair implemented

The selected `visual-treatment-v001/gyokeres-arteta.png` remains the identity source. Its facial contours are converted to native filled curves, with separate native eye parts and mouth geometry. These are editable vector shapes in Blender, **not image textures or a full-character picture moved to simulate speech**. They retain the source silhouette and feature placement rather than a shared generic face. The tracing method uses [VTracer’s raster-to-vector conversion](https://github.com/visioncortex/vtracer/tree/master/crates/vtracer-py), then semantic part separation and Blender construction; automatic conversion alone does not validate a character.

The neck is now one explicitly triangulated/quad surface fitted from collar anchors to jaw anchors at every frame. The filled collar cap is hidden and the garment opening follows the crew neck. Attachment order is corrected for the mirrored Arteta head.

Gyökeres’s shorts retain the **complete selected garment drawing**, including its seams, folds and marks, as one native triangulated object. One waist/crotch/hem mapping follows both thigh controls. The separate hip artwork and old markings are hidden; the underlying upper legs are skin. Fixed triangles avoid changing concave-polygon triangulation during motion. Footwear retains its planted sole offset.

The supporting scene, prior motion work and approved soundtrack remain inputs. This correction is fitted to the existing three-quarter views and current gestures/steps. It does not prove arbitrary turns, new running/jumping actions, or all remaining cast members.

## Evidence and scope

- `cast-coherence-v011.blend`: visible Blender authoring, saved editable candidate. v010 remains preserved as rejected evidence.
- `cast-motion-review-v011.mp4`: the complete 18-second signing passage, 432 frames at 24 fps, with its exact approved audio interval. It covers the bag set-down, both steps, reveal and dialogue.
- `frames/`: selected action, contact and speaking frames from the actual render.
- `checks.json`: native construction, neck ordering, support stability, mouth exposure and shorts topology checks after reopening the saved file.
- `feedback/`: the user’s rejected-face/neck and double-shorts screenshots.
- `assets/native-contours-v011/*.json`: source hash, semantic masks and native contour inputs.

Technical checks cannot certify likeness, drawing quality, acting or final lip sync. The mouth timing is a rough authored schedule; the brows and gaze retain the selected source expression. There is no claim of final dialogue performance or a completed first batch. **The first 42.54-second batch remains held for appearance repair/review; the rest of the film is not completed.**

## Carry-forward rule

Reuse motion controls and construction knowledge, but preserve each character’s own complete design. Before propagation, compare face and full body with the accepted source at a similar viewing size; inspect the same asset at contact and gesture extremes. Check jaw-to-collar continuity and each garment as a whole. A separate panel with extra detail is not a repair for a broken silhouette. New characters—including remaining players, Pep and Ferguson—retain their own appearance review; this repair is not blanket approval.
