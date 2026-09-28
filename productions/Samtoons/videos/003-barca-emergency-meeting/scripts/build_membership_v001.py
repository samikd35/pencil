"""S12 native supported acting. Run setup(), actors(), animate(), finish() visibly.
Selected drawing is converted to meshes; no whole-scene raster animation.
"""
import bpy,math,json,importlib.util,subprocess,array
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/staging-v001/membership-v001';END=312
sp=importlib.util.spec_from_file_location('s12_primitives',V/'scripts/build_consultation_v001.py');C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
M=C.M;B=M.B;n=M.n;key=C.key;visible=C.visible;at=C.at;A={};CHECK=[]
LINES=[('fan-delighted.wav',52,'BARÇA FAN: Now you know what it feels like!'),('fan-defensive.wav',230,'BARÇA FAN: That was before we hired their coach.')]

def setup():
 global S,CAM,DRAWER,INSERT,ICON
 assert not bpy.app.background
 assert not (O/'membership.blend').exists(),'Version delivered work'
 O.mkdir(parents=True,exist_ok=True)
 # New scene; the open S11 scene and any unsaved user state remain in memory.
 M.setup();S=M.s;S.name='S003_S12_Membership_v001';S.frame_end=END;CAM=S.camera
 bpy.data.batch_remove([o for o in n['col'].objects if o!=CAM]);S.render.resolution_x=1280;S.render.resolution_y=720
 B['rect']('S12 wall',-900,-430,1800,900,-130,'#708394',outline=False)
 B['shape']('S12 window light',[(-780,450),(-300,450),(360,-280),(-180,-280)],-129,'#80949f',outline=False,soft=False)
 for x in [-670,-400,-110,190,510,790]:B['stroke']('S12 wall panel',[(x,-390),(x,450)],-128,'#586c7e',1.5,soft=False)
 B['rect']('S12 chair rail',-900,-100,1800,12,-127,'#43596b',outline=False)
 B['rect']('S12 poster frame',-580,90,215,236,-120,'#24374a');B['rect']('S12 poster',-570,100,195,216,-119,'#e8e2ce',outline=False)
 for text,y,size in [('VALENCIA',277,20),('0 – 5',214,42),('BARCELONA',161,19)]:B['text']('S12 old result',text,-472,y,-118,size,'#6c4b42')
 B['rect']('S12 whiteboard edge',448,10,490,312,-120,'#27394c');B['rect']('S12 whiteboard',459,21,468,288,-119,'#e9e6d3',outline=False)
 B['text']('S12 board heading','EMERGENCY',650,257,-118,27,'#24384b');B['text']('S12 board sub','MEETING',650,216,-118,29,'#24384b')
 # The archive is part of the meeting-room right-hand furniture, between these seats.
 B['rect']('S12 archive cabinet',-93,-332,217,243,-95,'#86694e');B['rect']('S12 cabinet top',-104,-99,237,15,-93,'#b18b64')
 B['rect']('S12 lower drawer',-80,-312,191,101,-91,'#947356');B['rect']('S12 lower handle',-3,-241,40,7,-90,'#d1c4ab',outline=False)
 DRAWER=B['control']('S12 archive drawer')
 B['rect']('S12 open cavity',-79,-204,190,98,-90,'#332d2a',outline=False)
 B['shape']('S12 drawer tray',[(-81,-158),(113,-158),(140,-212),(-106,-212)],-89,'#c3a57d',DRAWER,True,False)
 B['rect']('S12 archive front',-106,-248,246,46,-88,'#a4815e',DRAWER)
 B['rect']('S12 archive label bed',-43,-237,121,25,-87,'#eee4ca',DRAWER,False);B['text']('S12 archive label','ARCHIVE',17,-231,-86,16,'#332e2a',DRAWER)
 # Place the drawer under the actual retrieval grip.
 for ob in list(n['col'].objects):
  if any(t in ob.name for t in ['archive cabinet','cabinet top','lower drawer','lower handle','open cavity']):ob.location.x-=55
 DRAWER.location.x=-55
 for x in [-252,309]:
  B['shape']('S12 chair back',[(x-123,-291),(x-130,40),(x-102,69),(x+91,69),(x+122,36),(x+127,-290)],-70,'#405364',soft=True)
  B['stroke']('S12 chair stitching',[(x-102,-250),(x-107,24),(x-88,43),(x+77,43),(x+99,23),(x+103,-250)],-69,'#5c7180',1.4,soft=False)
 # Foreground meeting table with a perspective edge, shared with earlier room treatment.
 B['shape']('S12 table',[(-900,-405),(900,-405),(785,-296),(-756,-296)],120,'#a7815d',soft=False)
 B['stroke']('S12 table edge',[(-756,-296),(785,-296)],121,'#6c503b',2,soft=False)
 B['shape']('S12 notebook',[(-480,-362),(-313,-362),(-281,-316),(-429,-316)],122,'#ebe4ce',soft=False)
 B['stroke']('S12 pen',[(-368,-340),(-296,-328)],124,'#223b50',3,soft=False)
 INSERT=B['control']('S12 card insert',parent=CAM);INSERT.location=(0,0,-110);INSERT.scale=(1,1,1)
 B['rect']('S12 insert field',-800,-450,1600,900,0,'#354654',INSERT,False)
 B['shape']('S12 insert shadow',[(-489,-242),(520,-232),(495,272),(-502,255)],1,'#253541',INSERT,False,False)
 B['rect']('S12 membership card',-480,-245,960,490,2,'#f2e6c8',INSERT)
 B['rect']('S12 card header',-480,155,960,90,3,'#273b50',INSERT,False)
 B['text']('S12 member header','FIRST MEMBER · 2020',0,183,4,43,'#f4e7c7',INSERT)
 B['rect']('S12 photo mat',-440,-193,258,306,3,'#fff6de',INSERT)
 B['rect']('S12 photo background',-428,-181,234,282,4,'#97a6a6',INSERT,False)
 B['text']('S12 card group','BARCELONA',122,70,4,29,'#263e59',INSERT)
 B['text']('S12 card score','2 – 8',133,-23,4,92,'#9e4146',INSERT)
 B['text']('S12 card opponent','BAYERN',126,-81,4,29,'#263e59',INSERT)
 B['text']('S12 card footer','SUPPORT GROUP · FOUNDING MEMBER',119,-178,4,19,'#6b5b46',INSERT)
 visible(INSERT,False,1);visible(INSERT,True,146);visible(INSERT,False,211)
 return {'scene':S.name,'frames':END}

