"""Assemble and verify the small comparison using the preserved original sound."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
revision = sys.argv[1]
assert Path(revision).name == revision
OUT = ROOT / 'artifacts' / revision
BASE = ROOT.parent / '001_heavy_box/artifacts/finish-v002/preview-with-sound.mp4'
sys.path.insert(0, str(ROOT.parent / '001_heavy_box'))
from journal import append_event


def run(arguments):
    return subprocess.run(arguments, check=True, capture_output=True, text=True)


ff = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n']
comparison = OUT / 'stickman-to-cartoon.mp4'
skin_movie = OUT / 'cartoon-with-sound.mp4'
graph = ("[0:v]scale=640:360,pad=640:408:0:48:color=0xfff9ed,"
         "drawtext=text='ORIGINAL STICKMAN':x=24:y=16:fontsize=20:fontcolor=0x25394c[a];"
         "[1:v]pad=640:408:0:48:color=0xfff9ed,"
         "drawtext=text='SAME MOTION / CARTOON SURFACE':x=24:y=16:fontsize=20:fontcolor=0x25394c[b];"
         "[a][b]hstack[v]")
run(ff + ['-i', str(BASE), '-i', str(OUT / 'cartoon-picture.mp4'), '-filter_complex', graph,
          '-map', '[v]', '-map', '0:a:0', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p',
          '-c:a', 'copy', '-movflags', '+faststart', str(comparison)])
run(ff + ['-i', str(OUT / 'cartoon-picture.mp4'), '-i', str(BASE), '-map', '0:v:0',
          '-map', '1:a:0', '-c', 'copy', '-movflags', '+faststart', str(skin_movie)])
run(ff + ['-i', str(comparison), '-vf', "select='eq(n,117)'", '-frames:v', '1',
          '-update', '1', str(OUT / 'comparison.png')])
run(ff + ['-i', str(skin_movie), '-vf', r'select=not(mod(n\,10)),tile=6x4',
          '-frames:v', '1', '-update', '1', str(OUT / 'motion-sheet.png')])
checks = {}
for movie in (comparison, skin_movie):
    data = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(movie)]).stdout)
    video = next(s for s in data['streams'] if s['codec_type'] == 'video')
    audio = next(s for s in data['streams'] if s['codec_type'] == 'audio')
    assert video['nb_frames'] == '240' and video['r_frame_rate'] == '24/1'
    assert abs(float(video['duration']) - 10) < .001
    assert audio['sample_rate'] == '48000' and audio['channels'] == 2
    run(['ffmpeg', '-v', 'error', '-i', str(movie), '-f', 'null', '-'])
    checks[movie.name] = {'frames': 240, 'seconds': 10, 'fps': 24,
        'width': video['width'], 'height': video['height'], 'audio_channels': 2,
        'audio_sample_rate': 48000, 'complete_decode': 'passed',
        'sha256': hashlib.sha256(movie.read_bytes()).hexdigest()}
# Compare decoded audio bytes, rather than assuming stream copy proves preservation.
def audio_hash(path):
    return run(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0',
                '-c:a', 'pcm_s16le', '-f', 'hash', '-hash', 'sha256', '-']).stdout.strip()
assert audio_hash(BASE) == audio_hash(comparison) == audio_hash(skin_movie)
checks['original_decoded_sound_preserved'] = True
checks['review_limit'] = 'Mechanism proof; sampled visual inspection and technical checks are not full playback acceptance.'
(OUT / 'video-checks.json').write_text(json.dumps(checks, indent=2)+'\n')
for script in ('build_skin.py', 'finish_proof.py'):
    (OUT / ('source-' + script)).write_bytes((ROOT / script).read_bytes())
append_event(ROOT, stage='checkpoint/'+revision+'/staging', status='pending_review',
    intent='Compare fuller cartoon artwork on the same proven movement',
    method='Ten-second low-resolution comparison with unchanged decoded source sound',
    inputs=['build_skin.py', 'finish_proof.py', 'README.md'],
    outputs=[str((OUT / name).relative_to(ROOT)) for name in
             ('stickman-to-cartoon.mp4', 'cartoon-with-sound.mp4', 'comparison.png',
              'cartoon-skin.blend', 'checks.json', 'video-checks.json')],
    result='Both movies decode completely at 24 fps/240 frames. All control frames, projected hand/shoe geometry and decoded sound are preserved. Native samples inspected; no user acceptance or full subjective playback claimed.',
    decision='Review whether this fuller rubber-hose construction is a useful cartoon direction before adding detailed artwork.')
print(json.dumps(checks, indent=2))
