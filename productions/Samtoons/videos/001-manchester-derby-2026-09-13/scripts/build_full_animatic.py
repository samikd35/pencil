"""150-second combined animatic. Run coherent scene batches in visible Blender."""
from pathlib import Path
from types import SimpleNamespace
import bpy,json,math,ast
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/animatic-v001';ART=ROOT/'assets/film-cast-v001'
D={'__file__':str(ROOT/'scripts/build_dramatic_actions.py')};exec(compile(Path(D['__file__']).read_text(),D['__file__'],'exec'),D)
A=D['A'];keys=D['keys'];pose=D['pose'];smooth=D['smooth_actor'];poly=D['poly'];text=D['text'];empty=D['empty'];rect=D['rect'];line=D['line'];oval=D['oval']
EDIT=[];CAST={};SPEECH=[]
BASE=[('S01',192),('S02',576),('S03',288),('S04',288),('S05',696),('S06',168),('S07',216),('S08',408),('S09',288),('S10',480)]
SOURCES=json.loads((ART/'landmarks.json').read_text())
for cfg in SOURCES.values():
 scale=1024/(cfg['crop'][2]-cfg['crop'][0]);cfg['coordinate_scale']=scale
 for k in ('center_x','floor_y','body_height'):cfg[k]*=scale
 for k in cfg['joints']:cfg['joints'][k]=[v*scale for v in cfg['joints'][k]]
 for k in ('eyes','brows'):cfg[k]=[[v*scale for v in row] for row in cfg[k]]
 cfg['mouth']=[v*scale for v in cfg['mouth']]
original_material=A['image_material']
def crop_material(path):
 im,mat=original_material(path)
 cfg=next((v for v in SOURCES.values() if Path(v['image']).name==Path(path).name and v.get('active')),None)
 return (SimpleNamespace(size=(1024,(cfg['crop'][3]-cfg['crop'][1])*cfg['coordinate_scale'])) if cfg else im),mat
A['image_material']=crop_material

def sc(beat,suffix,frames,loc=(.5,-7,2.3),target=(.1,0,1.1),touchline=False):
 s=D['scene']('FILM '+beat+' / '+suffix,frames,loc,target);EDIT.append(dict(beat=beat,scene=s.name,frames=frames));s['Scope']='Complete animatic candidate; new cast, acting and timing await combined review.'
 if touchline:
  for ob in list(D['col'].objects):
   if ob.name.startswith(('A / goal','A / net','A / top net','A / side net','A / area line')):D['col'].objects.unlink(ob)
  A['tube']('Touchline',[(-40,-.8,.02),(40,-.8,.02)],'#fff8e6',.032)
 return s

def use(scene,beat):
 s=bpy.data.scenes[scene];EDIT.append(dict(beat=beat,scene=s.name,frames=s.frame_end));bpy.context.window.scene=s
 D.update(s=s,col=s.collection.children[0],cam=s.camera);A.update(s=s,col=D['col'],cam=s.camera);A['base'].update(s=s,skin=D['col'],ink=A['mat']('#202329'),font=next(f for f in bpy.data.fonts if f.filepath.endswith('Arial Bold.ttf')))
 return s

def person(name,loc,tag=None):
 tag=tag or name+' '+str(len(EDIT));cfg=SOURCES.get(name)
 if cfg:
  for c in SOURCES.values():c['active']=False
  cfg['active']=True;D['CONFIG'][name]=cfg
 a=D['actor'](tag,name,loc);CAST[tag]=a
 if cfg:bind_new(a)
 if cfg:
  x0,y0,x1,y1=cfg['crop'];W,H=cfg['sheet_size']
  for uv in a['skin'].data.uv_layers.active.data:uv.uv=((x0+uv.uv.x*(x1-x0))/W,1-(y0+(1-uv.uv.y)*(y1-y0))/H)
  cfg['active']=False
 return a

