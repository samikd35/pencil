# Pencil + Samtoons — revised animation improvement plan

22 September 2026 · Revision 002 · **Plan complete; implementation pending; visual improvement not yet demonstrated.**

This is the consolidated plan for the next implementation task. It supersedes the [v001 plan](../performance-workflow-v001/plan.md) and incorporates its [quality-target assessment](../performance-workflow-v001/quality-target-assessment.md) and the [Blender/Python research](../../../productions/Samtoons/research/python-animation-practice-v001.md). Those documents remain historical evidence, not additional plans to implement separately.

The user will provide the next story later. Complete the preparation in Phase A before asking for that story. Phase B applies and tests the improved method on the actual story. This plan does not start a film, select a cast, modify the delivered videos, remove models or change existing approvals.

## 1. Outcome and diagnosis

For Samtoons, the target is **expressive characters, exaggerated readable poses, excellent comic timing, deliberate camera work, attractive environments, coherent color/shading, convincing movement and purposeful reaction details**. Simple animation can meet that target. More drawings, more bones, smoother curves or a different Blender representation do not establish quality by themselves.

Keep one shared Pencil workflow, its four creative checkpoints, the working voice system, useful native construction and the existing audio/render tools. Improve the authoring sequence:

**Story intention → rough staging and performance → required artwork and controls → authored poses and transitions → finished visual treatment → reviewed sequence → expansion.**

The existing guides already contain many correct rules. The failure was also in execution: required performance capabilities were missing or insufficiently used, generic movement substituted for acting, and review evidence did not consistently cover the finished result. Repeating the rules alone will not solve this.

| Observed failure | Evidence-supported cause | Change at the responsible layer |
|---|---|---|
| Similar facing, resting hands and expressions across the cast | The [neutral source prompt](../../../productions/Samtoons/videos/002-how-arsenal-won-the-league/assets/neutral-cast-v021/football-prompt.txt) standardizes the presentation; reused helpers expose a limited performance range. | Separate a construction pose from a performance. Derive required views, expressions and hand actions from staged shots before finalizing assets. |
| Characters move without communicating thought or reaction | The [source diagnosis](../../../productions/Samtoons/videos/002-how-arsenal-won-the-league/research/acting-root-cause-and-next-production.md) identifies rest-based gestures, limited inspected face controls and repeated choreography. | Author attention, attitude changes, key poses and listener responses; then construct and time their transitions. |
| Connected limbs still look implausible; one repair breaks another quality | Simplified projection and endpoint checks cannot establish weight, silhouette, surface continuity or correct hand orientation. Multiple construction layers were sometimes changed together. | Diagnose the failing layer; preserve the accepted appearance, timing and mechanics together through the changed interval. Reconstruct only what cannot support the shot. |
| A technically passing shot remains weak animation | Existing [cast checks](../../../productions/Samtoons/videos/002-how-arsenal-won-the-league/scripts/check_cast_v021.py) explicitly do not judge acting. | Keep mechanical checks, but require actual performance and whole-scene review. A moving-control count is not creative evidence. |
| Reuse/resume can lose or select the wrong work | Current metadata contains competing selections; some builders depend on live registries and older script definitions. | Define the selected source and how corrections survive rebuilds; verify chosen reuse after save/reopen. |

The [film comparison](../../../productions/Samtoons/videos/002-how-arsenal-won-the-league/research/benchmark-audit-v001/report.md) also motivates broader composition, color, environment and editorial work. Its sampled-frame limitations remain: it does not establish every shot's motion or sound quality.

**Two separate completion claims:** Phase A can establish a prepared, more reliable workflow. Only Phase B's reviewed output can establish better animation. Neither documentation nor an API check proves benchmark quality.

## 2. Ownership and scope

| Owner | Responsibility |
|---|---|
| General Pencil workflow | Intention-to-assets handoff, visual treatment, authoring passes, source ownership, review evidence and learning. Remains usable for non-character and non-comedy films. |
| Shared technique guides/helpers | Drawing/deformation choices, facing, anatomy, contacts, timing, runtime compatibility and reusable mechanisms where demonstrated. |
| Samtoons profile | Recognizable football caricatures, channel identity, comedy performance, football environments and chosen benchmark comparisons. |
| Individual film | Story, cast, factual/fictional treatment, visual choices, exact shot designs, adopted asset versions, sound and approvals. |

