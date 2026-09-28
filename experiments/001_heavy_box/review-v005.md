# Stronger push — controlled revision

[Updated 10-second preview](artifacts/rough-v005/preview.mp4) · [Before / revised comparison](artifacts/rough-v005/before-after.mp4) · [Editable Blender project](artifacts/rough-v005/character-and-motion.blend)

The user liked v003 and authorized continuation. This pass deepens the second-push crouch, adds a short anticipation hold, drives forward faster and strengthens the effort expression. Both recovery hands now clear the head. The character, camera, duration and silent format remain the same.

## What the revision test proves

All **136 protected frames**—opening 1–88 and ending 193–240—are pixel-identical to v003. These frames were rendered again from the revised Blender project, not copied from the old output. **90 frames changed**, all inside the permitted 89–192 window. [Comparison evidence](artifacts/rough-v005/revision-comparison.json).

All 240 evaluated frames pass the saved-project contact, foot-plant, limb-attachment, framing and release checks. The recovery check additionally confirms that mitten contours remain outside an expanded head ellipse during frames 154–179. This checks hand clearance, not every possible limb occlusion. [Project verification](artifacts/rough-v005/verified-project.json).

The video remains 1280×720, 24 fps, exactly 10 seconds, with no audio. [Video metadata](artifacts/rough-v005/verified-video.json).

## Visual review and limits

Inspected full-size anticipation, effort and recovery renders, the chronological contact sheet and a two-frame-step recovery sequence. The larger anticipation-to-push contrast reads clearly, and the hand silhouettes have more separation. The far arm still passes behind the head as it rises; this is not a fully unobstructed silhouette.

This remains a rough animation proof. The unchanged walk still deserves a separate timing pass. Final production-quality acceptance and user preference between the two versions are not inferred from technical tests.

## Recorded findings for the eventual pipeline

- Shot-specific timing and poses can change while character-construction code remains the same apart from versioned input/output paths. These are immutable experiment snapshots, not a finished shared animation framework.
- A bounded revision can protect unrelated rendered pixels. Use decoded pixels for this comparison: Blender embeds different file paths, dates and render times in PNG metadata. Complete-file hashes still identify the exact archived artifacts.
- Sparse stills missed a two-frame hand-edge graze in v004. The continuous clearance check found it; v005 corrects it. Both the failed version and checker results remain in the journal.

Sources: `shot-v005.json`, `scripts/build_v005.py`. Checks: `scripts/verify_v005.py`, `scripts/compare_v005_pixels.py`. Export recipe: `scripts/encode_v005.sh`. Render-file hashes: [manifest](artifacts/rough-v005/frames-manifest.json). Earlier artifacts and reviews remain intact.

The next useful reuse test is a different action with this character. That would show which controls and construction methods generalize before extracting a shared pipeline or skill. It has not been started in this revision.
