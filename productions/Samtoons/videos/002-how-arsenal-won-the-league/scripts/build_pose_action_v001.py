"""Complete authored pose exposures, contact anchors and a single flight trajectory."""
import bpy, math, json, hashlib
import numpy as np
from pathlib import Path
R=Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/002-how-arsenal-won-the-league')
A=R/'assets/bruno-action-poses-v001';O=R/'artifacts/pose-action-v001';NAME='S002_whole_pose_action_v001'
assert not O.exists() and NAME not in bpy.data.scenes
source=R.parent/'001-manchester-derby-2026-09-13/artifacts/delivery-v001/samtoons-final.blend'
with bpy.data.libraries.load(str(source),link=False) as (a,l):l.scenes=['S02 / kick and overreaction']
s=l.scenes[0];s.name=NAME;bpy.context.window.scene=s
for ob in list(s.objects):
 if not (ob.name.startswith('A /') or ob.name.startswith('S02 / touchline')):
  for col in list(ob.users_collection):col.objects.unlink(ob)
 elif ob.animation_data:ob.animation_data.action=None
s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=32
s.render.fps=24;s.frame_start=1;s.frame_end=192;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.use_sequencer=False
s.view_settings.view_transform='Standard';s.view_settings.look='None'
cd=bpy.data.cameras.new(NAME+' camera');cd.type='ORTHO';cd.ortho_scale=5.6
cam=bpy.data.objects.new(cd.name,cd);s.collection.objects.link(cam);cam.rotation_euler=(math.pi/2,0,0);cam.location=(0,-10,1.35);s.camera=cam
actor=bpy.data.objects.new('Bruno / whole-body pose and travel',None);s.collection.objects.link(actor)
actor['Method']='Coherent pose substitutions on twos; grounded supports; ballistic visual-mass proxy. No claim of joint rig or exact anatomical COM.'
scale=1.8/482
# UV bounds include boots/hand margins outside the nominal equal cells.
rects={'run':[(28,0,414,521),(433,0,768,523),(785,0,1150,523),(1148,0,1536,523),(20,522,416,1024),(432,525,769,1024),(780,523,1150,1024),(1146,521,1536,1024)],
'jump':[(70,0,325,530),(412,90,735,530),(782,0,1154,540),(1163,0,1536,510),(40,538,381,900),(442,539,758,1005),(846,592,1177,1024),(1234,520,1536,1024)]}
# Contact regions identify the actual lowest opaque sole/toe in each drawing.
foot_regions={'run':[(292,390,470,521),(539,639,480,523),(806,880,470,523),None,(300,408,955,1024),(540,648,960,1024),(809,891,948,1024),None],
'jump':[(82,305,476,527),(499,679,481,525),(790,851,483,539),None,None,(587,744,934,1000),(870,1064,946,1024),(1260,1478,948,1024)]}
poses={};metadata={}
for sheet in ['run','jump']:
 im=bpy.data.images.load(str(A/(sheet+'-sheet.png')));im.pack()
 W,H=im.size;pixels=np.empty(W*H*4,dtype=np.float32);im.pixels.foreach_get(pixels);alpha=pixels.reshape(H,W,4)[::-1,:,3]
 mat=bpy.data.materials.new('Bruno / '+sheet+' complete drawings');mat.use_nodes=True;nodes=mat.node_tree.nodes;nodes.clear();lk=mat.node_tree.links
 tex=nodes.new('ShaderNodeTexImage');tex.image=im;tex.interpolation='Linear'
 em=nodes.new('ShaderNodeEmission');lk.new(tex.outputs['Color'],em.inputs['Color'])
 transparent=nodes.new('ShaderNodeBsdfTransparent');mix=nodes.new('ShaderNodeMixShader');threshold=nodes.new('ShaderNodeMath');threshold.operation='GREATER_THAN';threshold.inputs[1].default_value=.95
 lk.new(tex.outputs['Alpha'],threshold.inputs[0]);lk.new(threshold.outputs[0],mix.inputs[0]);lk.new(transparent.outputs[0],mix.inputs[1]);lk.new(em.outputs[0],mix.inputs[2]);out=nodes.new('ShaderNodeOutputMaterial');lk.new(mix.outputs[0],out.inputs['Surface'])
 for i,(x0,y0,x1,y1) in enumerate(rects[sheet]):
  yy,xx=np.where(alpha[y0:y1,x0:x1]>.95);cx=float(xx.mean()+x0);cy=float(yy.mean()+y0)
  mesh=bpy.data.meshes.new(sheet+str(i));mesh.from_pydata([((x-cx)*scale,0,(cy-y)*scale) for x,y in [(x0,y1),(x1,y1),(x1,y0),(x0,y0)]],[],[(0,1,2,3)]);uv=mesh.uv_layers.new()
  for loop,(x,y) in zip(mesh.polygons[0].loop_indices,[(x0,y1),(x1,y1),(x1,y0),(x0,y0)]):uv.data[loop].uv=(x/W,1-y/H)
  ob=bpy.data.objects.new('Bruno / '+sheet+' pose '+str(i+1),mesh);s.collection.objects.link(ob);mesh.materials.append(mat);ob.parent=actor
  contact=None;region=foot_regions[sheet][i]
  if region:
   xa,xb,ya,yb=region;ys,xs=np.where(alpha[ya:yb,xa:xb]>.95);bottom=int(ys.max()+ya);near=ys+ya>=bottom-2;fx=float((xs[near]+xa).mean());contact=[(fx-cx)*scale,(cy-bottom)*scale]
  key=sheet+str(i);poses[key]=ob;metadata[key]={'rect':[x0,y0,x1,y1],'mass_pixel':[cx,cy],'foot':contact}
