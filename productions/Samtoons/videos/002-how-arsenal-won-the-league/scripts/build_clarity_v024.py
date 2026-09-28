"""Scoped revision of saved v023 scenes. Execute in visible Blender, not a separate build."""
import bpy,ast,json,math,subprocess
import numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
V=Path(__file__).resolve().parents[1];O=V/'artifacts/clarity-v024';OLD=V/'artifacts/final-batch-v023'
def defs(file,names):
 tree=ast.parse((V/'scripts'/file).read_text());exec(compile(ast.Module(body=[f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name in names],type_ignores=[]),file,'exec'),globals())
defs('build_gyokeres_proof_v015.py',['curves','rotate','ik','smooth'])
defs('continue_batch02_v017.py',['mat','poly','line','empty','lips'])
def key(ob,prop,f,value):setattr(ob,prop,value);ob.keyframe_insert(data_path=prop,frame=f)
def linear(ob):
 for c in curves(ob):
  for k in c.keyframe_points:k.interpolation='CONSTANT' if c.data_path.startswith('hide') or 'pose_index' in c.data_path else 'LINEAR'
defs('reconstruct_defence_v021.py',['pose','write_pose','projected_knee','step'])
b=dict(empty=empty,poly=poly,line=line,mat=mat,ik=ik)
defs('build_final_v023.py',['flat','rect','label','copy_objects','pulse'])
rows=json.loads((O/'edit.json').read_text());R={r['id']:r for r in rows};S={};A={}
def use(s):
 bpy.context.window.scene=s;s.frame_set(1)
 area=max(bpy.context.screen.areas,key=lambda a:a.width*a.height)
 if area.type!='VIEW_3D':area.type='VIEW_3D'
 area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_overlays=False

def setup():
 assert not bpy.app.background
 if bpy.context.screen.is_animation_playing:bpy.ops.screen.animation_cancel(restore_frame=False)
 # Copy only the new transition; the previous saved revision remains unchanged on disk.
 bpy.context.window.scene=bpy.data.scenes['S002_final_v023_VH04_mikel'];bpy.ops.scene.new(type='FULL_COPY');cp=bpy.context.scene;cp.name='S002_clarity_v024_CP00'
 for r in rows:
  s=cp if r['id']=='CP00' else bpy.data.scenes[r['source_scene']];s.name=r['scene'];S[r['id']]=s;s.frame_end=r['frames'];s.render.use_sequencer=False
  for arm in [o for o in s.objects if o.type=='ARMATURE']:
   skin=next((o for o in s.objects if o.type=='MESH' and any(m.type=='ARMATURE' and m.object==arm for m in o.modifiers) and len(o.data.vertices)>1000),None)
   if skin is None:continue
   C={};rest={}
   for pb in arm.pose.bones:
    bb=arm.data.bones[pb.name]
    for c in pb.constraints:
     if c.type not in ['COPY_LOCATION','STRETCH_TO'] or not c.target:continue
     name=c.target.name.split('CTRL ')[-1].split('.')[0];C[name]=c.target;rest[name]=(bb.head_local if c.type=='COPY_LOCATION' else bb.tail_local).copy()
   root=arm.parent;name=next((x for x in ['Gyokeres rear','Gyokeres','Arteta','Referee','Operator','Courier','opposition goalkeeper','opposing attacker','Gabriel','Saka','opposition defender 0','opposition defender 1'] if x in root.name),root.name)
   if len(C)<19:continue
   A[r['id']+' / '+name]=dict(name=name,s=s,root=root,skin=skin,arm=arm,C=C,rest=rest,objects=[root,*root.children_recursive],height=abs(root.scale.y)*1.8,base=root.location.copy(),face=math.pi if root.scale.x<0 else 0)
 use(S['CP00']);bpy.app.driver_namespace['clarity24']=globals();return {'scenes':len(S),'actors':len(A)}
def actor(sid,name):return A[sid+' / '+name]
def reach(a,p,side,target,pole=None,finger=Vector((0,.085,0))):
 r=a['rest'];sh=p[side+'shoulder'];l1=(r[side+'elbow']-r[side+'shoulder']).length;l2=(r[side+'wrist']-r[side+'elbow']).length;d=target-sh
 if d.length>l1+l2-.004:target=sh+d.normalized()*(l1+l2-.004)
 # Project the upper arm into depth when a folded hand approaches its shoulder.
 if d.length<=abs(l1-l2)+.006:
  if l1>l2:l1=l2+d.length*.75
  else:l2=l1+d.length*.75
 p[side+'elbow']=ik(sh,target,l1,l2,pole or sh+Vector((-.20 if side=='L' else .20,-.25,0)));p[side+'wrist']=target;p[side+'finger']=target+finger.normalized()*(r[side+'finger']-r[side+'wrist']).length

def talk(sid,name):
 a=actor(sid,name);s=S[sid];use(s);entries=[e for e in R[sid]['dialogue'] if e['role'].replace('Ö','O').lower()==name.lower()]
 if name=='Gyokeres rear':entries=[e for e in R[sid]['dialogue'] if e['role']=='GYÖKERES']
 if entries:lips(a,[(e['id'],e['frame']) for e in entries],clear=True)
