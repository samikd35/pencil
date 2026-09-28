"""Final chronological batch. Run named functions in the visible Blender instance.

Reuse the accepted v016/v021 fitted complete drawing rigs and dimensional stadium.
Each scene owns its performance; source assets, accepted movies and rigs stay intact.
"""
import bpy,math,json,copy,ast,subprocess
import numpy as np
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/final-batch-v023'
n=bpy.app.driver_namespace['cast21'];b=n['b'];q=n['q'];n16=n['n'];c22=bpy.app.driver_namespace['cast22']
smooth=n['smooth'];rot=n['rotate'];curves=n['curves'];key=q['key'];linear=q['linear'];S={};A={};rows=json.loads((O/'edit.json').read_text());byid={r['id']:r for r in rows}
def scene(sid,stadium=False):
 s=bpy.data.scenes.new('S002_final_v023_'+sid);s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_end=byid[sid]['frames'];s.render.use_sequencer=False;s.view_settings.view_transform='Standard';s.view_settings.look='None';s.world=n['s'].world;S[sid]=s;bpy.context.window.scene=s
 if stadium:
  for ob in q['env'].all_objects:
   if 'contact shadow' not in ob.name.lower():s.collection.objects.link(ob)
 byid[sid].update(scene=s.name,local_start=1)
 return s
def cam(s,loc,target,width=9):
 d=bpy.data.cameras.new(s.name+' camera');d.type='ORTHO';d.ortho_scale=width;ob=bpy.data.objects.new(d.name,d);s.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();s.camera=ob;return ob
def flat(s,name,loc=(0,0,0)):
 ob=b['empty'](s,'F23 '+name);ob.location=loc;ob.rotation_euler.x=math.pi/2;return ob
def rect(s,parent,name,x,y,w,h,col,z=0):return b['poly'](s,'F23 '+name,[(x,y),(x+w,y),(x+w,y+h),(x,y+h)],col,z,parent,False)
def label(s,parent,body,x,y,size=.2,color='#fff8e8',z=.03):
 d=bpy.data.curves.new('F23 '+body,'FONT');d.body=body;d.size=size;d.align_x='CENTER';d.materials.append(b['mat'](color));o=bpy.data.objects.new(d.name,d);s.collection.objects.link(o);o.parent=parent;o.location=(x,y,z);return o
def use(s):
 bpy.context.window.scene=s;s.frame_set(1)
 for area in bpy.context.screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA'
def clone(src,s,name,loc,height=1.8,flip=False):
 # Existing clone remaps bones/constraints; clear source pose/prop visibility as well.
 a=c22['clone_actor'](src,s,name);a.update(height=height,base=Vector(loc),face=math.pi if flip else 0)
 a['root'].location=loc;a['root'].rotation_euler=(math.pi/2,0,0);a['root'].scale=((-1 if flip else 1)*height/1.8,height/1.8,height/1.8)
 for ob in a['objects']:
  ob.hide_render=ob.hide_viewport=False
  if ob.type=='MESH' and ob.data.shape_keys:
   for k in ob.data.shape_keys.key_blocks:k.value=0
  if any(x in ob.name.lower() for x in ['native mouth','native teeth','phone','pointing','point hand','point silhouette','source left hand']):ob.hide_render=ob.hide_viewport=True
 for k,v in a['rest'].items():a['C'][k].location=v
 A[s.name+' / '+name]=a;return a
def lead(kind,s,loc,height=1.8,flip=False):return clone(n16['ACTORS']['opening Arteta' if kind=='Arteta' else 'unveiling Gyokeres'],s,kind,loc,height,flip)
def player(kind,s,loc,height=1.85,flip=False):return clone(n['actors'][kind],s,kind,loc,height,flip)
def pose(a,f,**kw):
 p=n['pose'](a,**kw);n['write_pose'](a,f,p);return p
def pulse(f,start,peak,end):return smooth((f-start)/max(1,peak-start))*(1-smooth((f-peak)/max(1,end-peak)))
def reach(a,p,side,target):
 r=a['rest'];sh=p[side+'shoulder'];length1=(r[side+'elbow']-r[side+'shoulder']).length;length2=(r[side+'wrist']-r[side+'elbow']).length;d=target-sh
 if d.length>length1+length2-.005:target=sh+d.normalized()*(length1+length2-.005)
 elbow=b['ik'](sh,target,length1,length2,sh+Vector((-.16 if side=='L' else .16,-.3,0)))
 p[side+'elbow']=elbow;p[side+'wrist']=target;p[side+'finger']=target+Vector((.01,.09,0)).normalized()*(r[side+'finger']-r[side+'wrist']).length
def speak(a,ident,start):
 old=b['O'];b['O']=O
 try:b['lips'](a,[(ident,start)],clear=True)
 finally:b['O']=old
def lineframe(sid,ident):
 return next(c['local_frame'] for c in json.loads((O/'captions.json').read_text()) if c['shot']==sid and c['id']==ident)
