"""New run/jump performance on the actual delivered Bruno asset; no replacement artwork."""
import bpy, math, json, hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/002-how-arsenal-won-the-league')
OUT=ROOT/'artifacts/bruno-action-v006';NAME='S002_Bruno_action_v006'
source=ROOT.parent/'001-manchester-derby-2026-09-13/artifacts/delivery-v001/samtoons-final.blend'
assert not OUT.exists() and NAME not in bpy.data.scenes
with bpy.data.libraries.load(str(source),link=False) as (available,loaded):loaded.scenes=['S02 / kick and overreaction']
s=loaded.scenes[0];s.name=NAME;bpy.context.window.scene=s;s.frame_set(1)
root=next(o for o in s.objects if o.name.startswith('A Drama Bruno / ROOT'))
family={root,*root.children_recursive}
keep={o for o in family if o.name.startswith('A Drama Bruno /')}
keep.update(o for o in s.objects if o.name.startswith('A /') or o.name.startswith('S02 / touchline'))
for o in list(s.objects):
 if o not in keep:
  for col in list(o.users_collection):col.objects.unlink(o)
 else:
  if o.animation_data:o.animation_data.action=None
# Clearing actions above preserves drivers, constraints and the complete original artwork.
arm=next(o for o in family if o.type=='ARMATURE')
body=next(o for o in family if o.type=='MESH' and any(m.type=='ARMATURE' for m in o.modifiers))
controls={};rest={}
for pb in arm.pose.bones:
 a=next(c.target for c in pb.constraints if c.type=='COPY_LOCATION')
 b=next(c.target for c in pb.constraints if c.type=='STRETCH_TO')
 for target,position in [(a,pb.bone.head_local),(b,pb.bone.tail_local)]:
  key=target.name.split('CTRL ')[1].split('.')[0];controls[key]=target;rest[key]=position.copy()
assert len(controls)==19
# Record exact surface/weights/UVs to demonstrate identity preservation.
def signature():
 rows={'vertices':[[*v.co,[(g.group,g.weight) for g in v.groups]] for v in body.data.vertices],  'bones':[(b.name,list(b.head_local),list(b.tail_local)) for b in arm.data.bones]}
 return hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()
before=signature()
import numpy as np,bmesh
texture=next(n.image for mat in body.data.materials for n in mat.node_tree.nodes if n.type=='TEX_IMAGE')
rgba=np.empty(len(texture.pixels),dtype=np.float32);texture.pixels.foreach_get(rgba)
alpha=rgba.reshape(texture.size[1],texture.size[0],4)[:,:,3]
bm=bmesh.new();bm.from_mesh(body.data);uvlayer=bm.loops.layers.uv.active
remove=[]
for face in bm.faces:
 samples=[loop[uvlayer].uv for loop in face.loops]
 samples.append(sum(samples,Vector((0,0)))/len(samples))
 visible=False
 for uv in samples:
  ix=max(0,min(texture.size[0]-1,round(uv.x*(texture.size[0]-1))))
  iy=max(0,min(texture.size[1]-1,round(uv.y*(texture.size[1]-1))))
  if alpha[max(0,iy-2):iy+3,max(0,ix-2):ix+3].max()>.93:visible=True;break
 if not visible:remove.append(face)
bmesh.ops.delete(bm,geom=remove,context='FACES_ONLY');bm.to_mesh(body.data);bm.free()
# No body redraw, replacement head, material or weighting change.

# Keep original body view and proportions; authored travel follows its local horizontal axis.
rotation=root.rotation_euler.to_matrix();unit=root.scale.x;base=root.location.copy();base.x=0;base.y=0
s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=32;s.render.fps=24;s.render.fps_base=1;s.frame_start=1;s.frame_end=192
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.use_sequencer=False
s.view_settings.view_transform='Standard';s.view_settings.look='None'
cd=bpy.data.cameras.new(NAME+' camera');cd.type='ORTHO';cd.ortho_scale=5.6
cam=bpy.data.objects.new(cd.name,cd);s.collection.objects.link(cam);cam.location=(0,-10,1.35);cam.rotation_euler=(math.pi/2,0,0);s.camera=cam
# Source ground shadow follows travel; original source drawing stays unchanged.
shadows=[o for o in s.objects if 'ground shadow' in o.name]
for ob in shadows:
 for col in list(ob.users_collection):col.objects.unlink(ob)
