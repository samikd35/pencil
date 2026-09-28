#!/usr/bin/env python3
"""Fit the selected Gemini phrases to the approved Samtoons branding motion."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[3]
BRANDING = PROJECT / "productions/Samtoons/videos/002-how-arsenal-won-the-league/artifacts/branding-v028"
DELIVERY = PROJECT / "productions/Samtoons/videos/002-how-arsenal-won-the-league/artifacts/delivery-v029"


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def probe(path: Path) -> dict:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-show_entries",
            "stream=codec_type,sample_rate,channels,width,height,r_frame_rate,nb_frames",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> None:
    intro_source = HERE / "sources/intro-gemini.mp3"
    outro_source = HERE / "sources/outro-gemini.mp3"
    intro_music = HERE / "intro-music-fit.wav"
    outro_music = HERE / "outro-music-fit.wav"

    # 0.32-2.72 is the generated intro's complete quiet-to-resolution phrase.
    # Preserve this exact reviewed filter chain; the final mix pads its release to 3s.
    run(
        "ffmpeg", "-y", "-v", "error", "-i", str(intro_source),
        "-af",
        "atrim=start=0.32:end=2.72,asetpts=PTS-STARTPTS,atempo=1.28,"
        "adelay=1125|1125,apad,atrim=duration=3,afade=t=out:st=2.88:d=0.12,"
        "loudnorm=I=-22:TP=-2:LRA=18,aresample=48000",
        "-c:a", "pcm_s24le", str(intro_music),
    )

    # 2.65-14.65 starts on a phrase boundary and reaches the track's first clean fallaway.
    # The opening duck preserves the paper gag; the last 450ms closes cleanly at 12s.
    run(
        "ffmpeg", "-y", "-v", "error", "-i", str(outro_source),
        "-af",
        "atrim=start=2.65:end=14.65,asetpts=PTS-STARTPTS,"
        "volume='if(lt(t,1.5),0.25+0.75*t/1.5,1)':eval=frame,"
        "afade=t=out:st=11.55:d=0.45,loudnorm=I=-24:TP=-2:LRA=14,aresample=48000",
        "-c:a", "pcm_s24le", str(outro_music),
    )

    outputs = {}
    for stem, seconds in (("intro", 3), ("outro", 12)):
        music = HERE / f"{stem}-music-fit.wav"
        foley = BRANDING / f"{stem}-audio/stems/foley.wav"
        mix = HERE / f"{stem}-mix-review.wav"
        video = HERE / f"{stem}-review.mp4"
        picture = DELIVERY / f"{stem}-1080p.mp4"
        run(
            "ffmpeg", "-y", "-v", "error", "-i", str(foley), "-i", str(music),
            "-filter_complex",
            f"[0:a][1:a]amix=inputs=2:weights='1 1':normalize=0,"
            f"alimiter=limit=0.891,apad,atrim=duration={seconds}[a]",
            "-map", "[a]", "-ar", "48000", "-c:a", "pcm_s24le", str(mix),
        )
        run(
            "ffmpeg", "-y", "-v", "error", "-i", str(picture), "-i", str(mix),
            "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
            "-b:a", "256k", "-t", str(seconds), str(video),
        )
        info = probe(video)
        duration = float(info["format"]["duration"])
        assert abs(duration - seconds) < 0.01, (video, duration)
        outputs[video.name] = {"duration_seconds": duration, "sha256": sha256(video), "probe": info}

    concat = HERE / "review-concat.txt"
    concat.write_text("file 'intro-review.mp4'\nfile 'outro-review.mp4'\n")
    combined = HERE / "intro-outro-review.mp4"
    run("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(combined))
    combined_duration = float(probe(combined)["format"]["duration"])
    assert abs(combined_duration - 15) < 0.05, combined_duration
    outputs[combined.name] = {"duration_seconds": combined_duration, "sha256": sha256(combined)}

    analysis = {
        "status": "selected by user for animated-v002 on 2026-09-22",
        "user_selection": "I love the motion in the music.",
        "sources": {
            intro_source.name: {"sha256": sha256(intro_source), "duration_seconds": 61.283208},
            outro_source.name: {"sha256": sha256(outro_source), "duration_seconds": 59.141167},
        },
        "selections": {
            "intro": {"source_interval_seconds": [0.32, 2.72], "tempo_factor": 1.28, "review_signal_activity_seconds": [0.52, 1.60]},
            "outro": {"source_interval_seconds": [2.65, 14.65], "opening_duck_seconds": 1.5, "fade_out_seconds": [11.55, 12.0]},
        },
        "outputs": outputs,
    }
    (HERE / "analysis.json").write_text(json.dumps(analysis, indent=2) + "\n")


if __name__ == "__main__":
    build()
