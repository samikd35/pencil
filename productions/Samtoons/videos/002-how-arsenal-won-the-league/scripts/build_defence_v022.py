"""Scoped native reaction insert and extended City performance, preserving v021 scenes."""
import bpy,math,json,copy
import numpy as np
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/defence-v022'
n=bpy.app.driver_namespace['cast21'];base=n['s'];b=n['b'];smooth=n['smooth'];curves=n['curves'];actors={}
def linear(ob):
 for fc in curves(ob):
  for p in fc.keyframe_points:p.interpolation='LINEAR'
def key(ob,prop,f,value):
 setattr(ob,prop,value);ob.keyframe_insert(data_path=prop,frame=f)
def scene(name,end,frame):
 base.frame_set(frame);bpy.context.window.scene=base;bpy.context.view_layer.update()
 s=bpy.data.scenes.new(name);s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=24;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_end=end;s.render.use_sequencer=False;s.world=base.world;s.view_settings.view_transform='Standard';s.view_settings.look='None'
 excluded=set()
 for a in list(n['actors'].values())+list(n['oldactors'].values()):excluded.update([a['root'],*a['root'].children_recursive])
 shadow_seen=set()
 for ob in base.objects:
  if 'contact shadow' in ob.name:
   loc=tuple(round(v,3) for v in ob.location)
   if loc in shadow_seen or frame==988 or loc[1]>-50:continue
   shadow_seen.add(loc)
  if ob in excluded or ob.type not in ['MESH','CURVE','FONT','LIGHT'] or ob.hide_render or ob.name=='v019 match ball':continue
  cp=ob.copy();cp.animation_data_clear();cp.parent=None;cp.matrix_world=ob.matrix_world.copy();s.collection.objects.link(cp)
 bpy.context.window.scene=s
 return s

def clone_actor(a,s,name,offset=None):
 group=[a['root'],*a['root'].children_recursive];mapping={}
 for ob in group:
  cp=ob.copy();cp.name='B22 / '+name+' / '+ob.name.split(' / ')[-1]
  if ob.type in ['MESH','ARMATURE','CURVE']:cp.data=ob.data.copy()
  for data in [cp,cp.data.shape_keys if cp.type=='MESH' else None]:
   if data is None:continue
   if offset is None:data.animation_data_clear()
   elif data.animation_data and data.animation_data.action:
    data.animation_data.action=data.animation_data.action.copy()
    for fc in curves(data):
     for j in range(len(fc.keyframe_points)-1,-1,-1):
      if fc.keyframe_points[j].co.x>711:fc.keyframe_points.remove(fc.keyframe_points[j],fast=True)
     for p in fc.keyframe_points:p.co.x-=offset;p.handle_left.x-=offset;p.handle_right.x-=offset
  s.collection.objects.link(cp);mapping[ob]=cp
 for ob,cp in mapping.items():
  if ob.parent in mapping:cp.parent=mapping[ob.parent]
  for co in cp.constraints:
   if hasattr(co,'target') and co.target in mapping:co.target=mapping[co.target]
  for mod in cp.modifiers:
   if hasattr(mod,'object') and mod.object in mapping:mod.object=mapping[mod.object]
  if cp.type=='ARMATURE':
   for pb in cp.pose.bones:
    for co in pb.constraints:
     if hasattr(co,'target') and co.target in mapping:co.target=mapping[co.target]
 aa=dict(a);aa.update(name=name,s=s,root=mapping[a['root']],skin=mapping[a['skin']],arm=mapping[a['arm']],C={k:mapping[o] for k,o in a['C'].items()},objects=list(mapping.values()));actors[name]=aa;return aa

def cam(s,source,name):
 c=source.copy();c.data=source.data.copy();c.name=name;c.animation_data_clear();c.data.animation_data_clear();s.collection.objects.link(c);s.camera=c;m=s.timeline_markers.new(name,frame=1);m.camera=c;return c

