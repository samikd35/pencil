"""Scoped acting repair and next chronological training sequence; reuse the fitted complete cast."""
import bpy,math,json,bmesh
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
V=Path(__file__).resolve().parents[1];O=V/'artifacts/batch02-v017';O.mkdir(exist_ok=True)
n=bpy.app.driver_namespace.get('batch16')
if n is None:
 source=V/'scripts/rebuild_batch01_v016.py';n={'__file__':str(source)};exec(compile(source.read_text(),str(source),'exec'),n)
 for name,record in json.loads((V/'artifacts/batch01-v016/cast.json').read_text()).items():
  cfg=record['cfg'];u=1.8/(cfg['floor']-cfg['top'])
  def xy(p,cfg=cfg,u=u):return Vector(((p[0]-cfg['center'])*u,(cfg['floor']-p[1])*u,0))
  r={'hip':xy((cfg['center'],cfg['hip'])),'neck':xy(cfg['neck']),'head':xy(cfg['head'])}
  for side in ['L','R']:
   for label,point in zip(['shoulder','elbow','wrist','finger','hip','knee','ankle','toe'],cfg[side]):r[side+label]=xy(point)
  x0=min(x for x,y in cfg['outline'])-12;x1=max(x for x,y in cfg['outline'])+12;y0=cfg['top']-7;y1=cfg['floor']+16;pixels=[(x0+(x1-x0)*i/90,y0+(y1-y0)*j/164) for j in range(165) for i in range(91)];root=bpy.data.objects[record['root']];skin=bpy.data.objects[record['skin']]
  n['ACTORS'][name]={'name':name,'kind':'gyokeres' if 'Gyokeres' in name else 'arteta','s':bpy.data.scenes[record['scene']],'prefix':'B01 / '+name+' / ','P':'B16 / '+name+' / ','root':root,'rest':r,'C':{k:bpy.data.objects[v] for k,v in record['controls'].items()},'skin':skin,'arm':next(m.object for m in skin.modifiers if m.type=='ARMATURE'),'cfg':cfg,'xy':xy,'pixels':pixels,'mirror':record['mirror'],'height':abs(root.scale.y)*1.8}
 bpy.app.driver_namespace['batch16']=n
smooth=n['smooth'];curves=n['curves'];ik=n['defs']['ik']

def keys(ob,path,vals):
 for f,v in vals:setattr(ob,path,v);ob.keyframe_insert(data_path=path,frame=f)
 for fc in curves(ob):
  for kp in fc.keyframe_points:kp.interpolation='LINEAR'

def mat(color):
 key='B17 '+color
 if bpy.data.materials.get(key):return bpy.data.materials[key]
 rgb=[int(color[i:i+2],16)/255 for i in (1,3,5)];rgb=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb];m=bpy.data.materials.new(key);m.use_nodes=True;ns=m.node_tree.nodes;ns.clear();e=ns.new('ShaderNodeEmission');e.inputs[0].default_value=(*rgb,1);out=ns.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],out.inputs[0]);return m

def poly(s,name,pts,color,z,parent=None,outline=True):
 vv=[Vector((x,y,z)) for x,y in pts];tri=tessellate_polygon([vv]);idx={tuple(p):i for i,p in enumerate(vv)};me=bpy.data.meshes.new(name);me.from_pydata(vv,[],[tuple(v if isinstance(v,int) else idx[tuple(v)] for v in t) for t in tri]);me.materials.append(mat(color));ob=bpy.data.objects.new(name,me);s.collection.objects.link(ob);ob.parent=parent
 if outline:line(s,name+' ink',pts+[pts[0]],'#20232d',z+.001,parent,.0035)
 return ob

def line(s,name,pts,color,z,parent=None,width=.0035):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=width;d.resolution_u=1;sp=d.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,(x,y) in zip(sp.points,pts):p.co=(x,y,z,1)
 d.materials.append(mat(color));ob=bpy.data.objects.new(name,d);s.collection.objects.link(ob);ob.parent=parent;return ob

def empty(s,name,parent=None):
 ob=bpy.data.objects.new(name,None);s.collection.objects.link(ob);ob.parent=parent;return ob

