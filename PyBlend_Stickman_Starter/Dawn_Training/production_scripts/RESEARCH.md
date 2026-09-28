# Dawn Training — research, hypotheses and results

Started 7 September 2026; completed across 7–8 September local time. This records the evidence used for the specific Grease Pencil cutout short, not general animation reliability.

## Reuse and scope

Read the repository's [Blender foundations](../../docs/research/blender-platform-foundations.md), the issue-tracker research gates, domain vocabulary and ADR 0002. Reused Experiment 001/003's native SVG → Grease Pencil import, unlit palette and orthographic-camera findings, and Experiment 004's bounded rigid-part attachment strategy. Their prior outputs are evidence for mechanisms, not an accepted fighter asset.

The explicit user request authorizes an independent complete 30-second simple cutout film. It does not certify the broader semantic 2.5D platform or satisfy ADR 0002's two-character/four-motion matrix. Text in the attached guide images was treated as reference context, while the user's typed request governed the work.

## Source-verified Blender behavior

Local CLI and Blender MCP both reported **Blender 5.2.0 LTS**, build **fbe6228777e7**. The pinned official source used in the existing foundations guide matches that prefix.

- [SVG importer, pinned source](https://github.com/blender/blender/blob/fbe6228777e7d9afefcd61a413844e790ae75db7/source/blender/io/grease_pencil/intern/grease_pencil_io_import_svg.cc): `SVGImporter::read` uses 96-dpi SVG units, converts millimeters to scene scale, groups paths using the SVG parent group ID, and retains editable Bezier curves. `shape_attributes_to_curves` writes fill colors, fill IDs, visibility and handles. This supports named semantic SVG groups compiling directly to native layers.
- The same source converts sRGB SVG colors to linear values. The local build uses Standard display transformation and disables Grease Pencil lighting, so dramatic scene lighting does not shift the character palette.
- Bundled Blender MCP manual `manual/grease_pencil/properties/layers.rst`, “Relations”: layers inherit parent transforms, specifically supporting cutout animation. Bundled `bpy.types.GreasePencilLayer` exposes `parent`, `parent_bone`, opacity and transforms.
- Bundled `bpy.types.GreasePencilDrawing` exposes editable drawings/attributes and warns that previously acquired stroke slices become stale after topology changes. The importer and authored helpers reacquire strokes after adding geometry.
- The local `scripts/modules/_bpy_internal/grease_pencil/stroke.py` exposes `fill_id` and `hide_stroke`. Newly authored filled curves need an explicit nonzero fill ID in this build. The deprecated material `show_fill` flag alone did not make the local helper's fill render.

Direct internet requests for three Blender manual/API pages failed with HTTP 402 in the web tool. The bundled MCP docs and pinned GitHub implementation were available and used instead. No unavailable page content is claimed as read.

## Research papers and practical projects

The local [paper landscape](../../docs/research/ai_animation_papers_landscape.md) was checked first.

- [AniClipart, first-party method and layered-animation examples](https://aniclipart.github.io/): the published system uses keypoint Bezier trajectories, differentiable ARAP deformation and video-prior optimization, with a skeleton-fidelity loss. This is relevant evidence for keeping explicit motion controls and handling topology through layers. Its neural optimization pipeline was **not adopted or run**: supplied pose drawings plus native bone animation meet this small deterministic production's needs without its compute/dependency burden. Its reported evaluation is not evidence of this experiment's quality.
- [SceneCraft, ICML proceedings](https://proceedings.mlr.press/v235/hu24g.html): the prior local review describes executable Blender code plus rendered inspection and refinement. That informs the retained build → render → inspect workflow, not a claim that SceneCraft solves character animation. No SceneCraft model was run here.
- [Blender MCP, first-party repository](https://github.com/ahujasid/blender-mcp) and its [execution interface](https://github.com/ahujasid/blender-mcp/blob/main/src/blender_mcp/server.py) provide a practical example of Python execution and scene inspection through MCP. This task's installed connector exposes a different tool set; the repository is a mechanism reference, not a verified version identity for the installed connector. Installed connector version and model cost are unknown. The local MCP connection, build metadata query, SVG pilot, fill test and saved-project reload were actually exercised.

No third-party demo's undisclosed manual labor, rendering time or visual quality was treated as a locally reproduced result. No external asset generation or animation service was needed.

## Tested hypotheses and retained failures

### 1. Native layer parenting preserves editable source-derived cutouts

**Hypothesis:** source silhouette/semantic masks → VTracer Bezier paths → SVG parent groups → native GP layers → native bone parents will retain the supplied identity and permit bounded animation.

**Local test:** imported a front SVG through Blender MCP, inspected coordinates and layer names, then built the seven variants. Applied the same coordinate conversion to positions and both Bezier handles. Created named armatures and parented each layer by bone. Rendered the character studio, five pose tests, seven representative film frames and the entire film. Saved/reloaded the native project and checked every artwork layer has an existing parent bone.

**Limit:** these are pose-specific drawings with consistent control names, not one continuous 360-degree rig. Simple source segmentation and rigid rotations are intentionally bounded; larger new movements still need correction art.

### 2. New fills need fill IDs

**Failure:** the initial skin-under-eye rectangles and joint caps had material fill enabled but rendered as missing fills or outlines. Closed-eye shots exposed the background through rectangular gaps.

**Investigation:** compared imported drawing attributes with newly authored helper attributes through MCP, then inspected the pinned importer and installed stroke helpers.

**Single-variable probe:** assigned `fill_id = 1` and `hide_stroke = True` to the same existing skin helper curves. Rendered `review/diagnostics/fill_probe.png`; skin coverage appeared without changing the camera or geometry. The helper now writes fill IDs and stroke visibility explicitly.

**Result:** fixed native fill behavior. The earlier probe image retains the old incomplete face segmentation; use the final shot renders to judge the final artwork.

### 3. Reference detail versus tracing artifacts

**Failures:** tracing small native-size source parts with coarse settings dropped narrow mouth and facial ink details. Nearest-neighbor enlarged input retained details but followed pixel stair steps. Resampling an already green-keyed part introduced green edge colors.

**Chosen change:** enlarge source RGB three times with Lanczos first, then apply a nearest-neighbor semantic mask and a hard green key. Trace this image at smaller effective spatial tolerance and remove only uniform green paths. This separates resampling from chroma masking. Final parameters are executable in `prepare_art.py` and the retained SVGs preserve the exact result.

**Result:** materially better identity/ink retention with native editable curves and no green interpolation at the mask edge. Fine contour fidelity remains limited by the provided sheet resolution. Flat colors and shadows are traced shapes, not independently hand-inked high-resolution art. Visual inspection, not path count, drove the choice.

### 4. Motion exposes hidden artwork and ownership errors

**Failures:** the first run appeared to float; a split power-up pant shape opened at the pelvis; shoulder/elbow caps placed from rough landmarks protruded; disconnected source fragments remained assigned to the torso and stayed behind as limbs moved.

**Chosen changes:** evaluated the posed foot geometry against the plateau for each two-frame run sample; retained the measured contacts in `review/contact_check.json`; added a native hidden pelvis drawing; revised power-up elbow landmarks against the source; removed unnecessary protruding caps; restricted the torso to its main connected owned component. Kept the effects separate from character control animation so they could not conceal the rig test.

**Result:** the final film and pose test renders retain the corrected source parts and overlays. These checks establish the authored motion, not collision-free arbitrary posing or a production-ready general rig.

### 5. Continuous sky and render checkpoints

**Failure:** a discretely layered sky ended against a different gradient, creating a horizontal color seam.

**Chosen change:** neighboring emission-colored mesh strips share their endpoint colors. The meshes interpolate continuously. The environment stays lightweight and editable.

Frames are rendered as lossless PNG before H.264/AAC encoding. Rig, pose-test and blocking checkpoints are retained. The final file packs reference images, fonts and the original procedural sound track. Verification records frame count/dimensions, unique frame hashes, shot-boundary exposure, animated root/limbs, facial driver evaluation and packed assets.

## Evidence and reproducibility

- Source identity hashes and explicit part polygons: `artifacts/dawn_training/geometry/characters.json`.
- Blender version, curve/layer/bone counts and shots: `build_report.json`.
- Visual inspections: `review/character_studio.png`, `pose_tests.png`, `shot_*.png`.
- Entire render: `frames/frame_0001.png` through `frame_0720.png`.
- Duration and render time: `render_report.json`; independent media inspection is recorded in `media_probe.json`.
- Saved-project verification: `validation.json`.
- Original audio synthesis and cues: `make_sound.py`, `sound_cues.json`.
- Repeat commands: [README.md](README.md).

No Creator approval is recorded yet. “Complete first cut” describes delivery and timing, not an unsupported professional-quality certification. Runtime/source facts, locally rendered observations, paper reports and still-limited artistic judgments remain separate.

## Delivery verification

The final 720-frame render completed in 287.61 seconds. All 720 lossless frames had valid 1920 × 1080 headers and distinct SHA256 hashes. H.264/AAC media probing confirmed 720 video frames at 24 fps and an exact 30.000-second container duration. Saved-project checks passed for native GP/bone relations, every shot-boundary exposure, root travel and limb motion, the blink drivers, the independent neutral studio and packed references/audio. Blender MCP reopened the final file and found no missing external resources. Its window-screenshot endpoint returned a truncated response, so viewport screenshot capture was not used as evidence; native rendered frames are retained instead. The final scene list contains only the character studio, pose tests and film.

No human drawing edits were requested during the run. Several scripted art/rig corrections are described above; exact authoring wall time and model cost were not recorded. This single completed clip is not a batch throughput claim.
