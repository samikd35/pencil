"""CP01 body pass: complete drawings, explicit contacts, independent load/travel/camera."""
import bpy, json, math, sys, ast
import numpy as np
from pathlib import Path
V=Path(__file__).resolve().parents[1]; A=V/'assets/chase-poses-v004'; O=V/'artifacts/animation-v002/CP01'
sys.path.insert(0,str(V.parents[3]/'pipeline'))
from checkpoints import require_checkpoint
for rev,stage in [('chase-v002','staging'),('opening-v002','sound'),('opening-v002','animatic')]:require_checkpoint(V,rev,stage)
NAME='S002_CP01_loaded_run_v001'; assert NAME not in bpy.data.scenes
previous=bpy.context.window.scene
with bpy.data.libraries.load(str(V/'artifacts/chase-v002/chase-v002.blend'),link=False) as (_,dst):dst.scenes=['S002_CP_chase_v002']
s=dst.scenes[0];s.name=NAME;bpy.context.window.scene=s
s.frame_start=1;s.frame_end=216;s.render.fps=24;s.eevee.taa_render_samples=16
O.mkdir(parents=True,exist_ok=True)
assert not (O/'CP01-v001.blend').exists()
# Reuse the existing source-sheet connected-component and material helpers only.
tree=ast.parse((V/'scripts/build_chase_v001.py').read_text())
helpers=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['components','sheet']],type_ignores=[])
exec(compile(helpers,'existing chase sheet helpers','exec'))
roots={name:next(o for o in s.objects if o.name.startswith('CP / '+name+' travel')) for name in ['Gabriel','Saliba','Gyokeres','Arteta','Pep']}
for name,root in roots.items():
 root.animation_data_clear();root['active']=0
 if name!='Pep':
  for child in list(root.children):bpy.data.objects.remove(child,do_unlink=True)
