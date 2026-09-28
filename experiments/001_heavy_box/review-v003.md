# Heavy Box — first motion preview

Status: **ready for user review as a rough animation**, not final production acceptance.

[Play the silent 10-second preview](artifacts/rough-v003/preview.mp4) · [Editable Blender project](artifacts/rough-v003/character-and-motion.blend) · [Contact sheet](artifacts/rough-v003/contact-sheet.png)

## What exists

C's oval head, bean torso, flexible limbs, mittens, shoes and expressions have been rebuilt as native Blender vector artwork. No generated image plane is used in the animation. The concept sheets guide appearance and acting intent.

The character approaches, tries a push, widens its stance, pushes harder, loses balance as the box slides, catches itself and gives a suspicious look. One fixed camera, 240 frames at 24 fps, 1280×720 H.264, no audio.

Named hand, foot, body, head and bend controls have editable keyframes. Native curve drivers keep limbs attached to these controls. Facial lines also have editable animation. This is a simple curve character, not a Grease Pencil or Rigify rig. Limb arc length is intentionally elastic; bends are authored controls rather than a full anatomical constraint system. Dense per-frame keys are convenient for this generated rough, but broader hand animation may benefit from fewer authored keys.

## Review and verification

Inspected selected full-size renders, a chronological half-second contact sheet and a closer two-frame-step release sequence. The action is readable in those sequences. The latest pass removes the crossed opening arms, improves leg silhouettes and fixes a hand jump at release.

Remaining polish: the walk and recovery need a real-time timing review; effort could have more varied spacing and holds; one raised hand briefly overlaps the head during recovery. The finish is a rough acting proof. These observations do not certify production quality or substitute for the user's review of playback.

The reopened `.blend` passed independent checks on **all 240 frames**, with automatic Python execution disabled: hand-contour contact during pushing, fixed planted feet, attached limb endpoints, continuous hand release, visible geometry inside the camera and no external asset dependencies. Ground overlap is under 0.001 scene units (about 0.05 pixels at this resolution). Video inspection confirms exactly 10 seconds, 240 frames and no audio stream.

Evidence: [project checks](artifacts/rough-v003/verified-project.json), [video metadata](artifacts/rough-v003/verified-video.json), [frame hashes](artifacts/rough-v003/frames-manifest.json).

## What the journal preserves

- v001: rejected opening arm/leg silhouettes and approximate wrist contact.
- v002: improved silhouettes, but a contact-to-release discontinuity was found.
- v003: corrected release and full preview.
- First independent framing checker failed because Blender's curve bounding boxes overestimated the actual outline. Its source and log remain; the replacement checks evaluated mesh vertices and passes.

The append-only journal records source/artifact hashes, findings and decisions. No database or speculative production framework was added. This JSONL history remains suitable for later SQLite import.

## Reproduce and continue

From the project root, build into `artifacts/rough-v003` with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python experiments/001_heavy_box/scripts/build_v003.py -- --samples --render
```

Then encode `frames/frame-%04d.png` with FFmpeg at 24 fps, H.264, CRF 18, yuv420p, faststart and no audio. The exact creative tracks are in `shot-v003.json`; the construction and contact-release rule are in `scripts/build_v003.py`. The independent reopened-project check is `scripts/verify_v003_mesh.py`.

**Preserve reviewed versions:** copy source and shot to a new version and update their output paths before rebuilding changes. The command above reproduces the existing version and would overwrite its build outputs.

Next: review the video, then make a bounded second-push revision and verify that opening and ending frames remain unchanged. That revision test has not yet been performed. Voice repair and a second independent action remain later experiments.
