"""Improve native character artwork while retaining v007 control animation exactly.
Run clone(), clothing(), hands_and_shoes(), inherit_new_visibility(), likeness(),
sleeves(), unify_garment(), full_body_view(), save() visibly.
"""
import bpy,math,json,hashlib
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v008'
n={'__file__':str(V/'scripts/build_ferguson_native_v007.py')};exec(compile(Path(n['__file__']).read_text(),n['__file__'],'exec'),n)
b=n['b'];smooth=n['smooth'];INK='#211f29';MAP={}

def clone():
 global s,col,C
 assert not bpy.app.background and 'S002_v008_Ferguson_dialogue' not in bpy.data.scenes
 if bpy.context.screen.is_animation_playing:bpy.ops.screen.animation_cancel(restore_frame=False)
 if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(O/'live-before-v008.blend'),copy=True)
 src=bpy.data.scenes['S002_v007_Ferguson_dialogue'];old=bpy.data.collections['S002 / Ferguson native artwork v007']
 s=src.copy();s.name='S002_v008_Ferguson_dialogue';s.use_fake_user=True;s.collection.children.unlink(old);col=bpy.data.collections.new('S002 / Ferguson native artwork v008');s.collection.children.link(col)
 for ob in old.objects:
  c=ob.copy();c.name=ob.name.replace('F7 /','F8 /');c.data=ob.data.copy() if ob.data else None
  if c.animation_data and c.animation_data.action:c.animation_data.action=c.animation_data.action.copy()
  col.objects.link(c);MAP[ob]=c
 for oldob,c in MAP.items():
  if oldob.parent in MAP:c.parent=MAP[oldob.parent]
 C={o.name.split('CTRL ')[1]:o for o in col.objects if 'CTRL ' in o.name};b['skin']=col;b['ink']=b['mat'](INK)
 n['roomns']['show'](s);s.frame_set(43);s['status']='Artwork refinement; v007 motion retained; unreviewed'
 return {'scene':s.name,'objects':len(col.objects),'preserved_source':src.name}

def outline(name,pts,z,parent,color=INK,width=1.15):
 name='F8 / '+name;ob=bpy.data.objects.get(name)
 if ob and ob.name in col.objects:
  d=ob.data;d.splines.clear();d.bevel_depth=width;d.materials.clear();d.materials.append(b['mat'](color))
 else:
  d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=width;d.bevel_resolution=2;d.materials.append(b['mat'](color));ob=bpy.data.objects.new(name,d);col.objects.link(ob);ob.parent=parent
 sp=d.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,(x,y) in zip(sp.points,pts):p.co=(x,y,z,1)
 return ob

def line(name,pts,z,color,parent,width=.8):return outline(name,smooth(pts,False),z,parent,color,width)
def shape(name,pts,z,color,parent,edge=True,soft=True):
 pts=smooth(pts) if soft else pts;ob=bpy.data.objects.get('F8 / '+name)
 if ob and ob.name in col.objects:
  mesh=ob.data;mesh.clear_geometry();mesh.from_pydata([(*p,z) for p in pts],[],[list(range(len(pts)))]);mesh.materials.clear();mesh.materials.append(b['mat'](color))
 else:ob=b['poly']('F8 / '+name,pts,z,color,parent,False)
 if edge:outline(name+' outline',pts+[pts[0]],z+.3,parent)
 return ob

def ellipse(name,x,y,rx,ry,z,color,parent,edge=False):return shape(name,b['oval'](x,y,rx,ry),z,color,parent,edge,False)
def hide(name):
 o=bpy.data.objects.get('F8 / '+name)
 if o and o.name in col.objects:o.hide_render=o.hide_viewport=True