Do not turn named players, old jokes, a fixed eight-second test or one earlier rig into requirements for future stories. Preserve the best evidence from Videos 1 and 2 without declaring either entire film the target. Their known weaknesses remain explicit.

## 3. The production method to implement

### 3.1 Stage the meaning before final asset generation

Use the existing audiovisual script and shot plan. For a consequential beat, record the audience's intended understanding, the trigger, starting state, response and ending state. Add the focus/camera, required views, meaningful poses, contacts, timing relationship to sound, missing asset capabilities and the preview that tests them. Group routine repeated actions; do not write a new record for every blink or footstep.

For character scenes, include body/head facing, gaze target, emotional change and relevant listener behavior. For other subjects, describe the corresponding visible state change without imposing human acting.

Rough layouts should resolve readable silhouettes, overlaps, scale, screen direction, eye-lines, negative space, opening/closing composition and the reason for a cut or camera move. Test the visual cause and response with temporary shapes/drawings before investing in detailed surfaces. Cinematic staging can use a held camera.

Keep these decisions in existing prose or permitted top-level creative metadata. Preserve the strict shot/event/cue contract in `audio.py`; do not invent another planning database.

### 3.2 Make image generation serve the intended performance

Declare the purpose of an image request:

| Purpose | What the result must supply |
|---|---|
| Identity/design | Coherent head-to-toe character, recognizable features where required, silhouette, proportions, clothes, shoes and finish. |
| Construction | Source view, separable components, hidden surfaces and registration suitable for the selected rig or native reconstruction. |
| Performance | The actual view, expression, hand shape, contact pose or transition drawing required by the scene. |

One drawing may serve several purposes. A neutral sheet alone does not demonstrate expressive range. Prompts come from the staged performance and chosen identity, not directly from dialogue or a universal cast template. State whether an image is reference-only or intended as renderable artwork.

Inspect outputs before fitting: likeness, complete silhouette, anatomy, pose meaning, hand/prop relationship, support, view consistency, markings and missing/repeated phases. The [rejected chase sheet](../../../productions/Samtoons/videos/002-how-arsenal-won-the-league/assets/chase-poses-v002/inspection.json) demonstrates why prompt compliance cannot be assumed. Correct the failed component or change its construction; repeatedly regenerating larger sheets is not a production method.

Choose the representation for the complete shot, including camera and shading demands:

- Use rigged native/vector/mesh or prepared illustrated surfaces where deformation preserves the required form.
- Use authored Grease Pencil drawings or coherent replacement components/poses where the view, expression, silhouette or contact cannot deform convincingly. Ordinary acting can need replacements too.
- Combine methods only when line, proportion, palette and motion continuity remain coherent. A detailed head on an unrelated body does not pass.

A fixed three-quarter face cannot become a profile through in-plane rotation. A wrong palm cannot be corrected merely by aiming its wrist. A static whole-character image cannot substitute for the required performance. Conversely, an intentional held drawing can be expressive when its placement and transitions serve the beat. Do not mandate a conversion of every asset to one backend.

### 3.3 Author shots in explicit, revisable passes

| Pass | Creative work | Codex/Python/Blender execution |
|---|---|---|
| Layout and treatment | Design the visual focus, set, palette/value structure, coverage and depth. | Place simple geometry/drawings, cameras and props; make rough composition previews and representative look frames. |
| Key performance poses | Choose the attitudes and changes that communicate the thought/action. | Set authored native drawings or controls at selected frames. Keep deliberate holds; do not begin with generic oscillation. |
| Breakdowns and mechanics | Design arcs, support, acceleration, overlap and contact between those poses. | Author trajectories, contact intervals, constraints and corrective/replacement drawings; inspect evaluated surfaces. |
| Face/body and editorial timing | Coordinate eyes, expression, body response, spoken stresses, pauses and cuts. | Adjust keys, exposure, curve handles and offsets; move sound events with the authored action. Do not smooth away comic accents. |
| Secondary action | Add motivated listener reactions, hands, clothes, props, crowd or impact details that support focus. | Author selected variations and follow-through. Avoid universal blink clocks or constant activity. |
| Cleanup and final look | Remove distracting defects; establish consistent contours, shading, contact shadows and shot-to-shot color. | Fix joins, masks, pops, slipping, intersections, layers/materials/compositing and final camera framing; review the edit again. |

These are authoring passes, not six new approval gates or an inflexible waterfall. Revise earlier decisions when later evidence exposes a problem. Finish performance before spending heavily on polish, while establishing enough of the look early to reveal construction limits.

