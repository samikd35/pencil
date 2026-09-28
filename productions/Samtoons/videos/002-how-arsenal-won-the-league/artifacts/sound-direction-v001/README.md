# Sound direction v001 — listening review

Two 35.875-second contextual sketches. [A: scored chase](audition-A.mp4) and [B: quieter chase](audition-B.mp4). Same performances, plot sounds, motif and hold tune; only chase underscore changes. Original held boards and existing chase footage provide context. No new character motion or lip-sync is represented. This is not the full-film animatic.

- 0:00–0:07: smug concealed narrator, unfinished two-note motif.
- 0:07–0:15: Arteta's panic contrasted with Pep's calm. A music exits before Pep answers; B keeps this passage sparse.
- 0:15–0:26: cheerful telephone service, banal original hold tune, ignored referee. This compact service audition groups the menu's two phrases; in the locked full-film script the second phrase follows the referee's interruption.
- 0:26–0:36: two-note return, lamp click and resolving note, recognition pause, performed meltdown, small paper finish.

[Full direction](../../sound-direction-v001.md) preserves the intent for every chapter, including unauditioned stadium, winner and wall effects. This sample does not validate all those future sounds. A thin hold tune is deliberate; an artificial stadium hiss would not be.

## Files / reproduction

`performance-directions.json` and each `*-raw.json` retain text, acting instructions, model identity, seed, timing and hashes. Generated source WAVs are cached. No real-person recording or cloning is used. VoiceDesign may change identity between calm and shouting takes; compare that continuity before full-film casting.

`plan-A.json` and `plan-B.json` feed the existing `pipeline/audio.py`. `mix-A/stems/` includes separated dialogue, music, score, plot effects and foley. [Dialogue alone](mix-A/stems/dialogue.wav) can diagnose performance independently. The live video `production.json` identifies A as the current sound review; `production-before.json` preserves the prior diagnostic state. Run film scripts under `.runtime/qwen-voice/.venv/bin/python`; the generator caches takes. Build/package scripts target this internal v001 directory: use a new revision before changing files after review. The shared mixer refuses existing output directories.

`comparison-check.json` confirms equal duration, finite peaks and sample-matched foreground outside the score interval. `encoding-checks.json` confirms 861 frames, 1280×720/24 fps, stereo AAC, complete decode, no clipping. Encoded measured loudness: A −22.49 LUFS, B −22.41 LUFS; both −7.14 dBTP. The report's `output_*` figures are loudnorm measurement-pass proposals, NOT processing applied to these files. The 0.08 LU difference provides a close comparison without different gains on the acting. Preserve performance dynamics; final mastering remains later.

Agent listening unavailable. Emotional delivery, voice continuity, accent, melody fit and joke timing remain unverified until actual listening. Starting a player is not a hearing assessment. Picture inspection confirmed the reveal frame and subtitle layout; held reference images cannot establish final contact sync.

## Credits / provenance

“Scheming Weasel (faster version)” by Kevin MacLeod (incompetech.com), [track](https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1100085), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Excerpted and faded. [Composer licensing page](https://incompetech.com/music/royalty-free/licenses/) rechecked 17 September 2026: free use requires credit. Retain this credit in publication copy, not picture. File is a video-local copy of the preserved episode 001 source; prior creative approval does not transfer.

Paper by Ezcah, [Freesound 248178](https://freesound.org/people/Ezcah/sounds/248178/), CC0. Processed short excerpt retained from episode 001's source record. Motif, resolution, hold melody, notification, switch and tiny tap: original production synthesis in the build script. Optional original boot asset is cached but deliberately unused: no guessed footsteps under held storyboard poses. Voice generation uses the existing pinned Qwen VoiceDesign Apache-2.0 model; runtime and model source copied into raw-take metadata.

## Review scope

Actual user preference and performance feedback pending. Selecting A/B only settles this treatment and heard takes; no approval of unheard cast lines, new action, full animation, or delivery. Chase-v002 remains below Bruno pose-action-v003 quality; Pep's walk and running require revision during the full-film work, as the user directed. No chase re-render performed here.
