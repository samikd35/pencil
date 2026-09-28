"""First batch: retain staged shots/audio; complete source-fitted characters and front-view gait."""
import bpy,ast,math,json,numpy as np
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/batch01-v016';O.mkdir(exist_ok=True)
source=V/'scripts/build_gyokeres_proof_v015.py';defs={ '__file__':str(source)};exec(compile(source.read_text(),str(source),'exec'),defs)
CFG=defs['ns']['DESIGNS'];old=defs['old'];curves=defs['curves'];smooth=defs['smooth'];rotate=defs['rotate'];ACTORS={}
SPEECH=json.loads((V/'artifacts/batch01-v014/speech-timing.json').read_text())

def empty(s,name,p,parent=None):
 o=bpy.data.objects.new(name,None);s.collection.objects.link(o);o.location=p;o.parent=parent;return o

def make(name,kind,mirror=False):
 group='opening' if name.startswith('opening') else 'unveiling';s=bpy.data.scenes['S002_B01_v016_'+group];bpy.context.window.scene=s;s.frame_set(1)
 prefix='B01 / '+name+' / ';original=bpy.data.objects[prefix+'CTRL character'];cfg=CFG[kind];u=1.8/(cfg['floor']-cfg['top']);P='B16 / '+name+' / '
 def xy(p):return Vector(((p[0]-cfg['center'])*u,(cfg['floor']-p[1])*u,0))
 root=empty(s,P+'character',original.location);height=original.scale.y*604;root.scale=((-1 if mirror else 1)*height/1.8,height/1.8,height/1.8)
 rest={'hip':xy((cfg['center'],cfg['hip'])),'neck':xy(cfg['neck']),'head':xy(cfg['head'])}
 for side in ['L','R']:
  for label,point in zip(['shoulder','elbow','wrist','finger','hip','knee','ankle','toe'],cfg[side]):rest[side+label]=xy(point)
 C={k:empty(s,P+'CTRL '+k,p,root) for k,p in rest.items()};bones={'torso':('hip','neck'),'head':('neck','head')}
 for side in ['L','R']:
  for label,aa,bb in [('upperarm','shoulder','elbow'),('forearm','elbow','wrist'),('hand','wrist','finger'),('thigh','hip','knee'),('calf','knee','ankle'),('foot','ankle','toe')]:bones[side+label]=(side+aa,side+bb)
 ad=bpy.data.armatures.new(P+'source fitted');arm=bpy.data.objects.new(ad.name,ad);s.collection.objects.link(arm);arm.parent=root;bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);bpy.context.view_layer.objects.active=arm;bpy.ops.object.mode_set(mode='EDIT')
 for k,(aa,bb) in bones.items():eb=ad.edit_bones.new(k);eb.head=rest[aa];eb.tail=rest[bb]
 bpy.ops.object.mode_set(mode='OBJECT')
 for k,(aa,bb) in bones.items():
  pb=arm.pose.bones[k];co=pb.constraints.new('COPY_LOCATION');co.target=C[aa];co=pb.constraints.new('STRETCH_TO');co.target=C[bb];co.rest_length=(rest[bb]-rest[aa]).length;co.volume='NO_VOLUME';co.bulge=0
 nx,ny=90,164;outline=cfg['outline'];x0=min(x for x,y in outline)-12;x1=max(x for x,y in outline)+12;y0=cfg['top']-7;y1=cfg['floor']+16
 pixels=[(x0+(x1-x0)*i/nx,y0+(y1-y0)*j/ny) for j in range(ny+1) for i in range(nx+1)];verts=[xy(p) for p in pixels];faces=[]
 for j in range(ny):
  for i in range(nx):q=j*(nx+1)+i;faces.extend([(q,q+1,q+nx+2),(q,q+nx+2,q+nx+1)])
 me=bpy.data.meshes.new(P+'complete source drawing');me.from_pydata(verts,[],faces);im,mat=old['image_material'](V/'assets/rig-art-v012/arteta-gyokeres.png');me.materials.append(mat);uv=me.uv_layers.new()
 for loop in me.loops:px,py=pixels[loop.vertex_index];uv.data[loop.index].uv=(px/1536,1-py/1024)
 skin=bpy.data.objects.new(me.name,me);s.collection.objects.link(skin);skin.parent=root;groups=[skin.vertex_groups.new(name=k) for k in bones];weights=np.zeros((len(pixels),len(bones)));names=list(bones)
 def near(pt,candidates):
  ds=sorted((old['segment_distance'](pt,rest[bones[k][0]],rest[bones[k][1]]),k) for k in candidates)[:2];ww=[math.exp(-(d*d-ds[0][0]**2)/.0025) for d,k in ds];total=sum(ww);return {k:v/total for (_,k),v in zip(ds,ww)}
 for i,(pt,(px,py)) in enumerate(zip(verts,pixels)):
  side='L' if px<cfg['center'] else 'R';nxp,nyp=cfg['neck'];hip=cfg['hip'];edge=cfg['body_edge'];width=float(np.interp(py,[r[0] for r in edge],[r[1] for r in edge]))
  if py<nyp-26:w={'head':1}
  elif py<nyp+6:t=max(0,min(1,(nyp+6-py)/32));w={'head':t,'torso':1-t}
  elif py<hip-40:
   t=max(0,min(1,(abs(px-cfg['center'])-width)/30));w={k:v*t for k,v in near(pt,[side+'upperarm',side+'forearm',side+'hand']).items()};w['torso']=1-t
  elif py<hip+75 and abs(px-cfg['center'])>160:w=near(pt,[side+'forearm',side+'hand'])
  elif py<hip:w={'torso':1}
  else:
   w=near(pt,[side+'thigh',side+'calf',side+'foot']);t=max(0,min(1,(hip+38-py)/38));w={k:v*(1-t) for k,v in w.items()};w['torso']=t
  for k,val in w.items():weights[i,names.index(k)]=val
 pix=np.empty(1536*1024*4,dtype=np.float32);im.pixels.foreach_get(pix);alpha=pix.reshape(1024,1536,4)[::-1,:,3];valid=np.array([alpha[min(1023,max(0,round(py))),round(px)]>.5 for px,py in pixels]).reshape(ny+1,nx+1);w=weights.reshape(ny+1,nx+1,-1);prior=w.copy()
 for iteration in range(95):
  total=w.copy();count=np.ones((ny+1,nx+1,1))
  for axis in [0,1]:
   for shift in [-1,1]:
    mask=np.roll(valid[:,:,None],shift,axis)
    if axis==0:mask[0 if shift==1 else -1,:,:]=False
    else:mask[:,0 if shift==1 else -1,:]=False
    total+=np.roll(w,shift,axis)*mask;count+=mask
  w=.35*w+.65*total/count
  for j in range(ny+1):
   if y0+(y1-y0)*j/ny<cfg['neck'][1]-32:w[j]=prior[j]
 weights=w.reshape(-1,len(bones));weights/=weights.sum(1,keepdims=True)
 for i,(px,py) in enumerate(pixels):
  # Shoes are rigid below the ankle cuff; keep the sole from breathing with the calf.
  ankle_y=(cfg['L'][6][1]+cfg['R'][6][1])/2;t=smooth((py-ankle_y+10)/32)
  if t>0:
   weights[i]*=1-t;weights[i,names.index(('L' if px<cfg['center'] else 'R')+'foot')]+=t
  for k,val in enumerate(weights[i]):
   if val>1e-7:groups[k].add([i],float(val),'REPLACE')
 mod=skin.modifiers.new('Continuous complete drawing on fitted bones','ARMATURE');mod.object=arm;mod.use_deform_preserve_volume=True
 for ob in s.objects:
  if ob.name.startswith(prefix) and ob.type in ['MESH','CURVE','FONT']:
   ob.hide_render=ob.hide_viewport=True
   # Old visibility drivers/keyframes must not resurrect superseded surfaces.
   for prop in ['hide_render','hide_viewport']:
    try:ob.driver_remove(prop)
    except Exception:pass
   for fc in list(curves(ob)):
    if fc.data_path in ['hide_render','hide_viewport']:
     for kp in fc.keyframe_points:kp.co.y=1
 a={'name':name,'kind':kind,'s':s,'prefix':prefix,'P':P,'root':root,'rest':rest,'C':C,'skin':skin,'arm':arm,'cfg':cfg,'xy':xy,'pixels':pixels,'mirror':mirror,'height':height};ACTORS[name]=a;return {'actor':name,'vertices':len(verts)}