Python implements artistic decisions and repetitive operations. It can insert keys, construct drawings, operate rigs, manage cameras/materials and produce previews. It cannot supply missing acting choices merely by interpolating endpoints. Codex remains responsible for designing, observing and revising those choices.

### 3.4 Make artwork, environment and finish one visual treatment

Use a compact section of the film's existing staging material to show characters and environment together: line/shapes, proportions, palette/value hierarchy, shading/light intent, scale, foreground/middle/background, contact and camera language. Do not accept separate attractive sheets as proof that the scene works.

Choose drawn shading, flat color, masks or scene lighting according to the selected medium. Lights cannot automatically relight shadows baked into an unlit image. Check adjacent shots for consistent value, color, shadows and spatial relationships. Depth should aid staging through perspective, occlusion, scale and suitable parallax; detail or camera drift is not a substitute.

For Samtoons, record the selected football world layout and relationships: pitch markings, goal and corner positions, player scale, ball size, contact and trajectories. Follow current story exaggerations deliberately rather than accidentally changing the world's geometry. Reuse a setting consistently across scenes that share it.

## 4. Technical reliability without a new engine

### Preserve corrections through rebuilds

For each changed asset/shot, identify its authoritative authoring source in the existing plan/reproduction notes:

- If the builder owns the animation, approved keys, drawings and corrections must be represented in its selected inputs/code.
- If the saved `.blend` owns the animation, subsequent scripts must operate on that selected file without destructively regenerating the corrected parts.
- If ownership is divided, name the boundary, such as builder-owned environment and file-owned character action. Do not let two sources independently overwrite the same property.

After a relevant correction, save/reopen and rerun the intended next operation on a versioned copy. Compare the corrected interval. A manual improvement lost on regeneration is not a completed repair. Live `driver_namespace` state is not a portable asset until the documented loading route recreates it.

### Validate only the mechanism being adopted

Read all callers before changing a shared helper. Reuse existing keying, contact, audio and render mechanisms first; extract a narrowly useful helper only when actual reuse warrants it. No universal rig, expression engine or 360-degree asset library is planned.

The [runtime research](../../../productions/Samtoons/research/python-animation-practice-v001.md) observed Blender 5.2.0 LTS, but one background inspection crashed before its Python code executed. The cause is unknown. During implementation, verify the selected authoring connection and a minimal preview/save/reopen route safely before relying on it. A failed headless launch does not by itself prove a drawing API is broken or require a renderer migration.

Before adopting a new API path, test that path in the installed runtime. Respect Action slots/channelbags and current Grease Pencil drawing/fill APIs; older examples are not automatically compatible. Do not describe mesh shape keys as native Grease Pencil shape keys. A two-bone or IK solver supplies geometry, not weight transfer, appealing poses or comic timing.

### Keep current selections unambiguous

The existing plan/journal must distinguish selected script, picture, sound, native source, checkpoint revision and delivered export from historical entries. Bind the actual dependencies of a review; the current guard checks declared hashes, not undeclared dependencies. Fix caller selections before extending a guard. Change executable infrastructure only for a demonstrated gap and add the smallest meaningful regression check.

Preserve finished packages and their provenance. Clarifying how to resume work is not a reason to retrofit gates, rebuild films or rewrite their historical approvals. Keep voice models, selected voice references and usable cached audio intact.

## 5. Acceptance evidence: judge the whole result

Use this matrix within existing reviews. Each applicable row needs an observed result, an exact artifact/interval and any unresolved gap. It is not an automatic score or a claim that every frame needs every effect.

| Quality target | Evidence to inspect |
|---|---|
| Strong art direction | Characters and setting feel like the same world at intended viewing size; line, palette, shape and shading choices agree. |
| Excellent character design | Recognizable and expressive silhouettes/faces where required; coherent proportions, clothes and shoes survive different poses. |
| Natural expressive movement | Actions have motivation, weight, anticipation, contact and recovery appropriate to the style. |
| Great timing | Holds, fast changes, reactions, overlap and cuts fit the joke and selected sound; movement does not default to slow motion. |
| Strong poses and facial expressions | Key poses communicate thought; gaze, lids/brows, mouth and body agree through the transition. |
| Cinematic composition | Clear focus, purposeful shot sizes/cuts, readable overlaps and screen direction; camera choices reveal or follow meaning. |
| Professional color and lighting | Controlled palette/value hierarchy and intentional shading/light; adjacent shots remain coherent. |
| Depth and environment | Perspective, scale, layers, occlusion and grounding convince in the actual camera. |
| Clean animation | No accidental contour changes, disconnected surfaces, pops, sliding, jitter, mask errors or inconsistent shadows. |
| Visual storytelling | The important cause and response read visually; dialogue adds information rather than concealing missing action. |
| Attention to small details | Relevant listeners and secondary elements respond purposefully without distracting or moving mechanically in unison. |
| Distinctive style | The combined drawing, staging and comedy feel like Samtoons; benchmarks inform craft rather than replacing the channel's identity. |

