"""Film-specific batch authoring. Whole drawings, native props and keyed performance.

Accepted CP01/Pep movies remain exact inputs. This is a first animation pass,
not a claim of completed performance polish or final sound design.
"""
import bpy,math,json,sys,ast,subprocess
from fractions import Fraction
import numpy as np
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v004';A=V/'assets/film-acting-v001'
sys.path.insert(0,str(V.parents[3]/'pipeline'));from checkpoints import require_checkpoint
for rev,stage in [('CP01-v002','staging'),('CP03_pep-v002','staging'),('opening-v002','sound'),('opening-v002','animatic')]:require_checkpoint(V,rev,stage)
O.mkdir(exist_ok=True);(O/'clips').mkdir(exist_ok=True);(O/'frames').mkdir(exist_ok=True)
edit=json.loads((V/'artifacts/animation-v003/edit.json').read_text());audio=json.loads((V/'artifacts/opening-v002/full-audio-plan.json').read_text())
events={x['id']:x['events'] for x in audio['shots']};SCENE=None;MATS={};sheets={};reports=[]
INK='#202a33'
# Reuse native drawing helpers, without invoking the historical rough-board builder.
code=ast.parse((V/'scripts/build_boards_v001.py').read_text())
exec(compile(ast.Module(body=[n for n in code.body if isinstance(n,ast.FunctionDef) and n.name in ['obj','poly','rect','line','disc','text']],type_ignores=[]),'existing drawing helpers','exec'))
INK='#202a33';WHITE='#fffaf0';RED='#ce3843';GOLD='#e8b947'
def material(color):
 if color not in MATS:
  rgb=[int(color[i:i+2],16)/255 for i in (1,3,5)];rgb=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
  m=bpy.data.materials.new('Film / '+color);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(*rgb,1);out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],out.inputs[0]);MATS[color]=m
 return MATS[color]
def empty(name,x=0,y=0,z=0):
 ob=bpy.data.objects.new(SCENE.name+' / '+name,None);SCENE.collection.objects.link(ob);ob.location=(x,y,z);return ob
def keyed(ob,path,values,kind='BEZIER'):
 for f,value in values:
  setattr(ob,path,value);ob.keyframe_insert(data_path=path,frame=f)
 ad=ob.animation_data
 if ad and ad.action:
  for layer in ad.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      if fc.data_path==path:
       for k in fc.keyframe_points:k.interpolation=kind;k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
 return ob
def move(ob,rows,kind='BEZIER'):return keyed(ob,'location',rows,kind)
def group(name,objects,x=0,y=0,z=0):
 p=empty(name,x,y,z)
 for ob in objects:ob.parent=p
 return p
def label(body,x,y,size=.4,color=WHITE,z=4):
 ob=text(body,x,y,size,color,z);ob.data.align_x='CENTER';return ob
def new_scene(row,bg='#d9e7ee'):
 global SCENE
 name='S002_fullmotion_'+row['id'];assert name not in bpy.data.scenes
 s=bpy.data.scenes.new(name);SCENE=s;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=8;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=row['frames'];s.view_settings.view_transform='Standard';s.view_settings.look='None';s.render.use_sequencer=False
 w=bpy.data.worlds.new(name);w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(.05,.05,.05,1);s.world=w
 d=bpy.data.cameras.new(name);d.type='ORTHO';d.ortho_scale=16;c=bpy.data.objects.new(name+' camera',d);s.collection.objects.link(c);c.location=(0,0,30);s.camera=c
 rect('backdrop',-20,-12,40,24,bg,-5);s['shot_id']=row['id'];s['stage']='First full-film animation pass; performance polish pending'
 return s
def camera(x=0,y=0,width=16):SCENE.camera.location=(x,y,30);SCENE.camera.data.ortho_scale=width
def stadium(training=False):
 rect('stand',-18,-.4,36,5.0,'#a9b6bd',-4)
 verts=[];faces=[]
 for r in range(4):
  for i in range(62):
   x=-18+i*.59+(r%2)*.2;y=.3+r*.78;start=len(verts)
   verts.extend([(x+.12*math.cos(j*math.tau/8),y+.16*math.sin(j*math.tau/8),-3.8) for j in range(8)]);faces.append(tuple(range(start,start+8)))
 mesh=bpy.data.meshes.new('crowd');mesh.from_pydata(verts,[],faces);mesh.materials.append(material('#6d7c89'));ob=bpy.data.objects.new(SCENE.name+' crowd',mesh);SCENE.collection.objects.link(ob)
 rect('fascia',-18,-.5,36,.48,'#a6313d',-3.5);rect('pitch',-20,-12,40,11.8,'#709e5d',-3)
 for i in range(-3,4):poly('grass stripe',[(i*6,-10),(i*6+3,-10),(i*4+3,-.2),(i*4,-.2)],'#7fa96a',-2.9)
 line('touchline',[(-18,-3.6),(18,-3.6)],WHITE,.035,-2.5)
 if training:
  for x in [-8,-5,5,8]:
   line('training fence',[(x,-.4),(x,5)],'#73848b',.025,-3.4)
  label('ARSENAL',5,.2,.4,WHITE,-3.3)