def blink(a):
 sk=a['skin'].data.shape_keys
 if sk and 'Blink' in sk.key_blocks:
  k=sk.key_blocks['Blink'];k.value=0;k.keyframe_insert(data_path='value',frame=1)
  for f in range(41,a['s'].frame_end,83):
   for ff,v in [(f,0),(f+2,.9),(f+4,0)]:key(k,'value',ff,v)
def finish(s):
 for a in A.values():
  if a['s']!=s:continue
  blink(a)
  for ob in [a['root'],*a['C'].values()]:linear(ob)
 s.frame_set(1);use(s)
def preview(sid,f=1):
 s=S[sid];use(s);s.frame_set(f);s.render.image_settings.file_format='PNG';s.render.filepath=str(O/'review-frames'/f'{sid}-{f:04}.png');bpy.ops.render.render(write_still=True);return s.render.filepath

# Measured source landmarks. No old character's thresholds or bone lengths transferred.
cfg=n['cfg'];NEW={
 'Pep':cfg((44,8,493,792),274,20,786,419,(276,183),(289,94),[(188,215),(135,326),(97,430),(87,481),(225,423),(197,560),(161,722),(125,771)],[(367,214),(409,329),(453,432),(466,481),(326,423),(348,561),(384,722),(427,771)],[(184,45),(231,88),(300,83),(368,92),(404,88)]),
 'Referee':cfg((521,1,990,793),756,14,786,391,(758,176),(774,91),[(659,213),(607,321),(568,434),(560,480),(701,399),(678,555),(644,722),(600,770)],[(856,213),(902,326),(947,433),(960,480),(814,399),(839,555),(868,722),(912,770)],[(180,45),(230,98),(300,93),(356,99),(379,98)]),
 'Courier':cfg((51,787,492,1530),278,790,1518,1174,(283,967),(300,877),[(189,1003),(144,1106),(103,1204),(93,1249),(228,1181),(201,1322),(167,1464),(124,1497)],[(376,1003),(422,1105),(456,1204),(465,1249),(334,1181),(354,1322),(388,1464),(433,1497)],[(968,43),(1010,87),(1080,82),(1134,87),(1163,91)]),
 'Operator':cfg((534,787,984,1531),756,793,1516,1176,(761,962),(780,871),[(661,1000),(614,1103),(574,1203),(565,1249),(703,1180),(680,1320),(646,1464),(602,1496)],[(855,1000),(901,1105),(943,1203),(952,1249),(810,1180),(830,1320),(866,1464),(910,1496)],[(963,41),(1011,88),(1080,82),(1130,88),(1162,91)])}
FACE={'Pep':((323,137,18),[(303,91,12,8),(335,87,8,7)]),'Referee':((800,117,18),[(783,79,12,8),(810,74,8,7)]),'Courier':((331,914,17),[(313,877,11,10),(346,872,7,9)]),'Operator':((803,911,16),[(781,875,11,10),(813,869,7,8)])}
def make(kind,s,loc,height=1.8,flip=False,sheet='support.png'):
 # Reuse the accepted fitting function with only its source path and measured config changed.
 ns=dict(n);ns.update(s=s,actors={},CONFIG=NEW)
 tree=ast.parse((V/'scripts/reconstruct_defence_v021.py').read_text());fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='make');src=ast.unparse(fn).replace("V / 'assets/neutral-cast-v021'", "V / 'assets/final-cast-v023'");exec(src,ns)
 src=src.replace("py < hip + 100 * ratio and abs(px - c['center']) > 0.82 * abs(c[side][2][0] - c['center'])", "py < max(c[side][3][1]+48*ratio,hip+100*ratio) and abs(px-c['center']) > .70*abs(c[side][2][0]-c['center'])")
 exec(src,ns)
 a=ns['make'](kind,kind,height,loc,0,sheet);a['root'].scale=((-1 if flip else 1)*height/1.8,height/1.8,height/1.8);a['objects']=[a['root'],*a['root'].children_recursive];A[s.name+' / '+kind]=a;new_face(a,kind);return a
def new_face(a,kind):
 # Separate editable mouth/vowels and eyelids, fitted to the complete source head.
 mx,my,mw=FACE[kind][0];c=a['cfg'];u=a['unit'];s=a['s']
 def xy(x,y):return ((x-c['center'])*u,(c['floor']-y)*u)
 def mesh(name,points,color,z):
  o=b['poly'](s,a['name']+' native '+name,[xy(*p) for p in points],color,z,a['root'],False);vg=o.vertex_groups.new(name='head');vg.add(list(range(len(o.data.vertices))),1,'REPLACE');mod=o.modifiers.new('Same fitted head','ARMATURE');mod.object=a['arm'];mod.use_deform_preserve_volume=True;return o
 pts=[(mx+mw*t,my-1.5*t+sign*math.sqrt(max(0,1-t*t))) for sign,ts in [(-1.2,np.linspace(-1,1,19)),(8,np.linspace(1,-1,19))] for t in ts]
 mo=mesh('mouth',pts,'#341b18',.030);te=mesh('teeth',[(mx-mw*.68,my-.5),(mx+mw*.68,my-2),(mx+mw*.68,my+1.5),(mx-mw*.68,my+3)],'#fff2dd',.033)
 mo.shape_key_add(name='Basis');closed=mo.shape_key_add(name='Closed');rounded=mo.shape_key_add(name='Rounded')
 for i,v in enumerate(mo.data.vertices):closed.data[i].co.y=xy(mx,my)[1];rounded.data[i].co.x=xy(mx,my)[0]+.65*(v.co.x-xy(mx,my)[0])
 closed.value=1;mo.hide_render=te.hide_render=True;a['objects'] += [mo,te]
 sk=a['skin'];sk.shape_key_add(name='Basis');bk=sk.shape_key_add(name='Blink')
 for i,(px,py) in enumerate(a['pixels']):
  for ex,ey,rx,ry in FACE[kind][1]:
   dx=abs(px-ex)/(rx+2);dy=abs(py-ey)/(ry+2)
   if dx<1.3 and dy<1.5:bk.data[i].co.y+=(py-ey)*u*.85*max(0,min(1,(1.3-dx)/.3))*max(0,min(1,(1.5-dy)/.5))
