# Pencil production pipeline

The reusable workflow is [SKILL.md](SKILL.md), the authoritative source used by the installed `produce-pencil-animation` skill. It coordinates brief, audiovisual script, design, assets, editable animation, sound, rendering, review and delivery. Each film supplies its subject, style, characters, timing, shot construction and sound palette. The workflow does not prescribe a niche, fixed effects or a film length.

## Guidance ownership

The main skill owns general production outcomes. [Production profiles](../productions/README.md#creative-context) own niche and creative defaults; each video owns its selected context and exceptions. Technique guides and tools are chosen by the actual action/medium, not automatically by the niche. For example, Samtoons uses character construction and speech guidance, while a silent mechanism diagram can use the same checkpoints without either human anatomy or TTS. New technical routes still require implementation and relevant evidence; profile selection alone cannot supply them.

Maintain the shared process in [SKILL.md](SKILL.md), execution conventions in this file, the adopted sound method in [sound-planning-method.md](sound-planning-method.md), and tested visual techniques in [styles/construction.md](styles/construction.md) and the relevant recipe. Original research and per-film journals are evidence, not parallel copies of current guidance. Add focused guidance files for demonstrated needs and link them from the relevant skill step; these files are not a fixed catalogue of future capabilities.

The installed `~/.codex/skills/produce-pencil-animation` directory links to `pipeline/skill`, which contains the regular `SKILL.md` file and its `agents/openai.yaml` UI metadata. `pipeline/SKILL.md` remains a stable link to that same source. The current Codex scanner follows linked directories but skips a linked `SKILL.md` file inside a skill folder; the dedicated folder also keeps archived workflows out of skill discovery. Edit the project source; if the workspace moves, reconnect the installed directory link instead of creating an independently edited copy. Archived snapshots remain historical. Record shared workflow changes in `pipeline/events.jsonl` and preserve reviewable versions when needed.

Run `python3 pipeline/test_workflow.py` to check this installation and the existing helpers' isolation of video reviews and selected shared-asset copies. This check uses disposable fixtures; it does not judge creative decisions.

**Current executable boundary:** `styles.py` validates the image catalogue and pins a film's selected visual recipe; `audio.py` resolves selected sound assets against named shot events and renders separate stereo stems plus a premaster with Python's standard library and FFmpeg. They do not generate a story, infer contacts, acquire licensed sounds, synthesize new sounds, judge listening quality or normalize the final movie automatically. Those decisions belong to the skill and the film's authored scripts. Blender scene building/rendering and final encoding reuse the existing film mechanisms below.

## Movement planning and geometry

Use [motion-planning.md](motion-planning.md) for authored layout, posing, breakdowns, face/body timing, secondary action and cleanup. `python3 pipeline/pose_geometry.py` checks the optional planar two-bone helper; it does not supply gait, balance or creative quality. The [Samtoons 002 diagnosis](../productions/Samtoons/videos/002-how-arsenal-won-the-league/research/body-mechanics-v001/diagnosis.md) preserves the earlier failed method and recovery investigation. Historical builders are evidence, not automatically current recipes.

## Choose the visual treatment

After understanding the storyline, open the [still-image style menu](styles/gallery.html) if the film has no settled treatment. It contains all 19 researched options grouped as character designs, finishes and presentation, now illustrated with attributed external artwork rather than native rig-test stills. Each image sets the design and finish quality to aim for; its source and concrete quality targets appear on the card. Choose a card and send its prepared text in the current Codex task; the page does not itself modify a film. Codex then records the actual user choice or scoped delegated decision:

The skill recommends a few options with images and short story-specific reasons before the choice, considering tone, clarity, likeness and movement demands. The gallery itself does not rank stories. Character design, finish and environment can be combined: #19 demonstrates layered 2.5D staging that can accompany other characters. The selector still pins one preset; record additional staging choices in the film brief and implement/review the combination in its scene.

```sh
python3 pipeline/styles.py list
python3 pipeline/styles.py select path/to/production.json chibi --reviewer user --reason 'Actual user choice'
python3 pipeline/styles.py resolve path/to/production.json
python3 pipeline/test_styles.py
```

Selection adds top-level `visual_style`, preserving picture timing, audio and other metadata. It stores versioned copies of the recipe, guide, reference image (`sample.png`), source/credit/quality targets (`option.json`), settings and benchmark implementation under the film's existing assets and appends a journal event. `resolve` checks the pinned hashes; resuming never silently upgrades a recipe. An explicit `--replace` keeps previous versions. Bind `assets/style-selection.json` to the existing staging/animatic checkpoints so a style revision invalidates affected visual acceptance. Keep unrelated sound inputs separate.

Open the film's pinned reference image and read its quality targets, selected recipe and [shared construction guide](styles/construction.md). Evaluate the actual production using the guide's [frame comparison, motion review, combined animatic and delivery review](styles/construction.md#evaluate-the-current-production). Select relevant shots and references from this film's requirements; metadata or a mechanically sound rig alone does not establish quality. `styles/build_samples.py` remains an optional fixed-view Heavy Box adapter for reproducing earlier evidence or checking related construction changes. It is not required for style selection or production acceptance. A new story supplies its own poses, camera, action and audio; the recipes retain construction examples and their actual evidence limits.

Demonstrated routes include native curves/meshes, fitted illustrated surfaces and matched drawings over editable controls. Their useful scope differs by shot. A style choice does not switch to a Grease Pencil armature or provide missing expressions/views. Existing GP experiments retain their own evidence. See [implementation and validation](../experiments/009_style_gallery/README.md).

The shared builder now separates the foreground arm, sleeve and hand with `character_layers.py`, and matches the derived shoulder sides to the source hand paths. New selections pin this helper too. The [corrected box-push comparison](../experiments/009_style_gallery/artifacts/hand-layer-v006/chibi/before-after.mp4) preserves all original controls and sound; earlier scenes and menu evidence remain archived as their original versions.

## Visible Blender authoring

Keep Blender's native window visible during authoring and preview playback. Reuse the available Blender connector; no separate live-view server or file watcher is needed. This is a view of the actual application alongside Codex, not an embedded video stream in the chat.

1. **Open and verify:** use the available app control to open/raise Blender (`cua.getApp("Blender")` on this desktop). Inspect the connected file with `get_blendfile_summary_path_info`, then verify the interactive instance, active scene and window before editing. On this Mac the existing `bl_ext.lab_blender_org.mcp` add-on auto-starts at `localhost:9876`; that is machine setup, not a portable project dependency. Discover the installed connector on another machine. Do not assume that an open window proves the connection works or that the connection targets the intended film.
2. **Preserve and select the work:** check the file path and unsaved changes before opening a different scene. Preserve existing work in an appropriate versioned file; clarify only if its ownership or save destination cannot be resolved. Load the selected film's working revision without overwriting delivered versions. Reinspect after user edits or scene changes, and avoid competing writes to the same scene. Unsaved work is a reason to preserve a copy before editing, not to silently move authoring into a background instance. Reverify the active visible scene after selecting it.
3. **Author visibly:** send short, coherent edit batches to the interactive Blender connector, using purpose-built tools where available and `execute_blender_code` for scene authoring when needed. Keep reproducible build/edit scripts under the film's `scripts/`. Show the relevant camera/viewport and let Blender redraw between batches. Do not run an old full-scene builder without checking for scene resets, file loads, automatic renders or quit calls. Long operations can temporarily freeze the interface; do not describe batch updates as continuous drawing strokes.
4. **Preview and inspect:** use the actual representative sequence for the existing staging review, following the [construction guide](styles/construction.md#demanding-motion-before-detailed-animation). Cover ordinary acting as well as hard mechanics where needed, keeping contacts and transitions visible. Play the current timeline and inspect actual viewport captures or rendered previews. Use native app capture if the connector's screenshot tool fails. If playback drops frames, judge timing with an encoded preview. A simplified viewport does not establish final lighting, compositing, sound or delivery quality. Retain the four existing reviews.
5. **Render separately when useful:** save a versioned scene, then run heavy rendering in a separate background Blender process with dedicated output paths and a log. Keep the interactive scene available; do not start another interactive bridge in the render process or overwrite its saved input during the render. Report real progress from the job, then show its actual output. Background edits do not appear automatically in the visible scene; loading a newer saved result is an explicit refresh after preserving unsaved work. Full-quality rendering still follows the existing accepted checkpoints or scoped waiver.

When streaming rendered stills into an encoder, remove the temporary frame before rendering and check that the render operator returned `FINISHED` before reading it. An interrupted render can otherwise reuse the previous frame. Cache validity should bind the native source hash, scene, frame range and output settings, rather than checking frame count alone. Samtoons 002 native delivery v027 applies these checks while retaining accepted creative inputs.

If the live connection fails, report that condition and restore it when possible. A visible saved-result preview can be used as a clearly identified fallback; do not silently claim a background job is being shown live. Journal meaningful scene revisions and render results under the current film root. Launching playback or capturing a screenshot alone does not constitute a creative motion or listening review.

### Runtime checks before adopting a new mechanism

Inspect the installed version, actual window/scene and connection first. On a versioned copy, verify only the API/control, preview/render operation and save/reopen behavior needed for the intended change. The [Phase A check](revisions/performance-workflow-v002/runtime-check/verify.json) demonstrates a saved native camera key and interactive render on Blender 5.2; it does not validate a new character rig or Grease Pencil authoring. The earlier failed background launch in the [research](../productions/Samtoons/research/python-animation-practice-v001.md) remains unexplained; the working live route is separate evidence.

Use supported Action slots/channelbags rather than legacy `action.fcurves` access on Blender 5.0+. Prefer `keyframe_insert()` for ordinary property keys. Verify exact Grease Pencil drawing/fill APIs before adopting new GP code; older scripts are not drop-in replacements. Mesh/curve/lattice shape keys do not establish native GP shape-key support. Viewport rendering needs the appropriate UI context; do not assume a headless operator is equivalent. Consult the installed API and the linked official references for the actual operation. Do not migrate working scenes simply because a new technique exists.

## Start or resume a production

Invoke `$produce-pencil-animation` in this workspace with the desired film or revision. For example: “Create an animation explaining this mechanism, without narration, with sound planned alongside the visuals.” Carry forward any already approved brief and current user direction.

Use [the production layout](../productions/README.md) for authorized new films: `productions/<production-name>/videos/<id-title>/`. Read the parent production context, then this video's brief, audiovisual script, plan and journal. Keep standalone as the default creative mode unless a series is explicitly requested; organization and shared assets do not determine storytelling.

The video directory is the **film root** for the commands and checkpoint examples below. Keep its `production.json`, selected local assets, authored scripts, `events.jsonl` and versioned artifacts there. Revisions use the same film root with new artifact versions. Existing legacy films and experiments remain in their current folders, which continue to serve as their film roots. Pass the correct root to the imported journal helper; its historical direct CLI targets Heavy Box.

For reusable production assets and applicable parent context, follow the layout's local snapshot convention before binding reviews. Earlier videos retain their chosen versions; shared updates require explicit adoption into the affected video. These are ordinary files, not a new project-management service.

The script describes **what the audience should understand and see/hear**. `production.json` holds **what was selected and when it happens**. An audio render writes a resolved copy with exact samples and asset hashes. These records serve different purposes; changing an output report does not change the input plan.

## Current selections and correction ownership

Keep one unambiguous current selection in the existing brief/plan: checkpoint revision(s), selected script, native source(s), edit/scene/frame map, sound plan/mix and review artifact. Use existing top-level metadata for these paths; the audio schema does not interpret arbitrary creative metadata. Resolve aliases such as `selected_script` versus `current_script` before a new operation; do not choose a source by newest filename. Read the delivered source map for completed work and preserve its historical plan and approvals. An active revision adopts changes explicitly into its own versioned records.

For each component being changed, state its authoritative source and next operation:

- **Builder-owned:** selected code/inputs reproduce the authored keys/drawings and approved corrections.
- **File-owned:** the selected `.blend` holds the animation; subsequent scripts operate on it without regenerating the corrected components.
- **Split ownership:** name a concrete boundary, such as builder-owned set and file-owned character action. Two independent sources must not overwrite the same property.

After a relevant correction, save/reopen and run the intended next operation on a versioned copy; compare the corrected interval and unchanged qualities. Live registries or extracted functions from older film scripts are not portable unless the loading route recreates them. Read all callers/dependencies before extracting or changing a helper. Do not execute historical builders blindly or overwrite delivered sources. Keep the selected voice model, voice references and cached takes intact.

Before a full operation, derive its required input paths from the **current selection**, then supply the decision-relevant paths to `require_checkpoint(..., required_inputs=[...])`. Record those files as checkpoint `inputs` when presenting the review. This catches a switch to an unreviewed filename even if the previous file remains unchanged. Bind any edit/selection record that selects scene ranges or dependencies, along with the relevant actual sources. Keep visual and sound inputs scoped; a picture-only change need not invalidate sound acceptance. The guard cannot discover undeclared dependencies or infer creative coverage. Do not fill `required_inputs` by copying the old approval's list.

Legacy calls remain compatible and delivered builders stay preserved. When a new native packaging step derives a file from an accepted source after review, record and verify that derivation/source mapping; do not label the new file user-approved merely to satisfy the check. Short technical proofs are not full-film delivery renders.

## Executable sound plan

From the project root, with `python3`, `ffmpeg` and `ffprobe` available:

```sh
python3 pipeline/audio.py resolve path/to/production.json --out path/to/resolved.json
python3 pipeline/audio.py build path/to/production.json --out path/to/artifacts/audio-v001
python3 pipeline/test_audio.py
```

`resolve` checks the plan, hashes selected files, probes formats, and writes resolved cues. `build` performs the same resolution, then mixes audio. Existing output paths are refused. A failed build records its error in that new output directory; rerun into a new revision after fixing the input.

This illustrative plan requires a real selected file and its actual SHA-256 before it will run:

```json
{
  "version": 1,
  "timeline": {"fps": "24", "start_frame": 1, "frames": 240, "sample_rate": 48000},
  "shots": [
    {"id": "action", "start_frame": 1, "events": {"release": 146}}
  ],
  "assets": {
    "slide-take": {
      "path": "assets/selected-slide.wav",
      "sha256": "REPLACE_WITH_ACTUAL_FILE_HASH",
      "source": "Record the creator and source URL, or original generation method",
      "license": "Record the applicable license and entitlement",
      "attribution": "Record required credit, or an empty string when none is required"
    }
  },
  "cues": [
    {
      "id": "release-slide", "shot": "action", "event": "release",
      "intent": "Make the change from resistance to movement audible",
      "asset": "slide-take", "stem": "foley",
      "in_seconds": 0, "duration_seconds": 0.7, "onset_seconds": 0.02,
      "offset_frames": 0, "gain_db": -6, "pan": 0,
      "fade_in_seconds": 0.004, "fade_out_seconds": 0.03
    }
  ],
  "mix_gain_db": -3
}
```

The example is a schema illustration, not a default film or preset. FPS, sample rate, duration, shot IDs, events, materials, stems and sound choices are supplied per production. Additional creative metadata may be stored at the plan's top level. Unknown fields inside timing/cue/asset records are rejected to catch misspelled controls.

### Timing and asset semantics

- `fps` is an exact positive integer or rational string such as `30000/1001`. `start_frame` and `frames` define the output range. Shot `start_frame` is absolute; each event is an offset from its shot start, with zero denoting the first frame of that shot. Fractional event/offset values are permitted.
- Cue `offset_frames` intentionally leads or follows its event. The source segment begins at `in_seconds` and lasts `duration_seconds`. `onset_seconds` is measured **from that segment's start**, not from the original file start. Its audible contact aligns to the event plus offset.
- A shot move changes its start; an internal action edit changes its event. The selected file/hash stays fixed. Duration is explicit: a longer action needs an updated segment or a prepared loop/extension; this command does not secretly stretch or repeat a sound.
- Asset paths resolve relative to the plan, allowing an existing shared library. The source, license and attribution fields are required provenance records; the tool checks their presence, not their legal correctness. The producer must establish suitability for the actual use. Cache generated/processed selections as files and describe their generation settings in `source` or the optional `notes` field.
- Mono and stereo sources are supported, resampled to the plan's rate and mixed to stereo. Multichannel sources require an explicitly prepared downmix. `pan` is a stereo balance from -1 to 1: it attenuates the opposite side without collapsing stereo ambience or boosting the other side. Fades and gain apply to the selected segment.
- A cue that crosses a film boundary fails unless its `allow_boundary_trim` is explicitly true. Trimming may be appropriate for a pre-lapped ambience or final fade; it must not conceal an accidentally cut-off contact/tail. A cue entirely outside the film always fails.
- Duplicate IDs, unresolved events/assets, changed hashes, invalid numbers, empty selections and source segments extending beyond the file fail before mixing. Quiet passages within a valid asset remain an audition decision.

### Outputs and responsibilities

The build writes `resolved-cues.json`, `stems/<name>.wav`, `mix-premaster.wav`, `checks.json` and `ffmpeg.log`. Stems and premaster are lossless stereo float32 WAV/RF64 as needed. The final movie's loudness target is deliberately not a shared creative preset: finish and measure it using the film's chosen specification. The report includes FFmpeg's premaster loudness/true-peak measurement, finite-sample and complete decode checks; it is not a listening-quality certificate. Levels above digital full scale are flagged for finishing rather than normalized silently. Plan and source hashes are checked again at completion to detect inputs changed during the render.

Mixing uses bounded groups of FFmpeg inputs and disk intermediates, which are removed after success. Memory does not require duration-wide Python arrays; disk/time still grow with duration, cue count and stem count. For very large projects, scene-local renders with explicitly preserved cross-scene tails can reduce this temporary-disk cost. There is no persistent processing cache or automatic contact extractor in this version; selected assets are the reusable cache boundary.

The tool computes sample positions from exact absolute time rather than accumulating rounded samples per frame. FFmpeg's per-input preprocessing, alignment and mix use those resolved integer samples. It preserves silent intervals, cue overlap, selected takes and tails within the requested output bounds. Cue gain belongs to the stem; `mix_gain_db` applies only to the premaster, and is recorded so stems can reproduce it.

## Where the proven mechanisms live

Read a source script before adapting it: existing paths, artwork, frame rates, fonts and loudness targets belong to its film.

| Need | Existing reference | Reuse boundary |
|---|---|---|
| Editable expressive motion, contact and restrained revisions | `experiments/001_heavy_box/README.md`, `artifacts/finish-v002/` | Preserve delivery; inspect relevant pose/contact mechanisms. C is an example, not a style requirement. |
| Original JSON-driven synthesis | `experiments/001_heavy_box/scripts/sound_finish_v001.py` | Author or reuse a suitable generator upstream; its output becomes a selected audio asset. |
| Local speech with acting instructions | `pipeline/qwen_voice.py`, `pipeline/qwen-voice/README.md` | Uses the shared MLX/Qwen runtime at `~/Models/qwen-voice`; produces a new raw WAV and provenance metadata. Select performances through the sound checkpoint; do not replace accepted takes when retiming. |
| Flat native artwork and keyframes | `experiments/003_alisson_winner/scripts/build_film.py` | Useful low-level construction functions; callers rely on film globals. No universal character rig has been extracted. |
| Held poses, facial replacements and hand/object checks | `experiments/006_just_five_minutes/scripts/build_film.py`, `verify_project.py` | Adapt motion and verification to current geometry. Existing artwork is film-specific. |
| Streamed native rendering | `experiments/006_just_five_minutes/scripts/render_film.py` | Adapt filenames, dimensions and actual frame rate including `fps_base`; preserve the bounded frame-storage pattern. |
| Muxing, two-pass loudness work and final encoded checks | `experiments/006_just_five_minutes/scripts/make_sound.py`, `finish_delivery.py` | Use the current plan's mix and delivery specification; inspect the encoded movie, not only the WAV. |
| Append-only tracking with artifact hashes | `experiments/001_heavy_box/journal.py` | Import `append_event` with the current production root; retain versioned files. |

For asset/tool decisions, read only the relevant part of `research/audio-tools/sound-production-tool-landscape.md`. For sound intention and auditioning, use [sound-planning-method.md](sound-planning-method.md). The original research proposal remains unchanged under `research/`; current execution capabilities are documented here.

## Adoption

Use this skill and shared audio input on the next authorized production or revision. Existing finished films keep their original scripts and assets. The implementation check creates temporary audio and exercises the real resolver/mixer; it is a technical check, not a new creative proof phase or evidence of audience response.

## Creative checkpoints (12 September 2026)

[SKILL.md](SKILL.md#creative-checkpoints) owns the user-requested staged review process, including acceptance, revision and scoped delegation. Technical audio checks verify samples, files and levels; they do not accept a sound's perceived identity or the scene's participant coverage. Apply the skill's current decisions to the selected film root; another video's approval or delegation does not authorize this one.

Use the existing production journal and `pipeline/checkpoints.py`. Append a checkpoint event under `checkpoint/<revision>/<staging|sound|animatic|delivery>` with the actual inputs/outputs. Use `pending_review` for a presented artifact, `rejected` for a rejected direction and `passed` with `reviewer="user"` only after explicit acceptance of those artifacts. A human-facing request, an agent's visual inspection or a technical pass cannot substitute. The guard checks the latest event for that revision/stage and rehashes its bound files. Changes to bound inputs invalidate acceptance. If the user explicitly waives a checkpoint, record `status="selected", reviewer="user", decision="waived"` and quote that instruction in the result; a waiver is not creative acceptance. Keep inputs scoped to the decision, so unrelated changes do not invalidate every review.

```python
from pipeline.checkpoints import require_checkpoint
# These paths must come from what this operation will actually consume.
require_checkpoint(film_root, revision, "animatic", required_inputs=current_picture_inputs)
```

Read-only CLI: `python3 pipeline/checkpoints.py FILM_ROOT REVISION animatic` checks the recorded bindings only; it does not know the pending operation's selection. Use the Python keyword above for that comparison. Run `python3 pipeline/checkpoints.py --self-test` and `python3 pipeline/test_workflow.py` for approval, source-switch and review-isolation behavior. An explicit scoped waiver still bypasses acceptance without claiming review. Preserve older delivered films and their original scripts.
