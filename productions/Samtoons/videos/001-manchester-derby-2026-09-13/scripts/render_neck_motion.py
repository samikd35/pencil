"""Stream the eight-second S01 review only. Never a full-film render entry point."""
from pathlib import Path
import bpy, subprocess, json, time
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/staging-v002'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'s01-neck-motion-v003.blend'))
s=bpy.data.scenes['Samtoons S01 — Morning Pep'];bpy.context.window.scene=s
assert s.frame_start==1 and s.frame_end<=192, 'This checkpoint renderer is limited to S01.'
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.eevee.taa_render_samples=16
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.use_sequencer=False
output=OUT/'s01-neck-picture-v003.mp4';assert not output.exists(),'Preserve previous review output'
temp=OUT/'working-frame.png';start=time.monotonic();fps=s.render.fps/s.render.fps_base
cmd=['/opt/homebrew/bin/ffmpeg','-hide_banner','-loglevel','error','-f','image2pipe','-vcodec','png','-framerate',str(fps),'-i','pipe:0','-an','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(output)]
with (OUT/'encode-v003.log').open('w') as log:
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
    try:
        for f in range(1,193):
            s.frame_set(f);s.render.filepath=str(temp);bpy.ops.render.render(write_still=True);p.stdin.write(temp.read_bytes())
            if f in (16,43,47,52,59,62,66,91,99,103,107,110,114,119,125,135,149,152,192): (OUT/f'v003-frame-{f:03}.png').write_bytes(temp.read_bytes())
            if f%24==0:print('S01_PROGRESS',f,192,round(time.monotonic()-start,1),flush=True)
        p.stdin.close();assert p.wait()==0,'Encoder failed'
    except BaseException:p.kill();p.wait();raise
temp.unlink(missing_ok=True)
(OUT/'render-checks-v003.json').write_text(json.dumps({'frames':192,'fps':fps,'width':1280,'height':720,'duration_seconds':8,'elapsed_seconds':time.monotonic()-start,'renderer':bpy.app.version_string,'kind':'Revised neck/motion proof from S01; sound B preserved'},indent=2)+'\n')
print('S01_RENDER_COMPLETE',flush=True)
