"""S07 screen-performance construction. Run coherent batches in visible Blender.
Reuses S06 native tracing/contour helpers; poses, staging and prop contacts are new.
Manual rig convenience is not a constraint. No runtime animation handler.
"""
import bpy,math,json,importlib.util,sys,wave,subprocess
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/staging-v001/coaching-performance-v001';ART=V/'assets/coaches-v001'
spec=importlib.util.spec_from_file_location('s07_draw',V/'scripts/build_football_v001.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
g.P='S07 / ';g.O=O;g.END=360;g.M={};A={};SCALE=.00185;END=360;FPS=24
BASE=Vector((12.2,.8,0));R=Vector((1,0,0));D=Vector((0,1,0))
EVENTS={'assistant':28,'flick':112,'reaction':207,'keeper':236,'watch':274,'clipboard':307,'ball_contact':337,'release':348}
at=g.at;turn=g.turn;key=g.key;poly=g.poly;oval=g.oval;line=g.line;empty=g.empty;outlined=g.outlined

def setup():
 global S,C,CAM,BALL,BALLSHADOW,STAND
 assert not bpy.app.background and bpy.context.window
 assert 'S003_S07_Coaching_v001' not in bpy.data.scenes
 with bpy.data.libraries.load(str(V/'artifacts/staging-v001/training-set-v001/training-set.blend'),link=False) as (src,dst):dst.scenes=['S003_Training_Set_v001']
 S=dst.scenes[0].copy();S.name='S003_S07_Coaching_v001';S.use_fake_user=True;bpy.context.window.scene=S
 C=bpy.data.collections.new('S07 / performance');S.collection.children.link(C);g.S=S;g.C=C
 S.frame_start=1;S.frame_end=END;S.render.fps=FPS;S.render.resolution_x=1280;S.render.resolution_y=720;S.render.resolution_percentage=100;S.render.use_sequencer=False;S.display.render_aa='16'
 S['construction']='S06 traced native caricature contours + scene-authored connected poses, corrective silhouettes, prop-specific hands, baked facial and body motion. Final screen performance takes priority over manual editing convenience.'
 # The new shot has its own camera; the inherited physical environment is unchanged.
 cd=bpy.data.cameras.new('S07 / camera');CAM=bpy.data.objects.new(cd.name,cd);C.objects.link(CAM);cd.type='ORTHO';cd.clip_end=250;S.camera=CAM
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=.11);BALL=bpy.context.object;BALL.name='S07 / ball'
 for c in list(BALL.users_collection):c.objects.unlink(BALL)
 C.objects.link(BALL);BALL.data.materials.append(g.mat('#fff4d7'));BALL.data.materials.append(g.mat('#172c42'))
 for p in BALL.data.polygons:p.material_index=1 if p.index%7==0 else 0
 BALLSHADOW=oval('ball shadow',0,0,.14,.07,'#557f4d');BALLSHADOW.rotation_euler.x=math.pi/2
 STAND=empty('clipboard stand');STAND.location=BASE+Vector((1.45,0,0))
 outlined('stand top',[(-.24,.85),(.24,.85),(.24,.91),(-.24,.91)],'#75888a',STAND,-.05)
 line('stand stem',[(0,.04),(0,.85)],'#435b67',.025,STAND,-.02)
 line('stand feet',[(-.20,.025),(0,.06),(.20,.025)],'#435b67',.025,STAND,-.02)
 for area in bpy.context.screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False;area.spaces.active.shading.type='SOLID';area.spaces.active.shading.light='FLAT';area.spaces.active.shading.color_type='MATERIAL'
 return {'scene':S.name,'environment_objects':len(S.objects)}

def text(n,body,parent,pos,size,color='#233349'):
 cu=bpy.data.curves.new('S07 / '+n,'FONT');cu.body=body;cu.size=size;cu.align_x='CENTER';cu.materials.append(g.mat(color));ob=bpy.data.objects.new(cu.name,cu);C.objects.link(ob);ob.parent=parent;ob.location=pos;ob.rotation_euler.x=math.pi/2;return ob

