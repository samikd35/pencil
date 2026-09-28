# Gyökeres chase excerpt v002 — pending review

[Eight-second picture review](chase-v002.mp4) · [Editable Blender scene](chase-v002.blend)

Adaptation of the accepted `pose-action-v003` method to CP02/CP03 of locked script v003. First five seconds: Gabriel, Saliba and Gyökeres carry the 1st podium, Arteta runs ahead. Final three seconds: cut to Pep's slower hands-in-pockets walk. Gyökeres retains the accepted swept-back blond hair, stubble, Arsenal shirt, number14, red socks and cream/red boots, in newly derived full-character action drawings. These new likenesses and movements remain subject to review.

## Scope

This is a silent picture-and-motion excerpt, not the whole City chase or full-film animatic. It tests loaded running and the sprint/stroll contrast. The City-win gap-closing gag, full wide comparison, dialogue, additional runners, courier and sound remain outside this excerpt. The script is unchanged. [Shot plan and sound intention](../../assets/chase-poses-v001/plan.md).

## Construction

Complete character drawings are mapped to connected native mesh surfaces. Each actor has a keyed `pose_index`, active-shot switch and world travel. Camera motion follows an independently authored path. Limited `Support X` and `Support Z` shape keys maintain feet against the road without moving the head or torso independently. Carriers register to their raised palms; the podium is a separate native editable object with its own label. It is a fixed-view drawing-substitution method; new views or markedly different silhouettes require drawings.

Gyökeres uses eight drawings; each supporting actor uses four. Carriers/Arteta travel at 4.2 world units/s; Pep's cutaway travels at 1.35, with a slower stride cadence. The hard cut is frame121. Each full body stays inside frame. The separate shots preserve different actual travel speeds rather than making Pep glide at the runners' speed.

## Actual checks

[Native checks](checks.json) cover all192 frames, one active drawing per actor, full-body framing, frame-to-frame horizontal registration and evaluated support correction. Horizontal registration movement is below0.001 pixel within each shot; support error below0.000001 world unit. These measurements certify those properties, not likeness, naturalness or humor. Critical full-size frames and consecutive rendered action frames are inspected; final normal-speed playback review belongs to the user.

The initial internal assembly v001 exposed a coupled X/Z shape delta; the builder now explicitly derives both corrections from Basis. The evaluated-geometry check caught it before movie rendering. Initial Pep passing drawings read as marching and were replaced with low-foot passing poses; the road edge was aligned to the support plane. Earlier sheets and v001 native scene are retained as iteration evidence.

## Edit and reproduce

Open scene `S002_CP_chase_v002`. Named `CP / <actor> travel` controls expose `pose_index`; pose meshes expose support corrections. Camera, podium, road, markers and text remain native. Packed images allow opening the file without external art paths.

Visible Blender authoring uses `scripts/build_chase_v001.py` with `CHASE_VERSION='v002'` in its execution namespace (requires an unused output version directory). This intentionally refuses overwriting review versions. Background rendering and verification:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b productions/Samtoons/videos/002-how-arsenal-won-the-league/artifacts/chase-v002/chase-v002.blend --python productions/Samtoons/videos/002-how-arsenal-won-the-league/scripts/render_chase_v001.py -- v002
/Applications/Blender.app/Contents/MacOS/Blender -b productions/Samtoons/videos/002-how-arsenal-won-the-league/artifacts/chase-v002/chase-v002.blend --python productions/Samtoons/videos/002-how-arsenal-won-the-league/scripts/check_chase_v001.py -- v002
```

Selected asset hashes and unchanged script hash: [provenance](provenance.json). [Generation prompts](../../assets/chase-poses-v001/prompts.md) and [Pep correction](../../assets/chase-poses-v001/pep-correction.md) retain the image-generation inputs. Selected manager sheet for v002 is `managers-low.png`. Original Bruno proof and video001 delivery were not modified.

Review: Does Gyökeres's appearance and loaded running preserve the quality of the accepted Bruno test? Approval would permit extending this construction to the remaining required actions; it does not approve unheard sound or the unassembled full movie.

## User review — supersedes pending status

Below Bruno-v003 quality, particularly Pep's walk and the running. User directed that this excerpt not be re-rendered now; improve the movements during full-video production. Keep this as rejected-quality evidence, not a motion template approved for replication. Bruno v003 remains the quality baseline. Advancement past this local proof is explicitly permitted; whole-film sound, animatic and delivery acceptance are not implied.
