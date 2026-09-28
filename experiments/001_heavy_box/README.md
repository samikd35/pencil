# Heavy Box — stickman animation experiment

Current direction: **C — Elastic Comic**, explicitly selected by the user. The latest 10-second preview adds color, illustrated lighting and original synthesized sound effects: [watch with sound](artifacts/finish-v002/preview-with-sound.mp4), [editable project with audio](artifacts/finish-v002/editable-project-with-audio.zip), [review and verification](review-finish-v002.md). All 240 frames of the original character motion are preserved. The earlier silent revision and comparison remain available in `review-v005.md`. See `events.jsonl` for the production history. Earlier README versions are preserved in `history/`.

## Purpose

Create an original, approximately 10-second action-only animation in Codex and Blender, then test a targeted revision. A stickman approaches a heavy box, struggles to push it, stumbles when it slides, and recovers. The proposed first test uses one fixed camera. These are this experiment's creative choices, not permanent pipeline restrictions.

The PyBlend starter is historical reference material only. Its fighter, paths, policies, approval history, timing, and rig limitations do not govern this project. Techniques may be reused after checking that they fit. Research and test current model capabilities rather than treating earlier experiments as their ceiling.

## Review criteria

- Action and emotion read without narration.
- Character proportions and line treatment remain intentional and stable.
- Hands maintain contact while pushing; planted feet do not slide unintentionally.
- Timing, anticipation, effort, and recovery communicate weight.
- Artwork and motion remain editable in the saved Blender project.
- A requested change to the second push preserves unrelated opening and ending work.

Technical checks and visual judgments are recorded separately. A generated concept image is not an animation-ready rig, and a technical pass is not user acceptance.

## Files

- `events.jsonl`: append-only production journal; one JSON object per meaningful event.
- `journal.py`: standard-library logger; validates local artifacts and records SHA-256 hashes.
- `test_journal.py`: a small runnable integrity check.
- `research/character-directions.md`: researched references, design choices, and uncertainties.
- `design/`: versioned concept boards and the exact generation prompts.
- Add scripts, Blender projects, and renders here as they are actually produced; do not create speculative infrastructure.

## Recording work

Before a generation/build, save the exact prompt or runnable script with a versioned name and log its inputs. Afterward, log the output paths, result, and review decision. Record failed attempts too. Keep source records and artifacts; write a new version rather than overwriting reviewed work.

Example from this folder:

```sh
python3 journal.py --stage design --status pending_review \
  --intent "Offer original character directions" \
  --method "Built-in image generation" \
  --input design/options-v001.prompt.txt \
  --output design/options-v001.png \
  --result "Comparison board generated; not rigged or motion-tested" \
  --decision "Await user character selection"
```

Paths are relative to this experiment. Use `--source` for external URLs or historical source references; they are not executed. Use `--seconds` only for measured elapsed time. Unknown time, model identity, or cost must stay unknown, not estimated as fact. Describe tools/models in `--method` only as specifically as verified. User selections are logged as `selected` only after an actual user choice.

To verify the journal helper:

```sh
python3 test_journal.py
```

Each event records a schema version, ID, UTC timestamp, stage, status, intent, method, inputs, outputs, result, decision, sources, and optional duration. Artifact hashes identify the exact files used at that step; they are not backups. Preserve the versioned files themselves. `events.jsonl` can later be imported into SQLite without adding a database service now.

## Next steps

1. Review the color-and-sound preview and tune the effect intensity if needed.
2. Try a different action with the same character before extracting reusable animation methods.
3. Separately refine the walk and final presentation once the reuse test informs the production method.

Completed: the targeted second-push/recovery revision changed 90 frames while preserving all 136 protected opening and ending frames. Continuous contact and hand-clearance checks pass; see `review-v005.md`.

Voice cleanup and pronunciation repair belong to a later, separate proof. This experiment has no spoken narration; its latest finish includes procedurally generated nonverbal cartoon sounds and Foley, authorized by the user. No installation, publication, or model-training work is implied by this setup.
