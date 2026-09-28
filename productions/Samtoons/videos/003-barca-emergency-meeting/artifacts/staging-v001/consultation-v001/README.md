# S09 — Ask the former employee

16-second staging candidate, not final film acceptance. The selected script is unchanged. Müller invites Robert into the remote call; Pérez asks his question; Robert places his cup on the desk, corrects the premise and glances toward his old Bayern memento.

## Construction and acting

Existing Müller/Pérez native contours and connected construction are reused with new seated acting; their old shot animation is not copied. Robert has a new generated caricature construction reference, converted into native colored contours with separate facial controls and a rigid cup. The first reference was rejected for an awkward wrist/cup relationship. Its corrected version establishes both forearms and the cup at a common desk height before animation.

The cup is lifted only 30 source pixels from that supported pose and lowered to the desk before Robert speaks; the connected drawing moves with it. The other arm remains supported. This is a bounded seated action, not a universal deformation rig or a solution for extreme reaches. No S07 standing, knee or squat motions are reused. The call is framed in three distinct remote spaces, followed by a held closer view on Robert's correction.

## Sound

New lines use the existing local Qwen runtime. Müller and Pérez are conditioned on their earlier generated character voice references; those source WAVs are preserved. Robert receives an original directed cartoon voice, not a clone of a real person's recording. All new takes remain candidates pending listening. The small contact tap reuses a project-generated sound from video002. Shared pipeline audio assembles the mix; speech is neither sped up nor cut off.

## Known evidence limits

The user rejected S07 v003's balance, knee and arm/clipboard mechanics. Those defects remain unresolved; moving to S09 is not approval. Technical lengths and planted feet were insufficient tests. S09 instead starts from a complete supported drawing and checks the actual hand/cup/desk relationship through set-down. Static images cannot certify normal-speed motion or listening quality.

Builder: `scripts/build_consultation_v001.py`. Construction preparation: `scripts/trace_lewandowski_v001.py`. Visible Blender batches: setup → callers → robert → animate → finish. Rendering uses the existing `render_staging_scene.py` with S09, S003_S09_Consultation_v001, consultation. The shared audio plan and selected assets are frozen in the output evidence.

## Delivery evidence

The encoded preview fully decodes: 384 frames, 1280×720, 24fps, 16.0 seconds, 48kHz stereo. Complete dialogue intervals are 1.00–4.28, 5.00–8.44 and 10.00–14.32 seconds. The cup contact is at frame222; speaking starts at241.

Inspected the native approach/contact frames208,214,218,222, then final encoded entry, join, cut, reply and end frames. Corrected the close-up head crop and Pérez’s eyeline before rendering. The cup and grip stay together through the small set-down, with the opposite hand retained at the desk. Mouth articulation and the small skin transition around the lips remain approximate; existing call-hand limits remain. No listening or benchmark-quality acceptance is claimed. `inspection.json` records the encoded checks and `cup-contact-review.jpg` the detailed contact inspection.

Artwork used the built-in image-generation tool. Selected source and exact prompts are in `assets/lewandowski-v001/reference-supported.png` and `assets/lewandowski-v001/prompts.md`; provenance includes the rejected initial pose.
