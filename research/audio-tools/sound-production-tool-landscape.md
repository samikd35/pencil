# Sound production tools for an animation pipeline

**Technical assessment · 11 September 2026**

## 1. The strongest options

**Build the reusable capability around licensed recordings, repeatable processing and an editable cue timeline. Add generation for sounds that the collection cannot supply.** This gives precise control over contacts and variations while leaving room for unusual textures and video-conditioned experiments.

For an existing Blender, Python, NumPy and FFmpeg pipeline, the most useful shortlist is:

| Role | First choice | Why it belongs |
|---|---|---|
| Reusable Foley and effects | Selected Sonniss packs, Kenney audio and carefully chosen Freesound recordings | Downloadable assets can be auditioned, trimmed and reused at exact cue positions. Licenses differ by source and sound. |
| Environmental recordings | Free To Use Sounds; targeted commercial field-recording packs | Real locations and material detail are difficult to replace with elementary synthesis. |
| Local discovery | Soundly Free or Sound Particles Explorer | Auditioning and metadata search are already solved products. Keep portable files and provenance alongside them. |
| Automated finishing | Existing FFmpeg | The installed build already includes loudness measurement, convolution, crossfades, denoising and Rubber Band. |
| Additional Python DSP | Spotify Pedalboard | Built-in effects, VST3/Audio Unit hosting and streaming I/O, with Intel and Apple Silicon wheels. |
| Editable human mixing | REAPER | A capable local mix environment with officially documented scripting. |
| Local generative trial | Stable Audio 3 Small-SFX through its MLX runtime | A current dedicated SFX model with an official Apple Silicon route, duration controls and editing modes. |
| Hosted generative comparison | ElevenLabs Sound Effects; Stability Audio API | Accessible APIs without local model installation; different controls and billing terms. |

These are **workflow recommendations, not an audible-quality ranking**. No blind listening comparison or model inference was performed. Product claims about fidelity or speed are identified below rather than treated as independent results.[^1][^2][^3][^4][^5][^6][^7][^8][^9]

The smallest useful next step is a small, well-labeled set of real impacts, footsteps, cloth, object handling and ambience, inserted through the existing cue mechanism. There is no need to build a database, plugin host or generative service before testing that improvement.

<!-- page -->

## 2. Existing capability and verified local findings

The inspected pipeline already has seeded NumPy synthesis, event cues associated with animation frames, separate Foley/music/atmosphere stems, two-pass FFmpeg loudness normalization, encoded-file measurement and decode checks. These should remain the foundation.

The inspected machine is **Apple M4, arm64, 24 GiB unified memory**. The research runtime contains Python 3.12.14 and NumPy 2.3.5. Blender is 5.2.0 LTS and FFmpeg is 8.0.1. SciPy, SoundFile, Pedalboard, librosa, Python-SoXR, pyloudnorm and PyTorch were not installed in that Python environment. This does not establish whether another environment contains them.

**Checks actually run:**

| Check | Observed result | What it establishes |
|---|---|---|
| Frame 38, origin frame 1, 24 fps, 48 kHz | Impulse at sample 74,000 | FFmpeg sample-based delay matched the calculated cue exactly. |
| Same frame at 30,000/1,001 fps | Impulse at sample 59,259 | Fractional frame rates can be mapped without cumulative rounding drift. |
| Stream one minute in 8,192-frame blocks to FFmpeg | Passed; each stereo float32 audio block was 65,536 bytes | Existing tools can accept incremental audio. This was not a full mixer or process-memory benchmark. |
| Blender API introspection | `StripsTopLevel.new_sound(name, filepath, channel, frame_start, stream=0)` | The installed Blender exposes native sound-strip creation. |
| Installed FFmpeg filters | Required filters present, including `rubberband`, `afir`, `loudnorm` and `afftdn` | These capabilities do not require replacing FFmpeg. Presence is not a listening-quality test. |

The current full-timeline float64 allocation has a measurable scaling cost: **one hour of stereo at 48 kHz requires 2.7648 GB per array; three stems require 8.2944 GB before the mix, temporary arrays and other applications**. Float32 halves that, but streaming solves the duration-dependent allocation more effectively.

Only about **1.93 GB of free disk space** remained during inspection. Large library archives and model downloads were therefore not attempted. No paid service was called, no new audio package was installed, and no film assets were changed.

Reproducible evidence accompanies this report in `local_checks.py`, `local-checks.json` and `availability-snapshot.json`. Package availability and repository activity are snapshots, not guarantees of future support.

<!-- page -->

## 3. Recorded sounds: sources worth using

| Source | Coverage, discovery and delivery | Commercial use and attribution |
|---|---|---|
| **Freesound** | Wide community collection: Foley, objects, machinery, nature and unusual recordings. Text, tags, metadata filters, previews, packs and API access. Recording quality and metadata vary considerably. | Check **each sound**. CC0 needs no attribution; CC BY requires credit and license information; CC BY-NC is unsuitable for a default commercial collection. Older licenses also occur. API terms are separate.[^3][^10][^11] |
| **Sonniss GameAudioGDC bundles** | Downloadable compilations from professional libraries, useful for impacts, movement, machinery and environments. Large archives; browse pack lists and import selectively. They are samples of multiple catalogs, not uniform coverage of every action. | Bundle license permits commercial projects, modification and use without attribution. No standalone redistribution. Current terms prohibit AI training/development uses; do not treat the packs as an unrestricted model dataset.[^1][^12] |
| **Kenney audio packs** | Compact themed downloads, particularly useful for interface, digital and stylized effects. Clear pack pages. A convenient starting collection, with less breadth for detailed naturalistic Foley. | Asset pages and included license identify CC0; commercial use and no attribution requirement are explicitly documented.[^2][^13] |
| **Free To Use Sounds** | Field recordings from locations around the world: transportation, cities, nature, interiors and immersive environments. Site and store discovery; downloadable libraries. Check each pack's recording format and contents. | Paid libraries: lifetime commercial synchronization without attribution, within the standard license's organization-size limit. Free packs require a website-link credit. No redistribution of original recordings as standalone products. Larger organizations and certain developer/AI uses require different terms.[^4] |
| **BOOM Library** | Targeted premium libraries with metadata. Construction Kits provide ingredients and variations; Designed products provide assembled effects. Useful when a specific material or effect category repeatedly falls short. | Commercial finished productions permitted without source attribution; the product license governs distribution and seats. Pack prices vary. Buying a focused pack is preferable to acquiring a huge catalog without a demonstrated need.[^14][^15] |
| **ZapSplat** | Broad searchable effects catalog and packs. Basic access and premium options; WAV access and download conveniences differ by tier. | Standard-license Basic sounds require attribution; eligible Premium downloads retain attribution-free use. CC0 items have separate terms. Save the license and account entitlement at download time.[^16][^17] |
| **BBC Sound Effects** | Valuable searchable archival/environmental recordings and a preview mixer. Useful for research and reference. | Free access is for eligible non-commercial use with credit; commercial licensing is a separate route. An educational subject does not automatically make a commercial production non-commercial.[^18] |

**Recommended collection policy:** retain original files, license text or license URL, creator, asset identifier, acquisition date and attribution text. Create working derivatives separately. A sound marketplace's homepage is not evidence that every uploaded sound has the same rights.

No archive was downloaded or auditioned in this assessment. Coverage and download features above come from provider documentation; relative fit is an assessment of the pipeline's needs.

<!-- page -->

## 4. Discovery, local organization and provenance