def phone(a,color='#d9ac3e'):
 root=b['empty'](a['s'],'F23 hand phone',a['root']);rect(a['s'],root,'phone',-.024,-.008,.062,.12,color,.04);rect(a['s'],root,'screen',-.017,.016,.048,.082,'#83a6af',.042);return root
def phone_pose(a,p,prop,f,amount=1):
 wr=p['Rwrist'].lerp(p['neck']+Vector((.115,.045,0)),amount);reach(a,p,'R',wr);key(prop,'location',f,wr+Vector((0,.06,0)));key(prop,'scale',f,(1.4,1.4,1));n['write_pose'](a,f,p)

def hotline(ids=None):
 for sid in (ids or ['VH01','VH02','VH03','VH03_answer','VH04_mikel','VH04_operator','VH04_two','VH04_button','VH05','VH05_wait','VH06']):
  office=sid in ['VH03','VH03_answer','VH04_operator','VH04_button'];s=scene(sid,not office);E=s.frame_end
  if office:
   root=flat(s,'VAR office',(0,50,0));rect(s,root,'wall',-7,-1,14,7,'#203346',-.4)
   for x in [-3,-.8,1.4]:
    rect(s,root,'monitor',x,2.15,1.85,1.2,'#0d1925',-.3);rect(s,root,'monitor pitch',x+.08,2.23,1.69,1.04,'#527f51',-.28)
    b['line'](s,'monitor markings',[(x+.2,2.4),(x+1.65,2.4),(x+1.65,3.12),(x+.2,3.12),(x+.2,2.4)],'#dce7cf',-.26,root,.008)
   label(s,root,'VAR',0,3.75,.42);a=make('Operator',s,(0,49.4,-.50),2.6);desk=flat(s,'VAR desk',(0,48.95,0));rect(s,desk,'desk fascia',-4,0,8,.75,'#364752');rect(s,desk,'desktop',-4,.75,8,.11,'#82949d');label(s,desk,'PENDING',-1.75,.44,.19);label(s,desk,'MIKEL',1.75,.44,.19,'#edc84e')
   grey=flat(s,'pending phone',(-1.75,48.80,.88));rect(s,grey,'phone base',-.34,0,.68,.14,'#909ca0');gold=flat(s,'gold phone',(1.75,48.80,.88));rect(s,gold,'phone base',-.34,0,.68,.14,'#e3b443');button=flat(s,'play on button',(.6,48.76,.90));rect(s,button,'button',-.26,0,.52,.12,'#d63e43');label(s,button,'PLAY ON',0,.035,.087)
   prop=phone(a);cam(s,(0,40,2),(0,49,1.6),6.2)
   for f in range(1,E+1):
    lift=smooth((f-4)/9) if sid!='VH03' else 0;press=pulse(f,1,9,24) if sid=='VH04_button' else 0;enthusiasm=pulse(f,12,20,min(E,65)) if sid in ['VH03_answer','VH04_operator'] else 0
    p=n['pose'](a,lean=-.012*lift+.027*press,ua=(-.3*enthusiasm,.08),fa=(-.45*enthusiasm,0),head=.025*enthusiasm)
    if sid=='VH03':p['head'].x-=.025*(1-smooth((f-18)/9));key(gold,'rotation_euler',f,(math.pi/2,0,.025*math.sin(f*1.5)*smooth((f-18)/3)));key(prop,'scale',f,(0,0,0));n['write_pose'](a,f,p)
    else:
     phone_pose(a,p,prop,f,lift)
     if press:
      reach(a,p,'L',Vector((.40,.95,0)));n['write_pose'](a,f,p);key(button,'scale',f,(1,1-.32*press,1))
   for ident in {'VH03_answer':['L29'],'VH04_operator':['L31']}.get(sid,[]):speak(a,ident,lineframe(sid,ident))
  elif sid in ['VH04_mikel','VH04_two']:
   a=lead('Arteta',s,(0,49,0),1.8);prop=phone(a,'#253749');cam(s,(0,40,1.5),(0,49,1.1),3.4)
   for f in range(1,E+1):
    order=pulse(f,9,17,45);p=n['pose'](a,ua=(-.25*order,0),fa=(-.50*order,0),lean=.015*order,head=-.025*order);phone_pose(a,p,prop,f)
   ident='L30' if sid=='VH04_mikel' else 'L32';speak(a,ident,lineframe(sid,ident))
  else:
   ref=make('Referee',s,(0,49,0),1.84);cam(s,(0,38,2.4),(0,49,1),6.7 if sid in ['VH01','VH05'] else 4.5)
   for f in range(1,E+1):
    announce=pulse(f,22,32,78) if sid=='VH01' else 0;hear=smooth((f-80)/10) if sid=='VH01' else 1;hope=pulse(f,1,9,45) if sid=='VH06' else 0;despair=smooth((f-95)/12) if sid=='VH06' else .22*smooth((f-54)/20)
    p=n['pose'](ref,ua=(0,.60*announce),fa=(0,.4*announce),head=-.04*despair+.055*hope,down=-.02*despair,lean=.02*hope)
    if hear:wr=p['neck']+Vector((-.23,.13,0));reach(ref,p,'L',p['Lwrist'].lerp(wr,hear))
    n['write_pose'](ref,f,p)
   if sid=='VH01':
    gab=player('Gabriel',s,(-2,49.3,0),1.90);opp=player('opposing attacker',s,(-1,49.25,0),1.82)
    for f in range(1,E+1):
     tug=pulse(f,1,13,30);fall=smooth((f-15)/18);recover=smooth((f-62)/30);p=n['pose'](gab,ua=(0,.35*tug),fa=(0,1.0*tug),lean=.06*tug);n['write_pose'](gab,f,p);p=n['pose'](opp,lean=-.34*fall*(1-recover),down=-.17*fall*(1-recover),ua=(-.6*fall,.7*fall),fa=(-.25*fall,.25*fall));n['write_pose'](opp,f,p);key(opp['root'],'location',f,(-1+.4*fall,49.25,-.05*fall*(1-recover)))
   if sid in ['VH02','VH05','VH05_wait','VH06']:
    card=flat(s,'ref status',(1.45,48.6,1.8));msg='PLEASE HOLD' if sid=='VH02' else '89:59' if sid=='VH05_wait' else 'SEASON ENDED' if sid=='VH06' else 'PLAY ON';rect(s,card,'status',-.75,-.1,1.5,.58,'#244966');label(s,card,msg,0,.12,.18)
    if sid=='VH06':
     for f,v in [(1,(0,0,0)),(94,(0,0,0)),(95,(1,1,1))]:key(card,'scale',f,v)
    if sid=='VH05':
     opp=player('opposing attacker',s,(-1.8,49.1,0),1.82)
     for f in range(1,E+1):g=pulse(f,8,20,78);pose(opp,f,ua=(-.55*g,.45*g),fa=(-.5*g,.65*g),head=.04*g)
   for ident in {'VH01':['L27'],'VH05':['L33'],'VH06':['L44']}.get(sid,[]):speak(ref,ident,lineframe(sid,ident))
  finish(s)
 return list(S)

