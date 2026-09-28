User rejected this revision: players still read as held action images. Superseded by the neutral reconstruction in v021; not an approved baseline.

# Second chronological batch — v020 cast-performance revision

Review candidate following the user's rejection of new players as static images. Approval remains with the user. This 43.625-second batch follows the approved 69.542-second v018 opening/training sequence.

- `batch02-review-v020.mp4`: revised corner/header, defensive wall and City notification, with the selected sound and speaker captions.
- `opening-through-defence-v020.mp4`: approved opening followed by this revision.
- `batch02-v020.blend`: editable match and narrator scenes, packed source artwork/masks, native joints and keyed performance. These are illustrated meshes and layered drawings controlled in Blender, **not native Grease Pencil artwork**.

## What changed

The new players previously used generic fitting, several without arm bones. Their limited performance did not reproduce the accepted first batch. Every cast rig now has independent fitted torso, head, arm, hand, leg and foot controls. Wall players retain clasped/crossed hands where appropriate; authored short steps, compression and staggered head responses supply their performance rather than arbitrary image wobble.

Saka signals, checks the run, prepares, kicks and follows through. Gabriel anticipates, drives his arms through the jump, heads, lands and reacts. The opposition defenders track and respond to losing the header. The opponent keeper sets and attempts a late reach; Raya steps in front of the wall and braces. Arteta/Gyökeres and their speech animation remain unchanged.

The illustrated hand-over-shirt overlap needed actual layer separation and cloth beneath it. A single rectangular deforming skin stretched hands, shorts and fabric when the limbs moved independently. Gabriel, the keepers and opposition players now have source-matched articulated arm layers; the body retains the same complete character artwork with native cloth/shoulder overlap where required. Original faces remain intact. The new non-speaking cast uses head acting; uncalibrated automatic blink deformation was disabled. This is a bounded frontal/three-quarter rig, not evidence that it supports unseen views or extreme running poses.

The first kick check found that the toe reached the stationary ball before release. The final forward stroke accelerates into frame 168; the ball begins its flight and the selected kick sound starts at that same frame. `kick-contact-check.json` records the last eleven toe/ball distances and the limitation of that geometric proxy.

## Review evidence and limits

Native checks covered Saka's signal, preparation/contact, Gabriel's jump/header/landing, the keepers' reaches, both defenders' post-goal reactions, wall assembly and Raya's stance. The `checks/` folder includes rejected intermediate fittings; filenames beginning `encoded-` are extracted from the actual clips. The final review inspected consecutive encoded kick frames 154–171, header/landing frames 209–232 and wall-step frames 430–445. Sampled contact frames do not establish a full normal-speed artistic review or approval of every frame.

`regression-checks.json` compares the saved v019/v020 lead meshes and keyed controls: Arteta and Gyökeres are unchanged. It also checks 18 fitted rigs with independently changing controls and an identical audio premaster. `encode-checks.json` verifies frame counts, 1280×720 / 24 fps, stereo 48 kHz audio and complete decoding. Technical checks do not establish quality, humor, listening or audience comprehension. Agent listening was not performed; the playable movie is the audiovisual checkpoint.

## Reproduction and future reuse

Render the saved native file with `scripts/render_defence_v020.py`, then run `scripts/package_defence_v020.py`. `edit.json`, captions/subtitles and the unchanged premaster retain the selected timing. The full audio provenance and stems remain in v019; voice generation models are untouched. The render helper validates existing clip frame counts before reuse. Any changed shot must have its stale clip removed before rerendering.

`rebuild_defence_cast_v020.py` consolidates the live authoring stages and source-coordinate calibrations. It requires the earlier live v019 helper registries and is not a standalone bootstrap; the saved packed Blender file is the portable editable source. `check_cast_v020.py` is a standalone background-Blender regression check. New action/view adaptations still require their own visible motion review; do not treat a bone count or this candidate as an automatically approved character standard.
