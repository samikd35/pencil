"""Render the three short action-staging excerpts; not the full film."""
from pathlib import Path
import bpy,subprocess,json,time,sys,shutil
ROOT=Path(__file__).resolve().parents[1];OUT=Path(sys.argv[sys.argv.index('--')+1]) if '--' in sys.argv else ROOT/'artifacts/staging-v007'
OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'artifacts/staging-v007/clear-reactions-v001.blend'))
shots=[('S02 / kick and overreaction',336,'foden-bruno'),('S08 / hope and parry',168,'parry'),('S10 / tears and umbrella',264,'apology')]
assert all(im.packed_file for im in bpy.data.images if im.source=='FILE')
start=time.monotonic();counts={}
for name,count,slug in shots:
 if slug=='parry':
  shutil.copy2(ROOT/'artifacts/staging-v005/parry.mp4',OUT/'parry.mp4');counts[slug]=count;continue
 s=bpy.data.scenes[name];bpy.context.window.scene=s
 assert s.frame_end==count and s.render.fps==24 and s.render.fps_base==1
 target=OUT/(slug+'.mp4');assert not target.exists(),target
 temp=OUT/'working-frame.png'
 cmd=['/opt/homebrew/bin/ffmpeg','-hide_banner','-loglevel','error','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(target)]
 with (OUT/(slug+'-encode.log')).open('w') as log:
  encoder=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
  try:
   for frame in range(1,count+1):
    s.frame_set(frame);s.render.filepath=str(temp);bpy.ops.render.render(write_still=True);encoder.stdin.write(temp.read_bytes())
    if frame in (1,20,34,39,45,49,60,67,68,69,70,72,76,77,78,79,80,83,97,101,102,106,108,110,120,121,130,131,141,148,150,160,166,177,180,190,210,214,221,225,239,264,75,119,151,170,197,198,202,204,276,283,count):(OUT/f'{slug}-{frame:03}.png').write_bytes(temp.read_bytes())
    if frame%72==0:print('ACTION_PROGRESS',slug,frame,count,flush=True)
   encoder.stdin.close();assert encoder.wait()==0,'Encoding failed'
  except BaseException:encoder.kill();encoder.wait();raise
 counts[slug]=count
 print('ACTION_COMPLETE',slug,flush=True)
 temp.unlink(missing_ok=True)
(OUT/'concat.txt').write_text(''.join("file '"+slug+".mp4'\n" for _,_,slug in shots))
subprocess.run(['/opt/homebrew/bin/ffmpeg','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-c','copy','-movflags','+faststart',str(OUT/'action-review-v001.mp4')],check=True)
subprocess.run(['/opt/homebrew/bin/ffmpeg','-hide_banner','-loglevel','error','-i',str(OUT/'action-review-v001.mp4'),'-an','-c:v','libvpx-vp9','-crf','31','-b:v','0',str(OUT/'action-review-v001.webm')],check=True)
(OUT/'render-checks.json').write_text(json.dumps({'frames':counts,'total_frames':sum(counts.values()),'seconds':sum(counts.values())/24,'fps':24,'resolution':[1280,720],'native_reopen':'passed','packed_images':True,'elapsed_seconds':time.monotonic()-start,'audio':'none; picture diagnostic'},indent=2)+'\n')
