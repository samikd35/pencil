"""Film-specific Ferguson action, authored in visible Blender in short batches.
Fitted rigs carry the acting. Matching drawings cover changes of silhouette.
"""
import bpy,math,json,ast,sys
import numpy as np
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v006';A=V/'assets/ferguson-actions-v002'
sys.path.insert(0,str(V.parents[3]/'pipeline'))
from pose_geometry import two_bone_joint
ns={'__file__':str(V/'scripts/build_narrator_room_v005.py')};exec(compile(Path(ns['__file__']).read_text(),ns['__file__'],'exec'),ns)
BOX=ns['box'];KEY=ns['key'];ROOM='S002 / Narrator room / shared v005'
# Explicit source-drawing joints; points are measured in sheet pixels.
OLD={3:dict(hip=(278,771),neck=(282,588),head=(281,510),Ls=(192,606),Le=(117,578),Lw=(81,520),Lf=(71,480),Rs=(365,612),Re=(432,575),Rw=(484,525),Rf=(507,495),La=(177,971),Ra=(386,971)),4:dict(hip=(796,772),neck=(763,607),head=(750,526),Ls=(672,627),Le=(609,631),Lw=(618,558),Lf=(630,527),Rs=(836,629),Re=(912,648),Rw=(971,672),Rf=(1000,688),La=(712,958),Ra=(946,979)),5:dict(hip=(1262,786),neck=(1293,614),head=(1290,537),Ls=(1205,632),Le=(1328,618),Lw=(1433,584),Lf=(1485,586),Rs=(1341,666),Re=(1356,719),Rw=(1378,760),Rf=(1387,772),La=(1131,951),Ra=(1321,975))}
NEW={0:dict(hip=(326,338),neck=(333,211),head=(326,133),Ls=(247,218),Le=(189,269),Lw=(215,305),Lf=(236,322),Rs=(406,221),Re=(442,269),Rw=(411,304),Rf=(396,324),La=(216,466),Ra=(421,465)),1:dict(hip=(775,299),neck=(775,174),head=(772,101),Ls=(672,178),Le=(639,230),Lw=(659,265),Lf=(677,285),Rs=(866,179),Re=(900,230),Rw=(871,263),Rf=(853,283),La=(676,466),Ra=(883,465)),2:dict(hip=(1230,288),neck=(1234,137),head=(1224,69),Ls=(1138,158),Le=(1077,198),Lw=(1062,153),Lf=(1054,118),Rs=(1321,161),Re=(1367,194),Rw=(1414,163),Rf=(1442,150),La=(1125,466),Ra=(1329,465))}
BONES={'torso':('hip','neck'),'head':('neck','head'),'L upper arm':('Ls','Le'),'L forearm':('Le','Lw'),'L hand':('Lw','Lf'),'R upper arm':('Rs','Re'),'R forearm':('Re','Rw'),'R hand':('Rw','Rf')}
SHEETS={};ACTORS={}

def new_scenes():
 for sid in ['N04_meltdown','N04_tap']:
  old=bpy.data.scenes['S002_v005_'+sid];name='S002_v006_'+sid;assert name not in bpy.data.scenes
  s=bpy.data.scenes.new(name);s.collection.children.link(bpy.data.collections[ROOM]);s.world=old.world;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=8;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_end=old.frame_end;s.view_settings.view_transform='Standard';s.view_settings.look='None';s['shot_id']=sid;s['stage']='Ferguson action candidate; not user approved'
  for ob in old.objects:
   if ob.type in ['CAMERA','LIGHT']:
    copy=ob.copy();copy.data=ob.data.copy();s.collection.objects.link(copy)
    if copy.type=='CAMERA':s.camera=copy
  if sid=='N04_meltdown':
   s.camera.location=(-.15,-3.4,2.1);s.camera.rotation_euler=(Vector((0,0,1.35))-s.camera.location).to_track_quat('-Z','Y').to_euler();KEY(s.camera.data,'lens',[(1,38),(5,38),(6,27),(168,27)])
   for layer in s.camera.data.animation_data.action.layers:
    for strip in layer.strips:
     for bag in strip.channelbags:
      for fc in bag.fcurves:
       for k in fc.keyframe_points:k.interpolation='CONSTANT'
  row=next(r for r in json.loads((V/'artifacts/animation-v003/edit.json').read_text()) if r['id']==sid);seq=s.sequence_editor_create();q=seq.strips.new_sound('Approved mix / '+sid,str(V/'artifacts/opening-v002/mix-premaster.wav'),channel=1,frame_start=2-row['start_frame']);q.frame_offset_start=row['start_frame']-1;q.frame_final_duration=row['frames'];s.render.use_sequencer=False
 ns['show'](bpy.data.scenes['S002_v006_N04_meltdown'])
 return {'created':['S002_v006_N04_meltdown','S002_v006_N04_tap']}