def phone_fix():
 a=n['ACTORS']['opening Arteta'];s=a['s'];bpy.context.window.scene=s;n['animate']('opening Arteta');C=a['C'];r=a['rest'];phone=bpy.data.objects['B01 Arteta phone'];phone.animation_data_clear();l1=(r['Relbow']-r['Rshoulder']).length;l2=(r['Rwrist']-r['Relbow']).length;lh=(r['Rfinger']-r['Rwrist']).length
 for f in range(1,410):
  s.frame_set(f);t=smooth((f-329)/12)*(1-smooth((f-394)/15));sh=C['Rshoulder'].location.copy();wr=C['Rwrist'].location.copy();fi=C['Rfinger'].location.copy();el=C['Relbow'].location.copy()
  # Wrist stays outside the cheek, elbow below/outside the shoulder, never across the nose.
  target=C['neck'].location+Vector((.47,-.04,0));target_el=ik(sh,target,l1,l2,sh+Vector((.24,-.22,0)))
  if f>=329:
   def blend_angle(v,w,t):
    aa=math.atan2(v.y,v.x);bb=math.atan2(w.y,w.x);return aa+((bb-aa+math.pi)%(2*math.pi)-math.pi)*t
   aa=blend_angle(r['Relbow']-r['Rshoulder'],target_el-sh,t);bb=blend_angle(r['Rwrist']-r['Relbow'],target-target_el,t)
   elbow=sh+Vector((math.cos(aa),math.sin(aa),0))*l1;want=elbow+Vector((math.cos(bb),math.sin(bb),0))*l2
   cc=blend_angle(r['Rfinger']-r['Rwrist'],Vector((-.06,1,0)),t);finger=want+Vector((math.cos(cc),math.sin(cc),0))*lh
  else:elbow=el;want=wr;finger=fi
  for k,v in [('Relbow',elbow),('Rwrist',want),('Rfinger',finger)]:keys(C[k],'location',[(f,v)])
  phone.location=(want.x-.007,want.y+.09,.025);phone.scale=(.00298,)*3 if 338<=f<=402 else (0,0,0);phone.keyframe_insert(data_path='location',frame=f);phone.keyframe_insert(data_path='scale',frame=f)
 s.frame_set(356);return {'phone':'outside cheek, elbow below shoulder, fitted lengths'}