def build_wall():
 global wall,wcam
 wall=scene('S002_defence_v022_coach_reactions',296,711)
 for name in ['Raya']+['wall '+str(i) for i in range(1,10)]:clone_actor(n['actors'][name],wall,name,511)
 for ob in wall.objects:
  for co in ob.constraints:
   if hasattr(co,'target'):
    for name in ['Raya']+['wall '+str(i) for i in range(1,10)]:
     if co.target==n['actors'][name]['root']:co.target=actors[name]['root']
 wcam=cam(wall,next(m.camera for m in base.timeline_markers if m.frame==512),'B22 wall reveal camera')
 oldq=wcam.rotation_euler.copy();target=(Vector((0,-51.6,2.18))-wcam.location).to_track_quat('-Z','Y').to_euler()
 for f,t in [(1,0),(157,0),(184,1),(296,1)]:
  key(wcam,'rotation_euler',f,tuple(x+(y-x)*t for x,y in zip(oldq,target)));key(wcam.data,'lens',f,42-8*t)
 # Continued subtle keeper attention after the extended beat; feet remain planted.
 a=actors['Raya'];r={k:v.location.copy() for k,v in a['C'].items()}
 for f in range(201,297):
  t=smooth((f-202)/10)*(1-smooth((f-254)/12));u=.025*math.sin((f-202)/23)*t
  for k in ['neck','head','Lshoulder','Rshoulder']:
   p=r[k].copy();p.x+=u;key(a['C'][k],'location',f,p)
 for o in [wcam,wcam.data,*a['C'].values()]:linear(o)
 return {'scene':wall.name,'frames':296}

# Source-space landmarks, fitted to this complete drawing rather than a generic face.
COACHES=[dict(name='Mourinho',box=(0,105,520,951),cx=263,neck=(275,426),eyes=[(279,278,23,14),(347,262,20,13)],brows=[(280,252),(341,238)],start=174,pos=(-70,355),entry=(-450,355),scale=.46,angle=-1.13),dict(name='Simeone',box=(521,99,1024,947),cx=770,neck=(779,424),eyes=[(798,292,23,14),(865,282,19,12)],brows=[(795,271),(863,262)],start=199,pos=(1330,355),entry=(1700,355),scale=.46,angle=1.13),dict(name='Conte',box=(1025,115,1535,950),cx=1284,neck=(1282,426),eyes=[(1283,270,22,13),(1351,254,20,12)],brows=[(1282,250),(1346,232)],start=225,pos=(650,-30),entry=(650,-460),scale=.40,angle=math.pi)]

