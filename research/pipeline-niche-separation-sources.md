# Shared workflow, creative profiles, and film choices

Research date: 2026-09-17. Scope: primary-source principles relevant to a flexible Pencil pipeline; no implementation or workflow changes.

## What the sources actually establish

| Primary source | Documented fact | Limited implication for Pencil |
| --- | --- | --- |
| [Blender Studio — Introduction](https://studio.blender.org/tools/pipeline-overview/introduction) | Documentation distinguishes design explanations from artist and technical guides. Department/workflow topics can be described at a high level and reference specific tools, add-ons, and workflows separately. | Keep the common production sequence understandable without embedding every renderer or animation technique in it. |
| [Blender Studio — Design Principles](https://studio.blender.org/tools/overview/design-principles) | Editorial and previs remain the reference point throughout production. The studio restricts add-ons to workflow/process-specific needs and documents infrastructure decisions in terms of its own production scale and tradeoffs. | Judge each film against its evolving edit and brief; choose technical machinery for actual production needs. These are Blender Studio's choices, not universal requirements for Pencil. |
| [Blender Studio — Asset Pipeline](https://studio.blender.org/tools/addons/asset_pipeline) | Productions can configure the number and contents of asset task layers. Optional hooks have production-wide or individual-asset scope. Published assets can retain older active versions when particular shots need them. | Reuse the process while allowing production-specific configuration and bounded exceptions. Record exactly which approved asset/reference version a film uses instead of silently replacing it. |
| [OpenUSD — Introduction, “USD can compose and override”](https://openusd.org/release/intro.html#usd-can-compose-and-override) | References assemble reusable assets; layers have an explicit strength ordering; downstream consumers can select bundled variants non-destructively. | Distinguish reusable definitions from the choices made by a particular film. Keep changes local unless they deliberately revise the reusable definition. |

These documents describe production systems and scene composition, **not a prescribed taxonomy of content niches or creative profiles**. The organization below is a recommendation inferred from their separation and reuse principles, combined with Pencil's stated needs.

## Minimal recommendation for Pencil

Use four responsibilities within the existing documentation and production folders:

1. **Shared workflow:** planning picture and sound together, evidence appropriate to the subject, readable action, review checkpoints, technical validation, delivery, and the production journal. State required outcomes; avoid making one niche, character design, or software technique a universal prerequisite.
2. **Production creative profile:** audience, editorial approach, visual language, sound/voice direction, selected reference families, and reusable assets for that production. Samtoons can contain its football and caricature direction here. A separate production can establish different choices without rewriting the shared workflow.
3. **Individual film selection:** its specific event or question, brief, references and versions, cast/assets, duration, treatment, sound plan, and approved deviations from production defaults. A film chooses only relevant resources; a profile is not a requirement to reuse every asset or style reference.
4. **Tool-specific implementation notes:** concrete Blender/Grease Pencil, rigging, compositing, rendering, audio, and validation instructions, consulted when the film uses that route. Technical support for a tool should not implicitly define the film's identity.

Use ordinary linked Markdown and the existing journal first. A short explicit record of profile, references, asset versions, and film-specific choices is enough; these sources do not establish a need for a registry, schema engine, plugin framework, USD migration, or asset database. Local creative choices refine defaults, while shared completion/review requirements remain applicable unless explicitly revised by the user.

Keep completed films and historical experiments intact. Promote a successful film's decision into a reusable profile only when it is intentionally selected for future work; folder names and accidental reuse are insufficient evidence of series intent.

## Access and confidence

OpenUSD's release introduction was opened directly (rendered as version 26.08). Blender Studio's official pages were available as substantial search-indexed extracts; direct browser-tool opens returned HTTP 402. The claims above stay within those retrieved extracts. This is architectural evidence and a proposed mapping, not a claim that the studios use Pencil's proposed four responsibilities verbatim.

## Pencil inspection: what exists versus what is proposed

Inspected `pipeline/skill/SKILL.md`, `pipeline/README.md`, `pipeline/styles/construction.md`, `pipeline/sound-planning-method.md`, `pipeline/checkpoints.py`, `pipeline/test_workflow.py`, `productions/README.md`, `productions/Samtoons/README.md`, and `CONTEXT.md`.

- The core already says a video's brief determines subject, treatment, duration and tools. It already has four creative checkpoints, including scoped delegation/waivers, and an improvement loop. Preserve these rather than creating a second workflow.
- `productions/README.md` already defines production context, versioned reusable assets, per-video plans and journals, and local snapshots of selected assets/context. This supplies most of the proposed profile mechanism today.
- `pipeline/README.md` explicitly limits current automation: style selection and sound resolution/mixing exist, while story, scene authoring, sourcing and creative judgment remain authored work. A flexible specification is not automatic technical support for arbitrary renderers or animation methods.
- The main skill embeds human-face/arm details and football examples. These are useful evidence, but detailed checks should live in relevant construction/domain guidance and be applied conditionally. A motion graphic without characters should not inherit an eye/nose clearance requirement.
- Samtoons' parent README mixes enduring identity with a dated 15 September restart status and a statement that 16:9 remains unselected. The later completed delivery makes these unsuitable as current resume guidance. Preserve historical statements in episode history; make the parent profile an evergreen source of applicable defaults.
- Ran `python3 pipeline/test_workflow.py` on 17 September 2026: PASS. This covers canonical skill installation, sibling review isolation, preservation of selected shared copies, and invalidation only when a video adopts a changed asset. It does not prove semantic profile resolution, visual quality, listening quality or multi-renderer support.

## Recommended ownership and applicability

| Responsibility | Existing owner / minimal extension | Examples and boundaries |
| --- | --- | --- |
| General production method | `pipeline/skill/SKILL.md` | Define audience intent; plan relevant picture/sound together; evaluate references; scope reviews; preserve accepted inputs; deliver editable work and inspect the actual export. Describe outcomes, not compulsory cartoon anatomy. |
| Reusable technique and execution | `pipeline/styles/construction.md`, `pipeline/sound-planning-method.md`, `pipeline/README.md`, existing helpers | Human-character anatomy, flat-art view limits, speech acting, procedural motion, Blender authoring and FFmpeg delivery. Apply a guide when the chosen medium/action needs it, across any niche. Keep hardware/runtime details out of creative identity. |
| Niche/domain expertise | Initially a clearly scoped section or linked guide in the relevant production | Football research and event reconstruction, player/club context, or scientific evidence and mechanism clarity. If multiple productions actually share this expertise, extract one shared domain guide then. Domain does not mandate humor, visual style or duration. |
| Production creative profile | `productions/<name>/README.md`, its selected benchmarks and versioned assets | Samtoons: audience, football parody, expressive caricatures, recurring personas, voice direction and approved reusable assets. A different football production can choose documentary treatment. |
| Individual video | Existing brief/script/`production.json`/journal/local snapshots | Actual story, learning objective or event; cast; views; sound; duration; aspect ratio; deviations from defaults; exact selected asset versions. No approval inheritance from siblings. |

This is a responsibility map, not a request to create five frameworks. User-facing model: one pipeline, a production profile, and a video brief. Tools and optional domain guidance support that model.

### Decisions must not collapse into one preset

Record independently where relevant: subject/domain; audience and purpose; production identity; standalone/series mode; visual treatment; format/duration; technical route. Football need not mean caricature, science need not mean a dry explainer, and a series need not imply continuing plot. The nineteen existing style options remain treatment references; they are not nineteen niches or nineteen guaranteed renderers.

### Resolution when a film starts or resumes

1. Read the user's actual current direction and existing scoped approvals.
2. Read the selected production context and that video's settled brief. Existing videos retain their adopted context snapshots and asset versions; a current parent change does not silently overwrite them.
3. For a new production, establish audience, purpose, evidence needs, visual/sound references and relevant constraints in its README. Ask only about material unknowns. Do not create unused assets or a new skill merely because the topic differs.
4. Select relevant domain and technique guidance from the actual story requirements. A no-dialogue diagram needs no TTS; a character comedy needs facial/acting review; a simulation needs an appropriate motion/physics review.
5. Record the effective choices and deliberate exceptions in the existing brief/plan, with selected copies and provenance. Specific authorized video choices refine production defaults. Conflicts with explicit user constraints require resolution, not silent guessing; unrequested deviations do not count as waivers of review.
6. Use the same applicable creative checkpoints, combining or scoping them according to the brief and established authorization. No extra checkpoint per profile or asset.

## How an episode teaches the larger system

Classify each finding before changing guidance:

- **General process failure:** early approval did not establish quality of expanded work. Core gets the rule to recheck changed inputs and demanding actions before propagation.
- **Technique failure:** a raised arm was distorted by head-proportion processing, or flat art was viewed edge-on. Relevant construction helper/guide gets the correction and a meaningful reproduction check. Apply anywhere that technique is used, not only football.
- **Domain requirement:** ball/boot contact and roles in a corner. Football guidance gets the domain detail; the general method retains the broader requirement for readable contact and supporting roles.
- **Production preference:** Samtoons' caricature identity, recurring voice/personality and comic exaggeration. Production profile owns it.
- **Episode-only decision:** Foden exiting a VAR door to fish. Keep it in this video's script; do not turn a successful gag into a compulsory format.

Fix the demonstrated issue first; preserve evidence and accepted work; adopt a reusable change at the smallest useful scope; verify the next actual use. Process guidance is not a substitute for correcting a defective shared helper. Conversely, a single film's workaround is not automatically a universal asset builder.

## Bounded implementation order (proposed, not executed)

1. **Clarify ownership without losing lessons.** Tighten the main skill into shared outcomes and conditional links. Move detailed human-character checks into the construction guide; keep evidence links and general review requirements. Add short definitions for domain and production profile to existing documentation if needed.
2. **Make Samtoons the first explicit profile.** Separate enduring direction from historical episode status, identify current selected references, and list only actual reusable assets with versions, tested actions/views and limitations. Preserve the original film and historical snapshots. Do not invent approval of every new asset merely because the final film was accepted.
3. **Strengthen selection/review records only where missing.** Reuse the current plan/journal and snapshot mechanism. Record applicable guides and resolved production defaults alongside video exceptions; add the smallest helper only for demonstrated repeated errors. Preserve independent picture/sound approvals and selective invalidation.
4. **Check flexibility with contrasting planning cases.** Use a Samtoons character-comedy brief and a non-football mechanism-explainer brief as disposable checks. Verify that each reads appropriate guidance, the second inherits no football/gag/voice defaults, and versions/approvals stay isolated. These are planning checks, not authorization to create another film or claims of demonstrated rendering quality.
5. **Extract reusable code selectively.** Inspect callers and dependencies before moving a film helper into the shared pipeline. Extract demonstrated general operations such as delivery assembly only when another actual use justifies it. Keep tool choice explicit; a new medium may require new implementation and a focused production-shot check.

No pipeline fork per niche, automatic profile-inheritance engine, new database, studio asset service, universal rig rewrite or USD migration is justified by this research. A specialized companion skill becomes useful only if a substantial repeated domain procedure needs independent invocation; it should reference the shared production workflow rather than duplicate it.

Success on subsequent productions means fewer repeated defects and avoidable revision rounds, correct context selection, preserved older deliveries and measured reductions in rework. No percentage savings, audience-performance improvement or cross-niche visual quality has yet been demonstrated.

This research pass created/expanded this report only. It did not change the active skill, production profile, helpers, assets or delivered films.