def point_fix():
 a=n['ACTORS']['unveiling Arteta'];s=a['s'];bpy.context.window.scene=s;C=a['C'];r=a['rest'];skin=a['skin'];P=a['P'];start,end=186,288
 # Isolate only the source hand, so the complete source stays untouched outside this gesture.
 hand=bpy.data.objects.get(P+'source left hand')
 if hand is None:
  hand=skin.copy();hand.data=skin.data.copy();hand.name=P+'source left hand';s.collection.objects.link(hand)
  def ishand(face):
   pts=[a['pixels'][v.index] for v in face.verts];return sum(p[0] for p in pts)/len(pts)<930 and 548<sum(p[1] for p in pts)/len(pts)<650
  for ob,keep in [(hand,True),(skin,False)]:
   bm=bmesh.new();bm.from_mesh(ob.data);bm.faces.ensure_lookup_table();dead=[f for f in bm.faces if ishand(f)!=keep];bmesh.ops.delete(bm,geom=dead,context='FACES_ONLY');bm.to_mesh(ob.data);bm.free()
 root=bpy.data.objects.get(P+'pointing hand') or empty(s,P+'pointing hand',a['root']);pts=[(-.008,-.023),(.052,-.025),(.073,-.019),(.082,-.008),(.079,.005),(.067,.013),(.062,.020),(.176,.020),(.186,.027),(.185,.034),(.176,.040),(.055,.039),(.045,.055),(.032,.062),(.016,.053),(.022,.035),(-.008,.026)]
 poly(s,P+'index extended',pts,a['cfg']['skin'],.021,root);poly(s,P+'knuckle shade',[(.024,-.021),(.066,-.018),(.077,-.006),(.062,.014),(.029,.017)],'#eaa36c',.022,root,False)
 for x in [.035,.050,.065]:line(s,P+'folded digit',[(x,-.017),(x+.008,-.004),(x+.002,.012)],'#775941',.023,root,.0017)
 l1=(r['Lelbow']-r['Lshoulder']).length;l2=(r['Lwrist']-r['Lelbow']).length;lh=(r['Lfinger']-r['Lwrist']).length
 for f in range(1,433):
  s.frame_set(f);t=smooth((f-175)/13)*(1-smooth((f-276)/17));sh=C['Lshoulder'].location.copy();wr=C['Lwrist'].location.copy();el=C['Lelbow'].location.copy();fi=C['Lfinger'].location.copy();target=sh+Vector((-.445,-.065,0));want=wr.lerp(target,t);d=want-sh
  if d.length>=l1+l2-.004:want=sh+d.normalized()*(l1+l2-.004)
  elbow=ik(sh,want,l1,l2,sh+Vector((-.20,-.22,0))) if t>.001 else el;direction=Vector((-1,.045,0)).normalized();finger=want+direction*lh
  if t>.001:
   for k,v in [('Lelbow',elbow),('Lwrist',want),('Lfinger',fi.lerp(finger,t))]:keys(C[k],'location',[(f,v)])
  root.location=want;root.rotation_euler.z=math.atan2(direction.y,direction.x);root.keyframe_insert(data_path='location',frame=f);root.keyframe_insert(data_path='rotation_euler',frame=f)
  for ob,hide in [(hand,start<=f<=end),(root,not(start<=f<=end))]:
   if ob==root:ob.scale=(0,0,0) if hide else (1,1,1);ob.keyframe_insert(data_path='scale',frame=f)
   else:ob.hide_render=ob.hide_viewport=hide;ob.keyframe_insert(data_path='hide_render',frame=f);ob.keyframe_insert(data_path='hide_viewport',frame=f)
 for ob in [hand,root]:
  for fc in curves(ob):
   if fc.data_path in ['scale','hide_render','hide_viewport']:
    for kp in fc.keyframe_points:kp.interpolation='CONSTANT'
 s.frame_set(204);return {'point':'extended index to number-nine corner flag; other fingers folded','source_hand_restored_after':end}

def snapshot():
 rows=json.loads((V/'artifacts/batch01-v016/edit.json').read_text());bpy.data.libraries.write(str(O/'batch01-revised-v017.blend'),{bpy.data.scenes[r['scene']] for r in rows},fake_user=True);(O/'batch01-edit.json').write_text(json.dumps(rows,indent=2))
 return {'saved':str(O/'batch01-revised-v017.blend')}

def clone_cast(source,s,name,x,y,mirror=False):
 src=n['ACTORS'][source];root=src['root'];obs=[root,*root.children_recursive];mapping={}
 for ob in obs:
  cp=ob.copy();cp.name='B17 / '+name+' / '+ob.name.split(' / ')[-1]
  if ob.data:cp.data=ob.data.copy()
  cp.animation_data_clear();s.collection.objects.link(cp);mapping[ob]=cp
 for ob,cp in mapping.items():
  cp.parent=mapping.get(ob.parent)
  if cp.data and hasattr(cp.data,'shape_keys') and cp.data.shape_keys:
   cp.data.shape_keys.animation_data_clear()
   for key in cp.data.shape_keys.key_blocks:key.value=0
  for mod in cp.modifiers:
   if mod.type=='ARMATURE':mod.object=mapping[mod.object]
  if cp.type=='ARMATURE':
   for pb in cp.pose.bones:
    for co in pb.constraints:
     if hasattr(co,'target') and co.target in mapping:co.target=mapping[co.target]
  if any(k in ob.name.lower() for k in ['native mouth','native teeth','phone']):cp.hide_render=cp.hide_viewport=True
 rr=mapping[root];rr.location=(x,y,1);rr.scale=((-.1 if mirror else .1)*src['height']/1.8*10,src['height']/1.8,src['height']/1.8)
 a=dict(src);a.update(name=name,s=s,root=rr,C={k:mapping[o] for k,o in src['C'].items()},skin=mapping[src['skin']],arm=mapping[src['arm']],objects=list(mapping.values()),mirror=mirror,P='B17 / '+name+' / ');return a