def load_sheet(name,path,count,rows):
 im=bpy.data.images.load(str(path),check_existing=True);im.pack();W,H=im.size;a=np.empty(W*H*4,np.float32);im.pixels.foreach_get(a);alpha=a.reshape(H,W,4)[::-1,:,3]
 tree=ast.parse((V/'scripts/build_chase_v001.py').read_text());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='components');source=ast.get_source_segment((V/'scripts/build_chase_v001.py').read_text(),node).replace('len(big)==8','len(big)==expected').replace('[a,y,b,y+1,0]','[a,y,b,y+1,0,[]]').replace('g[4]+=b-a','g[4]+=b-a;g[5].append((y,a,b))').replace('return sorted(big[:4],key=lambda g:g[0])+sorted(big[4:],key=lambda g:g[0])','return sum([sorted(big[i*expected//rows:(i+1)*expected//rows],key=lambda g:g[0]) for i in range(rows)],[])');env={'np':np,'expected':count,'rows':rows};exec(source,env);boxes=env['components'](alpha>.95)
 data=np.zeros((H,W,4),np.float32);data[:,:,3]=1
 for i,b in enumerate(boxes):
  for y,x0,x1 in b[5]:data[y,x0:x1,:3]=(i+1)/count
 mask=bpy.data.images.new(name+' / isolation',width=W,height=H);mask.colorspace_settings.name='Non-Color';mask.pixels.foreach_set(data[::-1].ravel());mask.pack();mats=[]
 for i in range(count):
  m=bpy.data.materials.new(name+' / '+str(i));m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links;t=n.new('ShaderNodeTexImage');t.image=im;mt=n.new('ShaderNodeTexImage');mt.image=mask;mt.interpolation='Closest';q=n.new('ShaderNodeMath');q.operation='COMPARE';q.inputs[1].default_value=(i+1)/count;q.inputs[2].default_value=.01;l.new(mt.outputs[0],q.inputs[0]);e=n.new('ShaderNodeEmission');l.new(t.outputs['Color'],e.inputs[0]);tr=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');l.new(q.outputs[0],mix.inputs[0]);l.new(tr.outputs[0],mix.inputs[1]);l.new(e.outputs[0],mix.inputs[2]);out=n.new('ShaderNodeOutputMaterial');l.new(mix.outputs[0],out.inputs[0]);mats.append(m)
 SHEETS[name]=(W,H,boxes,mats)

