"""Keep approved pose drawings; separate registered body travel and camera from contact."""
import bpy,json,math
from pathlib import Path
R=Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/002-how-arsenal-won-the-league');src=R/'artifacts/pose-action-v002';out=R/'artifacts/pose-action-v003';name='S002_whole_pose_action_v003'
assert not out.exists() and name not in bpy.data.scenes
with bpy.data.libraries.load(str(src/'pose-action-v002.blend'),link=False) as (a,l):l.scenes=['S002_whole_pose_action_v002']
s=l.scenes[0];s.name=name;bpy.context.window.scene=s
actor=next(o for o in s.objects if o.name.startswith('Bruno / whole-body pose and travel'))
rows=json.loads((src/'motion.json').read_text());meta=json.loads((src/'poses.json').read_text());scale=1.8/482
# Neck-base registration, in source-sheet pixels, inspected on the complete drawings.
neck=dict(zip(['run'+str(i) for i in range(8)]+['jump'+str(i) for i in range(8)],[(273,165),(650,168),(1032,153),(1393,135),(272,674),(650,674),(1030,672),(1425,665),(200,165),(653,263),(971,169),(1380,161),(220,680),(610,693),(1000,750),(1380,665)]))
for key,m in meta.items():m['neck']=[(neck[key][0]-m['mass_pixel'][0])*scale,(m['mass_pixel'][1]-neck[key][1])*scale]
# Translate the action together to meet the ready pose without a backward snap.
for row in rows:
 if row['frame']>=13:
  row['x']+=.5
  if row['contact_world']:row['contact_world'][0]+=.5
# Low-frequency travel anchors, independent of drawing switches. Running speed unchanged.
anchors=[(1,.253),(8,.253),(13,-.28),(109,20.12),(117,20.797),(122,20.952),(138,22.499),(145,22.748),(153,22.786),(192,22.786)]
anchors=[(f,x+(.5 if f>=13 else 0)) for f,x in anchors]
# Monotone cubic Hermite segments; zero derivative at an authored turn/hold.
slopes=[(b[1]-a[1])/(b[0]-a[0]) for a,b in zip(anchors,anchors[1:])]
tangents=[0.]+[0. if a*b<=0 else 2*a*b/(a+b) for a,b in zip(slopes,slopes[1:])]+[0.]
tangents[2]=tangents[3]=1.7/8
# Preserve constant forward launch speed across flight, without following silhouette-centre changes.
tangents[5]=tangents[6]=(22.499-20.952)/16

def travel(f):
 if f<=12:
  t=max(0.,min(1.,(f-8)/4));return .253+(.215-.253)*t*t*(3-2*t)
 for i,(a,b) in enumerate(zip(anchors,anchors[1:])):
  if a[0]<=f<=b[0]:
   h=b[0]-a[0];t=(f-a[0])/h
   return (2*t**3-3*t*t+1)*a[1]+(t**3-2*t*t+t)*h*tangents[i]+(-2*t**3+3*t*t)*b[1]+(t**3-t*t)*h*tangents[i+1]
 raise ValueError(f)

pose_objects={}
for i,key in enumerate(meta):
 label='Bruno / '+('run' if i<8 else 'jump')+' pose '+str(i%8+1)
 ob=next(o for o in actor.children if o.name.split('.')[0]==label);pose_objects[key]=ob
 old=ob.data;mat=old.materials[0];x0,y0,x1,y1=meta[key]['rect'];cx,cy=meta[key]['mass_pixel']
 # A connected textured grid supplies a small shear below the shorts. Entire head/torso
 # remains rigid and complete; no separately pasted head or regenerated artwork.
 nx,ny=24,40;verts=[];uvs=[];faces=[]
 for j in range(ny+1):
  py=y0+(y1-y0)*j/ny
  for k in range(nx+1):
   px=x0+(x1-x0)*k/nx;verts.append(((px-cx)*scale,0,(cy-py)*scale));uvs.append((px/1536,1-py/1024))
 for j in range(ny):
  for k in range(nx):
   a=j*(nx+1)+k;faces.append((a,a+nx+1,a+nx+2,a+1))
 mesh=bpy.data.meshes.new(label+' contact surface');mesh.from_pydata(verts,[],faces);mesh.materials.append(mat);uv=mesh.uv_layers.new()
 for poly in mesh.polygons:
  for loop in poly.loop_indices:uv.data[loop].uv=uvs[mesh.loops[loop].vertex_index]
 ob.data=mesh;ob.shape_key_add(name='Basis');sk=ob.shape_key_add(name='support compensation X');sk.slider_min=-1;sk.slider_max=1
 foot=meta[key]['foot'];weights=[]
 for v,kp in zip(mesh.vertices,sk.data):
  # Full correction near soles, zero above lower-body region; no vertical stretch.
  if foot:
   u=max(0.,min(1.,(foot[1]+.65-v.co.z)/.50));w=u*u*(3-2*u)
  else:w=0.
  kp.co.x+=w;weights.append(w)
 meta[key]['contact_weight_bounds']=[min(weights),max(weights)]
 ob['Correction']='Continuous body travel with local lower-body contact compensation; texture unchanged.'
 for row in rows:
  f=row['frame'];desired=travel(f)-meta[row['pose']]['neck'][0]
  sk.value=(row['x']-desired) if row['pose']==key and row['contact_world'] else 0.
  sk.keyframe_insert(data_path='value',frame=f)

for row in rows:
 f=row['frame'];head_x=travel(f);oldx=row['x'];row['x']=head_x-meta[row['pose']]['neck'][0]
 row['neck_world_x']=head_x;row['contact_compensation_x']=(oldx-row['x']) if row['contact_world'] else 0.
 actor.location=(row['x'],-.02,row['z']);actor.keyframe_insert(data_path='location',frame=f)
 # Camera follows planned travel, with a soft entrance into tracking. No feedback filter.
 d=max(0.,head_x-.05-.214);w=.9;camera_x=.214+(d*d/(2*w) if d<w else d-w/2)
 s.camera.location.x=camera_x;s.camera.keyframe_insert(data_path='location',frame=f);row['camera_x']=camera_x
for ob in [actor,s.camera,*[o.data.shape_keys for o in pose_objects.values()]]:
 ad=ob.animation_data
 if ad and ad.action:
  for layer in ad.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for kp in fc.keyframe_points:kp.interpolation='CONSTANT' if fc.data_path=='["pose_index"]' else 'LINEAR'
s['Review status']='Temporal correction candidate. Accepted pose drawings and exposure retained; screen-space travel/contact checks required.'
s['Travel method']='Registered neck-base trajectory; independent camera path; keyed lower-body contact compensation.'
s.frame_set(31)
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_overlays=False
out.mkdir(parents=True)
(out/'motion.json').write_text(json.dumps(rows,indent=2)+'\n');(out/'poses.json').write_text(json.dumps(meta,indent=2)+'\n')
prov=json.loads((src/'provenance.json').read_text());prov.update(revision='v003',camera_method='independent planned travel; soft entrance',contact_method='keyed continuous lower-body horizontal compensation',drawing_changes=False,travel_anchors=anchors,pose_exposure_changes=False);prov.pop('camera_follow_fraction_per_frame',None)
(out/'provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
bpy.data.libraries.write(str(out/'pose-action-v003.blend'),{s},fake_user=True)
result={'scene':name,'file':str(out/'pose-action-v003.blend'),'max_contact_correction':max(abs(r['contact_compensation_x']) for r in rows)}