| Tool | Useful capabilities | Fit and limitations |
|---|---|---|
| **Soundly** | Local/cloud search, waveform auditioning and drag-and-drop export. Free currently indexes 10,000 local files; Pro removes that limit and advertises a larger cloud collection. | macOS/Windows application, proprietary. Strong convenient browser. No general-purpose public headless search API was verified. Use exported files as the automation boundary. Exact paid checkout price was not reliably exposed in the retrieved page.[^5] |
| **Sound Particles Explorer** | Local metadata search, tags, ratings, playlists, notes, waveform preview and audio-property filters; stereo and immersive formats. | Free proprietary manager; macOS/Windows. A good candidate for an owned collection. Apple Silicon binary details and a public automation API were not established here; test the current installer before choosing it.[^19] |
| **SoundQ** | Local library databasing and access to purchased Pro Sound Effects collections. | The **SoundQ library subscription ended on 1 October 2024**. The software remains a free local manager. Old subscription comparisons are obsolete; the former-subscriber library entitlement is not an offer to new users.[^20] |
| **UCS** | A shared category vocabulary and filename convention for sound effects. | Public-domain initiative, not a sound library or search engine. Adopt useful categories gradually; do not rename every existing asset just to impose a taxonomy.[^21] |
| **BWF MetaEdit** | Embed, validate and export Broadcast WAV metadata; inspect file structure and audio-data checksums. | Free, MediaArea's code is public domain; macOS packages and command-line variants exist. Useful at interchange boundaries, not a waveform editor. Preserve masters before metadata rewrites.[^22] |
| **Existing files plus JSON** | Tags, paths, hashes, source links, license details and approved variants can live beside ordinary WAV/FLAC files. | Custom project metadata, using current practice. This remains the portable source of truth even if a browser app changes. No new SQL service is necessary. |

### Two licensing details change the architecture

**Freesound:** its official API exposes search, metadata, previews and downloads, with authentication requirements. Commercial API terms are negotiated with UPF. A commercially usable CC0 recording does not automatically grant unrestricted commercial API access. Start with normal downloads; add the API only under applicable access terms.[^10][^11]

**Soundly:** the November 2024 SFX license allows new productions during the subscription period and continued distribution of completed productions afterward. It explicitly restricts new productions using previously downloaded licensed sounds after expiry. It also prohibits uploading or using licensed catalog sounds in third-party AI tools. Therefore, do not treat a subscription cache as a perpetual owned library or as reference material for generative models. Local private sounds and third-party libraries retain their own applicable rights.[^23]

A practical per-asset record needs separate fields for **synchronization rights**, **attribution**, **new-project use after cancellation**, **redistribution**, and **AI-reference/training permission**. “Royalty free” cannot answer all five.

<!-- page -->

## 5. Procedural synthesis: the useful landscape

| Tool | What it adds | Automation, platform, license and effort |
|---|---|---|
| **NumPy + optional SciPy** | Envelopes, filtered noise, resonances, convolution, modulation and controllable transients. Suitable for stylized impacts, whooshes, electrical hum and basic weather textures. | Existing Python foundation; SciPy adds established DSP routines. Local CPU, Mac Intel/Apple Silicon. BSD-family licenses. Low effort. Material presets and event mappings are custom work, not built-in Foley intelligence.[^24] |
| **pyo** | A Python DSP graph with synthesis, sampling, filters, envelopes, granular processing and offline audio output. More comfortable than manually maintaining many oscillators and effect buffers. | Local C/Python engine, LGPL-3.0. Offline/manual server modes are documented. Medium setup effort: stable PyPI and documentation versions differ; see below.[^25][^26] |
| **SuperCollider** | Rich synthesis graphs, noise/resonator models, granular textures and timestamped scores. | GPLv3; native macOS universal build documented. `scsynth -N` renders an offline OSC score. Python can prepare files or invoke the CLI through **custom scripting**; it is not a native Blender connector. Medium/high learning effort.[^27][^28] |
| **Csound** | Mature synthesis, sampling and processing opcodes with offline rendering and a C host API. | LGPL-2.1-or-later, CLI and official Python bindings. Local CPU; macOS builds available. Csound 7 changes the API; 6.x is end-of-life. Pin engine and bindings together. Medium/high effort.[^29][^30] |
| **Sound Design Toolkit (SDT)** | Physically informed collisions, friction, rolling, scraping, water, wind, explosions and engines. The most directly relevant specialist toolkit for material-driven sound in this shortlist. | GPLv3 framework, C core, Max/Pure Data externals and Mac release assets. Python binding/contact integration requires custom work; ready Apple Silicon compatibility was not verified. High effort; repository activity is older than the other main candidates.[^31] |
| **jsfxr** | Compact, parameterized game-style effects such as jumps, hits, blips and lasers. | JavaScript/Node/browser library, Unlicense. Save the complete preset, not just a button choice. Low effort through Node invoked by Python. Deliberately synthetic character, limited realism.[^32] |
| **Faust** | Compile DSP descriptions into native code, standalone programs or plugins. Useful for a reusable custom synthesis instrument. | Local compiler and CLI toolchain; Mac support. The FAQ describes LGPL compiler licensing and separate library/architecture terms. Higher effort than NumPy or pyo; check licenses for the chosen export; no need to introduce it for ordinary asset placement.[^33] |

### What can sound convincing

**Assessment:** synthesis offers precise envelopes, pitch, resonance and intensity. It works well for stylization, continuous textures and controlled layers beneath recordings.

Recordings usually provide richer micro-detail for footsteps, cloth and breakage. Keep multiple takes and vary gain, pitch and filtering. Test SDT when **continuous** friction or material behavior justifies tuning physical parameters.

Material names need validated mappings to resonances, damping, excitation or recordings. These frameworks do not automatically turn Blender materials into convincing Foley.

<!-- page -->

## 6. Procedural tools: adoption details

### pyo: attractive Python interface, packaging needs attention

The documentation identifies version 1.0.6 and Python 3.9–3.13 support, but the normal PyPI JSON endpoint returned **1.0.5** as the current release during this inspection. Its listed Mac wheels cover Intel and ARM for selected Python versions, including 3.10 and 3.11; a Python 3.12 Mac wheel was not listed. The project's 1.0.6 testing announcement points to TestPyPI.[^26][^34]

This is a concrete reason not to promise that `pip install pyo` will work in the current Python 3.12 environment without building dependencies. An isolated compatible interpreter or a tested newer release is preferable to changing the production runtime. The documented offline server supports chosen sample rate/channel count and a global seed. No installation or sound generation was tested here.[^25]

### SuperCollider versus Csound

Choose **SuperCollider** if developing expressive synthesis graphs and offline scores is appealing. Its official universal Mac distribution is a stronger installation starting point than an unspecified cross-platform claim. Offline rendering consumes a prebuilt score; live OSC feedback is a different execution mode.[^27][^28]

Choose **Csound** if its opcode library or Python host API fits a particular sound instrument. The current development README identifies Csound 7 as beta and 6.x as end-of-life; the Python documentation explicitly describes breaking changes in version 7. This is a version-selection decision, not evidence that every existing Csound example still works unchanged.[^29][^30]

### SDT and commercial performance tools

SDT's physical models are compelling for parameter-driven Foley. However, its C/Max/Pd interfaces and older activity make it a specialist experiment, rather than the default pipeline dependency. A thin offline renderer would need to be written and validated against its release and architecture.[^31]

**Krotos Reformer Pro** is a commercial alternative for performing Foley from configured sound libraries, and **Krotos Studio** offers interactive sound-design workflows. These can be worthwhile for a human sound designer. Their performance/library systems should not be described as unrestricted open-source text-to-audio models. Synchronization use is documented; software, library and subscription terms remain product-specific. A dependable headless Python integration was not established here.[^35][^36]

