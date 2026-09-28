# Pencil and Samtoons — performance workflow improvement plan

22 September 2026 · **Proposed, not implemented or creatively validated.**

Scope: improve the existing general pipeline and Samtoons profile before the next production. This document does not start a film, choose its cast, revise either delivered video, or change an approval. The next idea determines its own characters, duration, style exceptions and representative scenes.

## Recommendation

Keep the existing production structure, four creative checkpoints, selected voice runtime, useful construction methods and render/audio tools. Repair the handoff from **story intention → staged performance → required artwork → editable controls → reviewed shot**.

The pipeline already states many correct principles. Video 2 demonstrates that recording those principles and moving several controls did not ensure their execution. The priority is to make each consequential intention visible in an actual shot before extending its construction across the film. Better illustration alone, extra interpolation, automatic blinking or conversion to Grease Pencil cannot supply that missing performance.

This is a plan for a better production method, not a claim that benchmark quality has already been achieved.

## 1. How the system works today

| Layer | Current owner and actual role |
|---|---|
| Shared workflow | [Authoritative skill](../../skill/SKILL.md), reached through `pipeline/SKILL.md` and the installed skill link. Coordinates planning, construction, sound, checkpoints and learning. |
| Production context | [Production conventions](../../../productions/README.md), [Samtoons profile](../../../productions/Samtoons/README.md) and [benchmark v002](../../../productions/Samtoons/benchmark-v002.md). Supply defaults; individual films retain adopted context and exceptions. |
| Creative planning | Film-local brief, versioned audiovisual script and `production.json`; selected context/reference snapshots under the film's assets. |
| Artwork and animation | Film-local image prompts, generated/edited drawings, Blender assets and Python builders. There is **no general performance engine or portable universal character rig**. Video 2 uses fitted illustrated meshes, native rigs/vector geometry, facial controls and matched action drawings. |
| Shared executable tools | `styles.py` pins visual selections; `audio.py` resolves selected assets against authored events; `qwen_voice.py` supports speech generation; `pose_geometry.py` supplies optional planar geometry. These tools do not direct acting. |
| Review | `checkpoints.py` verifies recorded user acceptance or explicit waiver and hashes of declared review inputs/outputs. It does not know whether an unlisted dependency changed or whether an expression communicates the scene. |
| Delivery | Film-local render/edit/mix scripts, source-bound caches, saved native projects, encoded checks and journal records. Video 2's v027/v029 packages identify the delivered sources and reproduction route. |

The intended flow is already brief/script → staging and sound decisions → combined animatic → full render → delivery review. The implementation relies on Codex making and preserving the artistic decisions at every transition. It is not an automatic script-to-animation application.

### What the audit established

| Finding | Evidence | Consequence for the plan |
|---|---|---|
| Source drawings predisposed the cast to identical presentation. | [Neutral cast prompt](../../../productions/Samtoons/videos/002-how-arsenal-won-the-league/assets/neutral-cast-v021/football-prompt.txt) requests the same neutral stance, camera-right three-quarter head and lowered arms. | Keep neutral construction drawings where useful, but distinguish them from the artwork needed to perform a scene. |
| A detailed prompt did not ensure correct movement drawings. | [Rejected chase-sheet inspection](../../../productions/Samtoons/videos/002-how-arsenal-won-the-league/assets/chase-poses-v002/inspection.json) records repeated leg phases despite explicit opposite-stride instructions. | Inspect generated poses and anatomical landmarks before fitting or propagating them. Prompt compliance is not evidence. |
| The principal reused helpers had narrower capabilities than the scenes required. | [Source diagnosis](../../../productions/Samtoons/videos/002-how-arsenal-won-the-league/research/acting-root-cause-and-next-production.md): in-plane head rotation; limited inspected face controls; rest-pose-based gestures; simple knee projection; repeated celebration choreography. | Extend only the capabilities the chosen shot needs, and author a new performance rather than copying a generic cycle. |
| Useful technical checks could pass weak acting. | [Cast check](../../../productions/Samtoons/videos/002-how-arsenal-won-the-league/scripts/check_cast_v021.py) checks bones, moving controls, preserved leads/audio and contacts, explicitly excluding artistic quality. | Preserve these checks and add actual performance evidence at the existing review, not a higher moving-control quota. |
| The guides already contain facing, gaze, anatomy and normal-speed review requirements. | [Construction](../../styles/construction.md), [motion planning](../../motion-planning.md), [skill](../../skill/SKILL.md). | Consolidate and connect the rules to working artifacts; do not append another disconnected checklist. |
| Resume metadata can point in several directions. | Video 2's [plan](../../../productions/Samtoons/videos/002-how-arsenal-won-the-league/production.json) still says `rough_cut_in_batches`, 5,954 timeline frames and `selected_script: script-v004.md`, alongside `current_script: script-v008.md`, a delivered 6,994-frame v029, and older `rebuild_required` entries. | Make the active selection unambiguous for new work. The correctly documented delivery is preserved; this is a state-management weakness, not proof of a corrupted movie. |
| Some authoring reuse depends on live session state and old scripts. | [Final-batch builder](../../../productions/Samtoons/videos/002-how-arsenal-won-the-league/scripts/build_final_v023.py) uses `bpy.app.driver_namespace` registries and extracts an earlier function via AST. | Prove selected reuse after save/reopen. Extract only the needed helper when a new shot actually needs it, rather than extending a chain of episode builders. |

