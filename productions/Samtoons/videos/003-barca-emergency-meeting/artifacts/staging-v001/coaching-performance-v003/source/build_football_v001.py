"""S06 native drawn football performance in the existing dimensional set.
Author setup/actor/animate/save in the visible Blender connection.
Connected joint poses drive both a native skeleton and baked contour shape keys;
portraits and kit contours are editable geometry, not raster planes.
"""
import bpy, math, json, sys
from pathlib import Path
from mathutils import Vector, Matrix
V=Path(__file__).resolve().parents[1];ROOT=V.parents[3]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from pipeline.pose_geometry import two_bone_joint
O=V/'artifacts/staging-v001/football-performance-v001'
ART=V/'assets/football-v001';A={};M={};CONTACTS={};P='S06 / '
INK='#192334';BLUE='#223d77';NAVY='#203251';RED='#a02d48';YELLOW='#f7d36c'
R=Vector((.822192,.569210,0));D=Vector((-.569210,.822192,0))
SCALE=.00188;FPS=24;END=312
EVENTS={'marking_set':35,'notice':48,'line':59,'pass':123,'receive':151,'touch':172,'plant':190,'strike':199,'goal':213,'net':218,'counter':222}

def mat(c):
 if c not in M:
  rgb=[int(c[i:i+2],16)/255 for i in (1,3,5)];rgb=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
  m=bpy.data.materials.new(P+c);m.diffuse_color=(*rgb,1);M[c]=m
 return M[c]
def empty(n,parent=None):
 o=bpy.data.objects.new(P+n,None);C.objects.link(o);o.parent=parent;o.empty_display_size=.05;return o

def poly(n,pts,color,parent=None,depth=0):
 me=bpy.data.meshes.new(P+n);me.from_pydata([(x,-depth,z) for x,z in pts],[],[list(range(len(pts)))]);me.materials.append(mat(color))
 o=bpy.data.objects.new(P+n,me);C.objects.link(o);o.parent=parent;return o

def line(n,pts,color=INK,width=.004,parent=None,depth=.001,closed=False):
 cu=bpy.data.curves.new(P+n,'CURVE');cu.dimensions='3D';cu.bevel_depth=width;cu.bevel_resolution=1;cu.resolution_u=1;cu.use_fill_caps=True
 sp=cu.splines.new('POLY');sp.points.add(len(pts)-1);sp.use_cyclic_u=closed
 for p,(x,z) in zip(sp.points,pts):p.co=(x,-depth,z,1)
 cu.materials.append(mat(color));o=bpy.data.objects.new(P+n,cu);C.objects.link(o);o.parent=parent;return o

def oval(n,x,z,rx,rz,color,parent=None,depth=0):return poly(n,[(x+rx*math.cos(k*math.tau/32),z+rz*math.sin(k*math.tau/32)) for k in range(32)],color,parent,depth)
def outlined(n,pts,color,parent=None,depth=0):
 o=poly(n,pts,color,parent,depth);line(n+' ink',pts,parent=parent,depth=depth+.001,closed=True);return o

def vector_part(n,rows,parent,origin,scale=SCALE,depth=0):
 made=[]
 for i,row in enumerate(rows):
  cu=bpy.data.curves.new(P+n+str(i),'CURVE');cu.dimensions='2D';cu.fill_mode='BOTH';cu.resolution_u=1
  for path in row['paths']:
   sp=cu.splines.new('POLY');sp.points.add(len(path)-1);sp.use_cyclic_u=True
   for q,(x,y) in zip(sp.points,path):q.co=((x-origin[0])*scale,(origin[1]-y)*scale,0,1)
  cu.materials.append(mat(row['color']));ob=bpy.data.objects.new(cu.name,cu);C.objects.link(ob);ob.parent=parent;ob.rotation_euler.x=math.pi/2;ob.location.y=-depth-i*.00006;made.append(ob)
 bpy.ops.object.select_all(action='DESELECT')
 for ob in made:ob.select_set(True)
 bpy.context.view_layer.objects.active=made[0];bpy.ops.object.convert(target='MESH');bpy.ops.object.join();ob=bpy.context.object;ob.name=P+n
 return ob

def key(o,f):
 for prop in ('location','rotation_euler','scale'):o.keyframe_insert(data_path=prop,frame=f)
def mix(a,b,t):return a+(b-a)*t

def at(f,rows,smooth=True):
 if f<=rows[0][0]:return rows[0][1]
 for (fa,a),(fb,b) in zip(rows,rows[1:]):
  if f<=fb:
   t=(f-fa)/(fb-fa);t=t*t*(3-2*t) if smooth else t
   if isinstance(a,(tuple,list)):return tuple(mix(x,y,t) for x,y in zip(a,b))
   return mix(a,b,t)
 return rows[-1][1]
def turn(p,a):
 c=math.cos(a);s=math.sin(a);return (p[0]*c-p[1]*s,p[0]*s+p[1]*c)

