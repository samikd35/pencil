#!/usr/bin/env python3
"""Add the approved Samtoons intro and outro to a locked episode master."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
INTRO = HERE / "samtoons-intro-1080p.mp4"
OUTRO = HERE / "samtoons-outro-1080p.mp4"
STAMP = re.compile(r"(\d\d):(\d\d):(\d\d),(\d\d\d)")
TIMING = re.compile(r"^(.*?)\s+-->\s+(.*?)$")


def probe(path: Path) -> dict:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-show_entries", "stream=codec_type,width,height,r_frame_rate,sample_rate,channels",
            "-of", "json", str(path),
        ],
        check=True, capture_output=True, text=True,
    )
    return json.loads(result.stdout)


def media_values(path: Path) -> tuple[float, dict, dict]:
    info = probe(path)
    video = next(stream for stream in info["streams"] if stream["codec_type"] == "video")
    audio = next(stream for stream in info["streams"] if stream["codec_type"] == "audio")
    return float(info["format"]["duration"]), video, audio


def validate(path: Path) -> float:
    duration, video, audio = media_values(path)
    expected = (video["width"], video["height"], video["r_frame_rate"], audio["sample_rate"], audio["channels"])
    if expected != (1920, 1080, "24/1", "48000", 2):
        raise SystemExit(f"{path} must be 1920x1080, 24 fps, stereo 48 kHz; found {expected}")
    return duration


def stamp_to_ms(value: str) -> int:
    match = STAMP.fullmatch(value)
    if not match:
        raise ValueError(f"Invalid SRT timestamp: {value}")
    hours, minutes, seconds, millis = map(int, match.groups())
    return ((hours * 60 + minutes) * 60 + seconds) * 1000 + millis


def ms_to_stamp(value: int) -> str:
    hours, remainder = divmod(value, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, millis = divmod(remainder, 1_000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"


def shift_srt(text: str, intro_at: float) -> str:
    boundary = round(intro_at * 1000)
    shifted = []
    for line in text.splitlines():
        match = TIMING.match(line)
        if not match:
            shifted.append(line)
            continue
        start, end = map(stamp_to_ms, match.groups())
        if start < boundary < end:
            raise ValueError("Place the intro between captions; one subtitle crosses the insertion point")
        if start >= boundary:
            start += 3000
            end += 3000
        shifted.append(f"{ms_to_stamp(start)} --> {ms_to_stamp(end)}")
    return "\n".join(shifted) + ("\n" if text.endswith("\n") else "")


def self_check() -> None:
    assert shift_srt(
        "1\n00:00:01,000 --> 00:00:02,000\nA\n\n2\n00:00:06,000 --> 00:00:07,000\nB\n",
        5,
    ) == "1\n00:00:01,000 --> 00:00:02,000\nA\n\n2\n00:00:09,000 --> 00:00:10,000\nB\n"
    assert abs(validate(INTRO) - 3) < 0.01
    assert abs(validate(OUTRO) - 12) < 0.01
    print("Samtoons branding assets and subtitle shift check passed.")


def assemble(episode: Path, output: Path, intro_at: float, force: bool) -> None:
    duration = validate(episode)
    validate(INTRO)
    validate(OUTRO)
    if not 0 <= intro_at < duration:
        raise SystemExit(f"--intro-at must be between 0 and {duration:.3f} seconds")
    if output.exists() and not force:
        raise SystemExit(f"Output exists: {output} (pass --force to replace it)")

    video = "fps=24,scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p,settb=AVTB"
    audio = "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo"
    if intro_at == 0:
        graph = (
            f"[1:v]{video},setpts=PTS-STARTPTS[vi];[1:a]{audio},asetpts=PTS-STARTPTS[ai];"
            f"[0:v]{video},setpts=PTS-STARTPTS[ve];[0:a]{audio},asetpts=PTS-STARTPTS[ae];"
            f"[2:v]{video},setpts=PTS-STARTPTS[vo];[2:a]{audio},asetpts=PTS-STARTPTS[ao];"
            "[vi][ai][ve][ae][vo][ao]concat=n=3:v=1:a=1[v][a]"
        )
    else:
        graph = (
            f"[0:v]split=2[vp0][vp1];[0:a]asplit=2[ap0][ap1];"
            f"[vp0]trim=end={intro_at},{video},setpts=PTS-STARTPTS[vpre];"
            f"[ap0]atrim=end={intro_at},{audio},asetpts=PTS-STARTPTS[apre];"
            f"[vp1]trim=start={intro_at},{video},setpts=PTS-STARTPTS[vpost];"
            f"[ap1]atrim=start={intro_at},{audio},asetpts=PTS-STARTPTS[apost];"
            f"[1:v]{video},setpts=PTS-STARTPTS[vi];[1:a]{audio},asetpts=PTS-STARTPTS[ai];"
            f"[2:v]{video},setpts=PTS-STARTPTS[vo];[2:a]{audio},asetpts=PTS-STARTPTS[ao];"
            "[vpre][apre][vi][ai][vpost][apost][vo][ao]concat=n=4:v=1:a=1[v][a]"
        )
    subprocess.run(
        [
            "ffmpeg", "-y" if force else "-n", "-v", "error", "-i", str(episode),
            "-i", str(INTRO), "-i", str(OUTRO), "-filter_complex", graph,
            "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium",
            "-crf", "16", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart",
            str(output),
        ],
        check=True,
    )
    actual = validate(output)
    expected = duration + 15
    if abs(actual - expected) > 0.05:
        raise SystemExit(f"Unexpected output duration: {actual:.3f}s, expected {expected:.3f}s")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode", type=Path, nargs="?")
    parser.add_argument("output", type=Path, nargs="?")
    parser.add_argument("--intro-at", type=float, default=0, help="Seconds into the locked episode; default 0")
    parser.add_argument("--subtitles", type=Path)
    parser.add_argument("--output-subtitles", type=Path)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if not args.episode or not args.output:
        parser.error("episode and output are required unless --self-check is used")
    if bool(args.subtitles) != bool(args.output_subtitles):
        parser.error("--subtitles and --output-subtitles must be supplied together")
    if args.episode.resolve() == args.output.resolve():
        parser.error("output must be different from the unbranded episode master")
    if args.subtitles:
        if args.subtitles.resolve() == args.output_subtitles.resolve():
            parser.error("output subtitles must be different from the source subtitles")
        if args.output_subtitles.exists() and not args.force:
            raise SystemExit(f"Output exists: {args.output_subtitles} (pass --force to replace it)")
    assemble(args.episode, args.output, args.intro_at, args.force)
    if args.subtitles:
        args.output_subtitles.write_text(shift_srt(args.subtitles.read_text(), args.intro_at))


if __name__ == "__main__":
    main()
