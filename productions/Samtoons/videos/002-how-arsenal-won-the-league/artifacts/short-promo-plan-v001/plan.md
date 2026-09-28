# Arsenal promotional Short — selection, edit and thumbnail plan

22 September 2026 · Planning only. No Short or thumbnail has been generated, and nothing has been published.

Target: promote **Video 002, How Arsenal Won the League**, using the experience of Video 001's Manchester derby Short. This is a derivative of the existing fictional football parody, not a new factual season recap. Preserve the finished film and its selected performances.

## Recommendation

Make **one 22.583-second Short about Arteta choosing a corner flag over Gyökeres**. Use a continuous sequence from the finished animation: the unveiling, Gyökeres's objection, the instructions and their absurd application in training. It provides its own setup and payoff while leaving the title-winning goal and narrator reveal for the full film.

Recommended title: **Arteta’s REAL Striker Isn’t Gyökeres 😂**

Recommended thumbnail text: **OUR REAL STRIKER**. Adapt the previously selected corner-flag concept to portrait format, using the film's actual character designs and training-ground treatment.

Use existing rendered shots and audio. The proposed edit needs reframing, captions, packaging and an encode; it does not need new Blender animation renders. Keep source speed and joke timing for the first review. Tighten only if actual playback reveals a weak hold, without losing speech, the reveal or contact.

## 1. What we actually did for Video 001

The working example is [City’s best defender?](../../../001-manchester-derby-2026-09-13/artifacts/short-post-v001/README.md), built by [make_post_short.py](../../../001-manchester-derby-2026-09-13/scripts/make_post_short.py).

| Part | Actual construction | Lesson to carry forward |
|---|---|---|
| Selection | The user selected 00:32.750–00:53.000 from delivery v003: two post hits, the post's imitation, its contract demand and Bruno's complaint. | Select a complete comic situation rather than unrelated highlights. |
| Footage | 486 existing frames, 20.25 seconds at 24 fps, preserved in order and at original speed. No new character animation. | Preserve an accepted performance when an editorial derivative is sufficient. |
| Portrait framing | Ten source-shot ranges used different crops. The post close-up tracked the upright through the original camera movement; a second-chance setup retained full width. | Follow the subject and reveal; widen when the ball/contact or geography needs it. Do not use one fixed center crop. |
| Layout | 1080×1920 cream/ink/coral canvas, S mascot and headline above, approximately square picture area, large captions and a full-cartoon prompt below. | A designed portrait layout can preserve landscape action. Branding and captions must leave enough room for the animation. |
| Captions | Dialogue crops excluded the film's small captions; larger text was drawn separately. | Use clean shots when available instead of sacrificing feet or accepting fragments of old subtitles. |
| Audio | Delivery v003's selected mix, with 35 ms entry and 150 ms exit fades. Voices, effects and music were not regenerated. | Keep comic impacts and complete lines; audition the new boundaries rather than regenerating sound. |
| Cover | A separate, source-referenced generated portrait image: the goalpost demanding “PAY ME!” beside Bruno. It was promotional recomposition, not a movie frame. | Preserve source identity/style when recomposing a thumbnail; distinguish the cover from the edited film. |
| Checks | Source alignment, full decode, 486 frames and technical audio checks, plus sequential contact sheets and enlarged stills. The record explicitly disclaims agent listening and real-time motion assessment. | Retain technical checks, but do not mistake them for a playback review or evidence of promotional success. |

Video 001's original [selection study](../../../001-manchester-derby-2026-09-13/artifacts/portrait-selection-v001/selection.md) proposed three independent jokes; only the talking-post Short and its packaging are evidenced here. No channel analytics were inspected, so this is a demonstrated production method, not a proven conversion formula.

For Video 002, improve the adaptation by using clean native shot encodes, reducing unnecessary header/footer space, making the full-film invitation specific, and protecting the reveal during the portrait crop. Do not copy Video 001's goalpost color-tracking algorithm: these shots have different subjects and camera movement.

## 2. Exact recommended segments

The following source times refer to the **branded delivery v029**, which the user watches. Its inserted intro shifts these scenes three seconds later than the clean v027 edit. Millisecond displays are rounded; the frame ranges below are authoritative.

| Short timeline | Source v029 | Shot | Picture and sound to retain |
|---|---|---|---|
| 00:00–00:05.000 | 00:47.958–00:52.958 | `TR02_flag` | Arteta: “Meet our real striker.” Follow his pointing direction and the existing camera reveal to the corner flag in the number-nine shirt. Preserve applause and time to read the nine. |
| 00:05.000–00:11.000 | 00:52.958–00:58.958 | `TR02_reaction` | Gyökeres: “Then why am I here?” Arteta: “Win us corners. That’s where we score.” Keep the response and expression changes. |
| 00:11.000–00:15.750 | 00:58.958–01:03.708 | `TR03_warning` | Establish training. “Don’t shoot! Hit the defender. Off him, out for a corner!” Keep the goal/defender relationship intelligible. |
| 00:15.750–00:18.750 | 01:03.708–01:06.708 | `TR03_kick` | Preserve the wind-up, boot/ball contact, defender deflection and ball exit. Do not crop away the action that makes Arteta's instruction funny. |
| 00:18.750–00:22.583 | 01:06.708–01:10.542 | `TR03_praise` | “Perfect. A corner! Now we can actually score.” Let this complete the joke; add the full-film invitation without interrupting the line. |

