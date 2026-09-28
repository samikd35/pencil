"""S13: established callers, small seated acting and a contact-driven transfer.
Visible Blender stages: setup(), cast(), console(), animate(), finish().
"""
import bpy,math,json,importlib.util,subprocess,array
from pathlib import Path
from mathutils import Vector,Matrix
V=Path(__file__).resolve().parents[1];O=V/'artifacts/staging-v001/transfer-v001';END=288
sp=importlib.util.spec_from_file_location('s13_primitives',V/'scripts/build_consultation_v001.py');C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
M=C.M;B=M.B;n=M.n;key=C.key;visible=C.visible;at=C.at
LINES=[('Perez','perez-expert.wav',9,'PÉREZ: Enough old results. I need someone who can stop this!'),('Muller','muller-transfer.wav',123,"MÜLLER: I'll connect you to our goal-scoring expert."),('Operator','connecting.wav',222,'Connecting your call.')]

def use(col):
 n['col']=col;n['b']['skin']=col;B['b']['skin']=col

def setup():
 global S,CAM,MAIN,REMOTE,OFF,STATUS,STATUS_OFF
 assert not bpy.app.background and not (O/'transfer.blend').exists(),'Preserve delivered versions'
 O.mkdir(parents=True,exist_ok=True);M.setup();S=M.s;S.name='S003_S13_Transfer_v001';S.frame_end=END;CAM=S.camera;MAIN=n['col']
 bpy.data.batch_remove([o for o in MAIN.objects if o!=CAM])
 REMOTE=bpy.data.collections.new('S13 Muller room');S.collection.children.link(REMOTE)
 use(MAIN)
 B['rect']('S13 Madrid wall',-720,-430,1440,860,-160,'#6d8296',outline=False)
 B['shape']('S13 cool light',[(155,420),(505,420),(370,-260),(-30,-260)],-158,'#7e95a6',outline=False,soft=False)
 for x in [-610,-420,-230,-40,150,340,530]:B['stroke']('S13 wall seam',[(x,-390),(x,390)],-157,'#586e81',1,soft=False)
 B['rect']('S13 tactics frame',207,45,435,292,-145,'#25384b');B['rect']('S13 tactics board',219,57,411,268,-144,'#eeeada',outline=False)
 B['text']('S13 board title','HOW TO STOP FLICK?',431,283,-143,23,'#263e50')
 for x,y in [(257,185),(590,137),(552,226)]:B['text']('S13 board mark','×',x,y,-143,29,'#667e8b')
 B['rect']('S13 monitor border',-621,-285,600,616,-100,'#243748');B['rect']('S13 monitor glass',-607,-269,572,581,-99,'#172b3c',outline=False)
 B['oval']('S13 webcam',-319,335,24,8,-80,'#1b2c3c');B['oval']('S13 webcam lamp',-308,335,2,2,-79,'#7da997')
 B['shape']('S13 desk',[(-720,-410),(720,-410),(705,-252),(-708,-252)],140,'#ab845c',soft=False)
 B['stroke']('S13 desk grain',[(-595,-338),(174,-275),(643,-317)],141,'#8e694a',1,soft=False)
 B['shape']('S13 notepad',[(103,-332),(355,-332),(394,-271),(145,-271)],143,'#f5ecd5',soft=False)
 for y in [-288,-299,-310]:B['stroke']('S13 note line',[(159,y),(323,y)],144,'#788083',1,soft=False)
 B['rect']('S13 name bar',-607,-270,572,26,170,'#1f3546',outline=False);B['text']('S13 name','THOMAS MÜLLER · BAYERN LEGEND',-321,-259,171,13,'#e0e8df')
 OFF=B['control']('S13 disconnected video');B['rect']('S13 dark screen',-607,-243,572,554,160,'#203747',OFF,False)
 B['text']('S13 connecting title','CONNECTING…',-321,80,161,30,'#eae4d1',OFF);B['text']('S13 connecting route','GOAL-SCORING EXPERT',-321,28,161,18,'#9cb7bc',OFF)
 visible(OFF,False,1);visible(OFF,True,204)
 use(REMOTE)
 B['rect']('S13 Munich wall',-390,-310,780,660,-160,'#d0ac7b',outline=False)
 for x in [-340,-170,0,170,340]:B['rect']('S13 oak moulding',x,-295,4,620,-158,'#b58e62',outline=False)
 B['rect']('S13 Munich print frame',-339,122,127,166,-149,'#735039');B['rect']('S13 Munich print',-329,132,107,146,-148,'#f2e8ce',outline=False)
 B['text']('S13 Munich','MÜNCHEN',-275,249,-147,14,'#9a3d44')
 B['shape']('S13 club shield',[(-311,223),(-239,223),(-239,161),(-275,145),(-311,161)],-147,'#a5434c',soft=False)
 for x in [-300,-276,-252]:B['shape']('S13 diamond',[(x,212),(x+9,198),(x,180),(x-9,198)],-146,'#f1e3c9',outline=False,soft=False)
 B['rect']('S13 Munich shelf',237,-202,145,217,-150,'#896246')
 for x,h,color in [(249,93,'#647e88'),(278,116,'#c58a6d'),(309,88,'#d7c9a6')]:B['rect']('S13 book',x,-185,17,h,-149,color)
 B['oval']('S13 plant pot',299,52,28,37,-147,'#617d80')
 for dx,dy in [(-37,70),(5,87),(32,67)]:B['shape']('S13 leaf',[(299,69),(299+dx,69+dy),(311+dx,74+dy),(307,72)],-148,'#477359',outline=False)
 B['rect']('S13 Munich desk surface',-390,-283,780,45,-20,'#b18b64',outline=False)
 B['rect']('S13 Munich desk edge',-390,-311,780,35,150,'#8c6648',outline=False)
 STATUS=B['text']('S13 live indicator','CAMERA ON',248,-262,151,14,'#dae4d2')
 STATUS_OFF=B['text']('S13 private indicator','CAMERA OFF',248,-262,151,14,'#cdd7cc')
 visible(STATUS,True,1);visible(STATUS,False,204);visible(STATUS_OFF,False,1);visible(STATUS_OFF,True,204)
 return {'scene':S.name,'frames':END}

