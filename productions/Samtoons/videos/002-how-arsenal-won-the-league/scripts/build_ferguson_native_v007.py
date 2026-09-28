"""Native flat artwork on articulated controls, authored in the visible Blender.
Reuses video001's flat-art primitives; no raster character material or pose planes.
"""
import bpy,math,json,sys
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v007';W=V.parents[3]
b={'__file__':str(V.parent/'001-manchester-derby-2026-09-13/scripts/build_staging.py')}
exec(compile(Path(b['__file__']).read_text(),b['__file__'],'exec'),b)
roomns={'__file__':str(V/'scripts/build_narrator_room_v005.py')};exec(compile(Path(roomns['__file__']).read_text(),roomns['__file__'],'exec'),roomns)
INK='#22212a';NAVY='#20263c';LIGHT='#343c57';DARK='#141a2d';SKIN='#efad82';SHADE='#d8886e';HILITE='#fac69b';UNIT=.0038
C={};LIMBS={};FAC={}

def smooth(points,closed=True):
 # Catmull-Rom sampling only constructs drawn contours; it does not generate motion.
 out=[];n=len(points)
 for i in range(n if closed else n-1):
  a=Vector(points[(i-1)%n] if closed or i else points[i]);p=Vector(points[i]);q=Vector(points[(i+1)%n]);d=Vector(points[(i+2)%n] if closed or i+2<n else points[-1])
  for j in range(6):
   t=j/6;out.append(tuple(.5*((2*p)+(-a+q)*t+(2*a-5*p+4*q-d)*t*t+(-a+3*p-3*q+d)*t*t*t)))
 if not closed:out.append(points[-1])
 return out

def shape(name,pts,z,color,parent,outline=True,soft=True):
 pts=smooth(pts) if soft else pts;o=b['poly']('F7 / '+name,pts,z,color,parent,False)
 if outline:stroke(name+' outline',pts+[pts[0]],z+.3,INK,1.15,parent,False)
 return o

def stroke(name,pts,z,color,width,parent,soft=True):
 return b['line']('F7 / '+name,smooth(pts,False) if soft else pts,z,color,width,parent)

def oval(name,x,y,rx,ry,z,color,parent,outline=False):return shape(name,b['oval'](x,y,rx,ry),z,color,parent,outline,False)
def control(name,loc,parent=None):
 ob=b['empty']('F7 / CTRL '+name,loc,parent);ob.empty_display_size=12;C[name]=ob;return ob

def setup():
 global s,col,root
 assert not bpy.app.background and bpy.context.window
 assert 'S002_v007_Ferguson_dialogue' not in bpy.data.scenes
 s=bpy.data.scenes.new('S002_v007_Ferguson_dialogue');s.collection.children.link(bpy.data.collections[roomns['ROOM']]);col=bpy.data.collections.new('S002 / Ferguson native artwork v007');s.collection.children.link(col);b['skin']=col;b['ink']=b['mat'](INK)
 old=bpy.data.scenes['S002_v005_N04_reveal'];s.world=old.world;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_end=168;s.view_settings.view_transform='Standard';s.view_settings.look='None';s.render.use_sequencer=False
 for ob in old.objects:
  if ob.type=='LIGHT':o=ob.copy();o.data=ob.data.copy();s.collection.objects.link(o)
 roomns['camera'](s,(-.10,-4.6,2.3),(0,0,1.55),5.5);s.camera.data.lens=44
 row=next(r for r in json.loads((V/'artifacts/animation-v003/edit.json').read_text()) if r['id']=='N04_meltdown');q=s.sequence_editor_create().strips.new_sound('Approved meltdown mix',str(V/'artifacts/opening-v002/mix-premaster.wav'),channel=1,frame_start=2-row['start_frame']);q.frame_offset_start=row['start_frame']-1;q.frame_final_duration=168
 root=control('character',(0,-.08,.0057749212719500065));root.rotation_euler.x=math.pi/2;root.scale=(UNIT,)*3
 s['status']='Native reconstruction and dialogue blocking; unapproved';s['construction']='Native mesh/curve artwork; separate facial shapes and articulated joints; no raster character'
 roomns['show'](s)
 return {'scene':s.name,'collection':col.name}