def setup():
 global S,C,CAM,BALL,SHADOW,COUNTER
 assert not bpy.app.background
 assert 'S003_S06_Football_v001' not in bpy.data.scenes
 with bpy.data.libraries.load(str(V/'artifacts/staging-v001/training-set-v001/training-set.blend'),link=False) as (src,dst):dst.scenes=['S003_Training_Set_v001']
 S=dst.scenes[0].copy();S.name='S003_S06_Football_v001';bpy.context.window.scene=S
 C=bpy.data.collections.new(P+'performance');S.collection.children.link(C)
 S.render.resolution_x=1280;S.render.resolution_y=720;S.render.resolution_percentage=100;S.render.fps=24;S.frame_start=1;S.frame_end=END;S.render.use_sequencer=False;S.display.render_aa='16'
 S['construction']='Native traced portraits/kit, articulated drawn limbs driven from connected skeleton poses; absolute contour keys preserve the authored silhouettes. No raster character planes. Dedicated S06 action, not copied S08 animation.'
 cd=bpy.data.cameras.new(P+'director');CAM=bpy.data.objects.new(cd.name,cd);C.objects.link(CAM);cd.type='ORTHO';cd.ortho_scale=16;cd.clip_end=300;S.camera=CAM
 # Low-poly native ball; at .11 m its size is in the same world as the goal.
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=.11)
 BALL=bpy.context.object;BALL.name=P+'ball'
 for c in list(BALL.users_collection):c.objects.unlink(BALL)
 C.objects.link(BALL);BALL.data.materials.append(mat('#fff5da'));BALL.data.materials.append(mat('#1c2937'))
 for p in BALL.data.polygons:p.material_index=1 if p.index%7==0 else 0
 SHADOW=poly('ball shadow',[(math.cos(i*math.tau/32)*.16,math.sin(i*math.tau/32)*.10) for i in range(32)],'#528844');SHADOW.rotation_euler.x=math.pi/2
 # Counter replacement belongs to this shot only, leaving the shared set intact.
 original=next(o for o in S.objects if o.name=='Goal count');COUNTER=original.copy();COUNTER.data=original.data.copy();C.objects.link(COUNTER)
 COUNTER.location.y-=.03;COUNTER.data.body='GOALS  7'
 # Original remains behind the opaque board overlay.
 for o in S.objects:
  if o.name=='Goal counter front':pass
 for a in bpy.context.screen.areas:
  if a.type=='VIEW_3D':
   a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.overlay.show_overlays=False;a.spaces.active.shading.type='SOLID';a.spaces.active.shading.light='FLAT';a.spaces.active.shading.color_type='MATERIAL'
 O.mkdir(exist_ok=True)
 return {'scene':S.name,'environment_objects':len(S.objects)}

# Continuous tapered surfaces are built from the same joint points as the skeleton.
# Each region retains its own surface ownership; no source background or grip is weighted into a sleeve.
def ribbon(joints,widths,segments=8):
 sh,el,wr=[Vector(p) for p in joints];pts=[]
 # Piecewise quadratic near the elbow softens only the actual joint, not the full limb.
 for i in range(segments*2+1):
  t=i/(segments*2)
  if t<.4:p=sh.lerp(el,t/.5)
  elif t>.6:p=el.lerp(wr,(t-.5)/.5)
  else:
   u=(t-.4)/.2;a=sh.lerp(el,.8);b=el.lerp(wr,.2);p=a*(1-u)**2+el*(2*u*(1-u))+b*u*u
  pts.append(p)
 left=[];right=[]
 for i,p in enumerate(pts):
  tangent=pts[min(len(pts)-1,i+1)]-pts[max(0,i-1)];tangent.normalize();n=Vector((-tangent.y,tangent.x));t=i/(len(pts)-1)
  width=at(t,[(0,widths[0]),(.5,widths[1]),(1,widths[2])]);left.append(tuple(p+n*width));right.append(tuple(p-n*width))
 return left+right[::-1]

def deform(n,pts,color,parent,depth):
 o=poly(n,pts,color,parent,depth)
 if len(pts)==34:
  o.data.clear_geometry();o.data.from_pydata([(x,-depth,z) for x,z in pts],[],[(i,i+1,32-i,33-i) for i in range(16)])
 o.shape_key_add(name='Basis');o.data.shape_keys.use_relative=False;o.data.shape_keys.eval_time=0
 # Flat outline uses its own strip, avoiding a bevel tube piercing the surface.
 return o

def pose_shape(o,pts,f):
 k=o.shape_key_add(name=f'pose {f:03}');k.interpolation='KEY_LINEAR'
 for v,(x,z) in zip(k.data,pts):v.co.x=x;v.co.z=z
 o.data.shape_keys.eval_time=k.frame;o.data.shape_keys.keyframe_insert(data_path='eval_time',frame=f)

def silhouette(o,pts,f):
 # Fill geometry includes a separate underlying enlarged silhouette: both are
 # rebuilt from joint centers, avoiding independent joint outlines.
 pose_shape(o,pts,f)

