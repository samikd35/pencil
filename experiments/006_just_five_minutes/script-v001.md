# Just Five Minutes — 30-second animation test

Status: script draft. No animation has been built or rendered for this experiment.

## Purpose and format

Test whether the existing Pencil Blender-to-FFmpeg workflow can reproduce the visual techniques observed in `/Users/samikd/Downloads/Meesha Final.mp4`: notebook line art, recognizable simple characters, held poses, facial replacements, short gestures, whole-drawing transforms, graphic effects, and comic editing.

Original fictional everyday comedy; this is a format experiment, not a football incident or factual educational explanation. It does not select a channel niche.

Proposed delivery: exactly 30 seconds, 1920×1080 landscape, 30 fps / 900 frames. Landscape preserves the reference's space for side entrances and text. Use monochrome drawings on faint ruled paper, with red accents. No voiceover or spoken dialogue for this test; short on-screen text carries the setup and punchline. Original Foley can support the action, but the silent picture must remain understandable.

## Timed visual script

Times are half-open intervals; frame ranges are inclusive at 30 fps.

| Time | Frames | Picture and acting | On-screen text | Animation technique / sound cue |
| --- | --- | --- | --- | --- |
| 0–3 s | 1–90 | Medium shot. Our protagonist smiles confidently at the viewer and lifts one finger. A simple desk and open laptop sit beside him. | WORK STARTS NOW. | Hold the body; eyebrow lift, blink, short arm gesture. Light text pop. |
| 3–6 s | 91–180 | Phone vibrates on the desk. His pupils move toward it before his head follows. He reaches for it, replacing confidence with a guilty smile. | None. | Eye lead, head turn, hand-to-phone contact. Two small drawn vibration marks; buzz and pickup tap. |
| 6–10 s | 181–300 | A second character leans into frame from the left, oversized in the foreground, with one eyebrow raised. The protagonist looks toward the friend and points confidently at his excuse. The friend rolls their eyes and slides out. | JUST 5 MINUTES. | Whole-character slide/rotation; clear eye-line exchange; two facial changes; held pointing pose. Short entrance swish. |
| 10–15 s | 301–450 | Cut to a seated three-quarter view. He scrolls happily with the phone held in one hand; the laptop remains untouched. A clock graphic enters the empty side of frame and its hands begin turning quickly. | None. | Repeated small thumb movement and a few facial changes; rotating clock hands. Sparse taps and accelerating ticks. |
| 15–19 s | 451–570 | Keep the same seated composition. Clock disappears and a red time card lands beside him. He continues scrolling for a beat, then freezes with thumb raised as he notices the card. | 3 HOURS LATER | Graphic pop with brief overshoot; delayed eye movement; freeze the scrolling loop. End the ticking abruptly. |
| 19–23 s | 571–690 | Punch into his face. Eyes widen, mouth opens, then eyelids droop. Pull back enough to reveal slumped shoulders and a tiny stretch. | None. | Three distinct expressions; a short body settle rather than continuous idle movement. Small chair creak. |
| 23–27 s | 691–810 | Medium shot. He puts the phone down beside the untouched laptop, turns to the viewer, and raises an open palm with complete seriousness. | I NEED A BREAK. | Clear release of the phone; head turn; replacement arm pose. Text appears after the expression is readable. |
| 27–30 s | 811–900 | Wide shot. He turns away and rapidly retreats, shrinking toward the centre with a couple of running poses and a small dust puff. The desk remains. The original WORK STARTS NOW card is still beside the untouched laptop. Hold the empty result for the last second. | WORK STARTS NOW. | Whole-drawing scale/position animation, two or three retreat poses, drawn dust effect. Quick footsteps and puff; quiet final hold. |

## Character and asset scope

- Two original characters with distinct black hair silhouettes. Use simple outlined shirts, thin limbs, dark shorts, and white faces. Keep each character's proportions and stroke treatment consistent across shots.
- Protagonist expressions: confident, guilty, amused, startled, exhausted, and earnest. Friend: skeptical and eye-roll. Mouth changes communicate emotion rather than simulated speech.
- Protagonist views: front/three-quarter standing, three-quarter seated, and back for retreat. The friend needs one leaning view with facial variants.
- One desk setup, laptop, phone, clock graphic, four text cards, vibration marks, and a small dust effect. Reuse the desk composition between shots.
- The reference guides format and technique; exact character drawings and footage are not required for this original test.

## Fit with the existing pipeline

The existing implementation provides the mechanisms needed, but this experiment's visual match is not yet demonstrated:

- `../001_heavy_box/artifacts/finish-v002/character-and-effects.blend`: source for editable character controls and limb mechanics. Preserve the original file and delivery.
- `../002_procrastination/scripts/build_animatic_v001.py`: existing held-pose keys, expression changes, flat shapes, clock movement, and camera framing. Its old artwork and timings do not govern this film.
- `../005_three_goals/scripts/build_film.py`: demonstrates replacing head/body artwork while retaining the existing motion controls, character groups, visibility keys, and orthographic framing.
- Existing render, sound, and FFmpeg delivery scripts provide the downstream workflow. Check their film-specific paths, frame rate, and dimensions before reuse.

New work is primarily the character drawings, ruled-paper treatment, scene poses, phone contact, and the timing of holds versus brief movement. Use stepped keys for replacement drawings; use interpolated keys for entrances, clock hands, camera changes, and retreat. Avoid applying smooth interpolation indiscriminately to every pose.

## What the rendered test should establish

1. The setup, elapsed-time reveal, and punchline read with audio muted.
2. Character identity, proportions, and line weight remain stable through the front, seated, and back views.
3. Held bodies feel intentional because eyes, gestures, and cuts direct attention; continuous idle animation is unnecessary.
4. Phone pickup and release have visible contact, and the scroll loop does not detach the thumb or phone from the hand.
5. The side entrance, face close-up, clock graphic, and retreat reproduce the reference's visual vocabulary without relying on elaborate scenery.
6. The final video decodes to exactly 900 frames / 30 seconds, and the saved Blender project retains editable artwork and motion.

Technical validity and resemblance to the reference are separate checks. A completed render alone will not establish a successful style match.
