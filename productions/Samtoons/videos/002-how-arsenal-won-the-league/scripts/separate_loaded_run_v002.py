"""Increase Arteta's clearance after encoded frames exposed a shoe overlap."""
import bpy,json
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v002/CP01'
s=bpy.data.scenes['S002_CP01_loaded_run_v001'];s.name='S002_CP01_loaded_run_v002';bpy.context.window.scene=s
root=next(o for o in s.objects if o.name.startswith('CP / Arteta travel'))
for layer in root.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    if fc.data_path=='location' and fc.array_index==0:
     for p in fc.keyframe_points:p.co.y+=.35;p.handle_left.y+=.35;p.handle_right.y+=.35
rows=json.loads((O/'motion.json').read_text())
for r in rows:
 if r['actor']=='Arteta':r['x']+=.35;r['plant']+=.35;r['foot_world'][0]+=.35
(O/'motion-v002.json').write_text(json.dumps(rows,indent=2))
s.frame_set(216);p=O/'CP01-v002.blend';assert not p.exists();bpy.ops.wm.save_as_mainfile(filepath=str(p))
s.render.filepath=str(O/'v002-frame-216.png');bpy.ops.render.render(write_still=True)
