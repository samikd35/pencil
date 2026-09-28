# Heavy Box — stickman animation experiment

Current direction: **C — Elastic Comic**, explicitly selected by the user. Character-sheet and key-pose development follows; no animation has been built. See `events.jsonl` for the latest production state. The original setup guide is preserved in `history/setup-readme-v001.md`.

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

1. User chooses or combines character directions.
2. Produce the selected character sheet and key-pose strip.
3. Build an editable character and rough motion pass.
4. Review and refine the animation, preserving failures and accepted changes.
5. Test a targeted revision and document reusable methods.

Voice cleanup and pronunciation repair belong to a later, separate proof. This experiment has no voiceover. No installation, publication, or model-training work is implied by this setup.