def goal(x=1.7,y=-2.7,w=5.4,h=4.1):
 obs=[rect('net panel',x,y,w,h,'#8aa38b',-2.5)]
 for i in range(1,15):obs.append(line('net string',[(x+i*w/15,y),(x+i*w/15,y+h)],'#b6c5b5',.013,-2.4))
 for i in range(1,9):obs.append(line('net string',[(x,y+i*h/9),(x+w,y+i*h/9)],'#b6c5b5',.013,-2.4))
 obs.append(line('goalpost',[(x,y),(x,y+h),(x+w,y+h),(x+w,y)],WHITE,.065,-2.2));return group('goal',obs)
def flag(x,y,height=2.7):
 return group('corner flag',[line('pole',[(0,0),(0,height)],WHITE,.035,.1),poly('flag',[(0,height),(.7,height-.2),(0,height-.6)],RED,.2)],x,y)
def ball(x,y,r=.18):
 obs=[disc('ball',0,0,r,WHITE,3),disc('ball centre',0,0,r*.39,INK,3.01)]
 for i in range(5):a=i*math.tau/5;obs.append(disc('ball patch',r*.76*math.cos(a),r*.76*math.sin(a),r*.18,INK,3.02))
 return group('ball path',obs,x,y)
def arc(ob,start,end,a,b,height):
 vals=[]
 for f in range(start,end+1):
  u=(f-start)/(end-start);vals.append((f,(a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u+4*height*u*(1-u),0)))
 move(ob,vals,'LINEAR');keyed(ob,'rotation_euler',[(start,(0,0,0)),(end,(0,0,-8))],'LINEAR')
def effect(x,y,frame,color=WHITE):
 obs=[]
 for i in range(9):a=i*math.tau/9;obs.append(line('impact',[(.24*math.cos(a),.24*math.sin(a)),(.53*math.cos(a),.53*math.sin(a))],color,.025,5))
 root=group('impact burst',obs,x,y);keyed(root,'scale',[(1,(0,0,0)),(frame-1,(0,0,0)),(frame,(1,1,1)),(frame+5,(0,0,0))],'LINEAR')
 return root
def load_sheet(name,count,rows=2):
 im=bpy.data.images.load(str(A/(name+'.png')),check_existing=True);im.pack();W,H=im.size;buf=np.empty(W*H*4,np.float32);im.pixels.foreach_get(buf);alpha=buf.reshape(H,W,4)[::-1,:,3]
 source=(V/'scripts/build_chase_v001.py').read_text();tree=ast.parse(source);node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='components');src=ast.get_source_segment(source,node).replace('len(big)==8','len(big)==expected').replace("return sorted(big[:4],key=lambda g:g[0])+sorted(big[4:],key=lambda g:g[0])","return sum([sorted(big[i*expected//row_count:(i+1)*expected//row_count],key=lambda g:g[0]) for i in range(row_count)],[])")
 src=src.replace('[a,y,b,y+1,0]', '[a,y,b,y+1,0,[]]').replace('g[4]+=b-a','g[4]+=b-a;g[5].append((y,a,b))')
 env={'np':np,'expected':count,'row_count':rows};exec(src,env);boxes=env['components'](alpha>.95)
 # One native label texture isolates connected drawings; bounding rectangles alone
 # can include a neighbouring hand or boot where sheet rows overlap.
 labels=np.zeros((H,W,4),np.float32);labels[:,:,3]=1
 for cell,box in enumerate(boxes):
  for yy,aa,bb in box[5]:labels[yy,aa:bb,:3]=(cell+1)/count
 mask=bpy.data.images.new(name+' component labels',width=W,height=H);mask.colorspace_settings.name='Non-Color';mask.pixels.foreach_set(labels[::-1].ravel());mask.pack()
 mats=[]
 for variant in range(count*2):
  cell,shadow=divmod(variant,2)
  m=bpy.data.materials.new('Film artwork / '+name+(' shadow' if shadow else ''));m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links;t=n.new('ShaderNodeTexImage');t.image=im;t.interpolation='Linear';e=n.new('ShaderNodeEmission')
  if shadow:e.inputs[0].default_value=(.005,.009,.014,1)
  else:l.new(t.outputs['Color'],e.inputs[0])
  tr=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');q=n.new('ShaderNodeMath');q.operation='COMPARE';q.inputs[1].default_value=(cell+1)/count;q.inputs[2].default_value=.01;mt=n.new('ShaderNodeTexImage');mt.image=mask;mt.interpolation='Closest';l.new(mt.outputs['Color'],q.inputs[0]);l.new(q.outputs[0],mix.inputs[0]);l.new(tr.outputs[0],mix.inputs[1]);l.new(e.outputs[0],mix.inputs[2]);out=n.new('ShaderNodeOutputMaterial');l.new(mix.outputs[0],out.inputs[0]);mats.append(m)
 sheets[name]=(W,H,boxes,mats)
