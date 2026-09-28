"""Second visible edit batch, preserving the first saved revision."""
from pathlib import Path
import bpy

out = Path(__file__).resolve().parent
assert Path(bpy.data.filepath) == out / 'preview-v001.blend'
assert bpy.context.scene.name == 'Pencil Live Check'
assert not (out / 'preview-v002.blend').exists()
actor = bpy.context.scene.objects['Live Check Actor']
actor.color = (1.0, 0.22, 0.12, 1)
bpy.context.scene.objects['Disposable connection test / editable motion'].data.body = 'Live update received / editable motion'
bpy.context.scene.frame_set(25)
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces.active.region_3d.view_camera_zoom = 15
        area.tag_redraw()
bpy.ops.wm.save_as_mainfile(filepath=str(out / 'preview-v002.blend'))
assert abs(actor.location.x - 2.4) < 0.001
result = {'saved': bpy.data.filepath, 'frame': bpy.context.scene.frame_current,
          'actor_x': actor.location.x, 'color': list(actor.color)}