**Decision:** retain NumPy; add SciPy only when a specific DSP operation needs it. Test one additional synthesis engine only after a recurrent sound category exposes a limitation. Installing pyo, SuperCollider, Csound, Faust and SDT together would add maintenance without establishing better sound.

<!-- page -->

## 7. Editing, processing and mixing tools

| Tool | Best use and strengths | Limits, cost and fit |
|---|---|---|
| **FFmpeg** | File conversion, cue assembly, fades, filters, convolution, dynamics, loudness analysis, final encoding and decode checks. | Already installed and scriptable. Keep it as the finishing/QA layer. Filtergraph construction and animation-event interpretation are custom scripting.[^7] |
| **Pedalboard** | Built-in compression, filtering, reverb, convolution, pitch effects; VST3 and macOS Audio Unit hosting; file/stream I/O. | GPLv3, free; Mac Intel/ARM wheels. Low/medium effort. Third-party plugins require their own compatible binary and license. It is not a full DAW timeline.[^6][^37] |
| **SoundFile / libsndfile** | NumPy-friendly WAV/FLAC reading, writing, seeking and block processing. | BSD-3-Clause wrapper, LGPL libsndfile; bundled Mac Intel/ARM wheels. Low effort. No mixing console or resampler. Add only if FFmpeg pipes or Pedalboard I/O become awkward.[^38] |
| **Python-SoXR** | High-quality streaming sample-rate conversion inside Python. | LGPL-2.1-or-later wrapper, following libsoxr’s license. Maintains state across chunks. Optional: the installed FFmpeg already has libsoxr support.[^39] |
| **librosa** | Onset/envelope/spectral analysis and reference analysis for evaluation. | Open-source Python library, ISC. Useful for offline analysis; no full mixer or plugin host. It offers streaming utilities, but many convenient transforms still load arrays. Do not introduce it just to trim WAV files.[^40] |
| **pyloudnorm** | Python implementation of BS.1770 loudness measurement and gain normalization. | MIT; useful inside numerical analysis. It does not replace true-peak limiting and final encoded-file verification. Existing FFmpeg measurement makes it optional.[^41] |
| **Rubber Band** | Pitch shifting and time stretching with independent control. | GPL-2.0-or-later, with commercial licensing available for proprietary integration. CLI/library. The installed FFmpeg already exposes it; a separate Python wrapper is unnecessary initially.[^42] |
| **REAPER** | Editable multitrack mixing, envelopes, routing, plugins, regions and stems. ReaScript can create and manipulate a session. | Proprietary; $60 discounted license if eligible, otherwise $225. Discount includes commercial users up to $20,000 annual gross revenue; 60-day full evaluation. Mac builds available. Medium effort.[^8][^43] |
| **Audacity** | Manual waveform/spectral inspection, cleanup and batch macros. | Free, GPLv2; Mac application. Python can send commands through optional `mod-script-pipe`. This is application automation, not a verified headless render service.[^44] |
| **IEM Plug-in Suite** | Ambisonic encoding/decoding, room reflections and spatial processing. | GPLv3, free; Mac builds. Optional advanced layer in a compatible host; verify architecture and channel-layout support. More complex than ordinary stereo positioning.[^45] |

**Setup priorities:** FFmpeg is already proven locally. Pedalboard has the clearest additional Python value. REAPER is the clearest improvement when manual listening, balancing and revision take more time than scripted assembly. SoundFile, SoXR and librosa solve specific needs; they are not mandatory companions to every installation.

<!-- page -->

## 8. What the existing stack covers—and where it needs care

### FFmpeg capability map

| Operation | Relevant existing filter/tool |
|---|---|
| Trim, rebase, place | `atrim`, `asetpts`, `adelay` with sample units |
| Layer and transition | `amix`, `afade`, `acrossfade` |
| Resample, stretch and pitch | `aresample`, `rubberband` |
| EQ and noise reduction | `equalizer`, `highpass`, `lowpass`, `afftdn` |
| Dynamics and ducking | `acompressor`, `sidechaincompress`, `alimiter` |
| Room response | `afir` with an appropriate impulse response |
| Loudness and diagnostics | `loudnorm`, `ebur128`, `astats`, `silencedetect`, `ffprobe` |

These are documented features; filter availability depends on the build. The main filters required for this pipeline were found locally.[^7]

### Processing decisions for reliable output

Keep source recordings at their original quality. Derive a consistent working sample rate—48 kHz fits the current pipeline—and resample once where practical. Use floating-point intermediates or suitable lossless files; avoid repeatedly encoding lossy files during revision.

**Pitch and timing are different decisions.** Moving a cue should not stretch its transient. For a longer movement, choose alternate recordings or loop a sustainable region before stretching an impact. Audition stretched sounds at the actual required ratio; no algorithm makes arbitrary stretching transparent.

A seamless ambience loop needs more than matching its first and last sample. Select a stable section, crossfade compatible material, listen across repeated boundaries, and avoid conspicuous repeated events. Stereo phase relationships matter; independently editing left and right can destabilize the image. This is a proposed editing procedure, not an automatic guarantee from a loop flag.

Pedalboard's documented parameter automation uses small processing chunks with parameter updates. Preserve effect state using `reset=False`, and explicitly render enough tail after the input ends. Its parameter API is real; automatic conversion of Blender motion curves into those updates would be custom code.[^37]

For perceived distance, combine source level, high-frequency attenuation, stereo placement and direct/reverberant balance. A simple pan slider alone does not reproduce distance or occlusion. More elaborate room/spatial modeling can use IEM, but a convincing stereo result often needs only a small, tuned processing chain.[^45]

The existing final loudness target is a project setting, not a universal target for all animation. Do not normalize every footstep to the same integrated loudness. Set balances first, measure the final mix, preserve intentional dynamics, and inspect the encoded delivery. Silence detectors should flag unexpected gaps within planned active regions; deliberate silence is not a failure.

<!-- page -->

## 9. Generative audio: candidates and adoption status

| Candidate | Available capability | Position in this pipeline |
|---|---|---|
| **Stable Audio 3 Small-SFX** | Public code and accessible, license-gated weights; text generation, audio editing and inpainting. Official MLX/portable CPU routes. | **First local AI trial.** Dedicated effects checkpoint and a credible Mac integration path. Commercial use is conditional, not unrestricted open source.[^9][^46][^47] |
| **Stable Audio 3 Medium / Large** | Medium weights and code; Large hosted API. Longer generation and editing. | Compare when Small-SFX fails an audible target. Standard Medium instructions require CUDA/Flash Attention, while the newer official MLX directory documents a Medium route: backend matters.[^9][^46] |
| **ElevenLabs Sound Effects v2** | Hosted text-to-effects API, duration and loop controls. | **First hosted comparison.** Low setup cost, but no public local model or documented seed control in the reviewed endpoint.[^48] |
| **MMAudio** | Public video/text-to-audio code and weights; CLI, seed and guidance controls. | Useful experimental video-conditioned candidate. Mac code path exists; official README only reports Ubuntu testing. Commercial suitability is expressly not guaranteed.[^49][^50] |
| **HunyuanVideo-Foley** | Public model and inference implementation; video plus text, batch generation, XL/XXL variants. | A remote Linux/CUDA experiment, not the default M4 installation. Custom community license and territory restrictions complicate adoption.[^51][^52] |
| **ControlFoley** | Public video/text/reference-audio conditioning and official ComfyUI workflows. | Particularly interesting controllability research, but **CC BY-NC 4.0 weights** rule it out as the default commercial production generator.[^53] |
| **TangoFlux, AudioLDM2, AudioGen, FoleyCrafter** | Accessible research implementations with useful generation approaches. | Relevant comparisons, but non-commercial terms or dependency restrictions prevent an uncomplicated commercial recommendation. Details follow.[^54][^55][^56][^57] |