def clothing():
 ch=C['chest'];hp=C['pelvis']
 # Stockier torso and soft, asymmetric hanging cardigan. All control positions stay fixed.
 shape('cardigan body',[(-76,-10),(-87,12),(-91,54),(-83,110),(-103,153),(-101,165),(-83,180),(-43,194),(-6,193),(43,194),(84,179),(103,163),(102,151),(83,107),(93,49),(87,11),(73,-11),(0,-17)],5,'#232940',ch)
 shape('cardigan left shade',[(-72,164),(-69,144),(-69,111),(-76,69),(-77,36),(-65,22),(-30,15),(-43,4),(-76,5),(-87,29),(-86,67),(-81,109)],6,'#151c30',ch,False)
 shape('cardigan right light',[(77,165),(71,139),(77,104),(86,69),(82,39),(63,22),(32,15),(62,34),(67,60),(60,99),(64,141)],6,'#303750',ch,False)
 shape('cardigan belly plane',[(-59,46),(-26,35),(4,38),(45,33),(65,46),(61,19),(24,8),(-23,13),(-65,25)],6.2,'#292f48',ch,False)
 shape('left underarm fold',[(-78,135),(-60,123),(-46,88),(-57,103),(-63,106),(-69,114)],7,'#12192d',ch,False)
 shape('right underarm fold',[(80,139),(62,113),(48,92),(59,126)],7,'#151b30',ch,False)
 shape('left drape fold',[(-73,62),(-42,51),(-16,56),(-42,43),(-69,49)],7,'#171d32',ch,False)
 shape('right drape fold',[(69,62),(45,55),(24,59),(45,47),(74,52)],7,'#1a2137',ch,False)
 shape('waist compression',[(-75,17),(-38,9),(1,15),(45,9),(78,16),(42,3),(6,8),(-30,1)],7,'#151d31',ch,False)
 shape('cardigan waistband',[(-78,3),(-76,-13),(-36,-18),(5,-18),(73,-12),(80,2),(40,-4),(0,-3),(-40,-4)],9,'#29314a',ch)
 for j in range(-59,62,8):hide('waist rib '+str(j))
 for j in range(-70,76,7):line('knit rib '+str(j),[(j,-3),(j*.985,-12)],10,'#121a2d',ch,.55)
 for old in ['cloth crease','cloth crease.001','shoulder stitch','shoulder stitch.001']:hide(old)
 for side in [-1,1]:
  line('shoulder seam '+str(side),[(side*48,185),(side*69,178),(side*87,166)],8,'#4c5265',ch,.7)
  line('lower fold highlight '+str(side),[(side*72,21),(side*43,18),(side*20,22)],8,'#444b63',ch,.7)
 shape('white shirt',[(-39,193),(-4,197),(40,192),(30,160),(1,113),(-31,160)],7,'#e7e3dc',ch)
 shape('shirt light',[(-28,180),(-4,174),(23,179),(12,141),(0,126),(-15,153)],7.4,'#fff9eb',ch,False)
 shape('neck',[(-27,220),(-29,191),(-17,179),(-3,172),(21,185),(31,209),(27,224)],8,'#e9a783',ch)
 shape('neck shadow',[(-26,218),(-17,200),(5,197),(24,212),(17,192),(-4,177),(-26,193)],8.4,'#c5846d',ch,False)
 shape('left collar',[(-34,197),(-4,175),(-17,157),(-42,181)],10,'#fff8eb',ch,True)
 shape('right collar',[(27,195),(-3,174),(14,156),(37,182)],10,'#f0ede4',ch,True)
 shape('tie knot',[(-13,173),(9,171),(14,159),(0,150),(-13,159)],11,'#8e2e3e',ch)
 shape('tie knot light',[(-10,170),(-1,168),(6,171),(0,152),(-5,156)],11.5,'#b34650',ch,False)
 shape('tie',[(-6,150),(5,152),(15,126),(0,109),(-13,127)],10,'#8f2939',ch)
 line('tie stitch',[(-2,149),(-3,131),(0,120)],11,'#c7585d',ch,1)
 shape('trouser pelvis',[(-73,15),(-75,-11),(-68,-37),(-38,-51),(-12,-38),(0,-32),(38,-52),(70,-31),(75,14)],4,'#48434a',hp,False)
 hide('trouser pelvis outline')
 shape('trouser fly shade',[(0,10),(4,-9),(-4,-31),(-16,-34),(-6,-13)],5,'#302f36',hp,False)
 line('trouser fly',[(0,9),(-1,-11),(-8,-25)],6,'#292830',hp,1)
 for side in ['L','R']:
  for segment,length,radius in [('thigh',112,32),('shin',107,26)]:
   ob=C[side+' '+segment]
   shape(side+' '+segment+' silhouette',[(-radius*.8,7),(-radius,0),(-radius*.93,-length*.36),(-radius*.72,-length*.73),(-radius*.76,-length+5),(-radius*.68,-length),(radius*.80,-length),(radius*.67,-length*.70),(radius*.85,-length*.30),(radius,0),(radius*.70,8)],0,'#48434a',ob,False)
   shape(side+' '+segment+' shade',[(-radius*.78,1),(-radius*.85,-length*.38),(-radius*.55,-length*.94),(-radius*.16,-length*.98),(-radius*.36,-length*.52),(-radius*.30,2)],.7,'#302f36',ob,False)
   shape(side+' '+segment+' light',[(radius*.55,-5),(radius*.46,-length*.42),(radius*.6,-length*.83),(radius*.28,-length*.65),(radius*.15,-length*.36)],.9,'#5b5459',ob,False)
   for sign in [-1,1]:line(side+' '+segment+' outer edge '+str(sign),[(sign*radius*.75,3),(sign*radius*.94,-length*.3),(sign*radius*.72,-length*.8),(sign*radius*.73,-length)],.4,INK,ob,1.05)
   line(side+' '+segment+' crease',[(radius*.08,-9),(-radius*.07,-length*.42),(radius*.10,-length*.75)],1.3,'#302e35',ob,.8)
   line(side+' '+segment+' fold',[(-radius*.60,-length*.83),(-radius*.10,-length*.76),(radius*.28,-length*.80)],1.4,'#6c6265',ob,.65)
 return {'changed':'torso silhouette, cloth drape, collar/tie, trousers'}

