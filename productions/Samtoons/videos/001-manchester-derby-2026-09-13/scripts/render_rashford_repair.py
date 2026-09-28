"""Render the saved nine-second staging repair; --stills checks framing first."""
from pathlib import Path
import bpy, sys, subprocess, json
OUT=Path(__file__).resolve().parents[1]/'artifacts/repair-v001'
if '--out' in sys.argv:OUT=Path(sys.argv[sys.argv.index('--out')+1]).resolve()
s=bpy.data.scenes['REPAIR S03 / strike and scratch']
bpy.context.window.scene=s
s.render.use_sequencer=False
s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.eevee.taa_render_samples=8
assert s.render.fps==24 and s.frame_end==216
frames=[1,27,32,39,43,55,58,79,97,118,160,210] if '--stills' in sys.argv else range(1,217)
if '--frames' in sys.argv:frames=[int(f) for f in sys.argv[sys.argv.index('--frames')+1].split(',')]
folder=OUT/('stills' if '--stills' in sys.argv else 'frames');folder.mkdir(exist_ok=True)
enc=None
if '--stills' not in sys.argv:
    enc=subprocess.Popen(['/opt/homebrew/bin/ffmpeg','-v','error','-y','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'picture.mp4')],stdin=subprocess.PIPE)
try:
    for f in frames:
        s.frame_set(f);target=folder/f'{f:03}.png';s.render.filepath=str(target)
        bpy.ops.render.render(write_still=True)
        if enc:enc.stdin.write(target.read_bytes())
        (OUT/'render-progress.json').write_text(json.dumps({'frame':f,'total':216,'mode':'clip' if enc else 'stills'}))
    if enc:enc.stdin.close();assert enc.wait()==0
except BaseException:
    if enc:enc.kill();enc.wait()
    raise
