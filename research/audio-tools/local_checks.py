"""Small, repeatable checks of the existing audio tools; no model inference.

Run with the project's NumPy-capable Python. Temporary audio is deleted.
"""
from datetime import datetime, timezone
from fractions import Fraction
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
import wave

import numpy as np

SR = 48_000


def command(args):
    return subprocess.run(args, check=True, capture_output=True)


def main():
    ffmpeg = shutil.which("ffmpeg")
    assert ffmpeg, "FFmpeg must be on PATH"
    filters = command([ffmpeg, "-hide_banner", "-filters"]).stdout.decode()
    required = ("adelay", "amix", "afir", "loudnorm", "ebur128", "astats",
                "silencedetect", "rubberband", "aresample", "acrossfade", "afftdn")
    assert all(name in filters for name in required)
    results = {"checked_at": datetime.now(timezone.utc).isoformat(),
               "machine": platform.machine(), "python": platform.python_version(),
               "ffmpeg": command([ffmpeg, "-version"]).stdout.decode().splitlines()[0],
               "filters_present": list(required), "tests": []}
    results["packages"] = {}
    for package in ("numpy", "scipy", "soundfile", "pedalboard", "librosa", "soxr", "pyloudnorm", "torch"):
        try:
            results["packages"][package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            results["packages"][package] = None
    with tempfile.TemporaryDirectory(prefix="pencil-audio-check-") as folder:
        source = Path(folder) / "impulse.wav"
        impulse = np.zeros((128, 2), dtype="<i2")
        impulse[0] = 8192
        with wave.open(str(source), "wb") as f:
            f.setparams((2, 2, SR, 0, "NONE", "not compressed"))
            f.writeframes(impulse.tobytes())
        for fps in (Fraction(24, 1), Fraction(30000, 1001)):
            frame, origin = 38, 1
            exact_sample = (frame - origin) * SR / fps
            offset = round(exact_sample)
            assert abs(Fraction(offset) - exact_sample) <= Fraction(1, 2)
            raw = command([ffmpeg, "-v", "error", "-i", str(source), "-af",
                           f"adelay={offset}S:all=1", "-f", "s16le", "-acodec",
                           "pcm_s16le", "pipe:1"]).stdout
            audio = np.frombuffer(raw, dtype="<i2").reshape(-1, 2)
            found = np.flatnonzero(audio[:, 0])
            assert found.tolist() == [offset] and len(audio) == offset + len(impulse)
            results["tests"].append({"test": "sample_exact_delay", "fps": str(fps),
                                     "frame": frame, "expected_sample": offset,
                                     "observed_sample": int(found[0]), "passed": True})
        # Stream one minute to FFmpeg without allocating a full-length timeline.
        block_size, total = 8192, SR * 60
        count = 0
        with subprocess.Popen([ffmpeg, "-v", "error", "-f", "f32le", "-ar", str(SR),
                               "-ac", "2", "-i", "pipe:0", "-af", "volume=0.5",
                               "-f", "null", "-"], stdin=subprocess.PIPE,
                              stdout=subprocess.DEVNULL, stderr=subprocess.PIPE) as proc:
            for start in range(0, total, block_size):
                n = min(block_size, total - start)
                t = (start + np.arange(n, dtype=np.float64)) / SR
                mono = (0.1 * np.sin(2 * np.pi * 440 * t)).astype("<f4")
                block = np.column_stack((mono, mono))
                assert np.isfinite(block).all()
                proc.stdin.write(block.tobytes())
                count += len(block)
            proc.stdin.close()
            errors = proc.stderr.read().decode()
            assert proc.wait() == 0, errors
        assert count == total
        results["tests"].append({"test": "block_stream_to_ffmpeg", "passed": True,
                                 "audio_frames": count, "block_audio_bytes": block_size * 2 * 4,
                                 "scope": "Bounded block arrays, not an RSS benchmark or full stem mixer"})
    results["one_hour_stereo_array_bytes"] = {
        "float64_per_stem": SR * 3600 * 2 * 8,
        "float32_per_stem": SR * 3600 * 2 * 4,
        "three_float64_stems_before_temporaries": SR * 3600 * 2 * 8 * 3}
    results["not_tested"] = ["AI models", "new package installation", "subjective listening",
                             "third-party applications", "full production retiming or mixing"]
    path = Path(__file__).with_name("local-checks.json")
    path.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