def hands_and_shoes():
 for side in ['L','R']:
  h=C[side+' hand']
  shape(side+' hand palm',[(-11,5),(-16,-4),(-18,-13),(-15,-28),(-9,-34),(3,-36),(12,-31),(16,-22),(14,-7),(10,4)],0,'#f0b48b',h)
  shape(side+' hand palm shade',[(-14,-6),(-16,-17),(-12,-29),(-5,-33),(3,-29),(-3,-19),(-5,-10)],.7,'#d99176',h,False)
  line(side+' hand palm line',[(-7,-12),(-8,-21),(-4,-29)],2,'#ba7d66',h,.65)
  line(side+' palm heart line',[(-10,-10),(-1,-13),(7,-10),(10,-14)],2,'#c38a70',h,.55)
  thumb=C[side+' hand thumb'];shape(side+' hand thumb',[(-3,4),(-10,1),(-16,-6),(-21,-12),(-21,-16),(-17,-18),(-12,-15),(-7,-10),(2,-6),(5,0)],0,'#efb28a',thumb)
  line(side+' thumb crease',[(-11,-8),(-8,-9),(-5,-11)],1,'#b87b65',thumb,.55)
  for i,(length,width,bend) in enumerate([(28,4.8,-1.5),(34,5.0,1),(31,4.6,2.1),(23,3.8,3)]):
   f=C[side+' hand finger '+str(i)]
   shape(side+' hand finger '+str(i),[(-width,3),(-width-1,-8),(-width+.2+bend*.4,-length*.65),(-width+1.5+bend,-length+2),(-.5+bend,-length),(width-1+bend,-length+1),(width+bend,-length+5),(width+.2,-length*.55),(width,3)],0,'#efb18a',f)
   line(side+' hand knuckle '+str(i),[(-width*.7+bend*.2,-length*.48),(-.2+bend*.2,-length*.51),(width*.55+bend*.2,-length*.48)],.7,'#bc7e66',f,.50)
   line(side+' finger tip '+str(i),[(bend-width*.5,-length+5),(bend,-length+4),(bend+width*.5,-length+5)],.8,'#d09074',f,.4)
  fist=C[side+' closed fist'];shape(side+' fist',[(-12,5),(-19,-6),(-20,-15),(-16,-26),(-9,-31),(11,-30),(19,-24),(21,-14),(17,-7),(10,-5),(6,-8),(1,-4),(-4,-7),(-9,-4)],0,'#efb28b',fist)
  shape(side+' curled thumb',[(-16,-8),(-9,-13),(2,-14),(11,-18),(12,-22),(8,-27),(-3,-24),(-15,-17)],1,'#f5c29a',fist)
  foot=C[side+' boot'];sign=-1 if side=='L' else 1
  pts=[(-22,12),(-24,-1),(-26,-12),(-22,-19),(-10,-22),(31,-22),(46,-17),(46,-11),(40,-5),(19,1),(15,13)]
  # Both shoes now turn out naturally; sole height and ankle controls are unchanged.
  shape(side+' boot',[(x*sign,y) for x,y in pts],0,'#202024',foot)
  shape(side+' boot shine',[(x*sign,y) for x,y in [(-16,8),(-17,-3),(-10,-9),(13,-10),(34,-12),(29,-7),(12,0),(9,9)]],1,'#434448',foot,False)
  shape(side+' toe cap',[(x*sign,y) for x,y in [(11,-4),(24,-4),(40,-10),(42,-14),(24,-17),(8,-14)]],1.4,'#292a30',foot,False)
  line(side+' sole',[(x*sign,y) for x,y in [(-24,-17),(-8,-19),(24,-19),(43,-15)]],2,'#77767b',foot,.9)
  line(side+' toe shine',[(x*sign,y) for x,y in [(21,-7),(31,-8),(37,-10)]],2,'#9b9ba0',foot,.8)
  for k in range(3):line(side+' lace '+str(k),[(x*sign,y) for x,y in [(-8,-1-k*3),(-1,-2-k*3),(8,-1-k*3)]],2.2,'#aaa4a4',foot,.6)
  line(side+' shoe seam',[(x*sign,y) for x,y in [(-18,6),(-14,-6),(-2,-12)]],2,'#16171f',foot,.75)
 return {'changed':'palm/thumb anatomy, tapered curved fingers, laced outward shoes'}

