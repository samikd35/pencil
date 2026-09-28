"""Bounded complete-character proof. Source-fitted Video 1 binding plus Bruno v003 action travel.
Run setup(), rig(), animate_rig(), action(), regular_surface(), facial(), fit_action_rest(), save() visibly.
"""
import ast, bpy, json, math
import numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt
V=Path(__file__).resolve().parents[1]; O=V/'artifacts/gyokeres-proof-v015'; A=V/'assets/gyokeres-proof-v015'
P=V.parent/'001-manchester-derby-2026-09-13'; PREFIX='G15 / '
# Reuse definitions without executing earlier production setup or mutation.
def definitions(path,names):
 tree=ast.parse(path.read_text());ns={'bpy':bpy,'math':math,'Vector':Vector}
 chosen=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
 exec(compile(ast.Module(body=chosen,type_ignores=[]),str(path),'exec'),ns);return ns
old=definitions(P/'scripts/build_option_a.py',['image_material','segment_distance'])
source_tree=ast.parse((V/'scripts/rebuild_batch01_v012.py').read_text())
# dict(...) calls in the old config are evaluated alone; no rebuilding/retargeting code runs.
ns={};node=next(n for n in source_tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DESIGNS' for t in n.targets));exec(compile(ast.Module(body=[node],type_ignores=[]),'source_landmarks','exec'),ns);CFG=ns['DESIGNS']['gyokeres']
helpers=definitions(V/'scripts/rebuild_batch01_v012.py',['inside']); inside=helpers['inside']
U=1.8/(CFG['floor']-CFG['top']); rest={};controls={};bones={};poses={};rows=[]
def curves(ob):
 return [fc for l in ob.animation_data.action.layers for st in l.strips for bag in st.channelbags for fc in bag.fcurves] if ob.animation_data and ob.animation_data.action else []
def empty(name,loc,parent=None):
 ob=bpy.data.objects.new(PREFIX+name,None);s.collection.objects.link(ob);ob.location=loc;ob.parent=parent;return ob

def setup():
 global s,cam,root
 assert not bpy.app.background
 assert not bpy.data.scenes.get('S002_Gyokeres_complete_proof_v015')
 with bpy.data.libraries.load(str(V/'artifacts/pose-action-v003/pose-action-v003.blend'),link=False) as (a,l):l.scenes=['S002_whole_pose_action_v003']
 s=l.scenes[0];s.name='S002_Gyokeres_complete_proof_v015';bpy.context.window.scene=s
 for ob in list(s.objects):
  if not(ob.name.startswith('A /') or ob.name.startswith('S02 / touchline')):
   for col in list(ob.users_collection):col.objects.unlink(ob)
 s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=24;s.render.fps=24;s.frame_start=1;s.frame_end=336
 s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.use_sequencer=False
 s.view_settings.view_transform='Standard';s.view_settings.look='None'
 cd=bpy.data.cameras.new(PREFIX+'Camera');cd.type='ORTHO';cd.ortho_scale=4.4
 cam=bpy.data.objects.new(cd.name,cd);s.collection.objects.link(cam);cam.rotation_euler=(math.pi/2,0,0);cam.location=(0,-10,1.0);s.camera=cam
 root=empty('complete rig root',(-.65,-.02,.05));root.rotation_euler=(math.pi/2,0,0)
 s['Status']='Internal candidate; not user approved. One complete design, fitted rest proportions, shot-specific action.'
 for ar in bpy.context.screen.areas:
  if ar.type=='VIEW_3D':ar.spaces.active.region_3d.view_perspective='CAMERA';ar.spaces.active.shading.type='MATERIAL';ar.spaces.active.overlay.show_overlays=False
 return {'scene':s.name}

def xy(p):return Vector(((p[0]-CFG['center'])*U,(CFG['floor']-p[1])*U,0))
def rig():
 global skin,arm,pixels
 rest.update(hip=xy((424,567)),neck=xy((425,220)),head=xy((418,106)))
 for side in ['L','R']:
  for label,point in zip(['shoulder','elbow','wrist','finger','hip','knee','ankle','toe'],CFG[side]):rest[side+label]=xy(point)
 for key,p in rest.items():controls[key]=empty('CTRL '+key,p,root)
 bones.update(torso=('hip','neck'),head=('neck','head'))
 for side in ['L','R']:
  for label,aa,bb in [('upperarm','shoulder','elbow'),('forearm','elbow','wrist'),('hand','wrist','finger'),('thigh','hip','knee'),('calf','knee','ankle'),('foot','ankle','toe')]:bones[side+label]=(side+aa,side+bb)
 data=bpy.data.armatures.new(PREFIX+'source-fitted skeleton');arm=bpy.data.objects.new(data.name,data);s.collection.objects.link(arm);arm.parent=root;arm.show_in_front=True
 bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);bpy.context.view_layer.objects.active=arm;bpy.ops.object.mode_set(mode='EDIT')
 for key,(aa,bb) in bones.items():eb=data.edit_bones.new(key);eb.head=rest[aa];eb.tail=rest[bb]
 bpy.ops.object.mode_set(mode='OBJECT')
 for key,(aa,bb) in bones.items():
  pb=arm.pose.bones[key];co=pb.constraints.new('COPY_LOCATION');co.target=controls[aa];co=pb.constraints.new('STRETCH_TO');co.target=controls[bb];co.rest_length=(rest[bb]-rest[aa]).length;co.volume='NO_VOLUME';co.bulge=0
 outline=CFG['outline'];points=list(outline)
 for py in range(20,1004,6):
  for px in range(170,690,6):
   if inside(px,py,outline):points.append((px,py))
 coords,edges,faces,*_=delaunay_2d_cdt([Vector(p) for p in points],[],[list(range(len(outline)))],1,.001,False)
 pixels=[tuple(p) for p in coords];me=bpy.data.meshes.new(PREFIX+'complete source surface');me.from_pydata([xy(p) for p in pixels],[],faces)
 _,material=old['image_material'](V/'assets/rig-art-v012/arteta-gyokeres.png');me.materials.append(material);uv=me.uv_layers.new()
 for loop in me.loops:px,py=pixels[loop.vertex_index];uv.data[loop.index].uv=(px/1536,1-py/1024)
 skin=bpy.data.objects.new(me.name,me);s.collection.objects.link(skin);skin.parent=root
 groups={k:skin.vertex_groups.new(name=k) for k in bones}
 def clamp(x):return max(0.,min(1.,x))
 def near(p,names):
  ds=sorted((old['segment_distance'](p,rest[bones[k][0]],rest[bones[k][1]]),k) for k in names)[:2]
  vv=[math.exp(-(d*d-ds[0][0]**2)/(.042**2)) for d,k in ds];total=sum(vv);return {k:v/total for (_,k),v in zip(ds,vv)}
 for i,(px,py) in enumerate(pixels):
  pt=xy((px,py));side='L' if px<424 else 'R'
  if py<196:w={'head':1.}
  elif py<226:
   t=clamp((226-py)/30);w={'head':t,'torso':1-t}
  elif py<510:
   # Source-measured shoulder seam and open armpit, not another actor's width.
   edge=319 if side=='L' else 530
   t=clamp(((edge-px) if side=='L' else (px-edge))/32)
   if py>374:t=1. if (px<318 or px>537) else 0.
   w={k:v*t for k,v in near(pt,[side+'upperarm',side+'forearm',side+'hand']).items()};w['torso']=1-t
  elif py<638 and (px<245 or px>625):w=near(pt,[side+'forearm',side+'hand'])
  elif py<570:w={'torso':1.}
  else:
   w=near(pt,[side+'thigh',side+'calf',side+'foot']);t=clamp((608-py)/38);w={k:v*(1-t) for k,v in w.items()};w['torso']=t
  for key,val in w.items():
   if val>1e-8:groups[key].add([i],val,'REPLACE')
 mod=skin.modifiers.new('Video 1 continuous source binding','ARMATURE');mod.object=arm;mod.use_deform_preserve_volume=True
 skin['Source policy']='One unchanged complete drawing, including original head, neck, collar, garment and shoes. No replacement head surface.'
 skin['Rest policy']='All bone rest endpoints use this drawing. No rescaling new limbs to old animation.'
 return {'vertices':len(me.vertices),'bones':len(bones),'body_height':1.8}

