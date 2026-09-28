"""Stream the bounded proof, retaining sample frames and the existing voice take."""
import bpy,json,subprocess,time,runpy
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/gyokeres-proof-v015'
runpy.run_path(str(V/'scripts/check_gyokeres_proof_v015.py'))
s=bpy.data.scenes['S002_Gyokeres_complete_proof_v015'];bpy.context.window.scene=s
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.use_sequencer=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
out=O/'gyokeres-proof-v015-review2.mp4';assert not out.exists()
cmd=['/opt/homebrew/bin/ffmpeg','-v','error','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-i',str(V/'artifacts/animatic-v001/voices/L08-mix.wav'),'-filter_complex','[1:a]adelay=3500|3500,apad[a]','-map','0:v','-map','[a]','-t','14','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)]
start=time.monotonic();temp=O/'working-frame.png'
with (O/'encode.log').open('w') as log:
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
 try:
  for f in range(1,337):
   s.frame_set(f);s.render.filepath=str(temp);bpy.ops.render.render(write_still=True);p.stdin.write(temp.read_bytes())
   if f in [1,6,12,18,24,30,42,54,64,69,78,85,89,98,106,119,127,143,145,157,159,161,163,165,167,169,171,253,261,265,269,273,277,281,282,285,289,297,336]:(O/f'frame-{f:03}.png').write_bytes(temp.read_bytes())
   if f%24==0:print('PROOF_PROGRESS',f,336,round(time.monotonic()-start,1),flush=True)
  p.stdin.close();assert p.wait()==0
 except BaseException:p.kill();p.wait();raise
temp.unlink(missing_ok=True)
(O/'render-checks.json').write_text(json.dumps({'frames':336,'fps':24,'seconds':14,'size':[1280,720],'speech_start_seconds':3.5,'voice_source':'artifacts/animatic-v001/voices/L08-mix.wav','elapsed_seconds':time.monotonic()-start,'status':'review candidate; user acceptance pending'},indent=2))
print('PROOF_COMPLETE',flush=True)
