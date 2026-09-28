# Barcelona wasn't ready. Trent was.

Authorized production from the user's event/treatment brief, 11 September 2026. A 36-second vertical Short, 1080 × 1920, 24 fps. No narration or dialogue; concise English screen text, original reconstructed sound, editable native Blender artwork. Simple expressive bodies, Liverpool red and Barcelona blue/maroon stripes, identifiable Trent 66, Origi 27 and Shaqiri 23. No archival footage or audio in the delivery.

The question: **who is ready when a corner can already be taken?** Keep Trent, Origi, defenders and goal together in an oblique wide view. A freeze introduces the puzzle; Trent walks away as Shaqiri approaches, notices the unmarked receiver, turns and delivers. Origi finishes first time. A labelled slower replay directs attention to the defenders' delayed turn. Finish on the decisive aggregate result and the user's title.

## Verified event and treatment boundaries

- UEFA's [7 May 2019 match report](https://www.uefa.com/uefachampionsleague/news/0251-0e99aae66a0d-4ef82ebc84f0-1000/) verifies Liverpool's 4–0 second-leg win, overturning a 3–0 first-leg deficit, and Alexander-Arnold's quick corner for Origi's decisive finish.
- The [Premier League report](https://www.premierleague.com/en/news/1212312) places the unmarked Origi's winner in the 79th minute. The tie was 3–3 before it and finished 4–3 on aggregate.
- In [Liverpool's interview with Shaqiri](https://www.liverpoolfc.com/news/first-team/392432-xherdan-shaqiri-interview-world-champions-barcelona-ronaldo-idol), published 11 April 2020, he recalls thinking they were swapping takers, approaching while looking down, and being surprised by Trent's delivery.
- [Sky Sports' contemporary report](https://www.skysports.com/football/news/11833/11714405/luis-suarez-says-barcelona-looked-like-schoolboys-defending-liverpools-winning-goal) describes Barcelona organising, Trent walking away, and his quick return/cross.

All checked 11 September 2026. The sequence, identities of the two decisive players, score and outcome are factual. Pitch distances are compressed for phone readability. Supporting defenders represent the defensive group; individual poses, gaze marks, held time, exaggerated reactions, crowd texture and music are authored reconstruction. Do not imply a rehearsed fake, private thoughts, an exact tracking-data reconstruction, or an authentic broadcast recording. Not every player was literally looking away; show a group still organising and a receiver with space.

## Audiovisual script

| Beat / shot | Time | Audience understanding and visible action | Sound, focus and synchronization | Review question |
|---|---|---|---|---|
| B01 / setup | 0–2 s | Anfield, 79th minute. Ball settled at the corner. Players continue small setup motions. Score 3–0, aggregate 3–3. | Distant stereo stadium texture; dry short turf contacts. Freeze at frame 49. | Are the corner, receiver and goal visible immediately? |
| B02 / freeze | 2–7 s | Freeze the shared view. “WHO'S READY?” Identify Trent and Origi; keep defenders visible. | Crowd drops into a subdued filtered bed; a short graphic stop accent, no whistle. | Does the viewer know this is editorial stopped time? |
| B03 / swap | 7–10 s | Resume. Trent takes steps away from the ball; Shaqiri approaches. | Turf contacts follow planted steps; low tonal pulse supports anticipation. | Is it clear the corner has not yet been taken? |
| B04 / opening | 10–14 s | Hold the opportunity. Trent's gaze and a thin dashed lane connect the unmarked Origi; two defenders remain oriented toward other positions. | A small rising two-note observation motif; stadium remains low. Marks appear at named events. | Does the open receiver explain the opportunity without invented dialogue? |
| B05 / action | 14–18 s | Release time. Trent pivots back, strikes at 15 s. Ball travels continuously; Origi's first-time contact at 16 s, net at 16.5 s. Defenders turn after delivery. | Restore crowd; distinct lower corner thump and sharper finishing strike, then net flutter and swelling cheer. All contacts named in scene and plan. | Do both feet meet the ball and do reactions follow the delivery? |
| B06 / goal | 18–23 s | Origi opens his arms, Trent and Shaqiri celebrate. Score updates to 4–0, aggregate 4–3. | Broad original crowd cheer and resolving instrumental chord. Preserve kick/net tails. | Is the decisive outcome readable without narration? |
| B07 / replay | 23–29 s | Explicit “SLOW REPLAY”. Same shared geometry, from Trent noticing to goal. Caption asks viewer to watch when defenders turn. | Softer crowd and same cached kick/net takes at new named events (24.5, 26, 26.75 s). | Does the replay clarify the lag without suggesting another goal? |
| B08 / payoff | 29–36 s | Return to celebration. “BARCELONA WASN'T READY. TRENT WAS.” Then final result: Liverpool through 4–3 on aggregate. | Final chord resolves, cheer recedes; intentional 0.4 s tail at end. | Are title, result and final tail complete? |

## Sound and assets

Near-field boot/ball contacts against a distant, nonverbal stadium. Restrained graphic accents for editorial holds. Original instrumental tension/resolution only where it supports the change in attention. Quiet passages are intentional relative reductions, not missing ambience. Generate deterministic selected WAVs upstream with the existing Pencil filtered-noise/oscillator helpers; cache each selection. The shared `pipeline/audio.py` owns cue placement and stems. Final specification: stereo 48 kHz, −18 LUFS target (±1 LU), at or below −1 dBTP after AAC encoding, aiming at −2 dBTP before encoding.

Required assets: editable field/goal/net/flag, seven simple player puppets (Trent, Origi, Shaqiri, three representative defenders, ter Stegen), one continuous ball, screen text, observation marks, original selected Foley/ambience/music. Reuse existing endpoint mechanics after reading their dependencies. New versioned `artifacts/film-v001/` delivery. Human listening and audience comprehension remain unknown unless actually performed.