Total: **542 frames at 24 fps**. The five shots are contiguous, so the first version needs no internal music or dialogue splice.

Zero-based, end-exclusive frame ranges:

| Shot | In Short | In unbranded v027 | In branded v029 |
|---|---|---|---|
| `TR02_flag` | [0, 120) | [1079, 1199) | [1151, 1271) |
| `TR02_reaction` | [120, 264) | [1199, 1343) | [1271, 1415) |
| `TR03_warning` | [264, 378) | [1343, 1457) | [1415, 1529) |
| `TR03_kick` | [378, 450) | [1457, 1529) | [1529, 1601) |
| `TR03_praise` | [450, 542) | [1529, 1621) | [1601, 1693) |

The recommended opening does not require the earlier transfer narration: Arteta's introduction and the headline supply the setup, then Gyökeres asks the audience's obvious question. The training example delivers a second payoff. If playback shows viewers need more setup, the existing arrival/transfer introduction at 00:39.958–00:47.958 is an available eight-second extension; it is not the default.

## 3. Portrait edit and sound direction

**Format:** 1080×1920, 24 fps, original proportions and speed. Use the S mascot, cream/coral/ink identity and actual footage. Proposed opening headline: **ARSENAL’S REAL STRIKER?** Start the dialogue immediately, with no separate logo intro. Omit the full film's three-second sting and twelve-second outro for this promotional derivative; keep brief branding in the layout instead.

Keep the picture dominant. Use shot-specific crops in a generous central picture area, with a wider inset when relationships cannot fit. Do not stretch the film to fill 9:16 or enlarge a crop until faces become soft.

- **Reveal:** begin with enough context to establish Arteta addressing Gyökeres. Follow the existing move toward the flag; keep the pointing direction and shirt connected. Do not crop so tightly that the flag appears unrelated or arrives after its reaction.
- **Objection/reply:** favor the speaking character where a two-shot becomes too small; retain the actual animated expression and complete relevant gesture. A crop change should support the exchange, not add constant artificial camera motion.
- **Training instruction:** retain a brief wide view that explains the available goal and the defender. The samples show that a narrow center crop would lose important geography.
- **Kick:** protect the ball and both contact participants throughout the movement. Follow the deflection only as needed. A wider frame is preferable to an unreadable close-up.
- **Payoff:** use Arteta's existing closer composition. Display **“Full Arsenal cartoon → linked video”** during the final beat in a separate readable area, not over his gesture or dialogue captions. No additional voice is needed.

Use large, speaker-labelled captions in meaningful phrases, normally no more than two lines. Obtain the wording/timing from the selected SRT, then map it to the Short. Keep hands, faces, ball, number nine, captions and invitation clear of actual Shorts interface overlays; verify on a phone-sized preview rather than claiming a universal pixel-safe zone.

Retain the existing voice identities, applause, kick/deflection effects, ambience and music. Use brief boundary fades only if needed to avoid a click or abrupt tail; do not fade into the first word or over the punchline. Check music/effect attribution against assets actually audible in this cut, not Video 001's unrelated credits.

The invitation links to the full film through YouTube's **Related Video** feature, which requires advanced-feature access and a public or unlisted target from the same channel. Verify availability and the exact full-film upload before publication; no upload URL is assumed here. [YouTube instructions](https://support.google.com/youtube/answer/14075157?hl=en).

## 4. Thumbnail and title plan

**Preferred concept: OUR REAL STRIKER.** This is a portrait adaptation of the user's selected full-film thumbnail direction, not a replacement for the full-film thumbnail.

- Make the flag's Arsenal number-nine shirt and Gyökeres's offended reaction the two largest elements.
- Include Arteta presenting the flag as a smaller supporting element if it remains readable at phone size. Preserve a plausible pointing hand.
- Use the film's recognizable faces, hair, kit, proportions and line/shading treatment. Use the training-ground green, red Arsenal barrier and pale sky/fence treatment as a simplified background.
- Keep **OUR REAL STRIKER** large and short. Small S mascot/wordmark; no extra headline, price tag, arrows, trophy or narrator reveal. The medal from the full-film concept is unnecessary for this earlier unveiling gag.
- If three subjects become crowded, reduce Arteta's prominence rather than shrinking the flag's nine or Gyökeres's face. Keep the main message centrally readable under different display crops.

Use source-frame references from the inspected unveiling and reaction for any image-generation/edit request. A recomposed cover may heighten the reaction, but must retain the film's character design; reject new faces, mismatched head/body rendering or unrelated stadium art. This task plans the image; it does not generate it.