shadow_src=next(o for o in bpy.data.objects if o.name.startswith('A Drama Bruno / ground shadow'))
shadow=shadow_src.copy();shadow.data=shadow_src.data.copy();shadow.animation_data_clear();s.collection.objects.link(shadow)
center=sum((v.co for v in shadow.data.vertices),Vector())/len(shadow.data.vertices)
for v in shadow.data.vertices:v.co-=Vector((center.x,center.y,0))
def rot(v,a):return Vector((math.cos(a)*v.x-math.sin(a)*v.y,math.sin(a)*v.x+math.cos(a)*v.y,v.z))
def ease(t):return t*t*(3-2*t)
def knee(h,a,l1,l2,sign=1):
 d=a-h;length=d.length
 assert abs(l1-l2)<length<l1+l2+.0001,(f,side,length,l1,l2)
 axis=d/length;along=(l1*l1-l2*l2+length*length)/(2*length)
 return h+axis*along+Vector((-axis.y,axis.x,0))*sign*math.sqrt(max(0,l1*l1-along*along))
def runfoot(f,side):
 offset=0 if side=='R' else 10;q=(f-13+offset)/20;cycle=math.floor(q);phase=q-cycle
 # Position in the actor's travelling local coordinate system. Stance is world-fixed.
 rootx=-5.2+(f-13)*.095
 plant=-5.2+cycle*1.9+.25-offset*.095+rest[side+'ankle'].x
 if phase<.42:return Vector((plant-rootx,rest[side+'ankle'].y,0)),0,True
 t=(phase-.42)/.58
 return Vector((plant+1.9*ease(t)-rootx,rest[side+'ankle'].y+.70*math.sin(math.pi*t),0)),.20*math.sin(math.pi*t),False
records=[]
for f in range(1,193):
 if f<13:x=-5.2;dy=0;lean=0
 elif f<=72:x=-5.2+(f-13)*.095;dy=-.19+.065*math.cos((f-13)*math.tau/10);lean=-.18
 elif f<=90:
  u=(f-72)/18;x=.405+.445*ease(u)
  dy=(-.19-.23*ease((f-72)/14)) if f<=86 else (-.42+.37*ease((f-86)/4))
  lean=-.18-.04*math.sin(math.pi*u)
 elif f<=110:
  u=(f-90)/20;x=.85+2.95*u;dy=-.05*(1-u)+1.25*4*u*(1-u);lean=-.22+.14*u
 elif f<=134:
  u=(f-110)/24;x=3.8;impact=min(1,(f-110)/4);release=max(0,(f-114)/20);dy=-.38*ease(impact)*(1-ease(release));lean=-.08-.10*ease(impact)*(1-ease(release))
 else:x=3.8;dy=0;lean=0
 p={k:rest['hip']+Vector((0,dy,0))+rot(v-rest['hip'],lean) for k,v in rest.items()}
 # Torso leans independently; pelvis anchors retain their width and leg reach.
 for side in ['L','R']:p[side+'hip']=rest[side+'hip']+Vector((0,dy,0))
 contacts={}
 for side in ['L','R']:
  r=rest;ank=side+'ankle';toe=side+'toe';h=side+'hip';k=side+'knee'
  roll=0;stance=False
  if f<13:a=r[ank].copy();stance=True
  elif f<=72:a,roll,stance=runfoot(f,side)
  elif f<=90:
   a0,roll0,_=runfoot(72,side);t=ease(min(1,(f-72)/7));a=(a0+Vector((.405,0,0))).lerp(r[ank]+Vector((.85,0,0)),t)-Vector((x,0,0));roll=roll0*(1-t);stance=f>=79
  elif f<=110:
   u=(f-90)/20;lift=math.sin(math.pi*u);a=r[ank]+Vector((.24*lift,dy+.05*(1-u)+(.35 if side=='L' else .20)*lift,0));stance=f==110
  else:a=r[ank].copy();stance=True
  p[ank]=a;p[toe]=a+rot(r[toe]-r[ank],roll)
  p[k]=knee(p[h],a,(r[k]-r[h]).length,(r[ank]-r[k]).length,1)
  shoulder,elbow,wrist,finger=[side+v for v in ['shoulder','elbow','wrist','finger']]
  if f<13:
   upper=fore=0
  elif f<=72:
   phase=(f-13+(0 if side=='R' else 10))*math.tau/20
   # Opposed upper arms; bent arms pump in opposing phases, keeping hands clear of the torso.
   swing=.55*math.cos(phase)
   upper=-math.pi/2+swing-math.atan2((r[elbow]-r[shoulder]).y,(r[elbow]-r[shoulder]).x)
   fore=-math.pi/2+swing+1.8-math.atan2((r[wrist]-r[elbow]).y,(r[wrist]-r[elbow]).x)
  elif f<=90:
   u=ease((f-72)/18);phase=(72-13+(0 if side=='R' else 10))*math.tau/20
   swing=.55*math.cos(phase)
   upper=(-math.pi/2+swing-math.atan2((r[elbow]-r[shoulder]).y,(r[elbow]-r[shoulder]).x))*(1-u)
   fore=(-math.pi/2+swing+1.8-math.atan2((r[wrist]-r[elbow]).y,(r[wrist]-r[elbow]).x))*(1-u)
   drive=ease(max(0,(f-86)/4))
   upper+=(.65 if side=='R' else -.65)*drive
   fore+=(.75 if side=='R' else -.75)*drive
  elif f<=110:
   u=(f-90)/20;lift=1-u
   upper=(.65 if side=='R' else -.65)*lift
   fore=(.75 if side=='R' else -.75)*lift
  else:
   u=max(0,1-(f-110)/24);upper=0;fore=(-.45 if side=='R' else .45)*u
  p[elbow]=p[shoulder]+rot(r[elbow]-r[shoulder],upper+lean)
  p[wrist]=p[elbow]+rot(r[wrist]-r[elbow],fore+lean)
  p[finger]=p[wrist]+rot(r[finger]-r[wrist],fore+lean)
  # Tiny drawing-plane separation resolves front/back overlaps without changing the artwork.
  for key in [h,k,ank,toe]:p[key].z=(-.025 if side=='L' else .025)
  for key,z in [(shoulder,.02),(elbow,.04),(wrist,.07),(finger,.08)]:p[key].z=z if side=='R' else -z
  contacts[side]={'stance':stance,'toe_local':list(p[toe]),'ankle_local':list(a)}
 root.location=base+rotation@Vector((x*unit,0,0));root.keyframe_insert(data_path='location',frame=f)
 for key,ob in controls.items():ob.location=p[key];ob.keyframe_insert(data_path='location',frame=f)
 shadow.location=(root.location.x,root.location.y,.002);shadow.keyframe_insert(data_path='location',frame=f)
 records.append({'frame':f,'travel':x,'body_offset':dy,'contacts':contacts})