def limb(name,a,c,length,radius,color,z):
 ob=control(name,(a[0],a[1],z),c);LIMBS[name]=(ob,length)
 shape(name+' silhouette',[(-radius*.65,6),(-radius,0),(-radius*.9,-length*.47),(-radius*.72,-length),(radius*.72,-length),(radius*.9,-length*.47),(radius,0),(radius*.65,6)],0,color,ob)
 shape(name+' shade',[(-radius*.7,0),(-radius*.82,-length*.4),(-radius*.62,-length+2),(-radius*.12,-length+2),(-radius*.30,-length*.45),(-radius*.3,0)],.7,DARK if color==NAVY else '#353437',ob,False)
 stroke(name+' fold',[(-radius*.55,-length*.78),(0,-length*.72),(radius*.4,-length*.76)],1.1,LIGHT if color==NAVY else '#686263',.8,ob)
 return ob

def hand(name,parent,side):
 h=control(name,(0,-LIMBS[parent.name.split('CTRL ')[1]][1],3),parent)
 # Palm, thumb and articulated four-finger fan: all share one wrist.
 shape(name+' palm',[(-13,4),(-17,-7),(-14,-29),(-4,-35),(12,-30),(15,-9),(10,3)],0,SKIN,h)
 shape(name+' palm shade',[(-13,-9),(-13,-28),(-4,-33),(4,-29),(-3,-22)],.7,SHADE,h,False)
 thumb=control(name+' thumb',(-11,-10,1),h);shape(name+' thumb',[(-3,4),(-14,-6),(-21,-11),(-20,-17),(-15,-19),(-3,-11),(4,-4)],0,SKIN,thumb)
 fingers=[]
 for i,(x,l,angle) in enumerate([(-10,29,-.19),(-2,36,-.065),(6,33,.09),(13,24,.28)]):
  f=control(name+' finger '+str(i),(x,-25,1.5),h);f.rotation_euler.z=angle;shape(name+' finger '+str(i),[(-4,4),(-4,-l+4),(-2,-l),(2,-l),(4,-l+4),(4,4)],0,SKIN,f)
  stroke(name+' knuckle '+str(i),[(-2,-l*.48),(1,-l*.50),(3,-l*.45)],.6,SHADE,.6,f);fingers.append(f)
 stroke(name+' palm line',[(-6,-13),(2,-17),(6,-26)],2,SHADE,.7,h)
 FAC[name+' fingers']=fingers
 return h