def animate(name):
 a=ACTORS[name];s=a['s'];bpy.context.window.scene=s;r=a['rest'];C=a['C'];root=a['root'];isgy=a['kind']=='gyokeres';p=a['prefix'];oldC={k:bpy.data.objects[p+'CTRL '+k] for k in ['chest','head','L upper arm','L forearm','L hand','R upper arm','R forearm','R hand']};base=bpy.data.objects[p+'CTRL character'].location.copy();scale=a['height']/1.8
 foot0={side:Vector((base.x+scale*r[side+'ankle'].x,base.y,base.z)) for side in ['L','R']};footrows=[]
 for f in range(1,s.frame_end+1):
  s.frame_set(f);pose={k:v.copy() for k,v in r.items()};chest=oldC['chest'].rotation_euler.z;head=oldC['head'].rotation_euler.z
  # Author projected approach, not a lateral side-view gait on frontal artwork.
  walk=smooth((f-40)/36) if isgy else 0.;root.location=base+Vector((.55*walk,.24*(1-walk) if isgy else 0,0));root.keyframe_insert(data_path='location',frame=f)
  hipshift=0.;hipdown=0.
  if isgy:
   hipshift=.025*math.sin(math.pi*max(0,min(1,(f-39)/18))) if f<58 else -.022*math.sin(math.pi*max(0,min(1,(f-57)/20)))
   hipdown=-.028*math.sin(math.pi*max(0,min(1,(f-40)/36)))
  offset=Vector((hipshift,hipdown,0));pose['hip']=r['hip']+offset
  for k in ['neck','Lshoulder','Rshoulder']:pose[k]=pose['hip']+rotate(r[k]-r['hip'],chest)
  pose['head']=pose['neck']+rotate(r['head']-r['neck'],chest+head)
  for side in ['L','R']:
   pose[side+'hip']=r[side+'hip']+offset
   if isgy:
    first,last=(42,55) if side=='L' else (60,73);u=smooth((f-first)/(last-first));lift=.042*math.sin(math.pi*max(0,min(1,(f-first)/(last-first))))
    start=Vector((foot0[side].x,base.y+.24,base.z));end=Vector((foot0[side].x+.55,base.y,base.z));world=start.lerp(end,u);world.y+=lift*scale
    pose[side+'ankle']=Vector(((world.x-root.location.x)/scale,(world.y-root.location.y)/scale,0))+Vector((0,r[side+'ankle'].y,0))
    # Knee bend projects mainly into depth in this frontal view. Keep the knee
    # under its hip instead of solving a sideways hinge that creates a bow-leg.
    top=pose[side+'hip'];ankle=pose[side+'ankle'];fraction=(r[side+'knee'].y-r[side+'hip'].y)/(r[side+'ankle'].y-r[side+'hip'].y)
    pose[side+'knee']=top.lerp(ankle,fraction);pose[side+'knee'].x+=(-1 if side=='L' else 1)*.012
    pose[side+'toe']=pose[side+'ankle']+r[side+'toe']-r[side+'ankle']
    footrows.append({'frame':f,'side':side,'swing':first<f<last,'sole_target':list(world),'root':list(root.location)})
   ua=oldC[side+' upper arm'].rotation_euler.z+chest;fa=ua+oldC[side+' forearm'].rotation_euler.z;ha=fa+oldC[side+' hand'].rotation_euler.z
   if a['mirror']:srcside='R' if side=='L' else 'L';ua=-oldC[srcside+' upper arm'].rotation_euler.z-chest;fa=ua-oldC[srcside+' forearm'].rotation_euler.z;ha=fa-oldC[srcside+' hand'].rotation_euler.z
   if isgy and 293<=f<=351:
    g=smooth((f-293)/8)*(1-smooth((f-340)/11));ha+=(-.72 if side=='L' else .72)*g
   for label,prev,ang in [('elbow','shoulder',ua),('wrist','elbow',fa),('finger','wrist',ha)]:
    length=(r[side+label]-r[side+prev]).length;pose[side+label]=pose[side+prev]+Vector((length*math.sin(ang),-length*math.cos(ang),0))
  for k,v in pose.items():C[k].location=v;C[k].keyframe_insert(data_path='location',frame=f)
 for ob in [root,*C.values()]:
  for fc in curves(ob):
   for kp in fc.keyframe_points:kp.interpolation='LINEAR'
 if footrows:(O/'gyokeres-approach-contacts.json').write_text(json.dumps(footrows,indent=2))
 return {'actor':name,'frames':s.frame_end,'gait':'projected approach with alternating planted soles' if isgy else 'retained shot gesture timing on source fitted bones'}

