"""Render only the 28-second representative action checkpoint, not the full film."""
from pathlib import Path
import bpy, subprocess, json, time, sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/staging-v003'
patch='--patch' in sys.argv
red_only='--red-only' in sys.argv
bpy.ops.wm.open_mainfile(filepath=str(OUT/('action-staging-v004.blend' if red_only else 'action-staging-v002.blend' if patch else 'action-staging-v001.blend')))
names=[('S02a · grounded kick',72),('S02b · resolved',120),('S08 · last hope',144),('S10 · any points with that',336)]
if patch:names=[names[0],names[2]]
if red_only:names=names[:1]
assert sum(frames for _,frames in names)==(72 if red_only else 216 if patch else 672)
start=time.monotonic();output=OUT/('action-red-v003.mp4' if red_only else 'action-patch-v002.mp4' if patch else 'action-picture-v001.mp4');assert not output.exists()
temp=OUT/'working-frame.png'
cmd=['/opt/homebrew/bin/ffmpeg','-hide_banner','-loglevel','error','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(output)]
done=0
with (OUT/('red-encode.log' if red_only else 'patch-encode.log' if patch else 'encode.log')).open('w') as log:
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
    try:
        for name,frames in names:
            s=bpy.data.scenes[name];bpy.context.window.scene=s;assert s.frame_end==frames
            s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.eevee.taa_render_samples=16;s.render.use_sequencer=False
            assert s.render.fps==24 and s.render.fps_base==1
            for f in range(1,frames+1):
                s.frame_set(f);s.render.filepath=str(temp);bpy.ops.render.render(write_still=True);p.stdin.write(temp.read_bytes());done+=1
                if f in (1,24,25,26,29,30,31,38,43,44,45,55,56,57,67,68,69,100,115,190,217,248,276,336):
                    (OUT/f'{"v003-" if red_only else "v002-" if patch else ""}{name.split(" ")[0]}-f{f:03}.png').write_bytes(temp.read_bytes())
                if done%48==0:print('ACTION_PROGRESS',done,672,round(time.monotonic()-start,1),flush=True)
        p.stdin.close();assert p.wait()==0,'Encoder failed'
    except BaseException:p.kill();p.wait();raise
temp.unlink(missing_ok=True)
(OUT/('red-render-checks.json' if red_only else 'patch-render-checks.json' if patch else 'render-checks.json')).write_text(json.dumps({'frames':done,'duration_seconds':done/24,'fps':24,'resolution':[1280,720],'elapsed_seconds':time.monotonic()-start,'native_images_packed':all(im.packed_file for im in bpy.data.images if im.source=='FILE'),'scene_names':[n for n,f in names]},indent=2)+'\n')
print('ACTION_RENDER_COMPLETE',flush=True)
