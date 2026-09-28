# Bottle FC opening — audiovisual storyboard v002

[Opening review: 42.542 seconds](bottle-fc-opening-v002.mp4) · [Full revised edit: 4:08.083](arsenal-animatic-v002.mp4) · [Editable Blender timeline](arsenal-animatic-v002.blend)

Implements the user-approved script-v004 replacement: hidden narrator's “Same bottle”, recycled 2025/2026 banner, Bottle FC annual truck delivery, driver's dry apology, and urgent striker request. The excerpt includes Gyökeres' arrival, corner-flag reveal and reaction using the existing approved audio. The replacement itself lasts 24.542 seconds; all later shots move earlier by 155 frames at24fps. No other performances were regenerated.

Five new original caricature voice performances use the existing local Qwen model and documented acting directions. They are not authentic recordings or clones. VoiceDesign can vary timbre across generations; listener review of continuity and comic delivery remains necessary. The narrator's selected two-note motif returns; a restrained paper sound marks the year change, two reversing beeps announce the truck, and a phone click bridges toward the unveiling. No music bed is added merely to fill silence. The broader full-film score still needs development.

This is an illustrated held-pose storyboard, not finished body motion or lip-sync. Banner before/after drawings communicate the peel; the truck is introduced on a cut, not an animated vehicle entrance. New sheet panels have wider compositions and are letterboxed to retain their complete content without stretching or cutting off the information. These compositions can be rebuilt for final16:9 artwork. The accepted Bruno motion baseline and unresolved chase gait correction remain intact.

The yellow-shirted moustached driver is distinct from the purple medal courier. CP04's existing shot already shows that courier with a trolley of visible silver medals, so it remains usable as his first appearance; its voice and picture stay untouched. No runners-up medal appears in the new opening. Full-film picture order and pacing have not yet been approved.

## Evidence and reproduction

- `edit.json` and `subtitles.json`: revised full timing and text; `clips/`: only seven new opening exposures. Later picture references the preserved animatic-v001 clips.
- `audio-plan.json`: changed opening through the shared mixer. `full-audio-plan.json`: retimed complete source/event plan.
- `mix-premaster.wav`: new opening plus the original master from31seconds onward. A blockwise float32 comparison confirmed all10,730,000 later samples are identical.
- `checks.json`: full decode, exact5954frames, measured−23.08LUFS/−7.06dBTP. Numeric checks do not establish listening approval; agent listening was unavailable.
- `native-check.json`: saved native timeline reopens on the authored scene, contiguous56shots with no missing media.
- `image-provenance.json`: exact built-in imagegen prompt and reference; generated source copied into this project as `boards.png`. Sheet and encoded contact frames visually inspected for year text, truck label, identities and crop boundaries.
- Scripts in ../../scripts: `generate_opening_v002.py`, `build_opening_v002.py`, `assemble_opening_native_v002.py`, `package_opening_native_v002.py`, `check_opening_native_v002.py`. Native authoring used visible connected Blender and preserved previous scenes and files.

Keep this folder together with animatic-v001: native clips and approved sources reference it. New changes should use a new revision rather than overwrite review media.

## Credits and review

Inherited assets retain [full animatic credits](../animatic-v001/CREDITS.md), including Kevin MacLeod's chase music. Paper by Ezcah, Freesound248178, CC0, retained prepared source and attribution in audio plan. Reversing alert is original synthesis. New voice model provenance is in voices/model-source.json.

Pending user review: does the new opening land and flow into the corner-flag joke? Script approval and earlier audio approval remain recorded, but do not constitute acceptance of these newly performed lines or the revised combined edit.
