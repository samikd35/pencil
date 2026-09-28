"""Repair appearance and acting on the connected v011 construction, visibly.
No image heads, automatic skin binding, proportion changes, or audio speed changes.
"""
import bpy, math, json
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/batch01-v013';O.mkdir(exist_ok=True)
n=bpy.app.driver_namespace['samtoons_batch01'];b=n['b'];INK='#20232d'

def curves(ob):
 return [fc for l in ob.animation_data.action.layers for st in l.strips for bag in st.channelbags for fc in bag.fcurves] if ob.animation_data and ob.animation_data.action else []

def face(name):
 a=n['ACTORS'][name];s=a['scene'];n['use'](s,a['col']);C=a['C'];h=C['head'];p=a['prefix']+'v013 ';art=a['kind']=='arteta';skin='#efb082' if art else '#ffc38b';shade='#cc9068' if art else '#dfa875';hair='#171d23' if art else '#996e3f';a['skin']=skin
 # One line/shadow vocabulary shared with the body. Existing head transform survives.
 for ob in list(h.children_recursive):
  if ob.type in ['MESH','CURVE','FONT']:bpy.data.objects.remove(ob,do_unlink=True)
 def sh(label,pts,col,z=5,par=h,edge=True):return n['poly'](p+label,pts,col,z,par,edge,1.1,True)
 def ln(label,pts,col=INK,z=10,w=.85,par=h):return n['line'](p+label,pts,col,z,w,par,True)
 facepts=[(-40,116),(-25,140),(8,146),(34,139),(43,122),(44,101),(48,81),(49,68),(54,59),(49,48),(49,32),(38,18),(18,10),(-5,13),(-26,25),(-38,46),(-43,80)] if art else [(-43,124),(-25,144),(10,149),(37,139),(43,120),(43,101),(48,80),(53,68),(50,59),(51,43),(45,25),(27,10),(2,8),(-23,22),(-38,44),(-45,80)]
 sh('face',facepts,skin,4)
 sh('temple and jaw shade',[(-40,107),(-30,91),(-31,60),(-21,35),(-1,21),(23,17),(42,30),(35,17),(16,10),(-6,13),(-28,27),(-40,49)],shade,5,edge=False)
 sh('ear',[(-37,86),(-49,97),(-59,91),(-60,78),(-50,61),(-37,56),(-31,67)],skin,6)
 ln('ear fold',[(-40,76),(-47,87),(-53,85),(-51,76),(-44,69)],'#a67153',7,.8)
 # Stubble is a shallow jaw plane, not a second muzzle pasted around the mouth.
 beard='#886d57' if art else '#b38d5f'
 sh('jaw stubble',[(-31,61),(-25,46),(-9,32),(8,29),(28,32),(45,44),(48,32),(37,19),(18,12),(-5,15),(-24,29),(-33,46)],beard,6,edge=False)
 for i in range(12):
  x=-23+i*5;y=27+abs(x-9)*.24;ln('stubble '+str(i),[(x,y),(x+.4,y+1.5)],'#795e47',6.2,.25)
 if art:
  sh('hair silhouette',[(-40,70),(-49,81),(-53,104),(-51,129),(-45,146),(-39,159),(-31,158),(-18,166),(-7,163),(5,168),(20,165),(34,160),(45,157),(51,147),(47,137),(37,131),(16,137),(-3,137),(-21,129),(-29,111),(-31,92),(-34,76)],hair,8)
  for i,pts in enumerate([[(-44,135),(-34,151),(-10,157),(18,155)],[(-35,129),(-23,143),(0,150),(28,149)],[(-24,126),(-6,139),(16,143),(39,141)],[(-47,110),(-44,128),(-37,139)]]):ln('hair sweep '+str(i),pts,'#343c43',9,.8)
 else:
  sh('undercut',[(-45,83),(-48,117),(-29,132),(-20,120),(-24,91),(-35,79)],'#967447',8,False)
  sh('swept quiff',[(-43,84),(-54,102),(-55,121),(-45,141),(-30,158),(-10,168),(13,171),(36,168),(48,157),(48,142),(40,135),(24,140),(8,142),(-12,132),(-29,120),(-34,102)],'#654b31',9)
  for i,(pts,col) in enumerate([([(-51,121),(-39,145),(-12,159),(16,159),(35,148),(14,151),(-12,146),(-33,130)],'#b58b51'),([(-37,146),(-13,163),(16,168),(36,161),(43,147),(31,153),(14,159),(-11,156)],'#c49a5e'),([(-48,112),(-30,129),(-5,142),(17,143),(-4,135),(-26,122),(-41,103)],'#ac834d')]):sh('hair lock '+str(i),pts,col,10,edge=False)
  for i,pts in enumerate([[(-45,129),(-21,150),(5,157),(25,153)],[(-30,151),(-6,163),(17,165),(37,153)],[(-46,117),(-22,135),(-3,141)],[(-43,101),(-30,116),(-18,121)]]):ln('hair sweep '+str(i),pts,'#d4ae72',11,.8)
 ln('nose bridge',[(21,109),(20,87),(28,70),(26,66),(17,64),(10,67)],'#795940',15,.9)
 ln('nostril',[(13,68),(18,67),(21,69)],'#795940',15,.8)
 ln('nose highlight',[(23,84),(27,73)],'#ffd5a3',15,.6)
 ln('cheek crease',[(4,58),(0,53),(-1,46)],'#bf865f',14,.5)
 # Eyes retain gaze controls; skin lids cover the iris rather than shrinking the whole eye.
 eyes=[]
 for side,center,wide in [('L',(-9,98),12),('R',(33,101),9)]:
  e=C[side+' eye'];e.animation_data_clear();e.scale=(1,1,1);e.location=(*center,12)
  outline=[(-wide,0),(-wide*.6,5.5),(wide*.2,6),(wide,2),(wide*.7,-4),(0,-5),(-wide*.7,-3)]
  n['poly'](p+side+' eye white',outline,'#fff6e5',0,e,True,.8,True)
  g=C[side+' gaze'];g.animation_data_clear();g.location=(2,0,1);g.scale=(1,1,1)
  n['ellipse'](p+side+' iris',0,0,3.4,4.4,'#645843',0,g)
  n['ellipse'](p+side+' pupil',.3,0,1.9,3.3,INK,.2,g)
  n['ellipse'](p+side+' glint',-.6,1.3,.65,.85,'#fff9e9',.3,g)
  # Four-point eyelid front edge; closed edge follows the lower lid.
  lidpts=[(-wide-2,10),(wide+2,10),(wide+2,1.5),(wide,2),(wide*.2,6),(-wide*.6,5.5),(-wide,0),(-wide-2,0)]
  lid=n['poly'](p+side+' upper lid',lidpts,skin,4,e,False)
  lid.shape_key_add(name='Open');closed=lid.shape_key_add(name='Closed')
  for i,y in [(2,-4),(3,-4),(4,-5),(5,-4),(6,-3),(7,-3)]:closed.data[i].co.y=y
  brow=C[side+' brow'];brow.animation_data_clear();brow.location=(center[0],center[1]+14,16);brow.rotation_euler.z=0
  n['poly'](p+side+' brow',[(-wide-3,0),(-wide*.5,5),(wide,3),(wide+2,-1),(wide*.2,0),(-wide*.6,1)],hair,0,brow,False,1,True)
  eyes.append((closed,g,brow))
 # Small integrated lip shapes, without opaque cover patches or a fixed smile behind speech.
 C['mouth'].location=(23,48 if art else 47,18);C['mouth'].scale=(1,1,1)
 for label,g in a['n']['FAC']['mouth shapes'].items():
  g.scale=(1,1,1);g.location=(0,0,0)
  if label in ['rest','MBP']:
   ln(label+' lip',[(-11,-.5),(-4,0),(4,-.8),(11,.3)],'#704b36',0,.7,g)
   if label=='rest':ln('lower lip',[(-5,-4),(2,-4.5),(7,-3.5)],'#ba7d57',.1,.45,g)
  else:
   w={'A':11,'E':12,'O':6,'U':5,'FV':10,'L':10}[label];hh={'A':9,'E':5,'O':8,'U':5,'FV':3,'L':6}[label]
   sh(label+' mouth',[(-w,0),(-w*.6,2),(0,2.5),(w*.7,1),(w,0),(w*.7,-hh*.7),(0,-hh),(-w*.7,-hh*.75)],'#412923',0,g)
   if label not in ['O','U']:sh(label+' teeth',[(-w*.75,.8),(0,1.5),(w*.75,.3),(w*.65,-1.5),(0,-2),(-w*.6,-1.5)],'#fff4e0',.2,g,False)
   if label in ['A','L']:sh(label+' tongue',[(-w*.45,-hh*.77),(0,-hh*.65),(w*.45,-hh*.78),(0,-hh*.93)],'#b96d64',.3,g,False)
 # Neck is redrawn from the actual jaw to the unchanged collar on every posed frame.
 old=bpy.data.objects.get(a['prefix']+'v011 connected neck')
 if old:old.hide_render=old.hide_viewport=True
 for f in range(1,s.frame_end+1):
  s.frame_set(f);bpy.context.view_layer.update();inv=C['chest'].matrix_world.inverted();ends=[inv@(h.matrix_world@Vector(v)) for v in [(-25,43,0),(25,19,0)]];ends.sort(key=lambda v:v.x)
  pts=[Vector((-27,184,0)),Vector((27,184,0)),ends[1],ends[0]]
  if f==1:
   neck=n['poly'](p+'connected neck',[(v.x,v.y) for v in pts],skin,8.5,C['chest'],False);neck.data.shape_keys if neck.data.shape_keys else None
  k=neck.shape_key_add(name=f'Pose {f:03}');neck.data.shape_keys.use_relative=False
  for dst,pt in zip(k.data,pts):dst.co=(pt.x,pt.y,8.5)
  k.interpolation='KEY_LINEAR';ks=neck.data.shape_keys;ks.eval_time=(f-1)*10;ks.keyframe_insert(data_path='eval_time',frame=f)
 a['face13']={'eyes':eyes,'neck':neck};s.frame_set(315 if s.frame_end==432 else 226)
 return {'actor':name,'face':'native filled geometry; same line and palette as body','body_controls_changed':False}

def show_frame(group,frame,path):
 s=n['SCENES'][group];n['use'](s);s.frame_set(frame)
 s.camera=max((m for m in s.timeline_markers if m.frame<=frame and m.camera),key=lambda m:m.frame).camera
 n['room']['show'](s);s.render.filepath=str(O/path);s.render.resolution_percentage=100;s.render.use_sequencer=False;bpy.ops.render.render(write_still=True)
 return str(O/path)
