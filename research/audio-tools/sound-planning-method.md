# Planning picture and sound together

Proposed working method for Pencil · 11 September 2026

This is a planning proposal grounded in the existing films and the [sound-tool research](/Users/samikd/MyProjects/Pencil/research/audio-tools/sound-production-tool-landscape.md). It does not change completed films or implement an audio integration. Its recommendations apply to different animation lengths and subjects. Each film's current creative direction governs its sound style.

## What should change

Plan the audience's understanding, picture and sound in the same script. Choose and audition important sounds during the animatic, while changes to acting and editing are still inexpensive. Continue developing sound through animation and finishing.

Without narration, picture and sound share the explanation. Sound can establish attention, material, weight, location, urgency and emotional perspective. Facts, identities and causal relationships may still need a visible action, diagram or short caption. A dramatic score cannot reliably explain an unclear action. An animation designed to communicate a particular sound can legitimately depend on hearing it; muted review is a diagnostic, not a universal requirement that every film work identically without audio.

## What already exists

- The Heavy Box sound script reads the cue list in `experiments/001_heavy_box/finish-v001.json`. It already separates data from synthesis and places effects by frame. Reuse that working approach.
- The later Just Five Minutes script includes a picture/sound column, but `experiments/006_just_five_minutes/scripts/make_sound.py` separately hard-codes most cue times and writes `sound-design.json` afterward. Its exported cue list primarily describes Foley; the separately added music is not a complete editable plan there.
- Blender shot markers, frame-based animation, separate audio stems, FFmpeg finishing and the append-only production journal already exist. The previous research verified basic sample placement and block streaming, not a complete event-based retiming system.
- The Just Five Minutes production notes explicitly distinguish numerical audio checks from subjective listening, which had not been performed. Production readiness needs that listening evidence as well.

The useful next integration is a shared input cue plan, connected to named animation events, with resolved timing and actual asset selections recorded after the build. No new database or general workflow engine is necessary.

## 1. Add sound decisions to the creative brief

For each film, write a short sound direction alongside its visual direction:

- What should the audience understand or feel, and which sounds carry essential information?
- What is the physical world: materials, setting, scale and listener position?
- How stylized is the treatment: naturalistic Foley, exaggerated physical sounds, graphic accents, or a deliberate combination?
- Where should attention shift, where should the mix become quiet, and where is music useful?

Select a few representative sounds early if they determine the film's identity. These are specific audible examples, not only adjectives such as “cinematic.” A restrained documentary explanation and elastic physical comedy can use the same tools with very different choices. Do not prescribe a permanent whoosh, palette, number of layers or music pattern for every film.

## 2. Give important story beats a sound intention

Extend the existing script table with the following information. A significant reveal deserves a detailed row; an ordinary walking sequence can reference one reusable footstep family.

| Planning question | What to record |
|---|---|
| What must the audience notice? | The specific information or change: resistance, release, an approaching object, a mistaken expectation. |
| What will they see? | The action, staging, expression, graphic or text that establishes it. |
| What will they hear? | A concrete sound description, with material, movement and perspective where relevant. |
| What leads attention? | Foreground event, supporting texture, music, or intentional quiet. Identify competing sounds to reduce. |
| What does it synchronize with? | Named contact, movement interval, reveal, cut, or camera/perspective change; allow deliberate lead or tail. |
| How will we obtain it? | Existing asset family, recorded library candidate, procedural design, or bounded generation trial. |
| How will we judge it? | An observable listening or comprehension question. |

An asset request should be usable by either a library search or a generator: “One heavy wooden crate starts sliding on a rough indoor floor; short dry scrape with a clear onset, close perspective, isolated, no voices or music.” Its exact duration follows the action. Describing the intended sound before choosing the source keeps tool choice tied to the film.

## 3. Build an animatic with auditioned sound

Place selected candidates against rough poses and cuts. Include the essential contacts, a representative ambience and any music or transition that materially controls pacing. Mark placeholders explicitly so that an unlicensed or unsuitable temporary clip cannot silently become a delivery asset.

For a difficult beat, compare two meaningfully different treatments at comparable perceived loudness. Changing the mix should answer a question: does the object feel heavy, does the reveal arrive too soon, or does the transition suggest an unintended event? Keep the stronger treatment or revise the picture when neither works.

Picture and sound can lead each other. A contact needs alignment with the visible action; a sustained scrape needs the duration and movement to agree; a designed musical phrase might justify extending an anticipation. Audition the relationship before detailed animation, then revisit it after timing changes. This document predates the user's 12 September 2026 request for staged review. Follow the installed `produce-pencil-animation` skill for current checkpoints; provide actual playable sound direction and combined-animatic artifacts for review.

## 4. Connect both tracks to named events

In the next implementation, extend the current per-film JSON rather than generating a second independent timeline. A beat owns its visual intent; events such as `push_start`, `box_breaks_free` and `recovery_foot_contact` anchor the detailed cues.

The sound build should read the plan and animation's resolved event positions. Keep the requested cue distinct from the build record showing what was actually rendered. The latter must cover music, ambience and level changes as well as one-shot Foley.