def dialogue():
 for sid in ['CP00','CP04_courier','VH03','VH03_answer','VH04_mikel','VH04_operator','VH04_two','VH04_button','VH05','FR02','FR03_complain','FR04','FR05']:
  s=S[sid];use(s)
  for a in [a for a in A.values() if a['s']==s]:
   if a['name'] in ['opposition goalkeeper','Gabriel','opposition defender 0'] and sid=='FR03_complain':
    for f in range(1,s.frame_end+1):write_pose(a,f,pose(a),Vector((a['base'].x,a['base'].y,0)))
    continue
   if a['name'] not in ['Arteta','Gyokeres','Gyokeres rear','Operator','Courier']:continue
   entries=[e for e in R[sid]['dialogue'] if e['role'].replace('Ö','O').lower() in a['name'].lower()];phone=next((ob for ob in s.objects if ob.name.startswith('F23 hand phone')),None) if a['name'] in ['Arteta','Operator'] and sid not in ['FR02','FR04','FR05'] else None
   for f in range(1,s.frame_end+1):
    g=max([pulse(f,e['frame'],e['frame']+8,e['frame']+min(38,int(e['seconds']*24))) for e in entries]+[0]);g2=max([pulse(f,e['frame']+42,e['frame']+50,e['frame']+77) for e in entries if e['seconds']>3.6]+[0]);p=pose(a,ua=(-.18-.30*g-.18*g2,.10+.2*g),fa=(-.20-.42*g,.08+.20*g),head=.025*g-.018*g2,lean=.012*g)
    if phone and sid!='VH03':
     target=p['neck']+Vector((.46,-.075,0));reach(a,p,'R',target);key(phone,'location',f,target+Vector((-.01,.035,.02)));key(phone,'scale',f,(1.35,1.65,1))
    if sid=='VH04_button':
     press=pulse(f,1,9,24);target=a['rest']['Lwrist'].lerp(Vector((-.40,1.045,0)),press);reach(a,p,'L',target,finger=Vector((0,-.08,0)))
    if sid=='CP00':
     target=p['neck']+Vector((.46,-.075,0));reach(a,p,'R',target)
    write_pose(a,f,p)
   talk(sid,a['name'])
  if sid=='FR03_complain':
   for o in s.objects:
    if 'ball /' in o.name:o.hide_render=True;o.animation_data_clear()
  if sid in ['VH03','VH03_answer','VH04_operator','VH04_button']:
   # Header and near-side button share one layout in every office angle.
   for o in s.objects:
    if o.type=='FONT' and o.data.body=='VAR':o.data=o.data.copy();o.data.body='VAR ROOM';o.location.y=3.10;o.data.size=.32
    if o.name.startswith('F23 play on button'):o.location.x=-.58
   s.camera.location.z+=.30;s.camera.data.ortho_scale=6.5
  for a in [a for a in A.values() if a['s']==s]:
   for ob in a['C'].values():linear(ob)
 # On-screen notification links the accepted defence ending with the literal title race.
 s=S['CP00'];p=flat(s,'City pursuit context',(-.4,48.65,2.1));rect(s,p,'City notification',-1.1,0,2.2,.42,'#7ec2de');label(s,p,'CITY WIN — STILL CHASING',0,.15,.135,'#102938');s.camera.data.ortho_scale=4.5
 return {'dialogue_scenes':14}

def chase():
 for sid in ['CP01','CP02_far','CP02_near','CP03_panic','CP03_pep','CP04_courier','CP04_reply','CP05']:
  s=S[sid];use(s);E=s.frame_end;pep=next(o for o in s.objects if o.parent is None and 'Pep travel' in o.name);travelroots=[o for o in s.objects if o.parent is None and ' travel' in o.name and o!=pep];camera=s.camera
  # Extend actual cadence, never stretch a short run to fill longer speech.
  allobs=[pep,*pep.children_recursive,*[o for r in travelroots for o in [r,*r.children_recursive]]];cache=[]
  for f in range(1,33):
   s.frame_set(f);cache.append({o:(o.location.copy(),o.get('pose_index'),{k.name:k.value for k in o.data.shape_keys.key_blocks} if o.type=='MESH' and o.data.shape_keys else {}) for o in allobs})
  for f in range(1,E+1):
   ph=(f-1)%32;travel=3.9*(f-1)/24
   for o in allobs:
    p,idx,shapes=cache[(f-1)%28 if o==pep or o in pep.children_recursive else ph][o];loc=p.copy()
    if o in travelroots:loc.x+=3.9*((f-1)-ph)/24
    if o==pep:
     o.scale=(1.12,)*3;loc.x=(1.14*(f-1)/24 if sid=='CP03_pep' else travel-(6.7 if sid in ['CP01','CP02_far'] else 3.5));loc.y=.02;loc.z=p.z*(1.12/.72 if sid!='CP03_pep' else 1.12)
    if o in travelroots or o==pep:key(o,'location',f,loc)
    if idx is not None:o['pose_index']=idx;o.keyframe_insert(data_path='["pose_index"]',frame=f)
    for kn,val in shapes.items():
     if kn!='Basis':key(o.data.shape_keys.key_blocks[kn],'value',f,val)
   if sid=='CP04_courier':
    # Keep the exchange within one visible encounter; performance continues while the group passes.
    cx=min(travel+1.0,7.0);key(camera,'location',f,(cx,-12,1.45));camera.data.ortho_scale=14
   else:
    cx=1.14*(f-1)/24+.2 if sid=='CP03_pep' else travel+(.05 if sid in ['CP01','CP02_far','CP02_near','CP05'] else 2.1);key(camera,'location',f,(cx,-12,1.45))
  for ob in [camera,*allobs]:linear(ob)
  for o in s.objects:
   if o.type=='FONT' and o.data.body in ['MARCH','APRIL','MAY']:o.data=o.data.copy();o.data.body='TITLE RUN-IN'
  if sid=='CP04_courier':
   for o in s.objects:
    if o.type=='FONT' and o.data.body=='RUNNERS-UP':o.data=o.data.copy();o.data.body='SECOND PLACE\nARSENAL';o.data.size=.10
 return {'Pep':'full adult scale, same ground plane; no tiny background proxy'}