def visibility(root,visible,f):
 for ob in [root]+list(root.children_recursive):
  if ob.type=='EMPTY':continue
  ob.hide_render=not visible;ob.hide_viewport=not visible
  ob.keyframe_insert(data_path='hide_render',frame=f);ob.keyframe_insert(data_path='hide_viewport',frame=f)

def hand_drawing(n,parent,skin,kind):
 h=empty(n,parent)
 if kind=='grip':
  pts=[(-.038,-.018),(.038,-.018),(.056,.025),(.060,.080),(.045,.12),(.021,.14),(-.023,.137),(-.051,.115),(-.058,.067),(-.047,.025)]
  outlined(n+' palm',round_contour(pts),skin,h,.025)
  for z in [.067,.09,.113]:line(n+' fold',[(-.041,z),(-.008,z+.008),(.028,z+.003)],'#a46f48',.0015,h,.028)
  line(n+' thumb',[(.046,.033),(.014,.065),(.024,.083),(.047,.073)],'#a46f48',.0018,h,.029)
 elif kind=='pen':
  pts=[(-.038,-.016),(.038,-.016),(.059,.027),(.054,.074),(.025,.13),(-.007,.137),(-.039,.115),(-.052,.06)]
  outlined(n+' palm',round_contour(pts),skin,h,.026)
  for z in [.045,.067,.089]:line(n+' fingers',[(-.018,z),(.018,z+.008),(.042,z)],'#a46f48',.0015,h,.028)
  line(n+' pen',[(-.052,-.035),(.054,.155)],'#172837',.005,h,.021);line(n+' pen nib',[(-.052,-.035),(-.065,-.054)],'#d1d0b9',.003,h,.023)
 elif kind=='ask':
  pts=[(.021,-.01),(.033,.024),(-.004,.046),(-.032,.03),(-.109,.035),(-.136,.025),(-.124,.008),(-.073,.001),(-.12,-.012),(-.114,-.029),(-.067,-.036),(-.023,-.021)]
  outlined(n+' palm',round_contour(pts),skin,h,.026);line(n+' palm crease',[(-.024,.017),(-.063,.004),(-.087,.007)],'#a46f48',.0018,h,.028)
 elif kind=='roll':
  # Palm down, fingers extend left along the ball's upper trailing surface.
  pts=[(.035,.026),(.032,-.017),(-.033,-.039),(-.083,-.047),(-.102,-.039),(-.099,-.023),(-.062,-.018),(-.118,-.013),(-.129,.001),(-.117,.014),(-.039,.018)]
  outlined(n+' palm',round_contour(pts),skin,h,.026);line(n+' fingers',[(-.035,-.007),(-.093,-.008)],'#a46f48',.0014,h,.029)
 return h

def round_contour(pts):
 out=[]
 for i,p in enumerate(pts):
  p=Vector(p);a=p.lerp(Vector(pts[i-1]),.22);b=p.lerp(Vector(pts[(i+1)%len(pts)]),.22)
  for k in range(5):
   t=k/4;out.append(tuple(a*(1-t)**2+p*(2*t*(1-t))+b*t*t))
 return out

def wrist_angle(p,side):
 a=p['arms'][side];d=Vector(a[2])-Vector(a[1]);return math.atan2(d.y,d.x)-math.pi/2

def leg_lengths(name,side):
 # Calibrate to this actor's standing drawing/stance, not an inherited long limb.
 ankle=-.19 if side=='L' else (.23 if name=='Flick' else .18)
 hip=-.10 if side=='L' else .10
 half=math.hypot(ankle-hip,.88-.045-.13)*1.003/2
 return half,half

