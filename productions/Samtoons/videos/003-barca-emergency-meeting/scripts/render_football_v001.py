"""Encode the saved S06 staging sequence; no authoring or full-film render."""
from pathlib import Path
import bpy, subprocess, hashlib, json
V=Path(__file__).resolve().parents[1];O=V/'artifacts/staging-v001/football-performance-v001';S=bpy.data.scenes['S003_S06_Football_v001'];bpy.context.window.scene=S
assert Path(bpy.data.filepath)==O/'football-performance.blend'
S.render.use_sequencer=False;S.render.image_settings.file_format='PNG'
frames=O/'review-frames';frames.mkdir(exist_ok=True);temp=O/'working-frame.png';ff='/opt/homebrew/bin/ffmpeg'
p=subprocess.Popen([ff,'-v','error','-y','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(O/'football-picture.mp4')],stdin=subprocess.PIPE)
try:
 for f in range(1,313):
  S.frame_set(f);temp.unlink(missing_ok=True);S.render.filepath=str(temp);assert bpy.ops.render.render(write_still=True)=={'FINISHED'};raw=temp.read_bytes();p.stdin.write(raw)
  if f%12==1 or 119<=f<=127 or 148<=f<=154 or 188<=f<=220 or f in [68,98,99,142,143,172,312]: (frames/f'{f:03}.png').write_bytes(raw)
  if f%24==0:print('S06_FRAME',f,flush=True)
 p.stdin.close();assert p.wait()==0
except BaseException:
 p.kill();p.wait();raise
temp.unlink(missing_ok=True)
plan=json.loads((V/'production.json').read_text());shot=next(x for x in plan['shots'] if x['id']=='S06');start=(shot['start_frame']-1)*2000
subprocess.run([ff,'-v','error','-y','-i',str(O/'football-picture.mp4'),'-i',str(O/'audio/mix-premaster.wav'),'-filter_complex',f'[1:a]atrim=start_sample={start}:end_sample={start+624000},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(O/'football-review.mp4')],check=True)
inputs=[Path(bpy.data.filepath),Path(__file__),V/'scripts/build_football_v001.py',V/'production.json',O/'audio/mix-premaster.wav']
(O/'render-inputs.json').write_text(json.dumps({str(p.relative_to(V)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},indent=2)+'\n')
print('S06_REVIEW_READY',flush=True)
