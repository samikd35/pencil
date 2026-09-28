# Just Five Minutes — 30-second animation test

Status: user endorsed the script and explicitly directed matching the reference environment and characters on 11 September 2026. Revision v002 applies that visual direction. No animation has been built or rendered for this experiment.

## Purpose and format

Test whether the existing Pencil Blender-to-FFmpeg workflow can reproduce the character designs, environment, and animation treatment observed in `/Users/samikd/Downloads/Meesha Final.mp4`: notebook line art, recognizable simple characters, held poses, facial replacements, short gestures, whole-drawing transforms, graphic effects, and comic editing.

Original fictional everyday comedy; this is a format experiment, not a football incident or factual educational explanation. It does not select a channel niche.

Proposed delivery: exactly 30 seconds, 1920×1080 landscape, 30 fps / 900 frames. Landscape preserves the reference's space for side entrances and text. Match the reference: white paper with faint grey horizontal rules, thin black outlines, black hair, white faces and shirts, dark shorts, and selective flat colour. Retain the reference desk's grey top, orange legs, black office chair, and desktop monitor. Use red for emphasis in the new captions. No voiceover or spoken dialogue for this test; short on-screen text carries the setup and punchline. Original Foley can support the action, but the silent picture must remain understandable.

## Timed visual script

Times are half-open intervals; frame ranges are inclusive at 30 fps.

| Time | Frames | Picture and acting | On-screen text | Animation technique / sound cue |
| --- | --- | --- | --- | --- |
| 0–3 s | 1–90 | Medium shot. Our protagonist smiles confidently at the viewer and lifts one finger. The reference-style grey desk with orange legs, desktop monitor, mouse, and black office chair sits beside him. | WORK STARTS NOW. | Hold the body; eyebrow lift, blink, short arm gesture. Light text pop. |
| 3–6 s | 91–180 | Phone vibrates on the desk. His pupils move toward it before his head follows. He reaches for it, replacing confidence with a guilty smile. | None. | Eye lead, head turn, hand-to-phone contact. Two small drawn vibration marks; buzz and pickup tap. |
| 6–10 s | 181–300 | A second character leans into frame from the left, oversized in the foreground, with one eyebrow raised. The protagonist looks toward the friend and points confidently at his excuse. The friend rolls their eyes and slides out. | JUST 5 MINUTES. | Whole-character slide/rotation; clear eye-line exchange; two facial changes; held pointing pose. Short entrance swish. |
| 10–15 s | 301–450 | Cut to a seated three-quarter view. He scrolls happily with the phone held in one hand; the computer remains untouched. A clock graphic enters the empty side of frame and its hands begin turning quickly. | None. | Repeated small thumb movement and a few facial changes; rotating clock hands. Sparse taps and accelerating ticks. |
| 15–19 s | 451–570 | Keep the same seated composition. Clock disappears and a red time card lands beside him. He continues scrolling for a beat, then freezes with thumb raised as he notices the card. | 3 HOURS LATER | Graphic pop with brief overshoot; delayed eye movement; freeze the scrolling loop. End the ticking abruptly. |
| 19–23 s | 571–690 | Punch into his face. Eyes widen, mouth opens, then eyelids droop. Pull back enough to reveal slumped shoulders and a tiny stretch. | None. | Three distinct expressions; a short body settle rather than continuous idle movement. Small chair creak. |
| 23–27 s | 691–810 | Medium shot. He puts the phone down beside the untouched computer, turns to the viewer, and raises an open palm with complete seriousness. | I NEED A BREAK. | Clear release of the phone; head turn; replacement arm pose. Text appears after the expression is readable. |
| 27–30 s | 811–900 | Wide shot. He turns away and rapidly retreats, shrinking toward the centre with a couple of running poses and a small dust puff. The desk remains. The original WORK STARTS NOW card is still beside the untouched computer. Hold the empty result for the last second. | WORK STARTS NOW. | Whole-drawing scale/position animation, two or three retreat poses, drawn dust effect. Quick footsteps and puff; quiet final hold. |

## Character and asset scope