# Anatomical horizontal registrations and mouth positions, inspected in each source.
LANDMARKS={
 'arteta':dict(x=[291,751,1237,288,758,1253],mouth=[(308,88),(775,101),(1255,95),(308,586),(781,596),(1236,601)],base=490),
 'gyokeres':dict(x=[260,830,1210,251,768,1255],mouth=[(278,88),(843,89),(1233,90),(261,581),None,(1271,581)],base=490),
 'ferguson':dict(x=[303,773,1293,275,750,1292],mouth=[None,(789,114),(1306,126),(288,545),(766,573),(1309,573)],base=550),
 'officials':dict(x=[222,579,990,1348,224,591,958,1337],mouth=[(247,132),(605,125),(1013,139),(1363,115),(193,777),(610,744),(976,746),(1340,780)],base=575),
 'support':dict(x=[313,810,1309,280,822,1313],mouth=[(277,194),(781,251),(1278,105),(270,559),(800,586),(1299,600)],base=520),
 'football':dict(x=[280,571,945,1373,264,576,983,1353],mouth=[None,None,None,None,None,None,None,None],base=455),
 'wall':dict(x=[],mouth=[None]*9,base=510),
 'saka-contact':dict(x=[660],mouth=[None],base=1067)}
def actor(sheet,cells,x,y,height=4.7,z=1,shadow=False,anchors=None):
 W,H,boxes,mats=sheets[sheet];lm=LANDMARKS[sheet];unit=height/lm['base'];root=empty(sheet+' actor',x,y,z);root['pose']=0;root.id_properties_ui('pose').update(min=0,max=len(cells)-1,soft_min=0,soft_max=len(cells)-1);root['mouth_close']=0.;root['beat']=0.;parts=[]
 for pi,cell in enumerate(cells):
  x0,y0,x1,y1,_=boxes[cell][:5];x0=max(0,x0-3);y0=max(0,y0-3);x1=min(W,x1+3);y1=min(H,y1+3)
  cx=(lm['x'][cell] if lm['x'] else (x0+x1)/2);cy=y1-3
  if anchors:cx,cy=anchors[pi]
  nx,ny=60,100;verts=[];uvs=[];pixels=[];faces=[]
  for j in range(ny+1):
   py=y0+(y1-y0)*j/ny
   for k in range(nx+1):
    px=x0+(x1-x0)*k/nx;verts.append(((px-cx)*unit,(cy-py)*unit,0));uvs.append((px/W,1-py/H));pixels.append((px,py))
  for j in range(ny):
   for k in range(nx):a=j*(nx+1)+k;faces.append((a,a+1,a+nx+2,a+nx+1))
  me=bpy.data.meshes.new(root.name+' pose');me.from_pydata(verts,[],faces);me.materials.append(mats[cell*2+int(shadow)]);uv=me.uv_layers.new()
  for p in me.polygons:
   for lp in p.loop_indices:uv.data[lp].uv=uvs[me.loops[lp].vertex_index]
  ob=bpy.data.objects.new(root.name+' / pose '+str(pi),me);SCENE.collection.objects.link(ob);ob.parent=root
  for prop in ['hide_render','hide_viewport']:
   d=ob.driver_add(prop).driver;d.expression='pose != '+str(pi);v=d.variables.new();v.name='pose';v.type='SINGLE_PROP';v.targets[0].id=root;v.targets[0].data_path='["pose"]'
  ob.shape_key_add(name='Basis');mouth=lm['mouth'][cell]
  if mouth and not shadow:
   key=ob.shape_key_add(name='Mouth closure')
   for (px,py),p in zip(pixels,key.data):
    dx=abs(px-mouth[0])/20;dy=abs(py-mouth[1])/14
    if dx<1.6 and dy<1.6:
     w=min(1,max(0,(1.6-dx)/.6))*min(1,max(0,(1.6-dy)/.6));p.co.y+=(py-mouth[1])*unit*.85*w
   d=key.driver_add('value').driver;d.expression='close';v=d.variables.new();v.name='close';v.type='SINGLE_PROP';v.targets[0].id=root;v.targets[0].data_path='["mouth_close"]'
  beat=ob.shape_key_add(name='Acting accent')
  for b,p in zip(me.shape_keys.key_blocks['Basis'].data,beat.data):
   p.co=b.co.copy();w=max(0,min(1,(b.co.y-height*.48)/(height*.32)));p.co.y+=.035*w;p.co.x+=.015*w
  d=beat.driver_add('value').driver;d.expression='beat';v=d.variables.new();v.name='beat';v.type='SINGLE_PROP';v.targets[0].id=root;v.targets[0].data_path='["beat"]'
  parts.append(ob)
 root['asset']=sheet;root['cells']=json.dumps(cells);root['contact']='foot/baseline registration; complete coherent source artwork';return root
