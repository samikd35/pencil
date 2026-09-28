"""Run inside the saved Blender revision. Scoped regressions, not artistic approval."""
import bpy,json,math
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/defence-v022';wall=bpy.data.scenes['S002_defence_v022_coach_reactions'];city=bpy.data.scenes['S002_defence_v022_City'];report={}
for s in [wall,city]:
 assert s.camera and s.render.fps==24
 for ob in s.objects:
  for co in ob.constraints:
   if hasattr(co,'target') and co.target:assert co.target.name in s.objects,(ob.name,co.target.name)
  if ob.type=='ARMATURE':
   for pb in ob.pose.bones:
    for co in pb.constraints:
     if hasattr(co,'target') and co.target:assert co.target.name in s.objects,(ob.name,co.target.name)
 report[s.name]=dict(frames=s.frame_end,objects=len(s.objects),armatures=sum(o.type=='ARMATURE' for o in s.objects),audio_strips=len(s.sequence_editor.strips),constraints_local=True)
assert report[wall.name]['armatures']==10 and report[city.name]['armatures']==1
for name in ['Mourinho','Simeone','Conte']:
 ob=next(o for o in wall.objects if o.type=='MESH' and o.name.startswith(name+' coherent bust'));assert set(['Nod','Blink','Brow','Write','Lift']).issubset(ob.data.shape_keys.key_blocks.keys());assert ob.data.shape_keys.animation_data and ob.data.shape_keys.animation_data.action
 assert next(n.image for n in ob.data.materials[0].node_tree.nodes if n.type=='TEX_IMAGE').packed_file
bpy.context.window.scene=city
phone=next(o for o in city.objects if '/ v019 Arteta phone' in o.name)
for f in range(1,241):
 city.frame_set(f);assert all(abs(v-1)<1e-6 for v in phone.scale)
report['phone_size_constant']=True;report['coach_complete_drawings_packed']=True;report['local_constraints_checked']=True
assert (Path.home()/'Models/qwen-voice/model/model.safetensors').exists() and (Path.home()/'Models/qwen-voice/base-model/model.safetensors').exists();report['voice_models_retained']=True
(O/'native-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
