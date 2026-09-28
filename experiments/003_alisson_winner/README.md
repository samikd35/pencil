# The Goalkeeper Who Scored the Winner

[Watch the completed Short](artifacts/film-v001/the-goalkeeper-who-scored-the-winner.mp4) · [Editable Blender project](artifacts/film-v001/alisson-winner.blend) · [Frame review](artifacts/film-v001/stills/final-contact-sheet.jpg)

40 seconds · 1080×1920 · 24 fps · 960 rendered frames. Original instrumental music and sound effects; no narration. Seven basic stick figures reuse the C / Elastic Comic character's editable shapes and controls. Football movement, stadium, ball, staging, camera movement and sound were authored for this film.

Alisson leaves his goal, runs upfield, meets Trent Alexander-Arnold's corner and heads Liverpool's late winner. The score changes from 1–1 to 1–2, followed by a celebration and his name. Kit colors, gloves, shirt numbers and sparse English captions establish identities without changing the simple character design.

## Historical basis

West Bromwich Albion 1–2 Liverpool, The Hawthorns, 16 May 2021. Alisson headed the 95th-minute winner from Alexander-Arnold's corner. The result helped Liverpool's Champions League qualification pursuit; it did not itself secure qualification or win a trophy. [Liverpool match report](https://www.liverpoolfc.com/news/first-team/434274-alisson-becker-west-brom-premier-league-match-report).

Robertson described Alisson running past him to join the attack. [Robertson's account](https://www.liverpoolfc.com/news/first-team/434370-any-striker-in-the-world-would-be-happy-with-alisson-s-header). [Official highlights](https://www.youtube.com/watch?v=rDa5A20jDGs) were inspected for visual reference, including kit colors and empty stands. No footage or broadcast audio appears in the film.

This is a condensed, stylized reconstruction. Poses, player placement, camera projection and slow motion are authored for clarity. The supporting players are illustrative; their positioning is not a tactical reconstruction.

## Review and verification

Technical checks passed: 960 decoded frames, 40.00 seconds, H.264 portrait picture, 48 kHz stereo AAC, full-file decode without reported errors, −16.01 LUFS integrated loudness and −2.97 dBTP true peak. The scene contains 336 valid limb drivers. Evaluated geometry checks verified boot/ball and head/ball contact and a stationary planted support foot during the corner kick. The source character project remains unchanged. [Video checks](artifacts/film-v001/video-checks.json) · [Project checks](artifacts/film-v001/project-checks.json) · [Audio checks](artifacts/film-v001/audio/exported-audio-check.json).

Agent visual review covered 19 decoded final frames across the film, including the full-size header contact. Draft review led to corrected pitch boundaries, clearer foreground staging, focused pre-goal expressions, aligned corner-kick contact and a continuous ball drop after reaching the net. The final frame sequence shows the delivery, jump, contact, goal, score change and celebration. This sampling and the numerical motion checks do not replace audience testing or a complete subjective listening review. Final user acceptance is pending.

## Editable delivery and tracking

The Blender file contains the corrected character and ball animation, original environment, camera, text and an embedded soundtrack. It opens on the header at frame 541. Individual music, atmosphere and Foley stems, a normalized mix and 44 timed sound cues remain in [audio](artifacts/film-v001/audio/).

The production record is [events.jsonl](events.jsonl), using the existing journal helper and file hashes. [brief.md](brief.md) holds the story and source boundaries. `artifacts/layout-v001/` preserves the first layout for comparison; `artifacts/film-v001/` contains the delivery. `picture-master.mp4` and `net-correction.mp4` are silent intermediate files; the linked completed Short is the viewing copy.

The scripts record the working steps: `build_film.py` authors the scene; `make_sound.py` creates the original sound stems and unnormalized mix; `render_film.py` renders the saved project; `pack_and_verify_project.py` embeds the normalized soundtrack and checks evaluated geometry; `finish_delivery.py` assembles and verifies the final MP4. The saved two-pass loudness logs document the normalized soundtrack. The final assembly uses a replacement render of frames 577–696 to incorporate the corrected net/drop motion. After future picture edits, regenerate both the full render and this replacement before reusing the assembly script.

This production used Blender 5.2.0 LTS, Python with NumPy, and FFmpeg. No new service, database or publication step was added.