def save():
 (O/'edit.json').write_text(json.dumps(rows,indent=2));(O/'cast.json').write_text(json.dumps({k:{'scene':a['s'].name,'root':a['root'].name,'skin':a['skin'].name,'controls':{k:o.name for k,o in a['C'].items()},'source':a.get('cfg',{}),'construction':'accepted fitted whole-drawing surface with independent body controls and native speech surfaces'} for k,a in A.items()},indent=2))
 bpy.data.libraries.write(str(O/'final-batch-v023.blend'),set(S.values()),fake_user=True,compress=True)
 return {'scenes':len(S),'built_frames':sum(byid[k]['frames'] for k in S),'file':str(O/'final-batch-v023.blend')}
bpy.app.driver_namespace['final23']=globals()

def copy_objects(objects,s,prefix):
 mapping={}
 for o in objects:
  z=o.copy();z.name=prefix+' / '+o.name
  if o.data:z.data=o.data.copy()
  if z.animation_data and z.animation_data.action:z.animation_data.action=z.animation_data.action.copy()
  if z.data and hasattr(z.data,'shape_keys') and z.data.shape_keys and z.data.shape_keys.animation_data and z.data.shape_keys.animation_data.action:z.data.shape_keys.animation_data.action=z.data.shape_keys.animation_data.action.copy()
  s.collection.objects.link(z);mapping[o]=z
 for o,z in mapping.items():
  if o.parent in mapping:z.parent=mapping[o.parent]
  for co in z.constraints:
   if hasattr(co,'target') and co.target in mapping:co.target=mapping[co.target]
  for mod in z.modifiers:
   if hasattr(mod,'object') and mod.object in mapping:mod.object=mapping[mod.object]
  if z.type=='ARMATURE':
   for pb in z.pose.bones:
    for co in pb.constraints:
     if hasattr(co,'target') and co.target in mapping:co.target=mapping[co.target]
  for db in [z,z.data.shape_keys if z.type=='MESH' else None]:
   if db and db.animation_data:
    for fc in db.animation_data.drivers:
     for v in fc.driver.variables:
      for t in v.targets:
       if t.id in mapping:t.id=mapping[t.id]
 return mapping

