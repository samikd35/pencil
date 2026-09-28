# Just Five Minutes

30-second reference-replication test using the user-endorsed [visual script](script-v002.md). The user explicitly requested the supplied video's characters and environment, then authorized production with “start.”

[Watch the 30-second film](artifacts/film-v001/just-five-minutes.mp4) · [Editable Blender project](artifacts/film-v001/just-five-minutes.blend) · [Source/reconstruction character comparison](artifacts/film-v001/stills/character-comparison.png)

## Visual construction

The source is the user-supplied `/Users/samikd/Downloads/Meesha Final.mp4`. Extracted [front](references/front.png), [cast](references/cast.png), and [desk](references/desk.png) frames informed the drawings. The main character's hair, tapered face, paired eyes, nose, smiling mouth, shirt and shorts were reconstructed against the early reference design. A curly-haired friend, ruled white paper, grey/orange desk, monitor, wired mouse and black office chair reproduce the reference's visual vocabulary.

All delivered artwork and movement are editable Blender objects. The source frames are reference evidence, not footage inserted into the new film. The story is original fictional comedy, independent of football or educational topic selection.

The existing Pencil flat-drawing and keyframe helpers are reused from experiment 003. The Heavy Box delivery remains unchanged, checked by SHA-256. This test uses newly reconstructed flat geometry rather than carrying the old character's silhouette into the reference design. The native Blender/FFmpeg render, audio synthesis and delivery mechanisms come from the prior experiments; no dependency or pipeline framework was added.

Animation combines held body poses, blinks and facial replacements, brief gestures, a foreground character entrance, phone pickup and release, scrolling-thumb motion, accelerated clock hands, captions, a face close-up, and a shrinking retreat with a drawn dust puff. The final shot holds the untouched computer and opening claim. The retreat uses a cut to clear space left of the desk so the character does not appear to run across the tabletop.

## Checks and review

[Saved-project checks](artifacts/film-v001/project-checks.json) cover 900 frames at 30 fps and 1920×1080, 591 held-phone frames, face/back-view visibility, the final desk, packed audio, and the unchanged Heavy Box source. The maximum measured hand/phone anchor separation in the saved project is approximately 0.000123 pixels.

Native still review covered 12 points across the story. A 30-frame overview of the first picture master checked story timing; a source/reconstruction head comparison led to stronger contours and a corrected eye/nose junction. Earlier internal failures included helper initialization, visibility keys overwriting previous poses, and depth ordering of white limb interiors. These were corrected before delivery. Caption overlap, seated layout and retreat placement were also corrected. The earlier picture master is retained in `artifacts/layout-v001/`.

This is an editable visual reconstruction, not a pixel-identical copy. New seated and gesture poses are authored for this script, and installed lettering fonts approximate the reference's lettering. Visual resemblance and comic effectiveness remain for user assessment. Geometric and format checks do not establish those judgments.

The final MP4 passed full-file decoding and format checks: exactly 900 frames, 30.00 seconds, 1920×1080, 30 fps, and stereo 48 kHz audio. Measured integrated loudness is −17.34 LUFS and true peak is −2.00 dBTP. See [video checks](artifacts/film-v001/video-checks.json) and [audio checks](artifacts/film-v001/audio/export-checks.json). Final visual inspection covered the [30-frame exported overview](artifacts/film-v001/stills/final-contact-sheet.jpg), plus 16 successive samples each of the [phone pickup](artifacts/film-v001/stills/pickup-motion.jpg) and [retreat](artifacts/film-v001/stills/retreat-motion.jpg). These are sampled frame inspections, not an audience test.

## Sound

Original synthesized Foley includes the phone buzz, taps, swishes, clock ticks, chair creak, footsteps and puff, plus a sparse instrumental scrolling loop. There is no voiceover, dialogue or source-video audio. Separate [Foley](artifacts/film-v001/audio/foley.wav), [music](artifacts/film-v001/audio/music.wav), and [cue record](artifacts/film-v001/audio/sound-design.json) are retained. Audio receives numerical loudness/peak verification; a subjective listening review has not been performed.

## Reproduction

From the Pencil project root, use Blender 5.2.0 LTS for `scripts/build_film.py` (optional `-- --samples`), its bundled Python/NumPy for `scripts/make_sound.py`, Blender for `scripts/verify_project.py` and `scripts/render_film.py`, then Python for `scripts/finish_delivery.py`. Scripts are relative to this experiment. Fonts and soundtrack are packed into the Blender file. FFmpeg streams rendered frames into the picture master without retaining 900 temporary PNGs.

[Production journal](events.jsonl) records the actual work and completed export verification with the existing journal helper. The film is ready for the user's visual assessment.