def arm_pose(who,f):
 return at(f,[(1,1),(20,1),(25,.92),(35,.2),(43,0),(END,0)]) if who=='Fan' else at(f,[(1,0),(89,0),(108,1),(116,1),(138,0),(END,0)])

def arm_drawing(a,amount):
 """Fresh continuous contours. No source mesh warp or inherited weight field."""
 c=a['c'];fan=c['who']=='Fan';o=c['origin'];parent=a['root']
 sh=Vector((932,478) if fan else (621,607))
 el=Vector((843-2*amount,668-107*amount) if fan else (639+77*amount,679-10*amount))
 wr=Vector(c['wrist'])+Vector((90,-178) if fan else (211,108))*amount
 # Rounded elbow: two line segments joined by a quadratic corner.
 before=el.lerp(sh,.25);after=el.lerp(wr,.25)
 pts=[sh.lerp(before,i/12) for i in range(13)]
 pts += [(1-t)**2*before+2*(1-t)*t*el+t*t*after for t in [i/16 for i in range(1,17)]]
 pts += [after.lerp(wr,i/12) for i in range(1,13)]
 widths=[(44 if fan else 35)*(1-i/(len(pts)-1))+23*i/(len(pts)-1) for i in range(len(pts))]
 left=[];right=[]
 for i,pt in enumerate(pts):
  d=pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)];normal=Vector((-d.y,d.x)).normalized()
  left.append(tuple(pt+normal*widths[i]));right.append(tuple(pt-normal*widths[i]))
 import sys
 sys.path.insert(0,str(V.parents[3]/'.runtime/vector-art'))
 from shapely.geometry import Polygon,Point
 from shapely.ops import unary_union
 # Swept discs form a valid rounded elbow even when the inner offsets cross.
 pg=unary_union([Point(tuple(pt)).buffer(w,quad_segs=8) for pt,w in zip(pts,widths)])
 assert pg.is_valid and pg.geom_type=='Polygon' and pg.area>1000,(c['who'],amount,'arm fold')
 root=B['control']('S12 '+c['who']+' arm drawing',parent=parent)
 def local(pp):return [(x-o[0],o[1]-y) for x,y in pp]
 color='#23314b' if fan else '#f4ad65'
 if fan:
  # One garment silhouette owns the shoulder join, underneath retained interior art.
  torso=Polygon([(931,451),(988,425),(1178,427),(1230,852),(924,852),(916,637)])
  union=pg.union(torso);assert union.geom_type=='Polygon','disconnected shoulder'
  B['shape']('S12 connected sweater',local(list(union.exterior.coords)[:-1]),-.5,color,root,True,False)
 B['shape']('S12 continuous arm',local(list(pg.exterior.coords)[:-1]),2 if fan else -.3,color,root,False,False)
 if not fan:
  fore=unary_union([Point(tuple(pt)).buffer(w,quad_segs=8) for pt,w in zip(pts[18:],widths[18:])])
  B['shape']('S12 crossing forearm',local(list(fore.exterior.coords)[:-1]),2,color,root,False,False)
 # Open attachment boundaries: ink describes the sides, never a cap through a joint.
 segment=[]
 for pt in list(pg.exterior.coords):
  keep=(Vector(pt)-sh).length>widths[0]+3 and (Vector(pt)-wr).length>26
  if keep:segment.append(pt)
  else:
   if len(segment)>1:B['stroke']('S12 arm contour',local(segment),2.2 if fan else -.1,'#20232b' if fan else '#332b24',1.35,root,False)
   segment=[]
 if len(segment)>1:B['stroke']('S12 arm contour',local(segment),2.2 if fan else -.1,'#20232b' if fan else '#332b24',1.35,root,False)
 return root

