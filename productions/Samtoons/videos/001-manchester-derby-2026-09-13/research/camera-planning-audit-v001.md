# Camera planning for the Samtoons repair

Prepared 15 September 2026. **Research and proposed treatment; no camera changes or animation tests were performed for this report.** Sources are first-party educational resources and this production's existing files. Film-specific recommendations below are our proposed direction, not claims about how 442oons built its film.

## Finding

The film needs stronger **visual coverage**: establishing the situation, showing decisive contact, revealing the result, and letting a face or prop deliver the joke. Adding continuous movement to every shot would not solve that problem. Camera movement should follow attention or reveal information; the existing camera code instead adds the same small ending push to most new scenes.

The earlier [reference study](../../../research/reference-analysis.md) explicitly identified wide action shots alternating with face/prop inserts and reactions. It did not establish that the benchmark uses elaborate camera movement throughout. Its sampled 56.1–58.0-second goal sequence makes approach, ball departure, keeper dive and outcome readable; the lesson is coordinated staging and timing. Its limits remain: sampled sequences, not an exhaustive frame-by-frame or audible review.

Local source evidence:

- [build_dramatic_actions.py](../scripts/build_dramatic_actions.py), `camera_keys`, lines 59–67: all initial camera keys use `CONSTANT` interpolation. These are cuts between viewpoints, not flowing moves.
- [finalize_animatic.py](../scripts/finalize_animatic.py), lines 63–71: most new scenes receive a 0.16-unit forward move over their final 72 frames, with Bezier interpolation. This is a blanket treatment rather than a beat-specific camera decision.
- [construction.md](../../../../../pipeline/styles/construction.md) already requires checking new angles and adding missing views or pose corrections. [The benchmark](../assets/benchmark-v001.md) already requires readable contact and purposeful edits. We need to apply those requirements to each new shot, not invent a new renderer.

## Terms we should keep separate

| Choice | What it means | Proposed use here |
|---|---|---|
| Shot size | How much the frame includes: wide, medium, close-up, detail insert. | Wide for player/ball/goal geography; medium for interacting bodies; close-up for a change in expression; insert for letter or card. |
| Camera angle | Where we view the action from: eye level, lower, higher, frontal, side, three-quarter. | Side/three-quarter for readable kicking legs; modest high view for goal-area relationships; lower view for Maguire's exaggerated heroic entrance. |
| Camera movement | A change within a shot: pan, tilt, track, push or pull. | Follow a run, redirect attention, or reveal a larger consequence. |
| Zoom | Lens/framing change from a fixed position, rather than physically approaching the actor. | A quick accent on sudden disbelief, if the drawing holds up at that size. |
| Cut / reaction insert | An immediate edit to another composition or reaction. | Show the post mocking Rashford after the clang; cut to Carrick after he reads the letter. |

