# Complete-film review v026

Current 4:36.4 complete review export: `samtoons-complete-v026.mp4`, 1280×720, 24 fps, 48 kHz stereo. This is a review candidate, not a claimed completed listening or normal-speed motion review. Native 1080p rendering has not been performed in this pass; the supplied movie is not upscaled.

## Preserved decisions

The user approved the v025 hand/body-movement fixes after the focused-review clarification. The v025 native file remains the selected animation source. First 2992 frames use the accepted v022 cumulative prefix. All remaining animation timing and scene order are preserved. The full encoded v025 audio is stream-copied into v026; matching decoded PCM SHA-256 verifies exact audio preservation. Voice models and references are untouched.

## Review and concrete corrections

Inspected 106 sampled frames: two frames, at approximately 25% and 75%, in each of the 53 shots. `shot-map.json` and `inspect-1.jpg` through `inspect-7.jpg` identify coverage. This checks sequence, framing, visible text and context; it does not establish smooth motion at normal speed. The supplied user approval covers the prior movement fixes.

The cumulative sequence communicates the Bottle FC subscription, striker/corner-flag setup, defensive formation, City pursuit, annual second-place delivery, VAR cancellation/corner, accidental winner, redirected medals, corner-side celebration and Ferguson reveal. The earlier City notification and new CP00 restatement both remain, preserving the authorized explicit chase explanation.

Found and corrected:

- Six long subtitles used a greedy character split, leaving brief one-word fragments or revealing later clauses too early. Replaced them with complete phrases at cached speech-analysis pauses: C00, C19, C30, C31, C35 and C46. Exact dialogue is preserved and asserted by the finishing script. Speech-analysis timing is approximate, not a listening certificate.
- Two music captions overlapped during the reveal. The suspense caption now ends where the final-note caption starts.
- The post-goal `1 ARSENAL 2 CITY` graphic could be mistaken for a losing match score. Its editorial replacement explicitly says `LEAGUE TABLE 1st ARSENAL 2nd CITY`. This is an editable finishing overlay in the script, not a native rig change.

Inspected the resulting encoded frames at 127.5, 130, 185, 187.5, 190, 193, 212, 215, 239, 262, 265 and 272 seconds. `finishing-review.jpg` records those frames. Approved character bodies, hands, animation and voices were not reconstructed.

## Timing and audio evidence

All 47 planned dialogue cues finish before their scene boundaries, with a minimum 0.513-second margin, and none is trimmed at the film boundary. `dialogue-boundaries.json` records every cue. This establishes edit placement, not whether a source voice take has perfect pronunciation or natural delivery. The focused hand excerpt intentionally cuts between selected intervals; those excerpt cuts are not used in the complete film.

Full-file decoding passes: 6634 video frames; video duration 276.428304 seconds; audio duration 276.45 seconds. The difference is about 22 milliseconds. Sound measurement of the unchanged full encode: -16.84 LUFS integrated, -1.14 dBTP, 10.50 LU loudness range. No new normalization was applied. `audio-measurement.log` is a numerical analysis, not agent listening.

Agent cannot hear playback through the available tools and has not claimed a full normal-speed audiovisual review. The complete file is supplied for that final human playback check. The user's hand-fix approval is retained; it is not promoted to an unheard full-film delivery approval.

## Reproduce

Run `python3 scripts/finish_review_v026.py` from this video directory (or use its full path). It reuses v025 clean remainder picture, v022 accepted prefix, v024 captions/timing and v025 full soundtrack. Assertions cover phrase preservation, caption duration/line count, final frame count/format, full decode and decoded-audio identity. Keep the linked source revisions available. Final checks are in `checks.json`.
