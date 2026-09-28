"""Create and verify A/B checkpoints, or finish the selected A animatic/full movie."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REV = os.environ.get('PENCIL_REVISION', 'film-v003')
OUT = ROOT / 'artifacts' / REV
FF = '/opt/homebrew/bin/ffmpeg'
PROBE = '/opt/homebrew/bin/ffprobe'


def run(args):
    return subprocess.run(args, capture_output=True, text=True, check=True)


def measured(path):
    result = run([FF, '-hide_banner', '-i', str(path), '-vn', '-af',
                  'loudnorm=I=-18:TP=-2:LRA=11:print_format=json', '-f', 'null', '-'])
    return json.loads(re.findall(r'\{[^{}]+\}', result.stderr)[-1])


def verify(movie, width, height, frames, seconds):
    data = json.loads(run([PROBE, '-v', 'error', '-count_frames', '-show_streams',
                           '-show_format', '-of', 'json', str(movie)]).stdout)
    video = next(s for s in data['streams'] if s['codec_type'] == 'video')
    sound = next(s for s in data['streams'] if s['codec_type'] == 'audio')
    assert (video['width'], video['height'], video['r_frame_rate'], int(video['nb_read_frames'])) == (width, height, '24/1', frames)
    assert abs(float(data['format']['duration']) - seconds) < .05
    assert sound['channels'] == 2 and sound['sample_rate'] == '48000'
    decoded = run([FF, '-v', 'error', '-i', str(movie), '-f', 'null', '-'])
    assert not decoded.stderr.strip(), decoded.stderr
    levels = measured(movie)
    assert float(levels['input_tp']) <= -1, levels
    return dict(path=movie.name, sha256=hashlib.sha256(movie.read_bytes()).hexdigest(),
                width=width, height=height, frames=frames, fps=24, seconds=seconds,
                channels=2, sample_rate=48000, full_decode=True, levels=levels)


def mux(picture, wav, movie, start, seconds):
    result = run([FF, '-hide_banner', '-n', '-i', str(picture),
                  '-ss', str(start), '-t', str(seconds), '-i', str(wav),
                  '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy',
                  '-af', f'afade=t=out:st={seconds-.2}:d=0.2', '-c:a', 'aac',
                  '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', str(movie)])
    movie.with_suffix('.mux.log').write_text(result.stderr)


if '--animatic' in sys.argv or '--full' in sys.argv:
    sys.path.insert(0, str(ROOT.parents[1]))
    from pipeline.checkpoints import require_checkpoint
    full = '--full' in sys.argv
    for stage in ('staging', 'sound') + (('animatic',) if full else ()):
        require_checkpoint(ROOT, REV, stage)
    movie = OUT / ('barcelona-wasnt-ready-trent-was.mp4' if full else 'animatic-A-clean.mp4')
    wav = OUT / 'soundtrack.wav' if (OUT / 'soundtrack.wav').exists() else OUT / 'review-A.wav'
    mux(OUT / ('full-picture.mp4' if full else 'animatic-picture.mp4'), wav, movie, 0, 38)
    report = verify(movie, 1080 if full else 540, 1920 if full else 960, 912, 38)
    report['listening'] = 'A sound direction selected by user; complete-movie listening not performed by agent.'
    (OUT / ('video-checks.json' if full else 'animatic-checks.json')).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    sys.exit(0)

reports = []
for letter, name in [('A', 'clean'), ('B', 'crowd')]:
    audio = OUT / f'audio-{name}-v003'
    wav = OUT / f'review-{letter}.wav'
    movie = OUT / f'checkpoint-{letter}-{name}.mp4'
    run([FF, '-hide_banner', '-n', '-i', str(audio / 'mix-premaster.wav'), '-af',
         'volume=3dB,alimiter=limit=0.794:level=false:latency=true',
         '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s24le', str(wav)])
    mux(OUT / 'staging-picture.mp4', wav, movie, 10, 12)
    reports.append(dict(candidate=letter, **verify(movie, 540, 960, 288, 12)))

# Isolate the uncertain layer at the same authored level as candidate B.
run([FF, '-hide_banner', '-n', '-ss', '10', '-t', '12',
     '-i', str(OUT / 'audio-crowd-v003/stems/atmosphere.wav'), '-af',
     'volume=3dB,alimiter=limit=0.794:level=false:latency=true,afade=t=out:st=11.8:d=0.2',
     '-ar', '48000', '-c:a', 'pcm_s24le', str(OUT / 'crowd-layer-isolated.wav')])
(OUT / 'checkpoint-checks.json').write_text(json.dumps(dict(
    candidates=reports, comparison='Same picture and foreground gain; B adds recorded crowd ambience.',
    audio_finishing='Common +3 dB gain and -2 dBFS peak limiter; no separate A/B loudness normalization.',
    contacts_seconds=[6.75, 8.0, 8.625], listening='Pending user audition; numerical checks do not certify perceived quality.',
    scope='Staging and sound proof, not a complete animatic or final film.'), indent=2) + '\n')
print(json.dumps(reports, indent=2))
