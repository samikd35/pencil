# Animation progress v003

[Current full progress movie](arsenal-progress-v003.mp4) · [Editable timeline](arsenal-progress-v003.blend) · [Nine-second CP01 pass with approved sound](../animation-v002/CP01/CP01-v002-with-audio.mp4) · [Editable CP01 scene](../animation-v002/CP01/CP01-v002.blend)

Two shots now have body animation: CP01 is a candidate; CP03_pep retains the user's explicit approval. The remaining 54 shots are still the accepted storyboard. This is not the finished film. CP01's phone-to-road transition, supporting runners, final facial acting and the remaining chase interactions are unfinished. No new checkpoint has been inserted in place of the user's earlier scoped chase waiver.

## Construction and review

Adapted the accepted Bruno run's complete pose sequence to Gabriel, Saliba, Gyökeres and Arteta. Whole drawings retain their own faces, clothes and shoes. Each has eight drawings held for two frames, independent continuous travel, explicit source registrations and bounded connected lower-body support corrections. Carrier support phases are offset under one nearly level podium; palms sit beneath its front edge. The camera follows the authored travel, never the changing silhouette centre. This preserves the established method without treating a textured drawing as an all-purpose skeletal rig.

The built-in image-generation prompts and sources are in `../../assets/chase-poses-v004/provenance.json`. Initial Gabriel art inherited the wrong sock/boot colours; the selected correction restores Arsenal colours. The initial Saliba sheet lost shirt lettering and clipped a boot; its correction is selected. The user's concern about repetitive generation was acknowledged. No further drawings were generated after that discussion; the already-running Saliba correction was collected. Future replacements should address a concrete observed shot defect, not repeat unconstrained requests for better animation.

Inspected the full source sheets, first 16 consecutive encoded frames, and ending frame. The initial render revealed Arteta's rear shoe touching Gyökeres's forward boot. Version 2 moves Arteta forward 0.35 scene units while retaining the entire gait and soundtrack. The corrected ending has clear separation. Earlier versions are preserved under animation-v002 and superseded by this progress edit.

All 216 frames were checked for evaluated pose selection, a single active drawing, actual mesh support deformation, constant horizontal registration relative to the independently authored camera, and full pose framing. The source contact locations are manually inspected points, not automatic proof of anatomy. These checks cannot certify leg-role interpretation, natural timing, expression, comedy or listening quality. Agent normal-speed playback and listening were unavailable; no subjective approval is invented. Bruno remains the accepted quality floor, and only Pep has subsequent user motion approval.

## Sound and deliverables

The preview uses the exact approved CP01 master interval, 98.6667–107.6667 seconds. No voice or music was regenerated. Full progress retains the original 5954 frames at 24 fps and approved soundtrack; both encoded movies decode successfully. The native timeline retains all 56 picture strips and the exact accepted Pep clip. All picture dependencies exist. Music credits remain in `../animatic-v001/CREDITS.md`.

The initial scene and timeline were authored additively through connected Blender, with the user's existing unsaved scene restored. Rendering, native startup packaging and the isolated spacing correction used saved scenes in a separate process; these changes were not presented as live edits. Existing films and accepted assets were not overwritten.

Reproduction: `build_loaded_run_v001.py`, `render_loaded_run_v001.py`, `separate_loaded_run_v002.py`, `render_loaded_run_v002.py`, `check_loaded_run_v002.py`, `package_animation_progress_v003.py`, `package_animation_native_v003.py` under the video's scripts directory. Versioned scripts intentionally refuse to overwrite outputs. CP01 evaluated checks live in `../animation-v002/CP01/evaluated-checks-v002.json`; this directory contains full-edit technical checks.

Next work: phone-to-road introduction, chase distance gag, panic/courier coverage and podium slip/catch; then the remaining action and acting shots. Preserve accepted Pep and voice takes. New interacting actions need their own contact/pose decisions, not blind reuse of this run cycle.
