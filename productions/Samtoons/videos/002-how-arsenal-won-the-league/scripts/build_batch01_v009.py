"""Bottle FC / first signing: native character acting, props and shared locations.
Author visibly: setup(), opening_cast(), opening_props(), opening_acting(),
unveiling(), narrator(), save(). Saved scenes render separately.
"""
import bpy,math,json,sys
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
V=Path(__file__).resolve().parents[1];O=V/'artifacts/batch01-v009';W=V.parents[3]
base={'__file__':str(V/'scripts/build_ferguson_native_v007.py')};exec(compile(Path(base['__file__']).read_text(),base['__file__'],'exec'),base)
b=base['b'];smooth=base['smooth'];room=base['roomns'];INK='#20232d';WHITE='#fff6e5';RED='#df1833';NAVY='#20283b';ACTORS={};SCENES={};PROPS={}
sys.path.insert(0,str(W/'pipeline'));from pose_geometry import two_bone_joint
FONT=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf',check_existing=True);b['font']=FONT;b['ink']=b['mat'](INK)

def use(s,col=None):
 global COL
 bpy.context.window.scene=s;COL=col or s.collection;b['skin']=COL;b['ink']=b['mat'](INK);b['font']=FONT

def poly(name,pts,color,z=0,parent=None,edge=True,width=.022,soft=False):
 pts=smooth(pts) if soft else pts;o=b['poly'](name,pts,z,color,parent,False)
 if edge:b['line'](name+' outline',pts+[pts[0]],z+.015,color=INK,width=width,parent=parent)
 return o

def line(name,pts,color=INK,z=0,width=.024,parent=None,soft=False):return b['line'](name,smooth(pts,False) if soft else pts,z,color,width,parent)
def rect(name,x,y,w,h,color,z=0,parent=None,edge=True):return poly(name,[(x,y),(x+w,y),(x+w,y+h),(x,y+h)],color,z,parent,edge)
def ellipse(name,x,y,rx,ry,color,z=0,parent=None,edge=False):return poly(name,b['oval'](x,y,rx,ry),color,z,parent,edge)
def text(name,body,x,y,size,color=WHITE,z=1,parent=None):return b['text'](name,body,x,y,z,size,color,parent)
def ctrl(name,loc=(0,0,0),parent=None):return b['empty'](name,loc,parent)
def key(ob,path,rows,interpolation='BEZIER'):
 for f,value in rows:setattr(ob,path,value);ob.keyframe_insert(data_path=path,frame=f)
 for layer in ob.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     if fc.data_path==path:
      for k in fc.keyframe_points:k.interpolation=interpolation;k.handle_left_type=k.handle_right_type='AUTO_CLAMPED'

def angle(ob,rows):key(ob,'rotation_euler',[(f,(0,0,math.radians(v))) for f,v in rows])
def expose(root,first,last,total):
 scale=tuple(root.scale)
 key(root,'scale',[(1,scale if first==1 else (0,0,0)),(first,scale),(last+1,(0,0,0))],'CONSTANT')

def camera(s,name,x,y,width,frame):
 d=bpy.data.cameras.new(name);d.type='ORTHO';d.ortho_scale=width;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=(x,y,40);m=s.timeline_markers.new(name,frame=frame);m.camera=o
 if not s.camera:s.camera=o
 return o

def scene(suffix,length):
 name='S002_B01_v009_'+suffix;assert name not in bpy.data.scenes
 s=bpy.data.scenes.new(name);SCENES[suffix]=s;s.use_fake_user=True;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_end=length;s.render.use_sequencer=False;s.view_settings.view_transform='Standard';s.view_settings.look='None';s.world=bpy.data.worlds.new(name+' world');s.world.color=(.15,.17,.2);use(s);return s

def setup():
 assert not bpy.app.background
 if bpy.context.screen.is_animation_playing:bpy.ops.screen.animation_cancel(restore_frame=False)
 if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(O/'live-before-batch01.blend'),copy=True)
 s=scene('opening',409)
 environment=bpy.data.collections.new('B01 / training ground shared');s.collection.children.link(environment);use(s,environment)
 rect('Training / sky',-25,-8,50,22,'#bcdce8',-15,edge=False)
 for x in range(-24,27,3):
  ellipse('Training / trees',x,5.7,2.2,1.8,'#668d67',-14);ellipse('Training / foliage',x+.5,6.4,1.5,1.1,'#82a96d',-13.9)
 rect('Training / building',-22,.7,12,4.4,'#c1cbd0',-13)
 for x in range(-21,-10,2):rect('Training / glass',x,1.1,1.45,3.4,'#729ba8',-12.8)
 rect('Training / wall',-24,.2,48,1.4,'#b94450',-12)
 for x in [-17,-9,1,12,21]:text('Training / sign','ARSENAL',x,.8,.55,WHITE,-11.8)
 for x in range(-24,25,2):line('Training / fence',[(x,.2),(x,5.5)],'#a8b8ba',-11.5,.035)
 line('Training / fence rail',[(-25,5.4),(25,5.4)],'#b3c5c6',-11.5,.04)
 rect('Training / grass',-25,-8,50,8.2,'#75a563',-11,edge=False)
 for x in range(-25,25,5):poly('Training / mowing',[(x,-8),(x+2.5,-8),(x+5,.2),(x+3,.2)],'#81b06c',-10.9,edge=False)
 line('Training / pitch line',[(-25,-3),(25,-3)],'#eeeace',-10.6,.035)
 for x in [-13,-11.5,13,14.5]:
  line('Training / dummy',[(x-.3,-.2),(x-.4,1.4),(x,1.7),(x+.4,1.4),(x+.3,-.2)],'#e67458',-10.5,.055);ellipse('Training / dummy head',x,2,.23,.3,'#e67458',-10.5)
 use(s);PROPS['ground']=environment
 camera(s,'B01 opening wide',0,.7,17.4,1);camera(s,'B01 recycled year',2.2,1.1,13.5,49);camera(s,'B01 delivery wide',0,.6,18,150);camera(s,'B01 offended Arteta',-3.4,.2,8.3,206);camera(s,'B01 driver reply',5.5,1.1,7.8,266);camera(s,'B01 phone request',-4.6,.45,7.5,338)
 room['show'](s);return {'scene':s.name,'frames':409}

