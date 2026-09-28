"""Render the eight-second native picture diagnostic; not a full-film render."""
from pathlib import Path
import bpy, subprocess, json, time

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/staging-v004'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'option-a-reaction-v002.blend'))
s=bpy.data.scenes['S02 / Option A'];bpy.context.window.scene=s
assert s.frame_end==192 and s.render.fps==24
assert all(im.packed_file for im in bpy.data.images if im.source=='FILE')
output=OUT/'option-a-reaction-v002.mp4';assert not output.exists()
temp=OUT/'working-frame.png';start=time.monotonic()
cmd=['/opt/homebrew/bin/ffmpeg','-hide_banner','-loglevel','error','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(output)]
with (OUT/'encode.log').open('w') as log:
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
    try:
        for frame in range(1,193):
            s.frame_set(frame);s.render.filepath=str(temp);bpy.ops.render.render(write_still=True);p.stdin.write(temp.read_bytes())
            if frame in (1,18,29,32,44,55,65,69,96,97,103,123,133,158,192):(OUT/f'frame-{frame:03}.png').write_bytes(temp.read_bytes())
            if frame%48==0:print('OPTION_A_PROGRESS',frame,192,flush=True)
        p.stdin.close();assert p.wait()==0,'Encoder failed'
    except BaseException:p.kill();p.wait();raise
temp.unlink(missing_ok=True)
(OUT/'render-checks.json').write_text(json.dumps({'frames':192,'seconds':8,'fps':24,'resolution':[s.render.resolution_x,s.render.resolution_y],'packed_images':True,'native_reopen':'passed','elapsed_seconds':time.monotonic()-start,'audio':'none; picture diagnostic'},indent=2)+'\n')
