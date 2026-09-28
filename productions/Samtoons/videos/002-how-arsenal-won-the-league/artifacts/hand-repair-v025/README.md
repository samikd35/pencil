# v025 — hand reconstruction and cumulative clarity review

21 September 2026. **Review candidate, not user approved.**

- `hands-review-v025.mp4`: 13.208-second excerpt of the referee raise/earpiece, operator headset/phone/button and final corner signal, with the corresponding soundtrack and captions.
- `samtoons-complete-review-v025.mp4`: complete 720p, 24 fps film, approximately 4:36.4.
- `hand-repair-v025.blend`: editable 30-scene snapshot. The native scene names retain `clarity_v024`; the file is the v025 reconstruction.
- `../../script-v008.md`: actual revised dialogue and shot actions.

## Why the previous patches failed

The neutral source drawing had an open hand. Rotating its controls could not create a phone grip or an inward earpiece touch. The v024 substitutions then introduced crude rectangular wrist extensions and attached to controls while the fitted artwork deformed elsewhere. Extreme folded arm poses also distorted the original exposed forearm. Adjusting only the hand could not repair that entire chain. The user explicitly rejected those results, including their still-visible construction defects.

The v025 referee/operator repair replaces exposed arm artwork from the evaluated sleeve edges, using rounded upper-arm contours and a continuous forearm-to-hand drawing. Specific silhouettes serve the earpiece, pointing, relaxed hand, phone grip and button press. Sleeve-edge positions follow the existing fitted character. The phone's fingers sit behind it and its thumb overlaps the near edge. Original faces, clothes, body rigs, sets, soundtrack and scene durations remain in use. The first two accepted batches are reused as the existing encoded prefix.

During inspection, the first reconstructed raise still shortened the forearm. Its wrist now travels around the elbow by angle, rather than interpolating straight through the elbow. The finished interval measures 0.279–0.321 drawing units; the change is projected foreshortening, not a physical simulation. The button fingertip is within 1.41 pixels of the button top at the contact frame in the 720p camera. These are narrow checks, not proof of perfect acting.

Other new v024 hand substitutions on Arteta's phone/point and the trophy/grab/cheering gestures were redrawn using the same more legible contour approach while retaining their fitted joins and motion. This is scoped native vector geometry inside Blender, alongside the established fitted illustrated character meshes. It does **not** convert the entire cast to Grease Pencil or replace the characters with static pictures.

## Actual visual review

Agent inspected full rendered frames and the saved detail sheets:

- Referee raise: VH01 84, 86, 88, 90, 92, 94, 96. The first inspection caught forearm collapse; `VH01-contact-review.png` records the corrected interval.
- Referee point: VH05 198, 202, 206, 210, 214, plus full-body frame 225. `VH05-contact-review.png`.
- Operator button: 1, 3, 5, 7, 9, 11, 14, 18, 22, 26, 30. `VH04_button-contact-review.png`. Also checked headset frame 15 and phone-answer frame 35.
- Arteta phone frame 45, delivery direction frame 90, trophy frame 115, and the complete bodies around the replacements.
- The retained revised corner encode was sampled at frames 28, 29, 31, 36, 44, 54, 63, 64, 65, 72, 81, 85. `corner-flight-review.png` records the uninterrupted delivery/contact/goal path.

Not every frame was visually inspected. Full normal-speed performance judgement and listening remain user review; the agent does not claim to have listened to the soundtrack. Keep the new hand finish provisional until that review. Dense frame inspection and geometric checks do not establish benchmark-level creative acceptance.

## Story and sound carried into this review

The v024 clarity changes now accompany the hand revision: explicit City pursuit; adult-scale Pep; the second-place subscription; visible shirt-pull/fall; labelled VAR room and direct no-penalty/corner decision; clearer narrator hopes; a direct corner-to-backside winner without Gabriel reversing the ball; Etihad Pharmacy delivery; a corner-side celebration; and Ferguson's expanded meltdown in the same room. The later still-waiting referee callback is removed. The initial hold-menu setup remains.

The existing Qwen Base voice model and voice references remain intact. The new dialogue, score and foley mix are reused from `../clarity-v024/mix`, with the same speaker-labelled subtitles. Symlinks retain those selected assets and unchanged scene clips without duplicating them. Keep both version directories together.

## Reproduction and checks

`scripts/repair_hands_v025.py` records the visible-session authoring operations and `check_contacts()` checks the actual posed forearm and camera-space button contact. Authoring uses the live v024 scene/actor mapping; it is not a standalone rebuild from an empty scene. The saved native snapshot is the reproducible render input.

Render with `render_hand_repair_v025.py`, selecting changed scene IDs. Assemble with `package_hand_repair_v025.py`. The package validates all scene frame counts, full decode, 1280×720/24 fps video and 48 kHz stereo audio. `encode-checks.json`, `hand-checks.json` and `prefix-preservation.json` record the actual checks. Previous native revisions and accepted videos are preserved.