The earlier [finished-film comparison](../../../productions/Samtoons/videos/002-how-arsenal-won-the-league/research/benchmark-audit-v001/report.md) and [supplemental reference study](../../../productions/Samtoons/research/reference-ijvy-v001/analysis.md) supply visual evidence. Their sampling and listening limitations remain in force. This audit traced documents, prompts, scripts, selections and journal records; it did not add a new full-speed film or audio review.

## 2. General pipeline changes

### A. Make the existing beat/shot plan drive construction

Before detailed asset generation, block the consequential scene changes in rough form. Extend the existing audiovisual beat entry with the performance information needed by that shot:

| Record once in the shot plan | Why it matters |
|---|---|
| Audience understanding and triggering event | Establishes what changes and why. |
| Starting state → noticed event → response → ending state | Gives the performance a causal sequence. For a mechanism this can be a physical state change, without imposing human acting. |
| Viewer focus, camera coverage and screen direction | Determines what must read and which subject views are actually needed. |
| For characters: body/head facing, look target, expression and relevant listener response | Prevents camera-facing resting art from substituting for interaction. |
| Key poses, contacts and purposeful holds | Defines the motion before interpolation; connects acting to body mechanics. |
| Selected sound/phrase event and intended timing relationship | Connects a gesture or reaction to the moment, without requiring every movement to hit a syllable. |
| Required asset capability, existing support and missing work | Makes the artwork/control decision follow the scene. |
| Actual preview/frame interval and observed result | Connects the intention to evidence rather than an unchecked prose promise. |

Use one compact entry per meaningful beat and group repetitive actions. Store prose in the existing script/shot plan or permitted top-level creative metadata. Do **not** add arbitrary fields inside `audio.py`'s strict shot/event/cue records or build a second planning database.

### B. Separate artwork purposes before writing image prompts

Image generation remains useful. Give each request a declared role:

1. **Identity/design:** coherent complete-character appearance, likeness, proportions, clothes, shoes and finish.
2. **Construction:** an appropriate source view, separable limbs, needed hidden surfaces and anatomical registration for the selected rigging method.
3. **Performance:** the particular expression, view, hand shape, whole-body pose or transition drawing demanded by the shot.

One image may serve more than one role if it actually meets them. A neutral sheet supports construction; it is not proof of expressive range. A dramatic action drawing is not automatically a deformable neutral base.

Derive prompts from the shot requirements, not directly from dialogue text. Carry the chosen identity reference, required view, action intention, expression, silhouette, hand/prop relationship, support foot where relevant, and continuity constraints. Identify whether the result is reference-only or intended to become rendered artwork.