def actor(sid,name,sheet,cell,points,unit=.0045):
 s=bpy.data.scenes['S002_v006_'+sid];ns['show'](s);W,H,boxes,mats=SHEETS[sheet];x0,y0,x1,y1=boxes[cell][:4];cx=points['hip'][0];cy=y1-1
 root=bpy.data.objects.new(name,None);s.collection.objects.link(root);root.rotation_euler.x=math.pi/2;root.location.z=.018
 xy=lambda p:Vector(((p[0]-cx)*unit,(cy-p[1])*unit,0));rest={k:xy(v) for k,v in points.items()};controls={}
 for name_,p in rest.items():o=bpy.data.objects.new(name+' / '+name_,None);s.collection.objects.link(o);o.parent=root;o.location=p;controls[name_]=o
 nx,ny=64,108;verts=[];uvs=[];pixels=[];faces=[]
 for j in range(ny+1):
  py=y0+(y1-y0)*j/ny
  for i in range(nx+1):px=x0+(x1-x0)*i/nx;verts.append(tuple(xy((px,py))));pixels.append((px,py));uvs.append((px/W,1-py/H))
 for j in range(ny):
  for i in range(nx):q=j*(nx+1)+i;faces.extend([(q,q+1,q+nx+2),(q,q+nx+2,q+nx+1)])
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.materials.append(mats[cell]);uv=mesh.uv_layers.new()
 for loop in mesh.loops:uv.data[loop.index].uv=uvs[loop.vertex_index]
 skin=bpy.data.objects.new(name+' / continuous skin',mesh);s.collection.objects.link(skin);skin.parent=root
 ad=bpy.data.armatures.new(name+' binding');arm=bpy.data.objects.new(ad.name,ad);s.collection.objects.link(arm);arm.parent=root
 bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);bpy.context.view_layer.objects.active=arm;bpy.ops.object.mode_set(mode='EDIT')
 for n,(a,b) in BONES.items():e=ad.edit_bones.new(n);e.head=rest[a];e.tail=rest[b]
 e=ad.edit_bones.new('support');e.head=rest['hip'];e.tail=rest['hip']+Vector((0,.1,0));bpy.ops.object.mode_set(mode='OBJECT')
 for n,(a,b) in BONES.items():
  c=arm.pose.bones[n].constraints.new('COPY_LOCATION');c.target=controls[a];c=arm.pose.bones[n].constraints.new('STRETCH_TO');c.target=controls[b];c.rest_length=(rest[b]-rest[a]).length;c.volume='NO_VOLUME';c.bulge=0
 groups={n:skin.vertex_groups.new(name=n) for n in [*BONES,'support']}
 def dist(p,a,b):d=b-a;return (p-(a+d*max(0,min(1,(p-a).dot(d)/d.length_squared)))).length
 for v,(px,py) in zip(mesh.vertices,pixels):
  if py>points['hip'][1]+20:weights=[('support',1)]
  elif py<points['neck'][1]-12 and abs(px-points['head'][0])<(120 if unit<.003 else 78) and not (unit<.003 and points['head'][0]>1000 and px>1230 and py<200):weights=[('head',1)]
  else:
   side='L' if px<cx else 'R';names=['torso','L upper arm','L forearm','L hand','R upper arm','R forearm','R hand']
   if py<points['neck'][1]+12 and abs(px-points['head'][0])<80:names=['head','torso']
   ds=sorted((max(0,dist(v.co,rest[BONES[n][0]],rest[BONES[n][1]])-(.12 if n=='torso' else 0)),n) for n in names)[:2];vals=[math.exp(-d*d/.008) for d,n in ds];total=sum(vals);weights=[(n,w/total) for (d,n),w in zip(ds,vals)] if total>1e-25 else [(ds[0][1],1)]
   if py>points['hip'][1]-16:t=min(1,(py-points['hip'][1]+16)/36);weights=[(n,w*(1-t)) for n,w in weights]+[('support',t)]
  for n,w in weights:groups[n].add([v.index],w,'REPLACE')
 mod=skin.modifiers.new('Fitted gesture joints','ARMATURE');mod.object=arm;mod.use_deform_preserve_volume=True
 a={'root':root,'skin':skin,'arm':arm,'controls':controls,'rest':rest,'unit':unit,'points':points,'pixels':pixels,'cx':cx,'cy':cy};ACTORS[name]=a;root['method']='Shot-specific fitted gesture rig; source substitution only for silhouette/view changes';return a

def exposure(a,start,end,total):
 for ob in [a['skin']]:
  for f,hidden in [(1,start>1),(max(1,start-1),True),(start,False),(end,False),(end+1,True)]:
   if f==1 and start==1:hidden=False
   for prop in ['hide_render','hide_viewport']:setattr(ob,prop,hidden);ob.keyframe_insert(data_path=prop,frame=f)

def sample(keys,f):
 if f<=keys[0][0]:return keys[0][1:]
 for a,b in zip(keys,keys[1:]):
  if a[0]<=f<=b[0]:t=(f-a[0])/(b[0]-a[0]);t=t*t*(3-2*t);return tuple(x+(y-x)*t for x,y in zip(a[1:],b[1:]))
 return keys[-1][1:]