def actor(name):
 data=json.loads((ART/(name.lower()+'.json')).read_text());c=data['design'];root=empty(name+' world');torso=empty(name+' body',root);head=empty(name+' head',root)
 a={'root':root,'torso':torso,'head':head,'c':c,'eyes':[],'limbs':{},'hands':{},'feet':[]};A[name]=a
 g.vector_part(name+' portrait',data['parts']['head'],head,c['neck'],SCALE,.022)
 g.vector_part(name+' jacket',data['parts']['body'],torso,c['hip'],SCALE,.025)
 a['neck']=g.deform(name+' neck',[(-.07,1.38),(.08,1.38),(.10,1.57),(-.08,1.57)],c['skin'],root,.017)
 # Upper trouser bridge covers the hip origins. Leg surfaces are continuous.
 outlined(name+' trouser yoke',[(-.21,.03),(.21,.03),(.22,-.12),(.075,-.18),(0,-.10),(-.075,-.18),(-.22,-.12)],'#233553',torso,.014)
 for side,idx in [('L',0),('R',1)]:
  for part,color,dep in [('arm',c['cloth'] if name=='Flick' else c['skin'],.065),('leg','#233553',-.012 if side=='L' else -.020)]:
   a['limbs'][part+side]=(g.deform(name+' '+part+side+' ink',[(0,0)]*34,g.INK,root,dep-.001),g.deform(name+' '+part+side,[(0,0)]*34,color,root,dep))
  if name=='Assistant':a['limbs']['sleeve'+side]=(g.deform(name+' sleeve'+side+' ink',[(0,0)]*34,g.INK,root,.040),g.deform(name+' sleeve'+side,[(0,0)]*34,c['cloth'],root,.041))
  # A few fabric creases follow the same authored limb, not arbitrary image weights.
  a['limbs']['crease'+side]=g.deform(name+' trouser fold'+side,[(0,0)]*34,'#314563',root,-.006)
  hand=empty(name+' wrist '+side,root);a['hands'][side]={'root':hand}
  rest=empty(name+' relaxed '+side,hand);g.vector_part(name+' hand '+side,data['parts']['hand'+str(idx)],rest,c['wrists'][idx],SCALE,.024);a['hands'][side]['rest']=rest
  for kind in ['grip','pen','ask','roll']:a['hands'][side][kind]=hand_drawing(name+' '+kind+side,hand,c['skin'],kind)
  foot=empty(name+' foot '+side,root);g.vector_part(name+' trainer '+side,data['parts']['boot'+str(idx)],foot,c['ankles'][idx],SCALE,.005);a['feet'].append(foot)
  if side=='L' and name=='Flick':
   watch=empty('Flick watch',hand);watch.location.z=-.08;outlined('watch strap',[(-.042,.027),(.047,.027),(.047,.052),(-.042,.052)],'#152839',watch,.032);oval('watch dial',.008,.04,.024,.024,'#b6ced1',watch,.034);line('watch hands',[(.008,.055),(.008,.04),(.021,.04)],'#152839',.0018,watch,.037)
 for i,(x,y,rx,ry) in enumerate(c['eyes']):
  eye=empty(name+' eye'+str(i),head);eye.location=((x-c['neck'][0])*SCALE,-.10,(c['neck'][1]-y)*SCALE+.0045)
  oval(name+' eye outline',0,0,(rx+1)*SCALE,(ry+1)*SCALE,g.INK,eye)
  white=oval(name+' sclera',0,0,rx*SCALE,ry*SCALE,'#fff4da',eye,.001)
  pupil=empty(name+' gaze'+str(i),eye);oval(name+' pupil',0,0,min(rx*.48,ry*.8)*SCALE,ry*.82*SCALE,'#24323b',pupil,.002);oval(name+' glint',-.003,.004,.0022,.0025,'#ffffff',pupil,.003)
  lid=oval(name+' lid',0,0,(rx+2)*SCALE,(ry+2)*SCALE,c['skin'],eye,.004)
  a['eyes'].append((eye,pupil,lid))
 mouth=empty(name+' mouth',head);x,y,rx,ry=c['mouth'];mouth.location=((x-c['neck'][0])*SCALE,-.11,(c['neck'][1]-y)*SCALE+.0053)
 oval(name+' mouth bed',0,0,(rx+2)*SCALE,(ry+2)*SCALE,c['mouth_skin'],mouth)
 aperture=oval(name+' speaking mouth',0,-.001,rx*SCALE*.78,.018,'#55332c',mouth,.002)
 teeth=poly(name+' teeth',[(-.035,.008),(.035,.008),(.028,.002),(-.028,.002)],'#fff0d7',mouth,.003)
 rest=line(name+' lip',[(-rx*SCALE*.8,0),(-rx*SCALE*.3,-.005),(rx*SCALE*.4,-.004),(rx*SCALE*.8,.003)],'#4d3429',.0024,mouth,.004)
 a['mouth']=(aperture,teeth,rest)
 a['shadow']=oval(name+' shadow',0,0,.28,.10,'#5a854d');a['shadow'].rotation_euler.x=math.pi/2
 # Paper and clipboard are authored from the hand's edge registration.
 board=empty(name+' board');a['board']=board;board.scale=(.74,)*3
 outlined(name+' board backing',[(-.38,-.16),(.012,-.16),(.012,.34),(-.38,.34)],'#34495a' if name=='Flick' else '#d9d3b4',board,.052)
 poly(name+' paper',[(-.357,-.14),(-.008,-.14),(-.008,.318),(-.357,.318)],'#fff3d3',board,.055)
 if name=='Assistant':text('result seven','7',board,(-.181,-.059,-.035),.28)
 else:
  poly('clipboard clip',[(-.25,.30),(-.12,.30),(-.12,.35),(-.25,.35)],'#aeb7ae',board,.057)
  for z in [.23,.18,.13,.08]:line('clipboard notes',[(-.32,z),(-.065,z)],'#7d9090',.002,board,.058)
 return {'actor':name,'construction':'native traced portrait/garment; authored limbs and grip drawings'}