Inspect actual outputs for identity, pose meaning, anatomical ownership, repeated/missing phases, cropping, transparency, markings and continuity with adjacent drawings. Repair a specific failed component or use native construction when appropriate. Repeatedly requesting a larger all-purpose sheet is not the default recovery method.

### C. Review the major performance risks, not just the largest movement

Keep the existing staging checkpoint. For a character film with dialogue and physical action, its evidence must cover **ordinary acting/interaction and demanding mechanics**. They may fit into one actual scene; otherwise use the smallest relevant excerpts. A good run/jump cannot certify listening, facial expression, a turn or a hand grip.

Select excerpts from the next film after its idea exists. No required old player, fixed test duration or unrelated exercise. Non-character films use their actual communication/motion risks.

Rough blocking establishes intention and timing cheaply. A finished representative portion establishes that the chosen artwork survives that performance. Test only uncertain adaptations; reuse relevant evidence within its demonstrated action/view limits.

### D. Prevent a repair from trading away another accepted quality

Record the rejected property and the aspects to preserve. Compare the same scene before/after at matching framing and playback speed. Review the changed interval, its entry/exit, and affected adjacent shots.

For character work, check appearance, connected anatomy/clothing, acting, timing and contact together. Keep unchanged audio/assets bound to their selected versions. Pixel/hash comparisons can prove preservation where appropriate; changed poses require visual judgment rather than identical-pixel requirements.

Repair the layer responsible: a contact path, view drawing, skin weighting, gaze control, edit or spoken setup. Expand to reconstruction when the existing representation cannot support the intended performance. Avoid both endless local patches and unnecessary whole-character replacement.

### E. Make active state and review bindings reliable

Within the current `production.json`/journal convention, identify one active script, working edit/timeline, native source selection, mix and review artifact for each selected revision. Retain older revisions in their versioned records; label historical fields instead of leaving contradictory fields apparently active.

Before resuming, verify the selected revision and resolve its dependencies. Before a full render, bind the actual selected edit, artwork/native sources, relevant helper versions and sound inputs to the affected review. Correct call-site omissions first. `checkpoints.py` already validates declared hashes; extend it only if a demonstrated wrong-revision selection cannot be prevented by correct bindings. Any executable change needs a small regression reproducing that failure.

Keep source/frame/settings-bound render caches and separate working outputs. Verify reusable assets after opening the saved file in a fresh Blender session. A successfully rendered saved scene and a builder dependent on an old interactive namespace are different reuse claims.

### F. Review at the right scale and record only what happened

Use normal-speed encoded playback for energy, reactions and scene flow; successive frames for contact, joins, registration and transitions; delivery-size crops for facial/hand detail. Review the full combined cut for setup/payoff and sound, not only isolated repaired clips. A deliberately abbreviated motion test must say if dialogue is cut and cannot pass the story/audio review.

Maintain separate technical results, creative observations and actual user decisions. If playback/listening is unavailable to the agent, leave it unreviewed and present the playable artifact at the existing checkpoint. Do not manufacture a listening or comprehension result from captions, meters, screenshots or a launched player.

After a recurring failure, update its maintained owner and check the next applicable use. Record actual revision rounds, recurrence and available generation/render time. Do not announce efficiency savings or benchmark parity without comparable evidence.

## 3. Character-animation implementation changes

These belong in the existing construction/motion guides and applicable helpers, not as compulsory rules for every Pencil medium.

- **Author meaningful poses before curves.** Block initial attitude, attention change and response through the shot camera. Then add breakdowns, spacing, overlap and recovery. Preserve a strong intentional hold; constant sway is not the objective.
- **Provide the needed expressive controls.** Separate gaze, lids/brows, mouth expression/articulation, head facing and body posing where the scene needs independent changes. Fit them to coherent artwork. Avoid exposing a second painted mouth/eye underneath an overlay.
- **Use new drawings for ordinary acting too.** A hand-on-head reaction, seated pose, profile look or changed facial silhouette may need a matched replacement as much as a run does. Use deformation for its supported range; add registered drawings/correctives when view, overlap or silhouette changes exceed it. Check neck, shoulders and clothing through the transition, not just the head endpoints.
- **Plan hand chains and contacts as a unit.** Choose palm/back/edge view and grip; trace sleeve → elbow → wrist → fingers through approach, contact and release. Inspect the full body to catch masks affecting unrelated limbs or shoes.
- **Replace inadequate gait logic when needed.** The existing two-bone helper can solve suitable planar segment geometry; it does not invent weight transfer. Author support, passing, foot roll, travel and recovery together. Do not promote the earlier knee projection/rest-toe method into a general walking solution. Contact checks use the visible surface and preceding/following frames.
- **Keep performance separate from reuse.** Reuse tested artwork, controls, materials and contact mechanisms. Assign new intentions/timing to new shots and reactions. Extract a small reusable function only after tracing its callers/dependencies and testing the actual shot; do not build a universal rig framework in advance.