**Estimated setup effort:** low for a hosted API, moderate for isolated Stable Audio 3 MLX, and high for video-Foley dependency/GPU environments. These are integration estimates, not installation results.

“Locally runnable” means an inference implementation and obtainable model components exist. It does not establish that installation succeeds on this Mac, that every operation works on Metal, or that outputs are fit to release.

No reviewed model provides a verified direct interface from Blender contact impulses or named animation events to an independently editable Foley stem for every object. Video synchronization, prompt following and access to seeds are useful controls; they are not a substitute for a cue timeline.

<!-- page -->

## 10. Stable Audio 3: the most promising local generative layer

**Best use:** unusual one-shots, designed textures, ambience candidates and variations that would otherwise require combining many recordings. It should generate assets for review; the mixer should not depend on live inference.

The main repository documents Small-SFX at up to **120 seconds**, stereo **44.1 kHz**, with CPU operation. Medium is listed at up to **380 seconds** and Large is API-only. The advertised parameter count is not a complete RAM or download estimate: encoders and decoders also matter.[^9]

The official **MLX implementation** supports Apple Silicon, Python/CLI invocation, seeds, negative prompts, guidance, audio-to-audio and region inpainting. It writes stereo 44.1 kHz PCM WAV. Intel Macs need a different runtime; the repository documents a TFLite CPU route for x86 and ARM. These are native project routes, not inferred support based merely on PyTorch having MPS.[^46]

**Performance evidence:** the MLX README reports roughly one second to generate a ten-second Small clip on an M1 with 8 GB, with about 1.6 GB peak RAM under its stated configuration. That is an **author-reported benchmark**, not a result on the inspected M4. It excludes an independently verified assessment of quality, installation and end-to-end production cost. The Small-SFX MLX components total roughly 1.8 GB before environment/cache overhead, based on the listed component sizes. Current free disk space is inadequate for a comfortable installation.[^46]

### Controls and limits

The inference documentation exposes duration, seed, inference settings, audio-to-audio strength and inpainting regions. Continuation extends an existing input within supported generation lengths. Inpainting windows control which region changes; they do not specify exact onset times for every event inside it. A request for several precisely spaced impacts still needs measurement and, usually, cue editing.[^58]

The Small model's documented 120-second operating range should remain the production assumption even though an optimized-runtime benchmark includes a longer input. A runtime accepting an argument is not evidence of equivalent quality beyond a checkpoint's documented range.

### Licensing and availability

Repository code is MIT. Weights use the **Stability AI Community License**, and the model card also names **Gemma terms** for the text encoder. The current license page explicitly includes Stable Audio 3. Commercial use under the community terms requires registration; the revenue threshold concerns total annual revenue including affiliates, rather than revenue generated by this tool alone. Larger commercial users need an enterprise agreement. The license distinguishes outputs from model derivatives.[^47][^59][^60]

The repository was not archived and had a September 2026 push in the availability snapshot. This supports active availability, not an SLA. Pin a release or commit and checkpoint revision before a trial. Save approved WAV files permanently rather than relying on seeds to recreate them after a runtime update.

<!-- page -->

## 11. Hosted sound generation

### ElevenLabs Sound Effects v2

The documented endpoint accepts text, duration, prompt influence, model ID and a loop flag. Official HTTP and Python integration are straightforward; a request can return audio that enters the ordinary asset-import path. No public code/weights for local inference were established. No seed or direct reference-audio/video input appears in the reviewed SFX endpoint.[^48]

**Documentation conflicts deserve explicit handling.** The API reference specifies **0.5–30 seconds**, while the overview says **0.1–30 seconds**. Use the endpoint's stricter lower bound until an authenticated test confirms otherwise. The overview describes 48 kHz WAV for non-looping effects; the endpoint also exposes output formats and tier-related restrictions. Stereo behavior and format entitlement should be checked on actual returned files, not assumed from a marketing example.[^48][^61]

The API pricing page advertises **$0.12 per generated minute**; the capability page separately describes **40 credits per second** for specified-duration requests. These are different billing presentations and should not be converted into each other without confirming the account's current plan. The advertised dollar rate implies $0.06 for 30 generated seconds before taxes, retries and any minimum/plan conditions; it is not a measured bill.[^62][^61]

Free use is restricted to non-commercial purposes; paid plans provide commercial rights subject to the applicable terms and exceptions. Upgrading does not retrospectively establish rights for a file generated under a free plan. Save the generation date and plan entitlement. Published latency evidence sufficient for an M4-to-service throughput estimate was not established.[^63][^64]

**Fit:** a low-friction way to audition difficult sound concepts and loopable beds. A loop request is useful, but still needs seam and unwanted-event review. Cache the chosen output because a future request may not reproduce it.

### Stability Audio API

The official platform lists **Stable Audio 3.0 at 26 credits per generation**, with one credit equal to **$0.01**: **$0.26 per generation** at the displayed rate. The platform also lists 25 initial free credits, which alone do not cover one 26-credit request.[^65]

The repository identifies Large as the API-only model. Official materials describe text generation, audio-to-audio, inpainting/continuation and output up to approximately six minutes; repository/API details give the longer family range as 380 seconds. Verify the exact endpoint parameters, limits and commercial service terms for the chosen request before integration. Self-hosted model licensing and paid API terms are separate.[^9][^66]

This is a useful comparison when longer coherent textures or reference editing matter. It is not a direct video-to-Foley endpoint. Cost comparisons should use **accepted assets**, including retries and editing time, rather than only generated seconds.

<!-- page -->

## 12. Video-conditioned Foley: promising, still a controlled experiment

### MMAudio

MMAudio combines visual/text conditioning with a synchronization model. Its default training/output duration is **8 seconds**; other durations are accepted, with quality cautions for large deviations. The recommended 44.1 kHz variant reportedly uses around **6 GB GPU memory** in the authors' 16-bit setup. This is not an Apple unified-memory measurement.[^49]

The current CLI selects CUDA, then MPS, then CPU, and exposes seed, duration, steps and guidance. That is verified source-level support for a Mac execution path, but the README says only Ubuntu was tested. Dependencies, MPS operation coverage, precision behavior and speed on this machine remain untested. Output channel guarantees were not clearly established from the reviewed model documentation; inspect generated files.[^50]

Code/model downloads are available. The repository's MIT license does not erase its explicit warning that pre-trained models are not guaranteed suitable for commercial use, given their training sources. Multiple encoders/VAE/vocoder components must also be tracked. Use as a research comparison until the relevant commercial-use questions are resolved.[^49][^67]

### HunyuanVideo-Foley

The implementation documents Linux/CUDA. XL requires **16 GB VRAM**, or **8 GB with offload**; XXL requires **20 GB**, or **12 GB with offload**. There is no verified native Apple Silicon route in the official instructions reviewed. Mac unified memory must not be treated as interchangeable with CUDA VRAM.[^51]

Source constants specify **48 kHz, two channels, 1–15-second video inputs**. Its CLI includes seed handling, guidance, inference steps and batch inputs. The authors publish comparative fidelity and synchronization results, but these are author evaluations, not a benchmark reproduced here. No dependable end-to-end throughput figure for this pipeline was established.[^68][^69]

The custom Tencent license excludes the EU, UK and South Korea from its defined territory. **Section 5(c) explicitly extends territorial restrictions to outputs**, not only model distribution. Other conditions include a separate license for organizations exceeding the stated 100-million-monthly-user threshold at release, restrictions on improving other AI models, and public AI-content identification in the acceptable-use policy. Although outputs are distinguished from model derivatives, they are not exempt from every use restriction. This is a poor default for globally distributed commercial animation without a separately suitable agreement.[^52]

