# REJECTED — static-pose assembly v004

User rejected this on 18 September 2026: it behaves as connected images, not the requested animation. The 34 shots are not completed animation and are not a reusable motion baseline. Preserve the file as failed evidence.


This version adds 34 acting/prop shots (138 seconds) to the complete 4:08 edit. CP01 and CP03_pep retain their exact user-approved movie inputs. The other 20 shots still use the previous staging clips; they have **not** been promoted to completed animation. `checks.json` lists the exact coverage after assembly.

New editable scenes cover Bottle FC, striker unveiling/reactions, the VAR exchange, and the concealed narrator/reveal/meltdown. The production now advances in batches; no individual movement approval loop has been reopened.

## Construction carried forward

- Complete, clothed character drawings retain their own heads, anatomy, kits and shoes. New views/actions use distinct matching drawings, not head swaps or primitive replacement bodies.
- Pose selection, anatomical registration, world travel and camera animation are separate. Selectors have bounds matching every actual drawing.
- Connected-component label textures isolate each drawing; rectangular crops alone can leak neighbouring boots/hands when sheet rows overlap. These native masks preserve the original artwork.
- Speech uses the selected voice take's measured amplitude to time bounded mouth closure and small acting accents. This is an initial performance pass, **not** completed phoneme animation.
- Native editable props carry the paper peel, truck reversal, notifications, hotline/button, confetti and final paper flight. Cameras hold except for authored reveals/reframing.

## Remaining production work

1. Football action: planted kick, cross/header, nine-player defensive wall with Raya in front and Gyökeres upfield, final missed header/backside deflection/goal. Prepared assets include a specific ground-contact Saka drawing; support and ball paths still need authoring and review.
2. Remaining chase coverage: phone-to-road transition, Pep distance change, panic, courier movement and podium slip/catch. Use accepted CP01/Pep motion as the floor; do not replace them with the old rejected proof.
3. Performance polish: gaze/eyelines, richer mouth and transition drawings, matched hand/prop contacts and timing across cuts. Current drawings/holds are first-pass acting, not final benchmark acceptance.
4. Complete music coverage and final effect synchronization/listening. The approved mix and captions are retained unchanged in this progress cut. No selected dialogue take was regenerated.

Technical verification checks frame counts, 24 fps, complete decode, native timeline dependencies and preservation of accepted clips. Sample renders were visually inspected; this does not substitute for normal-speed human viewing or actual audio listening. No new creative approval has been recorded.

Build: `scripts/build_film_animation_v004.py` → render: `scripts/render_film_batch_v004.py` → assemble: `scripts/package_film_batch_v004.py` / `scripts/package_film_native_v004.py`.