def cast():
 global FRAME,TIP
 original=n['carried_prop']
 def selected(a):
  if a['c']['who']=='Perez':original(a)
 n['carried_prop']=selected
 for who in ['Muller','Perez']:
  use(REMOTE if who=='Muller' else MAIN);M.skeleton(who)
  if who=='Muller':
   beats={'torso':[(1,0),(123,0),(136,-.6),(170,-.6),(190,0),(198,-1),(203,-1),(209,0),(215,0),(228,1.1),(244,.5),(END,.5)],'head':[(1,4),(113,4),(123,-2),(133,1),(173,1),(185,3),(198,5),(209,5),(215,5),(229,-3),(244,0),(END,0)],'wrist':[(1,(4,-32)),(END,(4,-32))],'hand':[(1,2),(END,2)]}
  else:
   beats={'torso':[(1,-1),(9,-1),(19,-3),(53,-3),(68,-3.6),(101,-3.6),(115,-1.5),(END,-1.5)],'head':[(1,1),(9,1),(18,-4),(49,-3),(66,-5),(103,-4),(119,1),(END,1)],'wrist':[(1,(0,6)),(54,(0,6)),(66,(-8,10)),(102,(-8,10)),(118,(0,6)),(END,(0,6))],'hand':[(1,0),(END,0)]}
  M.BEATS[who].update(beats)
 for f in range(1,END+1):
  S.frame_set(f)
  for a in M.A.values():M.pose(a,f)
 # The helper creates both characters; their complete hierarchies are moved to the owning room afterward.
 use(MAIN);M.attach_art()
 for who,x,y,scale in [('Muller',0,-218,.57),('Perez',342,-214,.57)]:
  a=M.A[who];a['root'].location=(x,y,0);a['root'].scale=(scale,)*3
  dest=REMOTE if who=='Muller' else MAIN
  for ob in [a['root'],*a['root'].children_recursive]:
   for col in list(ob.users_collection):col.objects.unlink(ob)
   dest.objects.link(ob)
 use(REMOTE)
 # Retain the established 4–1 memento from S11 with its original fixed grip attachment.
 sp=importlib.util.spec_from_file_location('s13_frame',V/'scripts/build_photograph_v001.py');F=importlib.util.module_from_spec(sp);sp.loader.exec_module(F)
 F.M=M;F.B=B;F.n=n;F.S=S;F.prop();FRAME=F.TURN;visible(F.FRONT,True,1);visible(F.BACK,False,1)
 # Contact is an existing fingertip on the complete resting right hand, not a new disjoint hand.
 a=M.A['Muller'];TIP=n['xy']((534,1001),a['c']['origin'])
 return {'cast':list(M.A),'joint_error_source_pixels':max(M.errors)}