def pose(name,f):
 move=0;lean=0;tilt=0;gaze=(0,0)
 if name=='Flick':
  x=.78;hip=Vector((at(f,[(1,0),(307,0),(336,.04),(360,.02)]),at(f,[(1,.88),(307,.88),(336,.61),(348,.61),(360,.64)])))
  lean=at(f,[(1,.02),(98,.02),(121,-.015),(209,-.015),(270,.045),(286,.045),(307,.06),(336,.74),(360,.74)])
  tilt=at(f,[(1,.08),(88,.08),(103,-.035),(184,-.02),(211,-.02),(272,.14),(286,.12),(305,.07),(336,.11)])
  gaze=(at(f,[(1,-.004),(92,-.004),(103,-.01),(214,-.01),(243,-.004),(269,-.003),(285,-.003),(320,-.008)]),at(f,[(1,-.006),(92,-.006),(103,0),(255,0),(270,-.007),(360,-.007)]))
  lf=(-.19,.13);rf=(.23,.13)
  wr=at(f,[(1,(.17,1.18)),(277,(.17,1.18)),(293,(.35,1.11)),(307,(.67,1.07)),(316,(.39,.94)),(337,(.28,.71)),(360,(.28,.73))])
  wl=at(f,[(1,(-.14,1.31)),(85,(-.14,1.31)),(107,(-.30,1.44)),(137,(-.34,1.44)),(199,(-.28,1.40)),(256,(-.28,1.40)),(273,(-.30,1.44)),(283,(-.30,1.44)),(299,(.41,1.19)),(309,(.35,.99)),(322,(-.35,.56)),(337,(-.55,.25)),(348,(-.70,.25)),(360,(-.85,.40))])
  if f<86:wl=(wl[0]+.012*math.sin(f*.35),wl[1]+.006*math.sin(f*.66))
  modes={'L':'pen' if f<307 else ('roll' if f>=323 else 'rest'),'R':'grip' if f<=307 else 'rest'}
 else:
  move=at(f,[(1,0),(32,.32)]);x=-1.32+move
  hip=Vector((0,at(f,[(1,.828),(20,.828),(35,.88),(360,.88)])))
  lean=at(f,[(1,-.04),(34,-.06),(74,-.09),(104,-.035),(190,-.035),(219,.045),(260,.02),(360,.03)])
  tilt=at(f,[(1,-.02),(35,-.04),(70,-.07),(103,-.03),(192,-.03),(215,.07),(240,.045),(276,.02),(346,.03)])
  gaze=(at(f,[(1,.005),(29,.01),(207,.01),(235,.002),(277,.009),(340,.003)]),at(f,[(1,-.002),(30,.001),(199,.001),(213,.003),(274,0),(341,-.010)]))
  step=at(f,[(1,0),(18,1)]);lfmove=at(f,[(18,0),(32,1)])
  lf=(-.19+.32*lfmove-move,.13+.075*math.sin(math.pi*lfmove));rf=(.18+.32*step-move,.13+.07*math.sin(math.pi*step))
  wr=at(f,[(1,(.21,1.15)),(36,(.21,1.22)),(100,(.21,1.22)),(190,(.21,1.22)),(227,(.19,1.04)),(360,(.19,1.04))])
  wl=at(f,[(1,(-.36,.97)),(28,(-.36,.99)),(55,(-.37,1.31)),(91,(-.37,1.31)),(114,(-.34,.98)),(201,(-.34,.98)),(218,(-.40,.91)),(360,(-.40,.91))])
  modes={'L':'ask' if 40<=f<=103 else 'rest','R':'grip'}
 neck=hip+Vector(turn((0,.57),lean));arms={};legs={}
 for side,sgn,wrist,foot in [('L',-1,wl,lf),('R',1,wr,rf)]:
  sh=hip+Vector(turn((sgn*.14,.49),lean));wrv=Vector(wrist)
  # Pose-owned poles keep the elbow outside the torso, including the low roll.
  elbow=g.two_bone_joint(tuple(sh),tuple(wrv),(.35,.35),(sh.x+sgn*.55,sh.y-.28))
  arms[side]=(tuple(sh),elbow,tuple(wrv))
  start=hip+Vector((sgn*.10,-.045));knee=g.two_bone_joint(tuple(start),foot,leg_lengths(name,side),(start.x+.4,start.y-.2))
  legs[side]=(tuple(start),knee,foot)
 return dict(world=BASE+Vector((x,0,0)),hip=hip,neck=neck,lean=lean,tilt=tilt,gaze=gaze,arms=arms,legs=legs,modes=modes)

