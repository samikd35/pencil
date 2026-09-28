# Corner-flag unveiling — visual proposal v001

Samtoons video 002 · TR02 · 16:9 · 17 September 2026

**Review the appearance of Arteta and Gyökeres in this scene.** The approved joke, dialogue and camera sequence are unchanged. This is the first character-design proposal for these two people in this video; it is not final animation.

![Unveiling scene](unveiling-wide.png)

Gyökeres: “Then why am I here?”

Arteta: “Win us a corner.”

![Closer view of the expressions](unveiling-reaction.png)

Gyökeres has an angular face, swept-back hair, broad shoulders and an offended palms-up pose. Arteta has compact dark hair, pronounced eyebrows and an utterly sincere presenting gesture. Their faces are proposed caricatures, not approved likenesses. The close view concentrates on their expressions; Arteta's presenting hand continues toward the offscreen flag.

## Relation to Samtoons

The retained direction is recognizable cartoon faces, clean dark contours, restrained cel shading and simple connected bodies. This uses the existing Samtoons treatment as a style reference, without importing its Manchester cast. The stadium, carpet, flag and shirt are native Blender artwork. The background is intentionally simpler than the characters; richer perspective and final environment detail remain later work.

![Existing Samtoons treatment reference](reference-samtoons.png)

Reference source: `productions/Samtoons/videos/001-manchester-derby-2026-09-13/assets/treatment-v001/A-clean-caricature.png`, copied here as a reference, not a movie layer. The current video's adopted profile and benchmark v002 remain authoritative. Benchmark B's purposeful reveal informs the flag presentation and reaction coverage; benchmark A's changing recurring gag connects this flag to later corners. No source audio was auditioned for this pass.

## Files and actual checks

- [Native scene](unveiling-treatment-v001.blend): separately positioned character planes, editable stadium/prop artwork, wide and reaction cameras; source character image packed into the file.
- [Character artwork](gyokeres-arteta.png): generated with the built-in image tool, using the existing Samtoons treatment as a style reference. [Exact prompt](image-prompt.txt). No photo was used as an input; exact likeness is for review.
- [Scene builder](../../scripts/build_treatment_v001.py): reuses the video's existing shape helpers and the established emission/alpha material method. Current Blender default materials required explicit emission nodes; this was corrected before these exports.

Both rendered views were visually inspected. The wide shows two separated characters, Arteta's gesture toward the number-nine flag, the carpet and fully visible boots. The closer view exposes facial details for review. Ground shadows were flattened after inspection. The saved native file was reopened in a separate Blender process: packed artwork, independent character placement and 1920×1080 settings were verified without changing the saved file.

**Limit:** the character poses are raster artwork on separate planes, not editable joint/face rigs. There is no verified turning, lip sync or body motion yet. Appearance acceptance would retain these designs for subsequent construction; it would not approve the remaining cast, animation, audio or complete film staging. Ferguson's concealment and eventual design remain separate work.

The earlier rough defensive-framing question was withdrawn after the user's clarification. It is not a prerequisite for continuing, and no approval of those placeholder drawings is inferred.
