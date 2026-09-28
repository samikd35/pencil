"""S09: seated consultation. Authored supported poses, native contours, existing cast.
Run setup(), callers(), robert(), animate(), finish() in visible Blender.
"""
import bpy,importlib.util,json,math,subprocess,array
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/staging-v001/consultation-v001';END=384
spec=importlib.util.spec_from_file_location('s09_call_art',V/'scripts/build_call_performance_v006.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
B=M.B;n=M.n
EVENTS={'add':12,'muller':25,'join':67,'perez':121,'cup_contact':222,'robert':241,'memory_look':357}

def at(f,rows):
 if f<=rows[0][0]:return rows[0][1]
 for (a,x),(b,y) in zip(rows,rows[1:]):
  if f<=b:return x+(y-x)*(f-a)/(b-a)
 return rows[-1][1]
def key(o,f,prop='location'):o.keyframe_insert(data_path=prop,frame=f)
def visible(o,on,f):
 for q in [o]+list(o.children_recursive):
  q.hide_render=q.hide_viewport=not on;key(q,f,'hide_render');key(q,f,'hide_viewport')
def setup():
 global S,CAM,RROOT
 assert not (O/'consultation.blend').exists(),'Version delivered work before rebuilding'
 M.setup();S=M.s;S.name='S003_S09_Consultation_v001';S.frame_end=END;CAM=S.camera
 # Keep primitive/art helpers, replace the former shot's environment and camera composition.
 for o in list(n['col'].objects):
  if o!=CAM:bpy.data.objects.remove(o,do_unlink=True)
 B['rect']('S09 background',-700,-400,1400,800,-150,'#142433',outline=False)
 # Separate remote rooms. Small caller tiles retain their selected identities.
 for x,y,w,h,col in [(-618,45,350,274,'#d0ac7b'),(-618,-260,350,274,'#60798b'),(-240,-260,855,579,'#c6d0c4')]:
  B['rect']('S09 tile frame',x-4,y-4,w+8,h+8,-120,'#0b1823',outline=False);B['rect']('S09 room',x,y,w,h,-119,col,outline=False)
 for y in [64,169,274]:B['stroke']('S09 warm panels',[(-618,y),(-268,y)],-118,'#b18d61',1,soft=False)
 B['rect']('S09 perez whiteboard',-570,-100,246,85,-117,'#e9e5d2');B['text']('S09 tactics','HOW TO STOP FLICK?',-446,-60,-116,15,'#334b5e')
 for x in [-208,25,258,491]:B['stroke']('S09 wall panels',[(x,-210),(x,319)],-118,'#aebfad',1,soft=False)
 B['shape']('S09 window light',[(350,319),(615,319),(615,-213),(455,-213)],-117,'#d8dfce',outline=False,soft=False)
 B['rect']('S09 old photo frame',-194,97,154,178,-110,'#79563f');B['rect']('S09 old photo paper',-183,108,132,154,-109,'#ece2c5',outline=False)
 # Illustrative memento, not a photograph or match-footage claim.
 B['shape']('S09 old Bayern shirt',[(-152,215),(-168,202),(-157,181),(-144,188),(-144,140),(-89,140),(-89,188),(-77,181),(-64,202),(-80,215)],-108,'#bd3441',soft=False)
 B['text']('S09 old number','9',-116,161,-107,38,'#f5ead4');B['text']('S09 old photo caption','BAYERN · 2020',-117,121,-107,12,'#4d4439')
 B['rect']('S09 shelf',458,35,157,13,-111,'#8c7057');B['oval']('S09 pot',539,83,32,42,-110,'#687c73')
 for dx,dy in [(-40,70),(0,97),(34,60)]:B['shape']('S09 leaf',[(539,103),(539+dx,103+dy),(539+dx*.5,115+dy),(545,108)],-111,'#55735c',outline=False)
 B['text']('S09 call heading','PRIVATE CALL',-492,337,180,19,'#dce8df');B['text']('S09 caller count','3 PARTICIPANTS',489,337,180,15,'#b8cec2')
 for x,y,w,label in [(-618,24,350,'THOMAS MÜLLER'),(-618,-282,350,'FLORENTINO PÉREZ'),(-240,-282,855,'ROBERT LEWANDOWSKI · FORMER BAYERN / BARÇA')]:
  B['rect']('S09 name bar',x,y,w,25,160,'#203a46',outline=False);B['text']('S09 name',label,x+w/2,y+7,161,13 if w<400 else 16,'#f4eedc')
 # Cup and relaxed opposite hand sit on this same table surface.
 B['shape']('S09 desk top',[(-240,-247),(615,-247),(615,-213),(-240,-213)],-20,'#b89873',soft=False)
 B['rect']('S09 desk front',-240,-260,855,14,170,'#886c54',outline=False)
 RROOT=B['control']('S09 Robert root',(205,-225,0));RROOT.scale=(-.385,.385,.385)
 connecting=B['control']('S09 connecting');B['rect']('S09 connecting cover',-240,-260,855,579,220,'#263e4b',connecting,False)
 B['text']('S09 connecting title','ADDING ROBERT…',187,39,221,29,'#f0e7d2',connecting)
 B['text']('S09 connecting sub','MÜLLER INVITED A PARTICIPANT',187,-7,221,15,'#b3c5c1',connecting)
 visible(connecting,True,1);visible(connecting,False,67)
 return {'scene':S.name,'frames':END}

def callers():
 # The same artwork and connected construction, with new small seated performances.
 for who in ['Muller','Perez']:
  base={'torso':[(1,2 if who=='Muller' else -1),(END,2 if who=='Muller' else -1)],'head':[(1,3),(25,1),(36,-2),(46,1),(102,1),(113,3),(185,0),(245,0),(256,4),(278,3),(END,3)],'wrist':[(1,(36,-123) if who=='Muller' else (0,10)),(END,(36,-123) if who=='Muller' else (0,10))],'hand':[(1,10 if who=='Muller' else 0),(END,10 if who=='Muller' else 0)]}
  M.BEATS[who].update(base);M.skeleton(who)
 for f in range(1,END+1):
  for a in M.A.values():M.pose(a,f)
 M.attach_art()
 for who,x,y,scale in [('Muller',-442,42,.274),('Perez',-443,-270,.285)]:
  a=M.A[who];a['root'].location=(x,y,0);a['root'].scale=((-scale if who=='Perez' else scale),scale,scale)
 # Foreground desk surfaces sit under the resting hands, rather than cut the wrists.
 B['rect']('S09 Muller desk',-618,44,350,14,150,'#997650',outline=False)
 B['rect']('S09 Perez desk',-618,-258,350,12,150,'#a38463',outline=False)
 return {'cast':list(M.A),'max_joint_error':max(M.errors)}

def robert():
 global R,RBODY,CUP,LIFT,HLEFT,HRIGHT
 data=json.loads((V/'assets/lewandowski-v001/robert.json').read_text());c=data['design']
 RBODY=n['vectors']('S09 Robert body',data['parts']['body'],RROOT,c['origin'],1)
 CUP=n['vectors']('S09 Robert cup',data['parts']['cup'],RROOT,c['origin'],8)
 RBODY.shape_key_add(name='Supported seated pose');LIFT=RBODY.shape_key_add(name='Cup lifted 30 pixels');HLEFT=RBODY.shape_key_add(name='Head left');HRIGHT=RBODY.shape_key_add(name='Head right')
 pivot=n['xy'](c['neck'],c['origin'])
 for i,v in enumerate(RBODY.data.vertices):
  sx=v.co.x+570;sy=1220-v.co.y
  # Small, continuous forearm lift from an already valid supported drawing.
  # ponytail: this drawing supports this 30px set-down only; larger reaches need new poses.
  w=max(0,min(1,(sy-850)/180))*max(0,min(1,(650-sx)/180))
  LIFT.data[i].co.y+=30*w
  h=max(0,min(1,(680-sy)/110))
  for target,angle in [(HLEFT,3),(HRIGHT,-3)]:
   target.data[i].co=v.co+(n['rot'](v.co-pivot,angle)-(v.co-pivot))*h
 CUP['contact_bottom_source_y']=1210
 # Neutral sweater beneath the small cup movement; no holes are revealed by lifting it.
 B['shape']('S09 shirt behind cup',[(x-570,1220-y) for x,y in [(400,1020),(585,1020),(585,1190),(400,1190)]],.8,'#30313a',RROOT,False,False)
 R={'c':c,'root':RROOT,'rest':{'neck':pivot},'data':data};n['facial'](R)
 mouth_back=bpy.data.objects.get(M.PREFIX+'Robert mouth skin backing');center=n['xy'](c['mouth_center'],c['neck'])
 for v in mouth_back.data.vertices:v.co=center+(v.co-center)*1.12;v.co.z=2
 mouth_back.data.materials.clear();mouth_back.data.materials.append(n['b']['mat']('#fbb974'))
 return {'native_vertices':len(RBODY.data.vertices),'cup_contact_table_y':RROOT.location.y+(1220-1210)*.415}

def envelope(name):
 raw=subprocess.check_output(['/opt/homebrew/bin/ffmpeg','-v','error','-i',str(V/'assets/voices-s09-v001'/name),'-f','f32le','-ac','1','-ar','24000','pipe:1']);a=array.array('f');a.frombytes(raw)
 e=[math.sqrt(sum(x*x for x in a[i:i+1000])/len(a[i:i+1000])) for i in range(0,len(a),1000)];m=max(e);return [v/m for v in e]

def animate():
 env={who:envelope(file) for who,file in [('Muller','muller-add.wav'),('Perez','perez-robert.wav'),('Robert','robert-answer.wav')]};starts={'Muller':25,'Perez':121,'Robert':241}
 for f in range(1,END+1):
  # Hold composition; one cut gives Robert the screen on his reply.
  close=f>=237;CAM.data.ortho_scale=890 if close else 1280;CAM.location=(186 if close else 0,15 if close else 0,1200);key(CAM,f);key(CAM.data,f,'ortho_scale')
  lift=at(f,[(1,1),(208,1),(212,.92),(218,.2),(222,0),(END,0)]);LIFT.value=lift;key(LIFT,f,'value');CUP.location.y=30*lift;key(CUP,f)
  angle=at(f,[(1,0),(238,0),(247,-2.4),(257,-.7),(298,-.7),(306,1.7),(316,.5),(349,.5),(357,2.8),(END,2.8)])
  HLEFT.value=max(0,angle/3);HRIGHT.value=max(0,-angle/3);key(HLEFT,f,'value');key(HRIGHT,f,'value');R['face'].rotation_euler.z=math.radians(angle);key(R['face'],f,'rotation_euler')
  for who,a in list(M.A.items())+[('Robert',R)]:
   start=starts[who];idx=f-start;am=env[who][idx] if 0<=idx<len(env[who]) else 0
   label=('O' if am>.62 else 'A' if am>.36 else 'E' if am>.12 else 'rest') if am>.08 else ('tight' if who=='Muller' else 'rest')
   for name,group in a['mouths'].items():visible(group,name==label,f)
   gaze=at(f,[(1,0),(111,0),(117,-4 if who=='Perez' else 1),(242,0),(248,-7 if who=='Muller' else 0),(350,0),(355,10 if who=='Robert' else -5),(END,10 if who=='Robert' else -5)])
   for i,(ctrl,closed,line,top,bottom) in enumerate(a['eyes']):
    ctrl.location.x=a['c']['eyes'][i]['pupil'][0]-a['c']['eyes'][i]['center'][0]+gaze;key(ctrl,f)
    blink= f in ([104,105,227,228,345,346] if who=='Robert' else [18,19,232,233,315,316])
    closed.value=1 if blink else 0;key(closed,f,'value');visible(line,blink,f)
    br=a['brows'][i];br.rotation_euler.z=math.radians(at(f,[(1,0),(239,0),(249,6 if who=='Robert' else -4),(280,3),(END,3)])*(1 if i==0 else -1));key(br,f,'rotation_euler')
 # Camera-parented captions preserve size and placement across the reply cut.
 for a,b,words in [(25,104,'MÜLLER: Robert played for both clubs. Ask him.'),(121,204,'PÉREZ: Robert, how do we make Flick stop scoring?'),(241,272,'LEWANDOWSKI: Wrong question.'),(273,345,'LEWANDOWSKI: He spent years telling me to score more.')]:
  root=B['control']('S09 caption',parent=CAM)
  B['rect']('S09 caption bed',-.46,-.021,.92,.044,0,'#152732',root,False)
  ob=B['text']('S09 caption words',words,0,-.008,.02,.018,'#f5eedc',root)
  for f in range(1,END+1):
   S.frame_set(f);w=CAM.data.ortho_scale;root.location=(0,-w*.249,-100);root.scale=(w,w,w);key(root,f);key(root,f,'scale')
  visible(root,False,1);visible(root,True,a);visible(root,False,b+1)
 for label,f in EVENTS.items():S.timeline_markers.new(label,frame=f)
 return {'dialogue_start_frames':starts,'cup_contact':222,'camera_cut':237}

def finish():
 # Data checks accompany visible review; they do not certify believable acting.
 assert max(M.errors)<.01
 for action in bpy.data.actions:
  for layer in action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT' if 'hide_' in fc.data_path else 'LINEAR'
 for f in [222,241,300,384]:
  S.frame_set(f);assert abs(CUP.location.y)<1e-6 and abs(LIFT.value)<1e-6
 S.frame_set(260);S['scope']='S09 16-second staged consultation; existing call cast and new supported Robert drawing. No standing/leg mechanics borrowed from S07.'
 bpy.ops.wm.save_as_mainfile(filepath=str(O/'consultation.blend'))
 (O/'construction-check.json').write_text(json.dumps({'frames':END,'fps':24,'cup_contact_frame':222,'cup_moves_after_contact':False,'max_caller_joint_error':max(M.errors),'source_pose':'reference-supported.png','limits':['Small supported cup set-down only; not an extreme-motion solution','S07 balance and limb mechanics remain rejected','Unheard voice candidates; facial mouth shapes are approximate']},indent=2)+'\n')
 return {'native':str(O/'consultation.blend')}