def rotate(v,a):return Vector((v.x*math.cos(a)-v.y*math.sin(a),v.x*math.sin(a)+v.y*math.cos(a),v.z))
def ik(top,foot,l1,l2,pole):
 d=foot-top;distance=d.length;assert abs(l1-l2)<distance<l1+l2,(distance,l1+l2)
 along=(l1*l1-l2*l2+distance*distance)/(2*distance);h=math.sqrt(max(0,l1*l1-along*along));direction=d/distance;normal=Vector((-direction.y,direction.x,0));a=top+along*direction+h*normal;b=top+along*direction-h*normal
 return min([a,b],key=lambda p:(p-pole).length)
def smooth(t):t=max(0.,min(1.,t));return t*t*(3-2*t)
def animate_rig():
 # Foot contacts are explicit world-space anchors; the pelvis moves over them.
 for f in range(1,145):
  t=(f-1)/24;walking=f<=57;travel=.016*min(f-1,48)+.128*smooth((f-49)/8);root.location.x=-.65+travel;root.keyframe_insert(data_path='location',frame=f)
  p={k:v.copy() for k,v in rest.items()};phase=(f-1)/24*math.tau
  bob=(.010*(1-math.cos(2*phase))) if walking else 0.;offset=Vector((0,bob-.017,0))
  for key in ['hip','neck','head','Lshoulder','Rshoulder','Lhip','Rhip']:p[key]+=offset
  for side,shift in [('L',0),('R',12)]:
   foot=rest[side+'ankle'].copy();angle=0.
   if walking:
    q=(f-1+shift)%24;cycle=(f-1+shift)//24
    # Each sole remains at its own plant for 14 frames, then swings to the next.
    if q<14:dx=cycle*.384-shift*.016;lift=0.
    else:u=(q-14)/10;dx=(cycle+smooth(u))*.384-shift*.016;lift=.065*math.sin(math.pi*u)
    foot.x+=dx-travel;foot.y+=lift
    envelope=1-smooth((f-45)/12);foot=rest[side+'ankle'].lerp(foot,envelope)
   p[side+'ankle']=foot;p[side+'toe']=foot+rest[side+'toe']-rest[side+'ankle']
   l1=(rest[side+'knee']-rest[side+'hip']).length;l2=(rest[side+'ankle']-rest[side+'knee']).length
   top=p[side+'hip'];delta=foot-top
   if delta.length>=l1+l2-.005:p[side+'hip'].y-=delta.length-(l1+l2-.005)+.003
   p[side+'knee']=ik(p[side+'hip'],foot,l1,l2,rest[side+'knee']+Vector((.15,0,0)))
   a=.10*math.sin(phase+(0 if side=='L' else math.pi))*(1-smooth((f-45)/12)) if walking else 0
   # Quick motivated gesture on the stressed 'why', then an asymmetric hold/release.
   g=smooth((f-78)/7)*(1-smooth((f-115)/12))
   ua=a+(-.58 if side=='L' else .62)*g
   fa=ua+(-.80 if side=='L' else 1.12)*g
   p[side+'elbow']=p[side+'shoulder']+rotate(rest[side+'elbow']-rest[side+'shoulder'],ua)
   p[side+'wrist']=p[side+'elbow']+rotate(rest[side+'wrist']-rest[side+'elbow'],fa)
   p[side+'finger']=p[side+'wrist']+rotate(rest[side+'finger']-rest[side+'wrist'],fa)
  for k,pos in p.items():controls[k].location=pos;controls[k].keyframe_insert(data_path='location',frame=f)
 for ob in [skin]:
  for f,value in [(1,False),(144,False),(145,True),(336,True)]:ob.hide_render=ob.hide_viewport=value;ob.keyframe_insert(data_path='hide_render',frame=f);ob.keyframe_insert(data_path='hide_viewport',frame=f)
 for ob in [root,*controls.values()]:
  for fc in curves(ob):
   for kp in fc.keyframe_points:kp.interpolation='LINEAR'
 for f,x in [(1,0),(144,0)]:cam.location.x=x;cam.keyframe_insert(data_path='location',frame=f)
 return {'walk':[1,64],'performance':[65,144],'line_frame':85}

