# Box-push hand visibility revision

User request: implement the hand-positioning fix and revise the existing box-pushing test. The existing chibi clip supplies the direct comparison. This is a 10-second, 640×360, 24fps review proof; all earlier deliveries remain unchanged.

The old compositor put both arms below the body. The revised compositor gives the near arm/sleeve and hand their own foreground passes. The old derived shoulder sides were crossed relative to the resting hands; those attachments are corrected. The near arm stays above the face throughout this shot, so it visibly crosses the large head during recovery. That is deliberate occlusion, with no draw-order switching. The rear arm can still pass behind the body/head. Different props or turns require authored ordering.

`checks.json` verifies all 240 original control poses, including the hand and elbow controls; identical hand/foot geometry; continuous limb endpoints; valid drivers; and a live hand edit after saving/reopening. Upper-arm geometry changes with the corrected shoulders. Layering itself leaves the corrected arm and sleeve geometry identical. Checks evaluate the non-rendered `Character editing` view layer so excluded render-pass objects do not produce stale coordinates.

The encoded full-action overview, walking frames 1–45 every two frames, consecutive push frames 103–110, and every recovery/settle frame 150–197 were visually inspected. The near hand reads in front at rest, both hands remain joined to the reaching arms, and the near arm stays visible across the head during recovery. No new contact gap or layer pop was observed in those intervals. The cropped release sheet trims some hands; `release-full-frames.png` is the complete view. This is frame-sequence review, not claimed real-time playback or listening. User playback remains the creative review.

`delivery-checks.json` verifies both movies decode, contain 240 video frames at 24fps, and last 10 seconds. Original AAC packets were copied; both their hash and decoded PCM hash match the old movie exactly. The original sound plan and mix remain in `proofs/workflow-v001/chibi/`.

Fresh builds of flat-vector and expressive-stickman also pass all 240 connection/control/contact checks and their native stills were inspected. The common builder, shared construction guide and pinned helper handling are updated. Older catalogue samples and pinned selections are preserved; this does not claim all styles have new motion proofs.

Reproduce from the Pencil workspace, choosing a new output directory:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b -t 4 --python experiments/009_style_gallery/revise_hand_layers.py -- --out NEW_DIRECTORY
/Applications/Blender.app/Contents/MacOS/Blender -b -t 4 --python experiments/009_style_gallery/revise_hand_layers.py -- --out NEW_DIRECTORY --render
```

`package_hand_fix.py` records the exact FFmpeg mux/comparison commands and audio/video assertions used here. Its paths identify this preserved revision; change its output path for a new run. `python3 pipeline/test_styles.py` also checks that a changed pinned layering helper is rejected on resume.
