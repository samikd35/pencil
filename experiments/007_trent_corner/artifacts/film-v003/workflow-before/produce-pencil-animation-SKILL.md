---
name: produce-pencil-animation
description: "Produce or revise Pencil animations with joint picture-and-sound planning, editable motion, reproducible audio and reviewed delivery. Use for a film or its production workflow; a research-only or niche-selection request does not start a film."
---

# Produce Pencil Animation

Run the requested production through the relevant work below. Resume from its actual state; existing scripts, accepted assets and user decisions remain inputs. The current brief determines subject, style, character construction, duration, aspect ratio, narration policy and tools. The reusable part is how decisions become editable, reviewable picture and sound.

## Locate and resume

In the user's Pencil workspace, read `AGENTS.md`, `README.md`, the selected production's brief and latest journal entries. Read `pipeline/README.md` for executable capabilities and the reference map. If the workspace is not available, obtain its location before writing a replacement project elsewhere.

Determine the requested deliverable and the earliest unresolved dependency that affects it. Reuse session authorization and settled creative choices. Ask only for a missing decision that materially prevents useful progress; routine revisions, internal quality checks and output generation do not create new approval gates. A request to explore or write a script remains that scope until production is authorized.

Preserve delivered revisions. Use a new versioned output directory for changes. Historical experiments supply mechanisms and evidence, not authority over a new film's art, timing or sound. Copy a useful helper only after reading its dependencies; older scripts import globals and definitions from other films.

## Plan picture and sound together

Write the film's brief and audiovisual script in its production folder. For each consequential beat, record: intended audience understanding, visible action, audible action, focus/emotional change, event or interval to synchronize, and a review question. Group ordinary repeated actions rather than writing a separate creative essay for each footstep. Use stable beat and shot IDs.

Establish the sound perspective, material character, degree of exaggeration, useful music, transitions and intentional quiet alongside the art direction. Explain precise information visually or with concise text when nonverbal sound cannot carry it. Read `research/audio-tools/sound-planning-method.md` when developing the sound treatment; it is methodological guidance, not a compulsory beat pattern.

When a film makes factual claims, verify its source event or mechanism before scripting the treatment and distinguish authored dramatization from fact. When fictional, label it accordingly. Football and educational exploration stay independent unless the user combines them. An approved brief can choose another subject entirely.

The script is ready to build when the important beats have coordinated picture/sound intentions, timing is plausible and required assets are identified. This internal completeness check is separate from any explicit user-requested script approval.

## Select assets and establish the treatment

Use references to establish the requested character, environment, readable silhouettes and sound palette. Image generation can supply designs, textures or backgrounds; rebuild or prepare the needed editable assets rather than treating a concept image as a finished rig. Use the relevant available image-generation tool/skill when creating raster artwork.

Audition actual sound candidates against rough poses and cuts early enough to change either. Match source to need: recorded material detail, controllable synthesis, or generated audio where it earns its extra effort. Consult the existing tool research only for the relevant category, and reverify volatile availability/licensing before acquisition or installation. Preserve source/license records and selected files. Temporary sounds remain marked as temporary until replaced or cleared for delivery.

Choose only the technical proof needed by unresolved risk. Reuse established motion when suitable; a new character or difficult action may need a short focused check. Do not impose a new proof film or a fixed sequence of beauty-frame approvals on every production. An animatic with useful sound can itself settle timing and comprehension.

## Author editable motion and resolve sound events

Build the scene and motion with the tool that best fits the brief, using Blender's editable assets for the current local workflow. Continuous movement, contacts and planted feet must be intentional; held poses and replacement drawings are valid when the style calls for them. Inspect contact through motion, not only one still. Separate draw order, camera motion, expressions, body motion and effects enough to revise the requested part.

Maintain one `production.json` using `pipeline/README.md`. Export named events from the authored animation timing into its shot records. The sound tool reads those events; it does not infer contacts from pixels. Cue records identify the selected audio, purpose, source onset, treatment and synchronization. Continuous sounds need their interval checked after movement changes. Shared code owns frame-to-sample conversion and stem assembly; each film owns its poses and cue selections.

Render selected audio through `pipeline/audio.py` into a new output directory. Use its stem and premaster outputs with Blender for preview. Sourcing, synthesis, AI inference and advanced processing produce ordinary selected files upstream of this command. Reuse these cached files when an edit merely moves the action. Extra processing tools are optional, chosen for a demonstrated sound need.

## Render, review and revise

Use the project's existing streaming Blender/FFmpeg rendering pattern, adapting paths, actual frame rate including `fps_base`, frame range, resolution and color treatment to this film. Save the native project with its dependencies and export a picture master. Keep a documented authoritative mix: Python/FFmpeg initially, or the selected DAW project if mixing moves there. Preview the same rendered audio rather than maintaining a second manually divergent mix.

Review the picture and sound together. Muted picture is a diagnostic for visual ambiguity, isolated sound for defects, and combined playback for the actual intended effect. Check representative contacts in successive frames, beginning/ending, transitions and other risky intervals; sampled stills alone do not establish motion quality. Listen on available playback systems and record which were actually used. If actual listening or an audience test was not performed, keep that result unknown.

Separate creative judgments from technical evidence. Verify format, frame count, duration, decoding, synchronization, sound presence, tails and the chosen loudness/true-peak specification after final encoding. Record expected quiet so silence is not automatically treated as failure. Technical success cannot certify comprehension, humor, emotional impact or “world-class” quality.

Revise the concrete failure, preserving unrelated accepted work. Select cues and variations explicitly so inserting an earlier cue does not randomize later selections. A timeline change reruns resolution; replacing an asset or processing changes its recorded hash. Never regenerate a chosen AI sound merely because a shot moved.

## Deliver and record

Deliver the requested playable movie or intermediate artifact, editable native project, necessary assets, separate stems, final mix, production plan, runnable film scripts and concise verification/reproduction notes. Package only what the task needs; identify missing or untested deliverables rather than declaring them complete. Publishing is a separate user-authorized action.

Use the existing `experiments/001_heavy_box/journal.py` helper for append-only events under the current production root. Record exact inputs/outputs, meaningful failures, selections, actual review results and tool/runtime versions; hashes identify files but do not replace versioned copies. The audio tool's resolved-cue record covers its own render; the production journal connects that render to the film.

Summarize the delivered behavior and evidence, remaining material limitations, and the next concrete action only when work remains. Keep new lessons scoped to the failure or capability they actually establish. Change this skill when repeated evidence changes the process, not to fossilize a successful film's creative choices.
