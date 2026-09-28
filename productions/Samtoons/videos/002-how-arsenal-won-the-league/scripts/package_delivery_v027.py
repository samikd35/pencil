"""Finish the native 1080p render with the approved soundtrack and editorial graphics."""
from pathlib import Path
import subprocess,json,hashlib
V=Path(__file__).resolve().parents[1];O=V/'artifacts/delivery-v027';FF='/opt/homebrew/bin/ffmpeg';FP='/opt/homebrew/bin/ffprobe'
rows=json.loads((O/'edit.json').read_text())
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True)
def probe(p):return json.loads(run([FP,'-v','error','-show_streams','-of','json',str(p)]).stdout)['streams']
for r in rows:
 p=O/'clips'/(r['id']+'.mp4');s=probe(p)[0]
 assert (s['width'],s['height'],int(s['nb_frames']),s['r_frame_rate'])==(1920,1080,r['frames'],'24/1'),r['id']
 assert p.with_suffix('.json').exists(),r['id']
(O/'picture-list.txt').write_text(''.join("file '"+str(O/'clips'/(r['id']+'.mp4'))+"'\n" for r in rows))
run([FF,'-v','error','-y','-f','concat','-safe','0','-i',str(O/'picture-list.txt'),'-c','copy',str(O/'picture-1080p.mp4')])
approved=V/'artifacts/delivery-review-v026/samtoons-complete-v026.mp4'
run([FF,'-v','error','-y','-i',str(approved),'-map','0:a:0','-c:a','copy',str(O/'approved-soundtrack.m4a')])
r=next(r for r in rows if r['id']=='FR04');start=(r['start_frame']-1)/24;end=start+r['frames']/24
enable=f'gte(t,{start})*lt(t,{end})'
vf=f"drawbox=x=188:y=0:w=1202:h=98:color=0x1c283f:t=fill:enable='{enable}',drawtext=fontfile=/System/Library/Fonts/Supplemental/Arial.ttf:text='LEAGUE TABLE    1st ARSENAL    2nd CITY':fontsize=42:fontcolor=0xf7f1df:x=227:y=27:enable='{enable}',ass={O/'subtitles.ass'}"
movie=O/'samtoons-final-1080p.mp4'
run([FF,'-v','error','-y','-i',str(O/'picture-1080p.mp4'),'-i',str(O/'approved-soundtrack.m4a'),'-map','0:v:0','-map','1:a:0','-vf',vf,'-c:v','libx264','-crf','16','-preset','slow','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(movie)])
streams=probe(movie);v=next(s for s in streams if s['codec_type']=='video');a=next(s for s in streams if s['codec_type']=='audio')
assert (v['width'],v['height'],int(v['nb_frames']),v['r_frame_rate'])==(1920,1080,6634,'24/1')
assert (a['sample_rate'],a['channels'])==('48000',2)
assert abs(float(v['duration'])-float(a['duration']))<1/24
run([FF,'-v','error','-i',str(movie),'-f','null','-'])
def audiohash(path):return run([FF,'-v','error','-i',str(path),'-map','0:a:0','-c:a','pcm_s24le','-f','hash','-hash','sha256','-']).stdout.strip()
assert audiohash(approved)==audiohash(movie),'Selected audio changed'
# Every decoded presentation interval is one frame; reject dropped or duplicated timestamps.
pts=json.loads(run([FP,'-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',str(movie)]).stdout)['frames']
times=[float(f['best_effort_timestamp_time']) for f in pts]
assert len(times)==6634 and max(abs(b-a-1/24) for a,b in zip(times,times[1:]))<.00001
checks=dict(resolution=[1920,1080],native_render=True,frames=6634,fps=24,seconds=float(v['duration']),audio_seconds=float(a['duration']),decode_passed=True,uniform_frame_timestamps=True,approved_audio_pcm_sha256=audiohash(movie),sha256=hashlib.sha256(movie.read_bytes()).hexdigest(),bytes=movie.stat().st_size)
(O/'checks.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
