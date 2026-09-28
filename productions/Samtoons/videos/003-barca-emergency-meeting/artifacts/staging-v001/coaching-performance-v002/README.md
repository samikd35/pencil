# S07 — continuous clothing revision, staging candidate

15 seconds, 1280 × 720, 24 fps. [Review movie](coaching-review.mp4) · [Native scene](coaching-performance.blend). This remains a staging candidate, not final film delivery or a benchmark-quality approval.

The assistant asks for a slower pace; Flick answers, checks his watch, puts the clipboard down and rolls another ball into play. The established two-shot, reply close-up, assistant reaction and action wide are retained. All three spoken lines remain complete, with speaker-labelled subtitles. Sound candidates have not been subjectively auditioned by the agent.

The user rejected v001's bent standing legs and discontinuous shoulder/hip connections. Joint positions alone were insufficient: independently outlined sleeve strips and a separate pelvis cap still produced detached-looking clothing. This revision computes one connected torso/sleeve silhouette and one connected trouser silhouette per actor per frame, with explicit collar-to-shoulder transitions, rounded elbows and forearm overlap. Interior reference artwork, faces, eye/mouth animation, props and the selected timing are retained. Rest proportions are calibrated to the planted stance. Bending for the ball remains intentional.

These are native vector drawings at 24 frames per second, baked from the existing authored motion. Shapely 2.1.2 performs offline polygon unions; the saved scene requires no Python playback handler or Shapely installation. The user explicitly prioritized screen performance over convenient manual rig editing. This is an implementation for these poses, not proof of unrestricted future articulation. Simplified hand drawings, limited head turns, lip shapes, shoulder volume/secondary acting and scenic finish remain below the target benchmark.

## Reproduction and evidence

Start with the documented v001 builder in visible Blender. Load `scripts/revise_coaching_surfaces_v002.py`; call `prepare(s07_module)`, `bake('Flick')`, `bake('Assistant')`, and `save()`. The revision uses the existing motion; it does not reset the production to a new experiment. The frozen source copies in this folder identify the implementation used here.

Render the saved project with `scripts/render_staging_scene.py -- S07 S003_S07_Coaching_v002 coaching`. Its selected audio comes from the shared `pipeline/audio.py` mix, copied from v001 without regenerating voices. `render-selection.json`, `render-inputs.json`, `surface-check.json` and `inspection.json` record selection and actual checks. `review-frames/` includes successive watch, clipboard, bend and release frames; the focused comparison prioritizes changed shoulders, hips and cuffs. Screenshots establish local visible differences, not normal-speed timing or subjective sound acceptance.

S07 uses one extra second beyond the initial 14-second budget. S08 onward moves by 24 frames in production.json; its local scene and existing sound assets are unchanged. Previous v001 files are retained as rejected construction evidence. S08 hand work remains deferred.
