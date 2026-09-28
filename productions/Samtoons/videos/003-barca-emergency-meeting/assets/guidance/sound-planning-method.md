# Planning picture and sound together

Current production method. The [original research proposal](../research/audio-tools/sound-planning-method.md) remains historical evidence; this guide owns the adopted methodology. Follow [SKILL.md](SKILL.md) for the current creative checkpoints and [README.md](README.md) for the executable sound-plan contract.

Each video's brief governs its sound treatment, duration, subject and use of narration. Plan audience understanding, visible action and audible action in the same script. Sound can convey attention, material, weight, location, urgency and emotion; facts, identities and causal relationships may still need visible action, diagrams or concise text. Muted review diagnoses ambiguity; it does not require every film to work identically without sound.

## Establish sound direction with the brief

Decide which information or emotion sound must carry, the physical materials and listener perspective, the degree of exaggeration, where attention shifts, and where music or quiet serves the story. A documentary explanation and physical comedy can use the same tools with different choices. Do not impose a universal palette, music pattern or number of sound layers.

Select a few representative playable candidates when they determine the video's identity. Describe the intended source and action before selecting a tool or library; the required duration follows the animation.

## Direct the performance, not just the voice

For consequential dialogue, specify what the character is doing with the line (calling across a pitch, pleading, dismissing), emotional intensity, stressed words, breath/voice behavior and the turn in emotion. Accent and timbre identify a character; they do not supply acting. A shout needs projected delivery and vocal effort, a tearful apology needs audible distress, and a dry comeback needs deliberate emphasis and timing. Adapt these choices to each scene rather than making every character loud.

Choose a source capable of that delivery. Punctuation, voice selection, speed, gain, pitch shifting and compression alone do not reliably turn a neutral read into shouting or crying. If the source stays neutral, regenerate with a model that supports performance instructions or use an appropriately performed recording. Speech-to-speech conversion can preserve an acted source, but a neutral source is not an emotional performance. Verify the specific model's controls, license, runtime/storage needs and service availability before using it; open weights do not guarantee free hosted inference.

At the existing sound checkpoint, compare the revised line with the rejected take in isolation and in context at comparable listening levels. Listen for the intended action, effort, emphasis, intelligibility and continuity into laughs/sobs. Do not approve emotion from an instruction string, waveform or volume increase. Leave agent listening unknown when unavailable. Preserve useful pauses and tails; adjust picture/cue timing when necessary instead of squeezing acting into a neutral placeholder's slot. Cache accepted performances and use the same standard for later lines.

Evidence: the Samtoons character-voice v001 review was rejected on 2026-09-15 because Bruno said “Ref” conversationally and the other lines lacked the scene's energy. Cast B was preferred, but the performances were not approved. This rule addresses the selection failure; later engine trials still require listening review.

## Keep recurring speaker identity stable

Once a voice is selected, retain its exact voice ID or reference recording/transcript and hash. A character name, seed and similar prompt do not guarantee the same speaker. Separate identity from scene performance; changing pitch/register descriptors to obtain authority can accidentally recast the character. For locally designed Qwen voices, use the selected synthetic take with the compatible Base model's reference conditioning for subsequent text. `pipeline/qwen_voice.py --reference-wav … --reference-text …` supports this route. The Base route does not apply VoiceDesign acting instructions; assess the actual performance instead of claiming an ignored direction was applied. Compare new lines against the selected take at equal listening levels. Keep both required model weights; reclaim superseded production trials when authorized, not active models.

Samtoons video 002 v018 implements reference conditioning after the user identified v017's Arteta voice drift. The reference is the generated opening B02, not a real-person recording. This fixes the identity mechanism; perceptual continuity and emotion still require listening review.

## Give consequential beats an audible intention

