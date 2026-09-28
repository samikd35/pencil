"""Package one body-motion shot into the accepted edit; label incomplete film honestly."""
from pathlib import Path
import json,subprocess,sys,hashlib
V=Path(__file__).resolve().parents[1];R=V.parents[3];A=V/'artifacts/opening-v002';O=V/'artifacts/animation-v001';P=O/'CP03_pep';FF='/opt/homebrew/bin/ffmpeg'
sys.path.insert(0,str(R/'pipeline'));from checkpoints import require_checkpoint
for revision,stage in [('chase-v002','staging'),('opening-v002','sound'),('opening-v002','animatic')]:require_checkpoint(V,revision,stage)
def run(args):
 p=subprocess.run([str(a) for a in args],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-2000:])
 return p
edit=json.loads((A/'edit.json').read_text());row=next(r for r in edit if r['id']=='CP03_pep');start=(row['start_frame']-1)/24
preview=P/'CP03_pep-v002-with-audio.mp4'
if not preview.exists():run([FF,'-v','error','-i',P/'CP03_pep-v002-silent.mp4','-i',A/'mix-premaster.wav','-filter_complex',f'[1:a]atrim=start_sample={round(start*48000)}:end_sample={round((start+4)*48000)},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-t',4,'-movflags','+faststart',preview])
row['clip']=str(P/'CP03_pep-v002-silent.mp4');row['stage']='body-motion candidate; mouth acting unfinished';(O/'edit.json').write_text(json.dumps(edit,indent=2));(O/'concat.txt').write_text(''.join("file '"+r['clip']+"'\n" for r in edit))
movie=O/'arsenal-progress-v001.mp4'
if not movie.exists():run([FF,'-v','error','-f','concat','-safe','0','-i',O/'concat.txt','-i',A/'mix-premaster.wav','-vf',f'ass={A/"captions.ass"}','-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-frames:v','5954','-t',5954/24,'-movflags','+faststart',movie])
run([FF,'-v','error','-xerror','-i',movie,'-f','null','-']);meta=json.loads(run(['/opt/homebrew/bin/ffprobe','-v','error','-show_streams','-of','json',movie]).stdout);assert int(meta['streams'][0]['nb_frames'])==5954
run([FF,'-v','error','-y','-i',P/'CP03_pep-v002-silent.mp4','-vf','fps=6,scale=320:180,tile=6x4','-frames:v','1',P/'v002-contact.jpg'])
report=dict(frames=5954,seconds=5954/24,replaced_shots=['CP03_pep'],replaced_interval_seconds=[start,start+4],decode='passed',sha256=hashlib.sha256(movie.read_bytes()).hexdigest(),sound='Exact accepted master used; no new voices or effects',finished=False,limits='One body-motion shot; remaining55shots held storyboard. Pep mouth animation and normal-speed gait judgment pending. No accepted motion baseline upgrade.')
(O/'checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