def pose_actor(a,f,ua=(0,0),fa=(0,0),hands=(0,0),lean=0,shift=(0,0),kick=0):
 r=a['rest'];p={k:v.copy() for k,v in r.items()};off=Vector((*shift,0));p['hip']+=off
 for k in ['neck','head','Lshoulder','Rshoulder']:p[k]=p['hip']+n['rotate'](r[k]-r['hip'],lean)
 for i,side in enumerate(['L','R']):
  p[side+'hip']+=off
  for label,prev,extra in [('elbow','shoulder',ua[i]),('wrist','elbow',ua[i]+fa[i]),('finger','wrist',ua[i]+fa[i]+hands[i])]:p[side+label]=p[side+prev]+n['rotate'](r[side+label]-r[side+prev],extra+lean)
  if side=='R' and kick:
   p['Rankle']+=Vector((.21*kick,.08*abs(kick),0));p['Rtoe']=p['Rankle']+n['rotate'](r['Rtoe']-r['Rankle'],.18*kick)
  top=p[side+'hip'];ankle=p[side+'ankle'];u=(r[side+'knee'].y-r[side+'hip'].y)/(r[side+'ankle'].y-r[side+'hip'].y);p[side+'knee']=top.lerp(ankle,u)+Vector(((-.01 if side=='L' else .01),.018*abs(kick) if side=='R' else 0,0))
 for k,v in p.items():a['C'][k].location=v;a['C'][k].keyframe_insert(data_path='location',frame=f)

