"""Retain the accepted timeline and substitute only the corrected CP01 picture."""
import bpy,json,os
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v003'
s=bpy.data.scenes['S002_animation_progress_v002'];s.name='S002_animation_progress_v003';bpy.context.window.scene=s
q=next(q for q in s.sequence_editor.strips if q.name=='Picture / CP01');assert q.frame_final_duration==216
q.filepath=str(V/'artifacts/animation-v002/CP01/CP01-v002-silent.mp4')
pictures=[q for q in s.sequence_editor.strips if q.name.startswith('Picture / ')]
assert len(pictures)==56 and sum(int(q.frame_final_duration) for q in pictures)==5954
assert all(os.path.exists(bpy.path.abspath(q.filepath)) for q in pictures)
assert next(q.filepath for q in pictures if q.name=='Picture / CP03_pep').endswith('CP03_pep-v002-silent.mp4')
s.frame_set(2369);target=O/'arsenal-progress-v003.blend';assert not target.exists();bpy.ops.wm.save_as_mainfile(filepath=str(target))
(O/'native-checks.json').write_text(json.dumps(dict(scene=s.name,picture_strips=56,frames=5954,all_picture_dependencies_present=True,accepted_Pep_retained=True),indent=2))
