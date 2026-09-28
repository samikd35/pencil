"""Stream native Blender frames to FFmpeg without keeping a gigabyte of PNGs."""
from pathlib import Path
import bpy
import subprocess
import time
import json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v001'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'alisson-winner.blend'))
scene=bpy.context.scene
preview='--preview' in __import__('sys').argv
patch='--patch' in __import__('sys').argv
scene.render.resolution_percentage=50 if preview else 100
scene.eevee.taa_render_samples=8 if preview else 16
start,end=(577,696) if patch else ((385,625) if preview else (1,960))
output=OUT/('net-correction.mp4' if patch else ('contact-preview.mp4' if preview else 'picture-master.mp4'))
temp=OUT/('frame-patch.png' if patch else ('frame-preview.png' if preview else 'frame-render.png'))
command=['/opt/homebrew/bin/ffmpeg','-hide_banner','-loglevel','error','-y','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(output)]
started=time.monotonic()
with (OUT/('encode-patch.log' if patch else ('encode-preview.log' if preview else 'encode.log'))).open('w') as log:
    process=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=log)
    try:
        for frame in range(start,end+1):
            scene.frame_set(frame);scene.render.filepath=str(temp);bpy.ops.render.render(write_still=True)
            process.stdin.write(temp.read_bytes())
            if frame%48==0:print('RENDER_PROGRESS',frame,end,round(time.monotonic()-started,1),flush=True)
        process.stdin.close()
        assert process.wait()==0,'FFmpeg failed: inspect encode log'
    except BaseException:
        process.kill();process.wait();raise
if temp.exists():temp.unlink()
(OUT/('render-patch.json' if patch else ('render-preview.json' if preview else 'render-checks.json'))).write_text(json.dumps({'first_frame':start,'last_frame':end,'fps':24,'rendered_frames':end-start+1,'render_seconds':time.monotonic()-started,'resolution_percentage':scene.render.resolution_percentage,'renderer':'Native Blender EEVEE, individually rendered continuous frames','output':output.name},indent=2)+'\n')
print('RENDER_FINISHED',output,flush=True)