def likeness():
 h=C['head']
 # Broader jowls, shorter forehead, thinner rectangular spectacles and swept hair.
 shape('face',[(-52,130),(-34,141),(-4,144),(27,141),(49,126),(55,103),(60,77),(63,56),(60,30),(44,13),(20,5),(-7,5),(-33,14),(-48,31),(-53,57),(-52,93)],4,'#ecac83',h)
 shape('face side shade',[(-51,111),(-43,99),(-45,70),(-37,43),(-25,29),(-6,23),(22,19),(48,31),(57,47),(59,30),(44,14),(20,6),(-7,6),(-31,14),(-47,32),(-52,59)],5,'#cf9076',h,False)
 shape('forehead light',[(-34,116),(-24,134),(-1,137),(24,132),(42,119),(23,122),(7,117),(-8,122)],5,'#f6bb92',h,False)
 shape('left cheek',[(-40,75),(-31,82),(-19,76),(-13,63),(-20,54),(-36,57)],6,'#df947b',h,False)
 shape('right cheek',[(36,79),(52,75),(59,62),(54,48),(42,51),(31,67)],6,'#db8c75',h,False)
 shape('jowl highlight',[(-29,34),(-13,28),(13,28),(34,34),(40,24),(28,16),(0,13),(-22,21)],6,'#f2b38a',h,False)
 shape('brow ridge left',[(-42,108),(-29,115),(-9,109),(-4,101),(-16,104),(-28,107)],9,'#d39477',h,False)
 shape('brow ridge right',[(17,106),(26,114),(46,113),(53,106),(35,108),(22,100)],9,'#d39477',h,False)
 shape('hair mass',[(-54,83),(-59,102),(-58,123),(-52,140),(-41,151),(-26,158),(-10,162),(6,165),(23,163),(40,157),(53,146),(59,129),(56,109),(52,94),(48,112),(39,128),(23,137),(4,137),(-12,132),(-26,128),(-35,119),(-40,106),(-42,87)],7,'#bab8b0',h)
 shape('hair crown highlight',[(-48,139),(-36,153),(-15,163),(14,164),(39,155),(26,151),(8,151),(-13,145),(-35,132)],8,'#e2e0d7',h,False)
 shape('silver sideburn',[(-54,112),(-44,111),(-41,94),(-39,80),(-46,75),(-54,89)],8,'#d6d5cd',h,False)
 for i in range(8):hide('swept hair '+str(i));hide('hair lock '+str(i))
 for i in range(6):hide('side hair '+str(i))
 locks=[([(-51,125),(-43,136),(-24,142),(-5,140)],'#8a8885'),([(-43,145),(-24,155),(0,157),(21,152)],'#95928c'),([(-31,145),(-15,151),(7,150),(28,143)],'#aaa59b'),([(-35,136),(-17,142),(0,139),(12,135)],'#f0e9dc'),([(-13,156),(7,162),(30,156),(44,150)],'#f4eee3'),([(9,144),(25,145),(39,138),(45,127)],'#ece5d7'),([(-56,116),(-51,105),(-47,95)],'#ece9dd'),([(-50,125),(-45,114),(-42,104)],'#868481')]
 for i,(pts,color) in enumerate(locks):line('hair sweep detail '+str(i),pts,9,color,h,.9 if i<5 else .7)
 for i in range(7):
  x=-39+i*11;line('fine hair '+str(i),[(x,145+(i%3)*4),(x+8,147+(i%3)*4),(x+19,141+(i%3)*4)],9.2,'#c9c6bd',h,.45)
 for side,x in [('L',-21),('R',35)]:
  pts=[(x-20,101),(x+18,101),(x+19,93),(x+15,81),(x-13,80),(x-20,85),(x-20,101)]
  outline(side+' glasses',smooth(pts,False),17,h,'#5f5c58',.75)
  brow=C[side+' brow'];shape(side+' eyebrow',[(-18,0),(-11,4),(-5,3),(0,4),(8,1),(17,-1),(12,-3),(3,-1),(-7,0)],0,'#aaa69b',brow,False)
  line(side+' brow ink',[(-17,-1),(-8,1),(3,-1),(15,-2)],1,'#57514a',brow,.7)
  line(side+' lower eye crease',[(x-15,77),(x-5,73),(x+9,75)],11,'#aa7866',h,.75)
  line(side+' eye bag lower',[(x-11,72),(x-3,70),(x+6,72)],11,'#c98e75',h,.55)
  for i in range(3):line(side+' crow foot '+str(i),[(x+(-21 if side=='L' else 20),87-i*3),(x+(-25 if side=='L' else 23),86-i*4)],11,'#b27d68',h,.45)
 line('glasses bridge',[(-2,98),(7,101),(15,98)],18,'#66615b',h,.65)
 line('glasses left temple',[(-41,98),(-53,105),(-59,97)],17,'#66615b',h,.85)
 shape('nose',[(8,101),(12,92),(13,83),(23,77),(25,71),(20,65),(10,62),(0,65),(-5,70),(-3,77),(4,82)],19,'#d98370',h)
 ellipse('nose light',7,78,6,7,20,'#ec9c7e',h)
 line('left nostril',[(-3,69),(2,67),(6,68)],21,'#884f48',h,.85)
 line('right nostril',[(15,66),(21,67),(23,72)],21,'#884f48',h,.85)
 line('nose bridge light',[(9,97),(8,88),(6,85)],20,'#f5b58c',h,.8)
 for old in ['nasolabial fold','nasolabial fold.001','forehead wrinkle','forehead wrinkle.001','frown crease']:hide(old)
 line('left mouth fold',[(-8,64),(-18,57),(-22,46),(-23,33)],12,'#b47562',h,.85)
 line('right mouth fold',[(25,63),(33,56),(36,44),(40,36)],12,'#a86b5e',h,.85)
 line('left jowl crease',[(-45,51),(-40,36),(-31,28)],12,'#b17d69',h,.65)
 line('right jowl crease',[(52,47),(53,34),(44,24)],12,'#b17d69',h,.65)
 for y,offset in [(123,0),(130,4)]:line('forehead line '+str(y),[(-28+offset,y),(-14,y-2),(0,y-4),(16,y-1),(29-offset,y)],10,'#be876d',h,.6)
 line('brow furrow left',[(-3,115),(1,109),(2,104)],14,'#a86e5a',h,.8)
 line('brow furrow right',[(10,114),(7,108),(7,104)],14,'#a86e5a',h,.7)
 jaw=C['jaw'];line('chin line',[(-22,-10),(-9,-15),(6,-16),(23,-10)],0,'#b67c67',jaw,.8)
 line('chin lower crease',[(-10,-20),(4,-21),(14,-18)],1,'#c88a70',jaw,.6)
 return {'changed':'Ferguson jowls, silver crop, smaller spectacles, nose and facial planes'}

