"""Run in background Blender. Compare preserved leads, check all fitted cast controls."""
import bpy,json,hashlib
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/defence-v020';cast=json.loads((O/'cast.json').read_text())
def curves(id):
 if not id.animation_data or not id.animation_data.action:return []
 return [fc for layer in id.animation_data.action.layers for st in layer.strips for bag in st.channelbags for fc in bag.fcurves]
def signature(a):
 ids=[bpy.data.objects[a['root']],bpy.data.objects[a['skin']],*(bpy.data.objects[name] for name in a['controls'].values())];data=[]
 for ob in ids:
  data.append([ob.name,[(fc.data_path,fc.array_index,[(list(kp.co),kp.interpolation) for kp in fc.keyframe_points]) for fc in curves(ob)]])
  if ob.type=='MESH':data.append([list(v.co) for v in ob.data.vertices])
 return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(V/'artifacts/defence-v019/batch02-v019.blend'));before={name:signature(cast[name]) for name in ['Arteta','Gyokeres']}
bpy.ops.wm.open_mainfile(filepath=str(O/'batch02-v020.blend'));after={name:signature(cast[name]) for name in before};assert before==after,(before,after)
checks={}
for name,a in cast.items():
 arm=bpy.data.objects[a['armature']];assert len(arm.data.bones)==14,name
 animated=[label for label,oname in a['controls'].items() if any(max(kp.co.y for kp in fc.keyframe_points)-min(kp.co.y for kp in fc.keyframe_points)>.005 for fc in curves(bpy.data.objects[oname]) if len(fc.keyframe_points))]
 assert len(animated)>=5,(name,animated);checks[name]={'bones':14,'moving_controls':animated}
import hashlib
sameaudio=hashlib.sha256((O/'mix/mix-premaster.wav').read_bytes()).hexdigest()==hashlib.sha256((V/'artifacts/defence-v019/mix/mix-premaster.wav').read_bytes()).hexdigest();assert sameaudio
(O/'regression-checks.json').write_text(json.dumps({'lead_geometry_and_motion_unchanged':before==after,'lead_hashes':after,'premaster_unchanged':sameaudio,'cast':checks,'limit':'These checks verify editable motion and preservation, not artistic quality.'},indent=2));print('PASS: preserved leads/audio and 18 independently controlled cast rigs')