def pose(root,values):
 for f,value in values:root['pose']=value;root.keyframe_insert(data_path='["pose"]',frame=f)
 for layer in root.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     if fc.data_path=='["pose"]':
      for k in fc.keyframe_points:k.interpolation='CONSTANT'
VOICE_ENVELOPES={}
def speak(root,start,end):
 # ponytail: actual voice amplitude drives mouth closure; phoneme drawings remain polish.
 candidates=[c for c in audio['cues'] if c['shot']==SCENE['shot_id'] and c.get('stem')=='dialogue' and events[c['shot']][c['event']]+1==start]
 envelope=[]
 if candidates:
  filename=audio['assets'][candidates[0]['asset']]['path']
  if filename not in VOICE_ENVELOPES:
   raw=subprocess.check_output(['/opt/homebrew/bin/ffmpeg','-v','error','-i',filename,'-ac','1','-ar','48000','-f','f32le','-'])
   a=np.frombuffer(raw,np.float32);rms=np.array([np.sqrt(np.mean(a[i:i+2000]**2)) for i in range(0,len(a),2000)]);scale=max(float(np.percentile(rms,85)),1e-6);VOICE_ENVELOPES[filename]=np.clip(rms/scale,0,1).tolist()
  envelope=VOICE_ENVELOPES[filename]
 for f in range(1,SCENE.frame_end+1):
  local=f-start;level=envelope[local] if 0<=local<len(envelope) and f<=end else 0.
  root['mouth_close']=1-.90*level
  root['beat']=max(0,level-.65)*.6
  root.keyframe_insert(data_path='["mouth_close"]',frame=f);root.keyframe_insert(data_path='["beat"]',frame=f)
def talk_interval(shot,index=0):
 cues=[c for c in audio['cues'] if c['shot']==shot and c.get('stem')=='dialogue']
 if index>=len(cues):return (1,1)
 c=cues[index];start=events[shot][c['event']]+1;return start,min(SCENE.frame_end,start+round(float(Fraction(str(c['duration_seconds'])))*24))
def phone(x,y,gold=False):
 color=GOLD if gold else '#727d86';return group('telephone',[rect('phone base',-.7,-.15,1.4,.3,color,3),line('handset',[(-.65,.2),(-.4,.4),(.4,.4),(.65,.2)],color,.13,3.1)],x,y)
def room(front=False):
 rect('wall panels',-10,-6,20,12,'#152433',-4)
 for x in range(-10,11,2):rect('wood panel',x,-6,.04,12,'#203547',-3.8)
 rect('floor',-12,-5,24,1.7,'#182029',-3)
 chair=group('chair',[rect('back',-1.5,-.1,3,3.7,'#282833',.2),rect('seat',-1.7,-.3,3.4,.35,'#3f3540',.3)],-.7,-3.4)
 tx=5.4 if front else -4.8
 tv=group('television',[rect('TV case',-1.8,-1.0,3.6,2.3,'#080e16',.6),rect('TV picture',-1.6,-.82,3.2,1.9,'#547d42',.7),line('TV pitch',[(-1.4,-.5),(1.4,-.5),(1.4,.7),(-1.4,.7),(-1.4,-.5)],WHITE,.018,.8)],tx,.1)
 rect('desk',-4,-2.2,8,.3,'#7d5035',2.5);rect('desk fascia',-4,-3.4,8,1.2,'#47362d',2.4)
 lamp=group('desk lamp',[disc('lamp base',0,0,.35,GOLD,3),line('lamp stem',[(0,0),(0,1.45)],GOLD,.045,3),poly('lamp shade',[(-.65,1.35),(.65,1.35),(.38,1.8),(-.38,1.8)],'#235d4f',3.1)],2.7,-2.0)
 return lamp,tv

