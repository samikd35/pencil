# S05–S08 continuous staging preview

53 seconds, 1280×720, 24fps. This is representative story coverage, not a finished-film or benchmark-quality claim.

| Preview time | Coverage |
|---|---|
| 00:00–00:07 | S05 rough moving tactics board; Pérez gives the marking order offscreen |
| 00:07–00:20 | Selected S06 v002 football performance, all frames and original sound |
| 00:20–00:35 | Selected S07 v002 coaches, all frames and original sound through release |
| 00:35–00:43 | Rough S08 failed-plan / call-connection insert; Pérez calls Bayern offscreen |
| 00:43–00:53 | Selected S08 v006 call excerpt, all frames and original sound |

The two new lines are locally generated using the existing synthetic Pérez take as reference conditioning. No existing voice take, model, performance scene or source clip was replaced. Subjective voice matching and listening remain unverified by the agent. New coverage uses native Blender curves/meshes and the inspected layout helpers. It deliberately omits the ensemble reaction performance; the tactics board and call insert are rough coverage only.

## Review and corrections

Inspected the outgoing and incoming frames around each of the four cuts, plus the new board and call inserts. Cleared a defender/label overlap on the tactics board. Corrected the new call insert to put the monitor left and tactics board right, matching the selected call scene. All original selected footage stays intact. The new insert uses the existing monitor setting rather than introducing the script’s unbuilt laptop.

The cut supports the left-to-right attacking direction and retains the goal-crossing, reaction and ball-release coverage. These are sampled-frame observations, not a claim of a normal-speed motion or listening audition. The encoded file passes a full decode, exact frame/duration checks and source-selection hashes; those checks do not certify acting quality.

## Consolidated polish priorities

1. Clarify the training counter (eight) versus the seven-goal result discussed in S07. The current cut exposes that ambiguity; it is not resolved by this assembly.
2. Upgrade the new rough inserts to the established environment finish and add the intended ensemble reactions when developing their complete scenes.
3. Preserve the selected performances while improving the known grips, limb silhouettes, facial turns and secondary reactions together. The deferred S08 wrist issue remains unresolved; this edit does not restart that experiment.
4. Review the passage at normal speed with sound before locking comedic holds and camera timing. New Pérez lines remain audition candidates.

S04 ensemble coverage and S09 onward remain outside this passage. The next production step is the S09 Lewandowski response using this call’s eyelines and reaction as its entry, with this shared polish list carried forward.

## Reproduction

`build_passage_inserts_v001.py` authors the two insert scenes in the visible Blender session; `passage-inserts.blend` stores their motion. `render_staging_scene.py` renders them. `assemble_passage_v001.py` concatenates the five exact inputs and runs the technical checks. `edit-map.json` records frame spans and source hashes. `render-selection.json` is a historical snapshot whose asset paths remain relative to the video root. The shared audio build was run against the video-root production.json; `audio/resolved-cues.json` records resolved paths and the input plan hash.

The full-film timeline still has 4992 frames. S08 keeps its existing 18-second budget: eight seconds of decision coverage followed by the ten-second selected excerpt. No later shot moved. `production-before.json` retains the pre-assembly timing map.
