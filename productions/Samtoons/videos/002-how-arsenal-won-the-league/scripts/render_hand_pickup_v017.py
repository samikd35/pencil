import bpy,subprocess
from pathlib import Path
O=Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/002-how-arsenal-won-the-league/artifacts/batch02-v017');s=bpy.data.scenes['S002_B01_v016_unveiling'];bpy.context.window.scene=s;s.render.use_border=False;s.render.resolution_percentage=100;s.render.image_settings.color_mode='RGB';s.render.image_settings.file_format='PNG';s.render.use_sequencer=False;s.eevee.taa_render_samples=24
p=subprocess.Popen(['/opt/homebrew/bin/ffmpeg','-v','error','-f','image2pipe','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(O/'hand-pickup-final.mp4')],stdin=subprocess.PIPE)
for f in range(186,289):
 s.frame_set(f);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=f),key=lambda m:m.frame).camera;s.render.filepath=str(O/'hand-frame.png');bpy.ops.render.render(write_still=True);raw=(O/'hand-frame.png').read_bytes();p.stdin.write(raw)
 if f<=205:(O/'review-frames'/f'hand-final-{f:03}.png').write_bytes(raw)
p.stdin.close();assert p.wait()==0;(O/'hand-frame.png').unlink();print('PICKUP_DONE',flush=True)
