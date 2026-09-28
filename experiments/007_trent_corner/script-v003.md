# Barcelona wasn't ready. Trent was. — advanced stickman revision

11 September 2026. Responds to the user's request for fictional sleeping-player/body-part jokes, more appealing art (especially the field) and varied camera angles. This supersedes the v001 treatment and the full-bodied v002 concept board; the existing files remain a technical draft. Authored delivery: 38 seconds (912 frames at 24 fps), vertical, no narration or dialogue, original sound.

**Creative premise:** a verified moment of inattention, made visible through a short impossible cartoon cutaway. The football sequence retains Trent's walk away, change of direction, quick delivery, Origi's first-time finish and Liverpool's decisive 4–3 aggregate outcome. Sleeping heads/legs are invented gags, not claims about what happened at Anfield.

The old draft's shortcomings: figures occupy too little of the frame; the repeated crowd pattern and large text margins compete with the action; pitch depth and light are weak; most acting uses similar frontal poses; one camera carries nearly the whole film. A camera change alone will not repair those weaknesses. The new version uses illustrated heads, a painted stadium panorama and native 3D stickman construction.

## Revised picture-and-sound script

| Shot / beat | Time | Picture and camera | Sound and sync | Review question |
|---|---|---|---|---|
| S01 / B01 | 0–2 s | Low corner-level close-up: a white ball, textured turf, red pennant and Trent's boot. Goal and waiting players fall into depth. Brief “WHO'S READY?” | Stadium surrounds us, flag cloth and a tiny turf scuff. Stop-time accent at 2 s. | Does the opening feel like a football scene immediately? |
| S02 / B02 | 2–4 s | Time visibly freezes. Cut tight to a representative Barcelona defender. His sleeping head rests on an impossibly tiny shoulder pillow; little sleep puffs escape. “CARTOON TIME” marks the invented cutaway. | One short comic snore, distant crowd almost disappears. The snore accompanies the pillow pose and drifting puffs. | Does the impossible prop make this an obvious comic exaggeration? |
| S03 / B03 | 4–6 s | Cut lower: another defender's upper body is alert and pointing, but his knees have droopy eyelids and his socked legs are asleep. The knees bend downward beneath two oversized closed eyes and a small “z z z”; the caption reads “KNEES: ASLEEP.” Keep the same one-joke premise; no unrelated gags. | Smaller answering snore and soft elastic knee-settle creak. | Is “only part of him is ready” readable in one glance? |
| S04 / B04 | 6–9 s | Snap back to ordinary stadium color and normal bodies. High three-quarter view establishes corner, goal and unmarked Origi. A small scoreboard: 79′, Liverpool 3–0, aggregate 3–3. No pillow, eyelids or sleep symbols remain. | Stadium returns sharply; no referee whistle or invented stoppage. | Is the geography clear and the fantasy visibly over? |
| S05 / B05 | 9–12 s | Medium shot: Trent steps away while Shaqiri approaches the corner. The flag and jersey number preserve the corner-taker identity across the cuts. | Grounded foot contacts; sparse tension pulse. | Does this preserve the real order of events? |
| S06 / B06 | 12–15 s | Low view along Trent's line of attention: Origi in space, goal beyond him, defenders still organising elsewhere. Trent fills the foreground, with Origi visible in the box. A brief separate shot shows Trent's focused expression. | Small observation motif; crowd narrows in perspective. No “evil mastermind” sting. | Does the audience see the opportunity before the pass? |
| S07 / B07 | 15–17 s | Low view of the pivot back to the ball, then cut on movement into the shared three-quarter view just before contact. The actual ball delivery starts here and stays continuous through the finish. | Turf plant, dry boot/ball thump at the authored contact. | Do the pivot and foot contact feel connected? |
| S08 / B08 | 17–20 s | Shared view: pass travels to Origi, defenders turn late, Origi meets it first time and scores. No gag obstructs the ball or alters the football. This shot holds the camera steady so ball travel remains legible. | Distinct finishing strike, net flutter, crowd release. Use named contact events exported from the final animation. | Can the viewer follow taker → ball → receiver → goal without reconstructing it across cuts? |
| S09 / B09 | 20–24 s | Origi celebrates in a closer, expressive view. Cut to a defender's startled face: eyelids spring wide, with a tiny disappearing sleep puff as an obvious graphic callback. Update 4–0 / aggregate 4–3. | Crowd cheer; one brief comic “wake-up” accent under it, without drowning the goal's release. | Does the callback reward the opening gag without stealing the goal? |
| S10 / B10 | 24–31 s | Explicit slow replay from the shared angle. Repeat the return, corner and finish at 0.75 times the main action speed. No sleeping gag on this explanatory pass. | Softer crowd; reuse selected kick/net takes against replay events, not newly regenerated sounds. | Can someone now explain what Trent exploited? |
| S11 / B11 | 31–38 s | Trent and Origi in a strong celebratory composition with the goal and stadium behind. “BARCELONA WASN'T READY. TRENT WAS.” Finish on Liverpool through, 4–3 on aggregate. | Warm resolving chord, cheer falling away, complete ending tail. | Does the title land as a payoff to both the joke and the real event? |

The native scene now contains this 38-second timeline. Main corner, finishing strike and net contact occur at frames 403, 433 and 448; replay contacts at 633, 673 and 693. `production.json` is the timing authority for all 29 sound cues. Retain verified historical sources in `brief.md`; those facts have not changed.

## Visual target

- Advanced stickman characters: narrow graphic jersey torsos, single-stroke black arms/legs with expressive elbows/knees, simplified articulated hands and football boots, and larger player-specific heads. No realistic muscular limbs or full-bodied human anatomy. Polish comes from posing, timing, deformation, facial acting, contact, composition and lighting. Trent and Origi should be recognisable through faces, 2019 hair and kits as well as their numbers. The user explicitly selected advanced stickman construction; individual designs remain an implementation choice within that direction.
- A convincing field plane with coherent touchline/endline/goal geometry, receding mowing bands, restrained turf texture, planted contact shadows and a consistent floodlight direction. Build it in 3D or as a controlled 2.5D scene so the new angles agree spatially.
- Deep emerald grass, charcoal/indigo stands, warm pale lights and Liverpool red as the visual anchor. Barcelona's striped shirts remain distinct. Keep texture strongest in the foreground and quiet behind faces.
- Group crowd masses into light and shadow shapes instead of drawing rows of identical symbols. Let the stadium support depth and scale.
- Fill the vertical frame with acting. Use a compact score overlay; reserve full-width type for the question and final payoff. Give body language time to read before introducing text.
- Use close-ups for jokes and attention, low views for physical action, and a shared wide view for the causal football sequence. Maintain screen direction and use the flag/goal as spatial anchors.

## Construction and implementation

Use one coherent native 3D field for camera changes and a deliberately graphic stickman cast. Keep thin ink-like limbs, narrow kit torsos, readable silhouettes and player heads. Native joints, face controls, camera motion and Foley events remain independently editable. Reuse cached selected sounds for the actual football contacts; add original nonverbal snore accents for the fictional cutaways. Preserve the previous native draft.

## What the concept board establishes

A generated style board explores color, field rendering, expressions, scale and camera language. It is a visual proposal, not an editable scene, a verified player model sheet, a tracking reconstruction or evidence of motion quality. Rebuild the chosen design as editable assets for film-v002; do not promise that a generated still is already an animation rig.
