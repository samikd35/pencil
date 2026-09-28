# S06 — football scene review candidate

13 seconds, 1280 × 720, 24 fps. [Review movie](football-review.mp4) · [Editable Blender scene](football-performance.blend). This is a scene-level staging candidate, not final film delivery or benchmark-parity approval.

Raphinha draws three practice defenders, points out the free player, Pedri passes through the opening, and Yamal receives, takes another touch and finishes. The camera establishes the marking, widens before the pass and follows the finish. The existing dimensional training set supplies the pitch, regulation-sized goal and background. The original S08 v006 files are preserved; its hand repairs remain deferred.

## Construction and sound

The existing 2D illustrated approach is retained. New player and fictional-defender references were generated with the built-in image tool and converted to native colored contours. Portraits, jersey details and boots retain those drawings; connected skeleton targets drive newly authored limb silhouettes, head/body controls, eyes, pointing and kicking. Contour motion is baked into editable native shape keys; playback has no Python handler. The saved skeleton and drawing keys are coordinated baked outputs, not a universal live rebinding system. Moving bones manually does not regenerate the baked contours; use the builder's joint schedule for coordinated revisions. This scope is specific to these views and actions.

Raphinha's line uses the installed local Qwen model. The cached kick and boot-contact sounds are reused with their provenance in production.json. Speaker-labelled subtitles cover the complete line. No voice model or previous voice asset was removed. These sound selections are candidates; subjective listening approval is not claimed. Net/counter details and the wider soundtrack remain part of the sound pass.

## Review and correction scope

Initial scene inspection exposed depth fighting between traced face colors, excessively bent resting legs and duplicated temporary defender identities. One coordinated construction pass increased contour depth spacing, revised the stance/weight transfer, fitted shorts to leg bends and supplied distinct fictional defender faces. An evaluated boot-mesh check then found that matching control targets still let the ball penetrate the drawn boots. Ball contacts now fit the actual visible geometry; reception approaches from the incoming-pass side. Target equality alone is no longer used as the contact check.

The [construction check](construction-check.json) measures the four evaluated boot-to-ball contacts, Yamal's planted support through the strike and goal crossing. It does not certify appeal, every in-between surface or arbitrary future motions. Frame review concentrates on pass 119–127, reception 148–154 and plant/strike/flight 188–220. See [the inspection record](inspection.json) and [focused contact crops](contact-review.png). The full export decodes without errors. Normal-speed subjective timing and sound acceptance remain pending; still frames do not establish them.

Minor contour simplifications, limited face/view range, restrained secondary acting and detailed environmental lighting remain staging limitations. Full head turn coverage, universal rig behavior and world-class quality are not claimed. Keep further refinements consolidated; next planned production work is S07 Flick/assistant acting.

## Ownership and reproduction

- Environment source: ../training-set-v001/training-set.blend, appended without overwriting it.
- Reference/contour source: ../../../assets/football-v001/ and ../../../scripts/trace_football_v001.py.
- Scene builder: ../../../scripts/build_football_v001.py. In visible Blender load the module, call setup(); create_actor() for Raphinha, Pedri, Yamal and three Defender actors using the matching source names; distinct_defenders(); animate_actor() for each; shorts_follow() for the three players; fit_visible_contacts(); animate_scene(); captions(); check_save(). Do not overwrite a delivered revision.
- Renderer: ../../../scripts/render_football_v001.py, run in background Blender against this exact saved scene. It encodes the complete 312-frame scene, saves selected weak frames and extracts S06 from the shared pipeline audio mix.
- audio/ contains the authoritative current pipeline mix and cue resolution. render-inputs.json records the original export inputs. render-selection.json preserves the exact selection used for the export. A subsequent viewport-only visibility correction is recorded separately in inspection.json; render comparison checks that the reviewed picture is unchanged.

The preliminary movie named before-contact-* is internal failure evidence, not the selected review.
