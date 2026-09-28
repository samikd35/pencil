# Checkpoint 1 — waiting players and sound

**Review outcome:** The user accepted this arrangement, selected A — sparse sound, then delegated the remaining checkpoint choices for this film. Completion continues in film-v004 without further checkpoint questions.

This is a preserved 12-second excerpt (10–22 seconds of the planned 38-second film), at 540 × 960 and 24 fps. It is a staging and sound-direction review, not the final animation.

- [A — sparse foreground, recorded cheer after the goal](checkpoint-A-clean.mp4)
- [B — same foreground, plus quiet recorded crowd ambience](checkpoint-B-crowd.mp4)
- [B's crowd layer in isolation](crowd-layer-isolated.wav)
- [Representative shared view](checkpoint-staging.png) and [encoded sequence overview](checkpoint-overview.jpg)
- [Editable native scene](trent-corner-advanced.blend), [script](../../script-v004.md), [cast/role map](../../staging-v004.json)

Review the waiting-player arrangement and choose A, B, or a sound revision. Acceptance unlocks the complete inexpensive animatic. That animatic has its own review before the full-quality export. Supporting faces currently share a placeholder design; individual face/pose polish remains after the arrangement is accepted. The existing sleeping-head/knee gags remain in the full scene but fall outside this excerpt.

## What changed in this film

The scene now contains 15 representative players: seven Liverpool players and eight Barcelona players including the goalkeeper. Four added Liverpool attackers are visibly distributed among the markers; Origi retains a clear opening. These are simplified staging positions, not a claim about the exact historic count or coordinates. The kit correction uses Liverpool's [official Inside Anfield footage, around 7:12](https://www.youtube.com/watch?v=Ik-DhHJM8eo&t=432s): Barcelona wore fluorescent yellow and their goalkeeper wore black. Henderson described [organizing protection against a counterattack](https://www.liverpoolfc.com/news/first-team/350694-jordan-henderson-champions-league-barcelona-spurs), so he is not invented as another box attacker.

The kick now enters its backswing from rest and returns to rest. Both teams remain in the shared corner-to-goal view. No new joke interrupts the real pass or first-time finish.

The rejected synthesized stadium, hush, cheer and musical assets are excluded by recorded hashes. A removes the continuous bed entirely. B uses a recorded crowd. Both retain the same contact effects and foreground gain, and both use a recorded goal reaction. These are CC0 library recordings from [D.jones](https://freesound.org/people/D.jones/sounds/528799/) and [Krizin](https://freesound.org/people/Krizin/sounds/651646/), not archival Anfield audio. [Provenance and rejected assets](../../assets/audio-v002/provenance.json).

## What changed across the system

| Failure | Cause in the workflow | Shared correction |
|---|---|---|
| “Crowd” sounded like rain | Noise synthesis was selected by label; numerical audio checks were treated as sufficient for delivery | Audition actual sound early, compare an isolated uncertain layer and a sparse alternative, retain rejected hashes, and distinguish listening from file checks |
| Missing waiting players | The cast was reduced to the main action without checking supporting roles in the frame | Require a cast/role map, relevant visual references, and a viewing-size staging review; player count alone is insufficient |
| Problems surfaced after the finished export | No concrete review boundary connected creative decisions to rendering | Staging → sound direction → combined animatic → delivery; retain unaffected acceptance and revisit changed inputs |

The installed [production skill](/Users/samikd/.codex/skills/produce-pencil-animation/SKILL.md), workspace instructions, [pipeline guide](/Users/samikd/MyProjects/Pencil/pipeline/README.md), and sound-planning guidance now agree on that process. The existing journal gains an optional reviewer field. A small [shared guard](/Users/samikd/MyProjects/Pencil/pipeline/checkpoints.py) checks the latest user decision and the hashes of reviewed inputs/artifacts. No new database or pipeline framework was added. Explicit user waivers remain possible and are recorded as waivers rather than acceptance. Preserved films retain their original scripts.

## Evidence and limitations

- [Staging checks](staging-checks.json): cast/role counts, camera framing, four added attackers visible by camera ray, four boot/ball contacts and planted support feet pass. Encoded sample frames were inspected for overlaps and role coverage.
- [Encoded checks](checkpoint-checks.json): both clips fully decode, contain 288 frames / 12 seconds, and carry stereo 48 kHz audio. A measures −17.51 LUFS / −2.04 dBTP; B measures −18.73 LUFS / −2.04 dBTP. Foreground gain is identical; loudness measurements differ because the ambience changes the gated measurement.
- Shared guard self-check passes for missing, pending, agent-only, accepted, changed, rejected and explicitly waived reviews. An actual full-render attempt was stopped before rendering because staging acceptance is absent.
- Installed skill validation passes. The original audio source-boundary failure was corrected by limiting the final cheer cue to 6.2 seconds of its 6.24375-second source.
- Actual listening is pending user audition. File measurements do not establish whether the new crowd sounds convincing. The full 38-second cut, all transitions, supporting faces and final polish have not passed user review.

## Reproduction record

The current revision uses `scripts/build_staged.py`, `verify_staged.py`, `sound_staged.py`, `render_staged.py` and `finish_checkpoint.py` in this film. The two candidate plans feed the existing `pipeline/audio.py`; successful current audio outputs are `audio-clean-v003/` and `audio-crowd-v003/`. `finish_checkpoint.py` applies the same +3 dB gain and peak limiter to both, trims 10–22 seconds, muxes the same native picture and checks each encoded result. It refuses to overwrite review files.

`render_staged.py` defaults to the short proof. `--animatic` requires staging and sound acceptance; `--full` additionally requires animatic acceptance. Record real user decisions with the existing journal helper and bind the actual reviewed artifacts, following the pipeline guide. Do not mark a review accepted merely to make a render command run.
