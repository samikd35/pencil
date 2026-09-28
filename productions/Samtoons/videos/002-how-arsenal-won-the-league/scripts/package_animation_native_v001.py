"""Saved-scene fallback: replace only CP03 Pep strip; current interactive file untouched."""
import bpy,json
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v001';s=bpy.data.scenes['S002_full_animatic_v002'];s.name='S002_animation_progress_v001';bpy.context.window.scene=s
q=next(q for q in s.sequence_editor.strips if q.name=='Picture / CP03_pep');assert q.frame_final_duration==96
q.filepath=str(O/'CP03_pep/CP03_pep-v002-silent.mp4');s['scope']='Only CP03_pep body motion replaced; all other shots storyboard. No final-quality completion claim.'
s.frame_set(int(q.frame_final_start));p=O/'arsenal-progress-v001.blend';assert not p.exists();bpy.ops.wm.save_as_mainfile(filepath=str(p));print('Saved progress native timeline with one replaced strip')