| Planning question | Record with the audiovisual beat |
|---|---|
| What must the audience notice? | The information or change: resistance, release, an approaching object, a mistaken expectation. |
| What will they see and hear? | Concrete action, staging and expression alongside material, movement and sound perspective. |
| What leads attention? | Foreground event, supporting texture, music or intentional quiet; reduce competing detail. |
| What does it synchronize with? | Named contact, movement interval, reveal, cut or perspective change, including intentional leads or tails. |
| How will it be obtained and judged? | A suitable selected asset or bounded sourcing trial, plus a listening or comprehension question. |

Group ordinary repeated actions such as footsteps; give significant reveals their own beats. Record precise facts visually or in text when nonverbal sound cannot communicate them.

## Audition before carrying a sound through the video

Present sound candidates against rough poses and cuts at the sound-direction checkpoint. Compare meaningful alternatives at similar perceived loudness; isolate an uncertain background layer when needed. Select or revise the treatment before the complete combined animatic, following the skill's acceptance or scoped-delegation rules.

Review whether sound suggests the intended source, material, scale and emotion. A filename or noise generator does not establish perceptual fit. For recognizable real-world ambience, start with appropriate recorded or previously auditioned material. Check misleading rain/static/wind, unintended speech or music, distracting loops and cut tails. A deliberately sparse alternative is useful when no credible bed is available.

Keep placeholders marked until replaced or cleared for delivery. Preserve rejected selections and chosen file hashes; a later timing edit must not quietly reselect a rejected take. Selected sound may justify changing the picture's timing, and changed picture may require revisiting sound.

## Connect cues to authored events

The current shared audio command reads the video's `production.json`, resolves named shot events and renders stems and a premaster. Animation scripts export those event positions; the command does not infer contacts from pixels. Use the exact timing, segment, onset and provenance fields documented in [the sound-plan contract](README.md#executable-sound-plan).

Move a shot by changing its start, or an action by changing its event, then resolve again with the same selected files. A sustained scrape or ambience must still cover the intended interval; the tool does not silently stretch or loop it. Preserve contacts and tails, intentional overlaps and quiet passages. Explicitly select sound variations so inserting an earlier cue does not randomize later choices.

Source acquisition, synthesis, generation and processing happen before the audio build. Match the source to the need: recorded material detail, controllable synthesis, or generated audio where it earns the extra effort. Synthesis remains a candidate whose perceptual fit must be demonstrated. Cache selected outputs with source/license records and actual processing settings. Consult [sound-tool research](../research/audio-tools/sound-production-tool-landscape.md) only for the relevant need and reverify changing availability or licensing before acquisition or installation.

Keep one authoritative mix. The current approach uses the shared audio output and film-specific finishing, previewed by Blender. If a DAW becomes the mix authority, record its project and rendered outputs; avoid independently edited mixes that diverge.

## Author transitions and quiet

Choose transitions for their purpose: a sound tail can maintain continuity; a sound arriving before picture can lead attention; removing a layer can convey release; changing perspective can shift the listener's viewpoint. Graphic accents are optional and must help the visible movement read. Additional layers must earn their place in context.

Annotate intentional silence or reduced backgrounds so technical checking does not treat them as missing work. For factual films, distinguish reconstructed sound from authentic recordings of the source event.

## Review three kinds of evidence separately

1. **Fit in context:** comprehension, material and scale, foreground clarity, transitions, repetition and emotional effect. Use actual combined playback; record which headphones or speakers were used, and mono playback where relevant.
2. **Technical integrity:** synchronization, complete decoding, channel format, tails, clipping and encoded loudness/true peak against this video's chosen specification.
3. **Reusability:** known provenance, no uncleared delivery placeholders, preserved selections and masters, reproducible processing and an editable cue record.

Muted picture and isolated sound are diagnostics; combined playback is the actual work. If no listening occurred, leave that outcome unknown and provide an auditionable artifact. Measurements and sampled stills cannot certify listening quality, emotional effect or audience understanding.

Record actual selections, rejected candidates, listening comparisons, technical results and delivered stems in the video's journal. Promote lessons only to the scope supported by the evidence; one film's sparse mix does not make all later soundtracks sparse.
