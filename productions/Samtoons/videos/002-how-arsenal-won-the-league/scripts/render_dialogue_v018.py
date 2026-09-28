"""Render modified speaking shots; reuse the selected physical-action shots unchanged."""
import bpy,json,subprocess,time
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/dialogue-v018';rows=json.loads((O/'edit.json').read_text());old={r['id']:r for r in json.loads((V/'artifacts/batch02-v017/edit.json').read_text())};F=O/'review-frames';F.mkdir(exist_ok=True);clips=O/'clips';clips.mkdir(exist_ok=True);FF='/opt/homebrew/bin/ffmpeg';unchanged={'N01','OP01_banner','OP02_truck','TR01','TR03_kick','TR04'};temp=O/'working.png';start=time.monotonic();count=0
for row in rows:
 out=clips/(row['id']+'.mp4')
 if out.exists():continue
 if row['id'] in unchanged:
  r=old[row['id']];subprocess.run([FF,'-v','error','-y','-i',str(V/'artifacts/batch02-v017/batches01-02-review-v017.mp4'),'-vf',f'trim=start_frame={r["start_frame"]-1}:end_frame={r["start_frame"]-1+r["frames"]},setpts=PTS-STARTPTS','-an','-c:v','libx264','-crf','18','-preset','fast',str(out)],check=True);print('REUSE',row['id'],flush=True);continue
 s=bpy.data.scenes[row['scene']];bpy.context.window.scene=s;s.render.use_sequencer=False;s.render.resolution_percentage=100;s.render.use_border=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.eevee.taa_render_samples=24
 p=subprocess.Popen([FF,'-v','error','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
 try:
  for f in range(row['local_start'],row['local_start']+row['frames']):
   s.frame_set(f);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=f),key=lambda m:m.frame).camera;s.render.filepath=str(temp);bpy.ops.render.render(write_still=True);raw=temp.read_bytes();p.stdin.write(raw);count+=1
   j=f-row['local_start']
   if j in [0,10,row['frames']//3,row['frames']//2,2*row['frames']//3,row['frames']-1]:(F/f'{row["id"]}-{f:03}.png').write_bytes(raw)
  p.stdin.close();assert p.wait()==0
 except BaseException:p.kill();p.wait();out.unlink(missing_ok=True);raise
 print('DONE',row['id'],count,round(time.monotonic()-start,1),flush=True)
temp.unlink(missing_ok=True);(O/'render-checks.json').write_text(json.dumps(dict(rendered=count,reused_shots=sorted(unchanged),elapsed_seconds=time.monotonic()-start),indent=2))