cam=s.camera;cam.animation_data_clear();cam.data.animation_data_clear();cam.data.ortho_scale=7.9
podium=next(o for o in s.objects if o.name.startswith('CP / first-place podium travel'))
podium.animation_data_clear()
for child in podium.children:child.animation_data_clear();child.hide_render=False;child.hide_viewport=False
metadata=json.loads((A/'registrations.json').read_text()); actors={};log=[]
speed=3.9;half=8;ground=.025
for name,offset,depth,phase in [('Gabriel',-2.10,.08,0),('Saliba',-.85,.03,4),('Gyokeres',.45,-.02,8),('Arteta',2.25,-.08,2)]:
 rec=metadata[name];alpha,boxes,mat,W,H=sheet(rec['file']);root=roots[name];root['active']=1
 root.id_properties_ui('pose_index').update(min=0,max=7,soft_min=0,soft_max=7)
 scale=rec['scale'];poses=[]
 for i,r in enumerate(rec['poses']):
  x0,y0,x1,y1,_=boxes[i];x0=max(0,x0-3);x1=min(W,x1+3);y0=max(0,y0-3);y1=min(H,y1+3)
  cx,cy=r['registration'];fx,fy=r['foot'];foot=((fx-cx)*scale,(cy-fy)*scale)
  nx,ny=24,40;verts=[];uvs=[];faces=[]
  for j in range(ny+1):
   py=y0+(y1-y0)*j/ny
   for k in range(nx+1):
    px=x0+(x1-x0)*k/nx;verts.append(((px-cx)*scale,0,(cy-py)*scale));uvs.append((px/W,1-py/H))
  for j in range(ny):
   for k in range(nx):
    a=j*(nx+1)+k;faces.append((a,a+nx+1,a+nx+2,a+1))
  mesh=bpy.data.meshes.new(NAME+name+str(i));mesh.from_pydata(verts,[],faces);mesh.materials.append(mat);uv=mesh.uv_layers.new()
  for poly in mesh.polygons:
   for lp in poly.loop_indices:uv.data[lp].uv=uvs[mesh.loops[lp].vertex_index]
  ob=bpy.data.objects.new(NAME+' / '+name+' pose '+str(i),mesh);s.collection.objects.link(ob);ob.parent=root;ob.shape_key_add(name='Basis');keys=[]
  for axis in [0,2]:
   key=ob.shape_key_add(name='Support '+str(axis));key.slider_min=-1;key.slider_max=1
   for basis,kp in zip(mesh.shape_keys.key_blocks['Basis'].data,key.data):
    kp.co=basis.co.copy();u=float(np.clip((foot[1]+.65-basis.co.z)/.5,0,1));kp.co[axis]+=u*u*(3-2*u)
   keys.append(key)
  for prop in ['hide_render','hide_viewport']:
   d=ob.driver_add(prop).driver;d.expression='pose != '+str(i);v=d.variables.new();v.name='pose';v.type='SINGLE_PROP';v.targets[0].id=root;v.targets[0].data_path='["pose_index"]'
  r.update(foot_local=list(foot),rect=[x0,y0,x1,y1]);poses.append((ob,keys))
 actors[name]=(root,poses)
 # Contacts are authored support phases, not inferred from the lowest pixel each frame.
 # ponytail: fixed-view whole drawings; a turn needs new drawings, not larger deformations.
 for f in range(1,217):
  tick=f-1;local=tick+phase;h,q=divmod(local,half);idx=(local//2)%8;flight=q>=6
  x=speed*tick/24+offset
  # The shared load stays nearly level while differently phased runners support it.
  load_z=.012*math.sin(tick*math.tau/32)
  z=rec['height']+load_z if name!='Arteta' else rec['height']+[0,-.012,-.028,-.016,.005,.028,.042,.025][q]
  plant=sum(speed*(h*half+j-phase)/24+offset+rec['poses'][((h*half+j)//2)%8]['foot_local'][0] for j in range(6))/6
  fx,fz=rec['poses'][idx]['foot_local'];dx=0 if flight else plant-x-fx
  dz=max(0,ground+.075-z-fz) if flight else ground-z-fz
  assert abs(dx)<.42 and abs(dz)<.22,(name,f,dx,dz)
  root.location=(x,depth,z);root.keyframe_insert(data_path='location',frame=f);root['pose_index']=idx;root.keyframe_insert(data_path='["pose_index"]',frame=f)
  for j,(ob,keys) in enumerate(poses):
   for key,value in zip(keys,[dx,dz]):key.value=value if j==idx else 0;key.keyframe_insert(data_path='value',frame=f)
  log.append(dict(frame=f,actor=name,pose=idx,contact=not flight,plant=plant,foot_world=[x+fx+dx,z+fz+dz],correction=[dx,dz],x=x,z=z))
for f in range(1,217):
 x=speed*(f-1)/24;bob=.012*math.sin((f-1)*math.tau/32)
 # Existing front's lower edge is 2.17. Palms contact its underside at 2.12.
 podium.location=(x,0,bob-.05);podium.keyframe_insert(data_path='location',frame=f)
 cam.location=(x+.05,-12,1.42);cam.keyframe_insert(data_path='location',frame=f)
for db in [cam,podium,*[r for r,_ in actors.values()],*[ob.data.shape_keys for _,poses in actors.values() for ob,_ in poses]]:
 if db.animation_data and db.animation_data.action:
  for layer in db.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for kp in fc.keyframe_points:kp.interpolation='CONSTANT' if fc.data_path=='["pose_index"]' else 'LINEAR'
# Evaluated selectors, active drawing count, support correction and camera tracking.
for f in range(1,217):
 s.frame_set(f);bpy.context.view_layer.update()
 for name,(root,poses) in actors.items():
  row=next(r for r in log if r['actor']==name and r['frame']==f)
  assert root['pose_index']==row['pose']
  assert sum(not ob.hide_render for ob,_ in poses)==1
  ob,keys=poses[row['pose']];fx,fz=metadata[name]['poses'][row['pose']]['foot_local']
  assert abs(root.location.x+fx+keys[0].value-row['foot_world'][0])<1e-5
  assert abs(root.location.z+fz+keys[1].value-row['foot_world'][1])<1e-5
  if row['contact']:assert abs(row['foot_world'][1]-ground)<1e-7
 assert abs(cam.location.x-speed*(f-1)/24-.05)<1e-5
s['scope']='CP01 9-second body pass; phone-to-road transition and final acting remain unfinished.'
s['motion_method']='Whole drawings; inspected sole/palm registrations; phased supports; separate load, root and camera paths.'
s.frame_set(1)
(O/'motion.json').write_text(json.dumps(log,indent=2));(O/'poses.json').write_text(json.dumps(metadata,indent=2))
(O/'checks.json').write_text(json.dumps(dict(frames=216,selectors='all match',contacts='216 frames checked for all four actors',max_correction=max(abs(x) for r in log for x in r['correction']),creative_acceptance=False),indent=2))
bpy.data.libraries.write(str(O/'CP01-v001.blend'),{s},fake_user=True,compress=True)
s.render.image_settings.file_format='PNG';s.render.filepath=str(O/'frame-001.png');bpy.ops.render.render(write_still=True)
bpy.context.window.scene=previous
result={'scene':NAME,'file':str(O/'CP01-v001.blend'),'frames':216,'prior_window_scene_restored':previous.name}
