# Productions

Normal new films belong here. Existing films and tests under `experiments/` stay in place. Create a named production and its video only when that work is authorized; the tree below is a convention, not a request to create empty projects.

```text
productions/
└── <production-name>/
    ├── README.md                 Production identity and applicable direction
    ├── assets/                   Versioned reusable assets, when needed
    └── videos/
        └── <id-title>/            Film root for this video
            ├── brief.md          Story, creative mode and local choices
            ├── script.md         Audiovisual script (version as needed)
            ├── production.json   This video's plan and selections
            ├── events.jsonl      This video's decisions and reviews
            ├── assets/           Selected copies and video-specific assets
            ├── scripts/          This video's authored work
            └── artifacts/        Versioned previews and deliveries
```

A standalone movie uses one video folder. An explicitly requested series uses the same neutral layout for its episodes. Add further files or subfolders only when the actual work needs them.

## Creative context

The production README is its **production profile**, not a copy of the general pipeline. For a new authorized production, record only the decisions needed by the current work:

- Audience, purpose and domain; factual verification or fictional treatment appropriate to the subject.
- Creative identity and standalone/series direction, selected benchmarks, visual and sound preferences.
- Applicable domain guidance and reusable assets, with versions, source/license, reviewed uses and limits.
- Any actual format, duration or tool defaults. Keep these independent from the niche and allow explicitly chosen video exceptions.

Keep enduring direction here and episode progress in that video's brief/journal. Link to the video instead of maintaining a second, easily stale status report. Historical research is evidence, not automatically the current profile. A shared subject does not imply shared creative identity. Extract a separate shared domain guide only when multiple actual productions need it; do not create a pipeline or skill fork per niche.

### Resolve the current video's choices

On a new video, read its production profile and current user direction, then record the effective choices in its brief. On resume, start from the video's adopted context, assets and approvals; compare newer parent guidance only when an update is requested or needed. Explicit video choices refine defaults; do not silently override an explicit constraint or invent a waiver. Clarify only material unresolved conflicts.

In the existing brief or top-level `production.json` metadata, record the applicable profile/source version, selected domain/technique guides with a short reason, and deliberate video exceptions. Use ordinary text and local snapshots rather than an automatic inheritance engine. Record review coverage in the shot plan/journal: changed asset/view/action, demanding interval, inspection performed, outcome and unresolved limitation. Do not infer coverage from a successful sibling shot.

Load only guidance required by the actual work:

| Work requires | Guidance to read | Do not infer |
| --- | --- | --- |
| Character performance or deforming artwork | Relevant parts of `pipeline/styles/construction.md` | A subject or style label certifies a rig or all views. |
| Dialogue, effects, ambience or music | Relevant parts of `pipeline/sound-planning-method.md`; execution instructions for selected tools | Every film needs speech, music or a particular voice engine. |
| Domain-specific explanation or reconstruction | The selected production's domain section/linked guide and sources | Football or educational rules apply to unrelated subjects. |
| A new technique not yet supported | Its actual tool documentation and a focused check within the current production | A general workflow or one of the nineteen style references implements every renderer. |

For intentionally silent work, record that sound choice at the existing sound checkpoint (combined with staging where useful); do not generate an unnecessary soundtrack. Retain existing review requirements and scoped user delegation. There is no additional profile approval gate.

The production README records its identity, audience, applicable direction and intended creative mode. **Standalone is the default; series requires an explicit user request.** A video's brief records any scoped exception. Names, numbering, multiple videos or reused assets never establish a series, continuing story, cliffhanger or recurring arc. The [main skill](../pipeline/SKILL.md) governs creative development for the requested mode.

Group by production identity. A shared niche or visual style alone does not make two unrelated works the same production. Conversely, a new visual treatment does not automatically require moving an established production. Keep episode relationships only where the user has requested series development.

On resume, read the production context and the selected video's brief, script, plan and latest journal entries. Resolve differences against the actual user direction and recorded selections; do not copy the most recent sibling video's decisions into the current video. An existing video's approvals or delegated review apply only within their recorded scope.

## Shared assets and stable selections

Reusable characters, environments, props and sounds may live in the production's `assets/`, with a version recorded for each actual selection. Preserve source, license, attribution, tested uses and limitations alongside the asset. Reusing a character or set does not establish shared story continuity.

An asset record distinguishes an independently reusable file from a scene-bound extraction reference. Include the actual file/hash, required dependencies, review evidence and supported actions/views; mark untested adaptations explicitly. A rendered film or attractive neutral drawing alone is not a reusable rig. Preserve accepted performances when retiming; review new acting separately.

Before binding a review, copy selected shared assets into the video's `assets/` and record their original paths, versions and hashes in its plan or journal. Keep the applicable production README snapshot as `assets/production-context.md`, noting its source and adoption in the video journal. Snapshot selected domain/technique guidance that materially defines the reviewed construction or treatment alongside that context, recording its source and version/hash; do not copy every guide. The current journal/checkpoint helpers bind files within the film root, so direct references to the parent production are insufficient for those reviews.

Bind the relevant local context, selected guidance/artwork/sounds and `assets/style-selection.json` when present to the appropriate checkpoints. A new shared version leaves existing video selections intact. An authorized update to this video refreshes the relevant local snapshot, preserves the old version with its reviewed artifacts and revisits affected checkpoints. Do not refresh selections merely because shared files changed.

## Existing tools

Run the [pipeline commands](../pipeline/README.md) from the Pencil workspace. Point style and audio commands at the selected video's `production.json`. Pass the video directory as `film_root` to `require_checkpoint` and as `root` to `append_event`; each video has its own journal even when revision names match. The historical journal CLI defaults to Heavy Box, so import its root-parameterized helper for new videos.

The four creative checkpoints and their delegation rules remain in the [main skill](../pipeline/SKILL.md). A folder convention does not provide approval, generate artwork or select a creative treatment.