def body():
 global hip,chest,head
 hip=control('pelvis',(0,250,0),root)
 for side,x in [('L',-40),('R',40)]:
  upper=limb(side+' thigh',(x,-8),hip,112,30,'#4c484a',0);lower=limb(side+' shin',(0,-112),upper,107,25,'#4c484a',.5)
  foot=control(side+' boot',(0,-107,2),lower)
  shape(side+' boot',[(-23,10),(-27,-7),(-30,-18),(-19,-22),(35,-22),(47,-16),(43,-8),(18,-2),(16,10)],0,'#202024',foot)
  shape(side+' boot shine',[(-16,4),(-16,-5),(15,-8),(30,-10),(15,-3),(8,4)],1,'#4b4c50',foot,False)
  stroke(side+' sole',[(-25,-18),(0,-19),(38,-18)],2,'#82818a',1,foot)
  for k in range(3):stroke(side+' lace '+str(k),[(-7,-2-k*3),(8,-1-k*3)],2,'#929098',.6,foot,False)
 shape('trouser pelvis',[(-65,22),(-68,-23),(-40,-43),(0,-26),(37,-43),(67,-21),(63,24)],4,'#4c484a',hip)
 stroke('trouser fly',[(0,14),(0,-12),(-8,-25)],6,'#292830',1,hip)
 chest=control('chest',(0,0,8),hip)
 for side,x in [('L',-86),('R',86)]:
  upper=limb(side+' upper arm',(x,166),chest,100,28,NAVY,0);lower=limb(side+' forearm',(0,-100),upper,101,23,NAVY,2)
  shape(side+' ribbed cuff',[(-18,-90),(-17,-103),(17,-103),(18,-90)],2,'#29314d',lower)
  for j in range(-12,16,5):stroke(side+' cuff rib '+str(j),[(j,-92),(j,-101)],3,'#10182a',.65,lower,False)
  hand(side+' hand',lower,side)
 shape('cardigan body',[(-64,-10),(-72,24),(-73,106),(-102,159),(-84,181),(-42,198),(0,200),(45,198),(83,181),(102,160),(72,103),(71,22),(62,-10)],5,NAVY,chest)
 shape('cardigan left shade',[(-88,165),(-74,130),(-65,80),(-61,27),(-24,11),(-63,9),(-70,35),(-71,111)],6,DARK,chest,False)
 shape('cardigan right light',[(72,154),(64,108),(60,51),(35,39),(53,80)],6,LIGHT,chest,False)
 shape('white shirt',[(-39,193),(0,203),(41,192),(30,159),(0,114),(-31,159)],7,'#f5ede0',chest)
 shape('neck',[(-24,224),(-25,185),(-4,167),(27,187),(26,225)],8,SKIN,chest)
 shape('left collar',[(-33,198),(-4,173),(-17,155),(-43,180)],10,'#fffbef',chest,True,False)
 shape('right collar',[(26,198),(-4,173),(13,155),(38,180)],10,'#fffbef',chest,True,False)
 shape('tie knot',[(-13,172),(9,172),(14,159),(0,149),(-13,158)],11,'#8e263b',chest,True,False)
 shape('tie',[(-6,151),(5,151),(15,126),(0,109),(-13,127)],10,'#ab3546',chest,True,False)
 stroke('tie light',[(-3,151),(-3,131),(0,119)],11,'#d56468',1.2,chest)
 stroke('cardigan V left',[(-43,190),(-30,153),(0,111)],12,'#101729',2,chest)
 stroke('cardigan V right',[(42,190),(26,148),(0,111),(0,5)],12,'#101729',2,chest)
 shape('cardigan waistband',[(-66,5),(-66,-10),(0,-16),(65,-10),(67,5),(0,0)],9,'#29314b',chest)
 for j in range(-59,62,8):stroke('waist rib '+str(j),[(j,-1),(j,-10)],10,'#141c30',.8,chest,False)
 for y in [91,58,26]:oval('button',3,y,4,4,14,'#726d65',chest,True);oval('button hole',3,y,1,1,15,'#171923',chest)
 for side in [-1,1]:
  stroke('cloth crease',[(side*65,46),(side*47,33),(side*20,31)],10,'#12182c',1.4,chest)
  stroke('shoulder stitch',[(side*48,186),(side*68,180),(side*84,164)],10,'#43495f',.8,chest)
 head=control('head',(0,199,18),chest)
 return {'native_body_objects':len(col.objects)}

