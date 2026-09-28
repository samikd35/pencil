# S07 v003 — performance revision

12.5 seconds, 300 frames at 24fps. Review candidate; not final film approval. Existing likeness, traced artwork, environment, connected v002 clothing and all three original voice recordings are retained. No voice is sped up or regenerated.

## Performance changes

The assistant approaches in 17 frames, presents the seven-goal sheet, makes a short open-hand request and waits. His eyes change before his head/body recoil on the punchline; his mouth briefly opens, then closes into a disappointed expression. Flick finishes discrete writing strokes, looks up eyes-first, gives two restrained gesture accents, and holds between them. His watch, clipboard and roll actions occupy a tighter ending. The paper rests on the repositioned stand before the grip releases.

Camera cuts: two-shot → Flick at frame77 → assistant at161 while Flick finishes speaking → action wide at206. These are motivated cuts with held framing, replacing the slow reply push. The entire scene is shorter through new motion timing and reduced waits, not a faster playback rate.

| Beat | New frame | Preview time |
|---|---:|---:|
| Assistant line | 13 | 0.50s |
| Flick line | 88 | 3.625s |
| Assistant reaction | 171 | 7.083s |
| Offscreen keeper line | 202 | 8.375s |
| Watch | 238 | 9.875s |
| Clipboard contact | 254 | 10.542s |
| Hand meets ball | 277 | 11.50s |
| Release | 286 | 11.875s |

## Focused review

Initial pose inspection exposed an elbow inversion while the sheet was lifted. A fixed world-space bend guide crossed the arm axis. This shot now uses a consistent authored bend branch; wrist targets and the return path were revised to avoid tightly passing through the shoulder. The paper-holding forearm now has a foreground skin pass so it remains visible when crossing the shirt. This is a shot-specific pose correction, not an assertion that every future pose uses the same branch. Maximum per-frame elbow displacement is checked to catch the detected discontinuity.

Numerical checks cover all 600 actor poses, fixed segment lengths, planted feet after approach, hand/ball contact and complete dialogue tails. Connected silhouette assertions remain active for both actors. The encoded-frame review prioritizes presentation, eye/head changes, the punchline reaction, watch/clipboard transition and consecutive release frames. Normal-speed audience response and subjective listening remain unverified by the agent; the playable clip is the motion-and-sound checkpoint.

## Remaining limits

Head direction still uses the existing three-quarter artwork with tilts and gaze changes, not newly drawn full head turns. Mouth shapes are limited and not a full phoneme performance. Hand drawings, sleeve volume and environmental finish still need the shared polish pass. This revision does not resolve the adjacent S06 training counter/eight versus S07 match-result/seven ambiguity or the deferred S08 wrists.

## Sources

`revise_coaching_performance_v003.py` owns the new poses, timing, facial reaction, camera and contacts. It reuses `build_coaching_v001.py` for character construction and `revise_coaching_surfaces_v002.py` for connected garment drawings. Run its documented batches in the visible Blender session; render the saved native scene with `render_staging_scene.py -- S07 S003_S07_Coaching_v003 coaching` after the shared audio build. `source/` freezes these files. The native scene needs no runtime handler or Shapely during playback.

`production-before.json` retains the previous selection. S07’s duration changes from15 to12.5 seconds and subsequent shot starts shift60 frames earlier; the full-film plan becomes205.5 seconds. `render-selection.json` is a snapshot with paths relative to the video root. Previous scenes, previews and voice models are preserved. The prior 53-second passage remains its historical v001 edit and does not contain this revision.

## Encoded delivery check

The delivered MP4 decodes fully: 300 frames, 1280×720, 24fps and 48kHz stereo, exactly12.5 seconds. All original voice hashes match; each dialogue cue ends before the cut without trimming. `coaching-before-after.mp4` plays the old15-second version followed by this12.5-second revision, both at their original playback speed.

Reviewed `gestures-review.jpg`, `ending-review.jpg` and enlarged `joint-contact-review.jpg` from the final encoded frames. Presentation and reaction poses retain the foreground forearm; the ending keeps the hand with the ball until release. Residual limitations are visible: the assistant’s grip is a stiff fist-like drawing, Flick’s sleeve silhouette becomes angular during the board transfer, and the pen-hand orientation is schematic. These remain explicitly deferred polish, not a claim of benchmark quality.
