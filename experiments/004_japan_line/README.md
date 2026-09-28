# How Was This Ball Still In?

[Watch the Short](artifacts/film-v001/how-was-this-ball-still-in.mp4) · [Editable Blender project](artifacts/film-v001/japan-line.blend)

32 seconds · 1080×1920 · 24 fps · no narration. Original instrumental music, designed atmosphere and 28 timed Foley cues.

The film opens on Mitoma chasing the ball and asks **IN OR OUT?** A close illustrated sphere stays fixed while the camera moves overhead. A highlighted cap reveals the overlap with the line. A separate rule demonstration shows the whole ball crossing the boundary, then returns it. The film returns to the match action: Mitoma's cutback, Tanaka's finish and Japan's 2–1 result.

The intended audience payoff is understanding why the ball could look out while remaining in play. That payoff, rather than the production tool or a redraw of a highlight, governs this episode.

## Historical basis and illustration

Japan beat Spain 2–1 on 1 December 2022. Ao Tanaka scored the winner in the 51st minute after Kaoru Mitoma's cutback. The ball had not wholly crossed the goal line, and the goal stood following the VAR check. [FIFA match account](https://www.fifa.com/en/articles/world-cup-upsets-japan-spain-2022), [RTVE replay and photo analysis](https://www.rtve.es/deportes/20221202/video-gol-japon-espana-var-replay-mundial-2022-qatar/2410751.shtml).

The ball is out when it has wholly passed over the boundary line, on the ground or in the air. Its curved edge matters, as well as its ground-contact point. [IFAB Law 9](https://www.theifab.com/laws/latest/the-ball-in-and-out-of-play/).

Match action is a condensed, stylized reconstruction. Player positions, poses, pacing and camera setups are illustrative. The macro sphere and its gap are a rule illustration, not an exact measured reconstruction or authentic VAR display. The explicitly labeled comparison moves the ball outside and back to demonstrate the rule; this is not additional match action. No exact distance, ball-sensor decision or automatic goal-line-technology claim is made.

The [official goal page](https://www.fifa.com/en/watch/c_eO4oo9k0KkMR0089vUTQ) and broadcaster references informed the event, kit colors and actions. No source footage, commentary, music or audio recording appears in the film.

## Motion and visual review

The native C / Elastic Comic character's editable shapes and controls are retained. This episode adds authored sprint and stretch poses, a cutback and recovery, knee contact for the finish, camera tracking, a physical sphere/camera orbit and a highlighted geometric overlap. The match artwork stays simple and uses the screen for action; the rule reveal deliberately uses a large shaded sphere.

Draft review corrected a hand that read too close to the ball, sprint foot sliding, annotation shadows on the sphere, low contrast, faceted panel normals, conflicting visibility groups and goal framing. Revised review covered 19 rendered samples, with full-size checks of the frozen touch, overhead overlap and knee finish. [Revised frame review](artifacts/film-v001/stills/review-revised.jpg).

Evaluated project checks passed: boot contact, clear hands at the frozen touch, two planted sprint-foot intervals, knee contact, stationary sphere throughout the camera reveal, correct visible in/out labels, continuous ball rotation on resuming play, goal visibility and annotation shadow settings. The original source character project is unchanged, verified by its SHA-256 hash. [Project checks](artifacts/film-v001/project-checks.json).

The final export passed full-file decode and format checks: 768 frames, 32.00 seconds, 1080×1920, 24 fps, stereo 48 kHz AAC, −15.77 LUFS integrated loudness and −1.74 dBTP true peak. [Video checks](artifacts/film-v001/video-checks.json) · [Audio checks](artifacts/film-v001/audio/export-checks.json).

Final visual review included decoded motion samples of the chase and finish, plus full-size exported views of the in/out demonstration. [Chase sequence](artifacts/film-v001/stills/motion-chase.jpg) · [Finish sequence](artifacts/film-v001/stills/motion-finish.jpg) · [Exported frame review](artifacts/film-v001/stills/final-contact-sheet.jpg). Mitoma's trailing hand briefly remains at the right edge as the camera follows the cutback; the full pose leaves the shot continuously. Supporting-player placement is illustrative, with the ball drawn in front of them during the cross.

These technical results and sampled visual reviews do not establish audience comprehension, subjective sound quality or world-class status. Creative acceptance remains with the user; audience response has not been tested.

## Working files and reproduction

The saved Blender file includes the animated artwork, camera, macro geometry and embedded normalized soundtrack. It opens on the overlap reveal. [Separate sound stems and cue record](artifacts/film-v001/audio/) remain available.

Run the production steps in order:

1. Blender background mode: `scripts/build_film.py` (optional `-- --samples` for review frames).
2. Python with NumPy: `scripts/make_sound.py`.
3. Blender background mode: `scripts/verify_project.py`, which checks and packs the soundtrack.
4. Blender background mode: `scripts/render_film.py`.
5. Python: `scripts/finish_delivery.py`, which assembles and verifies the final video.

This delivery used Blender 5.2.0 LTS and FFmpeg. Helpers are reused from the two earlier experiments, with their source hashes recorded. `artifacts/layout-v001/` preserves the first layout and its script. `picture-master.mp4` is a silent intermediate; the viewing copy is `how-was-this-ball-still-in.mp4`. [events.jsonl](events.jsonl) records actual production work through the existing journal helper. No new pipeline framework or database was added.
