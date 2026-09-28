"""Scoped live Blender save/reopen/render check on a copied existing source.

Set PHASE_A_STEP to 'prepare' or 'verify' in execute_blender_code. This is
operational evidence, not new animation or a creative review.
"""
import json
from pathlib import Path
import bpy

OUT = Path(__file__).resolve().parent
SCENE = 'S002_B01_v016_unveiling'
assert not bpy.app.background
window = bpy.context.window_manager.windows[0]
scene = bpy.data.scenes[SCENE]
window.scene = scene
scene.frame_set(220)
scene.camera = max((m for m in scene.timeline_markers if m.camera and m.frame <= 220),
                   key=lambda m: m.frame).camera

if PHASE_A_STEP == 'prepare':
    assert Path(bpy.data.filepath) == OUT / 'source-copy.blend'
    assert not (OUT / 'corrected-copy.blend').exists()
    camera = scene.camera.data
    assert camera.type == 'ORTHO'
    original = camera.ortho_scale
    # Probe an existing, visible native control; never alter the delivered file.
    camera.ortho_scale = original * 1.01
    assert camera.keyframe_insert(data_path='ortho_scale', frame=220)
    expected = camera.ortho_scale
    scene['phase_a_source_owner'] = 'This saved copy owns the probe key; render must not rebuild it.'
    scene.render.resolution_x, scene.render.resolution_y = 384, 216
    scene.render.resolution_percentage = 100
    scene.render.use_sequencer = False
    scene.render.use_border = False
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.eevee.taa_render_samples = 8
    report = {'blender': bpy.app.version_string, 'source': str(OUT / 'source-copy.blend'),
              'scene': SCENE, 'frame': 220, 'camera': scene.camera.name,
              'property': 'camera.data.ortho_scale', 'original': original, 'expected': expected,
              'keyframe_insert': True, 'interactive_window': True,
              'scope': 'Copied existing source; saved-file-owned native camera correction and render route only.'}
    (OUT / 'expected.json').write_text(json.dumps(report, indent=2) + '\n')
    assert bpy.ops.wm.save_as_mainfile(filepath=str(OUT / 'corrected-copy.blend')) == {'FINISHED'}
    scene.render.filepath = str(OUT / 'before-reopen.png')
elif PHASE_A_STEP == 'verify':
    assert Path(bpy.data.filepath) == OUT / 'corrected-copy.blend'
    report = json.loads((OUT / 'expected.json').read_text())
    assert abs(scene.camera.data.ortho_scale - report['expected']) < 1e-6
    action = scene.camera.data.animation_data.action
    assert action and len(action.slots) > 0
    report.update(reopened_value=scene.camera.data.ortho_scale, action_slots=len(action.slots),
                  saved_correction_preserved=True, no_authoring_registry_loaded_by_check=True)
    scene.render.filepath = str(OUT / 'after-reopen.png')
else:
    raise ValueError(PHASE_A_STEP)

image = Path(scene.render.filepath)
assert not image.exists(), 'Keep completed check outputs'
assert bpy.ops.render.render(write_still=True, scene=SCENE) == {'FINISHED'}
assert image.is_file() and image.stat().st_size > 0
report.update(render_finished=True, preview=str(image))
(OUT / (PHASE_A_STEP + '.json')).write_text(json.dumps(report, indent=2) + '\n')
result = report