def board_pose(name,f):
 # Its grip registration is shared with the wrist until release; then it rests.
 p=pose(name,min(f,307) if name=='Flick' else f);w=Vector(p['arms']['R'][2])+Vector(turn((0,.070),wrist_angle(p,'R')));return p['world']+Vector((w.x,-.02,w.y))

def ball_position(f):
 if f<=337:return BASE+Vector((.78-.65,-.08,.11))
 if f<=348:
  wrist=Vector(pose('Flick',f)['arms']['L'][2]);return BASE+Vector((.78+wrist.x-.10,-.08,.11))
 p=ball_position(348);t=(f-348)/24
 return p+Vector((-2.0*t,-1.05*t,0))

def speech_envelope(name):
 filename={'Flick':'flick-seven','Assistant':'assistant-seven'}[name];raw=subprocess.check_output(['/opt/homebrew/bin/ffmpeg','-v','error','-i',str(V/'assets/voices-v001'/f'{filename}.wav'),'-f','f32le','-ac','1','-ar','24000','pipe:1'])
 import array
 a=array.array('f');a.frombytes(raw);env=[]
 for i in range(0,len(a),1000):
  chunk=a[i:i+1000];env.append(math.sqrt(sum(x*x for x in chunk)/len(chunk)))
 peak=max(env);return [min(1,x/(peak*.65)) for x in env]

