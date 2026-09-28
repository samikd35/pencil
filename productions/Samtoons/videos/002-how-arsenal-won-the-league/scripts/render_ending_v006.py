"""Render the ending from the saved native scenes; bounded temporary storage."""
import bpy,json,subprocess,math
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v006';FF='/opt/homebrew/bin/ffmpeg'
shots=[('S002_v005_N04_dark',96),('S002_v005_N04_reveal',36),('S002_v006_N04_meltdown',168),('S002_v006_N04_tap',60)]
room=bpy.data.collections['S002 / Narrator room / shared v005'];checks={}
for name,count in shots:
 s=bpy.data.scenes[name];assert room in list(s.collection.children);assert s.frame_end==count
 if 'v006' in name:
  for f in range(1,count+1):
   s.frame_set(f);skins=[o for o in s.objects if o.name.endswith(' / continuous skin') and not o.hide_render];assert len(skins)==1,(name,f,len(skins))
 checks[name]={'frames':count,'shared_room':True}
s=bpy.data.scenes[shots[-1][0]];bpy.context.window.scene=s;s.frame_set(20);bpy.context.view_layer.update();p=bpy.data.objects['Ferguson / released notes'];contact=max((p.matrix_world@v.co).x for v in p.data.vertices);assert abs(contact-3.344)<1e-4,contact
s.frame_set(10);bpy.context.view_layer.update();hand=bpy.data.objects['Ferguson / follow through / Lf'];assert (p.matrix_world.translation-hand.matrix_world.translation).length<1e-4
checks['paper']={'surface_x_at_frame20':contact,'release_matches_hand':True}
(O/'native-checks.json').write_text(json.dumps(checks,indent=2))
(O/'frames').mkdir(exist_ok=True)
for name,count in shots:
 s=bpy.data.scenes[name];bpy.context.window.scene=s;s.render.use_sequencer=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.resolution_percentage=100;s.eevee.taa_render_samples=16
 output=O/(name+'.mp4')
 if output.exists():continue
 temp=O/'working-frame.png';partial=output.with_suffix('.partial.mp4')
 with (O/'encode.log').open('a') as log:
  proc=subprocess.Popen([FF,'-v','error','-y','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(partial)],stdin=subprocess.PIPE,stderr=log)
  try:
   for f in range(1,count+1):
    s.frame_set(f);s.render.filepath=str(temp);bpy.ops.render.render(write_still=True);raw=temp.read_bytes();proc.stdin.write(raw)
    if f in [1,5,6,7,8,13,14,19,20,32,94,142,143,151,156,168]: (O/'frames'/f'{name}-{f:03}.png').write_bytes(raw)
   proc.stdin.close();assert proc.wait()==0
  except BaseException:proc.kill();proc.wait();raise
 partial.replace(output);temp.unlink(missing_ok=True);print('SHOT_COMPLETE',name,flush=True)
rows=json.loads((V/'artifacts/animation-v003/edit.json').read_text());first=next(x for x in rows if x['id']=='N04_dark');start=(first['start_frame']-1)*2000
(O/'concat.txt').write_text(''.join("file '"+name+".mp4'\n" for name,count in shots))
subprocess.run([FF,'-v','error','-y','-f','concat','-safe','0','-i',str(O/'concat.txt'),'-i',str(V/'artifacts/opening-v002/mix-premaster.wav'),'-filter_complex',f'[1:a]atrim=start_sample={start}:end_sample={start+360*2000},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(O/'ferguson-ending-v006.mp4')],check=True)
print('ENDING_COMPLETE',flush=True)
