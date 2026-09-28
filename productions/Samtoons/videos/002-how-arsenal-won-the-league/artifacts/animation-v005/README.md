# v005 — live rebuild after v004 rejection

**Work in progress, not a replacement finished movie.** The user rejected v004's static-pose assembly and corrected the blanket use of action drawings. Its 34 shots no longer count as completed animation.

## What is implemented

- All seven narrator/Ferguson scenes link the **same** native room collection. Desk, chair, lamp, television and walls retain physical positions across cameras. The dark-to-reveal camera matrices match exactly.
- Five seated appearances use a fitted continuous artwork mesh and native joint controls adapted from video001's constrained-bone construction. The head remains part of the same drawing. Seated support stays fixed while torso/head/arms move, with individual shot amplitudes and a restrained recognition pause.
- The active project is authored through the connected, visible Blender instance in short batches. The previous unsaved workspace was preserved in `live-before-v005.blend`. `narrator-room-v005.blend` is the current saved work.
- `production.json` now maps all 56 shots to a construction choice, reason and environment. Native articulated parts, fitted skin, hybrid action drawings and previously approved clips have different scopes.

## What is not complete

Ferguson's rise, shouting/throw performance and the remaining film reconstruction are not finished. The two corresponding room scenes currently contain the shared set, not a finished character performance. The seated rig does not validate these extreme actions. The environment is a working set; final art direction/lighting and the complete audiovisual film still need review.

Native checks cover shared collection identity, dark/reveal camera identity, five rest-pose skin bindings, joint lengths throughout motion and fixed lower support. Viewport frames were inspected. Those checks and launching playback are not normal-speed creative acceptance or proof of heard sound.

`build_narrator_room_v005.py` exposes `build_room()` and `rig_seated(shot, rear=..., dark=...)` for additive live batches; do not invoke it as a scene-resetting background builder. `check_narrator_room_v005.py` checks the implemented scope. The movie has not been re-exported or promoted to approved animation.
