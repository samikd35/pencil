"""Render the saved native scene to a streamed H.264 picture master."""
from pathlib import Path
import bpy, subprocess, json, time, sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v001'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'three-goals.blend'));s=bpy.context.scene
preview='--preview' in sys.argv
s.render.resolution_percentage=40 if preview else 100
s.eevee.taa_render_samples=16 if preview else 24
name='motion-preview' if preview else 'picture-master'
temp=OUT/(name+'-frame.png');started=time.monotonic()
cmd=['/opt/homebrew/bin/ffmpeg','-hide_banner','-loglevel','error','-y','-f','image2pipe','-vcodec','png','-framerate',str(s.render.fps),'-i','pipe:0','-an','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(OUT/(name+'.mp4'))]
with (OUT/(name+'-encode.log')).open('w') as log:
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
    try:
        for f in range(s.frame_start,s.frame_end+1):
            s.frame_set(f);s.render.filepath=str(temp);bpy.ops.render.render(write_still=True);p.stdin.write(temp.read_bytes())
            if f%48==0:print('RENDER_PROGRESS',f,s.frame_end,round(time.monotonic()-started,1),flush=True)
        p.stdin.close();assert p.wait()==0,'FFmpeg encoder failed'
    except BaseException:p.kill();p.wait();raise
temp.unlink(missing_ok=True)
(OUT/(name+'-checks.json')).write_text(json.dumps({'frames':s.frame_end-s.frame_start+1,'fps':s.render.fps,'width':int(s.render.resolution_x*s.render.resolution_percentage/100),'height':int(s.render.resolution_y*s.render.resolution_percentage/100),'render_seconds':time.monotonic()-started,'output':name+'.mp4'},indent=2)+'\n')
print('RENDER_COMPLETE',name,flush=True)