def create_actor(name,source=None,defender=0):
 source=source or name;data=json.loads((ART/(source.lower()+'.json')).read_text());c=data['design'];root=empty(name+' world');root.rotation_euler.z=math.atan2(R.y,R.x)
 torso=empty(name+' torso',root);head=empty(name+' head',root)
 a={'name':name,'c':c,'root':root,'torso':torso,'head':head,'defender':defender,'eyes':[],'limbs':{},'boots':[],'data':data}
 A[name]=a
 # Full heads retain original illustration shape; eye openings have native moving pupils/lids.
 vector_part(name+' illustrated head',data['parts']['head'],head,c['neck'],depth=.011)
 for i,(x,y,rx,ry) in enumerate(c['eyes']):
  x=(x-c['neck'][0])*SCALE;z=(c['neck'][1]-y)*SCALE
  eye=empty(name+f' eye {i}',head);eye.location=(x,-.075,z)
  oval(name+' sclera',0,0,(rx+2)*SCALE,(ry+2)*SCALE,'#fff8e6',eye)
  pupil=empty(name+' gaze',eye);oval(name+' iris',0,0,rx*SCALE*.52,ry*SCALE*.75,INK,pupil,.001);oval(name+' eye shine',-.004,.005,.003,.004,'#ffffff',pupil,.002)
  lid=oval(name+' lid',0,0,(rx+3)*SCALE,(ry+3)*SCALE,c['skin'],eye,.003);lid.hide_render=True
  a['eyes'].append((pupil,lid))
 # Neck fills from collar to the actual cut edge of the source portrait.
 a['neck']=deform(name+' neck',[(-.075,1.32),(.075,1.32),(.10,1.53),(-.085,1.53)],c['skin'],root,.002)
 if not defender:
  vector_part(name+' drawn shirt',data['parts']['shirt'],torso,(c['cx'],577),depth=.012)
 else:
  outlined(name+' training bib',[(-.19,0),(.19,0),(.21,.55),(.105,.60),(-.105,.60),(-.21,.55)],['#e8c65e','#e9ad55','#e2cc79'][defender-1],torso,.012)
  line(name+' bib seam',[(-.19,.06),(.19,.06)],'#af863e',.003,torso,.014)
 a['shorts']=vector_part(name+' drawn shorts',data['parts']['shorts'],torso,(c['cx'],577),depth=.010)
 # Mouth aperture appears only while Raphinha speaks; the original rest mouth remains otherwise.
 mouth=empty(name+' speech mouth',head);mx,my,mw=c['mouth'];mouth.location=((mx-c['neck'][0])*SCALE,-.075,(c['neck'][1]-my)*SCALE)
 oval(name+' mouth backing',0,0,mw*SCALE*1.2,.022,c['skin'],mouth,0)
 oval(name+' mouth opening',0,-.002,mw*SCALE*.75,.016,'#512d2c',mouth,.001)
 line(name+' upper teeth',[(-mw*SCALE*.6,.006),(mw*SCALE*.55,.006)],'#fff3dc',.005,mouth,.002)
 a['mouth']=mouth
 for side in ('L','R'):
  for part,colr,dep in [('arm',c['skin'],.001 if side=='L' else -.010),('sleeve',BLUE,.005 if side=='L' else -.006),('leg',c['skin'],-.007 if side=='L' else -.014),('sock',NAVY,-.003 if side=='L' else -.010)]:
   n=part+side;pts=[(0,0)]*34
   outline=deform(name+' '+n+' silhouette',pts,INK,root,dep-.001)
   fill=deform(name+' '+n,pts,colr,root,dep)
   a['limbs'][n]=(outline,fill)
  hand=empty(name+' hand '+side,root);a['hand'+side]=hand
  hp=[(-.035,.015),(.025,.015),(.045,-.025),(.056,-.080),(.040,-.090),(.015,-.047),(.025,-.135),(.009,-.150),(-.009,-.133),(-.030,-.102),(-.046,-.045)]
  outlined(name+' relaxed hand '+side,hp,c['skin'],hand,.006)
  line(name+' fingers '+side,[(-.016,-.072),(-.007,-.12)],c['shadow'],.002,hand,.008)
  if name=='Raphinha' and side=='R':
   point=empty(name+' pointing drawing',root);a['point']=point
   outlined(name+' index finger',[(-.03,-.02),(-.025,.025),(.025,.045),(.15,.045),(.17,.03),(.16,.018),(.055,.016),(.065,-.017),(.047,-.044),(.0,-.049)],c['skin'],point,.008)
  foot=empty(name+' boot '+side,root);i=0 if side=='L' else 1;vector_part(name+' illustrated boot '+side,data['parts']['boot'+str(i)],foot,c['ankles'][i],depth=.006);a['boots'].append(foot)
 # Native connected skeleton, evaluated from the same authored joint schedule.
 rigdata=bpy.data.armatures.new(P+name+' skeleton');rig=bpy.data.objects.new(rigdata.name,rigdata);C.objects.link(rig);rig.parent=root;rig.hide_render=True;rig.show_in_front=True;rig.display_type='WIRE'
 bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT')
 bones={'spine':((0,.87),(0,1.43),None)}
 for side,sgn in [('L',-1),('R',1)]:
  bones[side+' thigh']=((sgn*.115,.86),(sgn*.13,.48),'spine');bones[side+' shin']=((sgn*.13,.48),(sgn*.15,.15),side+' thigh')
  bones[side+' upper']=((sgn*.175,1.39),(sgn*.29,1.1),'spine');bones[side+' fore']=((sgn*.29,1.1),(sgn*.34,.86),side+' upper')
 for name2,(p,q,parent) in bones.items():
  b=rigdata.edit_bones.new(name2);b.head=(p[0],0,p[1]);b.tail=(q[0],0,q[1]);
  if parent:b.parent=rigdata.edit_bones[parent];b.use_connect=name2.endswith(('shin','fore'))
 bpy.ops.object.mode_set(mode='OBJECT');a['rig']=rig
 # Empty targets drive native constraints, making the underlying skeleton inspectable.
 a['targets']={}
 for name2,(p,q,_) in bones.items():
  x=empty(name+' '+name2+' start',root);y=empty(name+' '+name2+' end',root);x.location=(p[0],0,p[1]);y.location=(q[0],0,q[1]);a['targets'][name2]=(x,y)
  pb=rig.pose.bones[name2];co=pb.constraints.new('COPY_LOCATION');co.target=x
  co=pb.constraints.new('STRETCH_TO');co.target=y;co.volume='NO_VOLUME';co.rest_length=(Vector(q)-Vector(p)).length
 # Grounding shadow belongs to this character and moves on the field.
 shadow=poly(name+' ground shadow',[(.29*math.cos(i*math.tau/32),.12*math.sin(i*math.tau/32)) for i in range(32)],'#528b48');shadow.rotation_euler.x=math.pi/2;a['shadow']=shadow
 return {'actor':name,'head':source,'native_parts':len(a['limbs'])}