def face():
 # One coherent native face; features share the head control and never replace it.
 shape('left ear',[(-51,89),(-62,99),(-69,91),(-67,66),(-55,52),(-46,60)],1,SKIN,head)
 stroke('ear cartilage',[(-58,84),(-61,87),(-61,73),(-56,70)],3,'#a66c61',1.2,head)
 shape('right ear',[(56,88),(65,93),(66,76),(59,62),(52,66)],1,SKIN,head)
 shape('face',[(-49,133),(-20,150),(24,147),(50,129),(57,99),(57,58),(52,26),(31,9),(0,6),(-27,13),(-45,34),(-51,71)],4,SKIN,head)
 shape('face side shade',[(-49,116),(-40,108),(-40,69),(-29,39),(-10,22),(32,19),(49,30),(34,10),(0,8),(-28,14),(-46,36),(-50,73)],5,SHADE,head,False)
 shape('forehead light',[(-29,115),(-24,133),(11,137),(38,123),(33,112),(8,122)],5,HILITE,head,False)
 shape('left cheek',[(-37,72),(-17,76),(-7,58),(-17,43),(-34,52)],6,'#ed947c',head,False)
 shape('right cheek',[(39,70),(54,66),(51,47),(35,42),(27,56)],6,'#df8b76',head,False)
 shape('hair mass',[(-53,84),(-59,103),(-56,130),(-47,150),(-29,161),(-8,170),(21,172),(44,162),(59,142),(62,115),(54,91),(48,112),(38,134),(16,144),(-7,142),(-29,132),(-40,119),(-43,91)],7,'#c7c2b9',head)
 shape('hair crown highlight',[(-51,136),(-39,153),(-13,164),(16,166),(43,156),(31,153),(0,157),(-24,146)],8,'#eee9df',head,False)
 shape('silver sideburn',[(-51,113),(-42,116),(-43,94),(-40,82),(-46,75),(-54,88)],8,'#eee9df',head,False)
 # Swept broken locks preserve Ferguson's distinctive silver crop.
 for i,(x,y) in enumerate([(-47,136),(-37,146),(-26,151),(-13,155),(0,158),(13,157),(28,154),(41,147)]):
  stroke('hair lock '+str(i),[(x-7,y-10),(x,y),(x+17,y+1),(x+24,y-5)],9,'#7c7979',.85,head)
 for i in range(6):stroke('side hair '+str(i),[(-54+i*2,116),(-51+i*2,104),(-48+i,96)],9,'#e9e6df',.8,head)
 # Native eyes, pupils and eyelids independent from brows/glasses.
 for side,x in [('L',-20),('R',34)]:
  e=control(side+' eye',(x,91,10),head);FAC[side+' eye']=e
  shape(side+' eye white',[(-14,0),(-8,7),(5,7),(14,1),(8,-7),(-5,-8)],0,'#fff9e7',e)
  p=control(side+' gaze',(4,0,2),e);oval(side+' iris',0,0,4.8,7,0,'#695c48',p);oval(side+' pupil',.5,0,2.6,5,1,'#23232b',p);oval(side+' glint',-.6,2,1.2,1.4,2,'#ffffff',p)
  brow=control(side+' brow',(x,111,13),head);FAC[side+' brow']=brow
  shape(side+' eyebrow',[(-18,0),(-8,5),(11,3),(18,-1),(13,-4),(-8,0)],0,'#8d8981',brow)
  stroke(side+' brow ink',[(-18,0),(-7,1),(12,-2),(18,-2)],1,'#59514e',.8,brow)
  stroke(side+' lower eye crease',[(x-13,78),(x-3,75),(x+10,77)],11,'#ad7667',.7,head)
 # Glasses: thin slightly rectangular lenses, anatomically located bridge.
 for side,x in [('L',-21),('R',35)]:
  stroke(side+' glasses',[(x-23,104),(x+21,104),(x+23,95),(x+18,78),(x-15,77),(x-23,84),(x-23,104)],17,'#61564e',1.2,head)
 stroke('glasses bridge',[(2,99),(7,103),(12,99)],18,'#514b49',1.1,head)
 stroke('glasses left temple',[(-44,100),(-55,105),(-60,94)],17,'#61564e',1.3,head)
 shape('nose',[(11,107),(13,87),(23,74),(21,65),(11,61),(2,65),(-3,72),(4,82)],19,'#dd7d68',head)
 oval('nose light',9,78,6,10,20,'#f19a7a',head)
 stroke('left nostril',[(-2,68),(3,66),(5,67)],21,'#874e4b',1,head);stroke('right nostril',[(14,65),(19,66),(22,70)],21,'#874e4b',1,head)
 for side in [-1,1]:stroke('nasolabial fold',[(side*18+6,63),(side*24+6,52),(side*27+6,38)],12,'#af7463',.8,head)
 for y in [122,130]:stroke('forehead wrinkle',[(-18,y),(-3,y-3),(8,y-2),(23,y)],10,'#b77d69',.65,head)
 stroke('frown crease',[(-1,113),(2,106),(4,111)],14,'#ac6f60',1,head)
 jaw=control('jaw',(6,31,14),head);FAC['jaw']=jaw
 stroke('chin line',[(-15,-12),(0,-16),(18,-11)],0,'#b67d69',1,jaw)
 build_mouth()
 return {'native_face_objects':len(head.children_recursive)}

