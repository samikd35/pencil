"""Retain editable full timeline and link the batch's native shot scenes."""
import bpy,json,os
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v004'
s=bpy.data.scenes['S002_animation_progress_v003'];s.name='S002_animation_progress_v004';bpy.context.window.scene=s
edit=json.loads((O/'edit.json').read_text());rows={r['id']:r for r in edit}
for q in s.sequence_editor.strips:
 if q.name.startswith('Picture / '):q.filepath=rows[q.name[len('Picture / '):]]['clip']
with bpy.data.libraries.load(str(O/'acting-batch-v004.blend'),link=True) as (src,dst):dst.scenes=[name for name in src.scenes if name.startswith('S002_fullmotion_')]
pictures=[q for q in s.sequence_editor.strips if q.name.startswith('Picture / ')]
assert len(pictures)==56 and sum(int(q.frame_final_duration) for q in pictures)==5954
assert all(os.path.exists(bpy.path.abspath(q.filepath)) for q in pictures)
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(O/'arsenal-progress-v004.blend'))
(O/'native-checks.json').write_text(json.dumps(dict(scene=s.name,picture_strips=56,frames=5954,native_shot_scenes=len(dst.scenes),dependencies_present=True),indent=2))