def build_coaches():
 global coach_records
 s=wall;bpy.context.window.scene=s
 im,mat=n['n']['old']['image_material'](V/'assets/coaches-v022/coaches.png');W,H=im.size;rgba=np.empty(W*H*4,np.float32);im.pixels.foreach_get(rgba);alpha=rgba.reshape(H,W,4)[::-1,:,3];coach_records=[]
 for cfg in COACHES:
  name=cfg['name'];x0,y0,x1,y1=cfg['box'];cx=cfg['cx'];floor=940;nx,ny=115,175
  pixels=[(x0+(x1-x0)*i/nx,y0+(y1-y0)*j/ny) for j in range(ny+1) for i in range(nx+1)];vv=[(x-cx,floor-y,0) for x,y in pixels];faces=[]
  for j in range(ny):
   for i in range(nx):
    k=j*(nx+1)+i;px,py=pixels[k];xx,yy=pixels[k+nx+2]
    if alpha[max(0,int(py)):min(H,int(yy)+2),max(0,int(px)):min(W,int(xx)+2)].max()>.93:faces.extend([(k,k+1,k+nx+2),(k,k+nx+2,k+nx+1)])
  root=bpy.data.objects.new('B22 cameo '+name,None);s.collection.objects.link(root);root.parent=wcam;root.rotation_euler.z=cfg['angle']
  me=bpy.data.meshes.new(name+' coherent bust');me.from_pydata(vv,[],faces);me.materials.append(mat);uv=me.uv_layers.new()
  for lp in me.loops:x,y=pixels[lp.vertex_index];uv.data[lp.index].uv=(x/W,1-y/H)
  ob=bpy.data.objects.new(me.name,me);s.collection.objects.link(ob);ob.parent=root;ob.shape_key_add(name='Basis')
  shape={k:ob.shape_key_add(name=k) for k in ['Nod','Brow','Blink','Write','Lift']}
  for i,(x,y) in enumerate(pixels):
   px,py=vv[i][:2];neckx,necky=cfg['neck'];weight=smooth((necky+32-y)/68);ang=-.075;dx=x-neckx;dy=necky-y
   shape['Nod'].data[i].co.x+=weight*(math.cos(ang)*dx-math.sin(ang)*dy-dx);shape['Nod'].data[i].co.y+=weight*(math.sin(ang)*dx+math.cos(ang)*dy-dy)
   for ex,ey,rx,ry in cfg['eyes']:
    qx=abs(x-ex)/(rx+2);qy=abs(y-ey)/(ry+2)
    if qx<1.3 and qy<1.5:shape['Blink'].data[i].co.y+=(y-ey)*.85*max(0,min(1,(1.3-qx)/.3))*max(0,min(1,(1.5-qy)/.5))
   for ex,ey in cfg['brows']:shape['Brow'].data[i].co.y+=13*math.exp(-((x-ex)/29)**4-((y-ey)/15)**4)
   if name=='Simeone':
    w=math.exp(-((x-719)/67)**4-((y-604)/88)**4);shape['Write'].data[i].co.x+=9*w;shape['Write'].data[i].co.y+=4*w
   if name=='Conte':
    w=math.exp(-((x-1290)/183)**6-((y-650)/154)**6);shape['Lift'].data[i].co.y+=38*w
  start=cfg['start'];end=296
  for f in range(1,end+1):
   enter=smooth((f-start)/12);exit=smooth((f-282)/13);x=cfg['entry'][0]+(cfg['pos'][0]-cfg['entry'][0])*enter;y=cfg['entry'][1]+(cfg['pos'][1]-cfg['entry'][1])*enter
   if exit:x+=(cfg['entry'][0]-cfg['pos'][0])*exit;y+=(cfg['entry'][1]-cfg['pos'][1])*exit
   # Camera-space coordinates maintain stable screen placement through the pullback.
   lens=42-8*smooth((f-157)/27);unit=wcam.data.sensor_width/lens/1280
   key(root,'location',f,((x-640)*unit,(360-y)*unit,-1));key(root,'scale',f,(unit*cfg['scale'],)*3)
   elapsed=f-start
   nod=(math.sin((elapsed-15)*math.pi/18)**2 if 15<=elapsed<33 else 0)+(math.sin((elapsed-40)*math.pi/22)**2*.55 if 40<=elapsed<62 and name=='Mourinho' else 0)
   brow=smooth((elapsed-9)/7)*(1-smooth((elapsed-60)/10))
   blink=max(0,1-abs(elapsed-48)/2)
   write=(.5+.5*math.sin((elapsed-16)*2*math.pi/5))*smooth((elapsed-16)/3)*(1-smooth((elapsed-62)/6)) if name=='Simeone' else 0
   lift=smooth((elapsed-14)/9)*(1-smooth((f-282)/10)) if name=='Conte' else 0
   for label,value in [('Nod',nod),('Brow',brow),('Blink',blink),('Write',write),('Lift',lift)]:key(shape[label],'value',f,value)
  linear(root);linear(ob.data.shape_keys)
  if name=='Conte':
   # Source-coherent notebook text, following its lift rather than floating over the shot.
   for text,y,size in [('ARTETA',666,38),('MASTERCLASS',626,22)]:
    d=bpy.data.curves.new('Conte notebook '+text,'FONT');d.body=text;d.align_x='CENTER';d.size=size;d.materials.append(b['mat']('#1a2630'));o=bpy.data.objects.new(d.name,d);s.collection.objects.link(o);o.parent=root;o.location=(1290-cx,940-y,.1);o.rotation_euler.z=math.pi
    for f in range(1,297):key(o,'location',f,(1290-cx,940-y+38*smooth((f-start-14)/9)*(1-smooth((f-282)/10)),.1))
    linear(o)
  if name=='Simeone':
   # Short ink strokes appear where his moving pencil is writing.
   for j in range(4):
    pts=[(761-cx+v,940-(654+j*12)+.26*v) for v in [0,14,31,54]];line=b['line'](s,'B22 Simeone note '+str(j),pts,'#423932',.08,root,1.1)
    for f,v in [(1,True),(start+20+j*8,True),(start+21+j*8,False)]:key(line,'hide_render',f,v);key(line,'hide_viewport',f,v)
  coach_records.append(dict(name=name,mesh=ob.name,root=root.name,source=cfg,keys=list(shape)))
 (O/'coaches.json').write_text(json.dumps(coach_records,indent=2));s.frame_set(264)
 return {'coaches':coach_records}

