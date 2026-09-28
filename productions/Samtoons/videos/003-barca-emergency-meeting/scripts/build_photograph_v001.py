"""S11 photograph reveal. Reuses selected cast artwork, authors a new performance.
Visible Blender stages: setup(), cast(), prop(), animate(), finish().
"""
import bpy, importlib.util, json, math, subprocess, array
from pathlib import Path
from mathutils import Matrix, Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/staging-v001/photograph-v001';END=312
spec=importlib.util.spec_from_file_location('s11_cast',V/'scripts/build_consultation_v001.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
M=C.M;B=M.B;n=M.n;key=C.key;visible=C.visible;at=C.at
LINES=[('Robert','robert-picture.wav',13,'LEWANDOWSKI: Show them the other picture.'),('Muller','muller-relevant.wav',95,"MÜLLER: That's not relevant."),('Robert','robert-four.wav',140,'LEWANDOWSKI: The one where Barcelona scored four against you.')]

def setup():
 global S,CAM
 assert not (O/'photograph.blend').exists(),'Preserve delivered versions'
 O.mkdir(parents=True,exist_ok=True);M.setup();S=M.s;CAM=S.camera;S.name='S003_S11_Photograph_v001';S.frame_end=END
 bpy.data.batch_remove([o for o in n['col'].objects if o!=CAM])
 B['rect']('S11 backdrop',-700,-400,1400,800,-160,'#142433',outline=False)
 for x,y,w,h,color in [(-618,45,350,274,'#c6d0c4'),(-618,-260,350,274,'#60798b'),(-240,-260,855,579,'#d0ac7b')]:
  B['rect']('S11 tile border',x-4,y-4,w+8,h+8,-150,'#0b1823',outline=False);B['rect']('S11 room',x,y,w,h,-149,color,outline=False)
 for x in [-210,-14,180,375,582]:B['rect']('S11 oak moulding',x,-255,5,570,-146,'#b38b5b',outline=False)
 B['rect']('S11 club frame',-195,126,132,155,-140,'#71543b');B['rect']('S11 club print',-186,135,114,137,-139,'#efe6cb',outline=False)
 B['text']('S11 Munich','MÜNCHEN',-128,237,-138,15,'#854238')
 B['shape']('S11 club shield',[(-166,214),(-88,214),(-88,158),(-127,145),(-166,158)],-138,'#a6424c',soft=False)
 for x in [-153,-129,-105]:B['shape']('S11 diamond',[(x,205),(x+9,190),(x,174),(x-9,190)],-137,'#efe6cb',outline=False,soft=False)
 B['rect']('S11 shelf',440,-225,175,210,-140,'#865d42')
 for x,h,color in [(456,86,'#d6b6a0'),(481,111,'#6c8689'),(510,102,'#bd7162'),(540,94,'#dad3b8')]:B['rect']('S11 book',x,-127,18,h,-139,color)
 B['oval']('S11 pot',536,23,33,38,-138,'#687e82')
 for dx,dy in [(-44,62),(0,91),(38,65)]:B['shape']('S11 leaf',[(536,43),(536+dx,43+dy),(546+dx,56+dy),(544,47)],-139,'#49695c',outline=False)
 B['rect']('S11 Perez board',-575,-113,259,114,-146,'#eeeada');B['text']('S11 tactics','HOW TO STOP FLICK?',-445,-56,-145,15,'#2e4454')
 for x in [-582,-469,-350]:B['stroke']('S11 Robert panel',[(x,45),(x,319)],-147,'#aabbab',1,soft=False)
 B['text']('S11 call heading','PRIVATE CALL',-492,337,180,19,'#dce8df');B['text']('S11 participants','3 PARTICIPANTS',489,337,180,15,'#b8cec2')
 for x,y,w,label in [(-618,24,350,'ROBERT LEWANDOWSKI'),(-618,-282,350,'FLORENTINO PÉREZ'),(-240,-282,855,'THOMAS MÜLLER')]:
  B['rect']('S11 name bar',x,y,w,25,170,'#203a46',outline=False);B['text']('S11 name',label,x+w/2,y+7,171,13 if w<400 else 16,'#f4eedc')
 for x,y,w in [(-618,44,350),(-618,-258,350)]:B['rect']('S11 desk',x,y,w,14,150,'#997650',outline=False)
 B['rect']('S11 Muller tabletop',-240,-260,855,55,-20,'#ac8860',outline=False)
 B['stroke']('S11 table rear', [(-240,-205),(615,-205)],-19,'#7a5b40',1,soft=False)
 C.RROOT=B['control']('S11 Robert root',(-432,47,0));C.RROOT.scale=(-.199,.199,.199)
 return {'scene':S.name,'frames':END}

def cast():
 original_prop=n['carried_prop']
 def selected_prop(a):
  if a['c']['who']=='Perez':original_prop(a)
 n['carried_prop']=selected_prop
 for who in ['Muller','Perez']:
  M.skeleton(who)
  if who=='Muller':
   beats={'torso':[(1,0),(101,0),(107,-1.2),(119,0),(219,0),(234,2.2),(250,3),(END,3)],'head':[(1,1),(92,1),(98,-3),(110,-1),(129,1),(219,1),(237,7),(252,5),(END,5)],'wrist':[(1,(0,0)),(212,(0,0)),(226,(0,-10)),(248,(4,-32)),(END,(4,-32))],'hand':[(1,0),(212,0),(252,2),(END,2)]}
  else:
   beats={'torso':[(1,-1),(END,-1)],'head':[(1,2),(213,2),(221,-2),(232,-1),(END,-1)],'wrist':[(1,(0,5)),(40,(0,5)),(46,(-3,8)),(51,(0,5)),(100,(0,5)),(106,(-3,8)),(112,(0,5)),(205,(0,5)),(211,(-3,8)),(216,(0,6)),(END,(0,6))],'hand':[(1,0),(END,0)]}
  M.BEATS[who].update(beats)
 for f in range(1,END+1):
  S.frame_set(f)
  for a in M.A.values():M.pose(a,f)
 M.attach_art();C.robert();C.LIFT.value=0;C.CUP.location.y=0
 for who,x,y,scale in [('Muller',205,-195,.48),('Perez',-443,-270,.285)]:
  a=M.A[who];a['root'].location=(x,y,0);a['root'].scale=((-scale if who=='Perez' else scale),scale,scale)
 return {'cast':list(M.A)+['Robert'],'max_joint_error':max(M.errors)}

def prop():
 global TURN,ANCHOR,GRIP,FRONT,BACK
 a=M.A['Muller'];ANCHOR=B['control']('S11 frame hand attachment',parent=a['root'])
 constraint=ANCHOR.constraints.new('COPY_TRANSFORMS');constraint.target=a['rig'];constraint.subtarget='L hand';constraint.target_space='POSE';constraint.owner_space='LOCAL'
 GRIP=n['xy']((110,550),a['c']['origin'])
 seat=B['control']('S11 shared grip pivot',parent=ANCHOR)
 seat.matrix_basis=a['rig'].data.bones['L hand'].matrix_local.inverted()@Matrix.Translation(GRIP+Vector((0,0,2)))
 TURN=B['control']('S11 frame turnover',parent=seat)
 FRONT=B['control']('S11 frame front',parent=TURN);BACK=B['control']('S11 frame back',parent=TURN)
 # ponytail: an edge-held 180-degree turn with a fixed finger grip; new grips need new hand drawings.
 B['rect']('S11 wooden frame',-3,-73,239,291,0,'#67482f',TURN,False)
 B['rect']('S11 front inset',11,-59,211,263,1,'#c39964',FRONT,False)
 B['rect']('S11 front paper',16,-54,201,253,1.3,'#fff5df',FRONT,False)
 for name,words,y,size,col in [('club','BARCELONA',162,24,'#263e59'),('result','4 – 1',87,64,'#19232f'),('opponent','BAYERN',40,25,'#9e3536'),('year','2024',-4,23,'#5c574b')]:B['text']('S11 '+name,words,117,y,1.6,size,col,FRONT)
 # Opaque rear face conceals the result until the turn passes edge-on.
 B['rect']('S11 rear board',9,-60,215,265,1,'#947454',BACK,False)
 B['rect']('S11 back seam',16,152,200,2,1.3,'#604b39',BACK,False)
 B['stroke']('S11 frame wire',[(32,108),(116,177),(202,108)],1.5,'#4c4034',1.3,BACK,False)
 return {'turn_pivot':'same L hand bone as grip','new_prop':True}

def envelope(file):
 raw=subprocess.check_output(['/opt/homebrew/bin/ffmpeg','-v','error','-i',str(V/'assets/voices-s11-v001'/file),'-f','f32le','-ac','1','-ar','24000','pipe:1']);a=array.array('f');a.frombytes(raw)
 e=[math.sqrt(sum(x*x for x in a[i:i+1000])/len(a[i:i+1000])) for i in range(0,len(a),1000)];m=max(e);return [v/m for v in e]

def animate():
 env=[(who,start,envelope(file),text) for who,file,start,text in LINES]
 for f in range(1,END+1):
  S.frame_set(f)
  # All participants remain visible through the pen-stop reaction; then cut to the reveal.
  close=f>=241;CAM.location=(187.5 if close else 0,37 if close else 0,1200);CAM.data.ortho_scale=895 if close else 1280;key(CAM,f);key(CAM.data,f,'ortho_scale')
  angle_prop=math.radians(at(f,[(1,-180),(215,-180),(221,-174),(230,-126),(238,-45),(246,0),(END,0)]))
  # Project the rigid rotation into the drawing plane: moving depth must not cut through flat fingers.
  TURN.scale.x=math.cos(angle_prop);key(TURN,f,'scale');visible(FRONT,TURN.scale.x>=0,f);visible(BACK,TURN.scale.x<0,f)
  angle=at(f,[(1,0),(14,0),(21,-2),(30,-.5),(140,-.5),(153,1.8),(170,.5),(213,.5),(223,2.4),(END,2.4)])
  C.HLEFT.value=max(0,angle/3);C.HRIGHT.value=max(0,-angle/3);key(C.HLEFT,f,'value');key(C.HRIGHT,f,'value');C.R['face'].rotation_euler.z=math.radians(angle);key(C.R['face'],f,'rotation_euler')
  for who,a in list(M.A.items())+[('Robert',C.R)]:
   amp=max([e[f-start] for w,start,e,t in env if w==who and 0<=f-start<len(e)]+[0])
   neutral='tight' if who=='Muller' and f>218 else 'smile' if who=='Robert' and f>224 else 'rest'
   label=('O' if amp>.62 else 'A' if amp>.36 else 'E') if amp>.12 else neutral
   for name,group in a['mouths'].items():visible(group,name==label,f)
   gaze=at(f,[(1,0),(210,0),(220,-7 if who=='Muller' else 3),(END,-7 if who=='Muller' else 3)])
   for i,(ctrl,closed,line,top,bottom) in enumerate(a['eyes']):
    ctrl.location.x=a['c']['eyes'][i]['pupil'][0]-a['c']['eyes'][i]['center'][0]+gaze;key(ctrl,f)
    blink=f in ([87,88,207,208] if who=='Robert' else [125,126,229,230] if who=='Muller' else [80,81,250,251]);closed.value=int(blink);key(closed,f,'value');visible(line,blink,f)
    br=a['brows'][i];br.rotation_euler.z=math.radians(at(f,[(1,0),(218,0),(233,10 if who=='Muller' else 4),(END,10 if who=='Muller' else 4)])*(1 if i==0 else -1));key(br,f,'rotation_euler')
 for who,start,e,words in env:
  root=B['control']('S11 caption',parent=CAM);B['rect']('S11 caption bed',-.49,-.021,.98,.044,0,'#152732',root,False);B['text']('S11 caption words',words,0,-.008,.02,.016,'#f5eedc',root)
  for f in range(1,END+1):
   S.frame_set(f);w=CAM.data.ortho_scale;root.location=(0,-w*.249,-100);root.scale=(w,w,w);key(root,f);key(root,f,'scale')
  visible(root,False,1);visible(root,True,start);visible(root,False,start+len(e))
 for name,f in [('Robert requests picture',13),('Muller deflects',95),('Robert says four',140),('Frame turn begins',216),('Pen stops',216),('Frame faces camera',246),('Read score and reaction',267)]:S.timeline_markers.new(name,frame=f)
 return {'lines':[{'actor':w,'start':s,'duration_frames':len(e)} for w,s,e,t in env],'turn':[216,246]}

def finish():
 assert max(M.errors)<.01
 for action in bpy.data.actions:
  for layer in action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT' if 'hide_' in fc.data_path or action==CAM.animation_data.action else 'LINEAR'
 checks=[]
 for f in range(1,END+1):
  S.frame_set(f);bpy.context.view_layer.update();a=M.A['Muller'];expected=a['root'].matrix_world@a['rig'].pose.bones['L hand'].matrix@a['rig'].data.bones['L hand'].matrix_local.inverted()@(GRIP+Vector((0,0,2)))
  checks.append((TURN.matrix_world.translation-expected).length)
 assert max(checks)<.01,max(checks)
 S.frame_set(270);S['scope']='S11 staged photograph reveal; authored turn and new dialogue. Pending creative review.'
 bpy.ops.wm.save_as_mainfile(filepath=str(O/'photograph.blend'))
 (O/'construction-check.json').write_text(json.dumps({'frames':END,'fps':24,'max_joint_error':max(M.errors),'max_grip_anchor_error':max(checks),'turn_frames':[216,246],'score_hold_frames':66,'voice_listened_by_agent':False,'limitations':['Fixed drawn finger grip during rigid prop turnover; requires visual review','Small seated motion range; not an extreme-motion guarantee']},indent=2)+'\n')
 return {'native':str(O/'photograph.blend'),'max_grip_error':max(checks)}
