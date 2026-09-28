"""Render changed shots only; retain focused consecutive frames without a giant PNG sequence."""
import bpy,json,subprocess,time
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/batch02-v017';rows=json.loads((O/'edit.json').read_text());rows=[r for r in rows if r['start_frame']>=518];F=O/'review-frames';F.mkdir(exist_ok=True);temp=O/'working.png';out=O/'changed-picture.mp4';assert not out.exists();start=time.monotonic();count=0
cmd=['/opt/homebrew/bin/ffmpeg','-v','error','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
with (O/'encode.log').open('w') as log:
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
 try:
  for row in rows:
   s=bpy.data.scenes[row['scene']];bpy.context.window.scene=s;s.render.use_sequencer=False;s.render.resolution_percentage=100;s.render.use_border=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.eevee.taa_render_samples=24
   print('SHOT_START',row['id'],flush=True)
   for f in range(row['local_start'],row['local_start']+row['frames']):
    s.frame_set(f);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=f),key=lambda m:m.frame).camera;s.render.filepath=str(temp);bpy.ops.render.render(write_still=True);raw=temp.read_bytes();p.stdin.write(raw);count+=1
    focused=(row['id']=='OP03_phone' and 338<=f<=352) or (row['id']=='TR01' and (20<=f<=30 or 42<=f<=73 or 180<=f<=192)) or (row['id']=='TR02_flag' and 193<=f<=205) or (row['id']=='TR03_kick' and 108<=f<=147)
    if focused or f in [row['local_start'],row['local_start']+row['frames']//2,row['local_start']+row['frames']-1]:(F/f'{row["id"]}-{f:03}.png').write_bytes(raw)
   print('SHOT_DONE',row['id'],count,round(time.monotonic()-start,1),flush=True)
  p.stdin.close();assert p.wait()==0
 except BaseException:p.kill();p.wait();raise
assert count==804;temp.unlink(missing_ok=True);(O/'render-checks.json').write_text(json.dumps({'changed_frames':count,'fps':24,'reused_prefix_frames':517,'total_frames':1321,'elapsed_seconds':time.monotonic()-start,'acceptance':'pending user review'},indent=2));print('DONE',flush=True)