def trolley(s,x,y):
 p=flat(s,'runner-up delivery',(x,y,0));rect(s,p,'cart',-.2,.28,1.25,.48,'#705371');rect(s,p,'cart stripe',-.2,.62,1.25,.14,'#e5d7a9');label(s,p,'RUNNERS-UP',.42,.44,.12)
 b['line'](s,'F23 trolley handle',[(-.60,.91),(-.35,.91),(-.30,.2),(1.18,.2)],'#ddd5b9',.04,p,.026)
 for x in [-.13,.95]:
  pts=[(x+.12*math.cos(t*math.tau/32),.14+.12*math.sin(t*math.tau/32)) for t in range(32)];b['poly'](s,'F23 trolley wheel',pts,'#242631',.05,p,False)
 return p

def chase():
 src=bpy.data.scenes['S002_CP01_loaded_run_v002'];ps=bpy.data.scenes['S002_CP03_pep_body_v001'];roots={name:next(o for o in src.objects if o.name.startswith('CP / '+name+' travel')) for name in ['Gabriel','Saliba','Gyokeres','Arteta']};pod=next(o for o in src.objects if o.name.startswith('CP / first-place podium travel'));pr=next(o for o in ps.objects if o.name.startswith('CP / Pep travel'))
 # Cache evaluated source cycles, including fitted support-foot corrections.
 cache={};pcache={};bpy.context.window.scene=src
 for f in range(1,33):
  src.frame_set(f);cache[f]={}
  for r in [*roots.values(),pod]:
   cache[f][r]=dict(location=tuple(r.location),index=r.get('pose_index',0),keys={o:{k.name:k.value for k in o.data.shape_keys.key_blocks} for o in r.children if o.type=='MESH' and o.data.shape_keys})
 bpy.context.window.scene=ps
 for f in range(1,29):
  ps.frame_set(f);pcache[f]=dict(location=tuple(pr.location),index=pr['pose_index'],keys={o:{k.name:k.value for k in o.data.shape_keys.key_blocks} for o in pr.children if o.type=='MESH' and o.data.shape_keys})
 for sid in ['CP01','CP02_far','CP02_near','CP03_panic','CP03_pep','CP04_forward','CP04_courier','CP05']:
  s=scene(sid);E=s.frame_end
  for o in src.objects:
   if not o.parent and 'travel' not in o.name and o.type!='CAMERA':s.collection.objects.link(o)
  chosen=[] if sid=='CP03_pep' else [*roots.values(),pod];objs=[o for r in chosen for o in [r,*r.children_recursive]];mp=copy_objects(objs,s,sid)
  for z in mp.values():
   if z.animation_data:z.animation_data.action=None
   if z.type=='MESH' and z.data.shape_keys and z.data.shape_keys.animation_data:z.data.shape_keys.animation_data.action=None
  pepmap=copy_objects([pr,*pr.children_recursive],s,sid);pep=pepmap[pr]
  for z in pepmap.values():
   if z.animation_data:z.animation_data.action=None
   if z.type=='MESH' and z.data.shape_keys and z.data.shape_keys.animation_data:z.data.shape_keys.animation_data.action=None
  camera=cam(s,(0,-12,1.45),(0,0,1.45),9.2 if sid not in ['CP03_panic','CP04_forward','CP03_pep'] else 4.1)
  courier=make('Courier',s,(0,-.28,0),1.8) if sid=='CP04_courier' else None;cart=trolley(s,0,-.35) if courier else None
  for f in range(1,E+1):
   tick=f-1;phase=tick%32+1;travel=3.9*tick/24
   for r in chosen:
    z=mp[r];rec=cache[phase][r];loc=Vector(rec['location']);loc.x+=travel-3.9*(phase-1)/24
    if sid=='CP05' and r in [roots['Gabriel'],pod]:
     sag=.13*pulse(f,25,35,49);loc.z-=sag
    key(z,'location',f,loc);z['pose_index']=rec['index'];z.keyframe_insert(data_path='["pose_index"]',frame=f)
    for ob,ks in rec['keys'].items():
     for kn,v in ks.items():
      if kn!='Basis':key(mp[ob].data.shape_keys.key_blocks[kn],'value',f,v)
   ph=tick%28+1;rec=pcache[ph];pl=Vector(rec['location']);pl.x=1.14*tick/24
   if sid=='CP03_pep':cx=pl.x+.2;pep.scale=(1,1,1)
   else:
    # Same measured walk cadence; perspective compression is revealed at the ping cut.
    gap=8 if sid in ['CP01','CP02_far'] else 3.3;pl.x=travel-gap;pl.y=.35;pep.scale=(.72,.72,.72);pl.z*=.72;cx=travel+(.05 if sid in ['CP01','CP02_far','CP02_near','CP05'] else 2.1)
   key(pep,'location',f,pl);pep['pose_index']=rec['index'];pep.keyframe_insert(data_path='["pose_index"]',frame=f)
   for ob,ks in rec['keys'].items():
    for kn,v in ks.items():
     if kn!='Basis':key(pepmap[ob].data.shape_keys.key_blocks[kn],'value',f,v)
   if courier:
    cx=travel+2.1;cp=Vector((travel+4.5,-.25,0));p=n['pose'](courier,ua=(-.2,0),fa=(-.2,0),head=-.025*pulse(f,12,20,58));n['write_pose'](courier,f,p,cp);key(cart,'location',f,(travel+3.8,-.35,0))
   key(camera,'location',f,(cx,-12,1.45))
  for z in [*mp.values(),*pepmap.values()]:
   for fc in curves(z):
    for k in fc.keyframe_points:k.interpolation='CONSTANT' if 'pose_index' in fc.data_path else 'LINEAR'
  if sid=='CP02_near':
   pop=flat(s,'City alert',(0,-.65,2.7));rect(s,pop,'alert',-.8,-.13,1.6,.43,'#76bedb');label(s,pop,'CITY WIN',0,0,.19,'#102b40')
   for f in range(1,E+1):key(pop,'location',f,(3.9*(f-1)/24-2,-.65,2.7))
  if courier:speak(courier,'L24',lineframe(sid,'L24'))
  finish(s)
 return list(S)

