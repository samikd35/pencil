# Barcelona wasn't ready. Trent was.

A 38-second vertical football comedy in the user-selected **advanced stickman** style: thin articulated limbs, expressive illustrated heads, narrow team jerseys, a textured 3D field and painted stadium. A sleeping head and sleeping knees make the opening inattention joke explicit. The real corner, first-time finish and result then unfold in one uninterrupted action view, followed by a slow replay.

Current revision: **film-v004, completed revision**, following the user's 12 September feedback. The user accepted the expanded waiting-player arrangement, selected sparse sound A, then delegated the remaining checkpoint decisions for this video. This revision adds varied supporting faces, corrects the match kit, improves the kick backswing and two close-up cameras, and removes the rejected synthetic atmosphere/music. [Current revision and workflow notes](artifacts/film-v004/review.md). The [current script](script-v005.md), [cast map](staging-v005.json) and [packed native scene](artifacts/film-v004/trent-corner-advanced.blend) remain editable. The [12-second A/B checkpoint and user decisions](artifacts/film-v003/checkpoint-review.md) are preserved.

Current delivery: [38-second movie](artifacts/film-v004/barcelona-wasnt-ready-trent-was.mp4), [editable package](artifacts/film-v004/trent-corner-editable-package.zip), [selected soundtrack](artifacts/film-v004/soundtrack.wav), [encoded checks](artifacts/film-v004/video-checks.json). 1080 × 1920, 24 fps, stereo 48 kHz. Final encoded frames and contact sequences were inspected; full-film listening by the producer was not performed.

The material below documents the preserved **film-v002 export**, whose sound and sparse staging prompted the revision. Its technical passes did not establish listening quality. `film-v001` is an older technical draft; `treatment-v002` is a superseded full-bodied concept.

## Preserved film-v002 export

[Editable production package](artifacts/film-v002/trent-corner-editable-package.zip) includes the movie, native scene, selected source assets, separate stems, mix, plan, scripts and review/check records.

- [Playable film](artifacts/film-v002/barcelona-wasnt-ready-trent-was.mp4)
- [Editable Blender project](artifacts/film-v002/trent-corner-advanced.blend), with head artwork, stadium, font and authoritative soundtrack packed.
- [Final stereo WAV](artifacts/film-v002/audio-v001/soundtrack.wav)
- Separate [atmosphere](artifacts/film-v002/audio-v001/stems/atmosphere.wav), [Foley](artifacts/film-v002/audio-v001/stems/foley.wav), [music](artifacts/film-v002/audio-v001/stems/music.wav) and [comic/editorial](artifacts/film-v002/audio-v001/stems/editorial.wav) stems.
- [Audiovisual script](script-v003.md), [preserved production plan](artifacts/film-v002/production.json), [resolved audio cues](artifacts/film-v002/audio-v001/resolved-cues.json), [native project checks](artifacts/film-v002/project-checks.json) and [encoded movie checks](artifacts/film-v002/video-checks.json).

1080 × 1920, 24 fps, 912 frames, 38 seconds. Original nonverbal sound; no narration, dialogue or archival match footage/audio. Main action contacts are at 16.750, 18.000 and 18.625 seconds; replay contacts are at 26.333, 28.000 and 28.833 seconds. The last 0.4 seconds intentionally lets the soundtrack rest.

## Fact and fiction

On 7 May 2019 Liverpool overturned Barcelona's 3–0 first-leg lead with a 4–0 win at Anfield. Trent Alexander-Arnold's quick corner supplied Origi's decisive goal. [UEFA match report](https://www.uefa.com/uefachampionsleague/news/0251-0e99aae66a0d-4ef82ebc84f0-1000/).

Origi was unmarked and scored in the 79th minute. [Premier League report](https://www.premierleague.com/en/news/1212312). Shaqiri recalled approaching the corner, believing he would take it, before Trent delivered it quickly. [Liverpool FC interview](https://www.liverpoolfc.com/news/first-team/392432-xherdan-shaqiri-interview-world-champions-barcelona-ronaldo-idol).

The pillow, sleeping knees, sleep puffs and wake-up reaction are invented visual jokes. “CARTOON TIME” introduces the cutaway; normal bodies return before the match action. Defenders are representative figures. Player spacing, stadium proportions, gestures and appearance are stylized; this is a narrative reconstruction, not tracked match footage. The important action order and 4–3 aggregate outcome are retained. More source notes are in [brief.md](brief.md).

## Editable construction and assets

The scene has one coherent 3D pitch, goal and ball path. Limbs are native curves with editable points and frame keys; boots, shirts, camera, captions, expressions and comic props are separate native objects. Heads use three illustrated expressions per design on native silhouette meshes. The generated head sheet contained a baked checkerboard; native silhouette geometry excludes that background while retaining the source image's pixels.

Original image-generation prompts and selected assets are in `design/treatment-v003/`: `prompt.txt`, `concept-board.png`, `heads-prompt.txt`, `heads.png`, `stadium-prompt.txt` and `stadium.png`. The board establishes the visual direction; the movie uses separately authored native motion. The stadium panorama is mapped onto distant walls, so very wide views simplify real stadium perspective.

Film-v002 audio selections and provenance are preserved in `artifacts/film-v002/production.json`. Twelve cached original synthesized sounds are reused; `sound_advanced.py` adds a deterministic snore. `pipeline/audio.py` owns exact event-to-sample alignment, stem assembly and premaster checks. Two-pass FFmpeg loudness finishing creates the authoritative WAV used in both the movie and Blender. Individual stems remain at their authored pre-normalization levels; reproduce the final balance through the documented premaster/normalization flow. This rejected sound direction is historical, not the default for the new revision.

## Verification and reproduction

`verify_advanced.py` checks all 912 frames for one active head expression per character, main/replay toe-ball contact, two planted support-foot intervals, continuous ball travel outside the intentional replay reset, action/replay ball framing, score states, native event markers and packed dependencies. `finish_advanced.py` checks the encoded movie's dimensions, frame count, duration, full decode, stereo 48 kHz audio, integrated loudness and true peak. The encoded movie passes full decoding and measures −18.19 LUFS integrated with a −2.00 dBTP true peak. Technical checks do not certify humor or comprehension. Actual listening and audience response remain unverified.

From this Pencil workspace, run:

```sh
experiments/007_trent_corner/scripts/reproduce-advanced.sh
```

Tested runtime: Blender 5.2.0 LTS, its bundled Python 3.13/NumPy, system Python 3 and FFmpeg 8.0.1. The shell script uses the installed macOS paths. It creates a fresh dated `film-v002-rebuild-*` directory, preserving the delivered movie and mix. Cached source assets must remain in place. It uses Blender's native FFmpeg output to avoid per-frame temporary PNG files, then muxes the finished soundtrack. No additional package installation is required in the current workspace.

The append-only [production journal](events.jsonl) records source selections, revisions, concrete failures and verification evidence.
