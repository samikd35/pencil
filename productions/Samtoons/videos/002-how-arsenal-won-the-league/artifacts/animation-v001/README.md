# Animation progress v001 — one body-motion shot

[Full progress movie](arsenal-progress-v001.mp4) · [Editable full timeline](arsenal-progress-v001.blend) · [Pep shot with existing sound](CP03_pep/CP03_pep-v002-with-audio.mp4) · [Editable Pep scene](CP03_pep/CP03_pep-v002.blend)

The user accepted the complete Bottle FC storyboard and authorized animation. This revision replaces only CP03_pep at119.167–123.167seconds. The rest of the film remains the accepted storyboard. It is not a finished film, completed chase or approved gait improvement. No new approval gate is requested for this local work. Loaded running, interactions, other movement, facial acting and full music development remain outstanding.

## What changed

Prepared an original native pose guide to make leg roles and contact/down/passing states explicit. Generated matching whole-character artwork, keeping face, clothes and shoes coherent. Two generated fourth-column poses did not supply the intended toe-off and were excluded. A single-pose alternative also failed the intended overlap and was not used. Six selected drawings provide this internal candidate; still-image interpretation of their leg roles remains a limitation, not an automated anatomy pass. The shot needs normal-speed qualitative judgment in the wider chase context before final adoption. The original accepted Bruno action remains the quality floor.

The [Animation Mentor walk tutorial](https://www.animationmentor.com/blog/tutorial-animating-human-walk-cycle/) was read for its contact/down/passing/opposite-contact blocking and separated root travel approach. Its embedded video was not watched. Existing Bayern benchmark all-04 frames240–319 were visually inspected for changing locomotion silhouettes and screen direction; they are running examples, not a verified calm-walk performance reference. The authored technical pose diagram is a construction guide, not independent evidence of good acting.

Pep uses complete painted poses with explicit neck and support registrations, independent continuous world travel/camera, and connected lower-body support compensation. This is a body-motion pass: mouths are not animated. Original selected Pep dialogue and the full accepted soundtrack are unchanged. Native geometry does not certify the character's normal-speed appeal.

## Reproduced implementation defect and correction

The reused root's ID-property limits still specified0–3 although the new library had six drawings. Blender's evaluated pose value at frame28 was3 while its authored F-curve requested5. That suppressed both new second-half poses. `fix_pep_selector_v002.py` resets hard/soft bounds to0–5. `check_pep_shot_v001.py` now asserts every evaluated index equals the authored exposure and evaluates actual geometry. It fails on the preserved library and passes the corrected saved scene.

This defect was introduced by expanding the reused control; it is not asserted to explain the old four-drawing chase's artistic rejection. Original builders already initialized bounds from their own drawing count. The new builder now does the same after replacing the library. Shared motion guidance documents the observed reuse failure.

Captured results: all96pose selections match; evaluated lower-support error below6e-8worldunits; horizontal registration range below0.001pixel; uniform independent camera travel; all complete pose meshes inside camera. Rendered96frames at24fps/1280×720. Full progress export decodes, retains5954frames, and its native56-strip timeline reopens with all dependencies. Source sheets and consecutive encoded contact frames were inspected. Agent normal-speed playback and audio listening were unavailable; no subjective acceptance is invented.

## Native fallback and files

The guide and initial scene were authored through visible Blender. The connector then disconnected; the current visible application showed a different unsaved Untitled cube scene. That window was left untouched. The one-property correction and progress timeline packaging used saved files in a separate background process, and were checked by reopening them. No claim that these fallback edits were shown live. Earlier sources, deliveries and rejected candidates remain intact.

- `CP03_pep/CP03_pep-library.blend` and first movie preserve the clamped-selector failure.
- `CP03_pep/CP03_pep-v002.blend` and `CP03_pep-v002-with-audio.mp4` are the corrected candidate.
- `CP03_pep/selector-check.json`, `native-checks.json`, `motion.json`, `poses.json`: implementation evidence.
- `edit.json`, `checks.json`: complete progress edit scope and exact output hash.
- Artwork, technical guide and generation prompts: ../../assets/chase-poses-v003/.
- Source/score credits remain those of ../animatic-v001/CREDITS.md. Existing source audio comes from ../opening-v002/mix-premaster.wav.

Keep earlier artifact directories: the full native timeline references their unchanged clips and audio. Use a new version for later revisions rather than overwrite this evidence.