def perform(a,start,end,beats):
 r=a['rest'];ctl=a['controls']
 def rotate(v,t):return Vector((math.cos(t)*v.x-math.sin(t)*v.y,math.sin(t)*v.x+math.cos(t)*v.y,0))
 for f in range(start,end+1):
  lean,left,right,head=sample(beats,f);hip=r['hip'];p={n:hip+rotate(v-hip,lean) for n,v in r.items()};p['hip']=hip;p['head']=p['neck']+rotate(r['head']-r['neck'],head)
  for side,angle in [('L',left),('R',right)]:
   for aa,bb,t in [('s','e',lean+angle*.35),('e','w',lean+angle),('w','f',lean+angle*.8)]:p[side+bb]=p[side+aa]+rotate(r[side+bb]-r[side+aa],t)
  for n,o in ctl.items():o.location=p[n];o.keyframe_insert(data_path='location',frame=f)
 for o in ctl.values():
  if o.animation_data:
   for layer in o.animation_data.action.layers:
    for strip in layer.strips:
     for bag in strip.channelbags:
      for fc in bag.fcurves:
       for k in fc.keyframe_points:k.interpolation='LINEAR'

CONTACT={0:dict(hip=(473,549),neck=(414,414),head=(366,307),Ls=(293,415),Le=(214,558),Lw=(133,707),Lf=(87,774),Rs=(596,331),Re=(657,426),Rw=(633,537),Rf=(650,598),La=(325,877),Ra=(719,889)),1:dict(hip=(1183,553),neck=(1226,292),head=(1181,173),Ls=(1092,309),Le=(1325,245),Lw=(1290,129),Lf=(1264,55),Rs=(1308,351),Re=(1356,440),Rw=(1412,532),Rf=(1448,576),La=(908,894),Ra=(1303,930))}

def register(a,start,end,neck_keys):
 """Register torso trajectory; bounded lower support follows the accepted Bruno principle."""
 skin=a['skin'];s=next(s for s in bpy.data.scenes if skin.name in s.objects and s.name.startswith('S002_v006_'));basis=skin.shape_key_add(name='Basis') if not skin.data.shape_keys else skin.data.shape_keys.key_blocks[0];vertical=skin.data.shape_keys.key_blocks.get('Lower support vertical compensation') or skin.shape_key_add(name='Lower support vertical compensation');horizontal=skin.data.shape_keys.key_blocks.get('Lower support horizontal compensation') or skin.shape_key_add(name='Lower support horizontal compensation');vertical.slider_min=-1;horizontal.slider_min=-1
 h=a['rest']['hip'].y
 for b,v,x in zip(basis.data,vertical.data,horizontal.data):
  w=max(0,min(1,(h+.05-b.co.y)/max(h-.10,.1)));v.co=b.co.copy();x.co=b.co.copy();v.co.y-=w;x.co.x-=w
 for f in range(start,end+1):
  s.frame_set(f);nx,nz=sample(neck_keys,f);neck=a['controls']['neck'].location;dx=nx-neck.x;dz=nz-neck.y
  assert abs(dz)<.32 and abs(dx)<.45,(a['root'].name,f,dx,dz)
  a['root'].location=(dx,0,dz+.018);a['root'].keyframe_insert(data_path='location',frame=f);vertical.value=dz;vertical.keyframe_insert(data_path='value',frame=f);horizontal.value=dx;horizontal.keyframe_insert(data_path='value',frame=f)
 return a

def build_rise():
 made=[]
 for i,start,end,z0,z1 in [(0,1,7,1.359,1.39),(1,8,13,1.43,1.58),(2,14,19,1.62,1.78)]:
  a=actor('N04_meltdown','Ferguson / rise '+str(i),'breakdowns',i,NEW[i]);perform(a,start,end,[(start,-.02,-.03,.025,0),(end,.015,.06,-.04,-.01)]);register(a,start,end,[(start,0,z0),(end,0,z1)]);exposure(a,start,end,168);made.append(a['root'].name)
 return {'rise_actors':made}

def mouth(a):
 import subprocess
 audio=json.loads((V/'artifacts/opening-v002/full-audio-plan.json').read_text());file=audio['assets']['meltdown']['path'];raw=subprocess.check_output(['/opt/homebrew/bin/ffmpeg','-v','error','-i',file,'-ac','1','-ar','48000','-f','f32le','-']);samples=np.frombuffer(raw,np.float32);rms=np.array([np.sqrt(np.mean(samples[i:i+2000]**2)) for i in range(0,len(samples),2000)]);levels=np.clip(rms/max(np.percentile(rms,85),1e-6),0,1)
 ob=a['skin'];basis=ob.shape_key_add(name='Basis') if not ob.data.shape_keys else ob.data.shape_keys.key_blocks[0];shape=ob.shape_key_add(name='Bounded jaw articulation')
 for b,v,(px,py) in zip(basis.data,shape.data,a['pixels']):
  dx=abs(px-286)/23;dy=abs(py-545)/24;w=max(0,min(1,(1.4-dx)/.4))*max(0,min(1,(1.4-dy)/.4));v.co.y+=(py-545)*a['unit']*.55*w
 for f in range(20,143):shape.value=1-(float(levels[f-3]) if 0<=f-3<len(levels) else 0);shape.keyframe_insert(data_path='value',frame=f)