- Reconstruct the reference protagonist and curly-haired friend as editable drawings. Match their particular hair contours, face outlines, eyes, noses, mouths, necks, shirt shapes, limbs, shorts, and feet. Do not substitute newly designed mascots. Keep the chosen reference proportions and stroke treatment consistent across shots.
- Protagonist expressions: confident, guilty, amused, startled, exhausted, and earnest. Friend: skeptical and eye-roll. Mouth changes communicate emotion rather than simulated speech.
- Protagonist views: front/three-quarter standing, three-quarter seated, and back for retreat. The friend needs one leaning view with facial variants.
- Reconstruct the reference desk setup: grey tabletop, orange legs, desktop monitor, wired mouse, and black office chair. Match the drawn phone treatment. Add a clock graphic and four text cards in the same drawing language, plus vibration marks and a dust effect. Reuse the desk composition between shots.
- The video is the direct visual target, not loose inspiration. The script and actions are new; recognizable character designs, environment, linework, palette, and limited-animation treatment must closely match the supplied video. Rebuild editable assets rather than treating extracted footage as the finished animation.

## Specific visual targets

Use the original video at these approximate times as the visual authority:

| Element | Reference | Match requirements |
| --- | --- | --- |
| Protagonist front and gestures | 0:08–0:18 and 0:28–0:39 | Large solid-black high hair silhouette, tapered rounded white face, expressive paired eyes and brows, simple outlined nose and mouth, narrow neck, boxy white shirt, dark shorts, thin outlined limbs, black feet. |
| Curly-haired friend and entrance | 0:19–0:25; group view around 1:11–1:19 | Use the curly-haired supporting character, including face and hair proportions. Match the edge intrusion, tilt, overlap, and comic scale change. |
| Desk environment | Around 1:00–1:01, 1:28–1:30, and 1:51–1:58 | Grey desktop, orange supports, black rounded office chair, simple monitor and mouse, thin outlines, white ruled-paper field, abundant empty space. |
| Phone | Around 1:25 | Simple outlined handset and hand, flat screen blocks; adapt screen content only as the new story needs. |
| Retreat and effects | Around 0:05–0:07 | Back-view hair silhouette, shrinking figure, economical running/tumbling drawings, hand-drawn movement marks, and grey dust puff. |
| Captions and graphic emphasis | Around 0:32–0:38 and 2:02–2:03 | Irregular handwritten lettering and bold red graphic emphasis; match visual weight and spacing, while using the new script's words. |

The source protagonist varies between sections. Anchor the front design to the early standing/gesturing sequence; use later desk and back views for construction evidence while preserving that chosen identity. New seated angles must look like the same character. Treat this as matching a specific model from the video, not averaging the early and late designs into a new character.

Keep the paper background flat and lightly ruled, without adding a room, scenic lighting, dimensional materials, or decorative scenery. Match the reference's restrained drawing changes and quick graphic movement. Its sparse animation is part of the target.

## Fit with the existing pipeline

The existing implementation provides the mechanisms needed, but this experiment's visual match is not yet demonstrated:

- `../001_heavy_box/artifacts/finish-v002/character-and-effects.blend`: source for editable character controls and limb mechanics. Preserve the original file and delivery.
- `../002_procrastination/scripts/build_animatic_v001.py`: existing held-pose keys, expression changes, flat shapes, clock movement, and camera framing. Its old artwork and timings do not govern this film.
- `../005_three_goals/scripts/build_film.py`: demonstrates replacing head/body artwork while retaining the existing motion controls, character groups, visibility keys, and orthographic framing.
- Existing render, sound, and FFmpeg delivery scripts provide the downstream workflow. Check their film-specific paths, frame rate, and dimensions before reuse.

New work is primarily faithful reconstruction of the reference character and environment drawings, scene poses, phone contact, and the timing of holds versus brief movement. The existing rig is an implementation aid: adapt or replace its visible geometry wherever needed to achieve the reference silhouettes and proportions. Earlier Pencil character artwork, colours, and shading do not govern this test. Use stepped keys for replacement drawings; use interpolated keys for entrances, clock hands, camera changes, and retreat. Avoid applying smooth interpolation indiscriminately to every pose.

## What the rendered test should establish

1. The setup, elapsed-time reveal, and punchline read with audio muted.
2. Side-by-side comparisons with the specific source frames establish close agreement in character silhouette, facial construction, proportions, line weight, background rules, desk shapes, and palette. Identity stays consistent through front, seated, and back views.
3. Held bodies feel intentional because eyes, gestures, and cuts direct attention; continuous idle animation is unnecessary.
4. Phone pickup and release have visible contact, and the scroll loop does not detach the thumb or phone from the hand.
5. The side entrance, face close-up, clock graphic, and retreat reproduce the reference's visual vocabulary without relying on elaborate scenery.
6. The final video decodes to exactly 900 frames / 30 seconds, and the saved Blender project retains editable artwork and motion.

Technical validity and resemblance to the reference are separate checks. A completed render alone will not establish a successful style match.
