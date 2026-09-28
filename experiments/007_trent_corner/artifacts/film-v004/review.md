# Barcelona wasn't ready. Trent was. — film-v004

Complete 38-second revision of the advanced stickman film. The user accepted the expanded player arrangement and selected sparse sound A, then explicitly asked the producer to decide all remaining checkpoints for this video. The journal records that delegation separately from user acceptance.

## Picture and sound decisions

The shared action view contains 15 representative players: seven Liverpool players and eight Barcelona players including the keeper. Four added Liverpool attackers remain visible among the markers, and Origi retains his opening. This is a compressed staging reconstruction, not exact tracking or a claim about the historical number of players in view.

Barcelona's fluorescent-yellow kit and black goalkeeper kit follow Liverpool's [official Inside Anfield footage](https://www.youtube.com/watch?v=Ik-DhHJM8eo&t=432s). Lead players retain their illustrated heads. Three newly generated supporting designs add blond hair, close-cropped black hair and swept black hair with a moustache to the existing supporting design. Supporting figures are representative, not named portraits.

The kick enters and leaves its backswing continuously. The sleeping-knee camera now looks closely at the legs without a foreground head blocking the gag. The celebration camera centers Origi. Caption geometry sits close to the camera so nearby players cannot hide it. The native field, goal, shadows, varied angles, comic cutaways and slow replay remain. Sleeping heads and knees are explicitly fictional; the quick corner, first-time finish and decisive result remain the verified event.

Sound A removes the rejected synthetic stadium, hush, cheer and musical material. Contact sounds, the short comic snores and a recorded cheer after the goal remain. There is no continuous crowd bed or music. The selected 38-second WAV is byte-for-byte identical to the full A mix underlying the user-reviewed excerpt. Recorded crowd is CC0 material from [D.jones](https://freesound.org/people/D.jones/sounds/528799/) and [Krizin](https://freesound.org/people/Krizin/sounds/651646/); only the Krizin reaction is cued in A. It is not archival Anfield sound. See the film's `assets/audio-v002/provenance.json` and production plan for processing, licenses and rejected hashes.

## Reusable workflow changes

The installed production skill now calls for concrete staging, sound-direction, combined-animatic and delivery reviews. Cast/role maps and event-specific visual references prevent missing supporting people or assumed kits. Sound must be auditioned as actual sound, with an isolated uncertain layer and a sparse alternative where useful; noise synthesis is not accepted as “crowd” merely because its filename says so. Numerical checks and actual listening remain separate.

The existing journal records reviewer identity and hashes the reviewed artifacts. `pipeline/checkpoints.py` blocks absent, pending, agent-only, stale or rejected acceptance before a full render. An explicit user waiver/delegation permits work to continue and is recorded as such. This film exercises both actual user selection and delegated review. There is no added database or general production framework. [Workflow validation](workflow-checks.json) and [skill snapshot](workflow/produce-pencil-animation-SKILL.md).

## Review evidence

The producer inspected sampled sequences from the complete film-v003 animatic, new supporting artwork, shared staging, contacts and corrected camera stills. The complete film-v004 encoded movie passed its own frame and format checks. The producer inspected the encoded overview and successive contact samples, including the corrected knee/celebration views, role coverage and score changes. The file contains 912 frames / 38 seconds at 1080 × 1920 and 24 fps, stereo 48 kHz, and fully decodes. It measures −21.31 LUFS integrated and −1.98 dBTP; the sparse quiet passages are intentional. [Encoded checks](video-checks.json), [overview](encoded-overview.jpg), [contacts](encoded-contacts.jpg). `staging-checks.json` verifies all 912 frames for one active head per actor, continuous ball motion, main/replay framing, four boot/ball contacts, planted support feet, score/gag states, cue timing and packed image/audio dependencies.

The shared audio build checks source hashes, sample boundaries, finite samples and complete decoding. The selected premaster and finished WAV were compared byte-for-byte against A. Quiet between foreground events is intentional. The user chose A from the 12-second clip; the producer did not actually hear the complete soundtrack, so full-film listening quality and audience response are not claimed as tested.

## Editable assets and reproduction

`trent-corner-advanced.blend` contains native limbs, jersey meshes, boots, ball, goal/net, camera keys, text and gag props, with the selected WAV, head images, stadium and font packed. The source film directory retains cached sound assets, separate stems, the production plan, scripts and generated artwork. Supporting-head artwork used the built-in image tool; its exact prompt is `design/treatment-v004/heads-prompt.txt` and its saved output is `design/treatment-v004/supporting-heads.png`.

The production used Blender 5.2.0 LTS, its bundled Python 3.13/NumPy, Python 3 and FFmpeg 8.0.1. Run scripts from the Pencil workspace. `build_polished.py` rebuilds the native scene and asserts that the selected audio-event timing is unchanged. `pipeline/audio.py build experiments/007_trent_corner/production.json --out NEW_AUDIO_DIRECTORY` resolves cached selected sounds into fresh stems. `verify_staged.py --delivery` checks and packs the selected mix. Set `PENCIL_REVISION` to the intended version when verifying, rendering or finishing; the current final revision is `film-v004`. `render_staged.py --full` checks that revision's checkpoint journal, renders 1080 × 1920 at 24 fps with 32 Eevee samples, and `finish_checkpoint.py --full` muxes the selected WAV and checks the encoded movie.

Finishing refuses to overwrite existing movies. Preserve delivered revisions and use a new output revision when making changes. A new revision needs the applicable actual acceptance or scoped delegation recorded in the journal; do not invent approval to make a command run. For a direct re-edit, the packed Blender file and separate WAV are sufficient to choose a new export path. The versioned scripts and plan remain the source for rebuilding authored motion.
