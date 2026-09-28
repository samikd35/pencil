# Color, lighting and sound finish

[Watch with sound](artifacts/finish-v002/preview-with-sound.mp4) · [Editable project with audio](artifacts/finish-v002/editable-project-with-audio.zip) · [Blender file](artifacts/finish-v002/character-and-effects.blend)

The user requested effects using available tools without supplying audio. This pass adds a warm background, teal box, coral shoes, navy ink, an illustrated spotlight, soft contact shadows, a box-edge highlight and a brief golden electric accent.

There are 19 timed sound cues: footsteps, contact taps, creaks, scraping, a whoosh, electric fizz and nonverbal effort/gasp/hum-like tones. All sounds were generated locally from oscillators, filtered noise and harmonic formants. No voice recordings, voice clone, speech model, downloaded samples or music were used. The character sounds are intentionally synthetic cartoon cues, not natural human speech.

## Tools and editable layers

- **Blender 5.2:** existing motion loaded unchanged; colors assigned through materials; procedural backdrop and transparent soft shadows; native curve sparks with compositor glow. Lighting is illustrated shading suitable for the flat emission artwork, not a physically lit 3D character.
- **NumPy and Python WAV output:** reproducible sound generation with a fixed random seed and a timed cue list. Separate footsteps, Foley, character and electric stems are saved.
- **FFmpeg:** level normalization and a final H.264/AAC video. The normalized mix is also referenced by a sound strip in the Blender project.

## Verification and review

The saved finish preserves **all 240 frames of all 44 original objects**: world transforms, mesh vertices, evaluated curve points and handles match v005 exactly. Colors intentionally change the rendered pixels. Sparks are confined to frames 129–145. The audio file resolves through a relative path beside the `.blend`. [Verification](artifacts/finish-v002/verified-finish.json).

The export contains 240 video frames, 1280×720 at 24 fps, plus 48 kHz stereo AAC, for exactly 10 seconds. Measured exported audio is approximately **−16.07 LUFS integrated and −1.49 dBTP true peak**. [Video metadata](artifacts/finish-v002/verified-video.json) · [Audio measurement](artifacts/finish-v002/audio/final-audio-check.json).

Inspected full-size sample renders and the chronological contact sheet. Palette and character silhouettes remain consistent; the spotlight and shadows add depth while the electric accent remains small. Signal timing, duration and audio levels were checked; subjective sound quality and the preferred effect intensity remain for playback review. This is a finished effects experiment, not a claim of final production-quality acceptance.

The first finish attempt remains archived: its spark highlights washed toward white, and Blender remapped the audio link to the previous project folder. The corrected version uses a saturated spark color and a size envelope, with the intended relative audio path preserved on save.

## Reproduction records

Visual settings and cues: `finish-v002.json`. Original audio generation: `scripts/sound_finish_v001.py` with `finish-v001.json` (the cue list is unchanged in v002). Visual finish: `scripts/finish_v002.py`. Export: `scripts/encode_finish_v002.sh`. Motion/dependency check: `scripts/verify_finish_v002.py`. All source hashes, outputs and failed attempts are recorded in `events.jsonl`.

The ZIP contains the editable project and its audio files; extract them together. The experiment folder retains the full source, cue data, measurements, rendered-frame hashes and reviews. The next independent-action reuse test remains unstarted.