def training():
 global TRAIN,TRAINCAST
 s=bpy.data.scenes.new('S002_B02_v017_training');TRAIN=s;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_end=300;s.render.use_sequencer=False;s.view_settings.view_transform='Standard';s.view_settings.look='None';s.world=bpy.data.scenes['S002_B01_v016_unveiling'].world;bpy.context.window.scene=s
 # Share the same training-ground environment; props and character animation stay local.
 env=bpy.data.collections['B01 / training ground shared'];s.collection.children.link(env)
 a=clone_cast('opening Arteta',s,'Arteta',-5.5,-2.9);g=clone_cast('unveiling Gyokeres',s,'Gyokeres',-1.0,-2.9);TRAINCAST={'Arteta':a,'Gyokeres':g}
 for f in range(1,301):
  s.frame_set(f);warn=smooth((f-5)/7)*(1-smooth((f-79)/12));proud=smooth((f-169)/8)*(1-smooth((f-223)/12));beat=.10*math.sin((f-181)*math.pi/8)*smooth((f-181)/4)*(1-smooth((f-211)/5))
  pose_actor(a,f,ua=(.10*proud,.68*warn+.22*proud),fa=(.18*proud,.42*warn+.65*proud),hands=(0,.35*warn),lean=-.018*warn+.018*proud,shift=(0,.005*beat))
  # Wind-up, single decisive strike and recovery; planted supporting foot never follows the kicking foot.
  if f<97:k=-.4*smooth((f-70)/20)
  elif f<=112:k=-.4+.75*smooth((f-97)/15)
  elif f<=119:k=.35+.55*smooth((f-112)/7)
  else:k=.9*(1-smooth((f-119)/22))
  react=smooth((f-18)/6)*(1-smooth((f-58)/8));pose_actor(g,f,ua=(.14*abs(k),-.18*abs(k)),fa=(-.12*react,.23*react),lean=-.025*abs(k),shift=(-.035*abs(k),-.018*abs(k)),kick=k)
 for a in TRAINCAST.values():
  for ob in a['C'].values():
   for fc in curves(ob):
    for kp in fc.keyframe_points:kp.interpolation='LINEAR'
 # Existing complete practice-defender illustration; native deformation, no pose cards.
 p=V/'scripts/build_film_animation_v004.py';lib={'__file__':str(p)};exec(compile(p.read_text(),str(p),'exec'),lib);lib['SCENE']=s;lib['load_sheet']('football',8);d=lib['actor']('football',[6],3.5,-2.9,4.7,1);TRAINCAST['defender_library']=lib;TRAINCAST['defender']=d
 # Goal remains visibly open: the absurdity is deliberately choosing the defender.
 lib['goal'](5.0,-2.8,4.0,3.3);flag=lib['flag'](7.8,-3.3,2.1)
 ball=lib['ball'](.55,-2.48,.19)
 # Ball and boot are registered at the same contact point before the launch.
 s.frame_set(112);bpy.context.view_layer.update();boot=g['root'].matrix_world@g['C']['Rtoe'].location;start=(boot.x+.19,-2.63);contact=(2.1,-2.34);end=(8.25,-3.67)
 path=[]
 for f in range(1,301):
  if f<113:p=start
  elif f<=124:u=(f-112)/12;p=(start[0]+(contact[0]-start[0])*u,start[1]+(contact[1]-start[1])*u+.10*math.sin(math.pi*u))
  elif f<=145:u=(f-124)/21;p=(contact[0]+(end[0]-contact[0])*u,contact[1]+(end[1]-contact[1])*u+.24*math.sin(math.pi*u))
  else:p=end
  path.append((f,(*p,0)))
 lib['move'](ball,path,'LINEAR');lib['keyed'](ball,'rotation_euler',[(1,(0,0,0)),(112,(0,0,0)),(145,(0,0,-9)),(300,(0,0,-9))],'LINEAR');lib['effect'](*contact,124)
 # The opponent recoils through his own mesh, while his far boot stays planted.
 for ob in d['parts'] if isinstance(d,dict) and 'parts' in d else []:pass
 # Isolated camera cuts preserve speed: wide warning, visible foot-ball contact, confident response, flag transition.
 def camera(name,x,y,width,frame):
  cd=bpy.data.cameras.new(name);cd.type='ORTHO';cd.ortho_scale=width;c=bpy.data.objects.new(name,cd);s.collection.objects.link(c);c.location=(x,y,40);m=s.timeline_markers.new(name,frame=frame);m.camera=c;return c
 s.camera=camera('B17 training warning',.4,.2,17.5,1);camera('B17 boot deflection',3.5,-1.0,12.3,97);camera('B17 calm authority',-5.3,.65,7.8,169);camera('B17 corner transition',7.6,-1.45,5.3,253)
 (O/'training-contacts.json').write_text(json.dumps({'boot_contact_frame':112,'ball_launch_frame':113,'defender_contact_frame':124,'byline_crossing_frame':145,'boot_contact_world':list(boot),'ball_start':list(start),'scope':'authored registration, visible contact review still required'},indent=2));s.frame_set(106);s.camera=next(m.camera for m in s.timeline_markers if m.frame==97);return {'scene':s.name,'frames':300}

def refine_point_hand():
 a=n['ACTORS']['unveiling Arteta'];s=a['s'];P=a['P'];root=bpy.data.objects[P+'pointing hand'];bpy.context.window.scene=s
 for ob in list(root.children):bpy.data.objects.remove(ob,do_unlink=True)
 # Coordinates below are a right-facing dorsal hand; compensate the mirrored
 # actor/180-degree hand frame exactly once. Index above curled fingers.
 def pts(pp):return [(x,-y) for x,y in pp]
 outline=[(-.023,.024),(.025,.032),(.055,.041),(.151,.041),(.158,.038),(.160,.032),(.156,.026),(.146,.024),(.083,.025),(.090,.012),(.089,.001),(.079,-.008),(.075,-.024),(.066,-.033),(.049,-.035),(.024,-.029),(-.023,-.023)]
 poly(s,P+'point hand',pts(outline),'#ffc18b',.022,root,False);line(s,P+'point silhouette',pts(outline),'#47362a',.023,root,.0025)
 poly(s,P+'palm shadow',pts([(.02,-.02),(.051,-.025),(.072,-.021),(.078,-.007),(.062,.003),(.040,-.009)]),'#eaa673',.023,root,False)
 line(s,P+'folded thumb',pts([(.027,.023),(.043,.014),(.064,.009),(.072,.002),(.067,-.007),(.058,-.009),(.036,-.002)]),'#94643f',.024,root,.0015)
 line(s,P+'curled middle',pts([(.080,.013),(.072,.007),(.067,.003)]),'#94643f',.024,root,.0013)
 line(s,P+'curled ring',pts([(.076,-.008),(.068,-.012),(.063,-.016)]),'#94643f',.024,root,.0013)
 s.frame_set(204);return {'native_hand':'index on top, folded fingers below, neutral wrist, open wrist contour joins source forearm'}

