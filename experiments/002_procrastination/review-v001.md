# Just One Thing — rough animatic review

10 September 2026. Delivery status: ready for user story review; creative acceptance pending.

[Watch the three-minute film](artifacts/animatic-v001/just-one-thing-animatic.mp4). [Editable Blender project](artifacts/animatic-v001/just-one-thing.blend). [Timed storyboard](storyboard-v001.md).

## What this version tests

An original, entirely wordless story using the actual C / Elastic Comic asset. One picture needs hanging on an existing hook. Measuring leads to lists, then a planning board, then a loop of consulting the preparations. The picture remains untouched. The character notices it, puts down the pencil and finally hangs it. A final crooked-frame temptation resolves with a simple nudge.

The 180-second edit contains 68 held key poses, framing changes and original synthesized music/Foley. No third-party recordings, AI voices, narration or on-screen explanatory captions are used. These held poses establish staging and editorial timing; they are not a claim of finished character animation or production-grade motion.

## Review observations

- The opening pairs the floor picture with an insert of the empty hook, then shows an interrupted hanging attempt. This makes the task concrete before the first detour.
- The room accumulates a desk, paper pile, board, tool box and connections while the original task stays visible in recurring wide shots.
- The quiet passage begins around 02:02. The picture and hook get a second pair of inserts before the character changes course.
- The final task is completed around 02:35; the crooked-frame callback tests whether the character's new behavior reads.
- The middle repeats list/board poses, especially around 01:39–02:02. This is the first passage to scrutinize for lost attention. A viewing response should determine whether to shorten it, rewrite the gags or invest in acting there.

Contact sheets were visually inspected across all 68 panels. A few medium task shots initially cropped foot contact, and one pleased reaction retained an effort expression; these were corrected before delivery. This is an authored review, not independent audience comprehension testing. No claim that three minutes has been proven engaging is made.

## Verification

- Encoded duration: exactly 180 seconds; 4,320 frames at 24 fps; 1280 × 720; stereo audio.
- Every encoded panel midpoint was compared with its source render within compression tolerance; the full video/audio decoded successfully.
- Existing character vector geometry and 48 limb endpoint drivers were reused. Episode props, poses and camera choices are new.
- The saved Blender timeline is checked after reopening, including each panel's camera scale and character position. The mastered review soundtrack is embedded for portability.
- The first export was rejected by its timing assertion at 178.916667 seconds. Explicit frame-rate conversion corrected the delivery; the failure and correction are recorded in the journal.

Check reports are in `artifacts/animatic-v001/`: `build-checks.json`, `video-checks.json`, `delivery-checks.json` and `project-checks.json`. Music and effects provenance is in `audio-report.json`. Episode state and exact panel durations are in `story.json`.

## Next decision

Watch once without reading the storyboard. Record the first moment attention drifts, whether the original task is clear, and whether the ending feels earned. Revise the story/edit based on that response before adding in-between motion or more visual polish. No new pipeline abstraction is required for this decision.
