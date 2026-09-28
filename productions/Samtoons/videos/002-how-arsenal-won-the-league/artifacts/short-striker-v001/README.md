# Arteta’s real striker — promotional Short

23 September 2026. **Complete edit for playback review; not published.**

[Play the Short](artetas-real-striker-1080x1920.mp4) · [Portrait thumbnail](thumbnail.png) · [Upload copy](upload-copy.md) · [Captions](captions.srt)

22.583 seconds, 1080×1920, 24 fps, 542 frames; H.264 video and stereo 48 kHz AAC. File size approximately 3.15 MB.

## Edit

Uses the five existing animated clips from `delivery-v027`: `TR02_flag`, `TR02_reaction`, `TR03_warning`, `TR03_kick`, and `TR03_praise`. Source interval is [1079,1621) frames, equivalent to 00:47.958–01:10.542 in branded delivery v029. Original performances, order, speed and sound are retained. No new Blender animation, frame interpolation, voice generation or music was added.

Portrait framing favors Arteta for the introduction, follows the existing flag reveal, cuts between speakers, briefly establishes the training geography, then follows the ball after defender contact. The first training view deliberately stays wide for 1.333 seconds. Speaker captions use the existing subtitle timings. The final shot carries the full-film invitation, with no added outro or extended runtime.

Audio is sample-trimmed from `delivery-v027/approved-soundtrack.m4a`: samples [2158000,3242000), with 20 ms entry and 80 ms exit fades. These fades fall outside the selected dialogue. No internal audio splice or time stretch.

## Checks and review limits

- Full decode, all 542 frame timestamps, dimensions, sample rate and channels passed. Video/audio duration difference is 0.000333 seconds.
- Encoded audio correlation with the selected source, excluding boundary fades: **0.999948**. This checks alignment, not listening quality.
- Inspected all encoded picture frames in eight sequential sheets, plus larger framing/contact/caption samples. Reviewed the complete kick and deflection sequence. The narrower initial action framing was revised before encoding to enlarge the players while retaining both contacts and the ball exit.
- Inspected the final portrait layout at reduced size and the generated cover against the selected film references. The cover is a promotional recomposition, not an inserted movie frame. Its original generated resolution is **941×1672**, without artificial 4K upscaling.
- Agent review did **not** include listening, real-time playback assessment or a test inside the actual YouTube mobile interface. User playback review remains pending. Existing acting limitations in the source film are not repaired by this derivative edit.

See [checks.json](checks.json), [source/edit mapping](edit.json), [final layout samples](inspection/final-layout-board.jpg), and [credits](CREDITS.md). A real frame fallback at 00:04.583 is provided as [cover-frame-004583.jpg](cover-frame-004583.jpg); no cover flash was inserted into the video.

## Reproduce

Run from the Pencil workspace with the existing Python/Pillow and FFmpeg installation:

```sh
/opt/anaconda3/bin/python productions/Samtoons/videos/002-how-arsenal-won-the-league/scripts/make_striker_short.py /absolute/path/to/new-output --check
/opt/anaconda3/bin/python productions/Samtoons/videos/002-how-arsenal-won-the-league/scripts/make_striker_short.py /absolute/path/to/new-output
```

The builder reuses Video 001’s streaming compositing pattern, records every crop and refuses to overwrite an existing movie. `--stills` creates framing previews only. The selected logo is pinned here; input hashes and thumbnail provenance are in [inputs.json](inputs.json). Preserve the source clips and approved soundtrack at the recorded paths. This is an editorial derivative; the original native Blender projects remain with Video 002.

Before publication, review the playable result and attach the full film as the Short’s related video. No account eligibility, upload URL or publication has been assumed.