def referee_and_foul():
 for sid in ['VH01','VH02','VH05']:
  s=S[sid];use(s);a=actor(sid,'Referee');E=s.frame_end
  for f in range(1,E+1):
   hear=smooth((f-85)/10) if sid=='VH01' else 1.;announce=pulse(f,42,49,84) if sid=='VH01' else 0;corner=smooth((f-205)/12) if sid=='VH05' else 0;p=pose(a,head=.015*math.sin(f*.04),ua=(0,-.10),fa=(0,0))
   if hear:target=p['neck']+Vector((-.40,.015,0));reach(a,p,'L',p['Lwrist'].lerp(target,hear),finger=Vector((.04,.08,0)))
   if announce:target=p['Rshoulder']+Vector((.38,-.30,0));reach(a,p,'R',p['Rwrist'].lerp(target,announce),finger=Vector((.07,-.05,0)))
   if corner:reach(a,p,'R',p['Rshoulder']+Vector((.45,.10,0)),finger=Vector((.08,.02,0)))
   write_pose(a,f,p)
  talk(sid,'Referee')
  if sid=='VH05':
   for o in s.objects:
    if o.type=='FONT' and o.data.body=='PLAY ON':o.data=o.data.copy();o.data.body='NO PENALTY\nARSENAL CORNER';o.data.size=.135
  for ob in a['C'].values():linear(ob)
 s=S['VH01'];use(s);gab=actor('VH01','Gabriel');opp=actor('VH01','opposing attacker');skin=opp['skin'];sk=skin.data.shape_keys
 if not sk:skin.shape_key_add(name='Basis')
 else:sk.key_blocks[0].name='Basis'
 shape=skin.data.shape_keys.key_blocks.get('Shirt pulled taut') or skin.shape_key_add(name='Shirt pulled taut');basis=skin.data.shape_keys.key_blocks['Basis'];sh=opp['rest']['Lshoulder'];el=opp['rest']['Lelbow']
 # Deform the actual shirt shoulder, then make the defender's wrist track that surface.
 for i,v in enumerate(basis.data):
  d=(v.co-Vector((sh.x+.08,sh.y-.12,0))).length;w=max(0,1-d/.18);shape.data[i].co.x-=.09*w
 target_index=min(range(len(basis.data)),key=lambda i:(basis.data[i].co-Vector((sh.x+.04,sh.y-.09,0))).length)
 for f in range(1,s.frame_end+1):
  pull=pulse(f,5,20,38);fall=smooth((f-22)/17)*(1-smooth((f-105)/25));p=pose(opp,lean=-.55*fall,down=-.31*fall,ua=(-.5*fall,.7*fall),fa=(-.25*fall,.5*fall));write_pose(opp,f,p,Vector((-1-.16*pull,49.25,-.10*fall)));key(shape,'value',f,pull);s.frame_set(f);bpy.context.view_layer.update();ev=skin.evaluated_get(bpy.context.evaluated_depsgraph_get());point=skin.matrix_world@ev.data.vertices[target_index].co;p=pose(gab,lean=.03*pull,ua=(0,.13),fa=(0,.3));target=gab['root'].matrix_world.inverted()@point;reach(gab,p,'R',p['Rwrist'].lerp(target,smooth((f-1)/6)*(1-smooth((f-35)/9))),finger=Vector((.03,-.06,0)));write_pose(gab,f,p)
 for a in [gab,opp]:
  for ob in [a['root'],*a['C'].values()]:linear(ob)
 return {'foul':'shirt deformation, tracked grab, visible loss of balance and spot signal','referee':'source-length constrained arm, outward/lower elbow'}

def preview(sid,f):
 s=S[sid];use(s);s.frame_set(f);s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(O/'review-frames'/f'{sid}-{f:04}.png');bpy.ops.render.render(write_still=True);return s.render.filepath

def save():
 bpy.data.libraries.write(str(O/'clarity-v024.blend'),set(S.values()),fake_user=True,compress=True);return str(O/'clarity-v024.blend')
bpy.app.driver_namespace['clarity24']=globals()

# Contextual hands use the accepted local drawing-swap technique. Arm controls alone
# cannot turn a permanently open palm into an earpiece touch or a phone grip.
def hand_drawing(a,side,kind):
 import bmesh
 s=a['s'];skin=a['skin'];r=a['rest'];wr=r[side+'wrist'];direction=(r[side+'finger']-wr).normalized();tag='C24 '+s.name+' '+a['name']+' '+side
 existing=bpy.data.objects.get(tag+' '+kind)
 if existing:return existing,bpy.data.objects[tag+' original hand']
 source=skin.copy();source.data=skin.data.copy();source.name=tag+' original hand';s.collection.objects.link(source)
 def selected(face):
  p=face.calc_center_median();return (p-wr).length<.24 and (p-wr).dot(direction)>-.055 and (p.x<-.27 if side=='L' else p.x>.27)
 for ob,keep in [(source,True),(skin,False)]:
  bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.delete(bm,geom=[f for f in bm.faces if selected(f)!=keep],context='FACES_ONLY');bm.to_mesh(ob.data);bm.free()
 root=empty(s,tag+' '+kind,a['root']);color='#ffc18b'
 if kind=='point':
  pts=[(-.027,-.025),(.027,-.025),(.034,.026),(.034,.128),(.030,.139),(.021,.142),(.013,.138),(.011,.128),(.011,.065),(-.004,.074),(-.015,.073),(-.025,.065),(-.032,.049),(-.035,.024)]
  creases=[[(.013,.064),(-.003,.045),(-.022,.044)],[(-.029,.030),(-.010,.027),(.009,.035)]]
 elif kind=='earpiece':
  pts=[(-.030,-.027),(.027,-.027),(.038,.018),(.046,.042),(.044,.064),(.034,.070),(.025,.060),(.022,.039),(.014,.046),(.015,.123),(.011,.139),(.003,.142),(-.005,.137),(-.009,.117),(-.011,.065),(-.017,.124),(-.025,.131),(-.033,.126),(-.036,.114),(-.032,.045),(-.043,.056),(-.052,.052),(-.054,.042),(-.044,.025),(-.035,.012)]
  creases=[[(-.029,.060),(-.015,.055),(-.010,.039)],[(.029,.059),(.027,.032),(.014,.018)]]
 elif kind=='phone grip':
  pts=[(-.031,-.025),(.029,-.025),(.038,.015),(.052,.036),(.052,.058),(.044,.063),(.035,.057),(.032,.039),(.016,.058),(.019,.112),(.014,.123),(.004,.124),(-.006,.116),(-.022,.115),(-.035,.103),(-.041,.080),(-.042,.035)]
  creases=[[(-.033,.092),(-.006,.088),(.012,.092)],[(-.037,.071),(-.007,.068),(.014,.072)],[(-.039,.050),(-.010,.047),(.014,.050)]]
 else:
  pts=[(-.030,-.026),(.029,-.026),(.037,.016),(.039,.059),(.031,.083),(.016,.094),(-.009,.094),(-.029,.082),(-.040,.056),(-.039,.025)]
  creases=[[(-.027,.074),(.014,.070),(.030,.050)],[(-.020,.050),(.005,.044),(.018,.047)]]
 pts[0]=(pts[0][0],-.085);pts[1]=(pts[1][0],-.085)
 poly(s,tag+' hand surface',pts,color,.032,root,False);line(s,tag+' hand contour',pts[1:]+[pts[0]],'#47362a',.034,root,.0023)
 poly(s,tag+' hand shade',[(-.03,-.02),(-.027,.033),(-.014,.068),(-.031,.06),(-.038,.025)],'#e6a36d',.033,root,False)
 for pp in creases:line(s,tag+' finger folds',pp,'#94643f',.035,root,.0014)
 return root,source

