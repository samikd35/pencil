# PyBlend Experiment 001 — Final Report

**Verdict: GO — all frozen gates passed.**

Experiment 001 tested whether a reference-locked OpenCV → VTracer → SVG → Blender 5.2 native Grease Pencil pipeline (Baseline B) preserves clean stylized 2D references better than two fresh direct image-to-Blender-Python attempts per image (Baseline A). It is a throwaway feasibility prototype, not the production framework.

## Frozen gate result

| Gate | Required | Observed | Result |
|---|---:|---:|---|
| Median boundary-error reduction | ≥ 20.0% | 93.5% | PASS |
| Median landmark-error reduction | ≥ 20.0% | 100.0% | PASS |
| Masked Baseline B wins | ≥ 12/16 | 14/16 | PASS |
| Positive line-art and flat-color median improvement | Both groups | Boundary and landmarks positive in both | PASS |

Supporting LPIPS-Alex also favored B: median score fell from 0.2793 for the per-image A mean to 0.0371, a median per-image reduction of 79.5%. LPIPS was not a gate.

## Per-image automated evidence

A values are the frozen per-image mean of A1 and A2. Lower boundary error, landmark NME, and LPIPS are better.

| Reference | Class | Renders | A boundary | B boundary | Reduction | A landmark | B landmark | Reduction | A LPIPS | B LPIPS |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| EVAL-L-ID-01 | binary_line_art | [Ref](../../../artifacts/dataset_v1/working/EVAL-L-ID-01.png) / [A1](../../../artifacts/baseline_a/EVAL-L-ID-01/attempt_1/render_evaluation.png) / [A2](../../../artifacts/baseline_a/EVAL-L-ID-01/attempt_2/render_evaluation.png) / [B](../../../artifacts/baseline_b/evaluation/EVAL-L-ID-01/render_evaluation.png) | 1.0000 | 0.0012 | 99.9% | 1.0000 | 0.0000 | 100.0% | 0.3854 | 0.0395 |
| EVAL-L-ID-02 | binary_line_art | [Ref](../../../artifacts/dataset_v1/working/EVAL-L-ID-02.png) / [A1](../../../artifacts/baseline_a/EVAL-L-ID-02/attempt_1/render_evaluation.png) / [A2](../../../artifacts/baseline_a/EVAL-L-ID-02/attempt_2/render_evaluation.png) / [B](../../../artifacts/baseline_b/evaluation/EVAL-L-ID-02/render_evaluation.png) | 0.8044 | 0.0051 | 99.4% | 0.5340 | 0.0000 | 100.0% | 0.3185 | 0.0347 |
| EVAL-L-S-01 | binary_line_art | [Ref](../../../artifacts/dataset_v1/working/EVAL-L-S-01.png) / [A1](../../../artifacts/baseline_a/EVAL-L-S-01/attempt_1/render_evaluation.png) / [A2](../../../artifacts/baseline_a/EVAL-L-S-01/attempt_2/render_evaluation.png) / [B](../../../artifacts/baseline_b/evaluation/EVAL-L-S-01/render_evaluation.png) | 0.4106 | 0.0097 | 97.6% | 0.0686 | 0.0000 | 100.0% | 0.1334 | 0.0244 |
| EVAL-L-S-02 | binary_line_art | [Ref](../../../artifacts/dataset_v1/working/EVAL-L-S-02.png) / [A1](../../../artifacts/baseline_a/EVAL-L-S-02/attempt_1/render_evaluation.png) / [A2](../../../artifacts/baseline_a/EVAL-L-S-02/attempt_2/render_evaluation.png) / [B](../../../artifacts/baseline_b/evaluation/EVAL-L-S-02/render_evaluation.png) | 0.0541 | 0.0131 | 75.7% | 0.0000 | 0.0000 | 0.0% | 0.0441 | 0.0299 |
| EVAL-F-ID-01 | flat_color | [Ref](../../../artifacts/dataset_v1/working/EVAL-F-ID-01.png) / [A1](../../../artifacts/baseline_a/EVAL-F-ID-01/attempt_1/render_evaluation.png) / [A2](../../../artifacts/baseline_a/EVAL-F-ID-01/attempt_2/render_evaluation.png) / [B](../../../artifacts/baseline_b/evaluation/EVAL-F-ID-01/render_evaluation.png) | 1.0000 | 0.0135 | 98.7% | 1.0000 | 0.0000 | 100.0% | 0.3385 | 0.0226 |
| EVAL-F-ID-02 | flat_color | [Ref](../../../artifacts/dataset_v1/working/EVAL-F-ID-02.png) / [A1](../../../artifacts/baseline_a/EVAL-F-ID-02/attempt_1/render_evaluation.png) / [A2](../../../artifacts/baseline_a/EVAL-F-ID-02/attempt_2/render_evaluation.png) / [B](../../../artifacts/baseline_b/evaluation/EVAL-F-ID-02/render_evaluation.png) | 0.7346 | 0.1782 | 75.7% | 0.0213 | 0.0158 | 25.8% | 0.3448 | 0.1140 |
| EVAL-F-S-01 | flat_color | [Ref](../../../artifacts/dataset_v1/working/EVAL-F-S-01.png) / [A1](../../../artifacts/baseline_a/EVAL-F-S-01/attempt_1/render_evaluation.png) / [A2](../../../artifacts/baseline_a/EVAL-F-S-01/attempt_2/render_evaluation.png) / [B](../../../artifacts/baseline_b/evaluation/EVAL-F-S-01/render_evaluation.png) | 0.4573 | 0.1158 | 74.7% | 0.0164 | 0.0000 | 100.0% | 0.2401 | 0.0982 |
| EVAL-F-S-02 | flat_color | [Ref](../../../artifacts/dataset_v1/working/EVAL-F-S-02.png) / [A1](../../../artifacts/baseline_a/EVAL-F-S-02/attempt_1/render_evaluation.png) / [A2](../../../artifacts/baseline_a/EVAL-F-S-02/attempt_2/render_evaluation.png) / [B](../../../artifacts/baseline_b/evaluation/EVAL-F-S-02/render_evaluation.png) | 0.6576 | 0.0700 | 89.4% | 0.1135 | 0.2350 | -107.0% | 0.2218 | 0.0502 |