### ControlFoley

A notable current alternative for reference-conditioned generation: video plus text, video plus reference audio, and conflicting audio/visual semantics are documented. Code is Apache-2.0; **weights are CC BY-NC 4.0**. Its CLI includes seeds and CPU/MPS/CUDA selection, but this does not establish successful Mac inference. Default duration is 8 seconds. An official ComfyUI integration is available; a portable C++ route is also linked by the project, without independently verified parity here.[^53][^70]

**Assessment:** sparse or stylized animation may provide weaker visual cues than the real/generated video examples used by these projects. Test against the actual animation style. Generated scene audio may contain unwanted music, speech-like sounds or a fused mix that is hard to separate. Exact contacts should remain replaceable with explicit cue assets.

<!-- page -->

## 13. Other models and capability boundaries

| Model/framework | Verified useful facts | Why it is not a default production choice |
|---|---|---|
| **TangoFlux** | Text-to-audio Python implementation, controllable duration, 44.1 kHz output and an author-reported 30-second generation in 3.7 seconds on A40. Code and checkpoints are available. | Model card explicitly restricts checkpoints to **non-commercial research**, with additional underlying terms. That supersedes any inference that a dependency's more permissive license permits commercial use. Mac performance and exact channel behavior were not established.[^54][^71] |
| **AudioLDM2** | Diffusers integration, downloadable checkpoints, seeds, variable duration; the general model example writes 16 kHz output. | Official weights are **CC BY-NC-SA 4.0**. Do not adopt a third-party wrapper's conflicting “commercial use OK” assertion. Generic platform snippets are not evidence that the audio pipeline runs correctly on MPS.[^55] |
| **AudioCraft / AudioGen** | AudioGen is a real released text-conditioned sound model within AudioCraft, with audio continuation support in the broader framework. | MIT code and **CC BY-NC 4.0 model weights** are distinct. GPU-oriented requirements and non-commercial weights make it a research comparator here, not a commercial default.[^56][^72] |
| **FoleyCrafter / Auffusion** | Video-conditioned inference, semantic/temporal controls and seeds; code and checkpoint downloads exist. | FoleyCrafter directs commercial users to Auffusion's license; Auffusion's license is **CC BY-NC-SA 4.0**. FoleyCrafter's own Apache-2.0 code does not remove that dependency restriction. Mac support was not validated.[^57][^73] |
| **Stable Audio Open / Open Small** | Older accessible text-to-audio models with a smaller deployment footprint in the Small variant. | Still relevant for existing integrations, but Stable Audio 3 provides a newer dedicated SFX route for a fresh Mac trial. Do not assume compatible checkpoints, controls or license files across versions.[^74] |

### Separate five different capabilities

**Text generation** describes the desired sound; **reference/audio-to-audio** uses an existing signal to influence a new one; **video conditioning** attempts to follow visible events; **inpainting** replaces a selected region; **continuation** extends an input. A repository implementing one does not automatically provide all five.

A motion-conditioned Foley system driven by numerical contact force, material and trajectory would provide a different kind of control from a video-conditioned neural model. SDT or a custom sample/synthesis mapping can accept such parameters through code; connecting Blender events to them remains integration work.

A generated “stem” requested in a prompt is not guaranteed isolated. Reject outputs with extra music, voices or events rather than building the pipeline around later separation. Music can be imported as its own licensed stem and mixed with the same tools; speech generation and cloning are outside this assessment.

<!-- page -->

## 14. Blender integration: native features and custom work

| Task | Existing/native capability | Required pipeline work |
|---|---|---|
| Place audio in Blender | Sound strips and `new_sound` through the Python API; confirmed in installed 5.2. | Read cue JSON and create/update the corresponding strips. |
| Preview level and placement | Keyframable volume and pan; waveform display; native sound retiming and pitch preservation. Pan applies to mono sources or an explicit mono mixdown. | Convert cue gains and spatial decisions into strip settings. Avoid inadvertently collapsing stereo ambience. |
| Subframe alignment | Sound-strip source offset is exposed in seconds. | Define offset semantics consistently and validate against the final rendered mix. |
| Trigger contact sounds | Animation data, evaluated transforms and scene markers are available to scripts. | Contact detection, material mapping, debounce and artistic selection are **custom**, not a built-in Foley generator. |
| Process via Pedalboard/FFmpeg | Their own Python/CLI APIs operate independently. | Export or reference assets, execute processors, then import approved results. No official direct Blender connector was verified. |
| Create a REAPER session | ReaScript provides track/item/envelope APIs. | A cue-import script is custom. Native scripting does not imply an existing Blender-to-REAPER bridge. |
| Generate neural Foley | Model APIs/CLIs accept their documented inputs. | Render a suitable preview, call the model, inspect output, trim/align and cache. Do not claim automatic semantic cue extraction. |

Blender documentation confirms sound-strip controls and its `aud` audio system. The installed 5.2 API uses `scene.sequence_editor.strips`; older examples using different collection names should not be copied blindly.[^75][^76][^77]

### Prefer event data to playback callbacks

For authored actions, record an event such as a foot planting, object impact or cloth movement in the animation's existing shot/cue data. For simulated motion, derive candidates from baked data, then reduce repeated contact samples to meaningful events. This is a proposed integration procedure.

Do not emit sounds directly from a live frame-change callback as the production record: scrubbing, repeat evaluation and rendering can visit frames more than once. Export a deterministic event list, inspect it, and render audio from that list.

Keep the audio package environment separate from Blender's bundled Python when dependencies become substantial. Calling an external Python process or CLI is a simple, explicit boundary; it avoids installing an entire neural stack inside Blender. Editable Blender strips can provide preview references, while FFmpeg or a DAW produces the final authoritative mix.

<!-- page -->

## 15. Reuse, retiming, caching and long timelines

### Extend the current cue records, not the infrastructure

| Information | Purpose |
|---|---|
| Stable cue ID, shot ID, event ID | Match a sound to an action through revisions. |
| Shot-relative frame/subframe and timeline origin | Retiming does not require manually rewriting every absolute timestamp. |
| Exact FPS numerator/denominator and sample rate | Compute placement without accumulating timing error. |
| Selected asset and its content hash | Reproduce the actual chosen take. |
| Source in/out, onset marker, tail length | Distinguish file start from audible contact; avoid cut-off reverb. |
| Gain, pan, processing parameters | Recreate the approved treatment. |
| Seed, generator version, checkpoint revision and prompt, when relevant | Trace generation; cached audio remains authoritative. |
| Source URL, creator, license, acquisition date and entitlement | Preserve provenance and attribution. |
| Output/stem hash and processing tool version | Make a finished render auditable. |

**Proposed timing rule:** with frame origin `f0`, sample rate `sr` and rational frame rate `fps`, place the cue at `round((frame - f0) × sr / fps)`. Calculate each position from its absolute rational time, rather than adding rounded samples-per-frame repeatedly. An asset's annotated attack may occur after its file start; subtract that onset offset when aligning a contact.

When an animation edit moves a shot, resolve its local events at the new shot start. When it changes the action internally, update the event itself. Moving an event and stretching its source sound must be separate operations. Rebuild affected stems while retaining selected takes unless the action materially changes.

**Variation:** use stable cue IDs and explicit seeds to select from a small approved family of recordings or presets. Record the selected file and actual parameters. A single global random sequence is fragile: adding an earlier cue can change every later selection.

**Caching:** hash source content, processing parameters, tool/model revision and relevant conditioning inputs. Store outputs as files and index them in existing JSON. Cache per generated/processed asset, then place that asset on the timeline. Do not generate again just because the edit moved it.