def inherit_new_visibility():
 # New palm/finger details must follow the existing open/fist exposure, not leak.
 for ob in col.objects:
  if ob.type not in ['MESH','CURVE'] or not ob.parent:continue
  if ob.animation_data and ob.animation_data.action:
   if not ob.animation_data.action_slot:ob.animation_data.action_slot=ob.animation_data.action.slots[0]
   continue
  siblings=[o for o in ob.parent.children if o!=ob and o.type in ['MESH','CURVE'] and o.animation_data and o.animation_data.action]
  if siblings:
   source=siblings[0];ob.animation_data_create();ob.animation_data.action=source.animation_data.action.copy();ob.animation_data.action_slot=ob.animation_data.action.slots[0]
 return {'checked':'new details inherit original hand visibility'}

def sleeves():
 # Native garment contours cover articulated seams without changing joint motion.
 # ponytail: contours are baked for this shot; rerun this function after changing poses.
 made=[]
 for o in list(col.objects):
  if ' continuous sleeve ' in o.name or ' continuous trouser ' in o.name:bpy.data.objects.remove(o,do_unlink=True)
 for kind,side in [(kind,side) for kind in ['sleeve','trouser'] for side in ['L','R']]:
  arm=kind=='sleeve';ch=C['chest' if arm else 'pelvis'];upper=C[side+(' upper arm' if arm else ' thigh')];lower=C[side+(' forearm' if arm else ' shin')];tip=C[side+(' hand' if arm else ' boot')]
  for ctrl in [upper,lower]:
   for o in ctrl.children:
    if o.type in ['MESH','CURVE'] and 'cuff' not in o.name:o.hide_render=o.hide_viewport=True
  objects={}
  palette=[INK,'#232940','#151c30','#343c53','#11192b','#485066'] if arm else [INK,'#48434a','#302f36','#5b5459','#302e35','#6c6265']
  for layer,color,z in zip(['outline','cloth','underside','light','fold','glint'],palette,[-.1,.3,.5,.7,1.,1.1]):
   me=bpy.data.meshes.new('F8 '+side+' '+kind+' '+layer);o=bpy.data.objects.new('F8 / '+side+' continuous '+kind+' '+layer,me);col.objects.link(o);o.parent=ch;me.materials.append(b['mat'](color));objects[layer]=(o,z)
  for frame in range(1,169):
   s.frame_set(frame);bpy.context.view_layer.update();inv=ch.matrix_world.inverted();a=(inv@upper.matrix_world.translation).xy;middle=(inv@lower.matrix_world.translation).xy;wrist=(inv@tip.matrix_world.translation).xy
   if arm:a.x*=.70;a.y-=8
   v1=middle-a;v2=wrist-middle;end=wrist-v2.normalized()*9 if arm else (inv@(tip.matrix_world@Vector((0,-5,0)))).xy;v2=end-middle;tm=(v1.normalized()+v2.normalized())*min(v1.length,v2.length)*.25
   r0,r1,r2=(27,23,17) if arm else (31,23,24)
   centres=[];radii=[]
   for start,finish,t0,t1,segment in [(a,middle,v1*.85,tm,0),(middle,end,tm,v2*.85,1)]:
    for j in range(17 if segment else 16):
     t=j/16;p=(2*t**3-3*t*t+1)*start+(t**3-2*t*t+t)*t0+(-2*t**3+3*t*t)*finish+(t**3-t*t)*t1;centres.append(p)
     radii.append((r0*(1-t)+r1*t+2*math.sin(t*math.pi)) if segment==0 else (r1*(1-t)+r2*t+2*math.sin(t*math.pi)))
   normals=[]
   for i,p in enumerate(centres):
    d=centres[min(i+1,len(centres)-1)]-centres[max(0,i-1)];d.normalize();normals.append(Vector((-d.y,d.x)))
   def strip(lo,hi,begin=0,end=None,extra=0,taper=False):
    ids=list(range(begin,len(centres) if end is None else end));edges=[]
    for sign in [1,-1]:
     edge=[]
     for j,i in enumerate(ids):
      fade=min(1,j/6,(len(ids)-1-j)/6) if taper else 1
      offset=(lo+hi)/2+sign*(hi-lo)/2*fade;edge.append(centres[i]+normals[i]*(radii[i]+extra)*offset)
     edges.extend(edge if sign==1 else reversed(edge))
    return edges
   contours={'outline':strip(-1,1,extra=1.25),'cloth':strip(-1,1),'underside':strip(-.96,-.48,1,len(centres)-1,taper=True),'light':strip(.40,.76,3,len(centres)-3,taper=True)}
   # Narrow fold wedges originate at the elbow's compressed side.
   side_sign=-1 if side=='L' else 1
   def point(i,k):return centres[i]+normals[i]*radii[i]*k*side_sign
   contours['fold']=[point(12,.85),point(16,.18),point(21,.72),point(17,.34)]
   contours['glint']=[point(12,.72),point(16,.03),point(20,.63),point(16,.10)]
   for layer,(ob,z) in objects.items():
    pts=contours[layer];coords=[(p.x,p.y,z) for p in pts]
    if frame==1:
     count=len(coords)//2
     faces=[(i,i+1,len(coords)-2-i,len(coords)-1-i) for i in range(count-1)] if layer in ['outline','cloth','underside','light'] else [(0,1,3),(1,2,3)]
     ob.data.from_pydata(coords,[],faces);key=ob.shape_key_add(name='Pose 001');ob.data.shape_keys.use_relative=False
    else:key=ob.shape_key_add(name=f'Pose {frame:03}')
    for v,co in zip(key.data,coords):v.co=co
    key.interpolation='KEY_LINEAR';keys=ob.data.shape_keys;keys.eval_time=(frame-1)*10;keys.keyframe_insert(data_path='eval_time',frame=frame)
  for ob,z in objects.values():
   for layer in ob.data.shape_keys.animation_data.action.layers:
    for strip_ in layer.strips:
     for bag in strip_.channelbags:
      for fc in bag.fcurves:
       for k in fc.keyframe_points:k.interpolation='LINEAR'
   made.append(ob.name)
 s.frame_set(43)
 return {'continuous_cloth_surfaces':len(made),'motion_keys_changed':False}