def build_pickup():
 load_sheet('contacts',A/'pickup-and-release.png',2,1)
 a=actor('N04_meltdown','Ferguson / collect notes','contacts',0,CONTACT[0],.0028);perform(a,143,168,[(143,-.06,-.34,.05,.02),(151,-.02,-.46,.02,-.03),(156,0,-.56,0,-.025),(168,.035,-.65,0,0)]);register(a,143,168,[(143,-.04,1.62),(152,-.035,1.66),(156,-.02,1.69),(168,.00,1.74)]);exposure(a,143,168,168)
 return {'actor':a['root'].name}

def build_throw():
 actors=[]
 for label,sheet,cell,points,unit,start,end in [('windup','original',4,OLD[4],.0045,1,5),('elbow lead','contacts',1,CONTACT[1],.0028,6,9),('follow through','original',5,OLD[5],.0045,10,60)]:
  a=actor('N04_tap','Ferguson / '+label,sheet,cell,points,unit)
  if label=='windup':beats=[(1,-.035,.03,-.03,-.04),(5,.035,-.10,.03,.035)]
  elif label=='elbow lead':beats=[(6,.015,.04,0,.025),(9,.055,-.12,-.03,.01)]
  else:beats=[(10,.045,-.13,.02,.015),(15,.07,.035,-.04,.035),(23,.035,.025,-.02,.015),(34,.018,0,0,0),(60,.018,0,0,0)]
  perform(a,start,end,beats);register(a,start,end,[(start,0,1.80),(end,.025 if start==10 else 0,1.79)]);exposure(a,start,end,60);actors.append(a)
 # One native paper object takes over exactly at release and reaches the TV at the approved tap cue.
 s=bpy.data.scenes['S002_v006_N04_tap'];s.frame_set(10);bpy.context.view_layer.update();a=actors[-1];release=a['controls']['Lf'].matrix_world.translation.copy();target=Vector((3.345,-1.1,1.68));frames=10;T=frames/24;g=9.81;vz=(target.z-release.z+.5*g*T*T)/T
 # Faceted crumpled paper, built natively; source windup/mid-throw drawings hold the paper before release.
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.062,location=release);paper=bpy.context.object;paper.name='Ferguson / released notes';paper.data.materials.append(ns['mat']('Crumpled notes',(.82,.80,.72)))
 for i,v in enumerate(paper.data.vertices):v.co*=1+.14*math.sin(i*2.31)
 for f in range(1,61):
  hidden=f<10
  paper.hide_render=hidden;paper.hide_viewport=hidden;paper.keyframe_insert(data_path='hide_render',frame=f);paper.keyframe_insert(data_path='hide_viewport',frame=f)
  if f<10:pos=release
  elif f<=20:
   t=(f-10)/24;u=t/T;pos=release.lerp(target,u);pos.z=release.z+vz*t-.5*g*t*t
  else:
   t=(f-20)/24;pos=Vector((target.x-min(.19,t*.35),target.y+.04*min(t,1),max(.074,target.z-.5*g*t*t)))
  paper.location=pos;paper.rotation_euler=(f*.31,f*.17,f*.28) if pos.z>.074 else (1.1,.5,.3);paper.keyframe_insert(data_path='location',frame=f);paper.keyframe_insert(data_path='rotation_euler',frame=f)
 for layer in paper.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path.startswith('hide_') else 'LINEAR'
 s['paper_release_frame']=10;s['paper_contact_frame']=20;s['release_world']=list(release);s['paper_target']=list(target)
 return {'throw_actors':[a['root'].name for a in actors],'paper':paper.name,'release':list(release),'hit':list(target),'hit_frame':20}

