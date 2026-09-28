# Samtoons 002 — branded 1080p delivery v029

The user accepted the combined v028 branding and full-film preview with “yes i accept”. This export preserves that timing and sound, renders only the new intro/outro at1920×1080, and inserts them into the existing v0271080 movie. No original film scene was Blender-rendered again.

- `samtoons-final-1080p.mp4`: complete branded movie, 6994frames,24fps,4:51.417,1920×1080, stereo48kHzAAC. Existing captions remain in picture.
- `samtoons-final.srt`: external captions with original wording and shifted timestamps.
- `intro-1080p.mp4` / `outro-1080p.mp4`: independent reusable channel segments.
- `samtoons-branding.blend`: two editable native vector scenes with packed fonts and approved sound mixes. Use the scene names to select intro/outro. Stored review render settings may be720p; `scripts/render_branding_v029.py` sets1920×1080 explicitly.
- `samtoons-branding-kit.zip`: the two1080 clips, native project, separate approved mixes, cue plans and this guide.
- `checks.json`: format, frame count, complete decode and original-film integrity checks. `final-checks.json` adds audio identity and frame-timestamp verification.

## Edit

00:00–00:07.500: original cold open.
00:07.500–00:10.500: approved3-second branding sting.
00:10.500–04:39.417: remaining original film, including the complete Ferguson ending.
04:39.417–04:51.417: approved12-second paper-gag outro/endcard.

Assembly decodes and encodes the existing picture once at CRF16; this is not bit-for-bit video stream copying. It preserves the source resolution/content/frame order. Audio is assembled from the same source and approved cached mixes as v028; no voice or music was regenerated. Source v027 remains untouched.

## YouTube end screen

Clickable elements must be added in YouTube Studio. Start after the paper gag settles, approximately04:41.5, and end with the movie. At1920×1080, the next-video rectangle is x1065–1785 / y350–755. The subscribe mark is centered near x1121/y888; adjust the actual YouTube element to its supported minimum size. Keep it below the thumbnail and clear of the mascot. Nothing has been uploaded or published.

## Editable original film and reproduction

The original scenes remain in `../delivery-v027/sources/` with their `edit.json` and complete prior delivery package. They have not been duplicated into this branding kit. The kit's native file edits only the new channel identity segments.

Film-local scripts: `render_branding_v029.py` checks the bound v028 approvals before rendering360 new frames; `assemble_branding_v029.py` inserts those clips into v027, shifts captions and validates the final movie. Earlier proof/build/sound scripts remain under the same film's `scripts/` directory.

The mascot/wordmark/signature/endcard are reusable channel assets. The flying paper is this episode's gag and can be replaced for another video. Preserve the accepted face, colors, timing and separate controls when adapting it.

## Provenance and review scope

Original mascot based on the supplied Samtoons S; native vector reconstruction with editable facial controls. Original three-note musical signature and sparse outro arrangement. Ball/whistle use video001's original production synthesis. Paper Foley: Ezcah, https://freesound.org/people/Ezcah/sounds/248178/, CC0, previously prepared excerpts.

Creative acceptance belongs to v028. The new1080 export receives technical and sampled visual checks, not a fabricated new user approval or agent listening claim.