def build_mouth():
 mouth=control('mouth',(8,37,23),head);FAC['mouth']=mouth;FAC['mouth shapes']={}
 # Different drawn contours, teeth and tongue; no painted-mouth compression.
 forms={'rest':(18,2,0),'MBP':(20,1,0),'A':(23,18,1),'E':(28,11,1),'O':(14,18,1),'U':(11,10,0),'FV':(21,5,1),'L':(22,12,2)}
 for label,(w,h,teeth) in forms.items():
  group=control('mouth '+label,(0,0,0),mouth);FAC['mouth shapes'][label]=group
  if label in ['rest','MBP']:
   stroke(label+' lips',[(-w,-2),(-w*.4,1),(w*.4,1),(w,-2)],0,'#713c38',1.2,group)
   stroke(label+' lower lip',[(-w*.6,-5),(0,-6),(w*.55,-5)],1,'#d08a72',.9,group)
  else:
   shape(label+' mouth cavity',[(-w,0),(-w*.7,h*.35),(0,h*.4),(w*.8,h*.2),(w,0),(w*.65,-h),(0,-h*1.2),(-w*.6,-h)],0,'#512b33',group)
   if teeth:
    shape(label+' teeth',[(-w*.79,h*.12),(w*.78,h*.12),(w*.65,-h*.24),(-w*.68,-h*.24)],1,'#fff4db',group,False)
   if h>7:shape(label+' tongue',[(-w*.55,-h*.80),(-w*.18,-h*.60),(w*.45,-h*.74),(w*.37,-h*.97),(-w*.35,-h*1.03)],2,'#d27d84',group,False)
   if teeth==2:oval(label+' tongue tip',0,-h*.15,w*.32,h*.36,3,'#dc9496',group)
   stroke(label+' lower lip',[(-w*.65,-h*1.12),(0,-h*1.35),(w*.55,-h*1.10)],1,'#ad645d',.9,group)
 return FAC['mouth shapes']

def visibility_tree(ob,visible,frame):
 for o in [ob,*ob.children_recursive]:
  if o.type not in ['MESH','CURVE']:continue
  o.hide_render=o.hide_viewport=not visible
  for p in ['hide_render','hide_viewport']:o.keyframe_insert(data_path=p,frame=frame)

def mouth_at(frame,label):
 for n,o in FAC['mouth shapes'].items():visibility_tree(o,n==label,frame)

def degrees(ob,f,value):ob.rotation_euler.z=math.radians(value);ob.keyframe_insert(data_path='rotation_euler',frame=f)

def block():
 # Distinct complete gestures: gather, assertion, exhausted breath, stop palm,
 # appeal to self, wide exasperation and recovery. Angles are individually posed.
 # f, torso, head, left upper, left elbow, left wrist, right upper, elbow, wrist
 poses=[(1,-3,4,-12,-38,4,12,38,-4),(7,-6,7,-20,-65,0,18,56,0),(15,2,-3,-42,-105,8,46,75,-10),(25,0,2,-54,-95,-8,75,62,0),(39,4,-7,-80,-65,-12,82,50,12),(47,2,-3,-75,-52,-8,74,45,8),(57,-3,7,-28,-34,0,30,30,0),(66,-5,8,-23,-30,0,26,28,0),(72,1,-3,-30,-90,5,80,5,-25),(81,3,-6,-25,-105,10,87,4,-24),(89,0,-2,-40,-100,4,59,35,-10),(97,2,-4,-60,-73,-8,37,85,8),(108,4,-8,-82,-58,-12,85,57,15),(118,2,-5,-87,-46,-8,92,36,10),(129,-1,1,-72,-41,-2,80,30,5),(141,-3,5,-40,-32,2,43,32,-2),(156,-2,4,-20,-26,0,24,28,0),(168,-2,4,-20,-26,0,24,28,0)]
 for f,t,h,lu,le,lw,ru,re,rw in poses:
  degrees(chest,f,t);degrees(head,f,h)
  for name,a in [('L upper arm',lu),('L forearm',le),('L hand',lw),('R upper arm',ru),('R forearm',re),('R hand',rw)]:degrees(C[name],f,a)
 # Planted legs, body compression then drive through the rise.
 sys.path.insert(0,str(W/'pipeline'));from pose_geometry import two_bone_joint
 feet={'L':Vector((-55,29)), 'R':Vector((57,29))}
 for f,y,x in [(1,197,0),(7,187,-3),(16,237,0),(24,242,0),(39,244,2),(57,236,0),(66,234,-2),(81,244,3),(97,241,0),(118,244,2),(141,239,0),(168,239,0)]:
  hip.location=(x,y,0);hip.keyframe_insert(data_path='location',frame=f)
  for side,sx in [('L',-40),('R',40)]:
   top=Vector((x+sx,y-8));foot=feet[side];joint=two_bone_joint(tuple(top),tuple(foot),(112,107),(-180 if side=='L' else 180,130));knee=Vector(joint)
   upper=C[side+' thigh'];lower=C[side+' shin'];a=math.atan2((knee-top).x,-(knee-top).y);bb=math.atan2((foot-knee).x,-(foot-knee).y)
   degrees(upper,f,math.degrees(a));degrees(lower,f,math.degrees(bb-a));degrees(C[side+' boot'],f,-math.degrees(bb))
 for side in ['L','R']:
  for f,ang in [(1,0),(15,-13 if side=='L' else 13),(47,-10 if side=='L' else 10),(59,0),(69,0),(75,-18 if side=='L' else 18),(126,-18 if side=='L' else 18),(145,-7 if side=='L' else 7),(168,-7 if side=='L' else 7)]:degrees(FAC[side+' brow'],f,ang)
  for f,scale in [(1,1),(53,1),(55,.07),(58,1),(135,1),(137,.06),(140,1),(168,1)]:FAC[side+' eye'].scale.y=scale;FAC[side+' eye'].keyframe_insert(data_path='scale',frame=f)
  for f,x in [(1,3),(13,5),(49,4),(57,0),(70,3),(83,5),(139,7),(168,7)]:C[side+' gaze'].location.x=x;C[side+' gaze'].keyframe_insert(data_path='location',frame=f)
 for ob in col.objects:
  if ob.animation_data:
   for layer in ob.animation_data.action.layers:
    for strip in layer.strips:
     for bag in strip.channelbags:
      for fc in bag.fcurves:
       for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type=k.handle_right_type='AUTO_CLAMPED'
 mouth_at(1,'rest');s.frame_set(25)
 return {'poses':len(poses),'frames':168}

