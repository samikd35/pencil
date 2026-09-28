# PyBlend v1 Animation Authoring

## Destination

Produce an approved, evidence-backed, implementation-ready PyBlend v1 product
and architecture specification for a local, Codex-driven workflow that enables
a Creator to turn approved stylized 2D references and written or multimodal
direction into a short, editable Blender Grease Pencil Shot with layered 2.5D
staging, approval checkpoints, targeted revisions, locks, reproducible history,
and explicit failure handling.

## Notes

- This map resolves product, evidence, and architecture decisions; it does not implement the production framework.
- Use the vocabulary in [`CONTEXT.md`](../../CONTEXT.md), especially Creator, Shot, Character Asset, Environment Asset, Motion Brief, Lock, Targeted Revision, and Adopted Edit.
- Consult `/grilling` and `/domain-modeling` for human decisions, `/prototype` for concrete proof gates, and `/research` for external runtime, packaging, and licensing facts.
- Experiment 001 is frozen evidence. Orient from the [final report](../../experiments/001_reference_locked/results/experiment_001_report.md) and [verdict](../../experiments/001_reference_locked/results/final_verdict_v1.json); do not rerun or replace it.
- Standing direction from exploration: local Codex orchestration, Blender-side Python execution, 24 fps by default, a short Shot as the authoring unit, hybrid rig/drawing animation as a hypothesis, and layered 2.5D rather than visible 3D reconstruction.
- Ticket 05 reopened the Character Asset proof after whole-image pose interpolation exposed missing semantic isolation. The later V4 proof resolved static ownership but not animation-ready correspondence, so Ticket 04 is claimed again and Ticket 05 is paused behind it.
- V3 is Creator-rejected: coordinate-based weights on a whole-character drawing cannot prove arm ownership and still expose foreign/background-looking geometry. The completed reference-film research gate selects a drawing-led hybrid for v4: approved pose/exposure states, explicit semantic layers, bounded same-topology deformation, hand substitutions, pose corrections, and keyed local occlusion. Ticket 05 remains blocked until that proof is clean and Creator-approved.
- V4 now uses committed Semantic Part masks, real under-head Hidden Artwork, explicit depth, and an independently declared Motion Envelope. Static reconstruction, all 36 Blender exposure frames, a 33-sample bounded sweep, a hand-only edit, and a retime passed their technical rejection gates and received explicit Creator approval on 2026-09-04.
- Ticket 05 run 4 is Creator-rejected: it preserved structural ownership and Locks but produced only 21 unique images across 120 frames, with static holds, one-frame pose changes, and remaining deformation/disconnection defects. Ticket 05 stays active behind a new research and single-interval proof gate; Ticket 06 must not start yet.
- The completed Strategy V2 research gate closes V6 as rejected rather than patching it again. V6 copied the contour/TPS fragment of the evidence while omitting fixed skeletal proportions, shared deformation geometry, correctives, and explicit occlusion/topology state. The replacement foundation is a certified semantic 2.5D Character Package tested on two characters and four motion classes before another Shot motion attempt.
- The backward Ticket 04 audit also found concrete bad ownership: V4 sleeve masks included fixed torso/hip pixels and the fixed body retained a 453-pixel arm fragment. A versioned V5 candidate repairs the seam, adds one completed torso underlap, and passes the 13-frame automatic topology/joint/alpha gates. Creator review is still pending, so Ticket 04 remains claimed.
- Direct Blender Python executed through isolated background CLI jobs is the production integration. Saved `.blend` files, renders, logs, and validation manifests are the observable outputs; MCP is deferred to optional live inspection or debugging.
- Current research priority is repeatable visual quality and reuse at multi-Shot scale. Cost and elapsed-time optimization are deferred until the Character Asset representation passes; a fast or cheap result with a bad joint does not pass.
- The Creator-selected quality benchmark is B/R Football's seven-minute *That was one wild transfer window*. Success means matching its observable line stability, clean silhouettes and overlaps, readable authored poses, controlled exposure timing, and stable character identity—not copying its art style. The same bar applies to every case in the two-character/four-motion matrix and the longer reuse test; per-frame repair is not scalability.
- Local Markdown is canonical; synchronize the map and tickets through ordinary Git.

## Decisions so far

<!-- Closed-ticket pointers go here. -->

- [Lock the first PyBlend v1 Shot contract](issues/01-lock-the-first-v1-shot-contract.md) — v1 anchors on a solo Creator producing a 3–8 second, one-character, flat-color, 2.5D Shot delivered as an editable `.blend` and 1080p MP4.
- [Define the v1 input envelope and refusal rules](issues/02-define-the-v1-input-envelope.md) — v1 accepts a small local package of clean character and environment artwork plus a Motion Brief, limits optional direction references, and refuses unsupported inputs before production.
- [Define faithful and editable animation success gates](issues/03-define-authoring-success-gates.md) — an Approved Shot must pass independent identity, style, motion, staging, editability, Lock, effort, and delivery gates backed by automatic evidence and explicit Creator approval.
- [Prove a reusable Character Asset](issues/04-prove-a-reusable-character-asset.md) — V6 is closed as rejected after exposing a 73% arm-length drift and an uncovered shoulder corridor. The next proof certifies two semantic 2.5D Character Packages, then runs the same compiler across four bounded motion classes; Ticket 05 remains blocked.

## Not yet specified

- Multi-Shot continuity, asset evolution, and story-to-movie orchestration after the first Shot contract is proven.
- Dialogue, lip-sync, sound design, multiple interacting characters, and advanced camera movement where the first Shot contract does not require them.
- Exact production module boundaries and verification fixtures until the character and environment proof gates expose the real seams.
- A polished Blender add-on or dedicated application after the Codex-driven workflow reveals stable repeated controls.
- The ordering and numbering of any new experiments until the input, character-animation, and 2.5D proof questions are resolved.

## Out of scope

- Production implementation while this Wayfinder map is active.
- Repeating, modifying, or replacing frozen Experiment 001 evidence.
- Visible reference-to-3D model or environment reconstruction.
- Hosted/cloud execution and render-farm infrastructure for v1.
- Delivering a complete multi-scene movie in v1; that remains the Movie-Creation North Star.