EVAL-F-S-02 is the important adverse case: B improved boundary error and LPIPS but its landmark NME was worse than the A mean. EVAL-L-S-02 had equal landmark NME. These results remain included; the frozen median gates and both subgroup medians still pass.

## Subgroups

| Style | Boundary reduction | Landmark reduction | Masked B wins |
|---|---:|---:|---:|
| Binary line art | 98.5% | 100.0% | 6/8 |
| Flat color | 82.5% | 62.9% | 8/8 |

## Raw masked preference, now unsealed

The user submitted all sixteen X/Y choices before the method mapping was opened.

| Trial | Reference | Compared A | Choice | X method | Y method | Selected |
|---|---|---|---:|---|---|---|
| T01 | EVAL-F-S-02 | A1 | X | B | A1 | B |
| T02 | EVAL-F-S-01 | A1 | Y | A1 | B | B |
| T03 | EVAL-L-S-02 | A1 | Y | B | A1 | A1 |
| T04 | EVAL-L-S-02 | A2 | X | A2 | B | A2 |
| T05 | EVAL-F-ID-02 | A1 | X | B | A1 | B |
| T06 | EVAL-L-S-01 | A1 | X | B | A1 | B |
| T07 | EVAL-F-ID-02 | A2 | Y | A2 | B | B |
| T08 | EVAL-L-ID-02 | A1 | X | B | A1 | B |
| T09 | EVAL-L-S-01 | A2 | Y | A2 | B | B |
| T10 | EVAL-F-S-02 | A2 | Y | A2 | B | B |
| T11 | EVAL-F-S-01 | A2 | Y | A2 | B | B |
| T12 | EVAL-F-ID-01 | A1 | Y | A1 | B | B |
| T13 | EVAL-F-ID-01 | A2 | Y | A2 | B | B |
| T14 | EVAL-L-ID-01 | A2 | X | B | A2 | B |
| T15 | EVAL-L-ID-02 | A2 | X | B | A2 | B |
| T16 | EVAL-L-ID-01 | A1 | Y | A1 | B | B |

## Complexity and timing (descriptive)

| Measure | Baseline A | Baseline B |
|---|---:|---:|
| Completed runs | 14/16 | 8/8 |
| Median model/pipeline time | 516.2 s model time | 2.71 s full pipeline |
| Median Blender time | 4.22 s | 2.08 s |
| Median Grease Pencil objects | 7.5 | 1.0 |
| Median strokes | 75.5 | 67.5 |
| Median points | 1660.0 | 1420.5 |
| Median blend size | 115.5 KiB | 130.3 KiB |
| Median SVG paths / size | n/a | 36.0 / 60.7 KiB |