def finish_contacts():
 s=bpy.data.scenes['S002_v006_N04_meltdown'];a=ACTORS['Ferguson / collect notes'];s.frame_set(143);bpy.context.view_layer.update();point=a['controls']['Lf'].matrix_world.translation.copy();point+=a['root'].matrix_world.to_3x3()@Vector((.0112,-.0112,0))
 room=bpy.data.collections[ROOM];BOX(room,'Room / notes side table',(point.x,point.y,point.z-.12),(.52,.48,.10),(.105,.054,.03));BOX(room,'Room / side table leg',(point.x,point.y,(point.z-.17)/2),(.14,.14,point.z-.17),(.065,.04,.025))
 # Earlier coverage establishes the crumpled notes at this location; the pickup drawing owns them from contact onward.
 for shot in ['N02','N03','N04_dark','N04_reveal','N04_meltdown']:
  sc=bpy.data.scenes[('S002_v006_' if shot=='N04_meltdown' else 'S002_v005_')+shot];bpy.context.window.scene=sc
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.062,location=point);p=bpy.context.object;p.name=sc.name+' / waiting notes';p.data.materials.append(ns['mat']('Crumpled notes',(.82,.80,.72)))
  if shot=='N04_meltdown':
   for f,hidden in [(1,False),(142,False),(143,True)]:
    for prop in ['hide_render','hide_viewport']:setattr(p,prop,hidden);p.keyframe_insert(data_path=prop,frame=f)
 # Cut on the reach to make the hand/contact and continuing set geography readable.
 cam=s.camera
 for f,loc,target,lens in [(1,(-.15,-3.4,2.1),(0,0,1.35),38),(5,(-.15,-3.4,2.1),(0,0,1.35),38),(6,(-.15,-3.4,2.1),(0,0,1.35),27),(142,(-.15,-3.4,2.1),(0,0,1.35),27),(143,(-2.8,-3.15,2.0),(.45,-.25,1.2),27),(168,(-2.8,-3.15,2.0),(.45,-.25,1.2),27)]:
  cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens;cam.keyframe_insert(data_path='location',frame=f);cam.keyframe_insert(data_path='rotation_euler',frame=f);cam.data.keyframe_insert(data_path='lens',frame=f)
 for ob in [cam,cam.data]:
  for layer in ob.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT'
 # Contact uses the paper's evaluated surface, not its centre passing through the screen.
 tap=bpy.data.scenes['S002_v006_N04_tap'];bpy.context.window.scene=tap;tap.frame_set(20);p=bpy.data.objects['Ferguson / released notes'];rot=p.rotation_euler.to_matrix();extent=max((rot@v.co).x for v in p.data.vertices);release=Vector(tap['release_world']);target=Vector((3.344-extent,-1.1,1.68));T=10/24;g=9.81;vz=(target.z-release.z+.5*g*T*T)/T
 for f in range(10,61):
  if f<=20:t=(f-10)/24;pos=release.lerp(target,t/T);pos.z=release.z+vz*t-.5*g*t*t
  else:t=(f-20)/24;pos=Vector((target.x-min(.19,t*.35),target.y+.04*min(t,1),max(.074,target.z-.5*g*t*t)))
  p.location=pos;p.keyframe_insert(data_path='location',frame=f)
 m=p.data.materials[0];m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(.85,.82,.73,1);out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],out.inputs[0]);tap['paper_target']=list(target);tap['paper_contact_plane_x']=3.344;s['pickup_world']=list(point);s['pickup_frame']=143
 return {'pickup':list(point),'paper_surface_contact_x':3.344,'paper_centre_at_impact':list(target)}

def build_performance():
 new_scenes();load_sheet('original',V/'assets/film-acting-v001/ferguson.png',6,2);load_sheet('breakdowns',A/'rise-and-throw.png',6,2)
 a=actor('N04_meltdown','Ferguson / standing outrage','original',3,OLD[3]);exposure(a,20,142,168);perform(a,20,142,[(20,-.018,.04,-.03,0),(32,.035,-.09,.12,-.06),(47,.012,.025,-.02,-.02),(62,-.025,.07,-.06,.04),(79,-.06,-.08,.13,-.10),(94,-.018,-.19,.18,-.11),(112,.05,.02,-.12,.025),(130,.012,.06,-.05,.01),(142,.01,.04,-.03,.015)])
 build_rise();mouth(a);build_pickup();build_throw();return finish_contacts()
