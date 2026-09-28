# Connected artwork over simple controls

Read this with the selected option's recipe. Curves and flat meshes are the demonstrated default; dedicated Grease Pencil remains an optional renderer with its own proof. Choosing a visual style does not silently switch the construction backend.

## The selected image sets the visual target

The current menu uses attributed artwork from external creators and studios. It is the standard to aim for in design and finish, not a render made by this pipeline. Earlier native guide images remain internal construction evidence. Reuse simple control mechanisms where they fit the new construction; the old benchmark character is not the finished art direction for a new story.

Build for the actual shot. Assess reusable character artwork and rig controls separately from the animation performed with them:

- **Same character, new action:** retain suitable artwork and controls; author the new performance. Different movements do not automatically require new construction.
- **Different character:** develop its intended design. Reuse compatible components, control mechanisms and construction knowledge, adapting proportions and attachments where needed; a shared style alone does not establish compatibility.
- **New camera angle or extreme pose:** first check what the existing asset supports. Add missing views, expression/hand drawings or pose corrections, or change the construction where necessary. A new angle does not automatically require rebuilding the whole character.
- **Reusing animation:** assess the performance separately, including control compatibility, proportions, timing, weight, contact and expression. A similar action is a candidate, not proof of suitability; adapt it to the shot or animate afresh when it does not fit.

Check uncertain adaptations in a focused pose/motion proof from the intended camera, using the existing creative checkpoints. Record the reuse or adaptation and its tested limits in the existing brief or journal. Never weaken the intended character, action, camera or finish simply to fit an old asset. Keep compatible parts and create only what the shot needs; the Heavy Box benchmark's limits do not define what future films may attempt.

This distinction follows Toon Boom's separation of [character master templates and action templates](https://docs.toonboom.com/help/harmony-20/premium/library/about-template.html), with [replacement drawings added during animation](https://helpcentre.toonboom.com/hc/en-ca/articles/41014001536275-How-do-I-add-a-substitution-drawing-while-animating-a-rig). These are workflow references, not evidence that our current builder supports every action or view.

## Evaluate the current production