def new_actor(s,name,kind,x,y,height=5,face_right=True):
 col=bpy.data.collections.new('B01 / '+name);s.collection.children.link(col);use(s,col);prefix='B01 / '+name+' / '
 n={'__file__':str(V/'scripts/build_ferguson_native_v007.py')};source=Path(n['__file__']).read_text().replace('F7 /',prefix.rstrip())
 exec(compile(source,n['__file__'],'exec'),n);n['b']['skin']=col;n['b']['ink']=n['b']['mat'](INK)
 C=n['C'];root=n['control']('character',(x,y,1));root.scale=(height/604,)*3
 hip=n['control']('pelvis',(0,245,0),root);ch=n['control']('chest',(0,0,8),hip);hd=n['control']('head',(0,202,18),ch)
 n.update(root=root,hip=hip,chest=ch,head=hd,col=col,s=s)
 skin='#efb082' if kind!='gyokeres' else '#f2bd91';n.update(SKIN=skin,SHADE='#ca8965',HILITE='#fbd1a3')
 shirt= NAVY if kind=='arteta' else '#e5b94d' if kind=='driver' else '#77858d' if kind=='worker' else RED
 for side,sign in [('L',-1),('R',1)]:
  up=n['control'](side+' upper arm',(sign*80,166,0),ch);lo=n['control'](side+' forearm',(0,-100,2),up);n['LIMBS'][side+' forearm']=(lo,101);n['hand'](side+' hand',lo,side)
  thigh=n['control'](side+' thigh',(sign*40,-8,0),hip);shin=n['control'](side+' shin',(0,-112,.5),thigh);boot=n['control'](side+' boot',(0,-107,2),shin)
  pts=[(-24,13),(-25,-9),(-22,-22),(32,-22),(46,-17),(45,-9),(19,0),(17,13)]
  poly(prefix+side+' shoe',[(sign*a,b_) for a,b_ in pts],WHITE if kind=='gyokeres' else '#273041',0,boot,width=1.15,soft=True)
  line(prefix+side+' sole',[(sign*-22,-18),(sign*8,-19),(sign*42,-15)],RED if kind=='gyokeres' else '#e5e4df',2,1.7,boot)
  for k in range(3):line(prefix+side+' lace',[(sign*-7,-k*3),(sign*9,-k*3-1)],'#b3b9bd',2,.7,boot)
  if kind=='gyokeres':
   for xx in [-17,12,31]:rect(prefix+'stud',sign*xx-2,-25,5,5,'#b73142',.7,boot,False)
  else:
   for k in range(3):line(prefix+'trainer stripe',[(sign*(8+k*7),-2),(sign*(1+k*7),-10)],WHITE,2,1.8,boot)
 # Native facial construction follows the selected Arteta/Gyokeres design, with independent eyes/brows/mouth.
 def sh(label,pts,c,z,par=hd,edge=True):return poly(prefix+label,pts,c,z,par,edge,1.05,True)
 def ln(label,pts,c,z,w=.85,par=hd):return line(prefix+label,pts,c,z,w,par,True)
 sh('neck',[(-24,225),(-26,190),(0,176),(25,193),(25,226)],skin,8,ch,False)
 sh('neck shade',[(-24,221),(-12,201),(12,202),(24,218),(19,191),(0,180),(-23,192)],'#cb8b67',9,ch,False)
 face=[(-46,128),(-29,144),(12,150),(43,135),(50,111),(51,79),(58,54),(51,25),(31,8),(-3,6),(-29,20),(-44,43),(-49,78)]
 if kind=='driver':face=[(-48,122),(-30,139),(17,142),(45,129),(53,103),(61,79),(59,46),(47,19),(22,6),(-12,7),(-41,22),(-52,61)]
 sh('face',face,skin,4);sh('ear',[(-45,90),(-57,101),(-66,88),(-62,69),(-48,57),(-39,68)],skin,5)
 ln('ear detail',[(-54,85),(-57,89),(-58,77),(-50,72)],'#a76c53',7,1)
 sh('face plane',[(-43,112),(-32,95),(-34,65),(-24,37),(-4,22),(30,20),(49,33),(40,14),(14,7),(-8,10),(-30,23),(-45,50)],'#d2936c',5,edge=False)
 sh('forehead light',[(-25,121),(-17,138),(17,140),(36,127),(24,119),(2,127)],'#f9c999',5,edge=False)
 if kind in ['arteta','gyokeres']:
  beard='#55463c' if kind=='arteta' else '#aa8457'
  sh('stubble shade',[(-35,59),(-25,40),(-5,28),(24,28),(48,39),(48,24),(29,10),(-1,10),(-25,22),(-38,39)],beard,6,edge=False)
  sh('chin skin',[(-12,36),(12,40),(33,33),(29,19),(9,16),(-6,23)],skin,7,edge=False)
  for i in range(20):
   xx=-31+(i%10)*7;yy=24+(i//10)*9;ln('stubble',[(xx,yy),(xx+1,yy+2)],'#785c46',7,.4)
 hair='#151c23' if kind=='arteta' else '#a47744' if kind=='gyokeres' else '#5e4631'
 sh('hair',[(-52,81),(-58,106),(-54,131),(-47,145),(-38,143),(-28,158),(-18,155),(-4,165),(6,161),(22,166),(38,158),(45,161),(54,144),(46,129),(25,135),(5,131),(-10,120),(-26,111),(-31,87),(-37,73)],hair,8)
 for i in range(8):
  xx=-46+i*11;yy=139+11*math.sin(i*.35);ln('hair sweep',[(xx-3,yy-9),(xx+6,yy+3),(xx+20,yy+4)],'#39414c' if kind=='arteta' else '#dbb374',9,1)
 if kind in ['driver','worker']:
  sh('cap',[(-58,118),(-59,138),(-34,158),(8,162),(42,149),(50,128),(5,131),(-35,125)],'#9c693a' if kind=='driver' else '#465d73',10)
  sh('cap peak',[(-56,123),(-25,134),(26,132),(47,121),(25,113),(-21,118)],'#b07c48' if kind=='driver' else '#34475a',11)
 eyes={};brows={}
 for side,xx in [('L',-15),('R',31)]:
  e=n['control'](side+' eye',(xx,94,11),hd);eyes[side]=e
  sh(side+' eye',[(-13,0),(-6,8),(7,9),(14,3),(9,-6),(-6,-7)],'#fff9e7',0,e)
  gaze=n['control'](side+' gaze',(4,1,2),e);ellipse(prefix+'iris',0,0,4.4,6,'#715c44',0,gaze);ellipse(prefix+'pupil',.5,0,2.4,4.4,INK,1,gaze);ellipse(prefix+'eye glint',-.7,2,1,1.3,WHITE,2,gaze)
  brow=n['control'](side+' brow',(xx,112,13),hd);brows[side]=brow;sh(side+' brow',[(-16,0),(-7,7),(12,5),(17,0),(10,1),(-4,2)],hair,0,brow,False)
  ln(side+' under eye',[(xx-10,82),(xx-1,79),(xx+8,81)],'#b47d60',12,.6)
 sh('nose',[(15,108),(16,88),(29,72),(27,65),(15,61),(6,66),(5,73),(12,83)],skin,17)
 ln('nostril',[(11,66),(16,65),(21,67)],'#95634e',19,.8)
 if kind=='driver':sh('moustache',[(1,62),(9,66),(16,62),(24,66),(36,59),(40,52),(27,48),(17,52),(8,48),(-2,51)],'#533c29',22)
 n['build_mouth']();C['mouth'].location=(15,43 if kind!='driver' else 39,23)
 for label,ob in n['FAC']['mouth shapes'].items():
  for child in ob.children_recursive:
   if child.type in ['MESH','CURVE']:child.hide_render=child.hide_viewport=label!='rest'
 if not face_right:hd.scale.x=-1
 # Garment detail attaches to chest, above the connected surface baked later.
 if kind=='gyokeres':
  sh('jersey front',[(-49,192),(-22,178),(20,178),(48,193),(64,168),(60,104),(69,22),(59,-8),(-60,-8),(-67,25),(-59,108),(-64,167)],RED,5,ch,False)
  sh('jersey shade',[(-55,154),(-45,128),(-48,64),(-29,34),(-57,17),(-61,60)],'#b41530',6,ch,False)
  ln('jersey fold',[(-48,21),(-12,15),(23,21),(48,30)],'#ae1b32',7,1,ch)
  for sign in [-1,1]:
   ln('jersey side seam',[(sign*55,141),(sign*58,56),(sign*61,6)],WHITE,8,1.3,ch)
  text(prefix+'sponsor','Emirates',0,118,27,WHITE,10,ch);text(prefix+'sponsor small','FLY BETTER',0,96,11,WHITE,10,ch)
  text(prefix+'shirt mark','///',-35,157,20,WHITE,10,ch);crest(ctrl(prefix+'crest',(36,152,10),ch),.6)
 else:
  sh('shirt left shade',[(-63,148),(-50,120),(-53,61),(-44,31),(-10,16),(-57,6),(-68,47)],'#151d2d' if kind=='arteta' else '#b08a38' if kind=='driver' else '#4d606c',6,ch,False)
  sh('shirt side light',[(60,150),(51,113),(57,60),(42,25),(62,39),(67,83)],'#303b50' if kind=='arteta' else '#f4d175' if kind=='driver' else '#97a3aa',6,ch,False)
  for yy in [26,49]:ln('shirt fold',[(-55,yy),(-24,yy-8),(13,yy-4),(45,yy+6)],'#121b2b' if kind=='arteta' else '#806c45',7,1.2,ch)
  if kind=='driver':
   for xx in [-42,13]:rect(prefix+'pocket',xx,89,29,31,'#e7ba56',8,ch);line(prefix+'polo placket',[(0,177),(0,90)],'#8d682d',9,1,ch)
 sh('collar',[(-31,200),(-22,186),(0,180),(23,187),(30,199)],WHITE if kind=='gyokeres' else '#111b29' if kind=='arteta' else '#c69b41',10,ch,False)
 # Cloth meshes have fixed strip topology; their points follow the real joint controls.
 a={'name':name,'kind':kind,'scene':s,'col':col,'n':n,'C':C,'root':root,'skin':skin,'shirt':shirt,'eyes':eyes,'brows':brows,'prefix':prefix};ACTORS[name]=a
 n['b']['skin']=col;use(s);return a

def crest(parent,scale=1):
 parent.scale=(scale,)*3
 ellipse(parent.name+'wheel',0,0,11,11,WHITE,0,parent)
 line(parent.name+'cannon',[(-20,5),(23,5)],WHITE,1,3,parent);line(parent.name+'axle',[(0,-11),(0,11)],RED,1,1,parent)

def mouths(a,phrases):
 n=a['n'];groups=n['FAC']['mouth shapes'];total=a['scene'].frame_end
 schedule={1:'rest'}
 for first,last,pattern in phrases:
  chars=pattern.split();step=(last-first)/max(1,len(chars))
  for i,label in enumerate(chars):schedule[round(first+i*step)]=label
  schedule[last]='rest'
 for f,label in sorted(schedule.items()):
  for k,g in groups.items():
   for child in g.children_recursive:
    if child.type in ['MESH','CURVE']:
     child.hide_render=child.hide_viewport=k!=label
     child.keyframe_insert(data_path='hide_render',frame=f);child.keyframe_insert(data_path='hide_viewport',frame=f)
 for e in a['eyes'].values():key(e,'scale',[(1,(1,1,1)),(total,(1,1,1))])
 for f in [35,117,203,323]:
  if f+5<total:
   for e in a['eyes'].values():key(e,'scale',[(f,(1,1,1)),(f+2,(1,.10,1)),(f+5,(1,1,1))])

def pose(a,rows):
 # Frame, chest tilt, head tilt, L upper/elbow/wrist, R upper/elbow/wrist.
 C=a['C']
 for i,name in enumerate(['chest','head','L upper arm','L forearm','L hand','R upper arm','R forearm','R hand'],1):angle(C[name],[(r[0],r[i]) for r in rows])
 # Grounded small weight shifts: solve both supports after chest/hip acting is authored.
 for f in range(1,a['scene'].frame_end+1):
  a['scene'].frame_set(f);hip=C['pelvis'].location
  for side,x in [('L',-55),('R',55)]:
   top=Vector((hip.x+(-40 if side=='L' else 40),hip.y-8));foot=Vector(a.get('foot_samples',{}).get(f,{}).get(side,(x,22)));knee=Vector(two_bone_joint(tuple(top),tuple(foot),(112,107),(-160 if side=='L' else 160,130)))
   aa=math.atan2((knee-top).x,-(knee-top).y);bb=math.atan2((foot-knee).x,-(foot-knee).y)
   for name,v in [(side+' thigh',aa),(side+' shin',bb-aa),(side+' boot',-bb)]:C[name].rotation_euler.z=v;C[name].keyframe_insert(data_path='rotation_euler',frame=f)
 a['scene'].frame_set(1)

def bake_clothes(a):
 s=a['scene'];use(s,a['col']);C=a['C'];kind=a['kind'];prefix=a['prefix'];made={}
 def meshpose(label,pts,faces,colors,ids,frame,parent,z):
  if frame==1:
   me=bpy.data.meshes.new(prefix+label);ob=bpy.data.objects.new(prefix+label,me);COL.objects.link(ob);ob.parent=parent;me.from_pydata([(p.x,p.y,z) for p in pts],[],faces)
   for c in colors:me.materials.append(b['mat'](c))
   for p,idx in zip(me.polygons,ids):p.material_index=idx
   made[label]=ob;k=ob.shape_key_add(name='Pose 001');me.shape_keys.use_relative=False
  else:ob=made[label];k=ob.shape_key_add(name=f'Pose {frame:03}')
  for v,p in zip(k.data,pts):v.co=(p.x,p.y,z)
  k.interpolation='KEY_LINEAR';keys=ob.data.shape_keys;keys.eval_time=(frame-1)*10;keys.keyframe_insert(data_path='eval_time',frame=frame)
 def ribbon(a0,knee,end,radii):
  v1=knee-a0;v2=end-knee;tm=(v1.normalized()+v2.normalized())*min(v1.length,v2.length)*.25;centres=[];rs=[]
  for start,finish,t0,t1,seg in [(a0,knee,v1*.85,tm,0),(knee,end,tm,v2*.85,1)]:
   for j in range(16 if seg==0 else 17):
    t=j/16;centres.append((2*t**3-3*t*t+1)*start+(t**3-2*t*t+t)*t0+(-2*t**3+3*t*t)*finish+(t**3-t*t)*t1);rs.append(radii[seg]*(1-t)+radii[seg+1]*t)
  norms=[]
  for i in range(33):d=centres[min(i+1,32)]-centres[max(i-1,0)];d.normalize();norms.append(Vector((-d.y,d.x)))
  return centres,rs,norms
 def edges(centres,rs,norms):return [p+n*r for p,r,n in zip(centres,rs,norms)],[p-n*r for p,r,n in zip(centres,rs,norms)]
 def strip_faces(count):return [(2*i,2*i+1,2*i+3,2*i+2) for i in range(count-1)]
 def stroke(label,path,f,parent,z):
  area=sum(p.x*q.y-q.x*p.y for p,q in zip(path,path[1:]+path[:1]));direction=1 if area>0 else -1;pts=[]
  for i,p in enumerate(path):
   d=path[(i+1)%len(path)]-path[(i-1)%len(path)];d.normalize();normal=Vector((d.y,-d.x))*direction;pts.extend([p-normal*.55,p+normal*1.15])
  faces=[(2*i,2*i+1,(2*i+3)%len(pts),(2*i+2)%len(pts)) for i in range(len(path))];meshpose(label,pts,faces,[INK],[0]*len(faces),f,parent,z)
 for f in range(1,s.frame_end+1):
  s.frame_set(f);bpy.context.view_layer.update();ch=C['chest'];inv=ch.matrix_world.inverted();sides={}
  for side,sign in [('L',-1),('R',1)]:
   start=(inv@C[side+' upper arm'].matrix_world.translation).xy;middle=(inv@C[side+' forearm'].matrix_world.translation).xy;end=(inv@C[side+' hand'].matrix_world.translation).xy
   centres,rs,norms=ribbon(start,middle,end,(23,19,12));positive,negative=edges(centres,rs,norms);outer,inner=(negative,positive) if side=='L' else (positive,negative)
   for edge,anchor in [(outer,Vector((sign*59,188))),(inner,Vector((sign*63,125)))]:
    target=edge[7].copy()
    for j in range(7):edge[j]=anchor.lerp(target,j/7)
   sides[side]=(outer,inner)
   shade=[]
   for j in range(33):
    fade=min(1,j/6,(32-j)/6);shade.extend([outer[j].lerp(inner[j],.75-.16*fade),outer[j].lerp(inner[j],.75+.16*fade)])
   cols=['#111c2e'] if kind=='arteta' else ['#c2c7d1','#d4916c'] if kind=='gyokeres' else ['#b28b36','#d4916c'] if kind=='driver' else ['#4f606c','#d4916c']
   meshpose(side+' sleeve shade',shade,strip_faces(33),cols,[0 if kind=='arteta' or j<(8 if kind=='gyokeres' else 15) else 1 for j in range(32)],f,ch,.8)
  ro,ri=sides['R'];lo,li=sides['L'];waist=[Vector(p) for p in [(64,91),(67,51),(65,11),(57,-11),(0,-14),(-57,-11),(-65,11),(-67,51),(-64,91)]];neck=[Vector(p) for p in [(-29,201),(0,202),(29,201)]]
  core=[ro[0],ri[0]]+waist+[li[0],lo[0]]+neck;pts=core[:];faces=[tuple(x) for x in tessellate_polygon([[Vector((p.x,p.y,0)) for p in core]])];ids=[0]*len(faces)
  for outer,inner,pair in [(ro,ri,(0,1)),(lo,li,(12,11))]:
   prev=pair
   for j in range(1,33):
    pair=(len(pts),len(pts)+1);pts.extend([outer[j],inner[j]]);faces.append((prev[0],pair[0],pair[1],prev[1]));prev=pair;ids.append(1 if kind!='arteta' and j>(8 if kind=='gyokeres' else 15) else 0)
  colors=[NAVY] if kind=='arteta' else [WHITE,a['skin']] if kind=='gyokeres' else [a['shirt'],a['skin']]
  meshpose('connected upper body',pts,faces,colors,ids,f,ch,0)
  stroke('garment exterior',ro+list(reversed(ri))+waist+li+list(reversed(lo))+neck,f,ch,-.2)
  inv=C['character'].matrix_world.inverted()
  for side in ['L','R']:
   start=(inv@C[side+' thigh'].matrix_world.translation).xy;knee=(inv@C[side+' shin'].matrix_world.translation).xy;end=(inv@(C[side+' boot'].matrix_world@Vector((0,5,0)))).xy
   centres,rs,norms=ribbon(start,knee,end,(29,21,18));one,two=edges(centres,rs,norms);pts=[p for pair in zip(one,two) for p in pair];faces=strip_faces(33)
   cols=[NAVY] if kind=='arteta' else [WHITE,a['skin'],RED,WHITE] if kind=='gyokeres' else ['#4d5b65']
   ids=[0 if kind!='gyokeres' or j<10 else 1 if j<20 else 2 if j<30 else 3 for j in range(32)]
   meshpose(side+' leg cloth',pts,faces,cols,ids,f,C['character'],.2);stroke(side+' leg contour',one+list(reversed(two)),f,C['character'],0)
   shade=[]
   for j in range(33):
    fade=min(1,j/5,(32-j)/5);shade.extend([centres[j]+norms[j]*rs[j]*(-.66-.16*fade),centres[j]+norms[j]*rs[j]*(-.66+.16*fade)])
   cols=['#141f31'] if kind=='arteta' else ['#c6cbd1','#d29970','#aa1c34','#c6cbd1'] if kind=='gyokeres' else ['#354652']
   meshpose(side+' leg shade',shade,faces,cols,ids,f,C['character'],.5)
 for o in made.values():
  for layer in o.data.shape_keys.animation_data.action.layers:
   for st in layer.strips:
    for bag in st.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='LINEAR'
 # Hip fill and waist are not independently outlined across the thigh joins.
 hip=C['pelvis'];color=WHITE if kind=='gyokeres' else NAVY if kind=='arteta' else '#4d5b65'
 poly(prefix+'hip cloth',[(-59,12),(59,12),(60,-29),(34,-45),(0,-26),(-34,-45),(-60,-29)],color,5,hip,False,soft=True)
 if kind=='gyokeres':
  text(prefix+'shorts number','14',33,-26,20,RED,8,hip);crest(ctrl(prefix+'shorts crest',(-34,-21,8),hip),.40)
  for sign in [-1,1]:line(prefix+'shorts stripe',[(sign*56,1),(sign*57,-29)],RED,8,1.4,hip)
 else:line(prefix+'fly',[(0,0),(-1,-15),(-7,-25)],'#111b2c',7,1,hip)
 s.frame_set(1);use(s);return {'actor':a['name'],'deformed_surfaces':len(made)}

def opening_cast():
 s=SCENES['opening'];art=new_actor(s,'opening Arteta','arteta',-4.8,-2.9,4.8);worker=new_actor(s,'banner worker','worker',5.9,-2.9,4.1,False);driver=new_actor(s,'delivery driver','driver',5.1,-1.7,3.2,False)
 # Two players listen at the left edge; their eyes/head react separately.
 p=new_actor(s,'preseason player','gyokeres',-8.2,-2.9,4.8);p['C']['head'].rotation_euler.z=.06
 use(s);room['show'](s);return {'actors':list(ACTORS)}

def opening_props():
 s=SCENES['opening'];use(s)
 banner=ctrl('B01 banner',(2.3,.75,-5));PROPS['banner']=banner
 for x in [-4.2,4.2]:line('Banner support',[(x,-3.65),(x,3.8)],'#7c8992',0,.06,banner)
 rect('Banner cloth',-4.15,-.35,8.3,3.9,'#cb3448',.1,banner)
 for i in range(10):poly('Banner fold',[(i*.82-4.1,-.3),(i*.82-3.87,3.5),(i*.82-3.45,3.5)],'#bc263d',.2,banner,False)
 text('Banner slogan','THIS IS OUR YEAR',0,2.0,.63,WHITE,.5,banner)
 crest(ctrl('Banner cannon',(0,3.05,.4),banner),.025)
 rect('Permanent year label',-.9,.15,2.2,1,'#fff6df',.5,banner);text('New year','2026',.2,.65,.8,INK,.6,banner)
 year=ctrl('B01 removable 2025',(.2,.65,.8),banner);rect('Old year paper',-1.1,-.5,2.2,1,'#f3ead8',0,year);text('Old year','2025',0,0,.8,INK,.1,year);PROPS['year']=year
 cover=ctrl('B01 unveiling cover',(0,0,1.2),banner);rect('Cover fabric',-4.2,-.4,8.4,4.0,'#e54754',0,cover);PROPS['cover']=cover
 rope=ctrl('B01 banner pull cord',(-4.3,.45,1),banner);line('Cord',[(0,3.2),(0,0),(-.1,-.5)],'#eacb7e',.1,.025,rope)
 # Native lorry: wheels rotate from travel, cab settles after braking.
 truck=ctrl('B01 delivery truck',(13,-2.75,-1));PROPS['truck']=truck
 rect('Lorry chassis',-4.5,.4,8.6,.35,'#293039',.1,truck)
 rect('Lorry box',-4.4,1.1,6.5,3.55,'#f4f2e8',.2,truck);rect('Lorry upper trim',-4.4,4.5,6.5,.17,'#cbd1d3',.4,truck)
 text('Delivery title','BOTTLE FC',-1.6,3.37,.74,'#164c38',.6,truck);text('Delivery subtitle','ANNUAL DELIVERY',-1.65,2.52,.39,'#164c38',.6,truck)
 bottle=ctrl('Lorry bottle emblem',(.91,3.15,.6),truck);angle(bottle,[(1,-16)]);poly('Bottle',[(-.2,-.8),(.2,-.8),(.23,.4),(.11,.55),(.11,.94),(-.11,.94),(-.11,.55),(-.23,.4)],'#164c38',0,bottle,False)
 poly('Cab outer',[(2.1,.65),(4.6,.65),(4.65,3.4),(4.1,4.5),(2.15,4.5)],'#eef0e9',.6,truck)
 rect('Cab window',2.38,2.08,1.87,1.93,'#253743',.8,truck);rect('Cab window sky',2.55,2.22,1.57,1.58,'#96c4d8',.9,truck)
 # Driver is placed in front of this window; foreground door occludes the lower body.
 door=ctrl('B01 cab foreground',(0,0,2.0),truck);poly('Cab door panel',[(2.14,.68),(4.62,.68),(4.62,2.06),(2.14,2.06)],'#e8eae3',.1,door)
 rect('Cab door handle',2.4,1.77,.4,.08,INK,.3,door)
 rect('Headlight',4.34,1,.29,.39,'#f8dda6',2.2,truck);rect('Bumper',2.11,.60,2.63,.18,'#707d83',2.3,truck)
 for x in [-2.9,.7,3.5]:
  wheel=ctrl('B01 truck wheel',(x,.66,2.5),truck);ellipse('Tyre',0,0,.66,.66,'#252b32',0,wheel,True);ellipse('Rim',0,0,.36,.36,'#87949b',.1,wheel)
  for i in range(6):
   t=math.tau*i/6;ellipse('Lug',.22*math.cos(t),.22*math.sin(t),.035,.035,INK,.2,wheel)
  PROPS.setdefault('wheels',[]).append(wheel)
 # Cellphone is attached to Arteta's hand, not an independently moving picture.
 a=ACTORS['opening Arteta'];use(s,a['col']);phone=ctrl('B01 Arteta phone',(0,-12,12),a['C']['R hand']);rect('Phone case',-14,-19,28,54,'#151b25',0,phone);rect('Phone screen',-11,-12,22,39,'#7294a1',.1,phone);ellipse('Phone camera',0,30,2,2,'#999e9c',.2,phone);PROPS['phone']=phone
 use(s);return {'props':'banner with removable year, truck with native wheels, held phone'}

def opening_acting():
 s=SCENES['opening'];use(s);a=ACTORS['opening Arteta']
 pose(a,[(1,0,0,-18,-25,2,45,32,-25),(12,-3,3,-15,-40,5,67,41,-20),(35,1,-3,-13,-25,0,78,38,-25),(49,0,2,-18,-20,0,60,48,-25),(73,-2,4,-20,-30,0,76,40,-25),(108,1,-3,-17,-23,0,60,55,-20),(146,0,0,-13,-15,0,15,25,-5),(164,-2,5,-15,-30,0,20,20,0),(189,3,-5,-16,-45,0,28,44,10),(206,-2,4,-30,-63,10,42,77,-25),(226,3,-6,-28,-70,8,62,65,-20),(246,2,-4,-25,-65,6,58,56,-18),(266,0,2,-16,-35,0,22,35,0),(304,-2,-5,-18,-38,0,17,36,0),(328,-2,-6,-20,-44,4,10,45,0),(340,0,-3,-24,-64,10,0,145,-15),(352,2,-5,-25,-65,10,-5,152,-12),(378,-1,4,-25,-63,10,-4,150,-12),(394,2,-4,-25,-64,10,7,132,-13),(409,0,0,-20,-45,5,25,48,-15)])
 mouths(a,[(67,127,'E U MBP FV E E A MBP L A MBP'),(213,239,'A O E E A MBP'),(346,386,'E MBP E A E A MBP O')])
 for brow in a['brows'].values():angle(brow,[(1,0),(148,0),(193,-10),(330,-12),(409,-8)])
 w=ACTORS['banner worker'];pose(w,[(1,0,4,-25,-30,0,-55,-95,-20),(48,0,4,-25,-30,0,-55,-95,-20),(56,2,0,-28,-40,10,-66,-92,-10),(76,-3,4,-35,-51,10,-48,-72,-10),(96,-5,6,-25,-45,10,-28,-50,-10),(120,-2,4,-20,-35,0,-20,-30,0),(409,-2,4,-20,-35,0,-20,-30,0)])
 mouths(w,[])
 d=ACTORS['delivery driver'];pose(d,[(1,0,0,-15,-55,20,15,55,-20),(260,0,0,-15,-55,20,15,55,-20),(273,-3,3,-35,-80,10,37,80,-10),(290,2,-3,-52,-85,12,55,75,-10),(310,0,3,-43,-72,5,48,68,-10),(328,0,0,-18,-55,15,18,55,-15),(409,0,0,-18,-55,15,18,55,-15)])
 mouths(d,[(272,319,'O E MBP FV O E A MBP E')])
 p=ACTORS['preseason player'];pose(p,[(1,0,0,-10,-14,0,10,14,0),(60,-1,3,-10,-15,0,10,14,0),(99,1,-4,-14,-22,0,16,25,0),(149,0,0,-10,-14,0,10,14,0),(409,0,0,-10,-14,0,10,14,0)]);mouths(p,[])
 key(PROPS['cover'],'scale',[(1,(1,1,1)),(5,(1,1,1)),(30,(.015,1,1)),(40,(0,1,1))])
 key(PROPS['year'],'location',[(1,(.2,.65,.8)),(54,(.2,.65,.8)),(64,(.85,.5,1)),(77,(2.2,-.2,1.3)),(98,(3.4,-1.2,1.3))]);angle(PROPS['year'],[(1,0),(54,0),(66,-14),(80,-24),(98,-36)])
 key(PROPS['truck'],'location',[(1,(13,-2.75,-1)),(150,(13,-2.75,-1)),(191,(1.6,-2.75,-1)),(199,(1.48,-2.78,-1)),(205,(1.55,-2.75,-1)),(409,(1.55,-2.75,-1))])
 for wheel in PROPS['wheels']:angle(wheel,[(1,0),(150,0),(191,math.degrees(11.4/.66)),(205,math.degrees(11.45/.66)),(409,math.degrees(11.45/.66))])
 # Driver follows the cab's travel. Character root remains independent for acting.
 d['root'].parent=PROPS['truck'];d['root'].location=(3.23,1.46,1.2)
 for actor in [a,w,d,p]:bake_clothes(actor)
 expose(w['root'],1,149,409);expose(p['root'],1,149,409);expose(PROPS['banner'],1,149,409);expose(PROPS['truck'],150,409,409);expose(PROPS['phone'],338,409,409)
 s.frame_set(226);room['show'](s);s.frame_set(226);return {'opening_frames':409,'native_characters':4}

def refine_cast(a):
 use(a['scene'],a['col']);prefix=a['prefix'];C=a['C'];kind=a['kind']
 # Focused eyes, subtle stubble and a real jumper neckline preserve the selected likeness.
 if kind in ['arteta','gyokeres']:
  ob=bpy.data.objects.get(prefix+'stubble shade');ob.data.materials[0]=b['mat']('#b68762' if kind=='arteta' else '#b79468')
  C['mouth'].scale=(.72,.82,1)
  for side,e in a['eyes'].items():
   pts=[(-16,14),(16,14),(16,3 if side=='L' else 7),(-16,7 if side=='L' else 3)]
   poly(prefix+side+' focused lid',pts,a['skin'],5,e,False)
   line(prefix+side+' eyelash',[(-14,6 if side=='L' else 2),(0,5),(14,2 if side=='L' else 6)],'#604738',5.1,.8,e)
  if kind=='arteta':
   # Remove shoulder shading that exceeded the new shared garment boundary.
   ob=bpy.data.objects[prefix+'shirt left shade'];pts=smooth([(-47,153),(-45,120),(-49,61),(-40,30),(-12,16),(-56,6),(-61,47)])
   ob.data.clear_geometry();ob.data.from_pydata([(x,y,6) for x,y in pts],[],[tuple(range(len(pts)))]);ob.data.materials.clear();ob.data.materials.append(b['mat']('#151d2d'))
   neck=bpy.data.objects[prefix+'collar'];neck.hide_render=neck.hide_viewport=True
   line(prefix+'jumper neckline',[(-29,198),(-23,183),(-3,176),(18,181),(29,196)],'#0f1725',11,2.3,C['chest'],True)
   line(prefix+'neckline highlight',[(-25,195),(-18,183),(-2,180),(14,184)],'#39455b',11.1,.7,C['chest'],True)
   poly(prefix+'jumper ribbed hem',[(-63,5),(63,5),(61,-12),(0,-16),(-61,-12)],NAVY,9,C['chest'],False,soft=True)
   line(prefix+'jumper waist seam',[(-60,4),(0,0),(60,4)],'#10192b',10,1,C['chest'],True)
   for xx in range(-52,55,8):line(prefix+'hem rib',[(xx,-3),(xx,-10)],'#131d2e',10,.6,C['chest'])
 if kind in ['driver','worker']:C['mouth'].scale=(.76,.75,1)
 use(a['scene'])

def opening_contacts():
 s=SCENES['opening'];use(s)
 for a in [ACTORS[n] for n in ['opening Arteta','banner worker','delivery driver','preseason player']]:refine_cast(a)
 d=ACTORS['delivery driver'];d['root'].scale=(4.1/604,)*3;d['root'].location=(3.23,.15,1.2)
 # The card follows the worker's actual finger contact throughout its peel.
 w=ACTORS['banner worker'];year=PROPS['year'];year.animation_data_clear();banner=PROPS['banner'];w['root'].animation_data_clear()
 s.frame_set(54);bpy.context.view_layer.update();tip=w['C']['L hand'].matrix_world@Vector((0,-43,2));wanted=banner.matrix_world@Vector((1.2,1.05,1.05));w['root'].location+=Vector((wanted.x-tip.x,wanted.y-tip.y,0));bpy.context.view_layer.update()
 for f in range(1,150):
  s.frame_set(f);bpy.context.view_layer.update()
  if f<54:loc=Vector((.2,.65,.8));theta=0
  else:
   grip=banner.matrix_world.inverted()@(w['C']['L hand'].matrix_world@Vector((0,-43,2)));u=min(1,(f-54)/48);theta=-.6*u;offset=Vector((math.cos(theta)-.4*math.sin(theta),math.sin(theta)+.4*math.cos(theta)));loc=Vector((grip.x-offset.x,grip.y-offset.y,1.05))
  year.location=loc;year.rotation_euler.z=theta;year.keyframe_insert(data_path='location',frame=f);year.keyframe_insert(data_path='rotation_euler',frame=f)
 # Stable ladder supports the raised worker at the banner.
 xx,yy=w['root'].location.x,w['root'].location.y
 for dx in [-.47,.47]:line('Worker ladder rail',[(xx+dx,-2.9),(xx+dx,yy+.1)],'#526774',-.3,.055)
 for step in range(7):
  sy=-2.8+step*(yy+2.8)/6;line('Worker ladder rung',[(xx-.5,sy),(xx+.5,sy)],'#b7c3c5',-.2,.045)
 expose(w['root'],1,149,409)
 # Phone: solve a hand target next to the ear for the held line, retain preparation/recovery.
 a=ACTORS['opening Arteta'];C=a['C'];upper=C['R upper arm'];lower=C['R forearm']
 for f in range(338,410):
  s.frame_set(f);u=max(0,min(1,(f-338)/12));u=u*u*(3-2*u)
  if f>393:u=max(0,1-(f-393)/16)
  target=Vector((80+(65-80)*u,-5+240*u));start=Vector((80,166));knee=Vector(two_bone_joint(tuple(start),tuple(target),(100,101),(175,145)))
  aa=math.atan2((knee-start).x,-(knee-start).y);bb=math.atan2((target-knee).x,-(target-knee).y)
  for ob,ang in [(upper,aa),(lower,bb-aa),(C['R hand'],-bb)]:ob.rotation_euler.z=ang;ob.keyframe_insert(data_path='rotation_euler',frame=f)
 # Re-bake only this changed arm/body pose; remove the previous baked surfaces first.
 for o in list(a['col'].objects):
  if o.type=='MESH' and o.data.shape_keys:bpy.data.objects.remove(o,do_unlink=True)
 for name in ['hip cloth','fly']:
  for o in list(a['col'].objects):
   if o.name==a['prefix']+name:bpy.data.objects.remove(o,do_unlink=True)
 bake_clothes(a)
 # Fingers wrap the phone instead of spreading through it during the call.
 for side in ['R']:
  for i in range(4):key(C[side+' hand finger '+str(i)],'scale',[(1,(1,1,1)),(337,(1,1,1)),(350,(1,.35,1)),(393,(1,.35,1)),(409,(1,1,1))])
 s.frame_set(375);return {'contact_pass':'worker card, seated driver, phone-to-ear'}

def unveiling():
 s=scene('unveiling',432);s.collection.children.link(PROPS['ground']);use(s)
 camera(s,'B01 striker arrival',-1.6,.4,13.8,1);pan=camera(s,'B01 carpet reveal',-1.6,.4,13.8,193);key(pan,'location',[(193,(-1.6,.4,40)),(206,(-1.6,.4,40)),(255,(7.4,.4,40)),(288,(7.4,.4,40))]);camera(s,'B01 flag reactions',.3,.4,12.8,289)
 poly('Unveiling / red carpet',[(-6.2,-3.2),(12.1,-3.2),(11.4,-1.7),(-6.2,-1.7)],'#ac253d',-.7)
 line('Unveiling / carpet gold edge',[(-6.2,-3.17),(12.06,-3.17),(11.4,-1.73),(-6.2,-1.73)],'#deb966',-.6,.026)
 flag=ctrl('B01 real star flag',(10.1,-2.9,.3));line('Flag pole',[(0,0),(0,5.4)],WHITE,0,.045,flag)
 banner=ctrl('Flag waving cloth',(0,5.35,.1),flag);poly('Flag',[(0,0),(1.15,-.23),(.86,-.55),(0,-.67)],RED,0,banner);angle(banner,[(1,0),(190,0),(217,8),(231,-4),(248,3),(272,0),(432,0)])
 shirt=ctrl('Flag number nine shirt',(0,2.8,.2),flag);poly('Flag jersey',[(-.6,.85),(.6,.85),(1.12,.42),(.8,-.04),(.6,.12),(.65,-1.12),(-.65,-1.12),(-.6,.12),(-.8,-.04),(-1.12,.42)],RED,0,shirt)
 for sign in [-1,1]:poly('Flag white sleeve',[(sign*.6,.85),(sign*1.12,.42),(sign*.8,-.04),(sign*.6,.12),(sign*.46,.64)],WHITE,.1,shirt,False)
 line('Flag collar',[(-.25,.82),(0,.60),(.25,.82)],WHITE,.2,.025,shirt);text('Star signing number','9',0,-.25,1.2,WHITE,.2,shirt)
 gy=new_actor(s,'unveiling Gyokeres','gyokeres',-3.25,-2.9,5.2);ar=new_actor(s,'unveiling Arteta','arteta',3.2,-2.9,4.8,False)
 # Two grounded steps after setting down the travel bag, with independent support targets.
 C=gy['C'];key(C['pelvis'],'location',[(1,(0,242,0)),(22,(0,230,0)),(31,(0,230,0)),(47,(0,244,0)),(56,(4,234,0)),(78,(39,234,0)),(103,(78,245,0)),(116,(80,245,0)),(432,(80,245,0))])
 samples={}
 for f in range(1,433):
  row={}
  for side,start,end,first,last in [('L',-55,65,53,76),('R',55,155,82,105)]:
   u=max(0,min(1,(f-first)/(last-first)));row[side]=(start+(end-start)*(u*u*(3-2*u)),22+38*math.sin(math.pi*u))
  samples[f]=row
 gy['foot_samples']=samples
 pose(gy,[(1,-2,5,-7,-5,0,9,10,0),(22,5,-6,-6,-4,0,11,18,0),(31,5,-6,-6,-4,0,11,18,0),(47,0,2,-9,-12,0,12,16,0),(57,1,-2,-18,-21,0,20,21,0),(77,-1,3,-8,-16,0,11,25,0),(100,0,0,-18,-25,0,18,17,0),(119,0,1,-11,-20,0,12,19,0),(180,0,3,-10,-16,0,11,18,0),(219,1,-5,-11,-17,0,13,20,0),(270,-2,6,-15,-26,0,16,25,0),(293,-3,5,-24,-67,8,25,60,-12),(319,2,-5,-45,-80,10,42,75,-10),(342,1,-3,-39,-73,6,41,67,-8),(361,-1,5,-24,-42,0,25,45,0),(391,-2,4,-20,-35,0,19,35,0),(415,-3,7,-11,-18,0,13,19,0),(432,-3,7,-11,-18,0,13,19,0)])
 pose(ar,[(1,0,0,-20,-35,0,15,15,0),(80,1,-2,-21,-35,0,16,20,0),(151,-1,3,-22,-35,0,22,35,0),(183,0,-2,-22,-40,0,50,45,-20),(207,2,-4,-25,-45,0,76,25,-12),(249,0,2,-24,-43,0,72,35,-16),(289,0,2,-25,-43,0,67,40,-20),(342,-1,3,-20,-40,0,55,50,-20),(360,2,-4,-18,-42,0,70,33,-15),(392,0,-1,-22,-42,0,72,31,-14),(432,0,-1,-22,-42,0,72,31,-14)])
 mouths(gy,[(301,339,'E A MBP A E')]);mouths(ar,[(351,376,'U E MBP A O E')])
 bake_clothes(gy);bake_clothes(ar);refine_cast(gy);refine_cast(ar)
 # A real bag follows the grip until contact; it remains on the carpet after release.
 use(s);bag=ctrl('B01 Gyokeres travel bag');s.frame_set(26);bpy.context.view_layer.update();grip=gy['C']['L hand'].matrix_world@Vector((0,-40,3));height=grip.y+2.9
 rect('Bag body',-.78,0,1.56,.82,'#233349',0,bag);poly('Bag rounded top',[(-.78,.8),(-.60,1.0),(.6,1.0),(.78,.8)],'#30465b',.1,bag)
 line('Bag handle',[(-.25,.9),(-.19,height),(0,height+.025),(.19,height),(.25,.9)],'#172638',.2,.035,bag)
 line('Bag zip',[(-.65,.84),(.65,.84)],'#bfc9ce',.2,.015,bag);text('Bag number','14',.40,.42,.38,WHITE,.3,bag)
 for f in range(1,433):
  s.frame_set(f);bpy.context.view_layer.update()
  if f<=26:pt=gy['C']['L hand'].matrix_world@Vector((0,-40,3));loc=(pt.x,pt.y-height,2.2);fixed=loc
  else:loc=fixed
  bag.location=loc;bag.keyframe_insert(data_path='location',frame=f)
 PROPS['bag']=bag;s.frame_set(315);room['show'](s);s.frame_set(315);return {'scene':s.name,'frames':432,'actions':'bag contact, two supported steps, carpet camera reveal, dialogue'}

def narrator():
 s=scene('narrator',180);use(s);s.collection.children.link(bpy.data.collections['S002 / Narrator room / shared v005'])
 source=bpy.data.scenes['S002_v005_N01'];s.world=source.world
 for ob in source.objects:
  if ob.type in ['LIGHT','CAMERA']:
   o=ob.copy();o.data=ob.data.copy();s.collection.objects.link(o)
   if ob==source.camera:s.camera=o
 use(s);root=ctrl('B01 hidden narrator',(0,0,.68));root.rotation_euler=(math.pi/2,0,math.pi);root.scale=(.0038,)*3
 torso=ctrl('Narrator / torso',(0,0,0),root);head=ctrl('Narrator / head',(0,192,2),torso)
 dark='#090e18';edge='#182431'
 poly('Narrator / sweater',[(-68,-10),(68,-10),(80,66),(94,150),(68,179),(34,193),(-34,193),(-68,179),(-94,150),(-80,66)],dark,1,torso,False,soft=True)
 poly('Narrator / neck',[(-24,180),(24,180),(25,220),(-24,220)],dark,1,torso,False)
 poly('Narrator / back of head',[(-54,54),(-57,103),(-45,145),(-22,166),(12,169),(45,153),(58,118),(54,64),(34,29),(-15,26),(-44,40)],dark,2,head,False,soft=True)
 poly('Narrator / ear left',[(-52,101),(-65,105),(-64,76),(-50,64)],dark,1,head,False,soft=True);poly('Narrator / ear right',[(52,100),(65,104),(65,76),(52,62)],dark,1,head,False,soft=True)
 line('Narrator / subtle rim',[(-52,112),(-44,144),(-21,160),(9,164)],edge,3,1.6,head,True)
 targets={}
 for side,sign in [('L',-1),('R',1)]:
  sh=ctrl('Narrator / '+side+' shoulder',(sign*79,157,0),torso);el=ctrl('Narrator / '+side+' elbow',(sign*104,74,0),torso);ha=ctrl('Narrator / '+side+' hand',(sign*139,92,0),torso)
  b['driven_limb']('Narrator / '+side+' connected sleeve',[sh,el,ha],21,dark,torso,.4)
  ellipse('Narrator / '+side+' hand',0,0,14,21,dark,2,ha);targets[side]=(sh,el,ha)
 remote=ctrl('Narrator / remote',(-2,14,3),targets['R'][2]);rect('Remote casing',-10,-11,20,57,'#131e2a',0,remote,False);ellipse('Remote power',0,37,2.2,2.2,'#7694a7',1,remote)
 key(targets['R'][2],'location',[(1,(135,89,0)),(6,(147,107,0)),(12,(147,105,0)),(25,(139,92,0)),(180,(139,92,0))]);key(targets['R'][1],'location',[(1,(104,74,0)),(7,(113,83,0)),(25,(104,74,0)),(180,(104,74,0))])
 angle(torso,[(1,0),(24,0),(68,-2),(118,-3),(150,-3),(180,-3)]);angle(head,[(1,0),(39,1),(79,-1),(125,2),(180,2)])
 # Camera has one deliberate introductory push, then holds through the dry line.
 cam=s.camera;start=cam.location.copy();target=Vector((.5,-.45,1.2));end=start+(target-start)*.045;key(cam,'location',[(1,tuple(start)),(55,tuple(end)),(180,tuple(end))])
 room['show'](s);return {'scene':s.name,'shared_room':True,'narrator_identity':'concealed native back view'}

def save():
 manifest=[]
 rows=json.loads((V/'artifacts/animation-v003/edit.json').read_text())[:10]
 for row in rows:
  group='narrator' if row['id']=='N01' else 'opening' if row['start_frame']<590 else 'unveiling';offset=0 if group=='narrator' else 180 if group=='opening' else 589
  manifest.append({**row,'scene':SCENES[group].name,'local_start':row['start_frame']-offset})
 (O/'edit.json').write_text(json.dumps(manifest,indent=2)+'\n')
 for group,s in SCENES.items():
  seq=s.sequence_editor_create();offset={'narrator':0,'opening':180,'unveiling':589}[group];q=seq.strips.new_sound('Approved batch mix',str(V/'artifacts/opening-v002/mix-premaster.wav'),channel=1,frame_start=1-offset);q.frame_offset_start=offset;q.frame_final_duration=s.frame_end
 room['show'](SCENES['opening']);SCENES['opening'].frame_set(226);bpy.ops.wm.save_as_mainfile(filepath=str(O/'batch01-native-v009.blend'));return {'file':bpy.data.filepath,'frames':1021}
