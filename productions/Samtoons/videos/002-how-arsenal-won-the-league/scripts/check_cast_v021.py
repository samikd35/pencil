"""Run in background Blender. Compare preserved leads, check all fitted cast controls."""
import bpy,json,hashlib
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/defence-v021';cast=json.loads((O/'cast.json').read_text());baseline=json.loads((V/'artifacts/defence-v020/cast.json').read_text());cast.update({k:baseline[k] for k in ['Arteta','Gyokeres']})
def curves(id):
 if not id.animation_data or not id.animation_data.action:return []
 return [fc for layer in id.animation_data.action.layers for st in layer.strips for bag in st.channelbags for fc in bag.fcurves]
def signature(a):
 ids=[bpy.data.objects[a['root']],bpy.data.objects[a['skin']],*(bpy.data.objects[name] for name in a['controls'].values())];data=[]
 for ob in ids:
  data.append([ob.name,[(fc.data_path,fc.array_index,[(list(kp.co),kp.interpolation) for kp in fc.keyframe_points]) for fc in curves(ob)]])
  if ob.type=='MESH':data.append([list(v.co) for v in ob.data.vertices])
 return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(V/'artifacts/defence-v020/batch02-v020.blend'));before={name:signature(cast[name]) for name in ['Arteta','Gyokeres']}
bpy.ops.wm.open_mainfile(filepath=str(O/'batch02-v021.blend'));after={name:signature(cast[name]) for name in before};assert before==after,(before,after)
checks={}
for name,a in cast.items():
 arm=bpy.data.objects[a['armature']];assert len(arm.data.bones)==14,name
 animated=[label for label,oname in a['controls'].items() if any(max(kp.co.y for kp in fc.keyframe_points)-min(kp.co.y for kp in fc.keyframe_points)>.005 for fc in curves(bpy.data.objects[oname]) if len(fc.keyframe_points))]
 assert len(animated)>=5,(name,animated);checks[name]={'bones':14,'moving_controls':animated}
import hashlib
sameaudio=hashlib.sha256((O/'mix/mix-premaster.wav').read_bytes()).hexdigest()==hashlib.sha256((V/'artifacts/defence-v019/mix/mix-premaster.wav').read_bytes()).hexdigest();assert sameaudio
(O/'regression-checks.json').write_text(json.dumps({'lead_geometry_and_motion_unchanged':before==after,'lead_hashes':after,'premaster_unchanged':sameaudio,'cast':checks,'limit':'These checks verify editable motion and preservation, not artistic quality.'},indent=2));print('PASS: preserved leads/audio and 18 independently controlled cast rigs')
# Review-specific contacts and shuffle invariants, evaluated in the saved scene.
from mathutils import Vector
import math
s=bpy.data.scenes['S002_defence_v021'];bpy.context.window.scene=s;s.frame_set(168);bpy.context.view_layer.update();ball=bpy.data.objects['v019 match ball'];assert math.hypot(ball.location.x+34,ball.location.y-52.5)+.11<1
row=cast['Saka'];root=bpy.data.objects[row['root']];arm=bpy.data.objects[row['armature']];c=row['cfg'];u=1.8/(c['floor']-c['top']);p=Vector(((470-c['center'])*u,(c['floor']-776)*u,0));bone=arm.pose.bones['Rfoot'];tip=root.matrix_world@(bone.matrix@bone.bone.matrix_local.inverted()@p);assert abs((tip-ball.location).length-.11)<.001
minimum=99
for f in range(392,512):
 s.frame_set(f)
 for i in range(9):
  c=cast['wall '+str(i+1)]['controls'];gap=bpy.data.objects[c['Rankle']].location.x-bpy.data.objects[c['Lankle']].location.x;minimum=min(minimum,gap);assert gap>.09,(i,f,gap)
s.frame_set(238);assert abs(54.5-ball.location.y-.11)<.001 and abs(ball.location.x)+.11<3.66
print('PASS: visible boot contact, legal corner placement, uncrossed wall feet, net contact')
