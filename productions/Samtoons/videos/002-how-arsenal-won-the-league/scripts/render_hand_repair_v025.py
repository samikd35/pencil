"""Stream the complete remaining 720p review batch from its saved native scenes."""
import bpy,json,subprocess,time,sys
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/hand-repair-v025';rows=json.loads((O/'edit.json').read_text());FF='/opt/homebrew/bin/ffmpeg';FP='/opt/homebrew/bin/ffprobe';start=time.monotonic();count=0
selection=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
for r in rows:
 if selection and r['id'] not in selection:continue
 out=O/'clips'/(r['id']+'.mp4')
 if out.exists():
  p=subprocess.run([FP,'-v','error','-show_entries','stream=nb_frames','-of','json',str(out)],capture_output=True,text=True)
  try:valid=p.returncode==0 and int(json.loads(p.stdout)['streams'][0]['nb_frames'])==r['frames']
  except (ValueError,KeyError,IndexError):valid=False
  if valid:continue
  out.unlink()
 s=bpy.data.scenes[r['scene']];bpy.context.window.scene=s;s.render.use_sequencer=False;s.render.use_border=False;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.eevee.taa_render_samples=24
 tmp=O/('working-'+r['id']+'.png');p=subprocess.Popen([FF,'-v','error','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
 try:
  for f in range(1,r['frames']+1):
   s.frame_set(f);s.render.filepath=str(tmp);bpy.ops.render.render(write_still=True);raw=tmp.read_bytes();p.stdin.write(raw);count+=1
   if f in [1,r['frames']//3,2*r['frames']//3,r['frames']] or (r['id'] in ['FR03_cross','FR03_bonk','FR03_goal','CP05','VH01'] and f%3==0):(O/'review-frames'/f'{r["id"]}-{f:04}.png').write_bytes(raw)
  p.stdin.close();assert p.wait()==0
 except BaseException:p.kill();p.wait();out.unlink(missing_ok=True);raise
 tmp.unlink(missing_ok=True);print('DONE',r['id'],r['frames'],round(time.monotonic()-start,1),flush=True)
assert sum(r['frames'] for r in rows)==3642
(O/('render-checks-'+('-'.join(selection) or 'all')+'.json')).write_text(json.dumps(dict(rendered=count,elapsed_seconds=time.monotonic()-start,selection=selection,review_resolution=[1280,720],fps=24),indent=2))
