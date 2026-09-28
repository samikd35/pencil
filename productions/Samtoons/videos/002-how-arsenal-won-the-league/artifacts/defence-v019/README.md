> Superseded following user rejection: new players read as static images. See v020 for the scoped construction/performance revision. Earlier technical/still checks below do not establish acceptance.

# Second chronological review batch — v019

This continues the user-approved v018 opening/training cut. The user's label “2nd Batch” means the next story section; older internal records split the opening into smaller batches.

43.625 seconds / 1,047 frames, 1280×720, 24 fps. Combined opening through this section: 1,669 + 1,047 = 2,716 frames, approximately 1:53.

## Story and preserved selections

Corner delivery → Gabriel's header → Arteta orders everybody back → nine outfield players form a wall, Raya stands in front → isolated Gyökeres asks his role → “Win another corner!” → concealed narrator crushes notes in the same room → confident Arteta → City notification / “Again?”

The selected Arteta and Gyökeres complete drawings and native joint rigs are reused. Narrator audio is reused. New Arteta and Gyökeres lines are conditioned on their selected original voice references. All active voice models remain installed. The narrator remains anonymous in captions. These are illustrated meshes deformed by native rigs; they are not native Grease Pencil drawings.

## Native construction and motion

- `batch02-v019.blend`: editable match and narrator scenes. `cast.json` records controls and rest coordinates for subsequent work.
- One 105×68 m pitch, both 7.32×2.44 m dimensional goals, flags at the four corners; attack and defensive-wall shots use opposite ends. The same shared narrator-room collection is retained.
- Source-fitted whole-character rigs retain clothing and head/body coherence. Nine wall players, Raya and the isolated Gyökeres establish Arsenal's eleven. Nine faces remain visible in the closer wall composition.
- Saka's source has crossing limb regions. Initial x-side weight assignment deformed the support boot. Nearest anatomical segments and a bounded ankle path correct this specific rig; large folded poses still exceed this single drawing's useful range. Do not promote it as a general running rig.
- Wall root travel is broken into alternating short steps. The initial whole-distance step produced splits and was rejected. Final maximum root/foot lateral offset is 0.182 m.
- Gabriel's 0.42 m jump lasts 15 airborne frames (0.625 s; equivalent ballistic gravity 8.60 m/s²), with anticipation, contact and compression. Saka gives a native arm signal before the kick; the source-specific sleeve influence is constrained so it does not drag his shirt hem. The initial 27-frame flight was too floaty and was shortened without stretching dialogue.
- The phone elbow pole is below the shoulder/wrist. An earlier wrong bend-plane pose was rejected. Source shading/gloves are preserved in the opponent keeper's fabric recolour.

## Actual review and limits

Native rendered frames inspected: Saka's ready stance, preparation and contact (1, 151, 154, 157, 160, 164, 168); Gabriel before/at/after the header (208, 216, 217, 225); Arteta speech/command (285, 322); wall assembly and settled formation (430, 490, 540); Gyökeres speaking (724, 740); phone reaction (1008); narrator paper (26). Successive contact frames are retained in `review-frames` for the encoded motion check. Earlier rejected checks remain distinguishable by filename; they are not selected artwork.

This is a review candidate. Still-frame and contact checks do not establish full motion quality or comic timing. Agent listening has not been performed; voice performance, music fit and the combined scene's clarity remain for user playback review. Whisper transcription supplied word timing only: hallucinated duplicate words during tails were not treated as script changes or proof of audible defects. Lip timing uses the actual take envelope and word cues; it is not phoneme-perfect.

## Reproduction

The saved native project is the authoritative current animation. Render it with `scripts/render_defence_v019.py` using Blender in background mode. The renderer streams PNGs to FFmpeg, retains selected review frames, and validates existing clip frame counts before reuse. Run `scripts/package_defence_v019.py` to burn the speaker captions, finish the existing premaster and assemble the cumulative review. `edit.json`, `audio-plan.json`, `subtitles.ass` and `subtitles.srt` are editable timing/caption sources. `mix/` contains the premaster, separate stems and resolved events.

Authored revision scripts (`build_defence_v019.py`, `refine_defence_v019.py`, `finish_defence_v019.py`, `contact_pass_v019.py`) were applied to the live selected v018 session. They require that session's existing helper registries; the saved project and standalone render/package scripts do not.

Encoded consecutive-frame inspections: kick 166–171, header 215–220, wall shuffle 430–435. Contact sheets were extracted from the actual MP4 clips, not source artwork. Caption composition was inspected on the encoded wall and City-phone frames. These sampling checks do not claim every frame was visually inspected or that sound was heard.
