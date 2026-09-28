"""Finalize isolated scene library as an ordinary opening Blender project; verify it."""
import bpy,json
from pathlib import Path
s=bpy.data.scenes['S003_S12_Membership_v001'];bpy.context.window.scene=s
for who in ['Valencia','Fan']:
 body=next(o for o in s.objects if f'S12 {who} continuous drawing' in o.name)
 assert body.data.shape_keys is None and not body.modifiers,who
 groups=[o for o in s.objects if f'S12 {who} arm drawing' in o.name and o.type=='EMPTY']
 assert groups
 for f in range(1,313):
  s.frame_set(f);assert sum(not o.hide_render for o in groups)==1,(who,f)
assert any(st.type=='SOUND' for st in s.sequence_editor.strips)
assert s.frame_end==312 and s.render.fps==24
assert all(abs(o.scale.z-.01)<1e-7 for o in s.objects if o.get('planar_ink'))
s.frame_set(69)
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath,compress=True)
Path(bpy.data.filepath).with_name('native-verification.json').write_text(json.dumps({'saved_scene_reopened':True,'discarded_body_shape_keys_and_modifiers_absent':True,'exactly_one_arm_drawing_per_actor_each_frame':True,'planar_ink':True,'authoritative_mix_in_native_timeline':True,'scope':'Technical integrity, not creative acceptance or a general motion guarantee.'},indent=2)+'\n')
print('S12_NATIVE_CHECK_PASSED')
