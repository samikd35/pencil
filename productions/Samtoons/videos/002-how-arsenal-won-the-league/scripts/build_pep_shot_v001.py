"""Visible Blender: CP03_pep body-animation pass, using complete coherent drawings."""
import bpy,json,math,sys,hashlib
import numpy as np
from pathlib import Path
V=Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/002-how-arsenal-won-the-league');O=V/'artifacts/animation-v001/CP03_pep';O.mkdir(parents=True,exist_ok=True);A=V/'assets/chase-poses-v003'
sys.path.insert(0,str(V.parents[3]/'pipeline'));from checkpoints import require_checkpoint
require_checkpoint(V,'chase-v002','staging');require_checkpoint(V,'opening-v002','sound');require_checkpoint(V,'opening-v002','animatic')
NAME='S002_CP03_pep_body_v001'
if NAME in bpy.data.scenes:
 s=bpy.data.scenes[NAME]
else:
 with bpy.data.libraries.load(str(V/'artifacts/chase-v002/chase-v002.blend'),link=False) as (_,dst):dst.scenes=['S002_CP_chase_v002']
 s=dst.scenes[0];s.name=NAME
bpy.context.window.scene=s;s.frame_start=1;s.frame_end=96;s.render.fps=24;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.eevee.taa_render_samples=16
for obname in [ob.name for ob in s.objects]:
 ob=bpy.data.objects.get(obname)
 if ob is None:continue
 if ' travel' in ob.name:
  ob.animation_data_clear()
  if 'Pep travel' in ob.name:
   for child in list(ob.children):bpy.data.objects.remove(child,do_unlink=True)
   root=ob;root['active']=1
  else:ob['active']=0
 if 'podium' in ob.name or 'first label' in ob.name:
  ob.animation_data_clear();ob.hide_render=True;ob.hide_viewport=True
s.camera.animation_data_clear();s.camera.data.animation_data_clear();s.camera.data.ortho_scale=5.0
im=bpy.data.images.load(str(A/'pep-guided-initial.png'));im.pack();W,H=im.size
m=bpy.data.materials.new(NAME+' complete artwork');m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links;t=n.new('ShaderNodeTexImage');t.image=im;t.interpolation='Linear';e=n.new('ShaderNodeEmission');l.new(t.outputs['Color'],e.inputs[0]);tr=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');alpha=n.new('ShaderNodeMath');alpha.operation='GREATER_THAN';alpha.inputs[1].default_value=.95;l.new(t.outputs['Alpha'],alpha.inputs[0]);l.new(alpha.outputs[0],mix.inputs[0]);l.new(tr.outputs[0],mix.inputs[1]);l.new(e.outputs[0],mix.inputs[2]);out=n.new('ShaderNodeOutputMaterial');l.new(mix.outputs[0],out.inputs[0])
# Explicit anatomical registrations and chosen support sole samples, inspected in source.
# Columns4 are excluded: generated toe-off repeated a down pose and was not adopted.
records=[
 dict(cell=0,neck=(224,151),foot=(283,470),rect=(86,35,358,480),phase='near contact'),
 dict(cell=1,neck=(600,153),foot=(611,470),rect=(502,35,680,480),phase='near down'),
 dict(cell=2,neck=(972,151),foot=(944,470),rect=(894,35,1033,480),phase='near support / far passing'),
 dict(cell=4,neck=(229,650),foot=(288,967),rect=(88,533,371,978),phase='far contact'),
 dict(cell=5,neck=(601,648),foot=(609,966),rect=(500,530,681,975),phase='far down'),
 dict(cell=6,neck=(974,646),foot=(935,963),rect=(894,530,1030,972),phase='far support / near passing')]
