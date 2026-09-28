# Codex-to-Blender integration for PyBlend

**Date:** 2026-09-04
**Scope:** reliability, observability, reproducibility, scalability, security,
and local artifacts for the PyBlend R&D workflow.

## Decision

Keep **versioned Blender Python plus direct command-line background execution**
as PyBlend's production path. Use Blender's normal UI to inspect the saved
`.blend` and rendered review artifacts. Treat MCP as an optional inspection and
interactive-debugging adapter, not as the authoring engine or source of truth.

PyBlend is already using the recommended core path. Its Python orchestrator
starts the local Blender executable with `--background --factory-startup
--python ...`, passes an explicit JSON manifest and output directory, captures
stdout/stderr, checks the process result, renders evidence, validates it, and
saves an editable `.blend`.

This is also consistent with Blender's own guidance: for non-interactive
scripts, command-line background execution is more efficient than driving the
interface, and useful outputs include a render, a saved `.blend`, and text or
file-based results ([Blender Python tips](https://docs.blender.org/api/main/info_tips_and_tricks.html#use-blender-without-its-user-interface)).
Blender documents background mode specifically for automation and batch
rendering ([command-line overview](https://docs.blender.org/manual/en/latest/advanced/command_line/index.html),
[rendering from the command line](https://docs.blender.org/manual/en/latest/advanced/command_line/render.html)).

## Comparison

| Method | Reliability and reproducibility | Visual QA and observability | Scaling | Security | PyBlend role |
|---|---|---|---|---|---|
| Direct `bpy` script run by `blender --background` | Highest: every run starts from explicit inputs, scripts, Blender version, and a fresh process; command arguments and their order are documented | Strong when each run writes logs, JSON validation, review renders, and a `.blend`; the `.blend` can then be opened normally | Natural job boundary for queues, retries, and separate worker processes; Blender warns that its embedded Python is not thread-safe, so process isolation is the safer unit | Still executes trusted Python, but the executable script and paths are reviewable and versioned; `--factory-startup`, `--disable-autoexec`, and an explicit output root reduce ambient state | **Primary authoring, rendering, validation, and packaging path** |
| Blender UI / UI automation | Low for repeatable production: window layout, focus, mode, selection, and context affect behavior. Blender documents that operators can fail when their UI context is wrong | Best for a human inspecting the viewport, timeline, collections, and controls; screenshots alone are weaker than render-plus-validation evidence | Poor as a batch primitive; one interactive state must be babysat | Actions affect the currently open, possibly unsaved scene | Human review and rare UI-specific acceptance tests only |
| Blender MCP server | Useful for querying or changing the currently open session, retrieving screenshots, and ad-hoc debugging; adds an MCP process, add-on, socket/session, and live Blender state between intent and result | Convenient live scene summaries and screenshots; does not replace saved artifacts or deterministic render checks | Appropriate for interactive sessions, not necessary for independent batch jobs | The official Blender Lab page says generated code runs without guards and recommends a VM or machine without sensitive data | Optional read/inspect/debug adapter on a disposable copy |

The UI-automation assessment is an inference from Blender's documented context
model: `bpy.ops` operators depend on active areas, selection, and modes and can
fail their `poll()` checks when context is wrong
([Using Operators](https://docs.blender.org/api/main/info_gotchas_operators.html)).
For PyBlend scripts, prefer Blender's data API and direct property changes;
use operators only where Blender exposes no practical data-API equivalent, such
as the supported SVG import, rendering, and final file save.

Blender also states that Python threads are not supported and can cause hard-to-
diagnose crashes; independent Blender processes are the documented alternative
for concurrent work
([threading gotcha](https://docs.blender.org/api/5.0/info_gotchas_threading.html)).

## Why MCP is supplementary, not the core

Blender now has an official **Blender Lab MCP Server**. It is a live bridge:
MCP client -> MCP server over stdio -> Blender add-on over a local TCP socket
([project overview](https://projects.blender.org/lab/blender_mcp/src/branch/main/readme.md)).
Its tools can inspect a scene, render to a path, take UI screenshots, search the
bundled Blender docs, and execute Python in Blender
([server README](https://projects.blender.org/lab/blender_mcp/src/branch/main/mcp/README.md)).

That convenience does not improve the determinism of PyBlend's compiler. The
official project still executes Python through `exec`, marks arbitrary execution
as destructive, and exposes a separate CLI tool which itself launches
`blender --background`
([execution tool](https://projects.blender.org/lab/blender_mcp/src/branch/main/mcp/blmcp/tools/execute_blender_code.py),
[CLI helper](https://projects.blender.org/lab/blender_mcp/src/branch/main/mcp/blmcp/tools_helpers/blender_cli.py)).
This is evidence that interactive MCP and background jobs are complementary,
not competing architectures.

The official Blender page gives a direct security warning: the server runs
LLM-generated Blender code without guards and recommends isolation
([Blender Lab MCP Server](https://www.blender.org/lab/mcp-server/)). The MCP
specification also assigns permission and lifecycle enforcement to the host and
requires local HTTP servers to bind to loopback and use appropriate protection
([MCP architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture),
[MCP transports and security](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)).

Therefore, if PyBlend later adopts MCP:

1. Use the official Blender Lab implementation, pinned to a reviewed revision.
2. Scope it to the trusted PyBlend project and restrict its exposed tools in
   Codex configuration ([Codex MCP configuration](https://developers.openai.com/codex/mcp/)).
3. Default to read-only scene summaries, named-object inspection, screenshots,
   and render-to-path tools.
4. Run arbitrary edits only on a copied `.blend` in an isolated workstation or
   VM, never on the sole canonical file.
5. Persist every accepted change as a versioned script/manifest and reproduce it
   through the direct background pipeline before promotion.

## Recommended executable contract

Use one explicit command per build or validation job:

```sh
/Applications/Blender.app/Contents/MacOS/Blender \
  --background \
  --factory-startup \
  --disable-autoexec \
  --offline-mode \
  --python-exit-code 1 \
  --python experiments/.../build_scene.py \
  -- --manifest /absolute/path/input.json --output /absolute/path/artifacts
```

Blender documents that command-line argument order is significant and provides
the background, Python, logging, factory-startup, auto-execution, and Python exit
code switches
([command-line arguments](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html)).
Use `--offline-mode` only for jobs that require no network access.
The Blender-side script should always write:

- the editable `.blend` with `bpy.ops.wm.save_as_mainfile`
  ([API contract](https://docs.blender.org/api/5.2/bpy.ops.wm.html#bpy.ops.wm.save_as_mainfile));
- representative stills/contact sheets and the review movie;
- a machine-readable validation/provenance manifest;
- captured Blender stdout and stderr;
- nonzero exit status for any failed invariant.

The outer Codex/Python process should own job paths, retries, hashing, comparison,
and final acceptance. Blender should be a deterministic compiler/renderer, not
the project tracker or orchestration database.

## Current local files

Generated outputs are local and intentionally live under the repository's
ignored `artifacts/` tree. The current main editable motion file is:

`/Users/samikd/MyProjects/PyBlend/artifacts/experiment_002_hybrid_character_motion/character_asset/animation-ready-v4-motion/animation_ready_wave_v4_exposure.blend`

Related locations:

- Main motion review bundle: `/Users/samikd/MyProjects/PyBlend/artifacts/experiment_002_hybrid_character_motion/character_asset/animation-ready-v4-motion/`
- Current semantic/static review: `/Users/samikd/MyProjects/PyBlend/artifacts/experiment_002_hybrid_character_motion/character_asset/animation-ready-v4-static/`
- Bounded editability proofs: `/Users/samikd/MyProjects/PyBlend/artifacts/experiment_002_hybrid_character_motion/character_asset/animation-ready-v4-editability/`
- Versioned Blender build scripts: `/Users/samikd/MyProjects/PyBlend/experiments/002_hybrid_character_motion/character_asset/`

To follow a run, inspect `blender_stdout.log`, `blender_stderr.log`, and the JSON
validation in its artifact folder; review the contact sheet/movie; then open the
`.blend` in Blender for the object/layer/timeline check. The saved file—not the
state of an MCP or UI session—is the reviewable Blender deliverable.

## Adoption trigger

Do not install MCP for the current ticket. Reconsider it when PyBlend needs
Creator-approved changes to an already-open Blender scene, live viewport
navigation, or interactive diagnosis that cannot be expressed cleanly as an
input manifest and a repeatable background run. Even then, keep the CLI pipeline
as the promotion gate.
