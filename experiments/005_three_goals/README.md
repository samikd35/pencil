# Three Goals. One Heartbreak.

[Watch the film](artifacts/film-v001/three-goals-one-heartbreak.mp4) · [Editable Blender project](artifacts/film-v001/three-goals.blend)

30 seconds · 1080×1920 · 24 fps · 720 frames · no narration or dialogue.

The approved dramatic sequence follows Mbappé's three goals in the 2022 World Cup final, his successful shootout kick, Argentina's deciding penalty and the presentation. The intended contrast is repeated hope followed by stillness. The last line is **He gave everything.**

## Artwork and movement

This film introduces new original illustrated heads, hairstyles, facial features, skin shading, jerseys and shorts on simplified bodies. Mbappé, Messi, Thuram, Kolo Muani, Montiel, Martínez, Lloris and a supporting Argentina player have individual assets. Recognition uses several cues together: face/hair, kit, number, role and event context. Resemblance remains for the user's review.

The earlier C character is a source of editable motion controls, not a fixed visual design. Reused mechanisms include curves driven by hand/foot/elbow/knee controls, geometric contact measurement, native frame rendering and sound synthesis. The new jerseys required separate left/right shoulder anchors. All earlier films and their character project are preserved.

The film uses keyframed breathing/posture, changing eye and mouth shapes, kick anticipation and follow-through, an elevated volley, connected goalkeeper dives, net response, small contact accents, brief celebrations, a trophy lift and final head lowering. The camera pushes from the illuminated stadium into the opening face, revisits that composition before the third goal, and eases back at the ending. The stadium darkens after the winning kick and again behind the final close-up.

## Historical basis and compression

The [FIFA match report](https://fdp.fifa.org/assetspublic/ce44/r2864/pdf/FullTimeMatchReport-English.pdf) records the final at Lusail on 18 December 2022: Argentina 3–3 France after extra time; Argentina won the shootout 4–2. Mbappé scored at 80′, 81′ and 118′; Thuram assisted the volley. Messi's extra-time goal is recorded at 108′. Mbappé converted France's first shootout kick and Montiel scored Argentina's deciding kick.

The film visibly resets to a separate shootout score, first 0–0 and then 0–1 after Mbappé's kick. A clear edit advances to 3–2 before Montiel and 4–2 afterward. Four indicators per side show the deciding sequence. The shootout kick is separate from the hat-trick.

[FOX final coverage](https://www.foxsports.com/stories/soccer/a-scintillating-performance-kylian-mbappe-gave-his-all-in-world-cup-final) and the [Amiri Diwan presentation record](https://www.diwan.gov.qa/briefing-room/news/activities-and-occasions/2022/december/18/hh-the-amir-crowns-argentina-as-the-fifa-world-cup-qatar-2022-champions?sc_lang=en) informed appearance/context. France's kit in this match was navy, including shorts and socks. Argentina's outfield shirts are sky-blue/white with white shorts; Martínez is green and Lloris yellow. Messi wears a simplified black/gold presentation bisht for the lift.

This is an original stylized dramatization, not a traced highlight. Exact positions, camera setups, acting, gesture timing, stadium construction and condensed travel are illustrative. The final line is the user's approved dramatic interpretation. The opponent goal, trophy lift and separate closing view are time-compressed edits. No source footage or source audio appears.

## Sound and checks

The original soundtrack has instrumental music, designed stadium texture, synthesized breathing noise and 51 timed Foley cues. There is no dialogue, narrator, voice clone, authentic player breathing or broadcast recording. The score builds toward the equalizers, stops at the deciding kick, and ends unresolved. Separate music, Foley and atmosphere stems are retained in [audio](artifacts/film-v001/audio/).

[Saved-project checks](artifacts/film-v001/project-checks.json) evaluate all 720 frames for visible actors and valid limb drivers, six actual boot-to-ball contacts, nine score states, embedded audio and the unchanged source-character hash. [Build record](artifacts/film-v001/build-checks.json).

Visual review used 25 native sample frames and enlarged views of expressions, the volley and final pose. Revisions tightened emotional framing, corrected shoulder origins for the new jerseys, refined the facial silhouettes/expressions, and separated the shootout score. [Revised frame sheet](artifacts/film-v001/stills/review-revised.jpg).

The final export passed full-file decoding and format checks: 720 frames, 30.00 seconds, 1080×1920, 24 fps, stereo 48 kHz audio, −16.09 LUFS integrated loudness and −1.77 dBTP true peak. [Video checks](artifacts/film-v001/video-checks.json) · [Audio checks](artifacts/film-v001/audio/export-checks.json).

Final visual inspection covered 25 exported stills and 24 additional motion samples of the volley and ending. Thuram now clears the shot before the volley. The last decoded frame is black. [Exported frame sheet](artifacts/film-v001/stills/final-contact-sheet.jpg) · [Volley movement](artifacts/film-v001/stills/volley-motion.jpg) · [Ending movement](artifacts/film-v001/stills/ending-motion.jpg). Technical checks and sampled visual inspection do not establish audience comprehension, accurate perceived likeness, subjective sound quality or world-class quality. No full subjective listening review, audience test or publication has been performed.

## Reproduction and tracking

Use Blender 5.2.0 LTS for `scripts/build_film.py` (optional `-- --samples`), then Python with NumPy for `scripts/make_sound.py`, Blender for `scripts/verify_project.py` and `scripts/render_film.py`, and Python for `scripts/finish_delivery.py`. FFmpeg assembles and checks the final export. Rendering streams one temporary frame at a time to conserve disk space. The Blender file packs the fonts and soundtrack.

[Production events](events.jsonl) use the existing journal helper and hash actual outputs. No new framework, database or dependency was introduced. The user authorized this film and the new simplified player treatment; final creative acceptance remains with the user.