def finals():
 NEW['Gyokeres rear']=cfg((155,10,863,1509),532,20,1495,831,(520,276),(474,153),[(379,371),(310,586),(228,786),(210,878),(444,846),(411,1030),(368,1364),(286,1460)],[(686,371),(750,590),(800,786),(818,878),(620,846),(667,1030),(710,1364),(748,1460)],[(276,57),(385,139),(460,133),(550,115),(645,135),(740,141)])
 FACE['Gyokeres rear']=((405,237,18),[(442,165,17,13),(390,155,9,11)])
 source=n['s'];bpy.context.window.scene=source;cache={}
 for f in range(1,270):
  source.frame_set(f);cache[f]={name:dict(p={k:o.location.copy() for k,o in a['C'].items()},loc=a['root'].location.copy()) for name,a in n['actors'].items() if name in ['Saka','Gabriel','opposition goalkeeper','opposition defender 0','opposition defender 1']}
 for sid in ['FR01','FR02','FR03_cross','FR03_complain','FR03_bonk','FR03_goal','FR04','FR05','N04_trophy']:
  s=scene(sid,True);E=s.frame_end;actors={}
  if sid in ['FR01','FR03_cross']:
   for name in cache[1]:actors[name]=player(name,s,cache[1][name]['loc'],n['actors'][name]['height'])
   gy=lead('Gyokeres',s,(1.65,48.4,0),1.89);actors['Gyokeres']=gy
   camera=cam(s,(-28,40,3.4),(-33,52,.9),5.7)
   for f in range(1,E+1):
    sf=1+int((f-1)*.50) if sid=='FR01' else 140+f-1;sf=min(269,sf)
    for name,a in actors.items():
     if name=='Gyokeres':pose(a,f,head=-.03*pulse(f,10,20,60));continue
     n['write_pose'](a,f,cache[sf][name]['p'],cache[sf][name]['loc'])
    if sid=='FR03_cross':
     u=smooth((f-28)/38);target=Vector((-33,52,.9)).lerp(Vector((-1,50,1.4)),u);loc=Vector((-28,40,3.4)).lerp(Vector((-1,36,3.7)),u);key(camera,'location',f,loc);key(camera,'rotation_euler',f,(target-loc).to_track_quat('-Z','Y').to_euler());key(camera.data,'ortho_scale',f,5.7+7*u)
  elif sid in ['FR03_complain','FR03_bonk','FR03_goal']:
   gy=make('Gyokeres rear',s,(1.35,48.7,0),1.89,sheet='gyokeres-rear.png');actors['Gyokeres']=gy
   gab=player('Gabriel',s,(-.7,49.1,0),1.90);keeper=player('opposition goalkeeper',s,(.9,52,0),1.86);d=player('opposition defender 0',s,(-2.2,49.5,0),1.83);actors.update(Gabriel=gab,keeper=keeper,defender=d)
   camera=cam(s,(1.5,38,2.2),(1.5,49,1),4.9 if sid!='FR03_goal' else 9.3)
   for f in range(1,E+1):
    react=pulse(f,7,12,23) if sid=='FR03_bonk' else 0;complaint=pulse(f,4,15,E-6) if sid=='FR03_complain' else 0;confused=smooth((f-16)/10) if sid=='FR03_goal' else 0
    pose(gy,f,lean=-.09*react,down=-.025*react,ua=(-.44*complaint-.24*confused,.27*complaint+.18*confused),fa=(-.6*complaint,.35*complaint),head=.035*complaint)
    sf=min(269,204+f) if sid=='FR03_complain' else 245;rec=cache[sf]['Gabriel'];p={k:v.copy() for k,v in rec['p'].items()}
    if sid!='FR03_complain':p=n['pose'](gab,ua=(-.22*confused,.22*confused),head=-.035*confused)
    n['write_pose'](gab,f,p,Vector((-.7,49.1,max(0,rec['loc'].z))) if sid=='FR03_complain' else Vector((-.7,49.1,0)))
    save=smooth((f-2)/10) if sid=='FR03_goal' else 0;pose(keeper,f,down=-.06,lean=-.12*save,ua=(-.3-.8*save,.3),fa=(-.35,.2),head=-.05*save);key(keeper['root'],'location',f,(.9-.75*save,52,0));pose(d,f,head=.04*confused,ua=(-.12*confused,.12*confused))
   if sid=='FR03_complain':speak(gy,'L39',lineframe(sid,'L39'))
  else:
   art=lead('Arteta',s,(-1.4,48.5,0),1.80);gy=lead('Gyokeres',s,(.55,48.5,0),1.89);actors.update(Arteta=art,Gyokeres=gy);cam(s,(-.4,37,2.0),(-.4,49,1),6.7)
   courier=make('Courier',s,(2.4,48.3,0),1.8,True) if sid=='FR05' else None;cart=trolley(s,3.1,48.2) if courier else None
   if courier:actors['Courier']=courier
   if sid=='N04_trophy':
    for i,name in enumerate(['Saka','Gabriel']):actors[name]=player(name,s,(-3.1 if i==0 else 2.3,49,0),1.85)
    trophy=flat(s,'champions trophy',(.55,48.0,1.25));b['poly'](s,'F23 trophy bowl',[(-.27,.75),(.27,.75),(.22,.39),(.08,.27),(.08,.12),(.24,.08),(.24,0),(-.24,0),(-.24,.08),(-.08,.12),(-.08,.27),(-.22,.39)],'#dfb33f',0,trophy,True)
    for side in [-1,1]:b['line'](s,'F23 trophy handle',[(side*.24,.68),(side*.43,.70),(side*.41,.40),(side*.21,.36)],'#f7d665',0,trophy,.032)
   for f in range(1,E+1):
    ask=pulse(f,6,16,70);order=pulse(f,78,88,E-5);celebrate=smooth((f-6)/16) if sid=='N04_trophy' else 0
    pose(art,f,ua=(-.12*ask-.52*order-.75*celebrate,.12*ask+.1*order+.68*celebrate),fa=(-.18*ask-.48*order-.65*celebrate,.15*ask+.48*celebrate),head=-.025*order,lean=.016*order)
    pose(gy,f,ua=(-.4*ask-.85*celebrate,.38*ask+.72*celebrate),fa=(-.5*ask-.6*celebrate,.5*ask+.6*celebrate),head=.03*ask,down=-.012*pulse(f,80,86,93))
    if sid=='N04_trophy':
     for name in ['Saka','Gabriel']:pose(actors[name],f,ua=(-.85*celebrate,.85*celebrate),fa=(-.65*celebrate,.65*celebrate),head=.04*math.sin(f*.09));key(trophy,'location',f,(.55,48.0,1.25+.68*celebrate))
    if courier:pose(courier,f,ua=(-.2*ask,.3*ask),fa=(-.25*ask,.45*ask),head=.04*ask)
   for name,ident in {'FR02':[('Gyokeres','L36'),('Arteta','L37')],'FR04':[('Gyokeres','L40'),('Arteta','L41')],'FR05':[('Courier','L42'),('Arteta','L43')]}.get(sid,[]):speak(actors[name],ident,lineframe(sid,ident))
  # Ball cloned from accepted dimensional ball; pose-independent object, explicit contacts.
  if sid in ['FR01','FR03_cross','FR03_complain','FR03_bonk','FR03_goal']:
   ball=q['ball'];mp=copy_objects([ball,*ball.children_recursive],s,'F23 '+sid+' ball');bb=mp[ball]
   for ob in mp.values():ob.animation_data_clear();ob.hide_render=ob.hide_viewport=False
   launch=Vector((-33.48,51.98,.11));arrive=Vector((1.48,48.53,.86));goal=Vector((2.65,54.35,.58))
   for f in range(1,E+1):
    if sid=='FR01':p=launch
    elif sid=='FR03_cross':
     u=max(0,min(1,(f-29)/65));p=launch.lerp(arrive,u);p.z+=2.5*4*u*(1-u);p.y+=1.3*math.sin(math.pi*u)
    elif sid=='FR03_complain':
     # Offscreen portion continues; foreground enters only at the end of the complaint.
     u=max(0,min(1,(f-(E-18))/26));p=Vector((-6,49.8,2.3)).lerp(arrive,u);p.z+=.25*math.sin(math.pi*u)
    elif sid=='FR03_bonk':
     if f<=8:p=Vector((-.9,49.05,1.30)).lerp(arrive,(f-1)/7)
     else:p=arrive.lerp(goal,(f-8)/40)
    else:
     u=min(1,(f+16)/40);p=arrive.lerp(goal,u)
     if f>24:p=goal+Vector((-.2*smooth((f-24)/15),-.24*smooth((f-24)/20),-.47*smooth((f-24)/28)))
    key(bb,'location',f,p);key(bb,'rotation_euler',f,(f*.11,f*.14,0))
   linear(bb)
  if sid in ['FR01','FR04','N04_trophy']:
   hud=flat(s,'final status',(-1,47.8,2.65));rect(s,hud,'score',-2.1,0,4.2,.45,'#1e2940');label(s,hud,'90+4     ARSENAL 0–0' if sid=='FR01' else '1  ARSENAL     2  CITY' if sid=='FR04' else 'ARSENAL — CHAMPIONS',0,.14,.20)
  finish(s)
 return list(S)