def fingertip(f):
 S.frame_set(f);bpy.context.view_layer.update();a=M.A['Muller'];bone=a['rig'].pose.bones['torso']
 return a['root'].matrix_world@bone.matrix@bone.bone.matrix_local.inverted()@TIP

def console():
 global BUTTON,TOUCH,FEED,LOCAL,CHECK
 CHECK=[];use(REMOTE)
 for f in range(1,END+1):
  S.frame_set(f);a=M.A['Muller'];a['root'].location.y=-218-at(f,[(1,0),(192,0),(200,4),(203,4),(212,0),(END,0)]);key(a['root'],f)
 TOUCH=fingertip(200)
 B['shape']('S13 transfer console',[(TOUCH.x-83,-274),(TOUCH.x+81,-274),(TOUCH.x+72,-229),(TOUCH.x-67,-229)],-5,'#35474c',soft=False)
 B['rect']('S13 console lower lip',TOUCH.x-83,-280,164,10,-4,'#223137',outline=False)
 BUTTON=B['control']('S13 transfer key',(TOUCH.x,TOUCH.y,0))
 B['shape']('S13 transfer key top',[(-40,0),(40,0),(46,-15),(-44,-15)],.4,'#6f9691',BUTTON,True,False)
 B['text']('S13 transfer label','TRANSFER',TOUCH.x,-261,5,14,'#eceddd')
 # Two instances of the same animated room: actual office and transmitted image.
 use(MAIN)
 LOCAL=bpy.data.objects.new('S13 actual Munich room',None);LOCAL.instance_type='COLLECTION';LOCAL.instance_collection=REMOTE;LOCAL.location=(-1600,0,0);MAIN.objects.link(LOCAL)
 FEED=bpy.data.objects.new('S13 transmitted Munich picture',None);FEED.instance_type='COLLECTION';FEED.instance_collection=REMOTE;FEED.location=(-321,15,0);FEED.scale=(.735,)*3;MAIN.objects.link(FEED)
 S.collection.children.unlink(REMOTE)
 visible(FEED,True,1);visible(FEED,False,204)
 return {'contact_frame':200,'source_fingertip':[534,1001],'button':list(TOUCH),'transmitted_picture_off':204,'private_exhale_starts':216}

def envelope(file):
 raw=subprocess.check_output(['/opt/homebrew/bin/ffmpeg','-v','error','-i',str(V/'assets/voices-s13-v001'/file),'-f','f32le','-ac','1','-ar','24000','pipe:1']);p=array.array('f');p.frombytes(raw)
 e=[math.sqrt(sum(x*x for x in p[i:i+1000])/len(p[i:i+1000])) for i in range(0,len(p),1000)];return [x/max(e) for x in e]