def action():
 global actor,metadata
 actor=empty('complete action root',(0,-.02,0));meta0=json.loads((V/'artifacts/pose-action-v003/poses.json').read_text());rows0=json.loads((V/'artifacts/pose-action-v003/motion.json').read_text())
 boxes={'run':[(28,5,410,511),(444,5,760,512),(785,5,1137,511),(1147,5,1536,511),(19,513,420,1024),(457,513,751,1024),(792,513,1122,1024),(1150,513,1536,1024)],'jump':[(60,8,338,514),(417,97,709,513),(782,8,1146,520),(1150,8,1530,508),(57,526,377,899),(480,525,762,986),(856,586,1176,1004),(1228,503,1505,1012)]}
 necks={'run':[(263,128),(626,128),(1000,128),(1388,128),(257,635),(622,635),(1001,635),(1382,635)],'jump':[(192,122),(641,214),(959,119),(1345,126),(204,642),(590,645),(989,712),(1373,617)]}
 feet={'run':[(305,406,468,509),(548,640,475,512),(790,860,456,509),None,(323,417,969,1014),(560,654,972,1015),(796,850,952,1006),None], 'jump':[(80,320,480,512),(500,687,474,513),(790,890,479,520),None,None,(610,751,930,986),(880,1065,963,1000),(1238,1496,974,1012)]}
 metadata={};scale=1.8/489
 for sheet in ['run','jump']:
  im,mat=old['image_material'](A/(sheet+'.png'));W,H=im.size;pix=np.empty(W*H*4,dtype=np.float32);im.pixels.foreach_get(pix);alpha=pix.reshape(H,W,4)[::-1,:,3]
  for i,rect in enumerate(boxes[sheet]):
   key=sheet+str(i);nx,ny=24,40;x0,y0,x1,y1=rect;cx,cy=necks[sheet][i];foot=None
   region=feet[sheet][i]
   if region:
    xa,xb,ya,yb=region;ys,xs=np.where(alpha[ya:yb,xa:xb]>.95);bottom=int(ys.max()+ya);near=ys+ya>=bottom-2;fx=float((xs[near]+xa).mean());foot=[(fx-cx)*scale,(cy-bottom)*scale]
   verts=[];uvs=[];faces=[]
   for j in range(ny+1):
    for k in range(nx+1):
     px=x0+(x1-x0)*k/nx;py=y0+(y1-y0)*j/ny;verts.append(((px-cx)*scale,0,(cy-py)*scale));uvs.append((px/W,1-py/H))
   for j in range(ny):
    for k in range(nx):q=j*(nx+1)+k;faces.append((q,q+nx+1,q+nx+2,q+1))
   me=bpy.data.meshes.new(PREFIX+key);me.from_pydata(verts,[],faces);me.materials.append(mat);uv=me.uv_layers.new()
   for loop in me.loops:uv.data[loop.index].uv=uvs[loop.vertex_index]
   ob=bpy.data.objects.new(me.name,me);s.collection.objects.link(ob);ob.parent=actor;poses[key]=ob
   ob.shape_key_add(name='Basis');sk=ob.shape_key_add(name='support compensation X');sk.slider_min=-1;sk.slider_max=1
   for v,kp in zip(me.vertices,sk.data):
    u=max(0,min(1,(foot[1]+.65-v.co.z)/.5)) if foot else 0;kp.co.x+=smooth(u)
   metadata[key]={'rect':rect,'neck_pixel':[cx,cy],'foot':foot,'scale':scale}
   for prop in ['hide_render','hide_viewport']:
    d=ob.driver_add(prop).driver;d.expression='pose != '+str(len(poses)-1);v=d.variables.new();v.name='pose';v.type='SINGLE_PROP';v.targets[0].id=actor;v.targets[0].data_path='["pose_index"]'
 actor['pose_index']=-1;actor.keyframe_insert(data_path='["pose_index"]',frame=1);actor.keyframe_insert(data_path='["pose_index"]',frame=144)
 launch_z=.05-metadata['jump2']['foot'][1];land_z=.05-metadata['jump5']['foot'][1];T=16/24;vy=(land_z-launch_z+4.905*T*T)/T
 for row in rows0:
  f=row['frame'];ff=f+144;key=row['pose'];foot=metadata[key]['foot'];x=row['neck_world_x'];contact=row['contact_world'];correction=(contact[0]-x-foot[0]) if contact and foot else 0.
  if contact and foot:z=.05-foot[1]
  elif row['phase']=='jump_flight':t=(f-122)/24;z=launch_z+vy*t-4.905*t*t
  else:z=row['z']+meta0[key]['neck'][1]
  actor.location=(x,-.02,z);actor.keyframe_insert(data_path='location',frame=ff);actor['pose_index']=list(poses).index(key);actor.keyframe_insert(data_path='["pose_index"]',frame=ff)
  for name,ob in poses.items():sk=ob.data.shape_keys.key_blocks['support compensation X'];sk.value=correction if name==key else 0.;sk.keyframe_insert(data_path='value',frame=ff)
  cam.location.x=row['camera_x'];cam.keyframe_insert(data_path='location',frame=ff)
  rows.append({'frame':ff,'phase':row['phase'],'pose':key,'neck':[x,z],'correction_x':correction,'contact':contact})
 for ob in [actor,cam,*[ob.data.shape_keys for ob in poses.values()]]:
  for fc in curves(ob):
   for kp in fc.keyframe_points:kp.interpolation='CONSTANT' if fc.data_path=='["pose_index"]' else 'LINEAR'
 cam.location.z=1.15
 (O/'motion.json').write_text(json.dumps(rows,indent=2));(O/'poses.json').write_text(json.dumps(metadata,indent=2))
 return {'drawings':16,'max_contact_correction':max(abs(r['correction_x']) for r in rows),'launch_velocity':vy}