s.frame_set(13);bpy.context.view_layer.update()
start_pose={key:ob.location.copy() for key,ob in controls.items()}
for f in range(1,13):
 t=ease((f-1)/12)
 for key,ob in controls.items():
  ob.location=rest[key].lerp(start_pose[key],t);ob.keyframe_insert(data_path='location',frame=f)
# Preserve native facial geometry; use its existing expression controls for effort and release.
mouth=next(o for o in keep if '/ mouth control' in o.name)
for f,value in [(1,.05),(13,.15),(72,.15),(89,.35),(96,.65),(116,.35),(138,.08),(192,.05)]:
 mouth['open']=value;mouth.keyframe_insert(data_path='["open"]',frame=f)
for ob in s.objects:
 ad=ob.animation_data
 if ad and ad.action:
  for l in ad.action.layers:
   for st in l.strips:
    for b in st.channelbags:
     for fc in b.fcurves:
      for key in fc.keyframe_points:key.interpolation='LINEAR'
assert signature()==before,'Artwork/binding changed'
s['Scope']='Actual episode 001 Bruno, original painted body/kit/shoes/face/binding; invisible grid faces removed. New eight-second run, jump, landing. Silent motion review; no Gyokeres adaptation.'
s['Events']=json.dumps({'run_start':13,'gather':73,'takeoff':90,'apex':101,'landing':110,'recovery':134})
s.frame_set(101);bpy.context.view_layer.update()
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_overlays=False
OUT.mkdir(parents=True)
(OUT/'motion.json').write_text(json.dumps(records)+'\n')
(OUT/'provenance.json').write_text(json.dumps({'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'surface_binding_sha256_before':before,'surface_binding_sha256_after':signature(),'vertices':len(body.data.vertices),'controls':len(controls),'scene':NAME,'artwork_changed':False,'invisible_faces_removed':len(remove)},indent=2)+'\n')
bpy.data.libraries.write(str(OUT/'bruno-action-v006.blend'),{s},fake_user=True)
result={'file':str(OUT/'bruno-action-v006.blend'),'scene':NAME,'artwork_unchanged':signature()==before}
