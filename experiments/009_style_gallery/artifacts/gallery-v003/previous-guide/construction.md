# Connected artwork over simple controls

Read this with the selected option's recipe. Curves and flat meshes are the demonstrated default; dedicated Grease Pencil remains an optional renderer with its own proof. Choosing a visual style does not silently switch the construction backend.

## Construction rules from the box and trio tests

- Keep motion controls separate from artwork. Preserve hand/foot contact targets; derive shoulders, hips and bend controls when proportions change. A good drawing alone does not establish a usable character.
- Use one live continuous curve for each limb. The hand and foot attach to the same endpoints that drive that curve. Put cuffs and sleeves on exact driven subcurves (`curve_section`), not independent images or separately keyed pieces.
- Combine shirt, hips and shorts fills before outlining their external silhouette. The existing `Unified body` compositor pass avoids independently outlined waist caps. Different shirt/shorts colors can meet inside that silhouette; never expose an unfilled joint gap. Check sleeve/body ordering separately.
- Draw head, hair, facial features and clothing in a coordinated visual language. Use native art attached to one head control, with a continuous neck behind the collar. Do not paste a photographic head onto a flat cartoon body. Likeness needs deliberate character design and review.
- Derive short-body proportions from the pelvis, with a floor/contact clearance suitable for that character. The benchmark's `max(body_y*0.70, max(foot_y)+0.78)` is an example, not an anatomical rule. Long reaches and low crouches may need new authored poses.
- Keep floor contact geometry unchanged when testing appearance alone. When feet change shape, recalculate their floor offset and recheck the full planted interval; endpoint agreement alone cannot prove no sliding.
- Treat draw order as authored shot design. Both arms in the stage pass get hidden when the body is composited above them; changing object Z cannot fix that. `pipeline/character_layers.py` separates the near arm, its driven sleeve and hand into foreground passes. The near arm/hand are in front by default; the scene's `front_arm_over_face` control can put the arm behind the face for an authored pose. Decide prop occlusion for each shot. Full turns, foreshortening, precise fingers, cloth simulation and quadruped rigs are outside the current proof.
- Match derived shoulders to the intended arms. In the box benchmark, the near hand rests screen-left: its shoulder must also be screen-left. The old opposite-side anchors made the arms cross the torso. Correcting these anchors changes upper-arm geometry while preserving the original hand, elbow and timing controls. Inspect the wrist, sleeve and shoulder together at rest, reach and recovery; do not move the hand target merely to hide a layering fault.
- Keep texture low contrast at moving seams. The sample's procedural Generated coordinates are deterministic and object-bound, but curved limbs can stretch patterns as their bounds change. Specific garment prints belong on stable body-local artwork; demanding texture tracking needs authored UVs or an additional proof.

## Actual reusable code and contract

`build_samples.py` loads only inspected helper definitions from the existing scripts (which otherwise execute film builds on import):

| Reused mechanism | Source |
|---|---|
| Native materials, polygons, ovals, source-control and endpoint checks | `experiments/008_cartoon_skin/build_skin.py` |
| Exact driven limb subcurves and material assignment | `experiments/008_cartoon_skin/build_ronny.py` |
| Derived anchors and continuous neck lines | `experiments/008_cartoon_skin/build_coherent.py` |
| Smoothing and world-space coordinate drivers | `experiments/001_heavy_box/scripts/build_v005.py` |
| Foreground arm/sleeve/hand compositor passes; editable face order | `pipeline/character_layers.py` |

The adapter opens `experiments/008_cartoon_skin/artifacts/coherent-proof-v003/cartoon-skin.blend`. It expects `CTRL_Body`, `CTRL_Head`, `CTRL_Hand_*`, `CTRL_Foot_*`, `CTRL_Elbow_*`, `CTRL_Knee_*`, `ATTACH_Shoulder_*`, `ATTACH_Hip_*`, `ANCHOR_Shoulder`; the `Arm_*`/`Leg_*` outline/fill pairs and hand/foot artwork; and the source's three composited view layers. Its `apply_style(option)` replaces visible artwork and adds derived `STYLE_*` controls, without rewriting source animation tracks.

For a new film, use its authored motion and adapt these bindings after reading its builder. This is a concrete benchmark adapter, not a promise to retarget arbitrary Blender scenes. Do not load the box action as the new storyline. Geometry choices live in `apply_style`; materials in `patterned`; camera/sample rendering in `render_sample`. The recipe identifies their exact settings.

## Evidence before promoting a new character

1. Save/reopen native artwork and edit a hand target: limb and hand must remain joined.
   Evaluate geometry in the non-rendered `Character editing` view layer. The stage pass now excludes the foreground arm, so its dependency graph cannot verify that arm's evaluated shape.
2. Compare all source control poses and contact geometry when the task only changes appearance.
3. Inspect successive frames of reach, maximum push, release, stumble and recovery. Check actual visible hands, wrists, collar, waist, feet and crossings at phone size. A numerical endpoint check does not prove layering.
4. Review a complete inexpensive animatic in the film's staging with its selected sound. Bind the film-local `style-selection.json` to staging and animatic journal entries. A changed selection requires a new affected visual review; retain unrelated sound decisions.
5. Keep evidence scoped. `Still + connection checks` means only the catalogue sample and mechanical benchmark passed. `Motion proof` needs inspected sequential frames/clip too. Neither establishes audience appeal, likeness, every angle or all possible actions.

## Selection and resuming

Open `gallery.html` after understanding the storyline and before detailed character construction. Each card prepares a text choice to send in the current Codex task; it cannot itself submit a message or modify a production. If a style was already settled, preserve it and use `resolve` instead of asking again. A legacy film with no metadata but an explicit style decision can retain that decision in its brief; do not replace its art to match a menu sample.

From the workspace root:

```sh
python3 pipeline/styles.py select PATH/production.json flat-vector --reviewer user --reason 'Actual user choice in this task'
python3 pipeline/styles.py resolve PATH/production.json
```

Use `--reviewer assistant` for delegated choices, stating the actual delegation. Use `--replace` only for an explicitly requested style revision. Selection preserves other top-level plan data, pins the recipe/guide/sample/settings/benchmark implementation under the film's assets and appends to its existing journal. The choice is a treatment preset. Finishes use the sample's flat human (whiteboard uses stickman), and presentations use flat-vector art; combining another character/finish/presentation is a film-specific adaptation requiring a small proof, not an already validated automatic combination.

The benchmark can consume the actual selection:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --production PATH/production.json --out NEW_OUTPUT_DIRECTORY --motion
```

This explicit benchmark accepts only its 240-frame/24fps timeline. New film scripts load `resolve`, use the selected settings/recipe when constructing their own story, and save `visual_style_id` in the native scene. Short tests are not full-quality delivery; new full render scripts keep the existing staging/sound/animatic gates.

## Lessons confirmed by the gallery proof

The five selection-to-animatic tests are in `experiments/009_style_gallery/proofs/workflow-v001/`. Their reviews cover source-preserved motion, native editability and successive push/recovery frames. Compact bodies and the toast mascot work within this action. Separate paper-shadow copies around torso/shorts reopened an internal seam; the shared builder now limits those offsets to head artwork. High-contrast Generated-coordinate stripes visibly stretch on limbs: keep detailed print on body-local shapes or author a better texture mapping for the film. Parallax is implemented by different layer travel rates, not just Z offsets.

The selection tool writes a stable `assets/style-selection.json` in addition to archived versions. Bind this stable file to affected visual checkpoints; binding only an archived selection would leave old approval valid after a new choice. The runnable selection test covers this failure and confirms sound approval remains valid.