def animate_actor(name):
 a=A[name];c=a['c'];env=speech_envelope(name);start=EVENTS['flick' if name=='Flick' else 'assistant']
 for f in range(1,END+1):
  p=pose(name,f);a['root'].location=p['world'];key(a['root'],f);a['torso'].location=(p['hip'].x,0,p['hip'].y);a['torso'].rotation_euler.y=-p['lean'];key(a['torso'],f)
  a['head'].location=(p['neck'].x,-.02,p['neck'].y);a['head'].rotation_euler.y=-p['lean']-p['tilt'];key(a['head'],f)
  shape=f%2==1 or f in EVENTS.values() or f==END
  if shape:
   pts=[tuple(p['neck']+Vector(turn(q,p['lean']+(p['tilt'] if q[1]>.03 else 0)))) for q in [(-.075,-.10),(.082,-.10),(.105,.10),(-.085,.10)]];g.pose_shape(a['neck'],pts,f)
  for side in ['L','R']:
   arm=p['arms'][side];leg=p['legs'][side]
   if shape:
    rows=[('arm'+side,arm,[.090,.076,.039] if name=='Flick' else [.061,.050,.029]),('leg'+side,leg,[.106,.083,.067])]
    if name=='Assistant':rows.append(('sleeve'+side,(arm[0],tuple(Vector(arm[0]).lerp(Vector(arm[1]),.35)),tuple(Vector(arm[0]).lerp(Vector(arm[1]),.74))),[.092,.086,.071]))
    for part,points,widths in rows:
     ink,fill=a['limbs'][part];g.pose_shape(ink,g.ribbon(points,[w+.003 for w in widths]),f);g.pose_shape(fill,g.ribbon(points,widths),f)
     if part.startswith(('arm','sleeve')):
      # Shoulder caps stay under the torso; the forearm can cross in front.
      # The old constant-depth closed strip exposed its cut end as a shoulder seam.
      for ob,edge in [(ink,True),(fill,False)]:
       for j,v in enumerate(ob.data.shape_keys.key_blocks[-1].data):
        t=(j if j<17 else 33-j)/16
        depth=at(t,[(0,-.006),(.35,-.002),(.6,.020),(1,.025)]) if part.startswith('sleeve') else at(t,[(0,-.007),(.23,-.003),(.52,.064),(1,.064)])
        v.co.y=-depth+(.001 if edge else 0)
    # A thin fold inside the trouser silhouette, tied to leg construction.
    fold=[tuple(Vector(pt)+Vector((.025,0))) for pt in leg];g.pose_shape(a['limbs']['crease'+side],g.ribbon(fold,[.008,.010,.004]),f)
   hand=a['hands'][side];w=Vector(arm[2]);hand['root'].location=(w.x,-.065,w.y)
   angle=wrist_angle(p,side);hand['root'].rotation_euler.y=-angle;key(hand['root'],f)
   for kind in ['ask','roll']:hand[kind].rotation_euler.y=angle;key(hand[kind],f)
   hand['rest'].rotation_euler.y=math.pi;key(hand['rest'],f)
   for kind in ['rest','grip','pen','ask','roll']:visibility(hand[kind],kind==p['modes'][side],f)
   foot=a['feet'][0 if side=='L' else 1];pt=leg[2];foot.location=(pt[0],-.005 if side=='L' else .012,pt[1]);key(foot,f)
  for i,(eye,pupil,lid) in enumerate(a['eyes']):
   pupil.location.x=p['gaze'][0];pupil.location.z=p['gaze'][1];key(pupil,f)
   blink=(f in range(96,99) or f in range(265,268)) if name=='Flick' else (f in range(107,110) or f in range(231,234))
   visibility(lid,blink,f)
   eye.scale.z=at(f,[(1,1),(199,1),(213,1.13),(250,1.02)]) if name=='Assistant' else 1;key(eye,f)
  amp=env[f-start] if 0<=f-start<len(env) else 0
  if name=='Assistant' and 211<=f<=342:amp=at(f,[(211,.55),(224,.7),(334,.7),(342,0)])
  aperture,teeth,rest=a['mouth'];visibility(aperture,amp>.09,f);visibility(teeth,amp>.35,f);visibility(rest,amp<=.09,f)
  aperture.scale.z=.12+amp*.86;key(aperture,f)
  a['board'].location=board_pose(name,f);key(a['board'],f)
  a['shadow'].location=(p['world'].x,p['world'].y,.022);key(a['shadow'],f)
 return {'actor':name,'frames':END}

