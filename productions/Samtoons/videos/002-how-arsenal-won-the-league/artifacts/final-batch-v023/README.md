# Samtoons 002 — final combined batch v023

This is the remaining animated review batch, awaiting user playback acceptance. It is not a claim of final artistic approval or a 1080p delivery master.

## Selected construction

- Arteta and front-view Gyökeres: copies of the accepted v016 complete illustrated surfaces, fitted armatures and independent body controls. These are deforming illustrated meshes, not native Grease Pencil strokes and not static image cards. Native mouth/teeth and eyelid controls follow the fitted face.
- Saka, Gabriel, defenders and keeper: accepted v021 reconstructed neutral full-body rigs. The release reuses the accepted approach/boot-contact action rather than holding a crossed leg image.
- Courier, referee and VAR operator: newly measured complete drawings fitted using the same construction function. Source body proportions and joint locations are measured independently. New artwork: `assets/final-cast-v023/support.png`.
- Rear Gyökeres: a coherent complete drawing for the required rear view, with its own fitted control landmarks, not a rear body with the old head pasted on. Source: `assets/final-cast-v023/gyokeres-rear.png`.
- Chase: complete matched action drawings, animated pose changes and measured support corrections from the existing chase sources. This route covers the loaded run and Pep walk. The wide chase drawings do not have the same independent speech surfaces as the dialogue rigs; do not describe them as word-perfect lip sync.
- Ferguson: existing editable native mesh/curve body, clothing and facial artwork from v008. The room collection is the same set as the accepted narrator opening. The silhouette and reveal share camera framing.

## Edit and sound

The remaining 33 shots total 3,586 frames at 24 fps (149.417 seconds). The accepted prefix contains 2,992 frames (124.667 seconds). Together: 6,578 frames, approximately 4:34.

`edit.json` maps every shot to a saved scene. `audio-plan.json` is the soundtrack authority; `mix/` contains its stems and premaster. Cached selected voices are reused. New Arteta takes retain the selected B02 reference and local Base voice model; no voice model was removed. Named sound contacts include corner release 29, backside impact 8, goal crossing 24, operator button 9 and paper/TV tap 32 in their respective shots. Speaker captions retain NARRATOR until the reveal, plus music labels. Long caption phrases use proportional timing, not claimed word alignment.

`build_final_v023.py` constructs the scenes in the visible Blender instance using the existing live source registries. Apply `refine_final_v023.py` after it. The saved native scene library is the reproducible render input; it does not require those live builder registries to render. `render_final_v023.py` streams the saved scenes into the named clips and skips valid completed clips. `finish_audio_final_v023.py` prepares sound and subtitles; `package_final_v023.py` packages and checks the combined review. Run scripts from the project root, retaining the existing local voice runtime for sound assembly.

## Corrections found in actual inspection

- Some newly fitted fingers were classified as lower-body pixels because the old hand region ended relative to the hip. The fitting region now includes the source fingertips and its surrounding mesh fringe. The keeper's glove fringe is assigned to its hand. This removed the observed stretched spikes; it is not a universal garment-weight preset.
- Phone poses initially compressed the arm too tightly against the head. The same characters now hold the phone near the mouth with a lower elbow. The operator presses a button on the near-hand side of the desk instead of crossing an unreachable arm through the torso.
- The courier stands by a roadside trolley as the runners pass, avoiding root translation with stationary feet.
- The inherited stadium collection contained shadows tied to earlier actors. Only environment objects are reused for these new shots; old actor shadow marks are excluded.
- Trophy height and hand targets are coordinated, with a wider team frame so the trophy no longer covers the lead's face.
- The ricochet uses an evaluated shorts-surface point and a ball-radius offset. The cross, complaint and impact share continuous endpoints. The complaint deliberately uses extended comic airtime for the dialogue; this is not a real-time ballistic simulation.

## Review evidence and limits

The agent inspected actual rendered frames of the phone gestures, press, shirt pull, loaded run, courier pass, corner release, missed header, backside impact, trophy, silhouette, reveal and paper tap. Consecutive CP01 frames were inspected for changing stride/support. The renderer also saves dense three-frame samples for the principal contact shots. No cross-scene bone constraint targets were found in the 33 current scenes.

These are scoped visual and numerical checks, not a claim that every frame was watched in real time. Agent listening was not performed. The review movie is for the user's normal-speed assessment of performance, humour, sound and any remaining visual defects. Existing accepted footage is preserved, and new clips remain unapproved until that review.

## Packaged review

- `samtoons-complete-review-v023.mp4`: complete 720p review, 6,578 frames, approximately 4:34, with selected soundtrack and burned-in speaker captions.
- `final-batch-review-v023.mp4`: remaining 33 shots only, approximately 2:29.
- `samtoons-complete-review-v023.srt`: external subtitles for the complete cut.
- `final-batch-v023.blend`: 33 editable native scenes. The saved file was reopened successfully after Blender closed during optional per-shot audio attachment. That attachment is not claimed as completed.
- `samtoons-complete-review-v023.blend`: separate Blender review timeline, referencing the complete movie and its soundtrack, with markers for the new shots.

Both encoded movies fully decoded and passed frame-count, size, frame-rate and stereo sample-rate checks. All 2,992 decoded prefix frames are pixel-identical to the accepted prefix (`prefix-preservation.json`). Final caption frames at complete-film seconds 128, 190 and 265 were inspected; Ferguson's two caption lines use the selected combined take's existing timing record. The combined video duration reported by the muxer is 274.095 seconds, with audio 274.116 seconds; this small container timing difference does not change the 6,578-picture-frame count.

The operator button is staged on the near-hand side for its press insert, while earlier office shots retain the original desk placement; this is a remaining prop-continuity detail for playback review. The chase pose drawings also retain simpler facial animation than the dialogue rigs. These are not described as solved or equivalent to every accepted acting detail.
