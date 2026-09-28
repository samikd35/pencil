# Phase A — implementation and verification

22 September 2026 · **Phase A implemented. Phase B awaits the next story.**

The [revised plan](plan.md) is preserved as the authorized planning snapshot. This record describes the implemented state. No new film or cast was started, and no benchmark-level creative improvement is claimed from these preparation checks.

## Completed work

| Package | Implemented result |
|---|---|
| A1 — Authoring guidance | Updated the authoritative [skill](../../skill/SKILL.md), [construction guide](../../styles/construction.md) and [motion guide](../../motion-planning.md). The existing steps now connect intention, rough layout, asset requirements, authored performance, look and complete-result review. Ordinary acting and demanding mechanics receive separate coverage where relevant. |
| A2 — Source reliability | Added explicit current-selection and builder/file ownership conventions to [execution guidance](../../README.md#current-selections-and-correction-ownership) and [production adoption](../../../productions/README.md). Added a narrowly scoped current-input comparison to the checkpoint guard and tested it. Verified a copied existing Blender source through keying, save/reopen and rendering. |
| A3 — Samtoons standards | Consolidated [profile v004](../../../productions/Samtoons/README.md), published [benchmark v003](../../../productions/Samtoons/benchmark-v003.md) and a [reuse catalogue v002](../../../productions/Samtoons/assets/reuse-v002/README.md). Accepted construction and later acting weaknesses are recorded together. The catalogue references existing binaries rather than duplicating them. |
| A4 — Verification | Reviewed the maintained changes against Phase A scope, ran the existing checks plus the source-switch regression, checked local links/anchors and preservation records. Evidence is in [checks.json](checks.json), [changes.diff](changes.diff) and the existing pipeline journal. |

The four creative checkpoints and scoped user delegation remain in place. General guidance stays independent of Samtoons' football/comedy preferences. No universal rig, planning database, new dependency or mandatory named-player test was added.

## Executable defect and correction

The baseline guard rehashed an approval's recorded files, but had no way for a caller to state that its next operation would use a different file. A disposable fixture demonstrated the problem: approval bound `source-A.blend`; the next selection was `source-B.blend`; the old call still passed because A's bytes were unchanged.

`require_checkpoint(..., required_inputs=[...])` now checks that the supplied current sources are inside the film root, exist and were bound as inputs to that review, then applies the existing hash checks. New full-render guidance requires decision-relevant paths from the actual current source/edit selection. Legacy calls and the read-only CLI retain their earlier behavior; this does not retrofit delivered scripts or automatically discover dependencies. Explicit user waivers keep their existing semantics.

The regression verifies an unbound source switch blocks, a newly reviewed selection passes, mutation after review blocks, invalid current inputs fail, and unchanged sound acceptance survives a picture-only switch. Canonical skill discovery, sibling isolation and pinned asset/profile/guide behavior also pass.

## Native runtime check

The live connector reported Blender 5.2.0 LTS, an interactive window and an initially clean untitled default scene. A workspace copy of video 002's `delivery-v027/sources/opening-dialogue.blend` supplied the check; the delivered file was not edited.

In `S002_B01_v016_unveiling`, frame 220, the check keyed the existing camera's orthographic scale from approximately 13.8 to 13.938, saved a separate corrected file, rendered at 384×216, reopened that file and rendered the same frame again. The key and Action slots persisted. The two PNG files contain different container bytes, but decoded RGB pixels are identical. The resulting preview was visually inspected for successful scene output, not for new acting quality.

- [Scoped check script](runtime-check/check.py), [prepare result](runtime-check/prepare.json), [reopen result](runtime-check/verify.json), [pixel comparison](runtime-check/comparison.json).
- [Saved corrected copy](runtime-check/corrected-copy.blend) and [rendered frame](runtime-check/after-reopen.png).

This demonstrates the selected **file-owned native correction → save/reopen → render** route. No old authoring registry was loaded by the check. It does not validate new character extraction, new expressions, arbitrary builder regeneration, Grease Pencil construction or full-speed playback. The earlier background startup failure remains unexplained; the working interactive route is distinct evidence. New API/asset paths still need their own bounded check when a real shot requires them.

## Checks and preservation

- `python3 pipeline/checkpoints.py --self-test` — passed.
- `python3 pipeline/test_workflow.py` — passed, including current-source switching and unchanged sound.
- `python3 pipeline/pose_geometry.py` — passed; geometry only.
- `python3 pipeline/test_styles.py` — passed; selected reference/recipe isolation and audio/timing metadata preservation.
- Local Markdown paths/heading fragments and catalogue source hashes — verified in `checks.json`.
- Nineteen protected file hashes match the pre-edit record, including delivered native/movie selections, the previous catalogue/benchmark and the approved plan. Three voice-model weight files retain their recorded size and modification time; no weights were changed or removed. This is a metadata preservation check for weights, not a new model inference test.

Before/after copies of maintained owners and the new benchmark/catalogue are retained beside this record. Completed video files, source art, sound selections, old profile snapshots and approval events were not rewritten. No new subjective listening, full-film playback or independent creative review was performed for Phase A.

## Next use

The next step is the user's new story. Run Phase B through the updated produce-pencil-animation workflow: develop that story, stage its actual performances, derive needed assets, prove a small representative finished sequence, review the full animatic, then complete the film. The quality improvement must be demonstrated there across acting, design, mechanics, staging, environment and finish together. Preparing this workflow does not by itself prove benchmark parity.
