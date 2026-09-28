"""Add CP01 body motion to the existing progress edit, preserving accepted Pep/audio."""
from pathlib import Path
import subprocess,json,hashlib,sys
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v002';P=O/'CP01';A=V/'artifacts/opening-v002';FF='/opt/homebrew/bin/ffmpeg'
sys.path.insert(0,str(V.parents[3]/'pipeline'));from checkpoints import require_checkpoint
for rev,stage in [('chase-v002','staging'),('opening-v002','sound'),('opening-v002','animatic'),('CP03_pep-v002','staging')]:require_checkpoint(V,rev,stage)
def run(args):
 p=subprocess.run([str(x) for x in args],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-3000:])
 return p.stdout
edit=json.loads((V/'artifacts/animation-v001/edit.json').read_text());row=next(r for r in edit if r['id']=='CP01');first=(row['start_frame']-1)*2000;end=first+row['frames']*2000
preview=P/'CP01-v001-with-audio.mp4'
assert not preview.exists()
run([FF,'-v','error','-i',P/'CP01-v001-silent.mp4','-i',A/'mix-premaster.wav','-filter_complex',f'[1:a]atrim=start_sample={first}:end_sample={end},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-t','9','-movflags','+faststart',preview])
row['clip']=str(P/'CP01-v001-silent.mp4');row['stage']='body motion candidate; phone transition and final acting unfinished'
next(r for r in edit if r['id']=='CP03_pep')['stage']='user-approved body motion; mouth acting unfinished'
(O/'edit.json').write_text(json.dumps(edit,indent=2));(O/'concat.txt').write_text(''.join("file '"+r['clip']+"'\n" for r in edit))
movie=O/'arsenal-progress-v002.mp4';assert not movie.exists()
run([FF,'-v','error','-f','concat','-safe','0','-i',O/'concat.txt','-i',A/'mix-premaster.wav','-vf',f'ass={A/"captions.ass"}','-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-frames:v','5954','-t',5954/24,'-movflags','+faststart',movie])
for path,frames in [(preview,216),(movie,5954)]:
 run([FF,'-v','error','-xerror','-i',path,'-f','null','-'])
 info=json.loads(run(['/opt/homebrew/bin/ffprobe','-v','error','-show_streams','-of','json',path]));assert int(info['streams'][0]['nb_frames'])==frames
(O/'checks.json').write_text(json.dumps(dict(frames=5954,seconds=5954/24,body_motion_shots=['CP01','CP03_pep'],approved_body_motion=['CP03_pep'],decode='passed',sha256=hashlib.sha256(movie.read_bytes()).hexdigest(),sound='Unchanged approved master; CP01 preview exact 98.6667–107.6667 second source interval',finished=False),indent=2))
print('Packaged CP01 and full progress v002; accepted Pep and soundtrack retained.')
