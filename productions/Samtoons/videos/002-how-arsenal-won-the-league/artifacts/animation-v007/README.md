# Ferguson native reconstruction v007

**Movement improvement acknowledged by the user; artwork is still below the video 001 baseline. Not a final character or an approved ending.**

The seven-second `ferguson-native-dialogue-v007.mp4` uses the selected meltdown mix. The character is native flat mesh/curve artwork in `ferguson-native-v007.blend`, with separate pelvis, chest, head, upper-arm, forearm, wrist, finger, leg, boot, eye, gaze, eyebrow and mouth controls. No character material contains an image texture. The same existing room collection supplies the environment. Earlier scenes and rejected revisions remain preserved.

Construction reuses video 001's inspected `build_staging.py` flat-art primitives. The new film-specific script authors Ferguson's contours and clothing around articulated controls. Distinct closed/open/wide/rounded/lip-teeth/tongue drawings supply facial articulation; the whole head is not replaced. Local Whisper analysis recovered the exact selected words and approximate word timestamps. Viseme placement within words is manually assigned and remains a draft, not forced phoneme alignment or listening approval. The voice itself was not regenerated. The assistant has not heard the mix.

The body blocking supplies separate preparations, assertion, breath, stop gesture, appeal and recovery. A per-frame two-bone solve retains planted boot controls while the pelvis moves. The render check verifies native character materials, shared set identity, one visible mouth per frame and support stability. These are construction checks, not a creative-quality certificate.

## Comparison requested by the user

The user said movement has improved a lot, then asked to compare body construction with video 001. The comparison used delivery-v001/frame-01-154.png and the current rendered Ferguson frames. Video 001 has more organic arm taper, hand anatomy, integrated clothing folds and richer coherent character drawing. v007 has more geometric sleeves, flat shading, overly uniform fingers and a more generic face. The current camera obscures the legs and shoes, so that shot cannot establish their visual quality. Native construction is not a reason to accept this drawing regression.

Retain the improved control/motion work. The next revision must improve the character contours, hands, clothing and likeness around those controls while preserving their movement. Do not promote the current artwork across the film, replace the rig with a warped picture, or assume user approval of likeness from the positive movement feedback.

## Evidence and reproduction

- `native-checks.json`: support/material/exposure checks.
- `dialogue-timing.json`: word intervals and authored mouth changes.
- `speech-analysis.json`: local ASR output; empty segments are model output, not extra dialogue.
- `frames/`: selected rendered frames; these do not replace normal-speed review.
- `dialogue-first-pass.mp4`: internal first pass retained; the current revision narrows the angry eyelids and corrects the sideways stop palm.

In an interactive Blender copy containing the v005 shared room, execute the definitions in `../../scripts/build_ferguson_native_v007.py`, then call `setup()`, `body()`, `face()`, `block()`, `hand_shapes()`, `bake_support()`, `refine_art()`, `speech()`, `anger_and_stop()`, and `save()` in visible batches. Do not rerun additive construction in a scene that already contains v007. The saved native project is directly editable without the builder. Render/check with `../../scripts/render_ferguson_native_v007.py` against the saved revision.