# Pose coordinates are metres in the actor's vertical drawing plane.
def body_pose(name,f):
 defender=A[name]['defender'];point=0;lean=0;headangle=0;gaze=0;step=0;move=0
 if name=='Pedri':
  world=(-6,-10.6);hip=(0,.98);lean=at(f,[(1,0),(89,0),(108,-.10),(121,.13),(138,.05),(165,0)])
  lf=at(f,[(1,(-.19,.16)),(92,(-.19,.16)),(110,(.02,.17)),(118,(.21,.16)),(140,(.21,.16)),(175,(.18,.16))]);rf=at(f,[(1,(.19,.16)),(91,(.19,.16)),(110,(-.34,.30)),(117,(-.38,.35)),(123,(.44,.18)),(131,(.66,.42)),(149,(.39,.16))]);rrot=at(f,[(1,0),(110,-.5),(123,.06),(132,.55),(149,0)]);lrot=0
  gaze=at(f,[(1,0),(62,0),(76,.007),(93,.009),(121,.0)]);headangle=at(f,[(1,0),(80,.04),(113,-.10),(140,0)])
 elif name=='Yamal':
  world=(2.35,-6.9);move=at(f,[(1,0),(104,0),(141,.32),(155,.45),(173,.88),(191,1.28),(202,1.34),(225,1.7),(250,2.12),(280,2.12)])
  hip=(.08,.96+at(f,[(1,0),(130,.015),(151,-.065),(174,.005),(192,-.06),(199,-.02),(211,.02),(232,-.025),(250,0)]));lean=at(f,[(1,0),(120,-.07),(151,.03),(178,-.04),(198,.16),(214,.10),(246,0)])
  lf=at(f,[(1,(-.18,.16)),(123,(-.18,.16)),(142,(-.34,.22)),(151,(-.02,.16)),(164,(-.24,.16)),(177,(.13,.30)),(190,(.27,.16)),(208,(.21,.16)),(226,(-.19,.30)),(245,(-.18,.16))]);rf=at(f,[(1,(.18,.16)),(123,(.18,.16)),(142,(.36,.24)),(151,(.26,.16)),(160,(.22,.22)),(172,(.48,.18)),(185,(-.33,.35)),(193,(-.44,.44)),(199,(.48,.19)),(207,(.70,.53)),(218,(.58,.38)),(235,(.21,.16))]);lrot=0;rrot=at(f,[(1,0),(142,-.2),(151,-.08),(172,.02),(188,-.7),(199,.02),(207,.67),(235,0)])
  headangle=at(f,[(1,0),(117,-.04),(145,-.1),(165,0),(186,-.08),(212,.08)]);gaze=at(f,[(1,-.008),(136,-.008),(171,.008),(235,.008)])
 elif name=='Raphinha':
  world=(-2.4,-6.6);hip=(0,.98);lf=(-.20,.16);rf=(.19,.16);lrot=rrot=0
  point=at(f,[(1,0),(42,0),(57,1),(93,1),(114,0)]);lean=at(f,[(1,0),(34,-.05),(60,.02),(95,.02),(115,0)]);headangle=at(f,[(1,-.03),(33,-.07),(48,.06),(93,.04),(132,0)]);gaze=at(f,[(1,-.010),(36,-.010),(49,.009),(140,.009)])
  move=at(f,[(1,0),(222,0),(264,-.70),(298,-1.10)])
  if f>222:
   ph=(f-222)/11;lf=(-.2+.13*math.sin(ph),.16+.08*max(0,math.sin(ph)));rf=(.19-.13*math.sin(ph),.16+.08*max(0,-math.sin(ph)))
 else:
  starts=[(-3.7,-5.3),(-1.1,-4.9),(-.5,-7.25)];world=starts[defender-1]
  move=at(f,[(1,.38 if defender!=3 else .65),(36,0),(144,0),(158,.16),(189,.48),(222,.70)])
  hip=(0,.96);ph=(f+defender*4)/10;active=f<36 or 153<f<224
  lf=(-.20+.12*math.sin(ph) if active else -.20,.16+.08*max(0,math.sin(ph)) if active else .16);rf=(.20-.12*math.sin(ph) if active else .20,.16+.08*max(0,-math.sin(ph)) if active else .16);lrot=rrot=0
  lean=at(f,[(1,-.04),(38,-.05),(148,-.05),(161,.10),(212,.12),(254,0)]);headangle=at(f,[(1,-.07),(148,-.07),(157+defender*4,.08),(246,.02)]);gaze=at(f,[(1,-.012),(148,-.012),(157+defender*4,.012)])
 world=Vector((*world,0))+R*move
 if name=='Yamal' and 190<=f<=212:
  plant_move=at(190,[(1,0),(104,0),(141,.32),(155,.45),(173,.88),(191,1.28),(202,1.34),(225,1.7),(250,2.12),(280,2.12)])
  lf=(.27+plant_move-move,.16)
 hip=Vector(hip)
 if name=='Pedri':hip.x=at(f,[(1,0),(110,.02),(123,.14),(149,.14)])
 neck=hip+Vector(turn((0,.53),lean));shoulders={side:hip+Vector(turn((sgn*.16,.46),lean)) for side,sgn in [('L',-1),('R',1)]}
 feet={'L':Vector(lf),'R':Vector(rf)};legs={};arms={}
 for side,sgn in [('L',-1),('R',1)]:
  start=hip+Vector((sgn*.095,-.05));end=feet[side];lengths=(.405,.405);dist=(end-start).length
  # Authored changes report reach failures instead of silently changing contacts.
  if dist>sum(lengths)+1e-6:raise ValueError((name,f,side,'unreachable foot',dist))
  knee=Vector(two_bone_joint(tuple(start),tuple(end),lengths,(start.x+.6,start.y-.2)))
  legs[side]=(tuple(start),tuple(knee),tuple(end))
  sh=shoulders[side];swing=at(f,[(1,0),(110,0),(124,-.12*sgn),(144,0)]) if name=='Pedri' else (.12*math.sin((f-115)/11)*sgn if name=='Yamal' and 120<f<242 else 0)
  wrist=sh+Vector((sgn*(.18+swing),-.48+abs(swing)*.8))
  if name=='Raphinha' and side=='R':wrist=wrist.lerp(sh+Vector((.53,.02)),point)
  if defender:wrist=sh+Vector((sgn*.28,-.33))
  elbow=Vector(two_bone_joint(tuple(sh),tuple(wrist),(.29,.29),(sh.x+sgn*.5,sh.y-.2)))
  arms[side]=(tuple(sh),tuple(elbow),tuple(wrist))
 return dict(world=world,hip=hip,neck=neck,lean=lean,headangle=headangle,gaze=gaze,legs=legs,arms=arms,rot={'L':lrot,'R':rrot},point=point)