def face(name):
 a=ACTORS[name];s=a['s'];cfg=a['cfg'];r=a['rest'];xy=a['xy'];root=a['root'];arm=a['arm'];mx,my,mw=cfg['mouth'];u=1.8/(cfg['floor']-cfg['top']);P=a['P']
 def mesh(label,points,col,z):
  me=bpy.data.meshes.new(P+label);me.from_pydata([(xy(p).x,xy(p).y,z) for p in points],[],[list(range(len(points)))]);ob=bpy.data.objects.new(me.name,me);s.collection.objects.link(ob);ob.parent=root;m=bpy.data.materials.new(P+label);m.use_nodes=True;n=m.node_tree.nodes;n.clear();em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(*col,1);out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(em.outputs[0],out.inputs[0]);me.materials.append(m);vg=ob.vertex_groups.new(name='head');vg.add(list(range(len(points))),1,'REPLACE');mod=ob.modifiers.new('Same head bone','ARMATURE');mod.object=arm;mod.use_deform_preserve_volume=True;return ob
 pts=[]
 for upper in [True,False]:
  for i in (range(17) if upper else range(16,-1,-1)):
   t=-1+i/8;arc=math.sqrt(max(0,1-t*t));pts.append((mx+mw*.83*t,my-2*t+(-1.4 if upper else 8)*arc))
 mo=mesh('native mouth',pts,(.055,.013,.010),.010);te=mesh('native teeth',[(mx-mw*.65,my),(mx+mw*.60,my-2.5),(mx+mw*.60,my+.5),(mx-mw*.60,my+2)],(.94,.88,.77),.012)
 mo.shape_key_add(name='Basis');closed=mo.shape_key_add(name='Closed');rounded=mo.shape_key_add(name='Rounded')
 for i,(px,py) in enumerate(pts):closed.data[i].co.y=xy((px,my-2*(px-mx)/(mw*.83))).y;rounded.data[i].co.x=xy((mx+.62*(px-mx),py)).x
 keys=SPEECH[name]['mouth_keys'];values={'rest':(0,0),'MBP':(.05,0),'A':(.95,0),'E':(.5,0),'O':(.85,1),'U':(.4,1),'FV':(.18,0),'L':(.55,0)}
 for fs,label in keys.items():
  f=int(fs);op,ro=values[label];closed.value=1-op;closed.keyframe_insert(data_path='value',frame=f);rounded.value=ro;rounded.keyframe_insert(data_path='value',frame=f)
  for ob in [mo,te]:ob.hide_render=ob.hide_viewport=(label in ['rest','MBP'] or ob==te and label in ['O','U']);ob.keyframe_insert(data_path='hide_render',frame=f);ob.keyframe_insert(data_path='hide_viewport',frame=f)
 for ob in [mo,te]:
  for fc in curves(ob):
   for kp in fc.keyframe_points:kp.interpolation='CONSTANT'
 for fc in curves(mo.data.shape_keys):
  for kp in fc.keyframe_points:kp.interpolation='LINEAR'
 # Use the same restrained blink deformation accepted for continuation, not a new face.
 sk=a['skin'];sk.shape_key_add(name='Basis');blink=sk.shape_key_add(name='Blink')
 for i,(px,py) in enumerate(a['pixels']):
  for ex,ey,rx,ry in cfg['eyes']:
   dx=abs(px-ex)/(rx+2);dy=abs(py-ey)/(ry+2)
   if dx<1.3 and dy<1.5:w=max(0,min(1,(1.3-dx)/.3))*max(0,min(1,(1.5-dy)/.5));blink.data[i].co.y+=(py-ey)*u*.85*w
 for f in [1,s.frame_end]:blink.value=0;blink.keyframe_insert(data_path='value',frame=f)
 for f in [36,158,277,403]:
  if f+4<s.frame_end:
   for k,v in [(f,0),(f+2,1),(f+4,0)]:blink.value=v;blink.keyframe_insert(data_path='value',frame=k)
 return {'actor':name,'speech':'existing timed take','head_replacement':False}