def actors():
 global ICON
 for who,x,y,scale in [('Valencia',-260,-240,.61),('Fan',305,-241,.64)]:
  data=json.loads((V/f'assets/membership-v001/{who.lower()}.json').read_text());c=data['design'];root=B['control']('S12 '+who,(x,y,0));root.scale=(scale,)*3
  body=n['vectors']('S12 '+who+' continuous drawing',data['parts']['body'],root,c['origin'],0)
  hand=B['control']('S12 '+who+' shared hand and prop',parent=root)
  n['vectors']('S12 '+who+' grip',data['parts']['hand'],hand,c['origin'],6)
  prop=n['vectors']('S12 '+who+' carried prop',data['parts']['prop'],hand,c['origin'],4)
  if who=='Fan':
   # Complete the scarf and sweater behind the phone. This is hidden artwork, not a joint cover.
   B['shape']('S12 complete left chest',[(x-c['origin'][0],c['origin'][1]-y) for x,y in [(897,455),(959,429),(1019,433),(1057,807),(932,817),(916,644)]],-.4,'#23314b',root,False,False)
   B['shape']('S12 hidden scarf',[(x-c['origin'][0],c['origin'][1]-y) for x,y in [(991,379),(1026,424),(1053,747),(936,745),(956,500)]],-.3,'#183d74',root,False,False)
   for yy in [395,511,639]:B['shape']('S12 hidden scarf stripe',[(x-c['origin'][0],c['origin'][1]-y) for x,y in [(956,yy),(1022,yy),(1038,yy+57),(948,yy+57)]],-.2,'#a02740',root,False,False)
  else:
   B['shape']('S12 complete shirt under arm',[(x-c['origin'][0],c['origin'][1]-y) for x,y in [(344,485),(568,486),(568,745),(345,745)]],-.4,'#f4eee7',root,False,False)
   B['shape']('S12 shirt behind card',[(x-c['origin'][0],c['origin'][1]-y) for x,y in [(341,492),(483,492),(486,592),(335,591)]],-.2,'#f4eee7',root,False,False)
   # Same card identity as the insert, drawn on the carried card at source coordinates.
   pt=n['xy']((394,529),c['origin']);B['text']('S12 held card year','2020',pt.x,pt.y,5,12,'#6d4b3c',prop)
   pt=n['xy']((400,552),c['origin']);B['text']('S12 held card score','2 – 8',pt.x,pt.y,5,15,'#9b3844',prop)
  a=dict(c=c,data=data,root=root,body=body,hand=hand,prop=prop,root_y=y,rest={'neck':n['xy'](c['neck'],c['origin'])});A[who]=a;c['skin']='#f5ad64' if who=='Fan' else '#f4ad65';n['facial'](a)
  for ob in a['face'].children_recursive:
   if 'skin backing' in ob.name:
    centre=sum((v.co for v in ob.data.vertices),Vector())/len(ob.data.vertices)
    for v in ob.data.vertices:v.co=centre+(v.co-centre)*1.15
    ob.location.z=1.3
  for i,ctrl in enumerate(a['brows']):
   bpy.data.batch_remove(list(ctrl.children_recursive))
   pp=c['brows'][i];origin=[sum(x for x,y in pp)/len(pp),sum(y for x,y in pp)/len(pp)]
   B['shape']('S12 '+who+' clean brow',[(x-origin[0],origin[1]-y) for x,y in pp],0,'#32291f',ctrl,False,True)
 # The insert uses a separately clipped copy of the same source face.
 fan=A['Fan'];ICON=B['control']('S12 card portrait',(-310,-65,6),INSERT);ICON.scale=(.76,.76,.76)
 n['vectors']('S12 same fan portrait',fan['data']['parts']['portrait'],ICON,[1060,235],0)
 B['shape']('S12 portrait lip backing',[(-84,-62),(-54,-64),(-7,-60),(22,-58),(25,-84),(-15,-92),(-60,-83),(-86,-75)],1.5,fan['c']['skin'],ICON,False,True)
 for x,y in [(-68,0),(10,-14)]:B['shape']('S12 photo tear',[(x,y-12),(x-6,y-32),(x,y-39),(x+6,y-32)],4,'#8ac5d4',ICON,False,True)
 B['stroke']('S12 crying mouth',[(-68,-80),(-30,-70),(9,-81)],4,'#633c2b',2,ICON)
 visible(ICON,False,1);visible(ICON,True,146);visible(ICON,False,211)
 return {'characters':list(A),'native_vertices':{w:len(a['body'].data.vertices) for w,a in A.items()}}