Review normal-speed playback for acting and timing, successive frames for contacts/transitions, and native-size crops for construction. Review the surrounding cut and combined sound after local fixes. Muted playback is a diagnostic, not a demand that the entire intended audiovisual film work silently.

Record what was actually viewed/heard. Screenshots, a launched player, hashes and loudness checks are not evidence of full playback or listening. Use an independent reviewer for the representative sequence where available, with the same disclosure of limits. Provide the user a playable artifact for qualities the agent cannot establish.

For a repair, state the failed property and accepted properties to preserve. Compare equivalent framing/speed, including entry, peak, recovery and affected adjacent shots. Verify likeness, connected construction, expression, motion, contact and sound relationship together. A regression in another required quality keeps the repair unresolved; a new user direction is a separate scoped change.

## 6. Phase A — implement before the next story

All items below are **pending**. They produce a prepared workflow and a concise implementation record, not a speculative film.

| Work package and order | Concrete changes / existing owners | Done when |
|---|---|---|
| **A1 — Consolidate authoring guidance** | Update `pipeline/skill/SKILL.md`, `pipeline/styles/construction.md` and `pipeline/motion-planning.md`. Integrate Sections 3–5; remove repeated/competing prescriptions. Keep process in the skill and detailed techniques in their guides. | The workflow carries an intention into actual artwork, authored performance, look and review; ordinary acting and hard mechanics are both covered where relevant. No extra approval gate or niche requirement enters the general core. |
| **A2 — Make selection and correction ownership reliable** | Update execution guidance in `pipeline/README.md`, adoption conventions in `productions/README.md` and stale root `README.md` descriptions. Document rebuild ownership and review bindings. Trace affected callers before any executable fix. | A reader can identify the current source and preserve corrections. A bounded check on a safe copy confirms the selected existing preview/save/reopen route; failures are resolved or precisely recorded as blockers to that route. Run existing workflow tests; extend code only for demonstrated failures. |
| **A3 — Consolidate Samtoons standards and evidence** | Revise `productions/Samtoons/README.md`; create the next benchmark revision from `benchmark-v002.md`; version the existing reuse catalogue only as needed to index useful accepted assets and limitations. Preserve old snapshots. | The next film can find the visual target, benchmark excerpts and relevant reusable sources without reconstructing the chat. Records distinguish references, scene-bound artwork, portable mechanisms and actual tested capabilities. No new cast is assumed. |
| **A4 — Review the prepared workflow** | Use the existing pipeline journal and a compact implementation review beside this plan. Check local links, canonical skill ownership, file selections and applicable regression results. | A1–A3 changes and unresolved limits are explicitly reported. No new artwork or benchmark-level performance is falsely claimed. The next step clearly requests the user's story. |

A2 and A3 can proceed independently after the ownership decisions in A1. Preserve prior artifacts and record the relevant before/after versions. Avoid bulk copying old assets, cleaning unrelated files or building an unused library.

Existing checks to rerun for the implementation where applicable:

```sh
python3 pipeline/checkpoints.py --self-test
python3 pipeline/test_workflow.py
python3 pipeline/pose_geometry.py
```

These already passed in the earlier audit; that historical pass is not a test of future edits. They establish workflow/geometry behavior, not creative quality. A native runtime check must also state its exact selected file, operation and observed result. New story-specific controls can wait until the story needs them.

### Samtoons-specific adoption details

The new benchmark record should retain the established A/B references and incorporate the [additional Short study](../../../productions/Samtoons/research/reference-ijvy-v001/analysis.md), with its limited sampling and unknown original software stated. Compare relevant excerpts for acting, staging, transitions, environment and finish; do not force every reference device into every shot.

Carry forward Video 1's whole-character coherence and Video 2's accepted motion, contact and construction improvements as scoped evidence. Also carry forward Video 2's repetitive acting as an unresolved weakness. Reuse artwork/controls separately from animation: a reused character needs a performance suited to the new situation.