def hand_shapes():
 for side in ['L','R']:
  h=C[side+' hand'];normal=list(h.children_recursive);fist=control(side+' closed fist',(0,0,4),h)
  shape(side+' fist',[(-13,4),(-20,-10),(-17,-24),(-10,-30),(10,-30),(19,-24),(20,-13),(15,-8),(10,-7),(6,-10),(2,-6),(-3,-9),(-8,-6),(-11,-1)],0,SKIN,fist)
  shape(side+' curled thumb',[(-16,-10),(-8,-15),(4,-17),(11,-22),(8,-27),(-5,-24),(-16,-18)],1,HILITE,fist)
  for x in [-10,-2,6,13]:stroke(side+' fist knuckle '+str(x),[(x,-11),(x+2,-15)],2,'#af725f',.8,fist)
  frames=[(1,True),(15,False),(31,False),(48,False),(55,True),(69,False),(89,side=='L'),(103,False),(142,True),(168,True)]
  for frame,closed in frames:
   for o in normal:
    if o.type in ['MESH','CURVE']:
     o.hide_render=o.hide_viewport=closed
     for prop in ['hide_render','hide_viewport']:o.keyframe_insert(data_path=prop,frame=frame)
   visibility_tree(fist,closed,frame)

def bake_support():
 sys.path.insert(0,str(W/'pipeline'));from pose_geometry import two_bone_joint
 for f in range(1,169):
  s.frame_set(f);x,y=hip.location.x,hip.location.y
  for side,sx,fx in [('L',-40,-55),('R',40,57)]:
   top=Vector((x+sx,y-8));foot=Vector((fx,29));knee=Vector(two_bone_joint(tuple(top),tuple(foot),(112,107),(-180 if side=='L' else 180,130)))
   a=math.atan2((knee-top).x,-(knee-top).y);bb=math.atan2((foot-knee).x,-(foot-knee).y)
   degrees(C[side+' thigh'],f,math.degrees(a));degrees(C[side+' shin'],f,math.degrees(bb-a));degrees(C[side+' boot'],f,-math.degrees(bb))
 for ob in col.objects:
  if not ob.animation_data:continue
  for layer in ob.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:
       if fc.data_path.startswith('hide_'):k.interpolation='CONSTANT'
       elif any(x in ob.name for x in ['thigh','shin','boot']):k.interpolation='LINEAR'
 s.frame_set(39)
 return {'support_frames':168}

