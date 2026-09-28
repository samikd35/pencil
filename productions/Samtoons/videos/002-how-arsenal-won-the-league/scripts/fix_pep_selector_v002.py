"""Saved-scene fallback after live connector disconnected. Preserve v001."""
import bpy,json
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v001/CP03_pep';s=bpy.data.scenes['S002_CP03_pep_body_v001'];bpy.context.window.scene=s
root=next(o for o in s.objects if 'Pep travel' in o.name)
rows=json.loads((O/'motion.json').read_text());s.frame_set(28);before=root['pose_index'];assert before==3
root.id_properties_ui('pose_index').update(min=0,max=5,soft_min=0,soft_max=5)
for r in rows:
 s.frame_set(r['frame']);bpy.context.view_layer.update();assert root['pose_index']==r['pose'],(r['frame'],root['pose_index'],r['pose'])
s['selector_revision']='v002: inherited maximum3 prevented poses4/5; explicit range0..5, all96frames checked against authored exposure.'
s.frame_set(1)
p=O/'CP03_pep-v002.blend';assert not p.exists();bpy.ops.wm.save_as_mainfile(filepath=str(p))
(O/'selector-check.json').write_text(json.dumps(dict(old_frame28=before,expected_frame28=5,corrected_all_frames=96,root_cause='Inherited ID-property max3 clamps pose Fcurve values4and5',live_authoring=False,reason='Connector disconnected; current user window shows unrelated Untitled scene, not overwritten'),indent=2))
print('PASS: old frame28 clamped3; revised all96frames match intended pose')