def world_boot(name,f,side='R'):
 p=body_pose(name,f);foot=Vector(p['legs'][side][2]);return p['world']+R*foot.x+Vector((0,0,foot.y))
def ball_position(f):
 launch=Vector(CONTACTS.get('pass',world_boot('Pedri',123)+R*.33));launch.z=.11
 receive=Vector(CONTACTS.get('receive',world_boot('Yamal',151)+R*.33));receive.z=.11
 touch=Vector(CONTACTS.get('touch',world_boot('Yamal',172)+R*.33));touch.z=.11
 strike=Vector(CONTACTS.get('strike',world_boot('Yamal',199)+R*.33));strike.z=.11
 goal=Vector((1.30,.10,.65));net=Vector((1.6,2.18,.36))
 if f<=123:return launch
 if f<=151:return launch.lerp(receive,(f-123)/28)
 if f<=172:return receive.lerp(touch,(f-151)/21)
 if f<=199:return touch.lerp(strike,(f-172)/27)
 if f<=213:
  t=(f-199)/14;p=strike.lerp(goal,t);p.z+=.65*4*t*(1-t);return p
 if f<=218:return goal.lerp(net,(f-213)/5)
 t=min(1,(f-218)/30);p=net.lerp(Vector((1.55,1.10,.11)),t);p.z+=.15*math.sin(math.pi*t);return p

