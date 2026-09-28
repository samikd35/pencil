# First animated batch — v012 review

**Scope:** opening 1,021 frames, 24 fps, 42.542 seconds. Concealed narrator → recycled year banner → Bottle FC truck → striker phone call → bag set-down and two lateral steps → number-nine corner-flag reveal → “Win us a corner.”

The user selected Video 1's illustrated-rig foundation after clarification that its finished cast used textured deformable meshes and separate native facial geometry, rather than exclusively hand-drawn Grease Pencil. The user then authorized starting the first batch. This selects construction and work scope; it is not acceptance of this new render.

## Construction

Arteta (both scenes) and Gyökeres use one coherent source drawing each for head, neck, clothing, limbs and shoes. `assets/rig-art-v012/arteta-gyokeres.png` is one generated derivative of the previously accepted `artifacts/visual-treatment-v001/gyokeres-arteta.png`, prepared with separated arms for rigging. The derivative remains a review candidate. Source identity, proportions and outfit were retained as design targets, not asserted as user-approved results.

The bitmap is mapped onto a native triangulated silhouette mesh, bound to a native 14-bone skeleton fitted to its measured joints. It is **illustrated mesh animation**, not automatic vector tracing, a rigid image plane, or hand-drawn Grease Pencil. The opaque background returned by generation is excluded by the native silhouette geometry; no regenerated background or altered raster was needed. The complete source head/body remain together. Neck weights blend across the collar; one source shorts garment follows the hips and thighs.

Existing body/prop timing is retained where compatible. Leg lengths are measured from the new artwork and the pelvis trajectory is fitted to reachable support targets. The phone arm is reposed for these proportions. The bag follows the rebuilt palm until frame 26 and stays on the carpet afterward. Foot geometry is bound rigidly below the sole region; automated checks evaluate the rendered mesh's planted sole vertices, not merely ankle controls.

The old approximate head/body surfaces are hidden. Native mouth shapes are independently exposed using the existing dialogue schedule; a native shape key closes the actual drawn eyes. Lip timing remains rough. Brows/gaze retain the source expression and these figures do not supply arbitrary head turns. The worker and driver retain their existing articulated native drawings. The concealed narrator uses native silhouette geometry in the established shared room; its reveal environment is unchanged.

This batch contains gestures and lateral steps. Bruno's accepted run/jump remains the construction reference for later extreme actions; no new run/jump validation is claimed here.

## Inspection and bounded fixes

The first binding attempt incorrectly gave lower shirt-edge vertices arm influence; the resulting spikes are preserved in `cast-check.png`. Correcting the semantic garment boundary removes those assignments in the rebuild script. Dual-quaternion volume preservation inflated the deeply folded phone sleeve; linear skinning and a refitted phone pose are used for this bounded scene. `phone-refitted.png` and the later rendered frames show that revision. These settings are scoped to this artwork and action.

Inspected stills cover the year gag, driver, speaking reactions, bag contact, steps and phone. File/geometry checks do not establish natural acting, likeness or listening quality. Normal-speed combined review is for the user; no agent listening acceptance is claimed. Do not label this batch or the full film creatively approved.

## Files

- `batch01-review-v012.mp4`: full first-batch review with the existing approved audio interval.
- `batch01-v012.blend`: editable native project with packed artwork.
- `edit.json`: exact shot order and scene/frame mapping.
- `cast-registry.json`: fitted source landmarks and native object/control names.
- `native-checks.json`: saved-file construction and evaluated contact checks.
- `encode-checks.json`: encoded format, duration, frame count and decode check.
- `frames/`: samples from the actual full-batch render.
- `live-before-rebuild.blend`: preserved prior interactive state.

The builder is `scripts/rebuild_batch01_v012.py`; its named operations run in the visible existing first-batch Blender session. The saved native project is the authoritative rendered state. Re-render with Blender in background opening this saved file and running `scripts/render_batch01_v012.py`. No source generation is needed to re-render it.

Next chronological batch starts at film frame 1022 (the practice kick). The rest of the film is not completed by this deliverable.
