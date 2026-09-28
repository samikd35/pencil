"""Stream the eight-second S01 review only. Never a full-film render entry point."""
from pathlib import Path
import bpy, subprocess, json, time
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/staging-v001'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'s01-morning-pep-v002.blend'))
s=bpy.data.scenes['Samtoons S01 — Morning Pep'];bpy.context.window.scene=s
assert s.frame_start==1 and s.frame_end<=192, 'This checkpoint renderer is limited to S01.'
s.render.resolution_percentage=50;s.eevee.taa_render_samples=16
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.use_sequencer=False
output=OUT/'s01-picture-v002.mp4';assert not output.exists(),'Preserve previous review output'
temp=OUT/'working-frame.png';start=time.monotonic();fps=s.render.fps/s.render.fps_base
cmd=['/opt/homebrew/bin/ffmpeg','-hide_banner','-loglevel','error','-f','image2pipe','-vcodec','png','-framerate',str(fps),'-i','pipe:0','-an','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(output)]
with (OUT/'encode-v002.log').open('w') as log:
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
    try:
        for f in range(1,193):
            s.frame_set(f);s.render.filepath=str(temp);bpy.ops.render.render(write_still=True);p.stdin.write(temp.read_bytes())
            if f in (16,70,110,114,125,135): (OUT/f'v002-frame-{f:03}.png').write_bytes(temp.read_bytes())
            if f%24==0:print('S01_PROGRESS',f,192,round(time.monotonic()-start,1),flush=True)
        p.stdin.close();assert p.wait()==0,'Encoder failed'
    except BaseException:p.kill();p.wait();raise
temp.unlink(missing_ok=True)
(OUT/'render-checks-v002.json').write_text(json.dumps({'frames':192,'fps':fps,'width':960,'height':540,'duration_seconds':8,'elapsed_seconds':time.monotonic()-start,'renderer':bpy.app.version_string,'kind':'S01 staging candidate; not combined film animatic'},indent=2)+'\n')
print('S01_RENDER_COMPLETE',flush=True)