def bind_new(a):
 # The new sheets have different limb silhouettes; blend distance weights across
 # the whole body instead of inheriting the first drawing's hard region cutoffs.
 bones={b.name:(Vector(b.head_local),Vector(b.tail_local)) for b in a['armature'].data.bones}
 for v in a['skin'].data.vertices:
  if v.co.y>a['rest']['neck'].y+.08:weights=[('head',1.)]
  else:
   ranked=sorted((max(0,A['segment_distance'](v.co,*ends)-(.28 if name=='torso' else 0)),name) for name,ends in bones.items())[:3]
   vals=[math.exp(-d*d/.055) for d,n in ranked];total=sum(vals)
   weights=[(n,w/total) for (d,n),w in zip(ranked,vals)] if total>1e-30 else [(ranked[0][1],1.)]
  hy=a['rest']['hip'].y;ny=a['rest']['neck'].y
  if v.co.y<hy-.35 and abs(v.co.x-a['rest']['hip'].x)<1.0:
   weights=[(n,w) for n,w in weights if n=='torso' or any(k in n for k in ('thigh','calf','foot'))]
   if not weights:
    name=min((n for n in bones if any(k in n for k in ('thigh','calf','foot'))),key=lambda n:A['segment_distance'](v.co,*bones[n]));weights=[(name,1.)]
   total=sum(w for n,w in weights);weights=[(n,w/total) for n,w in weights]

  if hy-.45<v.co.y<ny-.18:
   t=max(0,min(1,(v.co.y-hy-.5)/(ny-hy-.7)))
   width=.94-.53*t
   strength=max(0,min(1,(width-abs(v.co.x-a['rest']['hip'].x))/.12))
   weights=[(n,w*(1-strength)) for n,w in weights if n!='torso']+ [('torso',strength+sum(w for n,w in weights if n=='torso')*(1-strength))]
  for group in [g.group for g in v.groups]:a['skin'].vertex_groups[group].remove([v.index])
  for n,w in weights:a['skin'].vertex_groups[n].add([v.index],w,'REPLACE')

def arms(l=0,r=0):return [('L',['shoulder','elbow','wrist','finger'],[-.12,l,l]),('R',['shoulder','elbow','wrist','finger'],[.12,r,r])]
def act(a,poses):
 for f,t,off,l,r in poses:pose(a,f,t,off,arms(l,r))
 smooth(a)