def save():
 rows=json.loads((V/'artifacts/batch01-v014/edit.json').read_text())
 for r in rows:r['scene']=r['scene'].replace('v014','v016')
 (O/'edit.json').write_text(json.dumps(rows,indent=2));scenes={bpy.data.scenes[r['scene']] for r in rows};bpy.data.libraries.write(str(O/'batch01-v016.blend'),scenes,fake_user=True)
 (O/'cast.json').write_text(json.dumps({k:{'scene':a['s'].name,'root':a['root'].name,'skin':a['skin'].name,'controls':{k:o.name for k,o in a['C'].items()},'mirror':a['mirror'],'cfg':a['cfg']} for k,a in ACTORS.items()},indent=2))
 return {'native':str(O/'batch01-v016.blend'),'frames':1021}

def contact_props():
 """Rebuild phone reach on fitted lengths; reattach props to the actual drawn hands."""
 a=ACTORS['opening Arteta'];s=a['s'];bpy.context.window.scene=s;r=a['rest'];C=a['C'];phone=bpy.data.objects['B01 Arteta phone'];phone.parent=a['root'];phone.animation_data_clear();unit=.00794702023267746/(a['height']/1.8)
 l1=(r['Relbow']-r['Rshoulder']).length;l2=(r['Rwrist']-r['Relbow']).length
 for f in range(1,410):
  s.frame_set(f);t=smooth((f-331)/10)*(1-smooth((f-395)/14));shoulder=C['Rshoulder'].location.copy();target=C['neck'].location+Vector((.115,.045,0));old=C['Rwrist'].location.copy();wrist=old.lerp(target,t)
  elbow=defs['ik'](shoulder,wrist,l1,l2,shoulder+Vector((.25,-.25,0))) if t>.01 else C['Relbow'].location.copy()
  for k,v in [('Relbow',elbow),('Rwrist',wrist),('Rfinger',wrist+Vector((.005,.13,0)))]:C[k].location=v;C[k].keyframe_insert(data_path='location',frame=f)
  phone.location=(wrist.x-.007,wrist.y+.09,.022);phone.scale=(unit,)*3 if f>=338 else (0,0,0);phone.keyframe_insert(data_path='location',frame=f);phone.keyframe_insert(data_path='scale',frame=f)
 for ob in [phone,C['Relbow'],C['Rwrist'],C['Rfinger']]:
  for fc in curves(ob):
   for kp in fc.keyframe_points:kp.interpolation='CONSTANT' if fc.data_path=='scale' else 'LINEAR'
 a=ACTORS['unveiling Gyokeres'];s=a['s'];bpy.context.window.scene=s;C=a['C'];bag=bpy.data.objects['B01 Gyokeres travel bag'];s.frame_set(26);bpy.context.view_layer.update();bag.animation_data_clear();ground=bag.location.copy()
 # Raise/lower the existing bag into its final contact, with the grip solved to the handle.
 handle=next(o for o in bag.children_recursive if o.name.startswith('Bag handle'))
 bbox=[handle.matrix_world@Vector(c) for c in handle.bound_box];top=max(v.y for v in bbox);center=(min(v.x for v in bbox)+max(v.x for v in bbox))/2;offset=Vector((center-ground.x,top-ground.y,0));r=a['rest'];l1=(r['Lelbow']-r['Lshoulder']).length;l2=(r['Lwrist']-r['Lelbow']).length
 for f in range(1,433):
  s.frame_set(f);bag.location=ground+Vector((0,.28*(1-smooth((f-8)/18)) if f<=26 else 0,0));bag.keyframe_insert(data_path='location',frame=f)
  if f<=39:
   bpy.context.view_layer.update();grip=a['root'].matrix_world.inverted()@(bag.location+offset+Vector((0,0,a['root'].location.z-bag.location.z)));wrist=grip-Vector((0,-.06,0));shoulder=C['Lshoulder'].location.copy();d=wrist-shoulder
   # Bring the body down before contact if the carried handle exceeds its reach.
   if d.length>l1+l2-.008:wrist=shoulder+d.normalized()*(l1+l2-.008)
   elbow=defs['ik'](shoulder,wrist,l1,l2,shoulder+Vector((-.15,-.2,0)));release=smooth((f-27)/12)
   for k,v in [('Lelbow',elbow),('Lwrist',wrist),('Lfinger',grip)]:C[k].location=v.lerp(C[k].location,release);C[k].keyframe_insert(data_path='location',frame=f)
 for ob in [bag,C['Lelbow'],C['Lwrist'],C['Lfinger']]:
  for fc in curves(ob):
   for kp in fc.keyframe_points:kp.interpolation='LINEAR'
 return {'phone':'fitted elbow below shoulder; actual hand parenting','bag':'existing set-down timing and carpet contact retained'}

