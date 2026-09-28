"""Rerender only twelve changed phone-lift frames, retaining the other 228 frames."""
import bpy,subprocess
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/defence-v022';FF='/opt/homebrew/bin/ffmpeg'
s=bpy.data.scenes['S002_defence_v022_City'];bpy.context.window.scene=s;s.frame_set(1)
for old in list(bpy.data.scenes):
 if old.name=='Scene':bpy.data.scenes.remove(old)
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(O/'batch02-v022.blend'),compress=True)
s.render.use_sequencer=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.resolution_percentage=100
p=subprocess.Popen([FF,'-v','error','-y','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(O/'phone-lift.mp4')],stdin=subprocess.PIPE)
for f in range(1,13):
 s.frame_set(f);s.render.filepath=str(O/'phone-frame.png');bpy.ops.render.render(write_still=True);p.stdin.write((O/'phone-frame.png').read_bytes())
p.stdin.close();assert p.wait()==0
subprocess.run([FF,'-v','error','-y','-i',str(O/'phone-lift.mp4'),'-i',str(O/'clips/CD05_ping.mp4'),'-filter_complex','[1:v]trim=start_frame=12,setpts=PTS-STARTPTS[tail];[0:v][tail]concat=n=2:v=1:a=0[out]','-map','[out]','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p',str(O/'city-patched.mp4')],check=True)
(O/'city-patched.mp4').replace(O/'clips/CD05_ping.mp4');(O/'phone-frame.png').unlink();print('12 phone frames patched',flush=True)