def truck(x=0):
 obs=[rect('truck box',-2,-2.1,7.0,4.1,'#eee9dd',1),rect('truck trim',-2,-2.15,7,.14,'#737d83',1.1),poly('cab',[(5,-2.1),(7.6,-2.1),(7.6,.5),(6.6,1.7),(5,1.7)],'#e3e4df',1.1),rect('cab window',5.3,-.05,1.75,1.3,'#5b7988',1.2)]
 for xx in [-.8,4.1,6.3]:
  obs += [disc('wheel',xx,-2.1,.55,INK,2),disc('hub',xx,-2.1,.23,'#84919a',2.1)]
 obs += [label('BOTTLE FC',1.45,.55,.73,'#164c35',2),label('ANNUAL DELIVERY',1.45,-.1,.3,'#164c35',2)]
 return group('bottle delivery truck',obs,x,-.85)
def trolley(x=0,y=-3.4):
 obs=[rect('cart platform',-1.3,0,3.2,.18,'#8d9a9f',2),rect('crate',-1.2,.25,1.9,1.25,RED,2.1),line('handle',[(.7,.1),(1.1,1.7),(1.7,1.7)],'#8d9a9f',.065,2.2),label('RUNNERS-UP',-.25,.72,.2,WHITE,2.3)]
 for xx in [-.9,.7,1.65]:obs.append(disc('trolley wheel',xx,-.02,.18,INK,2.4))
 for i in range(6):
  xx=-1+i*.29;obs += [line('medal ribbon',[(xx,1.48),(xx+.13,.7)],WHITE,.025,2.4),disc('silver medal',xx+.13,.66,.13,'#b9c3cd',2.5)]
 return group('medal trolley',obs,x,y)
def officials_office():
 rect('office wall',-12,-6,24,12,'#1a2b3d',-4)
 for x in [-6.5,-3.5,0]:
  for y in [.5,2.5]:
   rect('monitor',x,y,2.6,1.6,'#080f1b',-3.5);rect('monitor grass',x+.1,y+.1,2.4,1.4,'#416c48',-3.4);line('monitor pitch',[(x+.3,y+.3),(x+2.2,y+.3),(x+2.2,y+1.25),(x+.3,y+1.25),(x+.3,y+.3)],'#adbda9',.012,-3.3)
 label('VAR',5,2.2,1.0,WHITE,-3)
 rect('desk',-10,-3.8,20,1.5,'#3d4958',3);rect('desk top',-10,-2.35,20,.16,'#778391',3.1)
 grey=phone(-4.3,-2.1);gold=phone(3.5,-2.1,True)
 for x,body,color in [(-4.3,'PENDING','#869099'),(3.5,'MIKEL',GOLD)]:
  rect('phone label',x-.95,-2.8,1.9,.43,color,4);label(body,x,-2.68,.26,INK,4.1)
 return grey,gold
def narrator_shot(row):
 sid=row['id'];end=row['frames'];front=sid.startswith('N04');lamp,tv=room(front)
 if sid in ['N01','N02','N03']:
  a=actor('ferguson',[0],.15,-3.3,5.0,.8,True);camera(-.3,-.2,15)
  if sid=='N01':
   keyed(SCENE.camera.data,'ortho_scale',[(1,15),(28,14.2),(end,14.2)]);move(a,[(1,(.15,-3.3,.8)),(22,(.15,-3.34,.8)),(end,(.15,-3.34,.8))])
  elif sid=='N02':
   paper=group('crushed notes',[poly('paper',[(-.3,-.2),(-.4,.2),(.2,.3),(.4,-.1)],'#c2c8c4',3)],1.6,-1.7);keyed(paper,'scale',[(1,(1,1,1)),(21,(.4,.45,1)),(end,(.4,.45,1))]);keyed(a,'rotation_euler',[(1,(0,0,0)),(22,(0,0,-.025)),(end,(0,0,-.025))])
  else:
   keyed(a,'rotation_euler',[(1,(0,0,0)),(18,(0,0,.035)),(end,(0,0,.035))]);move(SCENE.camera,[(1,(-.3,-.2,30)),(end,(.1,-.2,30))]);keyed(SCENE.camera.data,'ortho_scale',[(1,15),(end,14.6)])
 elif sid in ['N04_dark','N04_reveal']:
  dark=sid=='N04_dark';a=actor('ferguson',[1],-.7,-3.4,5.2,1,dark);camera(-.7,-.4,8.2)
  if dark:keyed(SCENE.camera.data,'ortho_scale',[(1,9),(70,8.2),(end,8.2)])
  else:poly('lamp light pool',[(-3.5,-2),(2.7,-2),(3,2),(-2.5,2.2)],'#70614c',-2.6)
 elif sid=='N04_meltdown':
  a=actor('ferguson',[2,3],-.7,-3.4,5.2,1);pose(a,[(1,0),(7,1)]);camera(-.4,-.25,12);keyed(SCENE.camera.data,'ortho_scale',[(1,8.2),(8,12),(end,12)]);speak(a,*talk_interval(sid));poly('lamp light pool',[(-3.5,-2),(2.7,-2),(3,2),(-2.5,2.2)],'#70614c',-2.6)
 else:
  a=actor('ferguson',[4,5],-1.8,-3.4,5.2,1);pose(a,[(1,0),(10,1)]);camera(0,-.1,15)
  p=group('thrown paper',[poly('paper',[(-.12,-.08),(-.15,.07),(.04,.14),(.16,0),(.07,-.1)],WHITE,4)],0,0);keyed(p,'scale',[(1,(0,0,0)),(9,(0,0,0)),(10,(1,1,1))],'CONSTANT');arc(p,10,20,(-.2,.65),(3.6,.15),.27);arc(p,21,41,(3.6,.15),(3.4,-3.3),.08);move(p,[(42,(3.4,-3.3,0)),(60,(3.4,-3.3,0))]);poly('lamp light pool',[(-3.5,-2),(2.7,-2),(3,2),(-2.5,2.2)],'#70614c',-2.6)