Baseline A's model time is not directly comparable to Baseline B's local pipeline time, but the difference is operationally material. Complexity, timing, and file size did not affect pass/fail.

## Failures retained

- Baseline A execution failures after the permitted repairs: `EVAL-L-ID-01-A2`, `EVAL-L-ID-02-A2`.
- Blank Baseline A comparison renders: `EVAL-F-ID-01-A1`, `EVAL-F-ID-01-A2`, `EVAL-L-ID-01-A1`, `EVAL-L-ID-01-A2`, `EVAL-L-ID-02-A2`.
- Baseline B held-out failures: none.

## Deviations

- **DEV-001:** The current Wikimedia raster redirect for DEV-L-01 produced 1280x1158 rather than the provisional 1132x1024 listing. Dataset membership and source asset were unchanged; no local resampling of the registered original was performed. Impact: Development-only source metadata drift; no held-out scoring impact.
- **A-HARNESS-001:** EVAL-L-ID-01-A1 executed after one repair but its blank render caused the normalization harness to fail before writing a manifest. Existing evidence was preserved and the manifest was recovered without rerunning the model or Blender. Impact: The attempt remains a blank scored failure. Transient temporary-path and precise harness timing evidence are unavailable.
- **B-ORDER-001:** The Baseline B runner computed its boundary metric inside each held-out run manifest, before all eight B runs had completed. Impact: Profiles were already frozen and no tuning, rerun, or execution decision used those values; the complete post-run evaluation was recomputed independently.
- **INSPECTOR-001:** The first post-run geometry inspection encountered Blender point handle attributes whose values were None. The inspector was fixed globally to omit absent handles and all 14 successful A scenes were inspected consistently; pre-fix logs were retained. Impact: No scene or render changed; complexity evidence only.

## Limitations

- The ten approved references are unusually clean and mostly vector-origin artwork, so the result is a ceiling test for the reference-locked path rather than proof on noisy raster-born art.
- The flat-color simpler-subject set contains two NIH BioArt assets from the same source family.
- Landmarks and masked preference use one human evaluator; masked preference is developer preference, not population-level human preference.
- Experiment 001 covers static, already-stylized 2D reconstruction only. It says nothing about animation, rigging, photo stylization, arbitrary SVG support, or 3D reconstruction.

## Decision and next step

Proceed to planning a narrowly scoped production framework around the reference-locked SVG-to-Grease-Pencil path. Keep direct image-to-Blender-Python generation out of the fidelity-critical baseline. Before broadening the product claim, run a second stress pilot on raster-born, antialiased, noisy, and imperfect-background references.

The evidence supports Baseline B as the fidelity-critical foundation for the clean line-art and flat-color scope tested here. It does not support using Baseline A as the reconstruction baseline: A had two execution failures, five blank comparison outputs, much higher median fidelity error, and lost 14 of 16 method-hidden comparisons.

The best next workflow is `/handoff` to preserve this completed experiment, followed by `/wayfinder` or `/to-spec` only after confirming the intended production scope. A separate Experiment 002 should test raster-born and noisy references before the framework claims broad input robustness.

## Evidence index

- [Machine-readable verdict](final_verdict_v1.json) — SHA-256 `39ab0cfa40cff9ebc5c01348503afd29bce8742337695f7cc8e6c2e3f657c935`
- [Automated metrics](automated_metrics_v1.json) — SHA-256 `90504ebd47eb31a5ccf778f66318ee1e30edae8e94676bd4c1b858e1d15382a7`
- [Masked preference results](masked_preference_results_v1.json) — SHA-256 `046f263e2b5f1596da70e5c4785484c3e3e399a9248801c7a3fa74df535bfaa6`
- [Complexity and timing](complexity_timing_v1.json) — SHA-256 `9460226b52c0e5541e1eb3480fe1c1298fa8fbc0c0d5e6a56d8b7889a623d475`
- [Evaluation environment](evaluation_environment_v1.json) — SHA-256 `e1151e285cfa7a274445cd56ca9b0ad28fee4debb4b3749ccba3fe644412288e`
- Full per-run inputs, commands, timings, outputs, and hashes are retained under `artifacts/baseline_a/`, `artifacts/baseline_b/`, and `data/manifests/`.