root.id_properties_ui('pose_index').update(min=0,max=len(records)-1,soft_min=0,soft_max=len(records)-1)
scale=1.94/437;poses=[]
for i,r in enumerate(records):
 x0,y0,x1,y1=r['rect'];cx,cy=r['neck'];fx,fy=r['foot'];nx,ny=24,40;verts=[];uvs=[];faces=[]
 for j in range(ny+1):
  py=y0+(y1-y0)*j/ny
  for k in range(nx+1):
   px=x0+(x1-x0)*k/nx;verts.append(((px-cx)*scale,0,(cy-py)*scale));uvs.append((px/W,1-py/H))
 for j in range(ny):
  for k in range(nx):
   a=j*(nx+1)+k;faces.append((a,a+nx+1,a+nx+2,a+1))
 me=bpy.data.meshes.new(NAME+' pose '+str(i));me.from_pydata(verts,[],faces);me.materials.append(m);uv=me.uv_layers.new()
 for poly in me.polygons:
  for lp in poly.loop_indices:uv.data[lp].uv=uvs[me.loops[lp].vertex_index]
 ob=bpy.data.objects.new(NAME+' pose '+str(i),me);s.collection.objects.link(ob);ob.parent=root;ob.shape_key_add(name='Basis');keys=[]
 for axis in [0,2]:
  sk=ob.shape_key_add(name='Support '+str(axis));sk.slider_min=-1;sk.slider_max=1
  for basis,kp in zip(ob.data.shape_keys.key_blocks['Basis'].data,sk.data):
   kp.co=basis.co.copy();u=np.clip(((cy-fy)*scale+.65-basis.co.z)/.50,0,1);kp.co[axis]+=float(u*u*(3-2*u))
  keys.append(sk)
 for prop in ['hide_render','hide_viewport']:
  d=ob.driver_add(prop).driver;d.expression='pose != '+str(i);a=d.variables.new();a.name='pose';a.type='SINGLE_PROP';a.targets[0].id=root;a.targets[0].data_path='["pose_index"]'
 r['foot_local']=[(fx-cx)*scale,(cy-fy)*scale];poses.append((ob,keys))
speed=1.14;half=14;step=speed*half/24;log=[]
for f in range(1,97):
 tick=f-1;h=tick//half;q=tick%half;part=0 if q<4 else 1 if q<8 else 2;idx=(h%2)*3+part;r=records[idx];x=speed*tick/24
 # Intentional modest neck-height rhythm: absorb, then recover before next contact.
 anchors=[(0,1.440),(4,1.415),(8,1.450),(14,1.440)]
 for (a,z0),(b,z1) in zip(anchors,anchors[1:]):
  if a<=q<=b:
   u=(q-a)/(b-a);z=z0+(z1-z0)*u*u*(3-2*u);break
 plant=h*step+.265;fx,fz=r['foot_local'];dx=plant-x-fx;dz=.025-z-fz
 assert abs(dx)<.32 and abs(dz)<.09,(f,dx,dz)
 root.location=(x,-.1,z);root.keyframe_insert(data_path='location',frame=f);root['pose_index']=idx;root.keyframe_insert(data_path='["pose_index"]',frame=f)
 for j,(ob,keys) in enumerate(poses):
  for sk,value in zip(keys,[dx,dz]):sk.value=value if j==idx else 0;sk.keyframe_insert(data_path='value',frame=f)
 s.camera.location=(x+.15,-12,1.25);s.camera.keyframe_insert(data_path='location',frame=f)
 log.append(dict(frame=f,pose=idx,phase=r['phase'],x=x,z=z,contact_x=plant,contact_z=.025,correction=[dx,dz]))
for db in [root,s.camera,*[o.data.shape_keys for o,_ in poses]]:
 if db.animation_data and db.animation_data.action:
  for layer in db.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for kp in fc.keyframe_points:kp.interpolation='CONSTANT' if fc.data_path=='["pose_index"]' else 'LINEAR'
s['scope']='CP03_pep body-motion candidate at approved shot duration. Six selected drawings, no mouth animation yet; inspect before adoption.'
s['source_status']='Candidate only: normal-speed quality unresolved; no automated phase or gait quality acceptance.'
s.frame_set(9);bpy.context.view_layer.update()
(O/'poses.json').write_text(json.dumps(records,indent=2));(O/'motion.json').write_text(json.dumps(log,indent=2));bpy.data.libraries.write(str(O/'CP03_pep-library.blend'),{s},fake_user=True,compress=True)
s.render.image_settings.file_format='PNG';s.render.filepath=str(O/'frame-009.png');bpy.ops.render.render(write_still=True)
result={'scene':NAME,'frames':96,'file':str(O/'CP03_pep-library.blend'),'max_support_correction':max(abs(r['correction'][0]) for r in log),'status':'candidate; unrendered full motion'}