def ending(ids=None):
 src=bpy.data.scenes['S002_v008_Ferguson_dialogue'];intro=bpy.data.scenes['S002_B01_v016_narrator'];room=next(c for c in intro.collection.children if 'Narrator room' in c.name);native=next(c for c in src.collection.children if 'native artwork' in c.name)
 for sid in (ids or ['N03','N04_dark','N04_reveal','N04_meltdown','N04_tap']):
  s=scene(sid);s.collection.children.link(room);E=s.frame_end;source=intro if sid=='N03' else src;objects=[o for o in source.objects if o not in {z for z in (next(c for c in source.collection.children if 'Narrator room' in c.name)).all_objects} and o.type!='CAMERA'];mp=copy_objects(objects,s,sid);bpy.context.window.scene=source
  # Bake the already reviewed native whole-body performance, including cloth surfaces.
  samples=[];frames=[] if sid in ['N03','N04_meltdown'] else [1,E] if sid in ['N04_dark','N04_reveal'] else list(range(1,E+1))
  for f in frames:
   sf=f if sid in ['N03','N04_meltdown'] else 1 if sid in ['N04_dark','N04_reveal'] else int(n['sample'](f,[(1,57),(9,66),(15,81),(24,118),(38,156),(60,168)]))
   source.frame_set(sf);samples.append({o:(o.location.copy(),o.rotation_euler.copy(),o.scale.copy(),o.hide_render,o.hide_viewport,o.data.shape_keys.eval_time if o.type=='MESH' and o.data.shape_keys and not o.data.shape_keys.use_relative else None) for o in objects})
  bpy.context.window.scene=s
  for z in (mp.values() if samples else []):
   z.animation_data_clear()
   if z.type=='MESH' and z.data.shape_keys:z.data.shape_keys.animation_data_clear()
  for f,vals in zip(frames,samples):
   for old,(loc,rotation,scale,hr,hv,ev) in vals.items():
    z=mp[old]
    for prop,v in [('location',loc),('rotation_euler',rotation),('scale',scale),('hide_render',hr),('hide_viewport',hv)]:key(z,prop,f,v)
    if ev is not None:key(z.data.shape_keys,'eval_time',f,ev)
  if sid=='N03':
   c=source.camera.copy();c.data=source.camera.data.copy();c.animation_data_clear();c.data.animation_data_clear();s.collection.objects.link(c);s.camera=c
  else:
   c=source.camera.copy();c.data=source.camera.data.copy();c.animation_data_clear();c.data.animation_data_clear();s.collection.objects.link(c);s.camera=c
   if sid=='N04_tap':c.location=(-2.8,-4.8,2.45);c.rotation_euler=(Vector((1,-.1,1.25))-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=36
   if sid=='N04_dark':
    dark=b['mat']('#0d1520')
    for old,z in mp.items():
     if old.name in native.objects and z.type in ['MESH','CURVE']:z.data.materials.clear();z.data.materials.append(dark)
     if z.type=='LIGHT' and 'practical' in z.name:z.data.energy=0
    for f in range(1,E+1):key(c,'location',f,Vector(source.camera.location)+Vector((0,.28*smooth((f-1)/(E-1)),0)))
   if sid=='N04_tap':
    paper=flat(s,'crumpled resignation',(0,-.2,1.5));pts=[(.08*math.cos(i*math.tau/9)*(1+.18*(i%2)),.065*math.sin(i*math.tau/9)) for i in range(9)];b['poly'](s,'F23 crumpled notes',pts,'#eee8d2',0,paper,True)
    for f in range(1,E+1):
     if f<15:p=Vector((-.1,-.4,1.6))
     elif f<=32:u=(f-15)/17;p=Vector((-.1,-.4,1.6)).lerp(Vector((3.32,-1.1,1.68)),u);p.z+=.3*4*u*(1-u)
     else:u=min(1,(f-32)/19);p=Vector((3.32-.18*u,-1.1,1.68-1.64*u*u))
     key(paper,'location',f,p);key(paper,'rotation_euler',f,(math.pi/2,0,f*.13));key(paper,'scale',f,(1,1,1) if f>=15 else (0,0,0))
  for z in mp.values():
   for fc in curves(z):
    for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path.startswith('hide') else 'LINEAR'
  s.world=source.world;finish(s)
 return list(S)
