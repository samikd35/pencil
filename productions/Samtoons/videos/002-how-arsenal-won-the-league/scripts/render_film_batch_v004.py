"""Resume-safe batch rendering; one temporary frame, no unbounded PNG sequence."""
import bpy,json,subprocess,time,sys
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v004';FF='/opt/homebrew/bin/ffmpeg'
batch=json.loads((O/'batch.json').read_text());preview='--preview' in sys.argv
for sid in batch['shots']:
 s=bpy.data.scenes['S002_fullmotion_'+sid];bpy.context.window.scene=s
 s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.eevee.taa_render_samples=4
 if preview:
  s.render.resolution_percentage=50;s.frame_set(min(24,s.frame_end));s.render.filepath=str(O/'frames'/(sid+'.png'));bpy.ops.render.render(write_still=True);continue
 output=O/'clips'/(sid+'.mp4')
 if output.exists():continue
 temp=O/'working-frame.png';partial=O/'clips'/(sid+'.partial.mp4');s.render.resolution_percentage=100
 with (O/'encode.log').open('a') as log:
  p=subprocess.Popen([FF,'-v','error','-y','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(partial)],stdin=subprocess.PIPE,stderr=log)
  try:
   for f in range(1,s.frame_end+1):
    s.frame_set(f);s.render.filepath=str(temp);bpy.ops.render.render(write_still=True);p.stdin.write(temp.read_bytes())
   p.stdin.close();assert p.wait()==0
  except BaseException:p.kill();p.wait();raise
 partial.replace(output);temp.unlink(missing_ok=True);print('SHOT_COMPLETE',sid,s.frame_end,flush=True)
print('BATCH_RENDER_COMPLETE',flush=True)