def animate():
 env=[(w,start,envelope(file),words) for w,file,start,words in LINES]
 use(MAIN)
 for f in range(1,END+1):
  S.frame_set(f)
  if f<9:x,y,width=0,0,1280
  elif f<119:x,y,width=at(f,[(9,200),(25,252),(END,252)]),20,at(f,[(9,1050),(25,900),(END,900)])
  elif f<216:x,y,width=-321,15,650
  elif f<252:x,y,width=-1600,0,750
  else:x,y,width=0,0,1280
  CAM.location=(x,y,1200);CAM.data.ortho_scale=width;key(CAM,f);key(CAM.data,f,'ortho_scale')
  # The key yields after fingertip contact; it never jumps to meet a distant hand.
  press=at(f,[(1,0),(195,0),(200,1),(203,1),(212,0),(END,0)])
  BUTTON.location.y=TOUCH.y+2*(1-press);key(BUTTON,f)
  for who,a in M.A.items():
   amp=max([e[f-start] for w,start,e,t in env if w==who and 0<=f-start<len(e)]+[0])
   label=('O' if amp>.63 else 'A' if amp>.36 else 'E') if amp>.12 else ('tight' if who=='Perez' else 'smile' if 119<=f<196 else 'rest')
   if who=='Muller' and 222<=f<=232:label='O'
   for name,group in a['mouths'].items():visible(group,name==label,f)
   for i,(gaze,closed,line,top,bottom) in enumerate(a['eyes']):
    look=at(f,[(1,0),(180,0),(193,-6 if who=='Muller' else 0),(212,-6 if who=='Muller' else 0),(237,0),(END,0)])
    gaze.location.x=a['c']['eyes'][i]['pupil'][0]-a['c']['eyes'][i]['center'][0]+look;key(gaze,f)
    blink=f in ([112,113,215,216] if who=='Perez' else [104,105]) or (who=='Muller' and 220<=f<=235)
    closed.value=int(blink);key(closed,f,'value');visible(line,blink,f)
    brow=at(f,[(1,3),(13,3),(22,-7),(106,-7),(119,-3),(END,-3)]) if who=='Perez' else at(f,[(1,7),(119,7),(133,-2),(193,-2),(216,0),(228,7),(END,7)])
    a['brows'][i].rotation_euler.z=math.radians(brow*(1 if i==0 else -1));key(a['brows'][i],f,'rotation_euler')
 for who,start,e,words in env:
  root=B['control']('S13 caption',parent=CAM);B['rect']('S13 caption bed',-.485,-.021,.97,.044,0,'#182e3d',root,False);B['text']('S13 caption text',words,0,-.006,.02,.018,'#f5edda',root)
  for f in range(1,END+1):
   S.frame_set(f);w=CAM.data.ortho_scale;root.location=(0,-w*.249,-100);root.scale=(w,)*3;key(root,f);key(root,f,'scale')
  visible(root,False,1);visible(root,True,start);visible(root,False,start+len(e))
 for label,f in [('Perez demand',9),('Muller offers expert',123),('Transfer press',200),('Outgoing picture disappears',204),('Private relief',216),('Recorded connecting voice',222),('Hold phrase',250),('Factory phone ring bridge',275)]:S.timeline_markers.new(label,frame=f)
 return {'lines':[{'actor':w,'start':s,'frames':len(e)} for w,s,e,t in env]}

def finish():
 objects=set(S.objects)|set(REMOTE.objects)
 for ob in objects:
  if ob.type=='CURVE' and ob.data.dimensions=='3D' and ob.data.bevel_depth and not ob.get('planar_ink'):
   pts=[p for sp in ob.data.splines for p in sp.points]
   if pts:
    z=pts[0].co.z;assert all(abs(p.co.z-z)<.001 for p in pts)
    for p in pts:p.co.z=0
    ob.location.z+=z;ob.scale.z=.01;ob['planar_ink']=True
 # Only this shot's used actions; leave delivered scenes untouched.
 acts={ob.animation_data.action for ob in objects if ob.animation_data and ob.animation_data.action}
 acts.add(CAM.data.animation_data.action)
 for ob in objects:
  if ob.type=='MESH' and ob.data.shape_keys and ob.data.shape_keys.animation_data:acts.add(ob.data.shape_keys.animation_data.action)
 for act in acts:
  for layer in act.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT' if 'hide_' in fc.data_path or act in [CAM.animation_data.action,CAM.data.animation_data.action] else 'LINEAR'
 mix=O/'audio/mix-premaster.wav'
 if mix.exists():
  ed=S.sequence_editor_create()
  if not ed.strips:ed.strips.new_sound('S13 authoritative premaster',str(mix),channel=1,frame_start=1)
 S.render.use_sequencer=False;S.frame_set(140);S['scope']='S13 technical-support staging candidate; existing likeness, small seated motion and timed transfer. Not final film.'
 bpy.data.libraries.write(str(O/'transfer.blend'),{S},fake_user=True,compress=True)
 (O/'construction-check.json').write_text(json.dumps({'frames':END,'max_skeleton_joint_error_source_pixels':max(M.errors),'press_frame':200,'picture_disappears_frame':204,'private_relief_start':216,'native_room_instances_share_same_actor':True,'audio_listened_by_agent':False,'limits':'Supported small gesture only; source grips retained. Contact and expression require visual review.'},indent=2)+'\n')
 return {'native':str(O/'transfer.blend')}
