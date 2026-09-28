# Image style menu and production adoption

Authorized workflow implementation, 14 September 2026. Fictional Heavy Box is the movement benchmark, not a new football film. Preserve all earlier delivered scenes, motion and sound.

User delegation for this implementation and its proofs: “implement it from step 1 to step 8 without stopping … if there are steps where you need a confirmation, confirm it yourself, approval, approve it yourself.” This authorizes agent review decisions for this work only; it is not user acceptance of viewed/heard artifacts or future films.

Requirements: (1) all 19 researched options grouped with evidence status; (2) shared construction guide; (3) specific reusable recipes; (4) native still per option; (5) usable image menu; (6) per-film selection and skill routing, preserving existing decisions; (7) representative end-to-end movement and staging/animatic tests; (8) lessons returned to the guides, helpers and journal.

The menu uses still images. Internal motion proofs are separate. New styles are limited to the demonstrated construction and angle; artwork is not a universal rig and a still is not motion evidence.

## Delivered

The current visual guide is revised in `artifacts/gallery-v003/`: all 19 images use the corrected arm layering and an open-arm still pose with both hands visible. Every saved guide pose passes wrist/framing checks; every underlying motion benchmark passes 240-frame connection checks. The current HTML and static menu use these images. Codex now recommends a short list for the story before an unresolved choice, and the menu clarifies that 2.5D environments can accompany other character styles. See the [guide revision record](artifacts/gallery-v003/review.md).

Latest box-push correction: [revised 10-second test](artifacts/hand-layer-v006/chibi/animatic-with-sound.mp4) · [before/after](artifacts/hand-layer-v006/chibi/before-after.mp4) · [editable scene](artifacts/hand-layer-v006/chibi/character.blend) · [review and reproduction](artifacts/hand-layer-v006/chibi/review.md). The shared builder now keeps the near arm/sleeve/hand in foreground passes and uses matching shoulder sides. All 240 original control poses and hand/foot geometry are preserved; derived upper-arm shapes change with the corrected shoulder anchors. Original sound is copied exactly. This is the user-requested test revision, not replacement of every historical film or catalogue sample.

[Open the 19-option gallery](../../pipeline/styles/gallery.html) · [View the image menu directly](../../pipeline/styles/menu.png) · [Shared construction guide](../../pipeline/styles/construction.md)

1. **Catalogue:** 19 options in `pipeline/styles/catalog.json`, grouped into 10 character designs, 7 visual finishes and 2 presentation methods. Status describes the exact new sample preset; previous stickman/cartoon proofs remain valid.
2. **Construction:** one guide maps continuous limbs, derived attachments, unified waist fills, native head/neck, proportions, contacts and draw order to inspected existing helpers.
3. **Recipes:** one specific Markdown recipe per option, with real settings, reusable helper references, customization guidance, sources and limits.
4. **Images:** 19 distinct stills rendered in Blender, with editable native projects and saved/reopened connection checks. Current guide poses and motion benchmarks are in `artifacts/gallery-v003`; `gallery-v001` and `gallery-v002` preserve the earlier versions.
5. **Menu:** offline HTML cards with category filters and prepared choice text; a static numbered image menu also works directly in the task. Copy the choice into the current animation task, or reply with its name/number.
6. **Workflow:** installed `produce-pencil-animation` updated after the story/before detailed construction. Selection pins recipe/guide/sample/settings/implementation in the film, preserves timing/audio, resumes without reselection and invalidates affected visual checkpoints on change.
7. **End-to-end proofs:** five actual production selections drove native Blender construction and complete inexpensive 10-second animatics through the existing audio pipeline. These internal videos are separate from the still-image menu.
8. **Lessons:** fixed the paper waist-shadow seam in the shared builder; recorded compact-body clearance, texture stretching, parallax and stable checkpoint-binding lessons in the guides, recipes and existing journals.

## Evidence

[Requirement-by-requirement audit](artifacts/completion-audit-v001.json).

| Tested preset | Encoded animatic | Actual scoped review |
|---|---|---|
| Chibi | [Watch](proofs/workflow-v001/chibi/animatic-v001/animatic-with-sound.mp4) | [Review](proofs/workflow-v001/chibi/animatic-v001/review.md) |
| Food mascot | [Watch](proofs/workflow-v001/food-mascot/animatic-v001/animatic-with-sound.mp4) | [Review](proofs/workflow-v001/food-mascot/animatic-v001/review.md) |
| Paper cutout | [Watch](proofs/workflow-v001/paper-cutout/animatic-v001/animatic-with-sound.mp4) | [Review](proofs/workflow-v001/paper-cutout/animatic-v001/review.md) |
| Collage | [Watch](proofs/workflow-v001/collage/animatic-v001/animatic-with-sound.mp4) | [Review](proofs/workflow-v001/collage/animatic-v001/review.md) |
| Parallax | [Watch](proofs/workflow-v001/parallax/animatic-v001/animatic-with-sound.mp4) | [Review](proofs/workflow-v001/parallax/animatic-v001/review.md) |

Every proof includes its actual `production.json`, pinned style assets, journal, editable `.blend`, original audio asset, resolved sound, premaster, encoded movie, checks and successive-frame sheets. Five × 240 = 1,200 rendered proof frames; each is 640×360, 24fps, 10 seconds. Original control poses and projected hand/foot geometry match the source on every frame. The authoritative premaster PCM matches the original soundtrack; the encoded movie uses lossy AAC. No new listening or real-time playback is claimed. Reviews inspected the full-action overview and every frame in the push (103–110) and release/recovery (150–173) intervals.

`pipeline/test_styles.py`, `pipeline/styles/test_gallery.cjs`, the existing checkpoint self-test, existing audio regression test and installed skill validator passed. The browser's URL policy blocked the local HTML preview; no browser workaround was used. Menu behavior was checked against an isolated DOM fixture and the static menu was visually inspected. Browser layout is not claimed as tested.

## Reproduce and extend

Run from the Pencil workspace root:

```sh
python3 pipeline/test_styles.py
node pipeline/styles/test_gallery.cjs
python3 pipeline/styles.py list
python3 pipeline/styles.py select PATH/production.json STYLE_ID --reviewer user --reason 'Actual user choice'
python3 pipeline/styles.py resolve PATH/production.json
/Users/samikd/MyProjects/PyBlend/.venv/bin/python pipeline/styles/build_gallery.py --sheet
```

To reproduce this implementation's representative proofs in a new output group: `python3 experiments/009_style_gallery/run_proofs.py --group workflow-v002`. The script's delegation record belongs only to this workflow test, never a future film. Native sample commands are in each recipe. Frame review extraction uses the installed PyBlend Python and `review_frames.py`.

A sample builder is a concrete adapter to the preserved Heavy Box scene, not an arbitrary-scene rigging service. New films provide their own story, poses, camera, identity artwork and audio. Fourteen new presets remain still-only for perceptual motion evidence; every preset has mechanical connection checks. New combinations, character turns, detailed hands, major proportion changes and tightly tracked textures still need focused proofs. No new database, server, dependency installation or online publication was added.
