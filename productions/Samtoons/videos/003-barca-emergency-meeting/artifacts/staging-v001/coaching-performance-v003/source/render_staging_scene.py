"""Render one saved staging scene, with its selected shared-pipeline audio mix.
Blender --background saved.blend --python this.py -- S07 scene_name coaching
"""
import bpy,sys,json,subprocess,hashlib
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=Path(bpy.data.filepath).parent
shot_id,scene_name,base=sys.argv[sys.argv.index('--')+1:]
assert shot_id in ['S05','S06','S07','S08']
S=bpy.data.scenes[scene_name];bpy.context.window.scene=S
S.render.use_sequencer=False;S.render.image_settings.file_format='PNG'
assert S.render.fps==24 and S.render.fps_base==1 and S.frame_start==1
frames=O/('review-frames-'+base if shot_id in ['S05','S08'] else 'review-frames');frames.mkdir(exist_ok=True);temp=O/'working-frame.png';ff='/opt/homebrew/bin/ffmpeg'
p=subprocess.Popen([ff,'-v','error','-y','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(O/f'{base}-picture.mp4')],stdin=subprocess.PIPE)
try:
 for f in range(1,S.frame_end+1):
  S.frame_set(f);temp.unlink(missing_ok=True);S.render.filepath=str(temp)
  assert bpy.ops.render.render(write_still=True)=={'FINISHED'}
  raw=temp.read_bytes();p.stdin.write(raw)
  risky=(shot_id=='S07' and (270<=f<=310 or 333<=f<=352)) or (shot_id=='S06' and f in [70,98,123,151,172,199])
  if f%24==1 or risky or f==S.frame_end:(frames/f'{f:03}.png').write_bytes(raw)
  if f%48==0:print(shot_id,'FRAME',f,flush=True)
 p.stdin.close();assert p.wait()==0
except BaseException:
 p.kill();p.wait();raise
temp.unlink(missing_ok=True)
plan_path=O/'render-selection.json';plan=json.loads(plan_path.read_text());shot=next(x for x in plan['shots'] if x['id']==shot_id);start=(shot['start_frame']-1)*2000
mix=O/'audio/mix-premaster.wav'
subprocess.run([ff,'-v','error','-y','-i',str(O/f'{base}-picture.mp4'),'-i',str(mix),'-filter_complex',f'[1:a]atrim=start_sample={start}:end_sample={start+S.frame_end*2000},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(O/f'{base}-review.mp4')],check=True)
inputs=[Path(bpy.data.filepath),Path(__file__),plan_path,mix]
(O/('render-inputs-'+base+'.json' if shot_id in ['S05','S08'] else 'render-inputs.json')).write_text(json.dumps({str(p.relative_to(V)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},indent=2)+'\n')
print(shot_id,'REVIEW_READY',flush=True)