def lips(a,lines,clear=False):
 import numpy as np,subprocess
 s=a['s'];bpy.context.window.scene=s;obs=a.get('objects',list(a['root'].children_recursive));mo=next(o for o in obs if 'native mouth' in o.name);te=next(o for o in obs if 'native teeth' in o.name);sk=mo.data.shape_keys;closed=sk.key_blocks['Closed'];rounded=sk.key_blocks['Rounded'];words=json.loads((O/'word-analysis.json').read_text())
 if clear:
  mo.animation_data_clear();te.animation_data_clear();sk.animation_data_clear()
  for f in [1,s.frame_end]:
   for ob in [mo,te]:ob.hide_render=ob.hide_viewport=True;ob.keyframe_insert(data_path='hide_render',frame=f);ob.keyframe_insert(data_path='hide_viewport',frame=f)
 for ident,start in lines:
  raw=subprocess.check_output(['/opt/homebrew/bin/ffmpeg','-v','error','-i',str(O/'voices'/(ident+'-mix.wav')),'-f','f32le','-ac','1','-ar','48000','-']);audio=np.frombuffer(raw,np.float32);env=np.array([np.sqrt(np.mean(audio[i:i+2000]**2)) for i in range(0,len(audio),2000)]);scale=max(float(np.percentile(env,85)),1e-6);ww=[w for sg in words[ident]['segments'] for w in sg.get('words',[])]
  for j in range(-1,len(env)+2):
   f=start+j;level=float(env[j]/scale) if 0<=j<len(env) else 0.;word=next((w['word'].strip().lower() for w in ww if w['start']<=max(0,j/24)<w['end']),'');op=min(.88,.18+.60*level) if level>.12 else 0.;ro=1. if word.strip('.,!') in ['our','us','now','goal','off','corner'] else 0.
   # Word attacks with bilabials close briefly; opening follows the actual take.
   if word.startswith(('m','b','p')) and any(abs(j/24-w['start'])<.045 for w in ww):op=0
   closed.value=1-op;rounded.value=ro;closed.keyframe_insert(data_path='value',frame=f);rounded.keyframe_insert(data_path='value',frame=f)
   for ob in [mo,te]:ob.hide_render=ob.hide_viewport=op<.10 or (ob==te and ro>.5);ob.keyframe_insert(data_path='hide_render',frame=f);ob.keyframe_insert(data_path='hide_viewport',frame=f)
 for ob in [mo,te]:
  for fc in curves(ob):
   for kp in fc.keyframe_points:kp.interpolation='CONSTANT'
 for fc in curves(sk):
  for kp in fc.keyframe_points:kp.interpolation='LINEAR'
 return {'lines':lines,'timing':'actual new take envelope with timed word shapes; not phoneme-perfect'}

def defender_recoil():
 a=TRAINCAST['defender'];s=TRAIN;bpy.context.window.scene=s
 surface=next(o for o in a.children if o.type=='MESH');key=surface.shape_key_add(name='Shin hit and upper body recoil');base=surface.data.shape_keys.key_blocks['Basis']
 for src,dst in zip(base.data,key.data):
  p=src.co.copy();w=smooth((p.y-.5)/2.0);p.x+=.20*w;p.y-=.10*w;dst.co=p
 for f,v in [(1,0),(123,0),(127,1),(133,.8),(143,0),(300,0)]:key.value=v;key.keyframe_insert(data_path='value',frame=f)
 return {'recoil':'ankle stationary, hips/chest give after shin contact'}

