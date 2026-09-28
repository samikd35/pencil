"""Embed the delivered soundtrack in the editable held-pose Blender timeline."""
import json
from pathlib import Path
import bpy

OUT=Path(__file__).resolve().parents[1]/'artifacts/animatic-v001'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'just-one-thing.blend'))
scene=bpy.context.scene
scene.sequence_editor_clear()
editor=scene.sequence_editor_create()
strip=editor.strips.new_sound('Original score and Foley — mastered review mix',str(OUT/'review-mix.wav'),channel=1,frame_start=1)
strip.sound.pack()
strip.sound.filepath='//review-mix.wav'
scene.render.use_sequencer=False
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'just-one-thing.blend'))
# Reopen the actual delivery rather than only checking transient state.
bpy.ops.wm.open_mainfile(filepath=str(OUT/'just-one-thing.blend'))
scene=bpy.context.scene
strip=next(s for s in scene.sequence_editor.strips if s.type=='SOUND')
assert strip.sound.packed_file is not None and scene.frame_end==4320
story=json.loads((OUT/'story.json').read_text())
for p in story['panels']:
    scene.frame_set(p['frame']+p['frames']//2)
    assert abs(scene.camera.data.ortho_scale-p['cam'][2])<1e-4
    assert abs(bpy.data.objects['CTRL_Body'].location.x-p['x'])<1e-4
(OUT/'project-checks.json').write_text(json.dumps({'status':'passed','timeline_frames':4320,
    'panel_states_checked':len(story['panels']),'packed_audio_bytes':strip.sound.packed_file.size,
    'scope':'Saved project reopened, embedded audio present, camera and character position verified at each panel midpoint.'},indent=2)+'\n')
print('Editable project reopened and verified with packed audio.')