def unify_garment():
 # One connected cardigan boundary: no closed chest outline crossing the sleeves.
 # This is a shot-specific flat drawing surface; the existing acting controls remain intact.
 for name in ['cardigan body','cardigan body outline','shoulder seam -1','shoulder seam 1']:
  hide(name)
 for side in ['L','R']:
  for layer in ['outline','cloth']:hide(side+' continuous sleeve '+layer)
 for o in list(col.objects):
  if ' unified cardigan ' in o.name:bpy.data.objects.remove(o,do_unlink=True)
 surfaces=[]
 for label,color,z in [('outline',INK,-.7),('cloth','#232940',-.5)]:
  me=bpy.data.meshes.new('F8 unified cardigan '+label);o=bpy.data.objects.new('F8 / unified cardigan '+label,me);col.objects.link(o);o.parent=C['chest'];me.materials.append(b['mat'](color));surfaces.append((o,z,label))
 for frame in range(1,169):
  sides={}
  for side,sign in [('L',-1),('R',1)]:
   key=bpy.data.objects['F8 / '+side+' continuous sleeve cloth'].data.shape_keys.key_blocks[frame-1]
   points=[v.co.xy.copy() for v in key.data];positive=points[:33];negative=list(reversed(points[33:]));outer,inner=(negative,positive) if side=='L' else (positive,negative)
   for edge,anchor in [(outer,Vector((sign*78,181))),(inner,Vector((sign*82,111)))]:
    target=edge[7].copy()
    for i in range(7):edge[i]=anchor.lerp(target,i/7)
   sides[side]=(outer,inner)
  ro,ri=sides['R'];lo,li=sides['L']
  waist=[Vector(p) for p in [(88,82),(93,49),(87,11),(73,-11),(0,-17),(-76,-10),(-87,12),(-91,54),(-87,82)]];neck=[Vector(p) for p in [(-43,194),(-6,193),(43,194)]]
  core=[ro[0],ri[0]]+waist+[li[0],lo[0]]+neck
  cloth=core[:]
  from mathutils.geometry import tessellate_polygon
  core3=[Vector((p.x,p.y,0)) for p in core]
  faces=[tuple(tri) for tri in tessellate_polygon([core3])]
  for outer,inner,start_pair in [(ro,ri,(0,1)),(lo,li,(12,11))]:
   previous=start_pair
   for j in range(1,33):
    pair=(len(cloth),len(cloth)+1);cloth.extend([outer[j],inner[j]]);faces.append((previous[0],pair[0],pair[1],previous[1]));previous=pair
  path=ro+list(reversed(ri))+waist+li+list(reversed(lo))+neck
  area=sum(a.x*b.y-b.x*a.y for a,b in zip(path,path[1:]+path[:1]));outward=1 if area>0 else -1
  for ob,z,label in surfaces:
   if label=='cloth':coords=[(p.x,p.y,z) for p in cloth];surface_faces=faces
   else:
    coords=[]
    for i,p in enumerate(path):
     d=path[(i+1)%len(path)]-path[(i-1)%len(path)];d.normalize();normal=Vector((d.y,-d.x))*outward
     for distance in [-.8,1.25]:
      q=p+normal*distance;coords.append((q.x,q.y,z))
    surface_faces=[(2*i,2*i+1,(2*i+3)%len(coords),(2*i+2)%len(coords)) for i in range(len(path))]
   if frame==1:ob.data.from_pydata(coords,[],surface_faces);key=ob.shape_key_add(name='Pose 001');ob.data.shape_keys.use_relative=False
   else:key=ob.shape_key_add(name=f'Pose {frame:03}')
   for v,co in zip(key.data,coords):v.co=co
   key.interpolation='KEY_LINEAR';keys=ob.data.shape_keys;keys.eval_time=(frame-1)*10;keys.keyframe_insert(data_path='eval_time',frame=frame)
 for ob,_,_ in surfaces:
  for layer in ob.data.shape_keys.animation_data.action.layers:
   for strip_ in layer.strips:
    for bag in strip_.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='LINEAR'
 s.frame_set(43)
 return {'garment':'one native chest-and-sleeves silhouette','frames':168}