def save_all():
 first=json.loads((V/'artifacts/batch01-v016/edit.json').read_text());second=[];cursor=1
 for row in json.loads((V/'artifacts/animation-v003/edit.json').read_text())[10:14]:
  r=dict(row);r.update(scene=TRAIN.name,local_start=cursor);second.append(r);cursor+=r['frames']
 assert cursor==301
 (O/'edit.json').write_text(json.dumps(first+second,indent=2));bpy.data.libraries.write(str(O/'batches01-02-v017.blend'),{bpy.data.scenes[r['scene']] for r in first+second},fake_user=True,compress=True);return {'frames':1321,'batch_two_frames':300,'native':str(O/'batches01-02-v017.blend')}

def connect_point_to_cuff():
 # Replace the exposed forearm and pointing hand as one surface for this gesture.
 # Its cuff endpoints follow the evaluated source sleeve, so there is no wrist patch seam.
 a=n['ACTORS']['unveiling Arteta'];s=a['s'];bpy.context.window.scene=s;root=bpy.data.objects[a['P']+'pointing hand'];ob=bpy.data.objects[a['P']+'point hand'];outline=bpy.data.objects[a['P']+'point silhouette'];idx=[min(range(len(a['pixels'])),key=lambda i:(a['pixels'][i][0]-x)**2+(a['pixels'][i][1]-y)**2) for x,y in [(907,488),(945,504)]]
 if not ob.data.shape_keys:ob.shape_key_add(name='Basis')
 key=ob.shape_key_add(name='Sleeve edge attachment');key.value=1
 for f in range(186,289):
  s.frame_set(f);bpy.context.view_layer.update();ev=a['skin'].evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();points=[root.matrix_world.inverted()@(a['skin'].matrix_world@me.vertices[i].co) for i in idx];ev.to_mesh_clear();points.sort(key=lambda p:p.y)
  for vi,point in [(0,points[0]),(len(ob.data.vertices)-1,points[1])]:
   key.data[vi].co=(point.x-.006,point.y,.026);key.data[vi].keyframe_insert(data_path='co',frame=f)
   cp=outline.data.splines[0].points[vi];cp.co=(point.x-.006,point.y,.027,1);cp.keyframe_insert(data_path='co',frame=f)
 # All surface points share the same draw plane at the join.
 for vi,p in enumerate(key.data):p.co.z=.026
 for child in root.children:
  if child not in [ob,outline]:child.location.z+=.006
 s.frame_set(204);return {'joined':'native exposed forearm+hand; cuff follows evaluated source garment'}


def stage_reveal_camera():
 s=n['ACTORS']['unveiling Arteta']['s'];camera=max((m for m in s.timeline_markers if m.camera and m.frame<=193),key=lambda m:m.frame).camera;camera.animation_data_clear();keys(camera,'location',[(193,(0,.4,40)),(227,(0,.4,40)),(262,(7.4,.4,40)),(288,(7.4,.4,40))])

def remove_point_overlap():
 # Both surfaces must not outline the same exposed forearm during the pointing swap.
 a=n['ACTORS']['unveiling Arteta'];skin=a['skin'];s=a['s'];cp=skin.copy();cp.data=skin.data.copy();cp.name=a['P']+'source exposed forearm';cp.animation_data_clear();s.collection.objects.link(cp)
 def exposed(face):
  pp=[a['pixels'][v.index] for v in face.verts];x=sum(p[0] for p in pp)/len(pp);y=sum(p[1] for p in pp)/len(pp);return x<975 and 488+(x-907)*16/38<y<650
 for ob,keep in [(cp,True),(skin,False)]:
  bm=bmesh.new();bm.from_mesh(ob.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[f for f in bm.faces if exposed(f)!=keep],context='FACES_ONLY');bm.to_mesh(ob.data);bm.free()
 for f,hide in [(1,False),(186,True),(289,False)]:
  cp.hide_render=cp.hide_viewport=hide;cp.keyframe_insert(data_path='hide_render',frame=f);cp.keyframe_insert(data_path='hide_viewport',frame=f)
 for fc in curves(cp):
  for k in fc.keyframe_points:k.interpolation='CONSTANT'
 return {'overlap_removed':True}
