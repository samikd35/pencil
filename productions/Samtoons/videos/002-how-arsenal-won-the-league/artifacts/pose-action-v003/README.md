# Eight-second action review v003

[Play revised review](pose-action-v003.mp4) · [Before/after: v002 left, v003 right](comparison-v002-left-v003-right.mp4) · [Editable Blender file](pose-action-v003.blend)

The user liked the complete-character running/jumping in v002 and requested correction of frame-to-frame vibration. v003 preserves all sixteen source drawings, pose choices, exposures, jump vertical trajectory, kit and face artwork. It changes horizontal registration/travel, camera tracking and limited lower-body contact compensation. No new image generation, detached-head replacement, optical-flow interpolation or soundtrack was used.

## Change and evidence

The previous camera chased a root that stopped on held drawings and jumped on substitutions. The revised character follows a planned neck-base trajectory; the camera follows that path independently. A connected textured mesh supplies keyed horizontal support compensation below the torso so boots remain planted while the upper body advances. The entire action after frame 12 is shifted 0.5 world units to meet the ready pose without the previous backward starting snap. Vertical flight and all pose exposures remain unchanged.

During steady-run frames 29–100, the previous registered body moved −41 to +68 pixels per frame on screen; v003's horizontal registration changes by less than 0.001 pixel. Background step variation falls from 10.87 pixels standard deviation to 0.00013. Evaluated contact error is below 0.000001 world units. The same [regression check](../../scripts/check_temporal_continuity.py) fails the old scene and passes this scene. [Native results](temporal-check.json) and [encoding](encoding.json) are recorded. Original video 001 delivery hash remains unchanged.

Consecutive run and jump frames and full-size support poses were visually inspected. The encoded movie has 192 frames, 24 fps, 1280×720 and eight seconds. These tests establish removal of the measured oscillation, not final creative acceptance. Subsequent user playback review accepted this revision: running/jumping almost perfect and better than video 001.

## Editing and reproduction

Scene: `S002_whole_pose_action_v003`. The Bruno root exposes `pose_index`; root and camera position keys remain editable. Each pose surface now has a keyed `support compensation X` shape key. Source images are packed. The correction is horizontal and zero over the head/upper torso; its largest value in this clip is 0.325 world units during gathering. It is a bounded deformation for these drawings, not a general anatomical leg solver. Inspect silhouette strain if altering timing or stride. New views or major pose changes need suitable artwork.

`../../scripts/revise_pose_action_v003.py` loads preserved v002, makes the new scene and saves an unused output version. `../../scripts/render_pose_action_v003.py` streams the saved version into the movie. `../../scripts/check_temporal_continuity.py` checks native output (default v003, `-- v002` reproduces failure). Do not overwrite preserved review versions. [Provenance](provenance.json), [per-frame motion](motion.json), [registered landmarks](poses.json), and the [original generation record](../../assets/bruno-action-poses-v001/prompts.md) retain inputs.

## Reuse status

The user endorsed the whole-character action-proof approach. It is documented in the shared motion guide, caricature recipe and Samtoons profile. The user subsequently approved the temporal correction as almost perfect and better than video 001, authorizing adaptation to Gyökeres. The full Arsenal film, script and other appearance approvals are unaffected; this is a silent method proof, not full-film staging acceptance.