def camera(f):
 # Deliberate cuts preserve the conversation axis. Only the reply has a small push.
 if f<103:x=-.12;z=1.04;width=4.9
 elif f<207:x=.69;z=1.48;width=at(f,[(103,1.95),(197,1.83),(206,1.83)])
 elif f<265:x=-.99;z=1.43;width=1.95
 else:x=.20;z=1.00;width=4.25
 target=BASE+Vector((x,0,z));CAM.location=target+Vector((0,-25,2.0));CAM.rotation_euler=(target-CAM.location).to_track_quat('-Z','Y').to_euler();CAM.data.ortho_scale=width;key(CAM,f);CAM.data.keyframe_insert(data_path='ortho_scale',frame=f)

def animate_scene():
 for f in range(1,END+1):
  camera(f);BALL.location=ball_position(f);BALL.rotation_euler=(0,-max(0,f-337)*.10,0);key(BALL,f);BALLSHADOW.location=(BALL.location.x,BALL.location.y,.024);key(BALLSHADOW,f)
 for label,f in EVENTS.items():S.timeline_markers.new(label,frame=f)
 S['events']=json.dumps(EVENTS);S.frame_set(1)

def captions():
 lines=[(28,91,'ASSISTANT: We scored seven. Can we slow down now?'),(112,146,'FLICK: We did slow down.'),(147,206,'FLICK: That is why it was only seven.'),(236,265,'BARÇA KEEPER (OFFSCREEN): Can we have a break?')]
 for start,end,words in lines:
  root=empty('caption '+str(start),CAM);bg=poly('caption panel',[(-.455,-.019),(.455,-.019),(.455,.019),(-.455,.019)],'#172432',root);bg.rotation_euler.x=-math.pi/2
  tx=text('subtitle',words,root,(0,-.007,.02),.021,'#fff3d7');tx.rotation_euler.x=0
  for f in range(1,END+1):
   S.frame_set(f);w=CAM.data.ortho_scale;root.location=(0,-w*9/32+w*.043,-1);root.scale=(w,w,w);key(root,f);visibility(root,start<=f<=end,f)

def check_save():
 for f in range(1,END+1):
  for name in A:
   p=pose(name,f)
   for side in ['L','R']:
    for points,lengths in [(p['arms'][side],(.35,.35)),(p['legs'][side],leg_lengths(name,side))]:
     assert all(abs((Vector(points[i+1])-Vector(points[i])).length-lengths[i])<1e-5 for i in [0,1])
  assert abs(ball_position(f).z-.11)<1e-8
 for f in range(337,349):
  p=pose('Flick',f);w=p['world']+Vector((p['arms']['L'][2][0]-.1,-.08,.11));assert (w-ball_position(f)).length<1e-5
 for name in A:
  for side in ['L','R']:
   hip,knee,ankle=map(Vector,pose(name,70)['legs'][side]);bend=(knee-hip).angle(ankle-knee)
   assert bend<math.radians(10),(name,side,'rest crouch',math.degrees(bend))
 for f in range(33,END+1):
  for name in A:
   p=pose(name,f)
   for side in ['L','R']:
    q=pose(name,33);assert (p['world']+Vector((p['legs'][side][2][0],0,p['legs'][side][2][1]))-q['world']-Vector((q['legs'][side][2][0],0,q['legs'][side][2][1]))).length<1e-6
 g.linear_keys();g.sync_preview_visibility();S.frame_set(1);S.use_fake_user=True
 O.mkdir(exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(O/'coaching-performance.blend'))
 report={'frames':END,'fps':FPS,'duration_seconds':END/FPS,'checks':['all authored arm/leg endpoints reachable, lengths retained','feet planted after approach','ball rests on field, shared hand/release schedule','preview drawing visibility matches render'],'limits':'Geometry checks do not certify visible surfaces, acting, sound or benchmark quality.'}
 (O/'construction-check.json').write_text(json.dumps(report,indent=2)+'\n');return report