def full_body_view():
 d=bpy.data.scenes.new('S002_v008_Ferguson_full_body');d.collection.children.link(col);d.world=s.world;d.render.engine='BLENDER_EEVEE';d.eevee.taa_render_samples=16;d.render.resolution_x=1280;d.render.resolution_y=960;d.render.resolution_percentage=100;d.render.fps=24;d.frame_end=168;d.view_settings.view_transform='Standard';d.view_settings.look='None'
 camdata=bpy.data.cameras.new('F8 / full body inspection');camdata.type='ORTHO';camdata.ortho_scale=3.5;cam=bpy.data.objects.new(camdata.name,camdata);d.collection.objects.link(cam);cam.location=(0,-8,1.2);cam.rotation_euler=(Vector((0,0,1.2))-cam.location).to_track_quat('-Z','Y').to_euler();d.camera=cam
 d.render.film_transparent=False;world=bpy.data.worlds.new('F8 / inspection neutral');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.14,.17,1);world.node_tree.nodes['Background'].inputs[1].default_value=.7;d.world=world
 d['purpose']='Unobstructed artwork inspection only; not a new story location.';d.frame_set(43)
 return {'inspection_scene':d.name}

def save():
 bpy.context.window.scene=s;s.frame_set(43);bpy.ops.wm.save_as_mainfile(filepath=str(O/'ferguson-art-v008.blend'));return {'file':bpy.data.filepath}