def animate_actor(name):
 a=A[name];c=a['c'];resthip=.91 if not a['defender'] else .86
 for f in range(1,END+1):
  p=body_pose(name,f);a['root'].location=p['world'];key(a['root'],f)
  a['torso'].location=(p['hip'].x,0,p['hip'].y);a['torso'].rotation_euler.y=-p['lean'];key(a['torso'],f)
  a['head'].location=(p['neck'].x,-.006,p['neck'].y);a['head'].rotation_euler.y=-(p['lean']+p['headangle']);key(a['head'],f)
  # Native key shapes at every second frame plus contact frames; interpolation is linear.
  shape_frame=f%2==1 or f in EVENTS.values() or f==END
  if shape_frame:
   neckpts=[]
   for q in [(-.07,-.03),(.075,-.03),(.10,.10),(-.079,.10)]:
    r=Vector(turn(q,p['lean']+(p['headangle'] if q[1]>.05 else 0)))+p['neck'];neckpts.append(tuple(r))
   pose_shape(a['neck'],neckpts,f)
  for side in ('L','R'):
   arm=p['arms'][side];leg=p['legs'][side]
   if shape_frame:
    for region,joints,widths in [('arm',arm,[.055,.048,.028]),('sleeve',(arm[0],tuple(Vector(arm[0]).lerp(Vector(arm[1]),.35)),tuple(Vector(arm[0]).lerp(Vector(arm[1]),.72))),[.083,.080,.067]),('leg',leg,[.079,.058,.038]),('sock',(tuple(Vector(leg[1]).lerp(Vector(leg[0]),.05)),tuple(Vector(leg[1]).lerp(Vector(leg[2]),.45)),leg[2]),[.061,.062,.042])]:
     edge,fill=a['limbs'][region+side];pose_shape(edge,ribbon(joints,[w+.0038 for w in widths]),f);pose_shape(fill,ribbon(joints,widths),f)
   hand=a['hand'+side];w=Vector(arm[2]);fore=w-Vector(arm[1]);ang=math.atan2(fore.y,fore.x)+math.pi/2;hand.location=(w.x,-.006 if side=='L' else .008,w.y);hand.rotation_euler.y=-ang;key(hand,f)
   if name=='Raphinha' and side=='R':
    visible=p['point']>.7
    for ob in hand.children:ob.hide_render=visible;ob.keyframe_insert(data_path='hide_render',frame=f)
    point=a['point'];point.location=(w.x,-.018,w.y);key(point,f)
    for ob in point.children:ob.hide_render=not visible;ob.keyframe_insert(data_path='hide_render',frame=f)
   foot=a['boots'][0 if side=='L' else 1];ankle=Vector(leg[2]);foot.location=(ankle.x,-.018 if side=='L' else .018,ankle.y);foot.rotation_euler.y=-p['rot'][side];key(foot,f)
   for bone,pts in [(side+' thigh',leg[:2]),(side+' shin',leg[1:]),(side+' upper',arm[:2]),(side+' fore',arm[1:])]:
    for target,pt in zip(a['targets'][bone],pts):target.location=(pt[0],0,pt[1]);key(target,f)
  for target,pt in zip(a['targets']['spine'],[p['hip'],p['neck']]):target.location=(pt[0],0,pt[1]);key(target,f)
  for i,(pupil,lid) in enumerate(a['eyes']):
   pupil.location.x=p['gaze']+.008;pupil.location.z=-.003 if name in ['Yamal','Pedri'] and 112<f<202 else 0;key(pupil,f)
   blink=(f in range(29+len(name),32+len(name))) or (f in range(239+len(name),242+len(name)));lid.hide_render=not blink;lid.keyframe_insert(data_path='hide_render',frame=f)
  speak=name=='Raphinha' and 59<=f<=94
  for ob in a['mouth'].children:ob.hide_render=not speak;ob.keyframe_insert(data_path='hide_render',frame=f)
  a['mouth'].scale.z=.6+.35*abs(math.sin(f*1.15)) if speak else 1;key(a['mouth'],f)
  a['shadow'].location=(p['world'].x,p['world'].y,.023);key(a['shadow'],f)
 return {'actor':name,'frames':END,'contour_samples':'every other frame + exact contacts'}

def camera_pose(f):
 # Opening establishes the crowding; cut to the field before the pass, then
 # follow the reception/finish from the same side of the action axis.
 if f<99:target=Vector((-1.4,-6.4,.95));scale=9.8
 elif f<143:target=Vector((-1.3,-6.7,.85));scale=16.6
 else:
  target=Vector(at(f,[(143,(2,-4.1,.9)),(202,(2,-3.2,.9)),(264,(5.1,1.4,1.0)),(312,(5.1,1.4,1.0))]));scale=at(f,[(143,10.2),(211,10.2),(264,14.0)])
 CAM.location=target-D*29+Vector((0,0,9));CAM.rotation_euler=(target-CAM.location).to_track_quat('-Z','Y').to_euler();CAM.data.ortho_scale=scale;key(CAM,f);CAM.data.keyframe_insert(data_path='ortho_scale',frame=f)