def contextual_hands():
 # Referee fingertip contact is authored in the same space as the moving head.
 for sid in ['VH01','VH02','VH05']:
  a=actor(sid,'Referee');s=S[sid];use(s);h,old=hand_drawing(a,'L','earpiece')
  for f in range(1,s.frame_end+1):
   s.frame_set(f);p={k:o.location.copy() for k,o in a['C'].items()};t=smooth((f-85)/10) if sid=='VH01' else 1.;target=p['neck']+Vector((-.14,.045,0));p['Lelbow']=p['Lelbow'].lerp(p['Lshoulder']+Vector((-.055,-.13,0)),t);p['Lwrist']=p['Lwrist'].lerp(target,t);p['Lfinger']=p['Lwrist']+Vector((.035,.105,0));write_pose(a,f,p)
   key(h,'location',f,p['Lwrist']);key(h,'rotation_euler',f,(0,0,-.25));key(h,'scale',f,(1,1,1) if t>.15 else (0,0,0));key(old,'hide_render',f,t>.15);key(old,'hide_viewport',f,t>.15)
  linear(old);linear(h)
 # All close telephone scenes need a grip; the phone occludes the fingers wrapping
 # behind it, while the thumb sits in front. No open-palm drawing behind the handset.
 for sid,name in [('CP00','Arteta'),('VH03_answer','Operator'),('VH04_mikel','Arteta'),('VH04_operator','Operator'),('VH04_two','Arteta'),('VH04_button','Operator')]:
  a=actor(sid,name);s=S[sid];use(s);h,old=hand_drawing(a,'R','phone grip');old.hide_render=old.hide_viewport=True
  phone=next(o for o in s.objects if o.name.startswith('F23 hand phone'))
  for f in range(1,s.frame_end+1):
   s.frame_set(f);wr=a['C']['Rwrist'].location.copy();key(h,'location',f,wr);key(phone,'location',f,wr+Vector((-.012,.025,.025)));key(phone,'scale',f,(1.0,1.3,1))
  # Thumb overlays the near edge of the phone, completing the grip silhouette.
  poly(s,'C24 '+sid+' thumb over phone',[(.008,.038),(.030,.045),(.040,.062),(.038,.072),(.030,.076),(.021,.069),(.014,.052)],'#ffc18b',.078,h,True)
  linear(h);linear(phone)
 return {'hands':'earpiece fingers and wrapped phone grip replace the open source palm'}

def foul_fall():
 s=S['VH01'];use(s);gab=actor('VH01','Gabriel');opp=actor('VH01','opposing attacker');skin=opp['skin'];basis=skin.data.shape_keys.key_blocks['Basis'];shape=skin.data.shape_keys.key_blocks['Shirt pulled taut'];sh=opp['rest']['Lshoulder'];ix=min(range(len(basis.data)),key=lambda i:(basis.data[i].co-Vector((sh.x+.04,sh.y-.09,0))).length)
 h,old=hand_drawing(gab,'R','shirt grip')
 for f in range(1,s.frame_end+1):
  fall=smooth((f-23)/20);p=pose(opp,ua=(-.45*fall,.60*fall),fa=(-.30*fall,.4*fall),head=-.08*fall);write_pose(opp,f,p,Vector((-1-.12*pulse(f,6,18,28),49.25,.17*fall)));key(opp['root'],'rotation_euler',f,(math.pi/2,1.42*fall,0));key(shape,'value',f,pulse(f,5,20,30));s.frame_set(f);bpy.context.view_layer.update();ev=skin.evaluated_get(bpy.context.evaluated_depsgraph_get());point=ev.matrix_world@ev.data.vertices[ix].co
  p=pose(gab,lean=-.025*pulse(f,8,20,35),ua=(0,.05));t=smooth((f-2)/7)*(1-smooth((f-26)/8));target=gab['root'].matrix_world.inverted()@point;reach(gab,p,'R',p['Rwrist'].lerp(target,t),finger=Vector((.04,.02,0)));write_pose(gab,f,p);key(h,'location',f,p['Rwrist']);key(h,'rotation_euler',f,(0,0,-math.pi/2));on=8<=f<=29;key(h,'scale',f,(1,1,1) if on else (0,0,0));key(old,'hide_render',f,on);key(old,'hide_viewport',f,on)
 for ob in [opp['root'],h,old,*opp['C'].values(),*gab['C'].values()]:linear(ob)
 return {'fall_frames':[23,43],'shirt_contact_frames':[9,26]}