def save():
 s.frame_set(95);bpy.context.view_layer.update()
 bpy.data.libraries.write(str(O/'gyokeres-proof-v015.blend'),{s},fake_user=True)
 return {'native':str(O/'gyokeres-proof-v015.blend'),'frames':s.frame_end}

def regular_surface():
 """Video 1's regular UV grid avoids narrow silhouette-triangulation slivers."""
 global pixels
 # Preserve the exact native weight-smoothing stage used in the visible proof.
 bpy.ops.object.select_all(action='DESELECT');skin.select_set(True);bpy.context.view_layer.objects.active=skin;bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.object.vertex_group_smooth(group_select_mode='ALL',factor=.7,repeat=20,expand=0);bpy.ops.object.vertex_group_normalize_all(group_select_mode='ALL',lock_active=False);bpy.ops.object.mode_set(mode='OBJECT')
 oldme=skin.data;nx,ny=90,164;x0,x1=156,702;y0,y1=10,1014
 pixels=[(x0+(x1-x0)*i/nx,y0+(y1-y0)*j/ny) for j in range(ny+1) for i in range(nx+1)]
 faces=[]
 for j in range(ny):
  for i in range(nx):q=j*(nx+1)+i;faces.extend([(q,q+1,q+nx+2),(q,q+nx+2,q+nx+1)])
 me=bpy.data.meshes.new(PREFIX+'regular complete source grid');me.from_pydata([xy(p) for p in pixels],[],faces);me.materials.append(oldme.materials[0]);uv=me.uv_layers.new()
 for loop in me.loops:px,py=pixels[loop.vertex_index];uv.data[loop.index].uv=(px/1536,1-py/1024)
 # Transfer existing semantic weights by source-space nearest vertex, then diffuse
 # locally on the image silhouette, so gaps cannot transfer sleeve weights to shirt.
 points=np.array([v.co[:2] for v in oldme.vertices]);prior=np.zeros((len(points),len(bones)))
 for v in oldme.vertices:
  for w in v.groups:prior[v.index,w.group]=w.weight
 weights=np.empty((len(pixels),len(bones)))
 for st in range(0,len(pixels),200):
  pp=np.array([xy(p)[:2] for p in pixels[st:st+200]]);idx=((pp[:,None,:]-points[None,:,:])**2).sum(2).argmin(1);weights[st:st+len(pp)]=prior[idx]
 im=next(n.image for n in oldme.materials[0].node_tree.nodes if n.type=='TEX_IMAGE');pix=np.empty(im.size[0]*im.size[1]*4,dtype=np.float32);im.pixels.foreach_get(pix);alpha=pix.reshape(im.size[1],im.size[0],4)[::-1,:,3]
 valid=np.array([alpha[min(1023,round(py)),min(1535,round(px))]>.5 for px,py in pixels]).reshape(ny+1,nx+1)
 w=weights.reshape(ny+1,nx+1,-1);original=w.copy();mask=valid[:,:,None]
 # Use the native image silhouette as the adjacency boundary. Source geometry is unchanged.
 for iteration in range(80):
  total=w.copy();count=np.ones((ny+1,nx+1,1))
  for axis in [0,1]:
   for shift in [-1,1]:
    m=np.roll(mask,shift,axis);rolled=np.roll(w,shift,axis)
    if axis==0:m[0 if shift==1 else -1,:,:]=False
    else:m[:,0 if shift==1 else -1,:]=False
    total+=rolled*m;count+=m
  w=.35*w+.65*total/count
  # Keep the face and central shirt rigid; diffuse only body joints and attachment seams.
  for j in range(ny+1):
   py=y0+(y1-y0)*j/ny
   if py<190:w[j]=original[j]
 skin.data=me;skin.vertex_groups.clear();groups=[skin.vertex_groups.new(name=k) for k in bones]
 weights=w.reshape(-1,len(bones));weights/=weights.sum(axis=1,keepdims=True)
 for i,row in enumerate(weights):
  for k,val in enumerate(row):
   if val>1e-7:groups[k].add([i],float(val),'REPLACE')
 skin['Grid']='Uniform UV grid, connected source drawing; local weights diffuse within source silhouette, no bone/proportion changes.'
 return {'vertices':len(me.vertices),'grid':[nx,ny]}