Prepare a **9:16 portrait cover** and a frame-selection fallback from the actual Short. Current YouTube Help documents custom Shorts thumbnail uploads in desktop Studio for verified accounts and recommends portrait artwork; it currently recommends 2160×3840 for Shorts images. Use that target when genuine source/generation resolution permits; do not claim extra detail from upscaling. [Current thumbnail guidance](https://support.google.com/youtube/answer/72431?hl=en).

If custom upload is unavailable on the account, select an actual Short frame in the mobile app. No need to insert an unrelated cover flash at the beginning. [Frame-selection instructions](https://support.google.com/youtube/answer/10343433?co=GENIE.Platform%3DAndroid&hl=en).

Title options, in preference order:

1. **Arteta’s REAL Striker Isn’t Gyökeres 😂** — character conflict and curiosity; the cover supplies the absurd answer.
2. **Arsenal Signed Gyökeres… Then Picked a CORNER FLAG 😂** — immediately explicit, stronger spoiler of this joke.
3. **“Don’t Shoot!” — Arteta’s Plan for Gyökeres 😂** — emphasizes the training reversal.

Proposed description:

> Gyökeres came to score goals. Arteta had a different job in mind. 😂
>
> Watch “How Arsenal Won the League” through the related video for the full Samtoons cartoon.
>
> Fictional animated football parody.
> #Arsenal #FootballComedy #Samtoons

Add only the credits required by the selected audio. Final wording that mentions the related video assumes the link is actually attached.

## 5. Other useful segments — separate later Shorts

These are alternatives or follow-ups, not extra scenes to cram into the recommended edit.

| Priority | Source v029 | Length | Hook / payoff and limitation |
|---|---|---|---|
| 2 | 00:20.083–00:34.000 | 13.917 s | **“Bottle FC: auto-renewed.”** Bottle delivery → Arteta's subscription complaint → “Preferably before April.” Compact complete dialogue joke; truck label must remain readable. |
| 3 | 01:23.750–01:52.167 | 28.417 s | **“One-nil. That’s enough football.”** Retreat → keeper in front of nine defenders → admiring coaches → isolated Gyökeres told to win another corner. Strong visual escalation, but the wall and edge cameos need generous width. |
| 4 | 02:15.083–02:34.917 | 19.833 s | **“Arsenal run. Pep walks.”** Leading-the-league narration → walking reassurance → panic → Pep's “tired around this part” reply. More difficult to preserve the pursuit and podium in portrait. |

Reserve the VAR customer-service sequence for a separate edit if wanted: its full foul-to-decision chain runs approximately 02:46.208–03:32.167, nearly 46 seconds, and loses meaning if reduced to isolated telephone replies. Preserve the accidental winner and Ferguson reveal for the full movie in this first promotion.

## 6. Implementation and review after selection

1. **Use the selected sources.** Picture comes from the five clean v027 native clip files in `../delivery-v027/clips/`, not a re-render. Audio comes from `../delivery-v027/approved-soundtrack.m4a`, interval [1079/24, 1621/24) seconds. The v027 SRT uses the same unbranded clock. Use v029 only for the viewer-facing time references and comparison.
2. **Make a few actual framing samples, then the complete inexpensive edit.** Reuse the simple extraction/compositing approach of Video 001; adapt crops and captions to these shots. Exact crop paths must follow inspected motion, not guesses from the nine planning stills.
3. **Review the playable Short.** Check normal-speed timing and listen for complete speech, applause cuts, impacts and the final tail. Inspect successive frames around the reveal, kick, deflection and crop transitions, plus close views of the weakest details. Check that portrait editing introduces no new jitter or missing gestures.
4. **Prepare the cover and copy.** Compare the thumbnail with the actual movie at phone size. Confirm the account's supported thumbnail route and related-video target when uploading is separately requested.
5. **Export and verify.** New versioned H.264/AAC MP4, 1080×1920 at 24 fps, 542 frames for the proposed cut, stereo 48 kHz. Verify decode, range mapping, audio sync, captions and color/aspect preservation. Retain source mapping and honest review limits in the existing journal. Preserve both films and installed models.

The current film's acting remains the source performance: reframing and packaging cannot create missing animation. If a crop exposes a distracting defect, revise the crop or source selection first. A new animation repair would be additional scoped work, not an invisible consequence of making the Short.

## Evidence and current status

Inspected the Video 001 selection, builder, output guide, checks, journal and packaging notes; viewed its framing board and separate cover. For Video 002, read the delivered source map, performed script, subtitles and edit; verified the five clip files and contiguous frame ranges; checked source format metadata; inspected eighteen selected source frames in [the recommended sequence board](inspection/striker-selection.jpg) and [alternatives board](inspection/alternatives.jpg), plus an enlarged reaction frame and a clean native reaction-clip frame confirming captions are absent from that source.

The [sample record](inspection/samples.json) identifies extraction times. These are planning samples, not exhaustive motion or listening review. No new audience analytics, publishing status, account eligibility, full-speed playback or agent listening is claimed. Platform instructions were checked against official YouTube pages on 22 September 2026.

**Next concrete step:** select the recommended corner-flag Short, then create its portrait edit and source-matched cover for review. This document completes the requested planning work.