def winning_corner():
 s=S['FR03_cross'];use(s);old=actor('FR03_cross','Gyokeres')
 for ob in old['objects']:ob.animation_data_clear();ob.hide_render=ob.hide_viewport=True
 src=actor('FR03_complain','Gyokeres rear');mp=copy_objects(src['objects'],s,'C24 winning Gyokeres');gy=dict(src);gy.update(s=s,root=mp[src['root']],skin=mp[src['skin']],arm=mp[src['arm']],C={k:mp[v] for k,v in src['C'].items()},objects=list(mp.values()));A['FR03_cross / Gyokeres rear']=gy
 for ob in gy['objects']:
  if 'native mouth' in ob.name or 'native teeth' in ob.name:ob.animation_data_clear();ob.hide_render=ob.hide_viewport=True
 for f in range(1,s.frame_end+1):
  hit=pulse(f,64,68,81);surprise=smooth((f-65)/8);write_pose(gy,f,pose(gy,lean=-.08*hit,down=-.025*hit,ua=(-.12*surprise,.14*surprise),fa=(-.18*surprise,.18*surprise)),Vector((1.35,48.7,0)))
  for name in ['Gabriel','opposition defender 0','opposition defender 1']:
   a=actor('FR03_cross',name);write_pose(a,f,pose(a,ua=(-.08*surprise,.08*surprise),head=-.035*surprise),Vector((-.7 if name=='Gabriel' else (-2.2 if name.endswith('0') else -3.4),49.1,0)))
  keeper=actor('FR03_cross','opposition goalkeeper');save=smooth((f-66)/10);write_pose(keeper,f,pose(keeper,lean=-.12*save,down=-.08,ua=(-.35-.75*save,.3),fa=(-.35,.2)),Vector((.9-.7*save,52,0)))
 s.frame_set(64);bpy.context.view_layer.update();ev=gy['skin'].evaluated_get(bpy.context.evaluated_depsgraph_get());want=Vector((.125,.82,0));ix=min(range(len(gy['skin'].data.vertices)),key=lambda i:(gy['skin'].data.vertices[i].co-want).length);surface=ev.matrix_world@ev.data.vertices[ix].co;arrive=surface+Vector((0,-.11,0));launch=Vector((-33.48,51.98,.11));goal=Vector((2.65,54.35,.58));ball=next(o for o in s.objects if o.name.startswith('F23 FR03_cross ball / v019 match ball'));camera=s.camera
 for f in range(1,s.frame_end+1):
  if f<=64:
   u=max(0,min(1,(f-29)/35));p=launch.lerp(arrive,u);p.z+=2.1*4*u*(1-u);p.y+=.75*math.sin(math.pi*u)
  elif f<=85:p=arrive.lerp(goal,(f-64)/21)
  else:
   u=smooth((f-85)/24);p=goal+Vector((-.16*u,-.20*u,-.47*u))
  key(ball,'location',f,p);key(ball,'rotation_euler',f,(f*.13,f*.20,0))
  # Track the actual uninterrupted flight, opening out before impact for cause/effect.
  u=max(0,min(1,(f-29)/35));target=Vector((-33,52,.9)).lerp(Vector((.8,50.7,1.2)),u);loc=target+Vector((2.8*(1-u),-13,2.4));key(camera,'location',f,loc);key(camera,'rotation_euler',f,(target-loc).to_track_quat('-Z','Y').to_euler());key(camera.data,'ortho_scale',f,5.7+3.6*smooth((f-50)/14))
 for ob in [ball,camera,camera.data,*gy['C'].values()]:linear(ob)
 (O/'contact-checks.json').write_text(json.dumps(dict(release_frame=29,backside_frame=64,goal_frame=85,surface=list(surface),ball_center=list(arrive),surface_distance=(arrive-surface).length,ball_radius=.11,header_removed=True,airtime_seconds=(85-29)/24),indent=2))
 return {'direct_flight':[29,64,85],'surface':list(surface)}

def contact_cleanup():
 s=S['VH01'];use(s);a=actor('VH01','Referee')
 for f in range(1,96):
  s.frame_set(f);p={k:o.location.copy() for k,o in a['C'].items()};t=smooth((f-85)/10)
  if t==0:
   rp=pose(a);p['Lelbow']=rp['Lelbow'];p['Lwrist']=rp['Lwrist'];p['Lfinger']=rp['Lfinger']
  else:p['Lfinger']=p['Lwrist']+(a['rest']['Lfinger']-a['rest']['Lwrist']).lerp(Vector((.035,.105,0)),t)
  write_pose(a,f,p)
 # Rotate the complete falling body, then place its lowest contact above the field.
 a=actor('VH01','opposing attacker')
 for f in range(23,s.frame_end+1):
  s.frame_set(f);bpy.context.view_layer.update();pts=[a['root'].matrix_world@a['C'][k].location for k in ['Ltoe','Rtoe','Lankle','Rankle','Lfinger','Rfinger','Lelbow','Relbow','head']];low=min(p.z for p in pts);loc=a['root'].location.copy();loc.z+=max(0,.06-low);key(a['root'],'location',f,loc)
 # The title belongs on a dedicated room sign, separate from the screen graphics.
 for sid in ['VH03','VH03_answer','VH04_operator','VH04_button']:
  s=S[sid];textob=next(o for o in s.objects if o.type=='FONT' and o.data.body=='VAR ROOM');rect(s,textob.parent,'VAR room nameplate',-1.17,3.01,2.34,.48,'#142a3a',.012)
 return {'referee_rest_hand_restored':True,'fall_contact':'lowest toe/finger contact above field'}

