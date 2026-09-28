"""Assemble substantial acting batch into the complete approved edit."""
from pathlib import Path
import subprocess,json,hashlib
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v004';A=V/'artifacts/opening-v002';FF='/opt/homebrew/bin/ffmpeg'
def run(args):
 p=subprocess.run(list(map(str,args)),capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-2500:])
 return p.stdout
edit=json.loads((V/'artifacts/animation-v003/edit.json').read_text());batch=json.loads((O/'batch.json').read_text())
for row in edit:
 if row['id'] in batch['shots']:
  path=O/'clips'/(row['id']+'.mp4');info=json.loads(run(['/opt/homebrew/bin/ffprobe','-v','error','-show_streams','-of','json',path]))['streams'][0]
  assert int(info['nb_frames'])==row['frames'] and info['r_frame_rate']=='24/1'
  row['clip']=str(path);row['stage']='First acting/prop animation pass; performance polish pending'
(O/'edit.json').write_text(json.dumps(edit,indent=2));(O/'concat.txt').write_text(''.join("file '"+r['clip']+"'\n" for r in edit))
movie=O/'arsenal-progress-v004.mp4';assert not movie.exists()
run([FF,'-v','error','-f','concat','-safe','0','-i',O/'concat.txt','-i',A/'mix-premaster.wav','-vf',f'ass={A/"captions.ass"}','-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-frames:v','5954','-t',5954/24,'-movflags','+faststart',movie])
run([FF,'-v','error','-xerror','-i',movie,'-f','null','-'])
info=json.loads(run(['/opt/homebrew/bin/ffprobe','-v','error','-show_streams','-of','json',movie]));assert int(info['streams'][0]['nb_frames'])==5954
(O/'checks.json').write_text(json.dumps(dict(frames=5954,seconds=5954/24,new_animation_shots=batch['shots'],new_animation_seconds=batch['frames']/24,approved_motion_retained=['CP01','CP03_pep'],remaining_board_shots=[r['id'] for r in edit if r['id'] not in batch['shots']+['CP01','CP03_pep']],decode='passed',sha256=hashlib.sha256(movie.read_bytes()).hexdigest(),sound='Approved mix and captions retained without retiming; final sync/mix review pending',finished=False),indent=2))
print('FULL_PROGRESS_PACKAGED',flush=True)