The practical limits remain: new views and expressive silhouettes require artwork and directed timing. No selected renderer or image model removes that work.

## 4. Samtoons-specific changes

### A. Define a combined baseline, with known weaknesses

The profile should point to the successful aspects of both films: coherent recognizable whole characters, clothes/shoes and connected construction; the approved action-proof travel/registration improvements; improved pitch scale, hands, voice continuity and delivery preservation.

Keep those strengths while explicitly marking Video 2's restricted acting vocabulary and repetitive staging as improvement targets. Film acceptance does not make every helper a benchmark-quality general solution. The 442oons references remain the craft target; local films are scoped implementation evidence.

### B. Make benchmark use visible in each new film

Retain references A/B and add the [user-supplied Short study](../../../productions/Samtoons/research/reference-ijvy-v001/analysis.md) as supplemental evidence in the next benchmark revision. Its original animation authorship/software remain unconfirmed.

Select relevant craft moments for the next story: attention shifts, contrasting reactions, an expressive held pose, contact and recovery, motivated inserts/cuts or an environment reveal. Compare actual output with those moments. Do not force a head turn into every shot, keep every body moving, duplicate the reference's jokes, or impose any past cast.

### C. Require scene-specific football comedy acting

Give each consequential participant an intention and relationship to the action. A speaker, listener, opponent, goalkeeper and crowd need not share a pose or react simultaneously. Stage the joke so the viewer knows who notices what and why the next response follows. Add dialogue only where it supplies useful context; do not use explanation to conceal an unreadable action.

Write comic status changes and reactions into the audiovisual plan. Direct face/body/voice together while preserving the selected voice identity and active local model. Suitable exaggeration can be impossible; accidental contact contradictions remain defects.

### D. Preserve football space and coverage

Keep pitch, goal, markings, flags, ball and characters in one spatial layout with deliberate scale and depth. Plan attacker/defender/keeper roles, support foot, ball route, contact and aftermath together. Keep screen direction, prop state and recurring-location geography across cuts. A new camera angle must be supported by the character artwork.

### E. Simplify the profile and reuse catalogue

Rewrite the long sequence of episode-specific lessons into concise current defaults with linked evidence and limits. Refresh the reusable catalogue to point at selected Video 2 construction/action/environment/brand/voice records as well as Video 1. Distinguish a portable asset from a scene-bound extraction reference and state demonstrated views/actions.

Retain the existing hierarchy: Samtoons owns football-comedy preferences; individual films own cast, premise, format and explicit fictional exceptions. General Pencil guidance remains usable for other subjects. Prior failures stay as evidence, not competing current instructions.

## 5. Implementation order and completion evidence

