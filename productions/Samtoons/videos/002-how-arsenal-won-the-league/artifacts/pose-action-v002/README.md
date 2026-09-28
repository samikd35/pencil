# Whole-body action blocking v002 — pending review

[Play the eight-second candidate](pose-action-v002.mp4) · [Editable Blender scene](pose-action-v002.blend)

This tests the root-cause correction in [the diagnosis](../../research/body-mechanics-v001/diagnosis.md): author complete coordinated poses, support contacts and travel before polishing transitions. Sixteen complete Bruno drawings replace the rejected independent limb curves. Video 001 supplies the appearance target and environment; the action drawings are new derivatives, not unchanged original artwork. The original delivered file is preserved.

## Review

Does the run, takeoff and landing read as one convincing body at normal speed? Acceptance would permit refining transitions and adapting the method to Gyökeres, not certify the whole film.

| Frames | Action |
|---|---|
| 1–12 | Ready and prepare |
| 13–108 | Alternating run cycle, mostly two-frame exposures |
| 109–122 | Gather, load, extend and release |
| 123–137 | Rise, tuck and landing reach |
| 138–152 | Contact, compression and recovery |
| 153–192 | Settled hold |

## Editable scope and limits

In scene `S002_whole_pose_action_v002`, select `Bruno / whole-body pose and travel` (Blender may append `.001`). Its keyed `pose_index` selects 0–7 run and 8–15 jump drawings. Root location and camera keys control travel and framing. Images are packed in the native file. This is pose-based blocking, not a joint-deformation rig: changing a limb silhouette requires editing/replacing its complete drawing. New drawing variations in face/kit and discrete pose transitions still need creative review. Sound is intentionally absent only for this diagnostic.

Ground-contact anchors constrain placement during support. Flight follows acceleration −9.81 world units/s² for a uniform-area silhouette mass proxy; this proxy is not an anatomical centre of mass or a force simulation. The run uses 1.7-unit alternating steps every eight frames (average 5.1 units/s). These calculations do not prove appealing motion.

## Evidence and reproduction

The evaluated native check verifies exactly one correct pose on each of 192 frames, contact-anchor error below 0.00001 world units, the authored jump-proxy acceleration and unchanged source delivery hash. [Encoding](encoding.json) confirms 1280×720, 24 fps, eight seconds. [Verification](verification.json) records the actual result. All consecutive frames were inspected in three contact sheets, plus full-size run/takeoff/apex/landing stills. No normal-speed creative acceptance is claimed from those checks.

[Asset plan](../../assets/bruno-action-poses-v001/plan.md), [generation prompts](../../assets/bruno-action-poses-v001/prompts.md), [provenance](provenance.json), [motion data](motion.json). Native authoring: `scripts/build_pose_action_v001.py`, then `scripts/revise_pose_action_v002.py` in visible Blender with unused output version directories. Render the saved revision using `scripts/render_pose_action_v002.py`; evaluate with `scripts/verify_pose_action_v002.py`. Existing version directories are intentionally protected from overwrite.

The initial run sheet was rejected for repeating the same arm/leg side. Its corrected second half is the selected sheet. v001's floor placement and tracking were revised in v002. The shared method remains adopted, while this specific pose-substitution technique remains experimental until reviewed.
