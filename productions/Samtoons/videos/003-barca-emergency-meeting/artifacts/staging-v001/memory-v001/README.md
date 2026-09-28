# S10 — Same boss, different shirt · staging v001

11-second, 24 fps staging preview, continuing the accepted S09 movement/timing. This is a review candidate, not final-film quality acceptance. S07's rejected mechanics remain unresolved.

The Bayern memory shows a planted-foot finish and recovery. Flick feeds the next ball from a supported seated position. A cut keeps the rolling ball's position, speed and direction while changing the recipient to Raphinha and the setting label to Barcelona. The final cut gives Flick's unchanged expression the last beat. This is illustrative training action, not claimed match footage.

## Files

- `memory-review.mp4`: exact encoded preview with complete narration and sparse contact cues.
- `memory.blend`: native S003_S10_Memory_v001, portable baked motion and drawing replacements.
- `construction-check.json`: contact/support checks; these do not certify artistic quality or physical realism.
- `render-inputs.json`, `render-selection.json`, `source-hashes.json`: selected dependencies.
- `encoded-review/`: frames extracted from the delivered encode for focused inspection.
- `audio/`: shared-pipeline audio mix and stems, on the complete film timeline.

## Ownership and reproduction

`build_memory_v001.py` owns the new choreography, camera, source placement, period cut and garment review. The S06 builder supplies drawing primitives, source portrait assembly and exact boot contact fitting. S07's continuous-clothing helper supplies silhouette unions only; its failed movements are not used. New Robert Bayern source was generated against selected Robert likeness and the football sheet, then traced by `prepare_memory_v001.py`. Raphinha/Flick source drawings are reused.

In a fresh visible Blender session, import `scripts/build_memory_v001.py` into a persistent module; use a new output version when rebuilding an existing delivered file. Run `setup()`, `actors()`, `animate()`, `review_corrections()`, `clothing_review()`, `finish()`. Point `g.pose_shape` at the included bulk writer. No playback handler is required by the saved native file. The first bake used slower per-coordinate writes; the maintained script batches equivalent coordinates, avoiding redundant dependency updates.

Build sound from the video-root `production.json` with `pipeline/audio.py`. Render the saved staging file with `scripts/render_staging_scene.py -- S10 S003_S10_Memory_v001 memory`. This is a short staging render, not the full-quality film render gate.

## Review scope and limits

- Reviewed wind-up, strike, recovery, coach reach, ball release and period cut using rendered and encoded frame sequences, with enlarged contact crops.
- Left support foot stays planted through Lewandowski's strike/follow-through. Coach pelvis stays over the seat. Kick/reception contact is fitted to the visible boot mesh.
- First close-up rejected a shoulder seam; replaced independent jacket/arm edges with the existing continuous silhouette union and restored selected interior garment detail. The source's current-club marks are excluded from the shared memory jacket region.
- Generic relaxed hand drawings remain simplified; this proof does not establish arbitrary grips, extreme poses or new views.
- Original Robert voice reference reused. Full 8.48-second line begins at 0.5 seconds; 2.02 seconds remain after it. No speech retiming or truncation. The agent has not heard this candidate; voice performance/sound fit still need playback judgment.
- New on-field likeness and movement remain pending user staging feedback. No benchmark/world-class claim is made.