def animate_scene():
 for f in range(1,END+1):
  BALL.location=ball_position(f);BALL.rotation_euler=(f*.15,f*.08,f*.11);key(BALL,f)
  SHADOW.location=(BALL.location.x,BALL.location.y,.025);SHADOW.scale=(max(.4,1-BALL.location.z*.3),)*3;key(SHADOW,f);camera_pose(f)
 # Two text objects switch once; text content itself is not animatable.
 COUNTER.data.body='GOALS  7'
 eight=COUNTER.copy();eight.data=COUNTER.data.copy();eight.data.body='GOALS  8';C.objects.link(eight)
 for f in [1,221,222,312]:
  COUNTER.hide_render=f>=222;COUNTER.keyframe_insert(data_path='hide_render',frame=f);eight.hide_render=f<222;eight.keyframe_insert(data_path='hide_render',frame=f)
 # Counter's original digits are covered by an exact shot-owned board.
 blocker=poly('counter backing',[(-1,-.325),(1,-.325),(1,.325),(-1,.325)],'#213849',None,0);blocker.location=(10.4,2.86,2.425)
 COUNTER.location.y=2.84;eight.location.y=2.84
 for label,f in EVENTS.items():S.timeline_markers.new(label,frame=f)
 S['events']=json.dumps(EVENTS);S.frame_set(1)
 return {'scene_frames':END,'events':EVENTS}

def linear_keys():
 for action in bpy.data.actions:
  if not action.name.startswith(P):continue
  for layer in action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='LINEAR'

def sync_preview_visibility():
 # Native viewport playback must use the same drawing swaps as rendering.
 channels=[]
 for ob in S.objects:
  ad=ob.animation_data
  if not ad or not ad.action:continue
  for layer in ad.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      if fc.data_path=='hide_render':channels.append((ob,fc))
 for ob,fc in channels:
  for point in list(fc.keyframe_points):
   f=int(point.co.x);ob.hide_viewport=bool(fc.evaluate(f));ob.keyframe_insert(data_path='hide_viewport',frame=f)
 for f in [1,59,96,97,199,222,312]:
  S.frame_set(f)
  assert all(ob.hide_viewport==ob.hide_render for ob,_ in channels)
 return len(channels)

def check_save():
 errors=check_visible_contacts()
 assert ball_position(212).y<0 and ball_position(213).y>0
 assert all(0<ball_position(f).z<2.44 for f in range(199,219))
 # Foot artwork extends below its ankle by about .15m; check source-calibrated rests.
 assert all(body_pose(who,f)['legs'][side][2][1]>=.15 for who in A for f in range(1,END+1) for side in ['L','R'])
 sync_preview_visibility();linear_keys();S.frame_set(1)
 bpy.ops.wm.save_as_mainfile(filepath=str(O/'football-performance.blend'))
 report={'frames':END,'fps':FPS,'duration':END/FPS,'visible_contact_gap_m':errors,'goal_crossing_frame':213,'actors':list(A),'construction':S['construction'],'scope':'Target/contact geometry only; visual review required. Restored file needs no Python playback handler.'}
 (O/'construction-check.json').write_text(json.dumps(report,indent=2)+'\n')
 return report

def distinct_defenders():
 for a in A.values():
  i=a['defender']
  if not i:continue
  data=json.loads((ART/f'defender-{i}.json').read_text());c=data['design'];scale=data['scale'];name=a['name']
  # Replace only illustration identity; retain the already-authored defensive action.
  for ob in list(a['head'].children_recursive):bpy.data.objects.remove(ob,do_unlink=True)
  a['eyes']=[];a['mouth']=empty(name+' silent mouth',a['head'])
  vector_part(name+' fictional defender head',data['head'],a['head'],c['neck'],scale,depth=.014)
  for j,(x,y,rx,ry) in enumerate(c['eyes']):
   eye=empty(name+f' eye {j}',a['head']);eye.location=((x-c['neck'][0])*scale,-.10,(c['neck'][1]-y)*scale)
   oval(name+' sclera',0,0,(rx+2)*scale,(ry+2)*scale,'#fff8e6',eye)
   pupil=empty(name+' gaze',eye);oval(name+' pupil',0,0,rx*scale*.6,ry*scale*.76,INK,pupil,.001);oval(name+' glint',-.004,.006,.003,.004,'#fff8e6',pupil,.002)
   lid=oval(name+' lid',0,0,(rx+3)*scale,(ry+3)*scale,c['skin'],eye,.003);a['eyes'].append((pupil,lid))
  a['c']['skin']=c['skin'];a['neck'].data.materials.clear();a['neck'].data.materials.append(mat(c['skin']))
  for side in ['L','R']:
   for region in ['arm','leg']:
    a['limbs'][region+side][1].data.materials.clear();a['limbs'][region+side][1].data.materials.append(mat(c['skin']))
   for ob in a['hand'+side].children:
    if ob.type=='MESH':ob.data.materials.clear();ob.data.materials.append(mat(c['skin']))
  a['shorts'].hide_render=True;a['shorts'].hide_viewport=True
  outlined(name+' plain training shorts',[(-.20,.015),(.20,.015),(.22,-.20),(.035,-.215),(0,-.10),(-.035,-.215),(-.22,-.20)],NAVY,a['torso'],.032)
 return {'distinct_defenders':3}

def clear_actor_keys(name):
 a=A[name]
 for ob in [a['neck']]+[o for pair in a['limbs'].values() for o in pair]:
  ob.shape_key_clear();ob.shape_key_add(name='Basis');ob.data.shape_keys.use_relative=False