def envelope(file):
 raw=subprocess.check_output(['/opt/homebrew/bin/ffmpeg','-v','error','-i',str(V/'assets/voices-s12-v001'/file),'-f','f32le','-ac','1','-ar','24000','pipe:1']);p=array.array('f');p.frombytes(raw)
 out=[math.sqrt(sum(x*x for x in p[i:i+1000])/len(p[i:i+1000])) for i in range(0,len(p),1000)];return [x/max(out) for x in out]

def animate():
 for who,a in A.items():
  drawings={}
  for f in range(1,END+1):
   amount=round(arm_pose(who,f),6)
   if amount not in drawings:drawings[amount]=arm_drawing(a,amount)
  for amount,ob in drawings.items():
   for f in range(1,END+1):visible(ob,round(arm_pose(who,f),6)==amount,f)
  if who=='Valencia':visible(a['prop'],False,1);visible(a['prop'],True,118)
 env=[(start,envelope(file),words) for file,start,words in LINES]
 for f in range(1,END+1):
  S.frame_set(f)
  # Tight opening conceals the club scarf until the phone drops and composition widens.
  width=at(f,[(1,620),(20,620),(41,1280),(END,1280)])
  camx=at(f,[(1,300),(20,300),(41,0),(END,0)]);camy=at(f,[(1,145),(20,145),(41,0),(END,0)])
  if 146<=f<=210:width=1140;camx=0;camy=0
  if f>=211:width=750;camx=290;camy=45
  CAM.location=(camx,camy,1200);CAM.data.ortho_scale=width;key(CAM,f);key(CAM.data,f,'ortho_scale')
  DRAWER.location.y=0;key(DRAWER,f)
  for who,a in A.items():
   fan=who=='Fan';amount=arm_pose(who,f)
   dx,dy=(90,-178) if fan else (211,108);a['hand'].location=(dx*amount,-dy*amount,0);key(a['hand'],f)
   CHECK.append(abs(a['hand'].location.x-dx*amount)+abs(a['hand'].location.y+dy*amount))
   bow=at(f,[(1,0),(212,0),(222,.35),(276,.35),(291,1),(END,1)]) if fan else 0
   a['root'].location.y=a['root_y']-30*bow;key(a['root'],f)
   amp=max([e[f-start] for start,e,t in env if fan and 0<=f-start<len(e)]+[0])
   label=('O' if amp>.65 else 'A' if amp>.35 else 'E') if amp>.1 else ('tight' if fan and f>=211 else 'rest')
   if fan and f in [8,9,10,11,14,15,16]:label='A'
   for name,group in a['mouths'].items():visible(group,name==label,f)
   for i,(ctrl,closed,line,top,bottom) in enumerate(a['eyes']):
    look=at(f,[(1,0),(82,0),(88,6 if fan else 8),(142,6 if fan else 8),(214,0),(224,-5 if fan else 4),(END,-5 if fan else 4)])
    ctrl.location.x=a['c']['eyes'][i]['pupil'][0]-a['c']['eyes'][i]['center'][0]+look;key(ctrl,f)
    blink=f in ([8,9,10,14,15,16,202,203,284,285] if fan else [92,93,225,226]);closed.value=int(blink);key(closed,f,'value');visible(line,blink,f)
    br=a['brows'][i];br.rotation_euler.z=math.radians(at(f,[(1,0),(83,0),(96,5 if not fan else 0),(212,5 if not fan else 0),(223,14 if fan else 5),(END,14 if fan else 5)])*(1 if i==0 else -1));key(br,f,'rotation_euler')
 for start,e,words in env:
  root=B['control']('S12 caption',parent=CAM);B['rect']('S12 caption bed',-.47,-.022,.94,.045,0,'#172d3b',root,False);B['text']('S12 caption words',words,0,-.008,.02,.018,'#f6edda',root)
  for f in range(1,END+1):
   S.frame_set(f);w=CAM.data.ortho_scale;root.location=(0,-w*.249,-100);root.scale=(w,w,w);key(root,f);key(root,f,'scale')
  visible(root,False,1);visible(root,True,start);visible(root,False,start+len(e))
 for name,f in [('Stifled laugh',8),('Phone down scarf reveal',25),('Fan laughs at Bayern',52),('Reach into established archive',89),('Card lifted',118),('Card insert',146),('Smile collapses',211),('Defensive reply',230),('Sinks into chair',280)]:S.timeline_markers.new(name,frame=f)
 return {'lines':[{'start':s,'frames':len(e)} for s,e,t in env],'insert':[146,210]}