**Long timelines:** mix only the events overlapping the current block or scene. Maintain filter state between adjacent blocks and carry reverb tails across boundaries. Rendering scenes independently without preserving tails can create discontinuities. Limit concurrently open sources and generative jobs; one FFmpeg input for every footstep can become an operating-system/file-descriptor problem even without large NumPy arrays.

Keep lossless masters and export separate action, Foley, ambience and music stems as appropriate. A processed master will not necessarily equal the sum of independently normalized stems: save a pre-master bus or document shared bus/master processing. For files approaching container size limits, use a suitable large-file format such as RF64 or split stems deliberately.

Append acquisition, generation, selection, processing, QA and delivery outcomes to the existing production journal. No new database or generalized workflow framework is required.

<!-- page -->

## 16. Three recommended configurations

### A. Minimal dependable improvement

**Existing NumPy + FFmpeg + cue JSON/journal + a small licensed recorded collection.** Use ordinary files for delivery and a free browser only if auditioning through Finder becomes inconvenient. Start with selected CC0 recordings/Kenney and Sonniss sounds under their applicable terms.

**Benefits:** no required new processing dependency; precise placement; repeatable approved assets; inexpensive; works offline after acquisition. The installed FFmpeg can already handle essential processing and Rubber Band.

**Tradeoff:** manual asset selection and limited editing ergonomics. Bespoke sounds still require synthesis, recording or searching. This is the recommended immediate adoption step, not an inferior temporary architecture.

### B. Stronger production stack

**Configuration A + Pedalboard + one local sound browser + REAPER when mix revision demands it.** Add focused owned Foley/environment libraries; use Soundly's cloud library only with an ongoing subscription plan consistent with future reuse. Add SoundFile only if its seeking/block API materially simplifies the mixer; Pedalboard also has streaming I/O.

**Benefits:** richer processing in Python, plugin access, fast auditioning and an editable mix session. Separates dependable automation from the listening decisions that benefit from a DAW.

**Tradeoff:** plugins and DAW projects add version/state management. REAPER costs $60 if eligible or $225 otherwise; optional libraries/browser subscriptions vary. No blanket claim that every plugin works in Pedalboard on ARM should be made.[^8]

### C. Production stack with optional generation

**Configuration A or B + isolated Stable Audio 3 Small-SFX MLX environment + one hosted comparison when useful.** Generated assets must pass the same checks and listening review as recordings. Retain ordinary asset fallback for critical contacts.

**Benefits:** local invention of unusual textures, privacy for eligible local reference material, controllable duration and region editing, and API alternatives for difficult requests.

**Tradeoff:** model licensing, disk space, prompt iteration and uncertain per-category quality. GPU/backend seeds do not guarantee identical future output. Video-conditioned Foley remains a separate experiment, rather than a prerequisite for this stack.

**Choice:** adopt A, evaluate the incremental value of Pedalboard and REAPER for B, then compare C on sound categories where A/B are weak. Do not choose a generative model solely because it is newest or its demo sounds impressive.

<!-- page -->

## 17. Practical integration order

1. **Preserve the current reference mix.** Keep the existing scripts, stems and final delivery unchanged. Choose a repeatable group of animation events for audio comparison.

2. **Build a compact approved asset set.** Select dry impacts, several footsteps, cloth/handling, one mechanical family and two contrasting environments. Save source/license records before modifying files. Use manageable downloads; resolve local storage pressure before model installation or multi-gigabyte bundles.

3. **Add recorded-asset cues.** Reuse the current cue placement and stem logic. Annotate audible onset and tail where necessary. Compare replacing only the relevant procedural sounds before changing the entire mix.

4. **Make timing and variants explicit.** Retain exact FPS, stable event IDs and selected file/parameter values. Test an edit that moves a shot and a separate edit that changes action timing. The selected sound should remain stable unless deliberately replaced.

5. **Remove duration-wide allocations where they become limiting.** Use FFmpeg pipelines or block I/O with one selected library. Verify overlapping sounds, cross-boundary tails and the final partial block. The accompanying block-stream check is an initial feasibility test, not this completed refactor.

6. **Evaluate Pedalboard with a small processing task.** Compare its reverb/filter/compressor or one plugin with the existing FFmpeg result. Adopt it only if audible control or implementation clarity improves. Pin a tested version and compatible plugin binaries.

7. **Use a DAW when listening revisions justify it.** Trial REAPER with exported stems or a small cue importer. Preserve edits in its native project and render stems plus a master. Avoid implementing a custom GUI mixing console.

8. **Trial generation in an isolated environment.** First test Stable Audio 3 Small-SFX after adequate storage and license registration. Compare a hosted service using the same briefs. Record failures, iterations and editing time, including silent or unwanted outputs.

9. **Add video-conditioned Foley only for a demonstrated need.** Test whether it saves work on the actual animation style. Evaluate onsets, event count and unwanted audio rather than accepting a plausible overall atmosphere.

10. **Keep the winning capability.** Save approved presets/assets, evaluation results and tool versions in the existing JSON/journal. Expand only when repeated production work exposes a gap.

These steps are an integration recommendation. Apart from the explicitly reported local checks, implementation has not been performed as part of the research.

<!-- page -->

## 18. A fair evaluation method

Use identical briefs and the same silent animation/contact markers across candidates. Evaluate recordings, procedural designs and AI outputs on the **same required result**, while allowing each approach its natural workflow. A prebuilt library clip and a model generation have different acquisition costs; include search and preparation time.

| Category | Representative task | What it reveals |
|---|---|---|
| Dry impacts | Light/heavy wood, metal and soft-material contacts | Attack precision, resonance, weight and material identity. |
| Footsteps | Slow/fast walking, start-stop, two surfaces | Timing, variation and repetitive artifacts. |
| Handling | Cloth, paper, a drawer and a small loose object | Micro-detail and unwanted noise. |
| Continuous contact | Rolling, scraping and sliding with changing speed | Parameter continuity and synchronization. |
| Mechanical/electrical | Motor startup, steady operation, stop; switch and hum | Stable timbre, controllable transitions and tails. |
| Air and water | Wind gusts, rain, stream and isolated drops | Natural variation, stereo coherence and loopability. |
| Stylized effects | Whoosh, elastic impact, transition and rising/falling gesture | Expressiveness and precise duration. |
| Spatial scene | Same source near/far and moving across the listener | Distance cues, movement and mono compatibility. |
| Composite event | Contact followed by rattle and a room tail | Event ordering and editability. |
| Endurance case | Repeated blocks and scene changes over a long timeline | Memory, drift, cache behavior and boundary artifacts. |

### Automated technical checks

Inspect format, sample rate, channel layout, duration and complete decodability. Check finite samples, unexpected silence, flat-topped/clipped samples, DC offset and large boundary discontinuities. Measure sample and true peak, integrated/short-term loudness where meaningful, and channel correlation. Evaluate timing against labeled contact onsets; waveform peaks alone are not always perceptual onsets.

Track exact onset error in milliseconds and frames, event count, export start offset and final duration. Test both integer and fractional FPS. Check again after final encoding. A silence-only output or missing tail is a technical failure, even if the tool reported success. Maintain expected-silence windows to avoid rejecting intentional silence.

Measure cold-start and warm generation separately; record machine/backend, model revision, duration, settings, wall time, peak memory if instrumented, download footprint and failures. Report local GPU memory and Mac unified memory separately. Repeat requests with fixed seeds and hash outputs, without assuming a hash mismatch necessarily sounds different.

### Subjective listening

Randomize labels and loudness-match comparisons sensibly; a louder candidate should not win by default. Listen to isolated effects and then against picture on headphones, speakers and in mono. Score material identity, weight, cleanliness, natural variation, timing, spatial credibility, unwanted events and ease of revision. For ambience, listen across several loop repetitions.

