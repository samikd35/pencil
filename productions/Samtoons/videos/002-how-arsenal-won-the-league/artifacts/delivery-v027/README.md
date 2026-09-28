# Samtoons 002 — native 1080p delivery v027

Approved creative cut: v026, explicitly accepted by the user on 21 September 2026. The v025 hand and movement fixes were separately accepted. v027 renders that selection at 1920×1080, preserving all 6,634 frames at 24 fps (approximately 4:36.4), its voices, sound design, subtitles and editorial corrections. The 1080p export is complete and technically verified. Approval of v026 is retained; it is not labelled as separate user review of v027.

## Files

- `samtoons-final-1080p.mp4`: captioned H.264/AAC film, 1920×1080, 24 fps, stereo 48 kHz.
- `samtoons-final.srt`: external speaker-labelled subtitles.
- `subtitles.ass`: editable full-film captions and title overlays, using the established 1280×720 design coordinates, rendered proportionately at 1080p.
- `approved-soundtrack.m4a`: selected complete soundtrack, copied without another audio encode.
- `sources/`: four editable Blender files, with artwork embedded. These are the actual accepted native source revisions; `edit.json` selects their scenes and local frame ranges. Their stored viewport/render defaults can remain at review resolution; the renderer explicitly sets native 1920×1080.
- `script.md`: actual performed dialogue and action plan.
- `edit.json`, `sources.json`, `source-dependencies.json`: selection, hashes and packed-dependency inventory.
- `checks.json`: final file validation and soundtrack identity.
- `clips/`: native 1080p shot encodes. Each JSON sidecar binds the source hash, scene, frame range, resolution and samples.

The model weights are working tools in the project runtime, not dependencies needed to open the Blender files or play the delivered soundtrack. They remain installed and untouched.

## Editable source map

| File | Selection |
| --- | --- |
| `sources/opening-motion.blend` | Accepted physical-action shots reused from v017: narrator opening, banner, truck, arrival, training kick and flag transition. |
| `sources/opening-dialogue.blend` | v018 retimed opening speech and reactions. |
| `sources/defence.blend` | v022 corner/header, defensive wall, coach cameos and City notification. |
| `sources/remaining.blend` | v025 chase, VAR hands, final corner/winner, corner-side celebration and Ferguson reveal. Scene names retain `clarity_v024`; the saved geometry includes v025 repairs. |

Open the file named in `edit.json`, select its `scene`, and use `local_start` through `local_start + frames - 1`. The film order is `start_frame`; source timeline positions are deliberately different. For shots with camera markers, use the latest camera marker at or before the local frame. All scene objects, rig controls and artwork remain editable. The existing film uses a hybrid of fitted illustrated meshes, native rigs/vector geometry, facial controls and matched action drawings. It is not an entirely Grease Pencil production.

## Reproduction

From the Pencil workspace, run `scripts/render_delivery_v027.py` under background Blender using its full video-local path. `-- proof` renders one native sample per shot. `-- opening` and `-- remaining` render disjoint shot groups. Resuming checks the bound source hash/scene/range/resolution instead of trusting frame count alone. Rendered frames are streamed into FFmpeg; there is no full PNG sequence. PNG compression is disabled only for temporary frame transfer; this is lossless and does not reduce drawing or render quality.

After all clips pass, run `scripts/package_delivery_v027.py` using the video-local path. It assembles shots, reapplies the approved league-table wording on its banner, renders captions at output resolution, and stream-copies the approved soundtrack. The finish uses CRF 16 H.264/yuv420p and fast-start MP4. The native scene is not a silent 720p movie stretched to 1080p; it is rendered at 1920×1080 from its authored geometry and selected artwork. Raster artwork retains its original authored resolution.

## Accepted production lessons

1. Keep a coherent whole-character drawing, recognisable face, garment joins and shoes together. Improve one feature without replacing the accepted body/motion system.
2. Fit a native rig to the actual artwork for ordinary gestures and dialogue. Use matched whole-character action drawings for extreme runs/jumps or views the fitted skin cannot support. Reusing a held extreme pose is not continuous acting.
3. A hand gesture requires the correct palm/edge/back view and finger shape. Review sleeve, elbow, wrist and hand as one chain. Keep a raised wrist on a reachable arc; straight interpolation through the elbow collapses the forearm. Bound source masks anatomically so unrelated legs or clothing are not cut away.
4. Review preparation, contact and recovery, plus the full body. A clean endpoint or passing contact coordinate cannot prove believable animation. Preserve user acceptance separately from agent checks.
5. Use a consistent shared set and physical scale. Put goals and corner flags in plausible pitch geography; narrator and reveal share one room.
6. Explain the cause before the reaction. Explicit striker/corner instructions, City pursuit and VAR decisions made the jokes readable. Keep speech and gesture timing tied to that meaning.
7. Preserve selected character voice references and cached takes. Do not regenerate a voice merely because an edit moves. Split subtitles at speech phrases; do not leave a single word flashing because a character-count threshold was reached.
8. Before final resolution rendering, verify native source/frame selections against the approved cut, especially shots reused from an earlier revision. Validate the final encoded file and compare its soundtrack with the approved one.

## Evidence and limits

The complete v026 cut and hand fixes are user approved. Agent proof comparison samples the midpoint of all 53 native shots, scaled to the approved movie for a framing/pose consistency check; numerical pixel differences are not creative approval. The final artifact checks cover dimensions, 6,634 frames, uniform frame timestamps, complete decoding, sample rate/channels, duration agreement and decoded soundtrack equality. No new agent listening claim is made.


## Completed delivery checks — 21 September 2026

Native rendering completed for all 53 shots / 6,634 frames. The final film is 1920×1080 at 24 fps, 276.416667 seconds, H.264 with stereo 48 kHz AAC; audio duration 276.45 seconds differs by 33 milliseconds (less than one frame). Complete decoding and uniform frame timestamp checks passed. Decoded PCM SHA-256 is identical to the user-approved v026 soundtrack. Final movie SHA-256: `516025cbe42bd57a68a759d9caac6ee6d1d8f76357995b8aa0501af823b3b924`. File size: 58,780,011 bytes.

Inspected native midpoint frames for arrival, opening Arteta, chase, courier, foul, referee earpiece, header, wall, button press, VAR decision, final corner, celebration, reveal and meltdown. Inspected the encoded final at 3, 46, 101, 172, 193, 239, 262 and 272 seconds (`encoded-delivery-review.jpg`). The opening title, speaker labels, coach cameos, hand repairs, complete subtitle phrases, clarified league-table graphic and single reveal music caption are visible in their intended compositions. These are sampled visual checks; no new agent listening or exhaustive normal-speed review is claimed.

`samtoons-delivery-1080p.zip` contains the movie, SRT/ASS subtitles, selected soundtrack, four packed native source files, script, edit/source maps, checks, a SHA-256 manifest and this guide. The streaming render and finishing scripts remain under this video's `scripts/` folder in the Pencil workspace. Intermediate shot clips and diagnostic PNGs are retained in the local delivery folder but excluded from the portable package.