def finish():
 # Planar ink cannot pierce foreground artwork like a bevelled 3D tube.
 for ob in S.objects:
  if ob.type=='CURVE' and ob.data.dimensions=='3D' and ob.data.bevel_depth and not ob.get('planar_ink'):
   pts=[p for sp in ob.data.splines for p in sp.points]
   if pts:
    z=pts[0].co.z;assert all(abs(p.co.z-z)<.001 for p in pts)
    for p in pts:p.co.z=0
    ob.location.z+=z;ob.scale.z=.01;ob['planar_ink']=True
 assert CHECK and max(CHECK)<.001
 for act in bpy.data.actions:
  if 'S12' not in act.name and act not in [CAM.animation_data.action,CAM.data.animation_data.action]:continue
  for layer in act.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT' if 'hide_' in fc.data_path else 'LINEAR'
 S.frame_set(69);S['scope']='S12 supported seated new fictional cast; limited art-directed planar poses, not general skeleton physics.'
 mix=O/'audio/mix-premaster.wav'
 if mix.exists():
  ed=S.sequence_editor_create()
  if not any(st.type=='SOUND' and Path(st.sound.filepath).resolve()==mix for st in ed.strips):ed.strips.new_sound('S12 authoritative preview mix',str(mix),channel=1,frame_start=1)
 S.render.use_sequencer=False
 # Write only this scene and its dependencies; keep the user's open S11 working state intact.
 bpy.data.libraries.write(str(O/'membership.blend'),{S},fake_user=True,compress=True)
 (O/'construction-check.json').write_text(json.dumps({'frames':END,'fps':24,'shared_wrist_parameter_error':max(CHECK),'construction':'Source arm and weight field discarded. Explicit continuous arm contours, connected sweater silhouette and rigid shared grip/prop. Projected drawings, not dynamics.','review':'Requires close-up visual inspection; parameter check is not a geometry-quality pass.','voice_listened_by_agent':False},indent=2)+'\n')
 return {'native':str(O/'membership.blend')}
