# Samtoons animated identity — v002

Current reusable channel branding, selected by the user on 22 September 2026. It keeps the accepted 3-second mascot intro and 12-second end screen, replaces their earlier synthesized music with the selected Gemini phrases, and retains the approved impact, whistle and paper Foley.

## Ready-to-use files

- `samtoons-intro-1080p.mp4`: 3 seconds, 72 frames, 1920×1080, 24 fps, stereo 48 kHz.
- `samtoons-outro-1080p.mp4`: 12 seconds, 288 frames, 1920×1080, 24 fps, stereo 48 kHz.
- `audio/`: isolated selected music and complete mixes.
- `assemble.py`: adds both clips to a locked episode master and optionally shifts an external SRT.
- `checks.json`: hashes, media properties and source identity checks.

The editable vector picture source remains [animated-v001](../animated-v001/README.md). Music fitting and generated-source provenance remain in [music-v001](../music-v001/README.md). These final MP4 files are byte-identical copies of the review clips the user heard and approved.

Music provenance: user-generated Gemini/Lyria output, with its embedded SynthID retained. Google documents [downloading and sharing generated tracks](https://support.google.com/gemini/answer/16901237?hl=en-GH), and its current [general terms](https://policies.google.com/terms?hl=en-US#toc-content) say Google does not claim ownership over original content generated in supported services. Publication remains subject to the user's Google account terms, applicable platform rules and third-party rights; no exclusive copyright claim is recorded here.

## Default use for future Samtoons videos

Finish and approve the episode master first. Insert the intro after the cold-open hook at the film's authored `branding_intro` boundary; when a film has no cold open, use the beginning. Append the outro after the story's final frame. Keep the unbranded episode master unchanged and create a separate branded delivery.

```sh
python3 productions/Samtoons/branding/animated-v002/assemble.py \
  path/to/episode-master.mp4 path/to/episode-branded.mp4 \
  --intro-at 7.5 \
  --subtitles path/to/episode.srt \
  --output-subtitles path/to/episode-branded.srt
```

Omit `--intro-at` when the intro belongs at 00:00. The master must be 1920×1080, 24 fps, stereo 48 kHz. Place the intro between subtitle cues. Add actual clickable next-video and subscribe elements in YouTube Studio over the outro.

Run `python3 assemble.py --self-check` in this folder to verify the package.