Use several examples per category and multiple generated candidates with a fixed retry budget. Report both first-pass success and best accepted result. This prevents unlimited prompt retries from looking equivalent to a reliable one-shot process.

**Primary decision measures:** accepted assets per hour of work; total acquisition/generation/editing cost per accepted asset; proportion requiring manual timing repair; and ease of reproducing an approved mix. CLAP similarity or distributional research metrics may supplement these, but do not measure an individual sound's production fitness by themselves.

<!-- page -->

## 19. Limitations, maintenance and unresolved questions

### Availability snapshot

The inspected GitHub repositories were not archived. Repository `pushed_at` is only an activity signal: it can reflect documentation or branch updates, not necessarily a new release or repaired inference.

| Project | Last repository push returned on 11 September 2026 | Adoption implication |
|---|---|---|
| Stable Audio 3 | 5 September 2026 | Active current candidate; pin a revision. |
| Pedalboard | 9 September 2026 | Active package; use a tested release rather than moving main. |
| ControlFoley | 28 August 2026 | Active research; non-commercial weights remain decisive. |
| pyo | 20 July 2026 | Activity does not resolve the PyPI/documentation mismatch. |
| FoleyCrafter | 15 June 2026 | Available implementation; dependency license still matters. |
| MMAudio | 23 February 2026 | Available; Mac runtime and commercial suitability remain unproven here. |
| TangoFlux | 28 January 2026 | Available research checkpoint, not an unrestricted production license. |
| HunyuanVideo-Foley | 28 September 2025 | Accessible release; CUDA requirements and license conditions are material. |
| SDT | 27 March 2024 | Useful specialist code, with greater maintenance/integration uncertainty. |

The Csound metadata request hit a GitHub API rate limit; its official documentation and repository README were used instead. Exact results are retained in `availability-snapshot.json`.

### Questions that require a trial or clarification from a provider

**Audible quality:** no shortlisted model, commercial library or new DSP package was installed and auditioned. Provider demonstrations and author benchmarks cannot establish performance on these particular animated scenes.

**Generative runtimes:** Stable Audio 3's Mac route is documented, but installation, account-gated download behavior, memory and latency on this M4 remain untested. MMAudio and ControlFoley contain MPS paths; that is weaker evidence than a successful supported Mac deployment. Exact stereo guarantees for some models/services remain unclear.

**Hosted details:** ElevenLabs' duration, output-format and billing documentation is not fully consistent. Verify entitlement and the actual request bill before depending on a particular rate or format. Soundly's paid checkout price and Explorer's current binary architecture were not established in the retrieved sources.

**Licensing:** synchronization rights do not imply AI-input rights or sample redistribution rights. Code, weights, encoders, recordings and hosted-service terms can all differ. GPL software use does not automatically impose GPL on ordinary rendered sound, but distributing a combined software product introduces separate license obligations. No report can establish that an arbitrary third-party upload contains no unauthorized material.

**What was not independently demonstrated:** no third-party comparative listening results sufficient to rank all candidates fairly were established. This report therefore recommends an evaluation order, not a claim that one model produces the best sound in every category.

<!-- page -->

## Sources

Primary sources accessed **11 September 2026** unless otherwise stated. “n.d.” means a publication date was not clearly identified. Versioned pages and repository files can change; record revisions at adoption. Numbered references distinguish provider documentation from the local checks described in section 2.