def facial():
 """Native lip articulation follows the head bone and the actual take's word timing."""
 def flat(name,points,color,z):
  me=bpy.data.meshes.new(PREFIX+name);me.from_pydata([(xy(p).x,xy(p).y,z) for p in points],[],[list(range(len(points)))]);ob=bpy.data.objects.new(me.name,me);s.collection.objects.link(ob);ob.parent=root
  m=bpy.data.materials.new(PREFIX+name);m.diffuse_color=(*color,1);m.use_nodes=True;n=m.node_tree.nodes;n.clear();em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(*color,1);out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(em.outputs[0],out.inputs[0]);me.materials.append(m)
  vg=ob.vertex_groups.new(name='head');vg.add(list(range(len(points))),1,'REPLACE');mod=ob.modifiers.new('Follow same head bone','ARMATURE');mod.object=arm;mod.use_deform_preserve_volume=True
  return ob
 # The closed painted lip is retained. Geometry is visible only during the spoken line.
 points=[]
 for upper in [True,False]:
  for i in (range(17) if upper else range(16,-1,-1)):
   t=-1+2*i/16;arc=math.sqrt(max(0,1-t*t));points.append((455+15*t,158-2*t+(-1.4 if upper else 8)*arc))
 mouth=flat('mouth cavity',points,(.075,.019,.014),.006)
 teeth=flat('upper teeth',[(443,158),(466,155),(466,158),(444,160)],(.94,.88,.77),.007)
 mouth.shape_key_add(name='Basis');narrow=mouth.shape_key_add(name='Rounded');closed=mouth.shape_key_add(name='Close')
 for i,(px,py) in enumerate(points):
  narrow.data[i].co.x=xy((455+.62*(px-455),py)).x
  closed.data[i].co.y=xy((px,158-2*(px-455)/15)).y
 keys=[(84,0,.1),(85,.3,.1),(88,.75,0),(92,.35,0),(95,.12,.1),(96,.2,1),(98,1,.4),(102,.6,0),(104,.75,0),(107,.05,0),(109,.8,.1),(112,.45,0),(115,.55,0),(119,.25,.25),(122,0,0)]
 for f,op,rounding in keys:
  closed.value=1-op;closed.keyframe_insert(data_path='value',frame=f);narrow.value=rounding;narrow.keyframe_insert(data_path='value',frame=f)
 for ob in [mouth,teeth]:
  for f,hide in [(1,True),(84,True),(85,False),(121,False),(122,True),(336,True)]:
   ob.hide_viewport=ob.hide_render=hide;ob.keyframe_insert(data_path='hide_viewport',frame=f);ob.keyframe_insert(data_path='hide_render',frame=f)
  for fc in curves(ob):
   for kp in fc.keyframe_points:kp.interpolation='CONSTANT'
 # A brief blink deforms the eyes within the same source mesh, not a new face image.
 skin.shape_key_add(name='Basis');blink=skin.shape_key_add(name='Blink')
 for i,(px,py) in enumerate(pixels):
  for ex,ey,rx,ry in CFG['eyes']:
   dx=abs(px-ex)/(rx+2);dy=abs(py-ey)/(ry+2)
   if dx<1.3 and dy<1.5:
    w=max(0,min(1,(1.3-dx)/.3))*max(0,min(1,(1.5-dy)/.5));blink.data[i].co.y+=(py-ey)*U*.85*w
 for f,value in [(1,0),(67,0),(69,1),(71,0),(125,0),(127,1),(129,0),(336,0)]:blink.value=value;blink.keyframe_insert(data_path='value',frame=f)
 for ob in [mouth.data.shape_keys,skin.data.shape_keys]:
  for fc in curves(ob):
   for kp in fc.keyframe_points:kp.interpolation='LINEAR'
 # Same chosen speech take; native soundtrack stays available in Blender playback.
 seq=s.sequence_editor_create();sound=seq.strips.new_sound('Gyokeres / Then why am I here',str(V/'artifacts/animatic-v001/voices/L08-mix.wav'),channel=1,frame_start=85);sound.volume=1
 s.sync_mode='AUDIO_SYNC'
 for f in range(1,337):
  cam.location.z=1.1 if f<145 else 1.35;cam.keyframe_insert(data_path='location',index=2,frame=f);cam.data.ortho_scale=4.4 if f<145 else 5.6;cam.data.keyframe_insert(data_path='ortho_scale',frame=f)
 for fc in curves(cam.data):
  for kp in fc.keyframe_points:kp.interpolation='CONSTANT'
 return {'line_frames':[85,122],'source':'L08-mix.wav','mouth':'native geometry on same head bone','blink':'same-source deformation'}