Evaluate the actual film against its brief and chosen references. Select representative shots and demanding moments from its storyboard or animatic to cover unresolved risks; do not substitute an unrelated test scene. Build only the missing capability those shots need, consistent with [professional rigging guidance](https://www.toonboom.com/training-punk-rig).

After `resolve`, open the film's pinned `sample.png` and read `option.json` → `reference` for the source, credit and visible `quality_targets`. These are stored with the recipe under `visual_style.files`; use those film-local copies on resume. The reference establishes craft and visual language, not a requirement to reuse its characters, logos, setting or exact composition as movie assets.

1. **Visual design:** translate the reference into the brief: silhouette/proportions, expressions, face/body consistency, line quality, palette, finish and composition. Describe story-driven changes and any combination of character, finish and environment. Compare a representative native frame with its intended finish beside the selected reference at comparable viewing size in the existing staging checkpoint. Record and fix visible gaps before detailed animation; a matching style label or working rig is insufficient.
2. **Movement and construction:** inspect a short preview of the actual shot from its intended camera, using relevant motion references when needed to judge timing, weight or acting. Check readable poses and expressions, contact, deformation, attachments and layering through the required action. For example, dialogue may need facial acting and gestures; a football kick needs ball contact and readable follow-through. Review normal-speed playback and successive frames where a defect needs diagnosis. Save/reopen the native assets and check the controls or drawing changes that the shot needs to remain editable. Add missing drawings or construction where needed.
3. **Story and performance:** watch the complete inexpensive animatic with the selected sound. Assess whether action, emotion, meaning, staging and pacing work together across cuts. A successful isolated shot cannot establish that the complete film works. Use the existing sound and combined-animatic checkpoints and their scoped delegation rules.
4. **Final quality:** review the actual encoded delivery at its intended viewing size for visual finish, motion, sound and story clarity, alongside the workflow's technical file checks. Rough previews support decisions; they do not establish delivery quality. Record actual review results and leave unreviewed qualities unknown.

Save comparisons, relevant references and findings in the current film's existing files/journal, and bind `assets/style-selection.json` to the visual checkpoints. If the design is weaker than the reference, revise the artwork or staging; do not quietly lower the target. Any user-directed reduction in scope belongs in the brief and affected review. These evaluations use the existing creative checkpoints without an additional approval process or separate proof film. A reference still cannot establish motion quality, and technical checks cannot certify creative success.

## Construction rules from the box and trio tests

- Keep motion controls separate from artwork. Preserve hand/foot contact targets; derive shoulders, hips and bend controls when proportions change. A good drawing alone does not establish a usable character.
- Use one live continuous curve for each limb. The hand and foot attach to the same endpoints that drive that curve. Put cuffs and sleeves on exact driven subcurves (`curve_section`), not independent images or separately keyed pieces.
- Combine shirt, hips and shorts fills before outlining their external silhouette. The existing `Unified body` compositor pass avoids independently outlined waist caps. Different shirt/shorts colors can meet inside that silhouette; never expose an unfilled joint gap. Check sleeve/body ordering separately.
- Draw head, hair, facial features and clothing in a coordinated visual language. Use native art attached to one head control, with a continuous neck behind the collar. Do not paste a photographic head onto a flat cartoon body. Likeness needs deliberate character design and review.
- For illustrated facial replacements, inspect where the drawing ends. Do not stack a closed, wide neck stump onto a second narrow neck. Join a jaw/skull attachment that follows the head to a collar attachment that follows the torso; check the resulting neck length, width, side contours and front-collar overlap in motion. Register replacement drawings against stable skull/eye landmarks rather than a mouth-dependent bounding box, and add intermediate expressions when a direct swap visibly pops. A 24-fps export or coincident endpoints alone does not establish natural anatomy or smooth acting.
- Derive short-body proportions from the pelvis, with a floor/contact clearance suitable for that character. The benchmark's `max(body_y*0.70, max(foot_y)+0.78)` is an example, not an anatomical rule. Long reaches and low crouches may need new authored poses.
- Keep floor contact geometry unchanged when testing appearance alone. When feet change shape, recalculate their floor offset and recheck the full planted interval; endpoint agreement alone cannot prove no sliding.
- Treat draw order as authored shot design. Both arms in the stage pass get hidden when the body is composited above them; changing object Z cannot fix that. `pipeline/character_layers.py` separates the near arm, its driven sleeve and hand into foreground passes. The near arm/hand are in front by default; the scene's `front_arm_over_face` control can put the arm behind the face for an authored pose. Decide prop occlusion for each shot. Full turns, foreshortening, precise fingers, cloth simulation and quadruped rigs are outside the current proof.
- Match derived shoulders to the intended arms. In the box benchmark, the near hand rests screen-left: its shoulder must also be screen-left. The old opposite-side anchors made the arms cross the torso. Correcting these anchors changes upper-arm geometry while preserving the original hand, elbow and timing controls. Inspect the wrist, sleeve and shoulder together at rest, reach and recovery; do not move the hand target merely to hide a layering fault.
- Keep texture low contrast at moving seams. The sample's procedural Generated coordinates are deterministic and object-bound, but curved limbs can stretch patterns as their bounds change. Specific garment prints belong on stable body-local artwork; demanding texture tracking needs authored UVs or an additional proof.

## Cast-expansion failure: visible surfaces and timing

The [Samtoons full-animatic audit](../../productions/Samtoons/videos/001-manchester-derby-2026-09-13/research/animatic-audit-v001/audit-and-repair-plan.md) found continuous earlier actors beside new actors with roughly cut raster arms, generic replacement curves, residual artwork and visible joint covers. Numerical wrist attachment checks passed despite these defects. This establishes a failed adaptation, not a tested replacement recipe.

For a new drawing, fit its actual silhouette, garment boundaries and joint overlap; do not copy pixel thresholds or approximate weights as if they described every body. If replacing a limb, inspect the complete visible shoulder-to-hand and pelvis-to-boot contours in all required poses, including residual source art, material/outline agreement and depth order. Character appearance belongs to asset identity, not a scene object’s name. Preserve the selected simple controls where suitable; add fitted surfaces, corrective drawings or missing views where the shot needs them.

Check a kick as a coordinated support-foot, pelvis, knee, ankle, boot and ball action. A point matching at one frame does not establish approach, surface contact, release or recovery. Inspect the full changed contact/bend/turn intervals frame by frame and at normal speed; record actual coverage. Retain purposeful holds, but distinguish them from sparse poses stretched to fill a duration. Do not adopt a new construction across the cast until its visible result meets the current film’s accepted standard.

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

## Optional Heavy Box regression check

Use this only when reproducing the earlier test or checking a change to the mechanisms exercised by the Heavy Box scene. It is not required for selecting a style, building a new character or accepting a production. The general evaluation method is the current-film review above; a box test covers only its own construction and action.

The archived native guide images use an open-arm still pose so both hands are visible, including on wide mascots. `render_sample` saves that separate `sample-pose.blend` and reopens it to check wrists and hand framing. The `character.blend` saved before the still pose retains its motion. These internal tests are separate from the external images now shown in the menu. A static presentation pose is not an additional animation proof.

1. Save/reopen native artwork and edit a hand target: limb and hand must remain joined.
   Evaluate geometry in the non-rendered `Character editing` view layer. The stage pass now excludes the foreground arm, so its dependency graph cannot verify that arm's evaluated shape.
2. Compare all source control poses and contact geometry when the task only changes appearance.
3. Inspect successive frames of reach, maximum push, release, stumble and recovery. Check actual visible hands, wrists, collar, waist, feet and crossings at phone size. A numerical endpoint check does not prove layering.
4. Keep rerun outputs in a new versioned experiment directory and compare the affected behavior with the previous result. Preserve the original scene, artwork, motion, sound and evidence.
5. Keep evidence scoped. A benchmark's still/connection status describes only our internal native test. `Motion proof` needs inspected sequential frames/clip too. Neither establishes reference-level artwork, audience appeal, likeness, every angle or all possible actions.

## Selection and resuming

Open `gallery.html` after understanding the storyline and before detailed character construction. Each card prepares a text choice to send in the current Codex task; it cannot itself submit a message or modify a production. If a style was already settled, preserve it and use `resolve` instead of asking again. A legacy film with no metadata but an explicit style decision can retain that decision in its brief; do not replace its art to match a menu sample.

Codex recommends a short list with sample images and story-specific reasons before an unresolved choice: tone, clarity, likeness, movement demands and production effort. The gallery has no story classifier. The user chooses, or Codex chooses within an explicit delegation; save the actual rationale in the existing brief/journal.

Character design, finish and environment are independent creative choices. The #19 parallax card is a reference for layered environment design. Other characters can use layered backgrounds, foreground scenery and simple 3D props. In this benchmark `design`, `finish` and `presentation` are separate settings, but the selector currently pins one preset; a combination is authored in the film's scene and brief, not silently substituted into pinned settings. Review camera framing, ground contact, foreground occlusion and finish consistency for the combination. The current actor is drawn for a fixed view; orbiting it requires new views or a different construction. Orthographic depth alone does not change apparent size ([Blender camera documentation](https://docs.blender.org/manual/en/4.4/render/cameras.html)); the existing parallax proof animates scenery at different rates.

From the workspace root:

```sh
python3 pipeline/styles.py select PATH/production.json flat-vector --reviewer user --reason 'Actual user choice in this task'
python3 pipeline/styles.py resolve PATH/production.json
```

Use `--reviewer assistant` for delegated choices, stating the actual delegation. Use `--replace` only for an explicitly requested style revision. Selection preserves other top-level plan data, pins the recipe/guide/reference image/source/quality targets/settings/benchmark implementation under the film's assets and appends to its existing journal. The choice sets an art direction and quality target. The old benchmark settings use a flat human for finishes/presentations and a stickman for whiteboard; these are construction examples, not the new film's required character. Combining character/finish/presentation is a film-specific adaptation requiring a small proof.

For an optional Heavy Box check, the adapter can consume a pinned selection:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python pipeline/styles/build_samples.py -- --production PATH/production.json --out NEW_OUTPUT_DIRECTORY --motion
```

This optional adapter accepts only its 240-frame/24fps timeline; do not change a production's timing to fit it. New film scripts load `resolve`, use the pinned reference, quality targets and recipe to design their own story artwork, adapting useful mechanisms, and save `visual_style_id` in the native scene. Evaluate those films using their own shots and references. Short tests are not full-quality delivery; new full render scripts keep the existing staging/sound/animatic gates.

## Lessons confirmed by the gallery proof

The five selection-to-animatic tests are in `experiments/009_style_gallery/proofs/workflow-v001/`. Their reviews cover source-preserved motion, native editability and successive push/recovery frames. Compact bodies and the toast mascot work within this action. Separate paper-shadow copies around torso/shorts reopened an internal seam; the shared builder now limits those offsets to head artwork. High-contrast Generated-coordinate stripes visibly stretch on limbs: keep detailed print on body-local shapes or author a better texture mapping for the film. Parallax is implemented by different layer travel rates, not just Z offsets.

The selection tool writes a stable `assets/style-selection.json` in addition to archived versions. Bind this stable file to affected visual checkpoints; binding only an archived selection would leave old approval valid after a new choice. The runnable selection test covers this failure and confirms sound approval remains valid.
