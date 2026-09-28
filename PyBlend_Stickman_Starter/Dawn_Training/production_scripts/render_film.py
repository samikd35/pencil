from pathlib import Path
import bpy,json,time
OUT=Path(__file__).resolve().parents[2]/'artifacts/dawn_training'
s=bpy.data.scenes['DT_03_DAWN_TRAINING'];bpy.context.window.scene=s;s.frame_set(1)
se=s.sequence_editor_create()
if not se.strips.get('Dawn Training | original sound'):
 se.strips.new_sound('Dawn Training | original sound',str(OUT/'Dawn_Training_Sound.wav'),channel=1,frame_start=1)
s.render.use_sequencer=False
bpy.ops.file.pack_all()
s.render.filepath=str(OUT/'frames/frame_');s.frame_start=1;s.frame_end=720
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Dawn_Training.blend'))
# Blocking checkpoint preserves the real rig keys and shot cameras, with FX/titles disabled.
for n in ['DT_FX | energy, dust and impact','DT_Titles']:bpy.data.collections[n].hide_render=True
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'stages/05_blocking.blend'))
for n in ['DT_FX | energy, dust and impact','DT_Titles']:bpy.data.collections[n].hide_render=False
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Dawn_Training.blend'))
begin=time.time()
bpy.ops.render.render(animation=True)
s.frame_set(1)
(OUT/'render_report.json').write_text(json.dumps({'seconds':time.time()-begin,'frame_count':720,'fps':24,'resolution':[1920,1080],'renderer':s.render.engine},indent=2))
