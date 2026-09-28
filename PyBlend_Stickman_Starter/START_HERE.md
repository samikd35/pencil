# PyBlend stickman starter materials

Copied from PyBlend on 9 September 2026. Originals remain in PyBlend.

1. Extract `Dawn_Training_Project.zip` here. It contains the editable Blender project, beginner guide, construction and pose checkpoints, artwork, references, production scripts, research notes, review images, verification records and rendered movie.
2. Open the extracted `Dawn_Training/BEGINNER_GUIDE.md`, then `Dawn_Training.blend`.
3. Read `docs/research/blender-platform-foundations.md` and `docs/research/blender-codex-integration.md` for the retained workflow and experiment index.
4. Earlier experiment reports are under `experiments/`. Broader platform plans are in `docs/adr/`, `docs/character-package-v2.md` and `.scratch/pyblend-v1-animation-authoring/map.md`.

Use the example's scene organization, named parts, bone controls, pose tests and render workflow as references for new stickman artwork. The existing film is a bounded cutout first cut, not a certified general stickman rig.

## Portability

Opening the packed Blender project does not require the build scripts. Rebuilding requires adapting the scripts' PyBlend folder assumptions and Desktop reference paths; preserve edited projects under new names because build scripts overwrite outputs. Existing document links may point back to PyBlend or additional files not included in this selected bundle. Historical plans and approval records belong to PyBlend and do not establish approval for a new Pencil production.
