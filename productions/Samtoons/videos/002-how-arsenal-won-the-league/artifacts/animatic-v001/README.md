# Arsenal — full audiovisual animatic v001

**4:14.542 · 55 shots · 47 scripted lines · 1280×720, 24fps.**

[Review movie](arsenal-animatic-v001.mp4) · [Editable Blender edit](arsenal-animatic-v001.blend) · [Native validation](native-check.json) · [Encoding validation](encoding-checks.json)

This is an illustrated storyboard animatic: complete story, edited pose drawings, dialogue, plot sounds, music A, captions and reaction intervals. It is not the finished animation. Drawings establish whole-character poses, roles and framing; bodies do not yet move continuously and mouths are not lip-synced. The Blender VSE edit has separate shot clips, captions, event markers and the authoritative sound mix. It does not pretend that the raster boards are freely deformable character rigs.

## What this review resolves

Does the full sequence sustain the joke, are any pauses slow, and does the narrator's recognition beat lead effectively into the final meltdown? Story order follows approved script-v003: medal delivery → corner-flag signing → defensive wall → City chase → privileged VAR hotline → accidental winner → callbacks → Ferguson. All47 lines are accounted for exactly in edit/subtitle records; the selected combined meltdown performs its two final lines together.

Sound A's opening, Pep reply, referee line and combined meltdown are preserved as exact standalone selected sources. Remaining performances are newly directed local Qwen takes, still subject to listening review; identical prompts/seeds do not prove voice identity continuity. The chase score now advances continuously across picture cuts and drops out for Pep's reply. Applause favours the flag and cuts at Gyökeres' reaction. Result pings, hold tune, privileged phone ring, medal/trolley callbacks, goal contact and the narrator motif each have distinct jobs. No invented stadium-noise bed fills the film.

Agent listening unavailable. Actual audience response, accent, emotion, lip-sync and final movement quality are not certified by the technical checks. This review does not silently clear new voices or gait defects.

## Movement and drawing review

Bruno pose-action-v003 remains the accepted motion baseline. The user rejected chase-v002's walk/run quality and explicitly deferred another local test render. This animatic replaces that cycle with new complete action key drawings; it does **not** claim a solved continuous Pep walk or loaded sprint. Those actions must still meet the Bruno floor before final-quality production is cleared. Do not adapt rejected cycles unchanged.

Boards were checked and corrected for three podium carriers, Gabriel rather than Gyökeres pulling the shirt, silver courier medals, a pre-kick setup with one ball, and a final league table rather than a 1–2 match score. The defensive wide contains nine red outfield players, Raya in front and a remote tenth outfielder; the following wide isolates Gyökeres. Background lettering, kit detailing, character consistency between generated poses, precise pitch geometry and material animation remain production work. The accepted Ferguson portrait supplies his recognition and spoken meltdown; the wider throw pose follows the lines.

The encoded board review exposed slivers of neighbouring panels: generated grid rows were not exactly equal. The shot preparer now measures the actual divider rows/column before cropping every panel. Original sheets and rejected sheet versions remain in boards/. No substitute head/body construction was introduced.

Some transition ideas remain blocked as cuts, not their final moving equivalents: phone-table-to-road, formation shuffle, loaded run/walk contacts, grip match, camera approach, ball travel and the final paper trajectory. Static exposure timing must be rechecked against the eventual movement. A storyboard hold is not a validated action cycle.

## Native edit and reproducibility

- `edit.json`: contiguous frame-based55-shot exposure plan; `clips/*.json`: source crop and hash per shot.
- `voices/`: cached sources, source model and per-line performance directions; `sounds/`: adopted files and source evidence.
- `audio-plan.json`: complete shared-mixer event plan. Per-section JSONs are bounded mix inputs.
- `section-*/stems/*.wv`: lossless WavPack float stems; section premaster files plus `audio-concat.txt` reconstruct `mix-premaster.wav`.
- `float-compression-checks.json`: retained roundtrip evidence. WavPack preserves float samples exactly; WAV removal happened only after byte-for-byte decoded comparison.
- `captions.ass`, `subtitles.json`: entertainment dialogue and the CITY WIN graphic only. Production labels/credits stay outside picture.
- Film scripts: `generate_animatic_voices_v001.py`, `plan_animatic_v001.py`, `add_animatic_cues_v001.py`, `mix_animatic_sections_v001.py`, `render_animatic_boards_v001.py`, `assemble_animatic_native_v001.py`, `package_animatic_v001.py`, `check_animatic_native_v001.py`.

Scripts describe the actual internal build sequence, not a universal turnkey film framework. Use a new revision for changed review assets. Voice source generation caches existing files; audio mixer refuses existing outputs. `audio-plan.json` is the final adopted plan (including score source offsets and added plot cues); earlier planning snapshots are historical. Reuse this final plan for a straight rebuild rather than rerunning the earlier proposal step over it. Native assembly runs in the visible Blender instance and retains unrelated scenes. The saved `.blend` uses relative external clip/audio paths; keep this artifact folder together.

## Storage incident

The all-film mixer ran out of disk space while creating padded temporary batches. The failed mix log/record remain; only this task's incomplete WAV outputs were removed. Existing documented section mixing solved it, followed by lossless float WavPack compression and exact decoded-sample checks. Earlier films, approved assets, model weights and user files were not deleted. This is an operational storage change, not an audio quality reduction. Available disk remains low; avoid unbounded PNG sequences or redundant float stems during subsequent full-quality rendering.

## Approval status

Sound A selected by the user. Its original approval entry bound the movie only as input; an append-only correction binds the same unchanged movie as the checkpoint's reviewed output. No creative approval was invented or requested again.

This exact full animatic remains **pending user review**. User acceptance of pacing/staging/sound is required before a full-quality render under the existing pipeline. Movement improvements and newly introduced performances stay explicitly outstanding until judged in their actual completed form.