def opening_shot(row):
 sid=row['id'];end=row['frames'];stadium(True)
 if sid.startswith('OP01'):
  rect('banner',-1.5,-.4,8.8,4.1,RED,-1.8);label('THIS IS OUR YEAR',2.9,2.2,.58,WHITE,-1.6);rect('year card',1.55,.1,2.7,1.3,WHITE,-1.5);label('2026',2.9,.42,.72,INK,-1.4)
  card=group('peel 2025',[rect('old year',-1.35,0,2.7,1.3,WHITE,2),label('2025',0,.33,.72,INK,2.1)],2.9,.1)
  a=actor('arteta',[0,1],-2.4,-3.5,4.8);pose(a,[(1,0),(12,1)]);w=actor('support',[2,3],6,-2.3,4.8,.5)
  line('worker ladder left',[(5.5,-3.55),(5.8,-1.8)],'#acb6bb',.055,.1);line('worker ladder right',[(6.55,-3.55),(6.25,-1.8)],'#acb6bb',.055,.1)
  for yy in [-3.25,-2.9,-2.55,-2.25]:line('ladder rung',[(5.65,yy),(6.4,yy)],'#acb6bb',.045,.1)
  for i in range(3):actor('wall',[i+2],-6.6+i*1.25,-3.45,3.7,.4)
  if sid=='OP01_year':
   pose(w,[(1,0),(30,1)]);move(card,[(1,(2.9,.1,0)),(22,(4.7,.5,0)),(34,(5.8,-1.0,0))]);keyed(card,'rotation_euler',[(1,(0,0,0)),(22,(0,0,-.2)),(34,(0,0,-.45))]);speak(a,*talk_interval(sid))
 elif sid in ['OP02_truck','OP02_arteta']:
  t=truck(-1);a=actor('arteta',[0,4],-5.5,-3.45,4.8,2.3);pose(a,[(1,0),(18,1)]);d=actor('support',[1],5.0,-.8,1.6,2.1)
  if sid=='OP02_truck':
   move(t,[(1,(4,-.85,0)),(42,(-1,-.85,0)),(end,(-1,-.85,0))]);move(d,[(1,(10,-.8,2.1)),(42,(5,-.8,2.1)),(end,(5,-.8,2.1))])
  else:camera(-2.2,.0,11);speak(a,*talk_interval(sid))
 elif sid=='OP02_driver':
  rect('cab surround',-8,-4.5,16,9,'#dddcd3',-.5);rect('cab opening',-4,-3,8,7,'#426476',0);d=actor('support',[1,0],0,-2.2,5.2,1);pose(d,[(1,0),(7,1),(end-7,0)]);rect('window sill',-5,-3,10,.75,'#efeee5',3);speak(d,*talk_interval(sid));camera(0,.2,11)
 else:
  a=actor('arteta',[4,2],0,-3.5,5.0);pose(a,[(1,0),(6,1)]);camera(.2,.1,9.8);speak(a,*talk_interval(sid))