| Keep with the cue | Purpose |
|---|---|
| Stable cue/beat/event identity | Preserve the relationship through revisions. |
| Shot-local position and explicit offset; start/end events for sustained sounds | Move events with a shot; change internal action timing deliberately. |
| Selected file, hash and audible-onset offset | Align the sound's attack, which may differ from file start. |
| In/out, gain, pan, fades, processing and mix role | Reproduce the treatment; retain tails across cuts where intended. |
| Selected variant and actual generation settings, if relevant | Avoid changing later sounds when an earlier cue is inserted. |
| Source, license, attribution and selection state | Know whether an asset can be used in the final production. |

Resolve timeline positions once, using exact frame-rate information. If a shot moves, reuse the chosen audio at its new position. If a movement becomes longer, review its sustained sound separately; moving a clip does not justify stretching every transient. Exact event export, cue resolution and Blender-strip synchronization require custom scripting; they are proposed work, not existing automatic features.

Keep the final mix authoritative in one place. For the initial integration, Python and FFmpeg produce it and Blender previews the resulting stems or mix. If a DAW later becomes the mix authority, record that decision and its rendered outputs rather than maintaining conflicting independent edits.

## 5. Treat transitions and quiet as authored cues

Choose a transition because it communicates a change:

- **Continuity:** carry room tone or an appropriate sound tail across a cut to maintain the same place.
- **Anticipation:** introduce an incoming sound before its image when it should direct attention forward.
- **Release or realization:** remove a previously established layer so the change becomes perceptible.
- **Perspective:** change distance, reverberation or filtering to move between external action and a character's subjective experience.
- **Graphic movement:** use a swish or accent when it helps the visible motion read.

These are options, not a checklist of sounds to add to each edit. Annotate intentional silence or reduced backgrounds so later automation does not mistake them for missing audio. Maintain a clear foreground; additional layers must earn their place in context. Musical rhythm and Foley rhythm can support each other without making every movement follow a beat.

For factual films, record when a sound is a reconstruction or subjective treatment. Do not imply that designed audio is an authentic recording of the source event. Verify permission for any archival audio actually used.

## A concrete example using Heavy Box

The table below proposes a fresh sound treatment of existing motion. It does not describe new work already performed or alter the approved delivery. Keep the illustrated box's material interpretation consistent with the picture; the material choices below are audition candidates.

| Beat | Audience takeaway | Proposed sound treatment | Listening question |
|---|---|---|---|
| Approach and plant | He commits his weight to the push. | Distinct, restrained floor contacts and a small handling sound. Quiet background. | Do the contacts feel planted rather than floating? |
| First push fails | Force builds, but the object resists. | Short body/cloth movement and compressed creak; save the sustained scrape for visible movement. | Can we distinguish resistance from actual sliding? |
| Stronger attempt | The effort increases. | Stronger pressure sound with controlled roughness; an optional stylized accent. Reduce competing detail. | Is greater effort audible without simply making everything louder? |
| Box breaks free | Resistance suddenly disappears. | End the strain at release, begin the scrape at visible displacement, then match its evolution to the slide. | Is the change from resistance to motion unmistakable? |
| Stumble and recovery | He loses balance and catches himself. | Uneven recovery contacts, a small secondary rattle, then a restrained tail or quiet hold. | Are the recovery contacts clear, and does the ending have room to land? |

This test can compare the preserved original mix with one alternate recorded/procedural treatment against identical picture. Music is optional; keep it out initially if it obscures what the Foley comparison is testing. The experiment isolates the value of sound selection before committing to another complete film.

## What earns production-ready status

Assess three things separately:

1. **Fitness in context:** the intended action is understandable, material and scale feel appropriate, important sounds remain audible, transitions make sense, repeated effects do not distract, and the emotional treatment fits the film. Judge against picture on headphones and ordinary speakers, including mono playback.
2. **Technical integrity:** synchronization, complete decoding, clean boundaries and tails, appropriate channel format, no unintended clipping or missing sounds, and final encoded loudness/true-peak checks against the project's chosen delivery specification. A numerical pass does not prove the first category.
3. **Reusability:** known rights, no delivery placeholders, preserved masters/selected variants, reproducible processing and an editable cue record. A successful rerender should not silently replace an accepted sound.

Use muted picture to locate visual ambiguity, isolated sound to inspect defects, and combined playback to judge the actual film. Where comprehension matters, show it to someone unfamiliar with the brief and ask what happened before explaining the intended answer. Record the observed result, not only the creator's expectation. Automated checks cannot certify emotional or educational clarity.

## Integration order

First, use the expanded script table and audition actual candidates in a rough animation. Reuse the Heavy Box JSON-input pattern for a small recorded-asset cue pass. Then connect selected cues to named action events and test a shot move plus an internal timing change. Preserve selected takes and verify contact timing and tails after both edits.

Use FFmpeg and the existing synthesis helpers for the first comparison. Introduce the processing tools or generative layer shortlisted in the research only when a specific sound brief exposes a gap. Keep source acquisition and generation outside the render loop, with approved audio cached as ordinary files.

Record the plan revision, chosen assets, listening comparisons, technical results and delivered stems with the existing journal helper. This document records exploration only; no sound candidates were acquired, auditioned or mixed in this step, and no runtime implementation has been changed.
