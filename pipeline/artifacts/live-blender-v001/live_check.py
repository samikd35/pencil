"""Run in an interactive Blender instance: disposable live-authoring check."""
from pathlib import Path
import json
import math
import bpy

OUT = Path(__file__).resolve().parent
target = OUT / 'preview-v001.blend'
assert not bpy.app.background, 'This check must run in the visible instance'
assert bpy.context.window is not None, 'No interactive window'
assert not bpy.data.is_dirty, 'Preserve unsaved work before running this check'
assert not target.exists(), 'Keep the previous check; use a new output directory'
assert 'Pencil Live Check' not in bpy.data.scenes, 'Check scene already exists'

previous_scene = bpy.context.scene.name
scene = bpy.data.scenes.new('Pencil Live Check')
bpy.context.window.scene = scene
scene.frame_start, scene.frame_end = 1, 48
scene.render.fps = 24
scene.render.engine = 'BLENDER_WORKBENCH'
scene.render.resolution_x, scene.render.resolution_y = 960, 540
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.display.shading.color_type = 'OBJECT'
scene.display.shading.light = 'STUDIO'
scene.display.shading.background_type = 'WORLD'
scene.world = bpy.data.worlds.new('Live Check World')
scene.world.color = (0.025, 0.035, 0.055)

bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, -0.65))
board = bpy.context.object
board.name = 'Live Check Board'
board.scale = (4.7, 2.6, 1)
board.color = (0.045, 0.12, 0.16, 1)

for words, position, size in [
    ('LIVE BLENDER', (-4.0, 1.45, 0), 0.48),
    ('Disposable connection test / editable motion', (-4.0, 0.98, 0), 0.19),
    ('VISIBLE AUTHORING + TIMELINE PREVIEW', (-4.0, -1.85, 0), 0.20),
]:
    data = bpy.data.curves.new(words, 'FONT')
    data.body, data.size = words, size
    obj = bpy.data.objects.new(words, data)
    scene.collection.objects.link(obj)
    obj.location = position
    obj.color = (0.9, 0.95, 1, 1)

bpy.ops.mesh.primitive_cube_add(size=0.9, location=(-2.4, -0.35, 0))
actor = bpy.context.object
actor.name = 'Live Check Actor'
actor.color = (1.0, 0.49, 0.12, 1)
bevel = actor.modifiers.new('Soft edges', 'BEVEL')
bevel.width, bevel.segments = 0.12, 4
for frame, x, angle in [(1, -2.4, 0), (25, 2.4, math.pi), (49, -2.4, math.tau)]:
    actor.location.x = x
    actor.rotation_euler.z = angle
    actor.keyframe_insert(data_path='location', frame=frame)
    actor.keyframe_insert(data_path='rotation_euler', frame=frame)

camera = bpy.data.cameras.new('Live Check Camera')
scene.camera = bpy.data.objects.new('Live Check Camera', camera)
scene.collection.objects.link(scene.camera)
scene.camera.location = (0, 0, 12)
camera.type, camera.ortho_scale = 'ORTHO', 10
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces.active.region_3d.view_perspective = 'CAMERA'
        area.spaces.active.shading.color_type = 'OBJECT'
        area.spaces.active.overlay.show_overlays = False
        area.tag_redraw()

positions = []
for frame in (1, 25):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    positions.append(round(actor.matrix_world.translation.x, 3))
assert positions == [-2.4, 2.4], positions
assert actor.animation_data.action is not None
assert previous_scene in bpy.data.scenes, 'Original scene must remain available'
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(target))
result = {'background': bpy.app.background, 'scene': scene.name,
          'path': str(target), 'original_scene_preserved': previous_scene,
          'frame_positions': positions, 'objects': len(scene.objects),
          'blender': bpy.app.version_string}
(OUT / 'live-check.json').write_text(json.dumps(result, indent=2) + '\n')
