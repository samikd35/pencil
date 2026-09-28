# Ferguson artwork refinement v008

Review candidate, not approved character artwork or an approved ending. The user's positive movement feedback applies to v007. This revision preserves that movement while improving the native drawing around it.

## What changed

- Fuller cardigan, coordinated folds/shading, collar and tie; broader face, silver hair, smaller spectacles and jowl detail.
- Less uniform fingers, palm/thumb contours, trousers and outward-facing detailed shoes.
- Continuous cloth around elbows and knees, with one connected cardigan surface spanning chest and sleeves. The chest no longer has a closed outline over the moving sleeves.
- New finger details inherit both the existing exposure action and its Blender action slot, so they disappear with the open hand during fist poses.

The shared narrator room, shot camera, selected audio and all v007 control motion remain unchanged. The character uses editable native flat meshes and curves, with no image-textured character materials. This is not a conversion to Grease Pencil objects.

## Root cause and repair

The first artwork pass still outlined the chest independently of the sleeves. The user correctly identified that it looked like a separate vest. Matching shoulder controls did not fix the visible garment. The final base mesh shares shoulder vertices between its torso and arm sections, with one exterior outline.

Deforming large concave filled polygons also produced stray triangular fills through bent sleeves and trousers. The final moving cloth, shading and outline strips use explicit triangle/quad topology. Inspected full-body poses include frames 7, 43, 81 and 121; scene-frame inspection also covers the gesture transitions. The full-body scene is a diagnostic view, not another story location. Foot-control stability alone does not establish the drawing's quality.

## Evidence and limits

`native-checks.json` checks every frame: v007/v008 control world matrices have zero difference, planted foot-control drift is below 0.000001 m, exactly one mouth is visible, new finger details match hand exposure, the cardigan mesh is connected and the same room is present. These are technical checks, not creative approval.

`ferguson-native-dialogue-v008.mp4` is the seven-second, 168-frame dialogue review with the same selected mix. Lip shapes retain v007's approximate word-aligned timing; final lip-sync and listening approval are not claimed. The assistant inspected rendered frames; user normal-speed review remains required for the revised artwork in motion.

## Edit and reproduce

Open `ferguson-art-v008.blend`. Use scene `S002_v008_Ferguson_dialogue` for the shot and `S002_v008_Ferguson_full_body` to inspect the entire figure. The earlier v007 scene remains preserved.

The artwork script is `../../scripts/refine_ferguson_art_v008.py`. In a visible Blender copy containing v007, load its definitions, then run `clone()`, `clothing()`, `hands_and_shoes()`, `inherit_new_visibility()`, `likeness()`, `sleeves()`, `unify_garment()`, `full_body_view()` and `save()` in visible batches. Do not clone into an existing v008 scene. Render/check the saved version with `../../scripts/render_ferguson_art_v008.py`.

Garment contours are editable absolute shape keys baked for this shot. After changing arm/leg motion, rerun `sleeves()` and `unify_garment()` before saving/rendering; they replace only their own v008 surfaces. This is a bounded method for these poses, not a tested general-purpose turn/foreshortening rig. Preserve v007 and the selected audio.