def unveiling_shot(row):
 sid=row['id'];end=row['frames'];stadium(True)
 poly('red carpet',[(-7,-4.2),(6,-4.2),(6,.2),(2,.2)],'#9e2434',-2)
 gy=actor('gyokeres',[0,5],-3.8,-3.5,4.8);ar=actor('arteta',[0,1,4],1.2,-3.5,4.7)
 fl=flag(5.5,-3.4,5.8);shirt=group('number nine shirt',[poly('shirt',[(-.5,1),(.5,1),(1,.4),(.6,.1),(.45,.3),(.45,-1.1),(-.45,-1.1),(-.45,.3),(-.6,.1),(-1,.4)],RED,2),label('9',0,-.75,1.1,WHITE,2.1)],5.5,-.1)
 if sid=='TR01':
  bag=group('striker bag',[rect('bag',-.55,0,1.1,.55,'#25374a',2),line('bag handle',[(-.3,.5),(-.3,.8),(.3,.8),(.3,.5)],INK,.04,2)],-5,-1.8);move(bag,[(1,(-5,-1.8,0)),(10,(-5,-3.5,0)),(14,(-5,-3.44,0)),(18,(-5,-3.5,0))]);pose(gy,[(1,0),(35,1)]);camera(-1.0,-.3,14)
 elif sid=='TR02_flag':
  pose(ar,[(1,0),(12,1)]);camera(-2,0,10);move(SCENE.camera,[(1,(-2,0,30)),(40,(1,0,30)),(end,(1,0,30))]);keyed(SCENE.camera.data,'ortho_scale',[(1,10),(40,16),(end,16)])
 else:
  pose(ar,[(1,0),(76,1)]);pose(gy,[(1,0),(end-15,1)]);camera(-1.5,-.3,13.5);speak(gy,*talk_interval(sid,0));speak(ar,*talk_interval(sid,1))

def hotline_shot(row):
 sid=row['id'];end=row['frames']
 if sid in ['VH03','VH03_answer','VH04_operator','VH04_button']:
  grey,gold=officials_office();op=actor('officials',[4,5,6,7],0,-2.4,6.0,1)
  if sid=='VH03':
   pose(op,[(1,0)]);keyed(gold,'rotation_euler',[(1,(0,0,0)),(5,(0,0,.04)),(9,(0,0,-.04)),(13,(0,0,0)),(24,(0,0,0)),(28,(0,0,.04)),(32,(0,0,-.04)),(36,(0,0,0))]);effect(-4.3,-1.45,4,GOLD);effect(3.5,-1.45,18,GOLD)
  elif sid=='VH04_button':
   pose(op,[(1,2),(7,3)]);button=group('PLAY ON control',[rect('control base',-.9,-.25,1.8,.5,INK,4),disc('red button',0,0,.42,RED,4.1),label('PLAY ON',0,-.18,.20,WHITE,4.2)],-1.25,-2.05);keyed(button,'scale',[(1,(1,1,1)),(6,(1,1,1)),(7,(1,.7,1)),(13,(1,1,1))]);move(grey,[(1,(-4.3,-2.1,0)),(15,(-4.65,-2.3,0)),(end,(-4.65,-2.3,0))])
  else:pose(op,[(1,1)]);speak(op,*talk_interval(sid));camera(0,.0,13)
 elif sid in ['VH04_mikel','VH04_two']:
  stadium();a=actor('arteta',[2],-.5,-3.5,5.0);camera(0,.1,9.5);speak(a,*talk_interval(sid))
 else:
  stadium();goal(1.2,-2.7,5.8,4.0);ref=actor('officials',[0,1,2,3],-2.3,-3.5,5.1,1)
  if sid=='VH02':pose(ref,[(1,1)]);rect('hold menu',.8,-.3,6,3.1,'#214c82',2);label('PLEASE HOLD',3.8,1.4,.55);rect('progress track',1.5,.3,4.6,.16,'#112943',3);bar=rect('hold progress',0,.3,3.1,.16,'#73b8ff',3.1);bar.location.x=1.5;keyed(bar,'scale',[(1,(.4,1,1)),(70,(1,1,1)),(end,(1,1,1))]);camera(0,0,14)
  elif sid=='VH06':
   pose(ref,[(1,2),(6,3),(95,1),(140,2)]);camera(-2.3,.0,8.5);speak(ref,*talk_interval(sid,0));rect('season over',.8,1,5.8,.9,'#173447',2);label('SEASON ENDED',3.7,1.25,.42)
  else:
   pose(ref,[(1,1),(min(60,end),2)]);actor('football',[6],3.4,-3.4,4.6,.8)
   if sid=='VH05':speak(ref,*talk_interval(sid,0));label('PLAY ON',4,2.5,.7,WHITE,3)
   if sid=='VH05_wait':
    camera(-2.0,.0,10);label('89:59',3.5,2.3,.6,WHITE,3);wrapper=poly('snack wrapper',[(1,-3.4),(1.2,-3.2),(1.6,-3.3),(1.5,-3.5)],'#d5bf6c',2);move(wrapper,[(1,(0,0,0)),(end,(-1.5,0,0))],'LINEAR')

