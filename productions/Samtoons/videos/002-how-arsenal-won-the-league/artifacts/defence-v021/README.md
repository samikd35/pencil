# Reconstructed second batch — v021

43.625-second review candidate, 1280×720, 24 fps. `batch02-review-v021.mp4` includes the selected soundtrack and speaker subtitles. `opening-through-defence-v021.mp4` prepends the accepted v018 opening (113.167 seconds total). This is the current batch revision, not the complete five-minute film or a claim of user approval.

## Reconstruction and corrections

The rejected v020 used action drawings as resting rigs. Saka consequently began and stayed in a kicking pose; local joint changes did not create a complete performance. This version rebuilds sixteen new player roles from complete neutral drawings, reusing v016's fitted continuous mesh, alpha-aware weighting, rigid shoes and arm depth ordering. These are coherent illustrations deforming on native Blender rigs, not Grease Pencil strokes or a sequence of still pose cards. The accepted Arteta/Gyokeres geometry, keyed performance and soundtrack remain unchanged.

Saka signals, steps into the kick, strikes and recovers. Gabriel anticipates, jumps, heads, lands and reacts. The goalkeeper reaches; opponents respond. Nine wall players take short alternating side steps before bringing their hands into position. Hero Saka and Gabriel use the same drawings in the wall.

User-identified contacts were corrected at their source:
- Ball centre is 0.7354 m from the corner inside its 1 m quadrant. The visible boot tip, rather than its internal control, meets the 0.11 m radius ball at frame 168.
- The ball meets the evaluated upper-forehead surface at frame 217 and changes direction there.
- The header lands without the boots floating above the pitch. The goal reaches the actual back net at frame 238, then drops under gravity.
- Wall strides stay short enough to prevent crossed legs. Hand weight boundaries follow the source anatomy rather than selecting the shorts; adjacent-row image fragments are excluded from each mesh.

## Evidence and limits

Actual encoded consecutive frames inspected: kick 154–171, header 209–232 and wall 430–445. Additional rendered detail checks covered preparation, follow-through, landing, wall assembly and net contact. `contact-checks.json`, `motion-checks.json`, `regression-checks.json` and `encode-checks.json` record the measured constraints and full decoding checks. Frame inspection establishes those observed details; normal-speed creative acceptance and listening remain with the user. The agent did not claim to hear this unchanged soundtrack.

`batch02-v021.blend` contains editable rigs, controls, set, cameras and packed art. `../../scripts/render_defence_v021.py` streams review renders; `package_defence_v021.py` assembles the unchanged selected mix and subtitles. `check_cast_v021.py` verifies preservation and the contact/step constraints. `reconstruct_defence_v021.py` records the visible authoring recipe and fitted source coordinates; its live setup uses the existing v016/v017/v019 session helpers. Neutral sources and generation prompts are in `../../assets/neutral-cast-v021/`.

v021 is pending user playback review. Keep the accepted v018 first batch as the approved baseline; do not promote a technical pass into approval of this reconstruction.