def fit_action_rest():
 """Transferred motion keeps its timing; neutral registration belongs to the new drawing."""
 start=-metadata['jump0']['foot'][0];end=rows[-1]['contact'][0]-metadata['jump0']['foot'][0]
 for r in rows:
  f=r['frame']-144
  if f<=8:x=start
  elif f<=12:x=start+(.22-start)*smooth((f-8)/5)
  elif f>=145:x=23.248+(end-23.248)*smooth((f-145)/8)
  else:continue
  r['neck'][0]=x;m=metadata[r['pose']];r['correction_x']=r['contact'][0]-x-m['foot'][0] if r['contact'] else 0
  actor.location=(x,-.02,r['neck'][1]);actor.keyframe_insert(data_path='location',frame=r['frame'])
  ob=poses[r['pose']];sk=ob.data.shape_keys.key_blocks['support compensation X'];sk.value=r['correction_x'];sk.keyframe_insert(data_path='value',frame=r['frame'])
 assert max(abs(r['correction_x']) for r in rows if r['phase'] in ['ready','settled'])<1e-8
 (O/'motion.json').write_text(json.dumps(rows,indent=2))
 return {'neutral_contact_correction':0,'start_neck_x':start,'settled_neck_x':end,'timing_changes':False,'artwork_changes':False}