[^1]: Sonniss. [GameAudioGDC bundle license](https://sonniss.com/gdc-bundle-license/). Current terms, n.d.
[^2]: Kenney. [Support: asset licensing and commercial use](https://kenney.nl/support). n.d.
[^3]: Freesound / Universitat Pompeu Fabra. [Frequently asked questions](https://freesound.org/help/faq/). n.d.
[^4]: Free To Use Sounds. [License agreement](https://www.freetousesounds.com/license-agreement). Includes dated revisions and separate paid/free provisions.
[^5]: Soundly. [Product, features and plans](https://getsoundly.com/). n.d.; current plan page.
[^6]: Spotify. [Pedalboard documentation](https://spotify.github.io/pedalboard/). v0.9.25 documentation.
[^7]: FFmpeg. [Audio filter documentation](https://ffmpeg.org/ffmpeg-filters.html). Current online manual.
[^8]: Cockos. [REAPER purchase and eligibility](https://www.reaper.fm/purchase.php). Current license prices.
[^9]: Stability AI. [Stable Audio 3 repository](https://github.com/Stability-AI/stable-audio-3). 2026; current README and code.
[^10]: Freesound / UPF. [API v2 resources](https://freesound.org/docs/api/resources_apiv2.html). Current API documentation.
[^11]: Freesound / UPF. [API terms of service](https://freesound.org/help/tos_api/). Current terms, n.d.
[^12]: Sonniss. [GameAudioGDC archive](https://sonniss.com/gameaudiogdc). Download archive, n.d.
[^13]: Kenney. [Digital Audio asset pack](https://www.kenney.nl/assets/digital-audio). Pack contents and CC0 designation.
[^14]: BOOM Library. [Permitted uses of sounds](https://www.boomlibrary.com/support/faq/what-am-i-allowed-to-do-with-your-sounds/). n.d.
[^15]: BOOM Library. [Designed versus Construction Kit](https://www.boomlibrary.com/support/faq/what-is-the-difference-between-designed-and-construction-kit/). n.d.
[^16]: ZapSplat. [Standard license](https://www.zapsplat.com/license-type/standard-license/). Current license page.
[^17]: ZapSplat. [FAQ](https://www.zapsplat.com/faq/). Tier/download features and CC0 exceptions.
[^18]: BBC. [BBC Sound Effects FAQ](https://sound-effects.bbcrewind.co.uk/faqs). n.d.
[^19]: Sound Particles. [Explorer features](https://lp.soundparticles.com/explorer). n.d.; product and search features.
[^20]: Pro Sound Effects. [SoundQ subscription notice](https://hello.prosoundeffects.com/help-center/soundq-subscription-notice). Changes effective 1 October 2024.
[^21]: Universal Category System. [UCS project and resources](https://universalcategorysystem.com/). Includes 8.2.1 update, January 2024.
[^22]: MediaArea. [BWF MetaEdit](https://mediaarea.net/BWFMetaEdit) and [Mac GUI/CLI downloads](https://mediaarea.net/BWFMetaEdit/Download/Mac_OS). Version 26.08.1 page; features and license.
[^23]: Soundly. [SFX subscription license](https://getsoundly.com/assets/Soundly-EULA.pdf). Last update stated in document: 11 November 2024, especially pp. 1–4.
[^24]: SciPy. [Signal processing reference](https://docs.scipy.org/doc/scipy/reference/signal.html). Current API manual.
[^25]: Olivier Bélanger / pyo. [Audio Server API](https://belangeo.github.io/pyo/api/classes/server.html). v1.0.6 documentation.
[^26]: Olivier Bélanger / pyo. [Installation documentation](https://belangeo.github.io/pyo/download.html). v1.0.6 documentation.
[^27]: SuperCollider. [Official downloads](https://supercollider.github.io/downloads). Universal macOS distribution.
[^28]: SuperCollider. [Non-realtime synthesis](https://docs.supercollider.online/Guides/Non-Realtime-Synthesis.html). v3.14.1 documentation.
[^29]: Csound. [Development README and license](https://github.com/csound/csound/blob/develop/README.md). Version 7 beta and 6.x EOL notice.
[^30]: Csound. [Python bindings and API migration](https://csound.com/csound-python.html). Csound 6/7 distinction.
[^31]: SkAT-VG. [Sound Design Toolkit repository](https://github.com/SkAT-VG/SDT). API, models, licensing and release instructions.
[^32]: Chris McCormick and contributors. [jsfxr](https://github.com/chr15m/jsfxr). Node/browser usage and Unlicense.
[^33]: GRAME. [Faust programming language](https://faust.grame.fr/) and [license FAQ](https://faustdoc.grame.fr/manual/faq/). Current project, toolchain and licensing overview.
[^34]: PyPI / pyo. [Release metadata](https://pypi.org/pypi/pyo/json) and project maintainer's [1.0.6 testing announcement](https://github.com/belangeo/pyo/discussions/293). Metadata retrieved directly; selected values saved locally.
[^35]: Krotos. [Synchronization permissions](https://www.krotosaudio.com/support/faq/i-allowed-use-krotos-presets-libraries-synchronisation/). n.d.
[^36]: Krotos. [Product and library terms](https://www.krotosaudio.com/terms-conditions/). Current product-specific terms.
[^37]: Spotify. [Pedalboard parameter automation FAQ](https://spotify.github.io/pedalboard/faq.html). State-preserving block-processing example.
[^38]: SoundFile contributors. [SoundFile documentation](https://python-soundfile.readthedocs.io/en/0.13.1/). Version 0.13.1; block I/O, wheels and licenses.
[^39]: Python-SoXR contributors. [Streaming resampling documentation](https://python-soxr.readthedocs.io/en/latest/) and [repository/license](https://github.com/dofuuz/python-soxr). Current documentation.
[^40]: librosa contributors. [librosa documentation](https://librosa.org/doc/latest/index.html). Current manual.
[^41]: Christian Steinmetz and contributors. [pyloudnorm](https://github.com/csteinmetz1/pyloudnorm). Implementation, examples and license.
[^42]: Breakfast Quay. [Rubber Band Library](https://breakfastquay.com/rubberband/). Library, CLI and licensing options.
[^43]: Cockos. [ReaScript documentation](https://www.reaper.fm/sdk/reascript/reascript.php) and [Mac downloads](https://www.reaper.fm/download.php). Official scripting API, platform binaries and Python setup.
[^44]: Audacity. [Scripting manual](https://manual.audacityteam.org/man/scripting.html) and [license](https://manual.audacityteam.org/man/license.html). Macros, mod-script-pipe and GPLv2.
[^45]: Institute of Electronic Music and Acoustics. [IEM Plug-in Suite](https://plugins.iem.at/). v1.15.0, 10 April 2025; features and GPLv3.
[^46]: Stability AI. [Stable Audio 3 MLX runtime](https://github.com/Stability-AI/stable-audio-3/tree/main/optimized/mlx). Runtime controls, hardware claims, benchmarks and component sizes.
[^47]: Stability AI. [Stable Audio 3 Small-SFX model card](https://huggingface.co/stabilityai/stable-audio-3-small-sfx). 2026; gated access and component terms.
[^48]: ElevenLabs. [Create sound effect API reference](https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert). Current endpoint contract.
[^49]: Ho Kei Cheng and collaborators. [MMAudio repository](https://github.com/hkchengrex/MMAudio). CVPR 2025; inference, limitations and commercial-use qualification.
[^50]: MMAudio authors. [Current demo source](https://github.com/hkchengrex/MMAudio/blob/main/demo.py). Device selection, seeds and controls.
[^51]: Tencent Hunyuan. [HunyuanVideo-Foley repository](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley). 2025; XL/XXL requirements and inference.
[^52]: Tencent Hunyuan. [HunyuanVideo-Foley license](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley/blob/main/LICENSE). Release date 28 August 2025.
[^53]: Xiaomi Research. [ControlFoley repository](https://github.com/xiaomi-research/controlfoley). 2026; conditioning, official integration and split code/weight licenses.
[^54]: DeCLaRe Lab. [TangoFlux model card](https://huggingface.co/declare-lab/TangoFlux). Current checkpoint terms and usage.
[^55]: University of Surrey CVSSP. [AudioLDM2 model card](https://huggingface.co/cvssp/audioldm2). Checkpoint license, sample rate and Diffusers usage.
[^56]: Meta. [AudioCraft repository](https://github.com/facebookresearch/audiocraft). Separate code and weight licenses.
[^57]: OpenMMLab. [FoleyCrafter repository](https://github.com/open-mmlab/FoleyCrafter). Inference, controls and Auffusion dependency notice.
[^58]: Stability AI. [Stable Audio 3 inference methods](https://github.com/Stability-AI/stable-audio-3/blob/main/docs/workflows/inference.md). Current controls and continuation examples.
[^59]: Stability AI. [Current license options and core-model coverage](https://stability.ai/license). Explicitly lists Stable Audio 3.0.
[^60]: Stability AI. [Community license linked by Small-SFX model card](https://huggingface.co/stabilityai/stable-audio-open-1.0/blob/main/LICENSE.md). 5 July 2024; registration, revenue, output and distribution provisions.
[^61]: ElevenLabs. [Sound-effects capability documentation](https://elevenlabs.io/docs/overview/capabilities/sound-effects). Duration, formats, looping and credit cost.
[^62]: ElevenLabs. [API pricing](https://elevenlabs.io/pricing/api). Current advertised dollar rates.
[^63]: ElevenLabs. [Terms of Service](https://elevenlabs.io/terms-of-use). Retrieved non-EEA terms; paid/free commercial-use distinction.
[^64]: ElevenLabs. [Publishing generated content](https://help.elevenlabs.io/hc/en-us/articles/13313564601361-Can-I-publish-the-content-I-generate-on-the-platform). Plan and attribution requirements.
[^65]: Stability AI. [API pricing](https://platform.stability.ai/pricing). Current credit price and starting-credit offer.
[^66]: Stability AI. [Stable Audio 3 prompt guide](https://stability.ai/guides/stable-audio-3-prompt-guide) and [API reference](https://platform.stability.ai/docs/api-reference). Generation and editing capabilities.
[^67]: MMAudio authors. [Model components and downloads](https://github.com/hkchengrex/MMAudio/blob/main/docs/MODELS.md). Checkpoint sizes and dependencies.
[^68]: Tencent Hunyuan. [Foley source constants](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley/blob/main/hunyuanvideo_foley/constants.py). 48 kHz, stereo and input-duration constants.
[^69]: Tencent Hunyuan. [Foley inference source](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley/blob/main/infer.py). Seed and batch inference handling.
[^70]: Xiaomi Research. [ControlFoley demo source](https://github.com/xiaomi-research/controlfoley/blob/main/demo.py). Seeds, device selection and reference input.
[^71]: DeCLaRe Lab. [TangoFlux repository and performance table](https://github.com/declare-lab/TangoFlux). Author-reported A40 benchmark.
[^72]: Meta. [AudioGen model card](https://github.com/facebookresearch/audiocraft/blob/main/model_cards/AUDIOGEN_MODEL_CARD.md). Model description and license.
[^73]: Auffusion authors. [Auffusion license](https://github.com/happylittlecat2333/Auffusion/blob/main/LICENSE). CC BY-NC-SA 4.0.
[^74]: Stability AI. [Stable Audio Open Small model card](https://huggingface.co/stabilityai/stable-audio-open-small). Model and licensing reference.
[^75]: Blender Foundation. [SoundStrip API, Blender 5.2](https://docs.blender.org/api/5.2/bpy.types.SoundStrip.html). Native audio controls.
[^76]: Blender Foundation. [Strip properties, Blender 5.2 LTS](https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/strip_properties.html). Mono panning, pitch preservation and waveform behavior.
[^77]: Blender Foundation. [Audio system API](https://docs.blender.org/api/5.2/aud.html). Native aud capabilities.