| Order | Work | Existing owner(s) | Evidence needed to finish |
|---|---|---|---|
| 1 — before the next film | Consolidate the process; add the performance-to-asset handoff and review-risk coverage; remove repetitive/conflicting guidance. | `pipeline/skill/SKILL.md`, `pipeline/styles/construction.md`, `pipeline/motion-planning.md` | A clear path from consequential beat to asset requirements and actual proof, applicable to character and non-character work; preserved historical snapshots. |
| 2 — before the next film | Define unambiguous current selections, correct review binding guidance and refresh stale entry-point descriptions. Preserve sound contracts and live-authoring conventions. | `pipeline/README.md`, `productions/README.md`, root `README.md`; `checkpoints.py`/`test_workflow.py` only for an evidenced executable gap | Resume resolves the intended revision; selected-input changes invalidate only affected reviews; saved-asset reuse claims have a reopen check. No retroactive gate on delivered films. |
| 3 — before the next film | Consolidate Samtoons defaults and benchmark lessons; index accepted assets with scoped limits and post-film weaknesses. | `productions/Samtoons/README.md`, next version of `benchmark-v002.md`, existing reuse catalogue | New production can find current quality targets and usable references without reconstructing the entire chat or reading every failed attempt. |
| 4 — after the next idea is selected | Make rough scene blocking, derive image/asset requirements, and implement missing acting/contact capabilities in the chosen excerpt(s). | New film's existing brief/script/plan, assets and scripts | Actual ordinary acting and demanding action, where present, meet the scene's intention while preserving likeness, joints, clothes, timing and contact. Use the existing staging/sound decision. |
| 5 — during that film | Expand proven construction into original performances; review a complete inexpensive cut before delivery rendering. | Existing animatic, shot scripts and journal | Story/visual continuity and performance survive across the cast and cuts. New views/actions receive relevant review; no propagation based on a bone count. |
| 6 — after use | Adopt what actually worked; narrow/remove ineffective guidance. | Relevant existing guide/profile/helper plus journal | Compare actual recurring defects, revision rounds and measured work with prior evidence. Mark unmeasured time/cost and unreviewed qualities unknown. |

Steps 1–3 are the next implementation task. They prepare the workflow without generating a speculative cast or another standalone test film. Step 4 supplies the first evidence that the proposed method improves the next production.

## 6. What a successful first use must demonstrate

The representative scene must show a readable intention/reaction, suitable view and expression, coherent head-to-toe design, appropriate hands, credible support/contact where relevant, and timing that fits the selected sound. Check the approach, peak and recovery; a good still is insufficient.

The ordinary-acting scene should no longer read as an unchanged resting character with a talking mouth. The demanding-action scene should retain the best contact/travel work already achieved. Both may use economical poses and holds when those serve the scene. No arbitrary score, expression count or animation-frame quota substitutes for this judgment.

Codex's responsibility is to make those staging/posing choices, prepare missing artwork and author the controls. Blender supplies editable construction, timing and rendering. Automation handles repetitive operations and measurable checks. The user reviews concrete creative outcomes at the already established checkpoints.

## 7. Evidence, checks and research limits

Read during this audit: root instructions/context, production conventions, the authoritative skill, execution/sound/construction/motion guides, Samtoons profile/benchmark/reuse records, Video 2 prompts/builders/checks/plan/journal/delivery notes, and the earlier benchmark and acting studies.

Read-only baseline checks run successfully on 22 September 2026:

- `python3 pipeline/checkpoints.py --self-test`: absent, stale, rejected and agent-only approvals block; current user approval/explicit waiver work.
- `python3 pipeline/test_workflow.py`: canonical installed skill, isolated film reviews, pinned asset/profile/guide adoption.
- `python3 pipeline/pose_geometry.py`: planar geometry, bend direction and invalid targets.

These passes demonstrate existing technical behavior, not an acting-quality improvement.

Primary research supports the proposed direction but does not validate our future implementation. Animation Mentor's [Facial Animation 101](https://www.animationmentor.com/blog/facial-animation-101/) explains meaningful expression changes, focused gaze and separate facial/body timing; it was rechecked for this plan. The [2025 2.5D character-rig paper](https://arxiv.org/html/2502.17866v1) explicitly documents projection, camera-facing action and external-contact limitations; it supports caution, not a recommendation to replace our pipeline with its system. Earlier [source research](../../../productions/Samtoons/videos/002-how-arsenal-won-the-league/research/acting-source-research.md) contains animation principles and official drawing-substitution references; the Toon Boom pages could not be fetched again during this audit.

The new Short's study used sampled browser frames, not an exhaustive motion/audio examination. Its software cannot be inferred confidently from the pixels. No new generated art, Blender scene, motion fix or production render was created as part of this plan.
