"""Native1080 rendering of user-approved branding only."""
import bpy,subprocess,sys
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/delivery-v029'
sys.path.insert(0,str(V.parents[3]))
from pipeline.checkpoints import require_checkpoint
for stage in ['staging','sound','animatic']:require_checkpoint(V,'v028',stage)
proof='stills' in sys.argv
for name,stem in [('SAMTOONS / 03s intro','intro'),('SAMTOONS / 12s outro','outro')]:
 s=bpy.data.scenes[name];bpy.context.window.scene=s;s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100
 temp=O/(stem+'-working.png');frames=[16,48,60] if stem=='intro' else [13,26,40,65,188,250]
 p=None if proof else subprocess.Popen(['/opt/homebrew/bin/ffmpeg','-v','error','-y','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p',str(O/(stem+'-picture.mp4'))],stdin=subprocess.PIPE)
 for f in frames if proof else range(1,s.frame_end+1):
  s.frame_set(f);temp.unlink(missing_ok=True);s.render.filepath=str(temp);assert bpy.ops.render.render(write_still=True)=={'FINISHED'};raw=temp.read_bytes()
  if p:p.stdin.write(raw)
  if f in frames:(O/f'{stem}-{f:03}.png').write_bytes(raw)
  if f%48==0:print('BRANDING',stem,f,s.frame_end,flush=True)
 if p:p.stdin.close();assert p.wait()==0
 temp.unlink(missing_ok=True)
