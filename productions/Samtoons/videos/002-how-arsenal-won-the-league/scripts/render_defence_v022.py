"""Streaming 720p batch review, not a final-quality delivery render."""
import bpy,json,subprocess,time,sys
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/defence-v022';rows=json.loads((O/'edit.json').read_text());F=O/'review-frames';F.mkdir(exist_ok=True);clips=O/'clips';clips.mkdir(exist_ok=True);FF='/opt/homebrew/bin/ffmpeg';temp=O/'working.png';start=time.monotonic();count=0
# Convert the library snapshot into an ordinary openable native mainfile.
s=bpy.data.scenes['S002_defence_v022_coach_reactions'];bpy.context.window.scene=s;s.frame_set(1)
for oldscene in list(bpy.data.scenes):
 if oldscene.name=='Scene':bpy.data.scenes.remove(oldscene)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(O/'batch02-v022.blend'),compress=True)
for row in rows:
 if '--proof' in sys.argv and row['id']!='CD01_cross':continue
 out=clips/(row['id']+'.mp4')
 if out.exists():
  check=subprocess.run(['/opt/homebrew/bin/ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','json',str(out)],capture_output=True,text=True)
  try:valid=check.returncode==0 and int(json.loads(check.stdout)['streams'][0]['nb_frames'])==row['frames']
  except (KeyError,ValueError,IndexError):valid=False
  if valid:continue
  out.unlink()
 s=bpy.data.scenes[row['scene']];bpy.context.window.scene=s;s.render.use_sequencer=False;s.render.resolution_percentage=100;s.render.use_border=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.eevee.taa_render_samples=24
 p=subprocess.Popen([FF,'-v','error','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
 try:
  for f in range(row['local_start'],row['local_start']+row['frames']):
   s.frame_set(f);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=f),key=lambda m:m.frame).camera;s.render.filepath=str(temp);bpy.ops.render.render(write_still=True);raw=temp.read_bytes();p.stdin.write(raw);count+=1;j=f-row['local_start']
   if j in [0,row['frames']//3,2*row['frames']//3,row['frames']-1] or (row['id']=='CD04' and 178<=f<=282 and f%3==0) or (row['id']=='CD05_ping' and f in [12,18,24,48,72,96,120,144,168,192,216,239]) or f in [151,154,157,160,164,167,168,169,170,214,215,216,217,218,219,230,231,232,237,238,239,430,438,446,454,992,996,1000,1005]:(F/f'{row["id"]}-{f:04}.png').write_bytes(raw)
  p.stdin.close();assert p.wait()==0
 except BaseException:p.kill();p.wait();out.unlink(missing_ok=True);raise
 print('DONE',row['id'],count,round(time.monotonic()-start,1),flush=True)
temp.unlink(missing_ok=True);(O/'render-checks.json').write_text(json.dumps(dict(rendered=count,elapsed_seconds=time.monotonic()-start,frames=sum(r['frames'] for r in rows)),indent=2))
assert sum(r['frames'] for r in rows)==1323