def shorts_follow(name):
 a=A[name]
 if a['defender']:return
 ob=a['shorts'];ob.shape_key_clear();ob.shape_key_add(name='Basis');ob.data.shape_keys.use_relative=False
 base=[v.co.copy() for v in ob.data.vertices]
 for f in [1,99,110,117,123,131,149,151,164,172,185,190,193,199,207,218,235,245,280,312]:
  p=body_pose(name,f);k=ob.shape_key_add(name=f'leg fold {f}');k.interpolation='KEY_LINEAR'
  for v,co in zip(k.data,base):
   side='L' if co.x<0 else 'R';hip,knee,_=p['legs'][side];d=Vector(knee)-Vector(hip);angle=math.atan2(d.y,d.x)+math.pi/2-p['lean']
   weight=max(0,min(1,(-co.y-.025)/.19));pivot=Vector((-.095 if side=='L' else .095,-.045));new=pivot+Vector(turn(tuple(Vector((co.x,co.y))-pivot),angle*weight))
   v.co.x=new.x;v.co.y=new.y
  ob.data.shape_keys.eval_time=k.frame;ob.data.shape_keys.keyframe_insert(data_path='eval_time',frame=f)

def captions():
 me=bpy.data.meshes.new(P+'caption backdrop');me.from_pydata([(-.34,-.03,0),(.34,-.03,0),(.34,.03,0),(-.34,.03,0)],[],[(0,1,2,3)]);me.materials.append(mat('#172432'))
 bg=bpy.data.objects.new(me.name,me);C.objects.link(bg);bg.parent=CAM
 cu=bpy.data.curves.new(P+'dialogue caption','FONT');cu.body="RAPHINHA: Who's watching him?";cu.align_x='CENTER';cu.align_y='CENTER';cu.materials.append(mat('#fff4da'))
 tx=bpy.data.objects.new(cu.name,cu);C.objects.link(tx);tx.parent=CAM
 for f in range(1,END+1):
  S.frame_set(f);w=CAM.data.ortho_scale;bottom=-w*9/32+w*.065
  bg.location=(0,bottom,-1);bg.scale=(w,w*.7,1);tx.location=(0,bottom,-.98);cu.size=w*.023
  for ob in [bg,tx]:ob.hide_render=not 59<=f<=96;ob.keyframe_insert(data_path='hide_render',frame=f);key(ob,f)
  cu.keyframe_insert(data_path='size',frame=f)
 return {'caption':'RAPHINHA: Who\'s watching him?','frames':[59,96]}

def linear_keys():
 actions=set()
 for ob in C.objects:
  for data in [ob,ob.data,getattr(ob.data,'shape_keys',None)]:
   ad=getattr(data,'animation_data',None)
   if ad and ad.action:actions.add(ad.action)
 for action in actions:
  for layer in action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='LINEAR'

def fit_visible_contacts():
 from mathutils.bvhtree import BVHTree
 CONTACTS.clear()
 for event,who,f in [('pass','Pedri',123),('receive','Yamal',151),('touch','Yamal',172),('strike','Yamal',199)]:
  S.frame_set(f);bpy.context.view_layer.update();a=A[who];ob=next(o for o in a['boots'][1].children if o.type=='MESH');ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh()
  verts=[ev.matrix_world@v.co for v in mesh.vertices];tree=BVHTree.FromPolygons(verts,[tuple(p.vertices) for p in mesh.polygons])
  base=world_boot(who,f);base.z=.11
  # Find the front tangent of the actual boot to a radius-.11 sphere. Bound by
  # the visible mesh, not an arbitrarily placed skeleton endpoint.
  direction=R.copy()
  if event=='receive':
   direction=Vector(CONTACTS['pass'])-base;direction.z=0;direction.normalize()
  lo=max((p-base).dot(direction) for p in verts);hi=lo+.25
  for _ in range(30):
   mid=(lo+hi)*.5;distance=tree.find_nearest(base+direction*mid)[3]
   if distance<.11:lo=mid
   else:hi=mid
  CONTACTS[event]=tuple(base+direction*((lo+hi)*.5));ev.to_mesh_clear()
 S['visible_ball_contacts']=json.dumps(CONTACTS)
 return CONTACTS

def check_visible_contacts():
 from mathutils.bvhtree import BVHTree
 gaps={}
 for who,f in [('Pedri',123),('Yamal',151),('Yamal',172),('Yamal',199)]:
  S.frame_set(f);bpy.context.view_layer.update();ob=next(o for o in A[who]['boots'][1].children if o.type=='MESH');ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh();tree=BVHTree.FromPolygons([ev.matrix_world@v.co for v in mesh.vertices],[tuple(p.vertices) for p in mesh.polygons])
  gap=tree.find_nearest(BALL.matrix_world.translation)[3]-.11;gaps[f'{who}:{f}']=gap;ev.to_mesh_clear()
 assert max(abs(v) for v in gaps.values())<.001,gaps
 # Native world-space plant remains fixed through the strike, independently of root travel.
 positions=[world_boot('Yamal',f,'L') for f in range(190,213)]
 assert max((p-positions[0]).length for p in positions)<1e-5
 return gaps
