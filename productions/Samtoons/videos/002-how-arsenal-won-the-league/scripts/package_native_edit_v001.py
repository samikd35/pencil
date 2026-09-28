"""Packaging only: add startup UI state to the scene authored in visible Blender."""
import bpy
from pathlib import Path
s=bpy.data.scenes['S002_full_animatic_v001']
bpy.context.window.scene=s
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':
   a.type='SEQUENCE_EDITOR'
   for space in a.spaces:
    if space.type=='SEQUENCE_EDITOR':space.view_type='PREVIEW'
s.frame_set(1)
p=Path(bpy.data.filepath).with_name('arsenal-animatic-v001.blend');assert not p.exists()
bpy.ops.wm.save_as_mainfile(filepath=str(p))
print('Packaged startup scene',s.name,'at',p)
