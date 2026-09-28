# Pencil production pipeline

The reusable workflow is the installed `produce-pencil-animation` skill. It coordinates brief, audiovisual script, design, assets, editable animation, sound, rendering, review and delivery. Each film supplies its subject, style, characters, timing, shot construction and sound palette. The workflow does not prescribe a niche, fixed effects or a film length.

**Current executable boundary:** `styles.py` validates the image catalogue and pins a film's selected visual recipe; `audio.py` resolves selected sound assets against named shot events and renders separate stereo stems plus a premaster with Python's standard library and FFmpeg. They do not generate a story, infer contacts, acquire licensed sounds, synthesize new sounds, judge listening quality or normalize the final movie automatically. Those decisions belong to the skill and the film's authored scripts. Blender scene building/rendering and final encoding reuse the existing film mechanisms below.

## Choose the visual treatment

After understanding the storyline, open the [still-image style menu](styles/gallery.html) if the film has no settled treatment. It contains all 19 researched options grouped as character designs, finishes and presentation. Choose a card and send its prepared text in the current Codex task; the page does not itself modify a film. Codex then records the actual user choice or scoped delegated decision:

The skill recommends a few options with images and short story-specific reasons before the choice, considering tone, clarity, likeness and movement demands. The gallery itself does not rank stories. Character design, finish and environment can be combined: #19 demonstrates layered 2.5D staging that can accompany other characters. The selector still pins one preset; record additional staging choices in the film brief and implement/review the combination in its scene.

```sh
python3 pipeline/styles.py list
python3 pipeline/styles.py select path/to/production.json chibi --reviewer user --reason 'Actual user choice'
python3 pipeline/styles.py resolve path/to/production.json
python3 pipeline/test_styles.py
```

Selection adds top-level `visual_style`, preserving picture timing, audio and other metadata. It stores versioned copies of the recipe, guide, sample, settings and benchmark implementation under the film's existing assets and appends a journal event. `resolve` checks the pinned hashes; resuming never silently upgrades a recipe. An explicit `--replace` keeps previous versions. Bind `assets/style-selection.json` to the existing staging/animatic checkpoints so a style revision invalidates affected visual acceptance. Keep unrelated sound inputs separate.

Read the selected recipe and [shared construction guide](styles/construction.md), then apply its settings in the film's native scene builder. Metadata alone does not change an animation. `styles/build_samples.py` demonstrates selection-to-artwork on the preserved Heavy Box scene; it is explicitly a fixed-view benchmark adapter. A new story supplies its own poses, camera, action and audio. The recipes describe reusable mechanisms, actual tests and limitations. New character/finish combinations need a small film-specific proof.

The default demonstrated implementation uses native curves and flat meshes over simple editable controls. A style choice does not switch to a Grease Pencil armature. Existing GP experiments remain renderer comparisons, with their own evidence. See [implementation and validation](../experiments/009_style_gallery/README.md).

The shared builder now separates the foreground arm, sleeve and hand with `character_layers.py`, and matches the derived shoulder sides to the source hand paths. New selections pin this helper too. The [corrected box-push comparison](../experiments/009_style_gallery/artifacts/hand-layer-v006/chibi/before-after.mp4) preserves all original controls and sound; earlier scenes and menu evidence remain archived as their original versions.

## Start or resume a production

Invoke `$produce-pencil-animation` in this workspace with the desired film or revision. For example: “Create an animation explaining this mechanism, without narration, with sound planned alongside the visuals.” Carry forward any already approved brief and current user direction.

Use the existing production folder for a revision, or create a new one for an authorized new film. Keep the brief/audiovisual script, `production.json`, selected assets, authored scripts and versioned artifacts there. Continue its `events.jsonl` with the existing journal helper. These are ordinary files, not a new project-management service.

The script describes **what the audience should understand and see/hear**. `production.json` holds **what was selected and when it happens**. An audio render writes a resolved copy with exact samples and asset hashes. These records serve different purposes; changing an output report does not change the input plan.

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
| Flat native artwork and keyframes | `experiments/003_alisson_winner/scripts/build_film.py` | Useful low-level construction functions; callers rely on film globals. No universal character rig has been extracted. |
| Held poses, facial replacements and hand/object checks | `experiments/006_just_five_minutes/scripts/build_film.py`, `verify_project.py` | Adapt motion and verification to current geometry. Existing artwork is film-specific. |
| Streamed native rendering | `experiments/006_just_five_minutes/scripts/render_film.py` | Adapt filenames, dimensions and actual frame rate including `fps_base`; preserve the bounded frame-storage pattern. |
| Muxing, two-pass loudness work and final encoded checks | `experiments/006_just_five_minutes/scripts/make_sound.py`, `finish_delivery.py` | Use the current plan's mix and delivery specification; inspect the encoded movie, not only the WAV. |
| Append-only tracking with artifact hashes | `experiments/001_heavy_box/journal.py` | Import `append_event` with the current production root; retain versioned files. |

For asset/tool decisions, read only the relevant part of `research/audio-tools/sound-production-tool-landscape.md`. For sound intention and auditioning, use `research/audio-tools/sound-planning-method.md`. Those documents distinguish researched, proposed and actually tested capabilities.

## Adoption

Use this skill and shared audio input on the next authorized production or revision. Existing finished films keep their original scripts and assets. The implementation check creates temporary audio and exercises the real resolver/mixer; it is a technical check, not a new creative proof phase or evidence of audience response.

## Creative checkpoints (12 September 2026)

The installed `produce-pencil-animation` skill is the authority for the user-requested staged review process. Technical audio checks verify samples, files and levels; they do not accept a sound's perceived identity or the scene's participant coverage. A full-quality export follows current staging, sound direction and combined-animatic acceptance, or the user's explicit waiver/delegation. Short proofs remain available while staging/sound decisions are pending; the combined animatic follows those decisions. When the user delegates checkpoint choices for a film, record the scoped waiver and make the producer's review decisions without asking again; do not call those decisions user acceptance.

Use the existing production journal and `pipeline/checkpoints.py`. Append a checkpoint event under `checkpoint/<revision>/<staging|sound|animatic|delivery>` with the actual inputs/outputs. Use `pending_review` for a presented artifact, `rejected` for a rejected direction and `passed` with `reviewer="user"` only after explicit acceptance of those artifacts. A human-facing request, an agent's visual inspection or a technical pass cannot substitute. The guard checks the latest event for that revision/stage and rehashes its bound files. Changes to bound inputs invalidate acceptance. If the user explicitly waives a checkpoint, record `status="selected", reviewer="user", decision="waived"` and quote that instruction in the result; a waiver is not creative acceptance. Keep inputs scoped to the decision, so unrelated changes do not invalidate every review.

```python
from pipeline.checkpoints import require_checkpoint
require_checkpoint(film_root, revision, "animatic")
```

Read-only CLI: `python3 pipeline/checkpoints.py FILM_ROOT REVISION animatic`. Run the behavioral self-check with `python3 pipeline/checkpoints.py --self-test`. This is a journal-backed guard, not an additional production database. Preserve older delivered films and their original scripts.