def delivery_and_celebration():
 s=S['FR05'];use(s);cart=next(o for o in s.objects if o.name.startswith('F23 runner-up delivery'));art=actor('FR05','Arteta');courier=actor('FR05','Courier');s.camera.data.ortho_scale=8.4
 sign=flat(s,'Etihad destination',(2.45,48.1,2.45));rect(s,sign,'Etihad sign',-1.1,0,2.2,.48,'#7ec2de');label(s,sign,'ETIHAD PHARMACY  →',0,.17,.15,'#172936')
 for o in cart.children:
  if o.type=='FONT':o.data=o.data.copy();o.data.body='SECOND PLACE';o.data.size=.11
 start=next(e['frame'] for e in R['FR05']['dialogue'] if e['role']=='ARTETA')
 for f in range(1,s.frame_end+1):
  s.frame_set(f);p={k:o.location.copy() for k,o in art['C'].items()};g=pulse(f,start,start+10,s.frame_end-5);target=p['Rshoulder']+Vector((.47,.08,0));reach(art,p,'R',p['Rwrist'].lerp(target,g),finger=Vector((.1,.03,0)));write_pose(art,f,p);key(sign,'scale',f,(1,1,1) if f>=start else (0,0,0))
 linear(sign)
 # Reposition the complete winners, cup and platform together beside the true corner.
 s=S['N04_trophy'];use(s);delta=Vector((-29.9,3.0,.18));winners=[a for a in A.values() if a['s']==s];cup=next(o for o in s.objects if o.name.startswith('F23 champions trophy'));hud=next(o for o in s.objects if o.name.startswith('F23 final status'));cache={}
 for f in range(1,s.frame_end+1):
  s.frame_set(f);cache[f]={ob:ob.location.copy() for ob in [*[a['root'] for a in winners],cup]}
 for f,data in cache.items():
  for ob,loc in data.items():key(ob,'location',f,loc+delta)
 hud.location=(-30.3,51.0,2.95);s.camera.animation_data_clear();s.camera.data.animation_data_clear();s.camera.location=(-32.0,37.2,4.0);target=Vector((-31.1,52.1,1.30));s.camera.rotation_euler=(target-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=10.0
 # Stage is in the pitch beside the corner; quadrant and flag remain unobstructed.
 me=bpy.data.meshes.new('C24 corner stage');x0,x1,y0,y1,z=-33.35,-26.65,50.75,52.45,.18;vv=[(x0,y0,0),(x1,y0,0),(x1,y1,0),(x0,y1,0),(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)];me.from_pydata(vv,[],[(0,1,5,4),(1,2,6,5),(4,5,6,7)]);me.materials.append(mat('#a92f41'));stage=bpy.data.objects.new('C24 corner trophy platform',me);s.collection.objects.link(stage)
 # Replace this scene's static pole only. Other football scenes retain their flag.
 for name in ['v019 corner flag.002','v019 red flag.002']:
  ob=s.objects.get(name)
  if ob:
   for col in list(ob.users_collection):
    if col==s.collection:col.objects.unlink(ob)
 root=flat(s,'celebrating corner',(-34,52.5,0));pole=line(s,'C24 rooted corner pole',[(0,0),(0,.5),(0,1),(0,1.5)],'#fff4da',0,root,.018);cloth=empty(s,'C24 corner pennant',root);poly(s,'C24 champion pennant',[(0,0),(.48,-.16),(0,-.37)],'#d33445',.015,cloth,False)
 medal=empty(s,'C24 flag winners medal',root);line(s,'C24 medal ribbon',[(-.05,.15),(0,0),(.05,.15)],'#dcae38',.03,medal,.014);poly(s,'C24 gold medal',[(.065*math.cos(i*math.tau/24),-.05+.065*math.sin(i*math.tau/24)) for i in range(24)],'#f6cf53',.04,medal,True)
 art=actor('N04_trophy','Arteta');art['root'].scale.x=-abs(art['root'].scale.x);talk('N04_trophy','Arteta')
 for f in range(1,s.frame_end+1):
  wave=.13*math.sin((f-12)*.22)*smooth((f-8)/12);bend=.045*math.sin(f*.22);sp=pole.data.splines[0]
  for i,point in enumerate(sp.points):point.co=(wave*(i/3)**2,.5*i,.0,1);point.keyframe_insert(data_path='co',frame=f)
  key(cloth,'location',f,(wave,1.5,0));key(cloth,'rotation_euler',f,(0,0,bend));key(medal,'location',f,(wave*.6,1.05,0))
  # Address the flag with the near hand, then join the celebration.
  s.frame_set(f);p={k:o.location.copy() for k,o in art['C'].items()};g=pulse(f,12,24,82);reach(art,p,'R',p['Rshoulder']+Vector((.34+.08*g,.13+.04*g,0)),finger=Vector((.07,.045,0)));write_pose(art,f,p)
 for ob in [cloth,medal,*[a['root'] for a in winners],cup]:linear(ob)
 return {'delivery':'Etihad Pharmacy sign; addressed courier','celebration':'whole team and cup on corner-side platform; rooted flag celebrates with a medal'}

def extend_ferguson():
 s=S['N04_meltdown'];use(s);obs=[o for o in s.objects if o.animation_data or o.type=='MESH' and o.data.shape_keys];cache={}
 for f in range(1,169):
  s.frame_set(f);cache[f]={o:(o.location.copy(),o.rotation_euler.copy(),o.scale.copy(),o.hide_render,o.hide_viewport,o.data.shape_keys.eval_time if o.type=='MESH' and o.data.shape_keys and not o.data.shape_keys.use_relative else None) for o in obs}
 # Keep the attacks fast; extend expressive holds between the new clauses.
 knots=[(1,1),(52,52),(80,53),(112,85),(146,86),(183,123),(205,124),(249,168),(s.frame_end,168)]
 for f in range(1,s.frame_end+1):
  for (f0,v0),(f1,v1) in zip(knots,knots[1:]):
   if f<=f1:sf=v0+(v1-v0)*(f-f0)/(f1-f0);break
  i=max(1,min(168,int(sf)));j=min(168,i+1);t=sf-i
  for o,vals in cache[i].items():
   other=cache[j][o]
   for k,prop in enumerate(['location','rotation_euler','scale']):key(o,prop,f,vals[k].lerp(other[k],t) if hasattr(vals[k],'lerp') else tuple(a+(b-a)*t for a,b in zip(vals[k],other[k])))
   for k,prop in [(3,'hide_render'),(4,'hide_viewport')]:key(o,prop,f,vals[k])
   if vals[5] is not None:key(o.data.shape_keys,'eval_time',f,vals[5]+(other[5]-vals[5])*t)
 # Mouth selection follows the new take; body and cloth keep their shared source time.
 raw=subprocess.check_output(['/opt/homebrew/bin/ffmpeg','-v','error','-i',str(O/'voices/C46-mix.wav'),'-f','f32le','-ac','1','-ar','48000','-']);audio=np.frombuffer(raw,np.float32);env=np.array([np.sqrt(np.mean(audio[i:i+2000]**2)) for i in range(0,len(audio),2000)]);norm=max(float(np.percentile(env,85)),1e-6);start=next(e['frame'] for e in R['N04_meltdown']['dialogue']);words=json.loads((O/'word-analysis.json').read_text());ww=[w for seg in words.get('C46',{}).get('segments',[]) for w in seg.get('words',[])]
 mouth={o.name.split('CTRL mouth ')[-1]:o for o in s.objects if 'CTRL mouth ' in o.name}
 for f in range(1,s.frame_end+1):
  i=f-start;level=float(env[i]/norm) if 0<=i<len(env) else 0.;word=next((w['word'].strip().lower() for w in ww if w['start']<=max(0,i/24)<w['end']),'');kind='rest' if level<.13 else 'O' if word.strip('!.,') in ['won','corner','stop','now'] else 'A' if level>.65 else 'E'
  for name,root in mouth.items():
   for ob in [root,*root.children_recursive]:key(ob,'hide_render',f,name!=kind);key(ob,'hide_viewport',f,name!=kind)
 for ob in obs:linear(ob)
 return {'native_ferguson':'new 10-second take; shared cloth/body time; clause holds between fast attacks'}

def grounded_fall():
 s=S['VH01'];use(s);a=actor('VH01','opposing attacker');skin=a['skin'];im=next(n.image for n in skin.data.materials[0].node_tree.nodes if n.type=='TEX_IMAGE');w,h=im.size;pix=np.asarray(im.pixels[:],dtype=np.float32).reshape(h,w,4);uv=skin.data.uv_layers.active.data;valid=set()
 for loop in skin.data.loops:
  u,v=uv[loop.index].uv;x=max(0,min(w-1,int(u*w)));y=max(0,min(h-1,int(v*h)))
  if pix[y,x,3]>.6:valid.add(loop.vertex_index)
 assert len(valid)>100
 for f in range(24,s.frame_end+1):
  s.frame_set(f);p={k:o.location.copy() for k,o in a['C'].items()};t=smooth((f-36)/13)
  for name,point in [('Relbow',(.29,1.13,0)),('Rwrist',(.16,1.22,0)),('Rfinger',(.10,1.23,0))]:p[name]=p[name].lerp(Vector(point),t)
  for side in ['L','R']:
   p[side+'ankle'].x=p[side+'ankle'].x*(1-t)+p[side+'hip'].x*t
   p[side+'toe']=p[side+'ankle']+(a['rest'][side+'toe']-a['rest'][side+'ankle']).lerp(Vector((0,-.12,0)),t)
   projected_knee(a,p,side)
  write_pose(a,f,p);bpy.context.view_layer.update();ev=skin.evaluated_get(bpy.context.evaluated_depsgraph_get());low=min((ev.matrix_world@ev.data.vertices[i].co).z for i in valid);loc=a['root'].location.copy();loc.z+=.008-low;key(a['root'],'location',f,loc)
 linear(a['root']);return {'opaque_surface_ground_contact_checked':len(valid)}

def operator_listens():
 sid='VH03';s=S[sid];a=actor(sid,'Operator');use(s);h,old=hand_drawing(a,'L','earpiece');old.hide_render=old.hide_viewport=True
 for f in range(1,s.frame_end+1):
  p=pose(a,head=-.015);p['Lelbow']=p['Lshoulder']+Vector((-.065,-.13,0));p['Lwrist']=p['neck']+Vector((-.165,.06,0));p['Lfinger']=p['Lwrist']+Vector((.035,.105,0));write_pose(a,f,p);key(h,'location',f,p['Lwrist']);key(h,'rotation_euler',f,(0,0,-.25))
 return {'operator':'two-finger headset contact before VIP call'}

def trophy_hands():
 sid='N04_trophy';s=S[sid];a=actor(sid,'Gyokeres');use(s);hands={side:hand_drawing(a,side,'handle grip') for side in ['L','R']};cup=next(o for o in s.objects if o.name.startswith('F23 champions trophy'))
 for h,old in hands.values():old.hide_render=old.hide_viewport=True
 cache={}
 for f in range(1,s.frame_end+1):s.frame_set(f);cache[f]=cup.location.copy()
 for f in range(1,s.frame_end+1):
  s.frame_set(f);p={k:o.location.copy() for k,o in a['C'].items()};lift=.25*smooth((f-85)/16)
  for side,sgn in [('L',-1),('R',1)]:
   target=Vector((sgn*.255/1.05,(.99+.34+lift)/1.05,0));reach(a,p,side,target,finger=Vector((-sgn*.075,.015,0)));h,_=hands[side];key(h,'location',f,p[side+'wrist']);key(h,'rotation_euler',f,(0,0,sgn*math.pi/2));key(h,'scale',f,(.83,.83,1))
  write_pose(a,f,p);key(cup,'location',f,cache[f]+Vector((0,0,lift)))
 # Distinct cheers, rather than matching aeroplane arms for everyone.
 for name,side in [('Saka','L'),('Gabriel','R')]:
  a=actor(sid,name);h,old=hand_drawing(a,side,'cheering fist');old.hide_render=old.hide_viewport=True
  for f in range(1,s.frame_end+1):
   g=smooth((f-6)/13);pump=.06*math.sin(f*.23)*g;p=pose(a,ua=(-2.0*g if side=='L' else -.18*g,2.0*g if side=='R' else .18*g),fa=(-.25*g,.25*g),head=.025*math.sin(f*.09));write_pose(a,f,p);key(h,'location',f,p[side+'wrist']);direction=p[side+'finger']-p[side+'wrist'];key(h,'rotation_euler',f,(0,0,math.atan2(direction.y,direction.x)-math.pi/2))
 return {'cup':'closed hands around handles; late lift','cheers':'distinct raised fists'}

def match_hand_palette():
 # Sample the actual forearm artwork; substitutions inherit each actor's skin tone.
 checks=[]
 for a in A.values():
  roots=[o for o in a['s'].objects if o.type=='EMPTY' and o.name.startswith('C24 '+a['s'].name+' '+a['name']+' ')];
  if not roots:continue
  me=a['skin'].data;im=next(n.image for n in me.materials[0].node_tree.nodes if n.type=='TEX_IMAGE');w,h=im.size;pp=np.asarray(im.pixels[:],dtype=np.float32).reshape(h,w,4);uv=me.uv_layers.active.data;idx=a['skin'].vertex_groups['Rforearm'].index;vals=[]
  for loop in me.loops:
   v=me.vertices[loop.vertex_index]
   if any(g.group==idx and g.weight>.60 for g in v.groups):
    u,t=uv[loop.index].uv;px=pp[max(0,min(h-1,int(t*h))),max(0,min(w-1,int(u*w)))];
    if px[3]>.94 and px[0]>.2 and px[0]>px[2]*1.3:vals.append(px[:3])
  if not vals:continue
  rgb=np.median(vals,axis=0);color='#'+''.join(f'{int(round(x*255)):02x}' for x in rgb);shade='#'+''.join(f'{int(round(x*255*.83)):02x}' for x in rgb)
  for root in roots:
   for ob in root.children_recursive:
    if ob.type not in ['MESH','CURVE']:continue
    if any(x in ob.name for x in ['surface','thumb over phone']):ob.data.materials.clear();ob.data.materials.append(mat(color))
    elif 'hand shade' in ob.name:ob.data.materials.clear();ob.data.materials.append(mat(shade))
  checks.append(dict(actor=a['name'],scene=a['s'].name,color=color))
 (O/'hand-palette-checks.json').write_text(json.dumps(checks,indent=2));return checks

def settle_cup():
 s=S['N04_trophy'];use(s);a=actor('N04_trophy','Gyokeres');cup=next(o for o in s.objects if o.name.startswith('F23 champions trophy'));hands={side:bpy.data.objects['C24 '+s.name+' Gyokeres '+side+' handle grip'] for side in ['L','R']}
 for f in range(1,s.frame_end+1):
  s.frame_set(f);p={k:o.location.copy() for k,o in a['C'].items()};bottom=.82+.17*smooth((f-6)/16)+.10*smooth((f-85)/16)
  for side,sgn in [('L',-1),('R',1)]:
   reach(a,p,side,Vector((sgn*.255/1.05,(bottom+.34)/1.05,0)),finger=Vector((-sgn*.075,.015,0)));p[side+'elbow']=p[side+'shoulder']+Vector((sgn*.16,-.22,0));key(hands[side],'location',f,p[side+'wrist'])
  write_pose(a,f,p);key(cup,'location',f,(-29.35,51.35,bottom+.18))
 return {'cup':'continuous reachable grip; no accumulated offset'}

def pointing_hands():
 for sid,name,side,start,end in [('VH01','Referee','R',43,82),('VH05','Referee','R',206,R['VH05']['frames']),('FR05','Arteta','R',next(e['frame'] for e in R['FR05']['dialogue'] if e['role']=='ARTETA'),R['FR05']['frames']-5),('VH04_button','Operator','L',3,24)]:
  s=S[sid];use(s);a=actor(sid,name);h,old=hand_drawing(a,side,'point')
  for f in range(1,s.frame_end+1):
   s.frame_set(f);wr=a['C'][side+'wrist'].location.copy();direction=a['C'][side+'finger'].location-wr;key(h,'location',f,wr);key(h,'rotation_euler',f,(0,0,math.atan2(direction.y,direction.x)-math.pi/2));on=start<=f<=end;key(h,'scale',f,(1,1,1) if on else (0,0,0));key(old,'hide_render',f,on);key(old,'hide_viewport',f,on)
  linear(old);linear(h)
 return {'explicit_index_gestures':['penalty spot','corner signal','Etihad direction','VAR button']}

def natural_button_arm():
 s=S['VH04_button'];use(s);a=actor('VH04_button','Operator');h=bpy.data.objects['C24 '+s.name+' Operator L point']
 for f in range(1,s.frame_end+1):
  s.frame_set(f);p={k:o.location.copy() for k,o in a['C'].items()};t=pulse(f,1,9,24);neutral=pose(a);p['Lelbow']=neutral['Lelbow'].lerp(p['Lshoulder']+Vector((-.105,-.185,0)),t);p['Lwrist']=neutral['Lwrist'].lerp(Vector((-.40,1.15,0)),t);p['Lfinger']=p['Lwrist']+Vector((0,-.105,0));write_pose(a,f,p);key(h,'location',f,p['Lwrist']);key(h,'rotation_euler',f,(0,0,math.pi))
 return {'button':'elbow below shoulder; fingertip meets the near desk button'}

def attach_hand_edges():
 # The fitted skin's evaluated wrist edge, not only its control, owns the join.
 # Reuse the accepted v017 continuous wrist-attachment method for every new hand.
 report=[]
 for a in A.values():
  roots=[o for o in a['s'].objects if o.type=='EMPTY' and o.name.startswith('C24 '+a['s'].name+' '+a['name']+' ')]
  if not roots:continue
  skin=a['skin'];me=skin.data;im=next(n.image for n in me.materials[0].node_tree.nodes if n.type=='TEX_IMAGE');w,h=im.size;px=np.asarray(im.pixels[:],dtype=np.float32).reshape(h,w,4);uv=me.uv_layers.active.data;opaque=set()
  for lp in me.loops:
   u,v=uv[lp.index].uv
   if px[max(0,min(h-1,int(v*h))),max(0,min(w-1,int(u*w))),3]>.94:opaque.add(lp.vertex_index)
  use(a['s'])
  for hand in roots:
   side=hand.name.split(a['name']+' ')[-1][0];wr=a['rest'][side+'wrist'];direction=(a['rest'][side+'finger']-wr).normalized();normal=Vector((-direction.y,direction.x,0));ids=[i for i in opaque if -.080<(me.vertices[i].co-wr).dot(direction)<-.045 and abs((me.vertices[i].co-wr).dot(normal))<.07]
   if len(ids)<2:continue
   ends=[min(ids,key=lambda i:(me.vertices[i].co-wr).dot(normal)),max(ids,key=lambda i:(me.vertices[i].co-wr).dot(normal))];surf=next(o for o in hand.children if 'hand surface' in o.name);edge=next(o for o in hand.children if 'hand contour' in o.name)
   if not surf.data.shape_keys:surf.shape_key_add(name='Basis')
   sk=surf.data.shape_keys.key_blocks.get('Evaluated wrist join') or surf.shape_key_add(name='Evaluated wrist join');sk.value=1
   for f in range(1,a['s'].frame_end+1):
    a['s'].frame_set(f)
    if abs(hand.scale.x)<.01:continue
    bpy.context.view_layer.update();ev=skin.evaluated_get(bpy.context.evaluated_depsgraph_get());inv=hand.matrix_world.inverted();pts=sorted([inv@(ev.matrix_world@ev.data.vertices[i].co) for i in ends],key=lambda p:p.x)
    for j,point in enumerate(pts):
     sk.data[j].co=(point.x,point.y,.032);sk.data[j].keyframe_insert(data_path='co',frame=f);cp=edge.data.splines[0].points[-1 if j==0 else 0];cp.co=(point.x,point.y,.034,1);cp.keyframe_insert(data_path='co',frame=f)
   report.append(dict(actor=a['name'],scene=a['s'].name,hand=side,join_vertices=ends))
 (O/'hand-attachment-checks.json').write_text(json.dumps(report,indent=2));return report
