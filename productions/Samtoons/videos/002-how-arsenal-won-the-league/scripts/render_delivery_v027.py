"""Native 1080p rendering from the exact approved scene/frame selections."""
import bpy, json, subprocess, time, sys, hashlib
from pathlib import Path
V=Path(__file__).resolve().parents[1]; O=V/'artifacts/delivery-v027'
sys.path.insert(0,str(V.parents[3]))
from pipeline.checkpoints import require_checkpoint
# Full-cut delivery approval supersedes earlier scoped review decisions for these inputs.
require_checkpoint(V,'v026','delivery')
rows=json.loads((O/'edit.json').read_text()); sources=json.loads((O/'sources.json').read_text())
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
proof='proof' in args; selected=[a for a in args if a not in ['proof','opening','remaining']]; FF='/opt/homebrew/bin/ffmpeg'; loaded=None; started=time.monotonic()
for name in dict.fromkeys(r['source'] for r in rows):
 for r in rows:
  if r['source']!=name or (selected and r['id'] not in selected): continue
  if 'opening' in args and name=='remaining':continue
  if 'remaining' in args and name!='remaining':continue
  out=O/'clips'/(r['id']+'.mp4'); stamp=out.with_suffix('.json')
  binding=dict(source=sources[name]['sha256'],scene=r['scene'],local_start=r['local_start'],frames=r['frames'],resolution=[1920,1080],samples=24)
  if not proof and out.exists() and stamp.exists() and json.loads(stamp.read_text())==binding:continue
  if loaded!=name:
   file=O/'sources'/(name+'.blend');assert hashlib.sha256(file.read_bytes()).hexdigest()==sources[name]['sha256']
   bpy.ops.wm.open_mainfile(filepath=str(file));loaded=name
  s=bpy.data.scenes[r['scene']];bpy.context.window.scene=s
  s.render.use_sequencer=False;s.render.use_border=False;s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100
  s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=0;s.eevee.taa_render_samples=24
  tmp=O/('working-'+r['id']+'.png')
  indices=[r['frames']//2] if proof else range(r['frames'])
  part=out.with_suffix('.partial.mp4')
  p=None if proof else subprocess.Popen([FF,'-v','error','-y','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p',str(part)],stdin=subprocess.PIPE)
  try:
   for j in indices:
    f=r['local_start']+j;s.frame_set(f)
    markers=[m for m in s.timeline_markers if m.camera and m.frame<=f]
    if markers:s.camera=max(markers,key=lambda m:m.frame).camera
    tmp.unlink(missing_ok=True);s.render.filepath=str(tmp)
    assert bpy.ops.render.render(write_still=True)=={'FINISHED'},(r['id'],f,'render cancelled')
    raw=tmp.read_bytes()
    if p:p.stdin.write(raw)
    if proof or j in [0,r['frames']//2,r['frames']-1]:(O/'review-frames'/f'{r["id"]}-{j:04}.png').write_bytes(raw)
    if j%48==0:print('PROGRESS',r['id'],j+1,r['frames'],round(time.monotonic()-started,1),flush=True)
   if p:
    p.stdin.close();assert p.wait()==0
    n=json.loads(subprocess.check_output(['/opt/homebrew/bin/ffprobe','-v','error','-show_entries','stream=nb_frames,width,height','-of','json',str(part)]))['streams'][0]
    assert (int(n['nb_frames']),n['width'],n['height'])==(r['frames'],1920,1080)
    part.replace(out);stamp.write_text(json.dumps(binding))
  except BaseException:
   if p:p.kill();p.wait()
   part.unlink(missing_ok=True);raise
  tmp.unlink(missing_ok=True);print('DONE',r['id'],round(time.monotonic()-started,1),flush=True)
print('COMPLETE',round(time.monotonic()-started,1),flush=True)
