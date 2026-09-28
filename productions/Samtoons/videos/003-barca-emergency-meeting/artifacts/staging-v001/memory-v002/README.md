# S10 — connected player surfaces, v002

Scoped repair of the rejected v001 shoulders, wrists and shorts/thigh joins on both Lewandowski and Raphinha. This is a review candidate, not final-film acceptance or a whole-character reconstruction.

## Diagnosis and repair decision

The original sleeves and torso had separate, incompatible boundary outlines. Simply moving them together left stepped shoulders. The wrist used a generic separate hand with a transverse seam. The shorts used an angle scaled by a vertex weight, so the leg opening did not fully follow the thigh.

The movement controls, approved reference designs and head/foot animation are independent of these faults. Under the user's clarified rule, a complete rig/scene rebuild is unnecessary: replace the defective surface contours and correct the shorts binding within the existing construction. New torso/sleeve contours have one outside boundary; new forearm/hand contours use hands traced from the selected reference. Shorts hems use the actual thigh coordinate frame while their waist remains attached to the torso. The shirt contour includes its neck opening, so its fill cannot cross the exposed neck; the original collar artwork supplies that edge.

During review, the first revision also exposed an inherited Blender Action-slot problem: clearing shape keys did not remove the old shared eval-time curve. Those old keys selected incorrect replacement shapes. The builder now replaces that curve explicitly and checks all 264 frames on both players, including holds and period visibility. Discrete authored surface frames hold until their next authored pose; no fabric-only drift during a body hold.

The original native file remains preserved in memory-v001. Retired drawing objects in v002 are disabled and have their visibility animation removed; this correction is not described as a clean rebuild. No script, audio, camera, skeleton pose, foot contact, ball timing or coach motion was re-authored.

## Ownership and reproduction

- Selected native source: `memory.blend`, scene `S003_S10_Memory_v002`.
- Base choreography: `scripts/build_memory_v001.py` in the video root.
- Repair owner: `scripts/revise_memory_connections_v002.py`.
- Hands: `scripts/prepare_memory_hands_v002.py`, reusing the existing vector tracing helper and selected reference images.
- To reproduce construction, open the preserved v001 native file in visible Blender and run the repair module's `setup()`, `prepare(name)` and `bake(name)` for each player, then `finish()`. Use a new output directory rather than overwriting this selected candidate.
- Render the saved native source with `scripts/render_staging_scene.py -- S10 S003_S10_Memory_v002 memory` through Blender background mode.
- Run `review_memory_connections_v002.py` with the project's PIL-enabled Python for export/hash/audio checks and encoded close-up evidence.

`surface-check.json` records connected polygons, not an aesthetic verdict. `verification.json` records the export checks and actual visual inspection coverage. `joint-comparison.jpg` compares the rejected and revised player joins at the same frames; `motion-joints.jpg` covers the kick and reception poses.

## Scope and remaining limits

This repair is for the existing S10 action. It does not certify arbitrary extreme poses, new turns, overall benchmark-level acting or all joints in other shots. S07 remains separately rejected. Sound is unchanged; no new subjective listening approval is claimed. S11 remains downstream of the S10 staging decision.
