# Dawn Training — start here

Open **Dawn_Training.blend** in Blender 5.2. The finished film is **Dawn_Training.mp4**: 1920 × 1080, 24 fps, exactly 30 seconds, with original synthesized atmosphere and action sounds.

This is a reference-based Grease Pencil cutout production. The character's visible artwork consists of editable vector drawings, not a textured plane. The seven supplied-view/pose interpretations share clear control names. Large silhouette changes use alternate drawings from the user's sheets; ordinary motion uses bone animation.

## First five minutes

1. Choose **DT_03_DAWN_TRAINING** in Blender's scene selector at the top right.
2. Press **Numpad 0** to see the active camera. Without a numpad, use **View → Cameras → Active Camera**.
3. Press **Space** to play. The timeline runs from frame **1** to **720**. Camera markers divide the six shots.
4. Switch to **DT_01_CHARACTER_STUDIO** to inspect an independent, neutral character.
5. In the Outliner, select **DT_STUDIO_RIG_FRONT**. Turn viewport overlays on if the bones are hidden, enter **Pose Mode**, select `forearm.L`, then press **R**, **Z**, and move the mouse. Press **Esc** to cancel the experiment or **Alt-R** to reset that bone's rotation.

The studio copy is separate from the film, so practice changes there do not alter the film's animation.

## 1. Setup and reference

All five original sheets are packed in the Blender project as image-reference empties in **DT_References | locked, non-rendering**. They are excluded from the render, locked against accidental selection, and shown at 35% opacity when enabled. Enable the collection in the Outliner to inspect them. Hide all but the sheet you need.

The character drawings face a camera on the +Z axis and lie in the XY plane. This makes cutout posing a simple **R Z** rotation. The attached sheets establish the artwork and proportions; text printed inside those sheets is supporting context, not an additional instruction source.

## 2. Drawing

Select **DT_STUDIO_GP_FRONT**. Its named layers contain the source-derived contours, flat colors, ink and cel-shadow shapes. Choose a layer, enter **Edit Mode** to edit its control points, or **Draw Mode** to add strokes. The imported artwork uses per-curve fill colors; material changes alone do not replace every existing traced color.

The main neutral drawing has separate layers for:

- Hair and head.
- Left/right eyes, eyebrows, and mouth.
- Torso, left/right upper arms, forearms, hands and wristbands.
- Waist sash and sash tail.
- Left/right pants, shin wraps and feet.

`HiddenJoint_*`, `SkinUnder_*` and the power-up pelvis overlap are deliberately underneath the visible artwork. They cover exposed attachment areas during movement. The source sheets are modest in resolution; this conversion preserves their design, but it is not a claim of a new hand-inked, resolution-independent master drawing. Very large close-ups can reveal source-derived contour detail.

## 3. Rigging

Each drawing has a simple armature with matching bone names. Grease Pencil layers use native **Parent / Bone** relations. There are no automatic weights, IK/FK switching systems, simulation requirements or custom playback handlers.

- Move the **armature object** in Object Mode to place the whole character.
- Rotate individual bones in Pose Mode with **R Z**.
- Keep X/Y bone rotations locked so the artwork remains in its drawing plane.
- Use small rotations around an existing pose. Major turns and extreme new actions need a new drawing or a local correction.

For the front and focus rigs, **Object Properties → Custom Properties** provides:

| Control | Values | Result |
|---|---|---|
| Blink | 0–1 | Open eyes to closed eyes |
| BrowFocus | −1–1 | Subtle eyebrow tilt |
| MouthOpen | 0–1 | Neutral mouth to simple open mouth |
| Smirk | 0–1 | Adds the confident smile line |

Keyframe a control by hovering over its value and pressing **I**. Body controls can be keyed with **I → Rotation** in Pose Mode. These are simple cutout facial controls, not a lip-sync or full facial deformation system.

## 4. Pose testing

Choose **DT_02_POSE_TESTS**. It contains standing, sitting, running, crouching and power-up drawings under equivalent named controls. Play frames **1–37** to inspect small head and arm movements around each pose. The examples test each pose-specific cutout; they do not claim that one front drawing can rotate smoothly into every view.

Use **review/pose_tests.png** for the overview. The seated reference's seat is retained as supporting pose context; the film itself uses the plateau environment.

## 5. Blocking and shot timing

| Time | Frames | Shot and editable character |
|---|---|---|
| 0:00–0:05 | 1–120 | Sunrise wide shot, `DT_RIG_BACK` |
| 0:05–0:10 | 121–240 | Focus close-up, `DT_RIG_FOCUS` |
| 0:10–0:15 | 241–360 | Run across the plateau, `DT_RIG_RUN` |
| 0:15–0:20 | 361–480 | Leap and power-up, `DT_RIG_POWER` |
| 0:20–0:25 | 481–600 | Directed energy blast, `DT_RIG_RUN` |
| 0:25–0:30 | 601–720 | Crouch landing, then `DT_RIG_FRONT` |

The run combines root travel with a repeating 16-frame leg/arm cycle. Contact samples align the lower foot to the plateau during contacts. The leap, recoil and recovery use a few clear key poses. Camera changes are bound to timeline markers; the modest zooms are on camera `Orthographic Scale`.

The file **stages/05_blocking.blend** preserves the rig animation and cameras with effects and titles disabled. It is useful for judging body motion without effects.

## 6. Polish

The environment is a lightweight collection of emission-colored meshes: continuous sunrise gradient, clouds, layered mountain silhouettes, rock pillars, plateau surface and cracks. Lighting is deliberately graphic so the character's reference palette stays consistent.

The **DT_FX** collection contains editable energy arcs, aura, speed lines, dust, levitating stones, practice-target rings, fragments and blast geometry. The beam is staged from the evaluated firing hand toward the target. The sound track is an original procedural WAV, also packed in the project; cue times are listed in **sound_cues.json**.

The animation intentionally uses limited cutout motion and drawing substitutions. Further hand-drawn cleanup, richer in-betweens and nuanced acting can be added on top of this complete first cut.

## 7. Render and export

For a still image: select the film scene, choose a frame, and press **F12**.

For all frames: **Render → Render Animation**. The project uses PNG output under `frames/`, which allows interrupted renders to be recovered. The video sound strip is present, while sequence rendering is disabled so Blender renders the shot cameras.

To encode the rendered frames and supplied soundtrack into the movie, run from this output folder:

```sh
ffmpeg -y -framerate 24 -i frames/frame_%04d.png -i Dawn_Training_Sound.wav -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -t 30 -movflags +faststart Dawn_Training.mp4
```

Save your own edited copy before rerunning any build script: the reproducible authoring scripts regenerate this experiment's output files.

## Files to keep

- **Dawn_Training.blend** — final editable project, packed references and sound.
- **Dawn_Training.mp4** — complete film.
- **Dawn_Training_Sound.wav** — editable audio master.
- **stages/03_drawing_and_rig.blend** — character construction checkpoint.
- **stages/04_pose_tests.blend** — pose testing checkpoint.
- **stages/05_blocking.blend** — animation checkpoint without FX/titles.
- **geometry/** — named SVG drawings and source/part manifest.
- **references/** — unchanged source images.
- **review/** — character, pose and shot inspection images.
- **build_report.json**, **render_report.json**, **validation.json** — runtime and verification records.

Research and reproducibility notes are in `experiments/011_dawn_training/README.md` and `RESEARCH.md` in the PyBlend repository, with copies under `production_scripts/` in the ZIP. The scripts expect the documented PyBlend folder layout; opening and editing the packed Blender project does not require those scripts.