def idle(a,end,emotion='neutral'):
 act(a,[(1,0,(0,0),-.15,.15),(end,0,(0,0),-.15,.15)])
 D['face_keys'](a,[(1,.03),(end,.03)],[(1,.4 if emotion=='happy' else -.35 if emotion=='angry' else 0)],angry=emotion=='angry')
 for i in (0,1):keys(a['facial']['eye'+str(i)],'scale',[(1,(1,1,1)),(end//2,(1,1,1)),(end//2+2,(1,.08,1)),(end//2+5,(1,1,1)),(end,(1,1,1))])

def speak(a,slug,frame,words=None):
 if isinstance(a,str):mouth=bpy.data.objects[a]
 else:mouth=a['facial']['mouth']
 SPEECH.append(dict(scene=D['s'].name,mouth=mouth.name,id=slug,frame=frame,text=words))

def cap(words,start=1,end=None,y=.4,size=.034):return D['label'](words,start,end or D['s'].frame_end,y,size)
def event(name,frame):
 s=D['s'];data=json.loads(s.get('events','{}'));data[name]=frame;s['events']=json.dumps(data)

def prop_card(name,body,loc,w=.8,h=.55,parent=None):
 root=empty(name,loc,parent)
 if not parent:root.rotation_euler.x=math.pi/2
 rect(name+' paper',-w/2,0,w,h,0,'#fff3db',root)
 text(name+' words',body,0,h*.56,.025,h*.25,'#243444',root)
 for ob in root.children:
  if ob.type=='CURVE':ob.data.bevel_depth=.006
 return root

def opening():
 sc('S01','Morning Pep',192,touchline=True)
 h=person('Haaland',(-.9,0,.02));m=person('Maresca',(.95,.15,.02));idle(h,192,'happy');idle(m,192)
 act(h,[(1,-.05,(0,0),-.1,.1),(46,.03,(0,0),-.1,1.3),(85,0,(0,0),-.1,.6),(192,0,(0,0),-.1,.3)])
 act(m,[(1,0,(0,0),-.1,.1),(107,0,(0,0),-.1,.1),(117,-.03,(0,0),-1.55,1.55),(192,-.02,(0,0),-1.55,1.55)])
 badge=prop_card('Maresca ENZO badge','ENZO',(0,.10,.15),.85,.5,m['controls']['Lfinger']);badge.scale=(2.3,2.3,1);D['visible_tree'](badge,114,192)
 cap('OLD TRAFFORD  /  13 SEP 2026',1,45);cap('UNITED 0–1 CITY',1,45,y=.33,size=.052)
 speak(h,'morning',59);event('greeting',59);event('badge_reveal',114)
 D['camera_keys']([(1,(.5,-7,2.3),(.1,0,1.1)),(108,(.5,-4.7,2.1),(.1,0,1.45))])

def exit_scene():
 use('S02 / kick and overreaction','S02');speak('A Drama Bruno / mouth control','bruno-approved',154,'REF! REF!')
 sc('S02','Gone fishing',240,touchline=True)
 f=person('Foden',(-1,0,.02));b=person('Bruno',(.75,.1,.02));r=person('Oliver',(1.85,.55,.02));idle(f,240,'angry');idle(b,240,'happy');idle(r,240)
 act(f,[(1,-.05,(0,0),-.1,.1),(12,-.1,(0,0),-.2,1.8),(38,-.07,(0,0),-.3,1.6),(66,0,(0,0),-.2,.3),(110,.05,(0,0),-1.0,.4),(240,.05,(0,0),-1.0,.4)])
 speak(f,'and-him',9);speak(f,'fishing',67);speak(b,'less-problem',180)
 rod=empty('Foden fishing rod',(.02,.0,.08),f['controls']['Lfinger']);line('Fishing rod',[(0,0),(-.35,2.8),(-.15,3.3)],0,'#75533b',.026,rod);line('Fishing line',[(-.15,3.3),(.3,2.5),(.36,.7)],.01,'#e5e1c9',.008,rod);D['visible_tree'](rod,90,240)
 keys(f['root'],'location',[(1,(-1,0,.02)),(109,(-1,0,.02)),(190,(-3.7,0,.02)),(240,(-5,0,.02))])
 # Small alternating planted-step lift during exit; whole body travels with the walk.
 for j,fr in enumerate(range(110,225,12)):
  for side,sign in [('L',1),('R',-1)]:
   for part in ('knee','ankle','toe'):
    ob=f['controls'][side+part];ob.location=f['rest'][side+part]+Vector((sign*.16*math.sin(j*math.pi/2),.15*max(0,sign*math.sin(j*math.pi/2)),0));ob.keyframe_insert(data_path='location',frame=fr)
 cap('11 v 10',164,240,y=.31,size=.11);cap('ONE LESS PROBLEM?',164,240,y=.40)
 stamp=prop_card('Decision stamp','RESOLVED',(-.85,-.2,1.85),.9,.35);D['visible_tree'](stamp,38,65);event('stamp',38)

def post_shot(beat,player,second=False):
 s=sc(beat,'Post saves again' if second else 'The first post',288,loc=(4,-4,3.3),target=(3.5,6,1.2))
 p=person(player,(3.0,2.8,.02));g=person('Donnarumma',(3.5,8.3,.02));idle(p,288);idle(g,288)
 wall=[]
 if not second:
  for i,name in enumerate(('Haaland','Fernandez')):
   x=person(name,(1.2+i*.6,5.4,.02),'Wall '+str(i));idle(x,288);wall.append(x)
 else:
  x=person('Fernandez',(5.7,5.7,.02),'Chasing defender');idle(x,288)
 for fr,k in [(1,0),(35,.4),(48,.65),(57,-.9),(70,-.25),(91,0),(288,0)]:pose(p,fr,limbs=[('R',['hip','knee','ankle','toe'],[k,k,k])]+arms(-.5,.5))
 smooth(p);s.frame_set(57);bpy.context.view_layer.update();start=p['controls']['Rtoe'].matrix_world.translation+Vector((.03,0,.03));contact=Vector((-.16,9,1.0))
 ball=D['football'](beat+' ball',start);keys(ball,'location',[(1,start),(56,start),(57,start),(84,contact),(101,(1.1,7.7,.5)),(117,(3.4,8.2,1.0)),(132,(3.4,8.2,.2)),(288,(3.4,8.2,.2))])
 for layer in ball.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
 event('strike',57);event('post_hit',84)
 # Cut to expressive footballer and the dimensional post, with an impossible face on it.
 face=empty(beat+' post personality',(-.16,8.92,1.1));face.rotation_euler.x=math.pi/2
 for x in (-.065,.065):poly(beat+' post eye',oval(x,.1,.045,.060),.025,'#fff8e9',face);poly(beat+' post pupil',oval(x,.1,.017,.030),.04,'#223240',face,False)
 mouth=empty(beat+' post mouth',(0,-.07,.04),face);poly(beat+' post grin',[(-.09,0),(.09,0),(.045,-.07),(-.045,-.07)],.01,'#263641',mouth,False)
 D['visible_tree'](face,106,288)
 if second:
  scarf=empty('City scarf',(-.16,8.87,.8));scarf.rotation_euler.x=math.pi/2
  rect('Scarf collar',-.2,0,.4,.14,0,'#8fd4f1',scarf);rect('Scarf tail',.06,-.55,.14,.6,.005,'#8fd4f1',scarf);D['visible_tree'](scarf,110,288)
  speak(mouth.name,'contract',146);br=person('Bruno',(1.3,8.2,.02),'Post Bruno');idle(br,288,'angry');speak(br,'bruno-approved',245,'REF! REF!')
  cap('TWO SAVES',111,145,y=.35,size=.06)
 else:
  act(p,[(90,0,(0,0),-.15,.15),(110,-.08,(0,0),-.15,2.1),(129,.03,(0,0),-.15,2.2),(162,-.06,(0,0),-.15,1.9),(194,.08,(0,0),-.15,2.1),(230,0,(0,0),-.15,.2),(288,0,(0,0),-.15,.2)])
  cap('RASHFORD',1,45)
 D['camera_keys']([(1,(4,-4,3.3),(3.5,6,1.2)),(108,(-.2,4.7,1.9),(.0,8.8,1.25)),(236,(.5,4.2,2.0),(1.1,8.0,1.5))] if second else [(1,(4,-4,3.3),(3.5,6,1.2)),(108,(2.8,-.5,2.1),(3.0,2.8,1.4)),(198,(-.1,4.7,1.7),(-.16,9,1.2))])

def goal():
 s=sc('S05','Goal then flag',264,loc=(12,-3,5),target=(3.5,6,1))
 h=person('Haaland',(5.7,7.5,.02));e=person('Fernandez',(2.0,6.8,.02));d=person('Martinez',(2.5,7.0,.02));g=person('Lammens',(3.5,8.4,.02))
 for a in (h,e,d,g):idle(a,264)
 cap('GVARDIOL’S DEFLECTED CROSS',1,68)
 act(e,[(1,0,(0,0),-.1,.1),(68,-.15,(.3,0),-.5,.5),(91,.13,(-.1,0),-.5,.5),(120,0,(0,0),-.1,.1),(264,0,(0,0),-.1,.1)])
 for fr,k in [(1,0),(92,.35),(110,-.8),(124,-.2),(145,0),(264,0)]:pose(h,fr,limbs=[('L',['hip','knee','ankle','toe'],[k,k,k])]+arms(-.3,.6))
 smooth(h);s.frame_set(110);bpy.context.view_layer.update();boot=h['controls']['Ltoe'].matrix_world.translation.copy()+Vector((0,0,.05))
 ball=D['football']('Goal ball',(-2,3.7,.5));keys(ball,'location',[(1,(-2,3.7,.2)),(28,(-2,3.7,.2)),(52,(-.3,5.0,1.5)),(74,(1.9,6.8,1.0)),(88,(3.6,7.3,.65)),(110,boot),(126,(5.8,10,.4)),(144,(5.9,10.4,.12)),(264,(5.9,10.4,.12))])
 flag=prop_card('Offside flag','NO GOAL',(0,.28,-2),.7,.33,D['cam']);D['visible_tree'](flag,157,264)
 loading=empty('Haaland loading wheel',(0,1.8,.1),h['face']);line('Loading ring',oval(0,0,.22,.22),0,'#f4d375',.03,loading);rect('Loading gap',-.05,.16,.1,.13,.04,'#304553',loading);D['visible_tree'](loading,166,264);keys(loading,'rotation_euler',[(166,(0,0,0)),(264,(0,0,-math.tau*2))])
 cap('HAALAND',103,145);event('cross',28);event('finish',110);event('flag',157)
 D['camera_keys']([(1,(12,-3,5),(3.5,6,1)),(145,(5.8,3.3,2.1),(5.7,7.5,1.4))])

def var_room():
 sc('S05','VAR office',216,loc=(0,-6,2.1),target=(0,0,1.4),touchline=True)
 # A camera-facing office insert replaces the stadium within this framing.
 wall=empty('VAR room wall',(0,1,0));wall.rotation_euler.x=math.pi/2;rect('Office wall',-5,0,10,5,0,'#273747',wall)
 screen=prop_card('VAR monitor','HAALAND ONSIDE\nNO TOUCH\nAFFECTED DEFENDER?',(0,.5,.65),3.4,1.9)
 D['s'].objects['VAR monitor words'].data.size=.225;D['s'].objects['VAR monitor words'].location.y=.91
 text('VAR title','VIDEO ASSISTANT REFEREE',0,1.65,.04,.13,'#26415a',screen)
 for i,fr in enumerate((45,81,1)):
  y=1.20-i*.32
  line('Check box '+str(i),[(-1.42,y-.07),(-1.28,y-.07),(-1.28,y+.07),(-1.42,y+.07),(-1.42,y-.07)],.04,'#49646b',.01,screen)
  if i<2:
   tick=line('Tick '+str(i),[(-1.42,y),(-1.37,y-.04),(-1.27,y+.075)],.05,'#39825a',.018,screen);D['visible_tree'](tick,fr,216)
 # Scanner/bar skips the third line; an enormous approval stamp lands over the desk.
 stamp=prop_card('VAR goal stamp','GOAL',(1.15,-.15,.3),1.1,.6);D['visible_tree'](stamp,111,216)
 speak('VAR monitor words','var',45);event('onside',45);event('no_touch',81);event('goal_given',111)
 cap('VAR',1,216)

def goal_reaction():
 sc('S05','What about him',216,touchline=True)
 d=person('Martinez',(-1.3,0,.02));e=person('Fernandez',(.15,.1,.02));h=person('Haaland',(1.4,.1,.02));b=person('Bruno',(-2.4,.6,.02));idle(d,216,'angry');idle(e,216);idle(h,216,'happy');idle(b,216,'angry')
 act(d,[(1,0,(0,0),-.1,.1),(19,-.08,(0,0),-.1,1.7),(72,-.03,(0,0),-.1,1.6),(216,0,(0,0),-.1,1.6)])
 speak(d,'him',20);speak(h,'yes',106)
 scroll=prop_card('Bruno endless complaint','COMPLAINT',(.1,.15,.1),.7,1,b['controls']['Lfinger']);keys(scroll,'scale',[(1,(1,.1,1)),(56,(1,.2,1)),(118,(1,2.6,1)),(216,(1,2.6,1))])
 keys(h['root'],'location',[(1,(1.4,.1,.02)),(104,(1.4,.1,.02)),(113,(1.4,.1,.45)),(125,(1.4,.1,.02)),(216,(1.4,.1,.02))])
 cap('UNITED 0–1 CITY',106,216,y=.39,size=.05);event('reboot',106)

def other_post():
 s=sc('S06','Ours works too',168,loc=(4,-4,3.3),target=(3.5,6,1.2))
 e=person('Fernandez',(4,3,.02));g=person('Lammens',(3.5,8.1,.02));idle(e,168);idle(g,168,'happy')
 act(g,[(1,0,(0,0),-.2,.2),(30,-.15,(0,-.15),-.6,.6),(56,-.35,(.1,.35),-2,2),(71,-.3,(.1,.3),-1.7,1.7),(94,0,(0,0),-.3,.3),(168,0,(0,0),-.3,.3)])
 s.frame_set(56);bpy.context.view_layer.update();glove=g['controls']['Rfinger'].matrix_world.translation.copy();ball=D['football']('Other end shot',(4,3,.15));keys(ball,'location',[(1,(4,3,.15)),(24,(4,3,.15)),(56,glove),(69,(7.16,9,1.7)),(91,(8.2,7.4,.5)),(168,(8.2,7.4,.13))]);speak(g,'ours',108);event('strike',24);event('tip',56);event('post_hit',69)
 D['camera_keys']([(1,(4,-4,3.3),(3.5,6,1.2)),(98,(3.7,4.6,2.1),(3.5,8.1,1.45))])

def header():
 s=sc('S07','Square head',216,loc=(4,-4,3.4),target=(3.5,6,1.2))
 m=person('Maguire',(4,6.5,.02));g=person('Donnarumma',(3.5,8.5,.02));idle(m,216);idle(g,216)
 for i,(name,loc) in enumerate([('Mainoo',(2.5,6,.02)),('Rashford',(5.8,6.7,.02)),('Haaland',(3.2,7,.02)),('Fernandez',(5.2,7.5,.02))]):a=person(name,loc,'Corner '+str(i));idle(a,216)
 act(m,[(1,0,(0,0),-.1,.1),(47,-.12,(0,-.22),-.6,.6),(66,.12,(0,.55),-.7,.7),(76,-.15,(0,.42),-.5,.5),(98,0,(0,0),-.1,.1),(216,0,(0,0),-.1,.1)])
 s.frame_set(74);bpy.context.view_layer.update();head=m['controls']['head'].matrix_world.translation.copy();ball=D['football']('Corner ball',(-2,8,2.8));keys(ball,'location',[(1,(-2,8,2.8)),(30,(-2,8,2.8)),(74,head),(93,(7.65,9,2)),(118,(9.5,11,.7)),(216,(9.5,11,.13))]);event('header',74);event('wide',93)
 cap('CORNER. BRING THE BIG HEAD.',1,58);cap('WIDE.',106,170,y=.31,size=.09)
 D['camera_keys']([(1,(4,-4,3.4),(3.5,6,1.2)),(127,(4.2,3,2.1),(4,6.5,1.5))])

def late_save():
 sc('S08','Surely now',120,touchline=True)
 b=person('Bruno',(-.7,0,.02));m=person('Mbeumo',(1,.15,.02));idle(b,120);idle(m,120)
 act(b,[(1,-.04,(0,0),-.6,.6),(38,-.08,(0,.04),-1.2,1.2),(95,-.05,(0,.04),-1.2,1.2),(120,-.05,(0,.04),-1.2,1.2)])
 speak(b,'surely',44);cap('90+5′  /  ONE LAST CHANCE',1,120)
 use('S08 / hope and parry','S08')
 sc('S08','Good wolf',120,loc=(4,4.2,2.3),target=(3.5,8,1.3))
 g=person('Donnarumma',(3.0,8,.02));h=person('Haaland',(4.6,8,.02));idle(g,120,'happy');idle(h,120,'happy')
 # Pointed ear silhouette belongs to the keeper's comic transformation, not his skin.
 for sign in (-1,1):poly('Wolf ear',[(sign*.34,1.23),(sign*.43,1.85),(sign*.08,1.5)],-.03,'#394650',g['face']);
 speak(h,'wolf',54);cap('DENIED.',1,39,y=.32,size=.08)

def celebration():
 sc('S09','Pep two point oh',288,touchline=True)
 h=person('Haaland',(-.95,0,.02));m=person('Maresca',(.95,.1,.02));idle(h,288,'happy');idle(m,288)
 lounge=empty('Maresca lounger',(.9,.4,.2));lounge.rotation_euler.x=math.pi/2;poly('Lounger canvas',[(-.65,0),(.65,0),(.65,1.2),(-.65,1.2)],-.1,'#96d2e7',lounge);line('Lounger frame',[(-.8,-.2),(-.65,1.3),(.65,1.3),(.8,-.2)],0,'#eef3df',.035,lounge)
 badge=prop_card('Perfect record','4 WINS / 4 GAMES',(0,.30,-2),.85,.24,D['cam']);
 cup=empty('Maresca teacup',(0,.1,.1),m['controls']['Rfinger']);rect('Cup',-.15,0,.3,.25,0,'#fff2df',cup);line('Cup handle',[(.15,.18),(.26,.18),(.26,.05),(.15,.05)],.01,'#fff2df',.025,cup)
 speak(h,'thanks',57);speak(m,'enzo',106);speak(h,'pep-two',184)
 act(m,[(1,0,(0,0),-.1,1.4),(100,0,(0,0),-.1,1.4),(112,-.06,(0,.05),-1.6,1.4),(148,0,(0,0),-.6,1.4),(225,0,(0,0),-.6,1.4),(288,0,(0,0),-.6,1.4)])
 cap('FULL TIME  /  0–1',1,43);event('name_bark',106)

def ending():
 use('S10 / tears and umbrella','S10');speak('A Apology Oliver / mouth control','oliver-approved',43,"I'm so... so sorry!");speak('A Apology Carrick / mouth control','carrick-approved',221,'Any points with that?')
 sc('S10','They are biting',216,loc=(1,-9,3.4),target=(0,0,1),touchline=True)
 f=person('Foden',(.8,0,.35));idle(f,216,'happy');act(f,[(1,0,(0,0),-1.0,.4),(78,-.05,(0,0),-1.05,.4),(145,.03,(0,0),-1.1,.5),(216,.03,(0,0),-1.1,.5)])
 water=A['surface']('Flooded pitch',[(-45,-20,.25),(45,-20,.25),(45,25,.25),(-45,25,.25)],'#6ab8d0')
 for y in range(-4,12,2):
  ripple=A['tube']('Water ripples',[(x,y+.10*math.sin(x*1.5),.265) for x in range(-10,11)],'#b8e5ea',.012);keys(ripple,'location',[(1,(0,0,0)),(216,(.7,.2,0))])
 rod=empty('Payoff rod',(.03,.02,.12),f['controls']['Lfinger']);line('Rod pole',[(0,0),(-.45,2.7),(-.85,3.2)],0,'#6b4d39',.025,rod)
 # Fixed line descends to the float on the flooded pitch; the float gets a small bite.
 line('Payoff fishing line',[(-.85,3.2),(-1.6,1.8),(-2.0,-.5)],.02,'#f2efd6',.006,rod)
 float_ob=A['surface']('Biting float',[(-.18+.055*math.cos(i*math.tau/24),-.2+.055*math.sin(i*math.tau/24),.28) for i in range(24)],'#f95249');keys(float_ob,'location',[(1,(0,0,0)),(130,(0,0,0)),(138,(0,0,-.05)),(145,(0,0,.025)),(158,(0,0,0)),(216,(0,0,0))])
 speak(f,'biting',60);event('float_plop',138);event('whistle_tail',169)
 cap('UNITED 0–1 CITY',1,45);cap('SAMTOONS',171,216,y=.2,size=.14);cap('TEN MEN. TWO POSTS. NO POINTS.',171,216,y=.06,size=.036)

def save():
 assert sum(x['frames'] for x in EDIT)==3600
 counts={k:sum(x['frames'] for x in EDIT if x['beat']==k) for k,_ in BASE};assert counts==dict(BASE),counts
 start=1
 for row in EDIT:row['start_frame']=start;start+=row['frames']
 (OUT/'edit.json').write_text(json.dumps(EDIT,indent=2)+'\n');(OUT/'speech.json').write_text(json.dumps(SPEECH,indent=2)+'\n')
 for row in EDIT:
  s=bpy.data.scenes[row['scene']];s['Animatic start']=row['start_frame'];s.render.resolution_percentage=75;s.eevee.taa_render_samples=8
 bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'combined-animatic-v001.blend'))
 return {'shots':len(EDIT),'frames':3600,'seconds':150,'speech_cues':len(SPEECH),'file':bpy.data.filepath}