# Native diagnostic controls (outside the entertainment picture).
actor['pose_index']=0;actor['Contact semantics']='A fixed point in world space during an exposed support pose; pose changes carry the whole body together.'
root_rows=[]
def put(frame,key,x,z,phase,contact=None):
 actor.location=(x,-.02,z);actor.keyframe_insert(data_path='location',frame=frame)
 for name,ob in poses.items():
  ob.hide_render=name!=key;ob.hide_viewport=name!=key
  ob.keyframe_insert(data_path='hide_render',frame=frame);ob.keyframe_insert(data_path='hide_viewport',frame=frame)
 cam.location.x=x;cam.keyframe_insert(data_path='location',frame=frame)
 root_rows.append({'frame':frame,'pose':key,'x':x,'z':z,'phase':phase,'contact_world':contact})
def grounded(frame,key,plant,phase):
 fx,fz=metadata[key]['foot'];put(frame,key,plant-fx,-fz,phase,[plant,0])
# Ready and body-loaded start.
for f in range(1,9):grounded(f,'jump0',0,'ready')
for f in range(9,13):grounded(f,'jump7',0,'prepare_run')
# Each half-stride is built from contact/down/push/flight poses.
step=1.70
for f in range(13,109):
 t=f-13;half=t//8;q=(t%8)//2;i=(half%2)*4+q;plant=half*step
 if q<3:grounded(f,'run'+str(i),plant,['contact','down','push'][q])
 else:
  last=metadata['run'+str((half%2)*4+2)];nxt=metadata['run'+str(((half+1)%2)*4)]
  x0=plant-last['foot'][0];x1=(half+1)*step-nxt['foot'][0]
  u=(t%8-4)/4;x=x0+(x1-x0)*u
  z0=-last['foot'][1];z1=-nxt['foot'][1];duration=4/24
  z=z0+(z1-z0)*u+.5*9.81*duration*duration*u*(1-u)
  put(f,'run'+str(i),x,z,'run_flight')
# Plant and gather into a purposeful forward jump.
plant=12*step
for f in range(109,113):grounded(f,'run0',plant,'gather_contact')
for f in range(113,117):grounded(f,'jump7',plant,'gather')
for f in range(117,121):grounded(f,'jump1',plant,'load')
for f in range(121,123):grounded(f,'jump2',plant,'extension')
launch_x=plant-metadata['jump2']['foot'][0];launch_z=-metadata['jump2']['foot'][1]
T=16/24;vx=2.4;g=9.81
land_z=-metadata['jump5']['foot'][1];vy=(land_z-launch_z+.5*g*T*T)/T
land_x=launch_x+vx*T;landing_plant=land_x+metadata['jump5']['foot'][0]
for f in range(123,139):
 t=(f-122)/24;key='jump3' if f<127 else ('jump4' if f<133 else 'jump5')
 put(f,key,launch_x+vx*t,launch_z+vy*t-.5*g*t*t,'jump_flight')
for f in range(139,141):grounded(f,'jump5',landing_plant,'landing_contact')
for f in range(141,145):grounded(f,'jump6',landing_plant,'absorb')
for f in range(145,153):grounded(f,'jump7',landing_plant,'recover')
for f in range(153,193):grounded(f,'jump0',landing_plant,'settled')
# The audience movie contains no diagnostic labels or explanatory text.
for ob in [actor,cam,*poses.values()]:
 ad=ob.animation_data
 if ad and ad.action:
  for layer in ad.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for kp in fc.keyframe_points:kp.interpolation='LINEAR' if fc.data_path=='location' else 'CONSTANT'
s['Scope']='Eight-second silent whole-body pose motion review; new coherent pose drawings derived from accepted Bruno; pending creative review.'
s['Review status']='Pending internal visual review, not approved'
s.frame_set(29)
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_overlays=False
O.mkdir(parents=True)
(O/'poses.json').write_text(json.dumps(metadata,indent=2)+'\n');(O/'motion.json').write_text(json.dumps(root_rows,indent=2)+'\n')
(O/'provenance.json').write_text(json.dumps({'source_blend':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'construction':'complete matching pose substitutions; no pasted head or generic replacement body','drawing_scale':scale,'run_step_distance':step,'run_half_stride_frames':8,'jump':{'seconds':T,'gravity':g,'launch_vy':vy,'vx':vx},'images':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [A/'run-sheet.png',A/'jump-sheet.png']}},indent=2)+'\n')
bpy.data.libraries.write(str(O/'pose-action-v001.blend'),{s},fake_user=True)
result={'scene':s.name,'file':str(O/'pose-action-v001.blend'),'drawings':len(poses),'frames':192}