For comedy, build contrasting attitudes, escalation, reactions and readable pauses. Hands must perform their role—point, grip, listen, reject—rather than default outward. For dialogue, keep each speaker's selected voice identity and direct emotional intention; preserve the existing sound-planning method and voice runtime. The user's future brief governs factual versus fictional treatment and all other story choices.

## 7. Phase B — apply and validate after the user supplies the story

1. **Develop the actual treatment and rough full-story timing.** Resolve premise, visual opportunities, consequential beats, roles, likely coverage and sound intention in the normal brief/script process. Use rough staging to expose ambiguity early.
2. **Select a small representative sequence from that story.** Cover ordinary acting/interaction, a meaningful transition/camera relationship and the intended environment/look. Include demanding physical mechanics if the story needs them. Choose sufficient coverage, not a predetermined duration or old cast.
3. **Build only the needed missing artwork and capabilities.** Follow the authored passes; produce a finished representative portion that tests the whole quality matrix. Use matching rough coverage around it so cuts, continuity and pacing can be judged. Use provisional or selected sound appropriate to the current checkpoint, and recheck consequential timing against the selected sound.
4. **Compare and revise before propagation.** Use comparable benchmark moments and the strongest relevant prior work. Diagnose any weak result at staging, drawing, controls, mechanics, timing, look or edit. Preserve the other accepted qualities. A bland performance remains unresolved even when every technical test passes.
5. **Expand to the complete inexpensive animatic and then the film.** Reuse proven construction with new authored performances. Review newly introduced views/actions and relationships; earlier approval is not blanket validation of a whole cast. Render the full-quality film after the existing animatic decision.
6. **Adopt demonstrated improvements.** Record what worked, its scope, known limits and reproduction route in the existing profile/guide/helper at the appropriate level. Compare recurring defects and actual revision effort; mark unmeasured time/cost unknown. Remove ineffective prescriptions rather than accumulating every experiment as a rule.

### Retain the four existing creative checkpoints

| Checkpoint | Revised evidence within the existing decision |
|---|---|
| Story and staging | Audiovisual script, rough layouts, unified visual treatment and representative finished performance evidence covering the actual risks. Short proofs remain permitted; this does not authorize a full-film quality render. |
| Sound direction | Actual playable candidates in context and selected vocal/music/effects intention, or intentional silence. Can be combined with staging when one artifact answers both. |
| Combined animatic | Complete inexpensive cut with actual coverage, performances/blocking, captions and selected sound. Judge rhythm and continuity across the film. |
| Delivery review | Exact encoded movie, honest playback/listening results, technical checks and remaining limitations. |

User acceptance or an explicit scoped delegation/waiver remains governed by the current skill. Internal authoring passes and regression checks do not create additional permission requests. Changed inputs reopen only affected decisions.

## 8. Research support and remaining uncertainty

The technical route is plausible and supported by professional practice:

- [Il Baracchino's production account](https://www.blender.org/user-stories/creating-il-baracchino-italys-first-adult-animated-series-made-with-blender/) describes mixed-media previz, camera/blocking/lighting intent and shot-specific rigs. It supports planning around the shot, not an autonomous Python claim.
- [Blender Studio's animation account](https://studio.blender.org/blog/sprite-fright-animation-tips-learned-hard-way/) supports reference, deliberate blocking and refinement; its 3D style is not a Samtoons requirement.
- [Blender Studio's lighting workflow](https://studio.blender.org/tools/pipeline-overview/shot-production/lighting) connects color/key-shot planning and continuity with technical tools, including Python overrides.
- Animation Mentor's [facial animation](https://www.animationmentor.com/blog/facial-animation-101/) and [polishing guidance](https://www.animationmentor.com/blog/tutorial-how-to-polish-your-animation/) support motivated expression/gaze, separate timing and refinement without indiscriminate smoothing.

The linked [technical research](../../../productions/Samtoons/research/python-animation-practice-v001.md) contains official API references, version distinctions and access/testing limits. Research establishes mechanisms and useful practice; it does not prove the new Codex-authored sequence will meet the benchmark. The remaining risk is artistic execution and reliable evaluation, which Phase B must test visibly.

**Next action:** implement Phase A. Once its completion and any limitations are reported, receive the user's next story and begin Phase B. Do not request the story merely to finish this preparatory work.