def reaction_shot(row):
 sid=row['id'];stadium(True);a=actor('arteta',[0,1,4],2,-3.5,4.8);g=actor('gyokeres',[0,5],-3 if sid.startswith('TR') else -15,-3.5,4.8);flag(5,-3.5)
 if sid=='TR03_warning':pose(a,[(1,0),(8,1)]);speak(a,*talk_interval(sid));camera(0,0,13)
 elif sid=='TR03_praise':pose(a,[(1,0),(8,1)]);speak(a,*talk_interval(sid));camera(1,0,11)
 elif sid=='TR04':pose(g,[(1,0),(12,1)]);speak(g,*talk_interval(sid));camera(-2,.2,9)
 elif sid=='CD05_proud':pose(a,[(1,0)]);speak(a,*talk_interval(sid));camera(2,0,9)
 elif sid=='CD05_ping':
  pose(a,[(1,0),(12,2)]);card=group('CITY WIN notification',[rect('phone notification',-2,0,4,1.1,INK,4),label('CITY WIN',0,.34,.55,WHITE,4.1)],1.8,-1.2);keyed(card,'scale',[(1,(0,0,0)),(8,(1,1,1))]);camera(2,0,9)
 elif sid=='FR04':pose(a,[(1,0),(10,1)]);speak(a,*talk_interval(sid));camera(2,0,9)
 elif sid=='FR05':
  pose(a,[(1,0),(12,1)]);speak(a,*talk_interval(sid));trolley(-3.2);actor('support',[5],-5.8,-3.5,4.5);camera(0,0,16)

def trophy_shot(row):
 stadium();actor('wall',[0],-2.4,-3.5,4.7);actor('wall',[1],2.4,-3.5,4.7);actor('arteta',[0],5.5,-3.5,4.6)
 cup=group('champions trophy',[poly('silver cup',[(-.8,1.6),(.8,1.6),(.6,.5),(.22,.1),(.18,-.65),(.65,-.85),(-.65,-.85),(-.18,-.65),(-.22,.1),(-.6,.5)],'#d9e4e8',3),line('left handle',[(-.7,1.4),(-1.1,1.4),(-1.1,.7),(-.55,.4)],GOLD,.08,3),line('right handle',[(.7,1.4),(1.1,1.4),(1.1,.7),(.55,.4)],GOLD,.08,3),rect('cup base',-.72,-1.1,1.44,.3,INK,3)],0,-.8)
 rect('trophy pedestal',-.85,-3.5,1.7,1.6,'#263747',2.5);label('CHAMPIONS',0,2.8,.72)
 for i in range(36):
  x=-7.5+(i*37%150)/10;y=4.8+(i%7)*.5;c=rect('confetti',x,y,.09,.2,RED if i%2 else GOLD,4);move(c,[(1,(0,0,0)),(row['frames'],(.6*math.sin(i),-8-(i%4),0))],'LINEAR')

if __name__=='__main__':
 for name,count,rows in [('arteta',6,2),('ferguson',6,2),('gyokeres',6,2),('officials',8,2),('support',6,2),('football',8,2),('wall',9,3)]:load_sheet(name,count,rows)
 selected=[]
 for row in edit:
  sid=row['id'];builder=None
  if sid in ['N01','N02','N03','N04_dark','N04_reveal','N04_meltdown','N04_tap']:builder=narrator_shot
  elif sid.startswith('OP'):builder=opening_shot
  elif sid in ['TR01','TR02_flag','TR02_reaction']:builder=unveiling_shot
  elif sid.startswith('VH') and sid!='VH01':builder=hotline_shot
  elif sid in ['TR03_warning','TR03_praise','TR04','CD05_proud','CD05_ping','FR04','FR05']:builder=reaction_shot
  elif sid=='N04_trophy':builder=trophy_shot
  if builder:
   s=new_scene(row);builder(row);s.frame_set(1);selected.append(sid);print('BUILT',sid,flush=True)
 assert len(selected)==len(set(selected)) and len(selected)>=30
 # Show season-ended notice only after the punchline lands.
 s=bpy.data.scenes['S002_fullmotion_VH06'];SCENE=s
 for ob in s.objects:
  if 'season over' in ob.name or (ob.type=='FONT' and ob.data.body=='SEASON ENDED'):keyed(ob,'scale',[(1,(0,0,0)),(94,(0,0,0)),(95,(1,1,1))],'CONSTANT')
 bpy.context.window.scene=bpy.data.scenes['S002_fullmotion_N01']
 bpy.ops.wm.save_as_mainfile(filepath=str(O/'acting-batch-v004.blend'))
 (O/'batch.json').write_text(json.dumps({'shots':selected,'frames':sum(r['frames'] for r in edit if r['id'] in selected),'stage':'First animation batch; football contact and remaining chase coverage next; acting polish pending'},indent=2))
 print('BATCH_BUILT',len(selected),flush=True)