def trim_transparent_grid():
 """Do not leave empty canvas triangles to fold over opaque body surfaces."""
 import bmesh
 for a in ACTORS.values():
  ob=a['skin'];im=next(nd.image for nd in ob.data.materials[0].node_tree.nodes if nd.type=='TEX_IMAGE');pix=np.empty(1536*1024*4,dtype=np.float32);im.pixels.foreach_get(pix);alpha=pix.reshape(1024,1536,4)[::-1,:,3];bm=bmesh.new();bm.from_mesh(ob.data);bm.faces.ensure_lookup_table();dead=[]
  for face in bm.faces:
   pp=[a['pixels'][v.index] for v in face.verts];x0=max(0,int(min(p[0] for p in pp)));x1=min(1536,int(max(p[0] for p in pp))+2);y0=max(0,int(min(p[1] for p in pp)));y1=min(1024,int(max(p[1] for p in pp))+2)
   if alpha[y0:y1,x0:x1].max()<.9:dead.append(face)
  bmesh.ops.delete(bm,geom=dead,context='FACES_ONLY');bm.to_mesh(ob.data);bm.free()
 return {'transparent_grid_removed':True}

def finalize_contacts_and_layers():
 # Coplanar arm/torso overlap was producing black rasterization wedges, even
 # where the garment remained connected. Semantic depth order solves that cause.
 for a in ACTORS.values():
  ob=a['skin'];names={g.index:g.name for g in ob.vertex_groups}
  for v in ob.data.vertices:
   z=sum(g.weight*(.018 if names[g.group].endswith('hand') else .013 if names[g.group].endswith('forearm') else .006 if names[g.group].endswith('upperarm') else 0) for g in v.groups);v.co.z=z
   if ob.data.shape_keys:
    for key in ob.data.shape_keys.key_blocks:key.data[v.index].co.z=z
 # Restore undistorted hand proportions, then stage the case around the actual grip.
 animate('unveiling Gyokeres');a=ACTORS['unveiling Gyokeres'];s=a['s'];bpy.context.window.scene=s;C=a['C'];bag=bpy.data.objects['B01 Gyokeres travel bag'];s.frame_set(26);ground=bag.location.copy();bag.animation_data_clear()
 for f in range(1,40):
  s.frame_set(f);dip=-.078*smooth((f-8)/18)*(1-smooth((f-27)/12))
  for k,ob in C.items():
   if any(k.endswith(t) for t in ['ankle','toe']):continue
   ob.location.y+=dip*(.4 if k.endswith('knee') else 1);ob.keyframe_insert(data_path='location',frame=f)
 s.frame_set(26);bpy.context.view_layer.update();grip=a['root'].matrix_world@(C['Lwrist'].location.lerp(C['Lfinger'].location,.42));ground.x=grip.x;handle_height=grip.y-ground.y
 handle=next(o for o in bag.children_recursive if o.name.startswith('Bag handle'));points=handle.data.splines[0].points;oldmax=max(p.co.y for p in points)
 for p in points:
  if p.co.y>.91:p.co.y=.9+(p.co.y-.9)*(handle_height-.9)/(oldmax-.9)
 for f in range(1,433):
  s.frame_set(f);bpy.context.view_layer.update()
  if f<=26:
   grip=a['root'].matrix_world@(C['Lwrist'].location.lerp(C['Lfinger'].location,.42));bag.location=(grip.x,grip.y-handle_height,ground.z)
  else:bag.location=ground
  bag.keyframe_insert(data_path='location',frame=f)
 for ob in [bag,*C.values()]:
  for fc in curves(ob):
   for kp in fc.keyframe_points:kp.interpolation='LINEAR'
 return {'prop':'extended travel-case handle meets palm; hand length preserved','layering':'hand in front of forearm, forearm in front of torso'}