def refine_art():
 # Remove transverse cap seams where the continuous garment covers a joint.
 for name,(ob,length) in LIMBS.items():
  radius=28 if 'upper arm' in name else 23 if 'forearm' in name else 30 if 'thigh' in name else 25
  edge=bpy.data.objects['F7 / '+name+' silhouette outline'];edge.hide_render=edge.hide_viewport=True
  for sign in [-1,1]:stroke(name+' outer edge '+str(sign),[(sign*radius*.65,4),(sign*radius,0),(sign*radius*.9,-length*.47),(sign*radius*.72,-length)],.4,INK,1.15,ob)
 for side in ['L','R']:
  for f in FAC[side+' hand fingers']:f.location.z=-2
  e=FAC[side+' eye'];e.scale.x=.88
  for layer in e.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      if fc.data_path=='scale' and fc.array_index==1:
       for k in fc.keyframe_points:k.co.y*=.80;k.handle_left.y*=.80;k.handle_right.y*=.80
 for i,(x,y) in enumerate([(-47,136),(-37,146),(-26,151),(-13,155),(0,158),(13,157),(28,154),(41,147)]):
  old=bpy.data.objects['F7 / hair lock '+str(i)];old.hide_render=old.hide_viewport=True
  stroke('swept hair '+str(i),[(x-5,y-9),(x+2,y-3),(x+15,y),(x+21,y-3)],9,'#858080',.7,head)
 s.frame_set(39)

def speech():
 data=json.loads((O/'speech-analysis.json').read_text());words=[w for seg in data['segments'] for w in seg.get('words',[])];assert len(words)==12
 # Drawn visemes, manually grouped within ASR word intervals. These are draft
 # phonetic placements, not claimed forced phoneme alignment or heard approval.
 patterns=[['A','E'],['E','L'],['A','E'],['U','A','E'],['U','E','A','E','L'],['E','A','MBP'],['E','FV','E'],['MBP','E'],['U','E','L','E'],['L','U'],['A','MBP'],['MBP','A','E']]
 schedule={1:'rest'};record=[]
 for w,forms in zip(words,patterns):
  start=3+round(w['start']*24);end=3+round(w['end']*24)
  for i,label in enumerate(forms):schedule[max(3,start-1+round((end-start)*i/len(forms)))]=label
  record.append({'word':w['word'].strip(),'start_frame':start,'end_frame':end,'shapes':forms})
 schedule[55]='rest';schedule[130]='rest';schedule[168]='rest'
 for f,label in sorted(schedule.items()):mouth_at(f,label)
 for f,label in sorted(schedule.items()):
  FAC['jaw'].location.y=31-({'A':4,'O':3,'E':2,'L':2,'U':1}.get(label,0));FAC['jaw'].keyframe_insert(data_path='location',frame=f)
 for ob in col.objects:
  if not ob.animation_data:continue
  for layer in ob.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      if fc.data_path.startswith('hide_'):
       for k in fc.keyframe_points:k.interpolation='CONSTANT'
 (O/'dialogue-timing.json').write_text(json.dumps({'source':'Selected meltdown.wav; local Whisper tiny word timestamps; manually assigned visemes','listening_review':'not performed by assistant','words':record,'mouth_keys':schedule},indent=2))
 s.frame_set(40)
 return {'words':len(record),'mouth_changes':len(schedule)}

def save():
 s.frame_set(40);bpy.ops.wm.save_as_mainfile(filepath=str(O/'ferguson-native-v007.blend'))
 return {'file':bpy.data.filepath}

def anger_and_stop():
 # The first render exposed wide-eyed delivery and a sideways STOP palm.
 # Act the expression and arm silhouette; do not hide the problem with camera motion.
 for side in ['L','R']:
  eye=FAC[side+' eye'];inner=-1 if side=='L' else 1
  shape(side+' angry upper lid',[(-18,13),(18,13),(18,-2 if side=='L' else 6),(-18,6 if side=='L' else -2)],6,SKIN,eye,False,False)
  stroke(side+' angry lash',[(-15,5 if side=='L' else -1),(0,2),(15,-1 if side=='L' else 5)],6.3,'#5a443e',1.2,eye)
  brow=FAC[side+' brow'];brow.location.y=105
 for f,ru,re,rw in [(72,55,95,20),(81,55,100,20)]:
  for name,value in [('R upper arm',ru),('R forearm',re),('R hand',rw)]:degrees(C[name],f,value)
 s.frame_set(73)
