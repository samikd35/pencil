"""Render the eight-second CP chase picture excerpt."""
import bpy, subprocess, time, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERSION=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'v001'
OUT=ROOT/('artifacts/chase-'+VERSION)
s=bpy.data.scenes['S002_CP_chase_'+VERSION]
if bpy.context.window:bpy.context.window.scene=s
assert s.frame_start==1 and s.frame_end==192 and s.render.fps==24
output=OUT/('chase-'+VERSION+'.mp4')
assert not output.exists(), 'Keep delivered versions'
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
temp=OUT/'working-frame.png'
cmd=['/opt/homebrew/bin/ffmpeg','-v','error','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(output)]
st=time.monotonic()
with (OUT/'encode.log').open('w') as log:
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
    try:
        for f in range(1,193):
            s.frame_set(f);s.render.filepath=str(temp);bpy.ops.render.render(write_still=True)
            p.stdin.write(temp.read_bytes())
            if f in [1,13,15,17,19,21,23,25,27,61,109,120,121,125,129,133,137,141,145,149,153,157,161,177,192]:
                (OUT/f'frame-{f:03}.png').write_bytes(temp.read_bytes())
            if f%24==0:print('PROOF_PROGRESS',f,192,round(time.monotonic()-st,1),flush=True)
        p.stdin.close();assert p.wait()==0
    except BaseException:
        p.kill();p.wait();raise
temp.unlink(missing_ok=True)
(OUT/'render-checks.json').write_text(json.dumps({'frames':192,'fps':24,'seconds':8,'width':1280,'height':720,'audio':'intentionally absent in picture-only proof','elapsed_seconds':time.monotonic()-st,'blender':bpy.app.version_string},indent=2)+'\n')
print('PROOF_COMPLETE',flush=True)