Close-ups can emphasize faces or objects; their meaning depends on surrounding shots. Angles and movement are separate choices. Zoom changes apparent size without moving the camera. [Columbia: Close-Up](https://filmglossary.ccnmtl.columbia.edu/term/close-up/), [Camera Angle](https://filmglossary.ccnmtl.columbia.edu/term/camera-angle/), [Zoom Shot](https://filmglossary.ccnmtl.columbia.edu/term/zoom-shot/).

## A small useful camera vocabulary

| Technique | Definition and proposed storytelling use | Limit for this film |
|---|---|---|
| Pan / tilt | Turn the view horizontally / vertically. Follow attention from player to post, or reveal Maguire's head from his heroic stance. [Columbia](https://filmglossary.ccnmtl.columbia.edu/term/pan-shot/). | End on a composed frame; do not sweep past the actual contact. |
| Track / truck | Move with the subject, including a lateral move. Keep a runner readable while the environment passes. [Adobe's tracking lesson](https://www.adobe.com/creativecloud/video/production/cinematography/camera-shots-and-angles/tracking-shot.html). | Plan the actor and camera paths together; keep the ball's travel relative to the pitch apparent. |
| Push in / pull out | Move closer / farther away. Push toward a realization; pull back to expose the growing flood and Foden enjoying it. [Columbia: Dolly](https://filmglossary.ccnmtl.columbia.edu/term/dolly-dolly-shot/). | Use an authored start and end composition. A tiny automatic drift is not a reveal. |
| Crash / snap zoom | A very fast zoom for a sudden accent; proposed example: Rashford realizing the post has copied his gesture. This is a fast use of the zoom mechanism above. | Reserve it for a selected punchline. It magnifies weak drawing and cannot replace facial acting. |
| Whip / swish pan | A rapid, blurred move connecting attention between places. Proposed example: Bruno's shout to Oliver's exhausted face. [Columbia: Swish Pan](https://filmglossary.ccnmtl.columbia.edu/term/swish-pan/). | Do not blur the kick, parry or red-card direction the viewer needs to understand. |
| Locked reaction | Hold a deliberate composition while the character reacts. Proposed example: Carrick's deadpan response. | The pose, eyes and pause must change meaning; prolonged idle animation does not become a joke because the camera is still. |

Adobe's lesson recommends deciding the narrative purpose in a shot list and rehearsing camera and cast together. We can apply that principle without buying Adobe software. [Adobe](https://www.adobe.com/creativecloud/video/production/cinematography/camera-shots-and-angles/tracking-shot.html).

## Flat characters impose a real design constraint

Multiplane animation places flat drawings at different depths; camera travel then produces parallax. It gives depth to a scene but does not supply the unseen sides of a character. [Toon Boom: What is a multiplane?](https://helpcentre.toonboom.com/hc/en-ca/articles/51906223976339-What-is-a-multiplane).

**Our application/inference:** a front-facing drawing cannot become a convincing side or back view just because Blender's camera moves around it. An orbit can expose thin edges, separated layers and incorrect overlaps. The supplied Mainoo-shot screenshot's edge-on background player is the kind of failure to prevent. New camera angles require the appropriate character drawing/view, a suitable native construction, or a separately composed shot. Rotating every sprite to face the camera can preserve visibility but still give incorrect body direction and contact.

Keep the useful 3D pitch and goal perspective; choose a limited set of authored character views for each required shot. Allow modest depth movement where it passes visual review. Require new drawings when the planned action demands foreshortening or a turn. Do not force every character into the same frontal pose to accommodate the rig.

## Proposed coverage for the repair

These are shot intentions, **not a tested timing lock**. Preserve approved acting and sound where they still fit. The umbrella remains removed.

| Beat | Proposed coverage and sound relationship |
|---|---|
| Foden / Bruno | Retain the approved readable contact staging. Keep both bodies and the ground visible for the kick and fall. Move attention to Bruno's protest only after the physical consequence is clear. Show Oliver's card aimed toward Foden with face and card readable together. A reaction cut may be stronger than another zoom. |
| Rashford free kick | Establish wall, keeper, goal and ball. Use a side/three-quarter action frame that shows the planted foot, striking foot and release. Follow the ball briefly or cut to its arrival at the post. Clang, short registration pause, then Rashford's premature temple gesture becoming a scratch. Give the post's imitation its own readable composition. |
| Mainoo / second post | Maintain direction from shot to post to rebound. Include keeper and rebound destination together for the possession change. Then a medium post/keeper frame reveals the scarf and contract gag. Cut to Bruno for the renewed complaint. |
| Goal / VAR dispute | Establish relevant attackers, defender and keeper with separation. Show the touch/deflection and final finish before the celebration reversal. A close insert clarifies the flag or decision; the following reaction should show who objects and whom they point at. A wide tableau of stationary people is insufficient coverage. |
| Lammens save / Maguire miss | Show keeper anticipation, hand contact and deflection in one readable action passage. For Maguire, a brief low-angle heroic reveal can set up the joke, followed by a clear wider header-to-wide outcome and an embarrassed reaction. Do not use a camera cut to conceal missing body action. |
| Mbeumo / Donnarumma | Preserve the approved parry mechanics. A closer anticipation shot can intensify hope; keep the actual shot, glove contact and ball departure legible. Let the keeper/Haaland reaction support the wolf joke through acting, not ears alone. |
| Apology / final reveal | Medium two-shot: Oliver visibly carries and transfers the letter. Brief insert: readable SORRY / OUR MISTAKE. Oliver releases it; then the crying starts. Carrick reads, crumples, bins it; hold his dry response. Only afterward pull back to reveal the growing water and fishing Foden. Place Foden's line after the reveal has registered. |

Maintain a consistent action axis through each kick/save exchange. Opponents should keep intelligible screen positions and gaze directions. If changing sides of the action, re-establish geography deliberately rather than accidentally reversing the ball's direction. This applies Columbia's continuity convention; it is not a prohibition on expressive exceptions. [Columbia: 180-Degree Rule](https://filmglossary.ccnmtl.columbia.edu/term/180-degree-rule/).

## Minimal addition to the existing planning process

For each consequential shot, add these decisions to the current audiovisual plan: **what the viewer must notice; opening and closing composition; size and angle; movement or deliberate hold; action axis; required character views; cut/move trigger tied to the action or sound.** Use named contact/reveal events already supported by the pipeline. No camera database, new software or extra approval ladder is needed.

Review the planned first frame, contact/peak frame and ending frame; then inspect every intervening frame of demanding movement and watch the passage at normal speed. Check visibility, silhouettes, plant/contact, view compatibility and continuity across cuts. Camera easing, drawing count and frame rate should serve the chosen timing; neither a higher frame count nor extra camera motion guarantees energy. A purposeful deadpan pause should remain, while unmotivated waiting should be removed or replaced by real performance.

Next implementation order: agree the repair coverage, correct the affected bodies, stage these camera/action combinations in the actual film shots, retime the performance, then re-synchronize the retained sound. This report establishes a plan to test, not a claim that the current camera or animation has been repaired.