def build_city():
 global city,arteta
 city=scene('S002_defence_v022_City',240,988);base.frame_set(988);bpy.context.window.scene=base;bpy.context.view_layer.update();arteta=clone_actor(n['q']['A'],city,'City Arteta');bpy.context.window.scene=city
 phone=next(o for o in arteta['objects'] if '/ v019 Arteta phone' in o.name);phone.hide_render=phone.hide_viewport=False
 cc=cam(city,next(m.camera for m in base.timeline_markers if m.frame==988),'B22 City response camera');r=arteta['rest']
 for f in range(1,241):
  # Read the ping; small disbelieving recoil, a pointed fortress gesture, then look behind.
  disbelief=smooth((f-13)/7)*(1-smooth((f-47)/8));fortress=smooth((f-48)/7)*(1-smooth((f-89)/9));behind=smooth((f-93)/7)*(1-smooth((f-140)/10));listen=smooth((f-155)/8)
  b['pose_actor'](arteta,f,ua=(-.65*fortress-.30*behind,0),fa=(-.35*fortress-.65*behind,0),hands=(-.14*fortress,0),lean=-.025*disbelief+.02*fortress,shift=(0,-.009*disbelief))
  t=smooth((f-3)/9);sh=arteta['C']['Rshoulder'].location.copy();wr=arteta['C']['Rwrist'].location.lerp(Vector((.47,1.36-.07*listen,0)),t);el=b['ik'](sh,wr,(r['Relbow']-r['Rshoulder']).length,(r['Rwrist']-r['Relbow']).length,sh+Vector((.12,-.36,0)));fi=wr+Vector((.02,.098,0)).normalized()*(r['Rfinger']-r['Rwrist']).length
  for k,v in [('Relbow',el),('Rwrist',wr),('Rfinger',fi)]:key(arteta['C'][k],'location',f,v)
  key(phone,'location',f,wr+Vector((.015,.025,0)));key(phone,'scale',f,(1,1,1))
  p=arteta['C']['head'].location.copy();p.x-=.023*disbelief;p.x+=.055*listen;key(arteta['C']['head'],'location',f,p)
 for ob in arteta['C'].values():linear(ob)
 # Same selected facial surfaces and timed voice-envelope machinery as accepted first batch.
 oldO=b['O'];b['O']=O
 try:b['lips'](arteta,[('L18b',18)],clear=True)
 finally:b['O']=oldO
 sk=arteta['skin'].data.shape_keys
 if sk and 'Blink' in sk.key_blocks:
  k=sk.key_blocks['Blink']
  for f,v in [(1,0),(11,0),(13,.85),(15,0),(146,0),(148,.9),(150,0),(224,0),(226,.9),(228,0),(240,0)]:key(k,'value',f,v)
 return {'scene':city.name,'frames':240}

def save():
 rows=json.loads((V/'artifacts/defence-v021/edit.json').read_text());cursor=1
 for r in rows:
  if r['id']=='CD04':r.update(scene=wall.name,local_start=1,frames=296)
  elif r['id']=='CD05_ping':r.update(scene=city.name,local_start=1,frames=240)
  r['start_frame']=cursor;cursor+=r['frames']
 (O/'edit.json').write_text(json.dumps(rows,indent=2))
 for shot,sc in [('CD04',wall),('CD05_ping',city)]:
  ed=sc.sequence_editor_create()
  for strip in list(ed.strips):ed.strips.remove(strip)
  rr=next(r for r in rows if r['id']==shot);offset=rr['start_frame']-1;strip=ed.strips.new_sound('Authoritative v022 mix',str(O/'mix/mix-premaster.wav'),channel=1,frame_start=1-offset);strip.frame_offset_start=offset;strip.frame_final_duration=rr['frames'];sc.sync_mode='AUDIO_SYNC';sc.render.use_sequencer=False
 wall.frame_set(263);bpy.context.window.scene=wall
 for area in bpy.context.screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA'
 bpy.data.libraries.write(str(O/'batch02-v022.blend'),{base,n['room'],wall,city},fake_user=True,compress=True)
 return {'frames':cursor-1,'file':str(O/'batch02-v022.blend')}
