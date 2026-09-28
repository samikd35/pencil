# Live authoring recipe from the v019 session. Saved v020 blend is the portable editable source.
# Requires batch16, b17, build19 and finish19 live registries; not intended to run on v020 again.


# ---- acting_cast_v020.py ----
import bpy,math,json,shutil,numpy as np
from pathlib import Path
from mathutils import Vector
q=bpy.app.driver_namespace['build19'];n=q['n'];b=q['b'];lib=q['lib'];s=q['s'];V=q['V'];O=V/'artifacts/defence-v020';O.mkdir(exist_ok=True);(O/'checks').mkdir(exist_ok=True)
key=q['key'];rot=n['rotate'];smooth=q['smooth'];curves=q['curves'];bpy.context.window.scene=s
# Preserve the last candidate before touching the new-player rigs. A/Y and world stay intact.
assert s.name=='S002_defence_v019'
s.name='S002_defence_v020';q['room'].name='S002_narrator_v020'
for name in ['edit.json','audio-plan.json','captions.json','subtitles.ass','subtitles.srt']:
 p=V/'artifacts/defence-v019'/name;text=p.read_text().replace('S002_defence_v019','S002_defence_v020').replace('S002_narrator_v019','S002_narrator_v020');(O/name).write_text(text)
# Audio is unchanged; retain exactly the selected premaster rather than regenerating voices.
(O/'mix').mkdir(exist_ok=True);shutil.copy2(V/'artifacts/defence-v019/mix/mix-premaster.wav',O/'mix/mix-premaster.wav')
for name in ['render_defence','package_defence']:
 src=V/'scripts'/f'{name}_v019.py';(V/'scripts'/f'{name}_v020.py').write_text(src.read_text().replace('v019','v020'))
# Fitted landmarks, read from each complete illustration rather than a generic humanoid template.
keeper={'hip':(1346,776),'neck':(1350,604),'head':(1356,546),'Lshoulder':(1271,626),'Lelbow':(1229,679),'Lwrist':(1256,713),'Lfinger':(1297,730),'Rshoulder':(1418,625),'Relbow':(1457,673),'Rwrist':(1429,709),'Rfinger':(1394,730),'Lhip':(1306,790),'Lknee':(1295,867),'Lankle':(1257,953),'Ltoe':(1223,979),'Rhip':(1386,790),'Rknee':(1417,864),'Rankle':(1450,950),'Rtoe':(1476,978)}
defender={'hip':(981,788),'neck':(987,641),'head':(989,590),'Lshoulder':(910,665),'Lelbow':(863,720),'Lwrist':(849,779),'Lfinger':(845,805),'Rshoulder':(1034,669),'Relbow':(1075,719),'Rwrist':(1096,778),'Rfinger':(1105,805),'Lhip':(943,806),'Lknee':(896,858),'Lankle':(858,949),'Ltoe':(835,979),'Rhip':(1014,806),'Rknee':(1064,856),'Rankle':(1102,950),'Rtoe':(1133,980)}
wall_points=[
[(199,306),(202,141),(199,78),(122,175),(128,241),(179,298),(200,318),(258,173),(252,239),(210,290),(185,313),(152,330),(127,395),(109,492),(76,517),(243,330),(262,399),(278,492),(304,517)],
[(513,308),(519,141),(520,78),(452,177),(457,242),(501,297),(520,316),(573,176),(568,245),(529,298),(507,316),(468,335),(450,399),(430,494),(399,517),(558,335),(579,399),(597,494),(623,517)],
[(837,307),(835,140),(824,80),(773,178),(777,229),(852,230),(885,206),(901,174),(900,235),(824,248),(801,247),(786,331),(774,401),(753,492),(727,517),(877,333),(900,397),(923,493),(951,517)],
[(190,815),(190,650),(185,586),(120,683),(129,748),(172,797),(195,818),(259,686),(252,754),(208,803),(185,823),(151,844),(124,911),(102,1000),(72,1027),(232,844),(255,911),(277,1000),(304,1027)],
[(512,815),(510,650),(510,586),(445,688),(448,756),(491,804),(515,821),(578,687),(572,758),(531,803),(509,823),(468,844),(449,912),(430,1004),(398,1029),(558,844),(578,913),(600,1003),(629,1029)],
[(834,816),(831,649),(831,587),(774,688),(776,754),(820,805),(840,824),(903,688),(900,755),(850,804),(828,825),(790,847),(769,911),(749,1005),(719,1029),(878,847),(900,912),(929,1004),(959,1029)],
[(190,1321),(190,1159),(187,1096),(121,1192),(126,1259),(175,1310),(193,1333),(257,1190),(254,1255),(210,1311),(187,1333),(148,1350),(122,1418),(102,1498),(75,1522),(233,1350),(256,1418),(276,1498),(304,1522)],
[(510,1310),(510,1152),(505,1092),(447,1184),(450,1239),(524,1242),(572,1214),(579,1184),(580,1235),(494,1253),(458,1233),(466,1345),(446,1419),(431,1498),(401,1523),(554,1345),(578,1419),(599,1498),(627,1523)],
[(839,1321),(838,1160),(836,1098),(779,1196),(781,1261),(824,1310),(844,1333),(909,1193),(905,1256),(856,1310),(833,1333),(797,1350),(775,1418),(757,1498),(729,1522),(882,1350),(904,1418),(929,1498),(959,1522)]
]
labels=['hip','neck','head','Lshoulder','Lelbow','Lwrist','Lfinger','Rshoulder','Relbow','Rwrist','Rfinger','Lhip','Lknee','Lankle','Ltoe','Rhip','Rknee','Rankle','Rtoe']
BONES={'torso':('hip','neck'),'head':('neck','head')}
for side in 'LR':
 for lab,aa,bb in [('upperarm','shoulder','elbow'),('forearm','elbow','wrist'),('hand','wrist','finger'),('thigh','hip','knee'),('calf','knee','ankle'),('foot','ankle','toe')]:BONES[side+lab]=(side+aa,side+bb)
def fit(a,sheet,cell,pts,height):
 box=lib['sheets'][sheet][2][cell];x0,y0,x1,y1=box[:4];u=height/(y1-y0);cx=lib['LANDMARKS'][sheet]['x'][cell] if lib['LANDMARKS'][sheet]['x'] else (x0+x1)/2
 xy=lambda p:Vector(((p[0]-cx)*u,(y1-p[1])*u,0));r={k:xy(v) for k,v in pts.items()};a['rest']=r;a['fitted_pixels']=pts;a['unit']=u;a['sheet']=sheet;a['cell']=cell
 for k,p in r.items():a['C'][k].animation_data_clear();a['C'][k].location=p
 arm=a['arm'];bpy.ops.object.select_all(action='DESELECT');arm.hide_set(False);arm.select_set(True);bpy.context.view_layer.objects.active=arm;bpy.ops.object.mode_set(mode='EDIT')
 for k,(aa,bb) in BONES.items():eb=arm.data.edit_bones.get(k) or arm.data.edit_bones.new(k);eb.head=r[aa];eb.tail=r[bb]
 bpy.ops.object.mode_set(mode='OBJECT')
 for k,(aa,bb) in BONES.items():
  pb=arm.pose.bones[k]
  for co in list(pb.constraints):pb.constraints.remove(co)
  co=pb.constraints.new('COPY_LOCATION');co.target=a['C'][aa];co=pb.constraints.new('STRETCH_TO');co.target=a['C'][bb];co.rest_length=(r[bb]-r[aa]).length;co.volume='NO_VOLUME';co.bulge=0
 sk=a['skin'];sk.vertex_groups.clear();names=list(BONES);groups=[sk.vertex_groups.new(name=k) for k in names];weights=np.zeros((len(sk.data.vertices),len(names)))
 def near(p,opts):
  vals=[]
  for k in opts:
   aa,bb=[r[t] for t in BONES[k]];d=bb-aa;t=max(0,min(1,(p-aa).dot(d)/d.length_squared));vals.append(((p-aa-d*t).length,k))
  vals=sorted(vals)[:2];w=[math.exp(-(d*d-vals[0][0]**2)/.0012) for d,k in vals];return {k:v/sum(w) for (_,k),v in zip(vals,w)}
 for v in sk.data.vertices:
  p=v.co;side='L' if p.x<r['hip'].x else 'R';py=y1-p.y/u;px=cx+p.x/u
  if p.y>r['neck'].y+.05:w={'head':1}
  elif p.y>r['neck'].y-.02:
   t=smooth((p.y-r['neck'].y+.02)/.07);w={'head':t,'torso':1-t}
  elif p.y>r['hip'].y-.04:
   # Keep the torso contiguous; sleeves only own pixels outside the torso contour.
   t=max(0,min(1,(r['neck'].y-p.y)/(r['neck'].y-r['hip'].y)));left=r['Lshoulder'].x+.025+(r['Lhip'].x-.025-r['Lshoulder'].x)*t;right=r['Rshoulder'].x-.025+(r['Rhip'].x+.025-r['Rshoulder'].x)*t
   amt=smooth((left-p.x)/.045) if side=='L' else smooth((p.x-right)/.045)
   w={k:val*amt for k,val in near(p,[side+'upperarm',side+'forearm',side+'hand']).items()};w['torso']=1-amt
  else:
   w=near(p,[side+'thigh',side+'calf',side+'foot']);t=smooth((p.y-r['hip'].y+.08)/.09);w={k:val*(1-t) for k,val in w.items()};w['torso']=t
  for k,val in w.items():weights[v.index,names.index(k)]=val
 # Source-fitting and smooth joint transitions, as in accepted batch 1. Shoes remain rigid.
 grid=weights.reshape(101,61,len(names))
 for _ in range(30):grid[1:-1,1:-1]=.6*grid[1:-1,1:-1]+.1*(grid[:-2,1:-1]+grid[2:,1:-1]+grid[1:-1,:-2]+grid[1:-1,2:])
 weights/=weights.sum(1,keepdims=True)
 for v in sk.data.vertices:
  side='L' if v.co.x<r['hip'].x else 'R';shoe=smooth((r[side+'ankle'].y+.025-v.co.y)/.055)
  if shoe:weights[v.index]*=1-shoe;weights[v.index,names.index(side+'foot')]+=shoe
  for j,val in enumerate(weights[v.index]):
   if val>1e-7:groups[j].add([v.index],float(val),'REPLACE')
 assert len(arm.data.bones)==14
 return a
for a in [q['K'],q['R']]:fit(a,'football',7,keeper,1.86 if a==q['K'] else 1.83)
for a in [*q['D'],q['opp']]:fit(a,'football',6,defender,1.83 if a!=q['opp'] else 1.82)
for i,a in enumerate(q['wall']):fit(a,'wall',i,dict(zip(labels,wall_points[i])),[1.90,1.92,1.78,1.85,1.78,1.80,1.79,1.82,1.77][i])
# Preserve Saka/Gabriel's specifically corrected source weights. Their independent limbs already exist.
# Pose from whole body: planted soles, projected knees, opposing chest/head overlap.
def act(a,f,lean=0,down=0,shift=0,head=0,ua=(0,0),fa=(0,0),hand=(0,0),lift=(0,0),foot=(0,0)):
 r=a['rest'];p={k:v.copy() for k,v in r.items()};off=Vector((shift,down,0));p['hip']+=off
 for k in ['neck','Lshoulder','Rshoulder']:p[k]=p['hip']+rot(r[k]-r['hip'],lean)
 p['head']=p['neck']+rot(r['head']-r['neck'],lean+head)
 for i,side in enumerate('LR'):
  p[side+'hip']+=off
  for label,prev,ang in [('elbow','shoulder',lean+ua[i]),('wrist','elbow',lean+ua[i]+fa[i]),('finger','wrist',lean+ua[i]+fa[i]+hand[i])]:p[side+label]=p[side+prev]+rot(r[side+label]-r[side+prev],ang)
  p[side+'ankle']+=Vector((foot[i],lift[i],0));p[side+'toe']+=Vector((foot[i],lift[i],0))
  t=(r[side+'knee'].y-r[side+'hip'].y)/(r[side+'ankle'].y-r[side+'hip'].y);delta=p[side+'hip'].lerp(p[side+'ankle'],t)-r[side+'hip'].lerp(r[side+'ankle'],t);p[side+'knee']+=delta;p[side+'knee'].x+=(-1 if side=='L' else 1)*max(0,-down)*.25
 for k,v in p.items():key(a['C'][k],'location',f,v)
 return p
def beat(f,start,attack,hold,release):return smooth((f-start)/attack)*(1-smooth((f-start-attack-hold)/release))
# Track the corner; defenders prepare and then recoil after losing the header.
for f in range(1,270):
 for i,a in enumerate(q['D']):
  track=beat(f,177+i*3,10,22,10);flinch=beat(f,215+i*3,3,2,9);lost=beat(f,237+i*3,6,19,10)
  act(a,f,lean=(-.035 if i==0 else .035)*track+.045*flinch,down=-.075*track-.025*flinch,shift=(-.03 if i==0 else .03)*track,head=.10*track-.12*lost,ua=(-.12*track-.30*lost,.12*track+.30*lost),fa=(-.20*lost,.20*lost))
 # The keeper reads the cross, sets, reaches late, recoils and looks into the goal.
 setp=beat(f,183,10,26,9);reach=beat(f,219,5,4,12);lost=beat(f,244,5,12,7)
 act(q['K'],f,lean=-.12*reach+.035*lost,down=-.085*setp,shift=.09*reach,head=-.10*setp+.15*lost,ua=(.18*setp+.36*reach,-.18*setp-.26*reach),fa=(.12*reach,-.12*reach))
 # One short push across goal, then recovery; feet and travel authored together.
 hop=max(0,1-((f-227)/8)**2)*.10 if 219<f<235 else 0;travel=.36*smooth((f-219)/12);key(q['K']['root'],'location',f,(1+travel,52,hop))
# Wall keeps established planted shuffle, adds coordinated compression and eye-line response.
for i,a in enumerate(q['wall']):
 r=a['rest'];x0=(i-4)*1.05;D=(i-4)*(.70-1.05);start=400+i*2
 for f in range(392,1048):
  t=max(0,min(64,f-start));u=t/64;key(a['root'],'location',f,(x0+D*u,-51.7,0));lifts=[];offsets=[]
  for side,offset in [('L',0),('R',8)]:
   if t<offset:travel=0;lift=0
   elif t>=64:travel=D;lift=0
   else:
    cycle=int((t-offset)//16);st=offset+cycle*16;frac=max(0,min(1,(t-st)/8));old=max(0,(st-8)/64);new=min(1,(st+8)/64);travel=D*(old+(new-old)*smooth(frac));lift=.045*math.sin(math.pi*frac)
   offsets.append(-(travel-D*u));lifts.append(lift)
  squeeze=beat(f,468+i*2,6,8,12);look=beat(f,528+i*3,7,30,14);settle=beat(f,648+i*2,6,20,11);walk=math.sin(math.pi*u)
  # Clasped/crossed hands remain together: rotate chest and head, not disconnected hands.
  act(a,f,lean=.015*walk*(-1 if i<4 else 1)+(.025 if i%2 else -.025)*squeeze,down=-.024*walk-.032*squeeze,shift=.01*walk,head=(.065 if i<4 else -.065)*look+.035*settle,ua=(-.02*squeeze,.02*squeeze),lift=lifts,foot=offsets)
# Raya takes two steps out, plants, then braces to protect the people behind him.
for f in range(392,1048):
 u=smooth((f-477)/26);key(q['R']['root'],'location',f,(.35,-51.2+.85*u,0));left=.065*math.sin(math.pi*max(0,min(1,(f-477)/10)));right=.065*math.sin(math.pi*max(0,min(1,(f-491)/10)));brace=beat(f,510,9,102,12);glance=beat(f,578,6,16,9)
 act(q['R'],f,down=-.045*math.sin(math.pi*u)-.065*brace,head=-.10*glance,ua=(.25*brace,-.25*brace),fa=(.08*brace,-.08*brace),lift=(left,right))
 doubt=beat(f,521,8,18,12);giveup=beat(f,607,8,30,16)
 act(q['opp'],f,lean=.035*doubt,head=-.09*doubt+.07*giveup,ua=(-.32*doubt-.4*giveup,.32*doubt+.4*giveup),fa=(-.18*doubt,.18*doubt))
# Saka: look for the run, signal, load support leg, drive the kick, follow through.
# Retain the corrected kick contact/boot path; layer body/head/arms onto those leg keys.
for f in range(1,198):
 s.frame_set(f);a=q['S'];r=a['rest'];leg={k:a['C'][k].location.copy() for k in r if any(k.endswith(x) for x in ['hip','knee','ankle','toe'])};signal=beat(f,29,8,28,11);check=beat(f,98,7,13,9);load=beat(f,148,10,0,10);follow=beat(f,168,5,3,17)
 p=act(a,f,lean=-.045*load+.065*follow,down=-.08,shift=-.022*load,head=-.075*signal-.06*check+.065*follow,ua=(-1.4*signal-.08*load+.12*follow,.12*load-.20*follow),fa=(-.15*signal,-.12*follow))
 for k,v in leg.items():key(a['C'][k],'location',f,v)
# Gabriel's full-body preparation, arm drive, airborne tuck, header snap and landing.
for f in range(1,270):
 a=q['G'];load=beat(f,198,9,0,5);u=(f-209)/15;jump=.42*4*u*(1-u) if 0<u<1 else 0;flight=math.sin(math.pi*max(0,min(1,u)));snap=beat(f,213,4,1,7);land=beat(f,224,3,1,9);cheer=beat(f,244,6,10,9)
 key(a['root'],'location',f,(0,49.1,jump));p=act(a,f,lean=-.075*load+.105*snap,down=-.085*load-.075*land,head=-.06*load+.14*snap-.04*land,ua=(-.22*load-.42*flight-.45*cheer,.22*load+.42*flight+.45*cheer),fa=(-.18*flight-.12*cheer,.18*flight+.12*cheer),lift=(.04*flight,.055*flight))
# Expressive eye blinks on the existing complete faces, not floating replacement heads.
# Small bounded deformation retains the original eye drawing and follows the head armature.
for a in [q['S'],q['G'],q['K'],q['R'],*q['D'],q['opp'],*q['wall']]:
 sk=a['skin'];basis=sk.data.shape_keys.key_blocks['Basis'];blink=sk.data.shape_keys.key_blocks.get('Blink20') or sk.shape_key_add(name='Blink20')
 head=a['rest']['head'];neck=a['rest']['neck'];ey=head.y-.055;ex=head.x+.015
 for i,v in enumerate(basis.data):
  blink.data[i].co=v.co
  dx=abs(v.co.x-ex)/.105;dy=abs(v.co.y-ey)/.035
  if dx<1 and dy<1:blink.data[i].co.y+=(ey-v.co.y)*.80*(1-dx**4)*(1-dy**4)
 starts=[91,187] if a in [q['S'],q['G'],q['K'],*q['D']] else [557+list(q['actors']).index(a['name'])*3,672]
 blink.value=0;blink.keyframe_insert(data_path='value',frame=1)
 for st in starts:
  for f,value in [(st,0),(st+2,1),(st+4,0)]:blink.value=value;blink.keyframe_insert(data_path='value',frame=f)
 for ob in [*a['C'].values(),a['root']]:
  for fc in curves(ob):
   if fc.data_path!='scale':
    for kp in fc.keyframe_points:kp.interpolation='LINEAR'
# Refit flight to the evaluated head after changed header performance; keep source sound contacts.
ball=q['ball'];s.frame_set(168);bpy.context.view_layer.update();contact=q['S']['root'].matrix_world@q['S']['C']['Rtoe'].location;contact.z=.12
s.frame_set(217);bpy.context.view_layer.update();head=q['G']['root'].matrix_world@q['G']['C']['head'].location;head.z+=.04;end=Vector((2.2,53.15,1.15))
for f in range(1,270):
 if f<168:p=contact
 elif f<=217:u=(f-168)/49;p=contact.lerp(head,u);p.z+=1.25*4*u*(1-u)
 elif f<=238:u=(f-217)/21;p=head.lerp(end,u);p.z+=.08*math.sin(math.pi*u)
 else:u=min(1,(f-238)/18);p=end.lerp(Vector((2.2,53.45,.11)),u)
 key(ball,'location',f,p)
# Basic regression verifies independent joints and unchanged A/Y source geometry, not artistic success.
checks={}
for name,a in q['actors'].items():
 assert len(a['arm'].data.bones)==14,name
 checks[name]={'bones':len(a['arm'].data.bones),'controls':len(a['C']),'mesh':a['skin'].name,'vertices':len(a['skin'].data.vertices)}
(O/'construction-checks.json').write_text(json.dumps(checks,indent=2));bpy.app.driver_namespace['cast20']=dict(q=q,O=O,s=s,act=act,beat=beat)
for f in [55,159,168,209,217,226,253,434,490,546,596]:
 s.frame_set(f);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=f),key=lambda m:m.frame).camera;s.render.filepath=str(O/'checks'/f'acting-{f}.png');bpy.ops.render.render(write_still=True)
bpy.data.libraries.write(str(O/'batch02-v020.blend'),{s,q['room']},fake_user=True,compress=True)
result={'scene':s.name,'new_cast':16,'checks':str(O/'checks'),'native':str(O/'batch02-v020.blend')}


# ---- refine_cast_v020.py ----
import bpy,math,numpy as np
from mathutils import Vector
z=bpy.app.driver_namespace['cast20'];q=z['q'];s=z['s'];O=z['O'];key=q['key'];rot=q['n']['rotate'];smooth=q['smooth'];act=z['act'];beat=z['beat'];b=q['b'];bpy.context.window.scene=s
# Fit fingers below the shirt hem to their actual arm, never to thigh bones.
a=q['G'];r=a['rest'];sk=a['skin'];names={g.index:g.name for g in sk.vertex_groups}
for v in sk.data.vertices:
 p=v.co;side='L' if p.x<r['hip'].x else 'R';edge=r[side+'hip'].x+(-.18 if side=='L' else .18)
 t=smooth(((edge-p.x) if side=='L' else (p.x-edge))/.08)*smooth((p.y-r[side+'finger'].y+.10)/.10)
 if t>0:
  ds=[]
  for label,aa,bb in [('upperarm','shoulder','elbow'),('forearm','elbow','wrist'),('hand','wrist','finger')]:
   a0=r[side+aa];d=r[side+bb]-a0;u=max(0,min(1,(p-a0).dot(d)/d.length_squared));ds.append(((p-a0-u*d).length,side+label))
  ds=sorted(ds)[:2];ws=[math.exp(-(d*d-ds[0][0]**2)/.0016) for d,k in ds];total=sum(ws);prior={names[g.group]:g.weight for g in v.groups}
  for k,w in prior.items():sk.vertex_groups[k].add([v.index],w*(1-t),'REPLACE')
  for (_,k),w in zip(ds,ws):sk.vertex_groups[k].add([v.index],prior.get(k,0)*(1-t)+t*w/total,'REPLACE')
# Gloves and sleeves have explicit ownership from the actual source contour.
polys={
'L':[(1284,610),(1239,634),(1208,666),(1209,689),(1240,725),(1262,741),(1298,744),(1311,731),(1300,717),(1268,703),(1254,688),(1275,655)],
'R':[(1409,610),(1447,634),(1479,665),(1478,687),(1443,725),(1425,741),(1392,744),(1370,736),(1379,718),(1413,702),(1429,685),(1405,653)]}
def inside(x,y,poly):
 yes=False;j=len(poly)-1
 for i,(xi,yi) in enumerate(poly):
  xj,yj=poly[j]
  if (yi>y)!=(yj>y) and x<(xj-xi)*(y-yi)/(yj-yi)+xi:yes=not yes
  j=i
 return yes
for a in [q['K'],q['R']]:
 sk=a['skin'];r=a['rest'];unit=a['unit'];cx=q['lib']['LANDMARKS']['football']['x'][7];cy=q['lib']['sheets']['football'][2][7][3]
 for v in sk.data.vertices:
  px=cx+v.co.x/unit;py=cy-v.co.y/unit
  for side,poly in polys.items():
   if not inside(px,py,poly):continue
   ds=[]
   for label,aa,bb in [('upperarm','shoulder','elbow'),('forearm','elbow','wrist'),('hand','wrist','finger')]:
    p0=r[side+aa];d=r[side+bb]-p0;t=max(0,min(1,(v.co-p0).dot(d)/d.length_squared));ds.append(((v.co-p0-t*d).length,side+label))
   ds=sorted(ds)[:2];ww=[math.exp(-(d*d-ds[0][0]**2)/.0016) for d,k in ds]
   for vg in sk.vertex_groups:vg.remove([v.index])
   for (_,k),w in zip(ds,ww):sk.vertex_groups[k].add([v.index],w/sum(ww),'REPLACE')
# Ground Saka's second boot for his signal. The kick is a short action rather than a seven-second foot hold.
a=q['S'];r=a['rest'];l1=(r['Rknee']-r['Rhip']).length;l2=(r['Rankle']-r['Rknee']).length
s.frame_set(168);contactank=a['C']['Rankle'].location.copy();contacttoe=a['C']['Rtoe'].location.copy();ready=Vector((.26,.12,0));readytoe=ready+Vector((.17,-.06,0))
for f in range(1,169):
 s.frame_set(f);wind=beat(f,145,10,0,10);hit=smooth((f-157)/11);ank=ready.lerp(Vector((.12,.27,0)),wind).lerp(contactank,hit);hip=a['C']['Rhip'].location.copy();d=ank-hip
 if d.length>l1+l2-.003:ank=hip+d.normalized()*(l1+l2-.003)
 knee=b['ik'](hip,ank,l1,l2,hip+Vector((.3,-.2,0)));toe=readytoe+(ank-ready);toe=toe.lerp(contacttoe,hit)
 for k,v in [('Rknee',knee),('Rankle',ank),('Rtoe',toe)]:key(a['C'][k],'location',f,v)
# Give the goalie a readable reaching action with both elbows; retain shirt and body as one source.
for f in range(1,270):
 setp=beat(f,183,10,26,9);reach=beat(f,219,5,4,12);lost=beat(f,244,5,12,7)
 act(q['K'],f,lean=-.09*reach+.035*lost,down=-.065*setp,shift=.06*reach,head=-.10*setp+.15*lost,ua=(.12*setp+.50*reach,-.12*setp-.50*reach),fa=(.08*reach,-.08*reach))
for f in range(392,1048):
 u=smooth((f-477)/26);left=.055*math.sin(math.pi*max(0,min(1,(f-477)/10)));right=.055*math.sin(math.pi*max(0,min(1,(f-491)/10)));brace=beat(f,510,9,102,12);glance=beat(f,578,6,16,9)
 act(q['R'],f,down=-.025*math.sin(math.pi*u)-.025*brace,head=-.10*glance,ua=(.16*brace,-.16*brace),fa=(.04*brace,-.04*brace),lift=(left,right))
for f in [55,159,168,209,217,226,253,490,546,596]:
 s.frame_set(f);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=f),key=lambda m:m.frame).camera;s.render.filepath=str(O/'checks'/f'refined-{f}.png');bpy.ops.render.render(write_still=True)
bpy.data.libraries.write(str(O/'batch02-v020.blend'),{s,q['room']},fake_user=True,compress=True)
result={'corrected':'hand ownership and second planted boot','native':str(O/'batch02-v020.blend')}


# ---- contact_cast_v020.py ----
import bpy,math
z=bpy.app.driver_namespace['cast20'];q=z['q'];s=z['s'];O=z['O'];act=z['act'];beat=z['beat'];key=q['key'];smooth=q['smooth'];bpy.context.window.scene=s
a=q['G'];r=a['rest'];sk=a['skin']
for v in sk.data.vertices:
 side='L' if v.co.x<r['hip'].x else 'R';outer=v.co.x<-.47 if side=='L' else v.co.x>.40
 if outer and r[side+'finger'].y-.17<v.co.y<r[side+'wrist'].y+.055:
  for vg in sk.vertex_groups:vg.remove([v.index])
  sk.vertex_groups[side+'hand'].add([v.index],1,'REPLACE')
# Opponent's delayed save spreads gloves towards the flight, rather than clasping them.
for f in range(1,270):
 setp=beat(f,183,10,26,9);reach=beat(f,219,5,4,12);lost=beat(f,244,5,12,7)
 act(q['K'],f,lean=-.08*reach+.035*lost,down=-.055*setp,shift=.06*reach,head=-.10*setp+.15*lost,ua=(-.08*setp-.65*reach,.08*setp+.65*reach),fa=(-.65*reach,.65*reach))
for f in range(392,1048):
 u=smooth((f-477)/26);left=.055*math.sin(math.pi*max(0,min(1,(f-477)/10)));right=.055*math.sin(math.pi*max(0,min(1,(f-491)/10)));brace=beat(f,510,9,102,12);glance=beat(f,578,6,16,9)
 act(q['R'],f,down=-.025*math.sin(math.pi*u)-.025*brace,head=-.10*glance,ua=(-.20*brace,.20*brace),fa=(-.24*brace,.24*brace),lift=(left,right))
for f in [217,226,546]:
 s.frame_set(f);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=f),key=lambda m:m.frame).camera;s.render.filepath=str(O/'checks'/f'ownership-{f}.png');bpy.ops.render.render(write_still=True)
result={'checked':[217,226,546]}


# ---- layers_cast_v020.py ----
"""Cut folded arms at their source contours; overlap on a drawn torso backing.
A continuous rectangular skin cannot reveal cloth hidden under painted gloves.
"""
import bpy,math,numpy as np
from mathutils import Vector
z=bpy.app.driver_namespace['cast20'];q=z['q'];s=z['s'];O=z['O'];key=q['key'];smooth=q['smooth'];bpy.context.window.scene=s
POLYS={
'keeper':{
'L':[(1280,609),(1242,630),(1205,665),(1205,690),(1233,725),(1255,744),(1279,758),(1294,752),(1309,740),(1315,724),(1304,712),(1284,710),(1269,715),(1253,697),(1251,681),(1280,651)],
'R':[(1410,610),(1448,630),(1484,665),(1484,689),(1448,730),(1424,746),(1395,755),(1383,756),(1369,745),(1365,733),(1372,719),(1387,710),(1410,713),(1426,696),(1434,680),(1406,651)]},
'gabriel':{
'L':[(1300,135),(1271,151),(1241,191),(1217,231),(1183,249),(1170,264),(1172,282),(1181,286),(1192,271),(1208,269),(1234,249),(1256,227),(1283,193),(1318,170)],
'R':[(1428,132),(1450,164),(1456,191),(1481,238),(1517,260),(1526,280),(1518,294),(1508,288),(1495,279),(1490,270),(1467,252),(1440,218),(1420,190),(1412,171)]}}
def mask_poly(poly,X,Y):
 inside=np.zeros(X.shape,bool);j=len(poly)-1
 for i,(xi,yi) in enumerate(poly):
  xj,yj=poly[j];inside^=((yi>Y)!=(yj>Y))&(X<(xj-xi)*(Y-yi)/(yj-yi+1e-10)+xi);j=i
 return inside
X,Y=np.meshgrid(np.arange(1536)+.5,np.arange(1024)+.5)
for a,kind,cell,height in [(q['K'],'keeper',7,1.86),(q['R'],'keeper',7,1.83),(q['G'],'gabriel',3,1.90)]:
 sk=a['skin'];r=a['rest'];box=q['lib']['sheets']['football'][2][cell];unit=height/(box[3]-box[1]);cx=q['lib']['LANDMARKS']['football']['x'][cell];cy=box[3];regions={side:mask_poly(poly,X,Y) for side,poly in POLYS[kind].items()};joined=regions['L']|regions['R']
 def masked_material(source,label,mask):
  im=bpy.data.images.new(a['name']+' '+label+' source contour',width=1536,height=1024);im.colorspace_settings.name='Non-Color';pixels=np.ones((1024,1536,4),np.float32);pixels[:,:,:3]=mask[::-1,:,None];im.pixels.foreach_set(pixels.ravel());im.pack()
  mat=source.copy();mat.name=a['name']+' '+label;ns=mat.node_tree.nodes;ls=mat.node_tree.links;out=next(n for n in ns if n.type=='OUTPUT_MATERIAL');up=out.inputs['Surface'].links[0].from_socket;tex=ns.new('ShaderNodeTexImage');tex.image=im;tex.interpolation='Linear';mix=ns.new('ShaderNodeMixShader');tr=ns.new('ShaderNodeBsdfTransparent');ls.new(tex.outputs['Color'],mix.inputs[0]);ls.new(tr.outputs[0],mix.inputs[1]);ls.new(up,mix.inputs[2]);ls.new(mix.outputs[0],out.inputs[0]);return mat
 source=sk.data.materials[0];sk.data.materials[0]=masked_material(source,'body without overpainted arms',~joined)
 # Main cloth now follows torso/legs only; arm contours are their own articulated layers.
 for v in sk.data.vertices:
  ws={sk.vertex_groups[g.group].name:g.weight for g in v.groups};removed=sum(w for k,w in ws.items() if k.endswith(('upperarm','forearm','hand')))
  if removed:
   for k in ws:
    if k.endswith(('upperarm','forearm','hand')):sk.vertex_groups[k].remove([v.index])
   side='L' if v.co.x<r['hip'].x else 'R';name='torso' if v.co.y>r['hip'].y-.07 else side+'thigh';sk.vertex_groups[name].add([v.index],ws.get(name,0)+removed,'REPLACE')
 # Native filled cloth behind the source's former hand overlap. It shares torso bone.
 if kind=='keeper':
  outline=[(1277,626),(1340,611),(1411,626),(1407,675),(1405,705),(1423,770),(1350,779),(1268,770),(1285,705),(1282,675)]
  pts=[((x-cx)*unit,(cy-y)*unit,-.004) for x,y in outline];me=bpy.data.meshes.new(a['name']+' hidden cloth backing');me.from_pydata(pts,[],[list(range(len(pts)))]);ob=bpy.data.objects.new(me.name,me);s.collection.objects.link(ob);ob.parent=a['root'];me.materials.append(q['mat']('#f7e92d' if a==q['R'] else '#73a6e8'));vg=ob.vertex_groups.new(name='torso');vg.add(list(range(len(pts))),1,'REPLACE');mod=ob.modifiers.new('Same torso','ARMATURE');mod.object=a['arm']
 for side,mask in regions.items():
  ob=sk.copy();ob.data=sk.data.copy();ob.name=a['name']+' articulated '+side+' sleeve forearm glove';ob.animation_data_clear();s.collection.objects.link(ob);ob.parent=a['root'];ob.data.materials[0]=masked_material(source,side+' articulated arm',mask);ob.vertex_groups.clear();groups={k:ob.vertex_groups.new(name=side+k) for k in ['upperarm','forearm','hand']};ob.location.z=.004
  for v in ob.data.vertices:
   p=v.co;ds=[]
   for lab,aa,bb in [('upperarm','shoulder','elbow'),('forearm','elbow','wrist'),('hand','wrist','finger')]:
    start=r[side+aa];d=r[side+bb]-start;t=max(0,min(1,(p-start).dot(d)/d.length_squared));ds.append(((p-start-t*d).length,lab))
   # Preserve the complete glove/fingers rigidly; blend only the actual wrist joint.
   if p.y<r[side+'wrist'].y-.018:weights={'hand':1}
   else:
    ds=sorted(ds)[:2];ws=[math.exp(-(d*d-ds[0][0]**2)/.0013) for d,k in ds];weights={k:w/sum(ws) for (_,k),w in zip(ds,ws)}
   for k,w in weights.items():groups[k].add([v.index],w,'REPLACE')
  ob['construction']='Source-matched layered drawing with fitted joints; original whole face and kit retained'
for f in [209,217,226,253,546]:
 s.frame_set(f);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=f),key=lambda m:m.frame).camera;s.render.filepath=str(O/'checks'/f'layers-{f}.png');bpy.ops.render.render(write_still=True)
bpy.data.libraries.write(str(O/'batch02-v020.blend'),{s,q['room']},fake_user=True,compress=True)
result={'layered_characters':['Gabriel','Raya','opposition goalkeeper'],'unchanged':['Arteta','Gyokeres','audio','environment']}


# ---- trim_cast_v020.py ----
import bpy,bmesh,numpy as np
z=bpy.app.driver_namespace['cast20'];q=z['q'];s=z['s'];O=z['O'];bpy.context.window.scene=s
X,Y=np.meshgrid(np.arange(1536)+.5,np.arange(1024)+.5)
for a,kind,cell,height in [(q['K'],'keeper',7,1.86),(q['R'],'keeper',7,1.83),(q['G'],'gabriel',3,1.90)]:
 if kind=='gabriel':
  left=np.interp(Y,[125,160,200,240,275,310],[1291,1310,1280,1245,1220,1220]);right=np.interp(Y,[125,160,200,240,275,310],[1420,1417,1440,1470,1484,1484]);masks={'L':(Y>130)&(Y<304)&(X<left),'R':(Y>130)&(Y<304)&(X>right)}
 else:
  left=np.interp(Y,[605,650,700,712,745,758,770],[1280,1280,1287,1315,1317,1289,1263]);right=np.interp(Y,[605,650,700,712,745,758,770],[1410,1408,1407,1362,1361,1384,1420]);masks={'L':(Y>605)&(Y<768)&(X<left),'R':(Y>605)&(Y<768)&(X>right)}
 joined=masks['L']|masks['R'];allm={'body without overpainted arms':~joined,'L articulated arm':masks['L'],'R articulated arm':masks['R']}
 for label,mask in allm.items():
  im=bpy.data.images[a['name']+' '+label+' source contour'];pixels=np.ones((1024,1536,4),np.float32);pixels[:,:,:3]=mask[::-1,:,None];im.pixels.foreach_set(pixels.ravel());im.pack()
  ob=a['skin'] if label.startswith('body') else bpy.data.objects[a['name']+' articulated '+label[0]+' sleeve forearm glove']
  # Remove transparent rectangles outside the owned drawing. This prevents layered alpha-depth artifacts.
  bm=bmesh.new();bm.from_mesh(ob.data);uv=bm.loops.layers.uv.active;remove=[]
  for face in bm.faces:
   samples=[l[uv].uv for l in face.loops];valid=False
   for pt in samples:
    px=min(1535,max(0,int(pt.x*1536)));py=min(1023,max(0,int((1-pt.y)*1024)));valid|=bool(mask[py,px])
   if not valid:remove.append(face)
  bmesh.ops.delete(bm,geom=remove,context='FACES');bm.to_mesh(ob.data);bm.free()
# Only soft body motion is needed after contact; the corrected isolated arm has room to articulate.
for f in [209,217,226,253,546]:
 s.frame_set(f);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=f),key=lambda m:m.frame).camera;s.render.filepath=str(O/'checks'/f'trimmed-{f}.png');bpy.ops.render.render(write_still=True)
bpy.data.libraries.write(str(O/'batch02-v020.blend'),{s,q['room']},fake_user=True,compress=True)
result={'trimmed':True}


# ---- defenders_cast_v020.py ----
import bpy,math,numpy as np
z=bpy.app.driver_namespace['cast20'];q=z['q'];s=z['s'];O=z['O'];bpy.context.window.scene=s
for a in [*q['D'],q['opp']]:
 sk=a['skin'];r=a['rest'];u=a['unit'];cx=q['lib']['LANDMARKS']['football']['x'][6];cy=q['lib']['sheets']['football'][2][6][3]
 for v in sk.data.vertices:
  px=cx+v.co.x/u;py=cy-v.co.y/u;side='L' if px<981 else 'R';edge=float(np.interp(py,[645,690,735,775,810,840],[913,906,884,875,870,864] if side=='L' else [1026,1045,1070,1080,1088,1090]));isarm=645<py<840 and (px<edge if side=='L' else px>edge)
  prior={sk.vertex_groups[g.group].name:g.weight for g in v.groups}
  if isarm:
   for vg in sk.vertex_groups:vg.remove([v.index])
   if py>774:weights={side+'hand':1}
   else:
    ds=[]
    for lab,aa,bb in [('upperarm','shoulder','elbow'),('forearm','elbow','wrist'),('hand','wrist','finger')]:
     start=r[side+aa];d=r[side+bb]-start;t=max(0,min(1,(v.co-start).dot(d)/d.length_squared));ds.append(((v.co-start-t*d).length,side+lab))
    ds=sorted(ds)[:2];ws=[math.exp(-(d*d-ds[0][0]**2)/.0016) for d,k in ds];weights={k:w/sum(ws) for (_,k),w in zip(ds,ws)}
   for name,w in weights.items():sk.vertex_groups[name].add([v.index],w,'REPLACE')
  elif py>735:
   removed=sum(w for k,w in prior.items() if k.endswith(('upperarm','forearm','hand')))
   for k in prior:
    if k.endswith(('upperarm','forearm','hand')):sk.vertex_groups[k].remove([v.index])
   if removed:
    name='torso' if py<790 else side+'thigh';sk.vertex_groups[name].add([v.index],prior.get(name,0)+removed,'REPLACE')
for f in [217,237,253]:
 s.frame_set(f);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=f),key=lambda m:m.frame).camera;s.render.filepath=str(O/'checks'/f'defenders-{f}.png');bpy.ops.render.render(write_still=True)
bpy.data.libraries.write(str(O/'batch02-v020.blend'),{s,q['room']},fake_user=True,compress=True)
result={'checked':'both defenders and opposing attacker'}


# ---- defender_layers_v020.py ----
import bpy,math,numpy as np
z=bpy.app.driver_namespace['cast20'];q=z['q'];s=z['s'];O=z['O'];bpy.context.window.scene=s
POLYS={'defender':{'L':[(916,649),(890,670),(863,707),(842,736),(829,771),(822,807),(828,827),(840,825),(845,816),(856,823),(866,810),(864,791),(879,754),(907,716),(935,681)],'R':[(1031,650),(1064,688),(1088,730),(1109,769),(1127,793),(1127,817),(1115,827),(1107,811),(1100,807),(1098,826),(1084,821),(1079,798),(1071,780),(1050,744),(1028,708),(1010,677)]}}
def mask_poly(poly,X,Y):
 inside=np.zeros(X.shape,bool);j=len(poly)-1
 for i,(xi,yi) in enumerate(poly):
  xj,yj=poly[j];inside^=((yi>Y)!=(yj>Y))&(X<(xj-xi)*(Y-yi)/(yj-yi+1e-10)+xi);j=i
 return inside
X,Y=np.meshgrid(np.arange(1536)+.5,np.arange(1024)+.5)
for a,kind,cell,height in [(a,'defender',6,1.83 if a!=q['opp'] else 1.82) for a in [*q['D'],q['opp']]]:
 sk=a['skin'];r=a['rest'];box=q['lib']['sheets']['football'][2][cell];unit=height/(box[3]-box[1]);cx=q['lib']['LANDMARKS']['football']['x'][cell];cy=box[3];regions={side:mask_poly(poly,X,Y) for side,poly in POLYS[kind].items()};joined=regions['L']|regions['R']
 def masked_material(source,label,mask):
  im=bpy.data.images.new(a['name']+' '+label+' source contour',width=1536,height=1024);im.colorspace_settings.name='Non-Color';pixels=np.ones((1024,1536,4),np.float32);pixels[:,:,:3]=mask[::-1,:,None];im.pixels.foreach_set(pixels.ravel());im.pack()
  mat=source.copy();mat.name=a['name']+' '+label;ns=mat.node_tree.nodes;ls=mat.node_tree.links;out=next(n for n in ns if n.type=='OUTPUT_MATERIAL');up=out.inputs['Surface'].links[0].from_socket;tex=ns.new('ShaderNodeTexImage');tex.image=im;tex.interpolation='Linear';mix=ns.new('ShaderNodeMixShader');tr=ns.new('ShaderNodeBsdfTransparent');ls.new(tex.outputs['Color'],mix.inputs[0]);ls.new(tr.outputs[0],mix.inputs[1]);ls.new(up,mix.inputs[2]);ls.new(mix.outputs[0],out.inputs[0]);return mat
 source=sk.data.materials[0];sk.data.materials[0]=masked_material(source,'body without overpainted arms',~joined)
 # Main cloth now follows torso/legs only; arm contours are their own articulated layers.
 for v in sk.data.vertices:
  ws={sk.vertex_groups[g.group].name:g.weight for g in v.groups};removed=sum(w for k,w in ws.items() if k.endswith(('upperarm','forearm','hand')))
  if removed:
   for k in ws:
    if k.endswith(('upperarm','forearm','hand')):sk.vertex_groups[k].remove([v.index])
   side='L' if v.co.x<r['hip'].x else 'R';name='torso' if v.co.y>r['hip'].y-.07 else side+'thigh';sk.vertex_groups[name].add([v.index],ws.get(name,0)+removed,'REPLACE')
 # Native filled cloth behind the source's former hand overlap. It shares torso bone.
 if kind=='keeper':
  outline=[(1277,626),(1340,611),(1411,626),(1407,675),(1405,705),(1423,770),(1350,779),(1268,770),(1285,705),(1282,675)]
  pts=[((x-cx)*unit,(cy-y)*unit,-.004) for x,y in outline];me=bpy.data.meshes.new(a['name']+' hidden cloth backing');me.from_pydata(pts,[],[list(range(len(pts)))]);ob=bpy.data.objects.new(me.name,me);s.collection.objects.link(ob);ob.parent=a['root'];me.materials.append(q['mat']('#f7e92d' if a==q['R'] else '#73a6e8'));vg=ob.vertex_groups.new(name='torso');vg.add(list(range(len(pts))),1,'REPLACE');mod=ob.modifiers.new('Same torso','ARMATURE');mod.object=a['arm']
 for side,mask in regions.items():
  ob=sk.copy();ob.data=sk.data.copy();ob.name=a['name']+' articulated '+side+' sleeve forearm glove';ob.animation_data_clear();s.collection.objects.link(ob);ob.parent=a['root'];ob.data.materials[0]=masked_material(source,side+' articulated arm',mask);ob.vertex_groups.clear();groups={k:ob.vertex_groups.new(name=side+k) for k in ['upperarm','forearm','hand']};ob.location.z=.004
  for v in ob.data.vertices:
   p=v.co;ds=[]
   for lab,aa,bb in [('upperarm','shoulder','elbow'),('forearm','elbow','wrist'),('hand','wrist','finger')]:
    start=r[side+aa];d=r[side+bb]-start;t=max(0,min(1,(p-start).dot(d)/d.length_squared));ds.append(((p-start-t*d).length,lab))
   # Preserve the complete glove/fingers rigidly; blend only the actual wrist joint.
   if p.y<r[side+'wrist'].y-.018:weights={'hand':1}
   else:
    ds=sorted(ds)[:2];ws=[math.exp(-(d*d-ds[0][0]**2)/.0013) for d,k in ds];weights={k:w/sum(ws) for (_,k),w in zip(ds,ws)}
   for k,w in weights.items():groups[k].add([v.index],w,'REPLACE')
  ob['construction']='Source-matched layered drawing with fitted joints; original whole face and kit retained'
for f in [209,217,226,253,546]:
 s.frame_set(f);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=f),key=lambda m:m.frame).camera;s.render.filepath=str(O/'checks'/f'layers-{f}.png');bpy.ops.render.render(write_still=True)
bpy.data.libraries.write(str(O/'batch02-v020.blend'),{s,q['room']},fake_user=True,compress=True)
result={'layered_characters':['Gabriel','Raya','opposition goalkeeper'],'unchanged':['Arteta','Gyokeres','audio','environment']}

# Final contour calibration and sleeve overlap from the live review.
import bpy,math,json,numpy as np,bmesh
z=bpy.app.driver_namespace['cast20'];q=z['q'];s=z['s'];O=z['O'];bpy.context.window.scene=s
X,Y=np.meshgrid(np.arange(1536)+.5,np.arange(1024)+.5)
left=np.interp(Y,[125,160,200,240,275,310],[1291,1310,1290,1285,1240,1220]);right=np.interp(Y,[125,160,200,240,275,310],[1420,1417,1416,1420,1460,1484]);masks={'L':(Y>130)&(Y<304)&(X<left),'R':(Y>130)&(Y<304)&(X>right)}
for label,mask in [('body without overpainted arms',~(masks['L']|masks['R'])),('L articulated arm',masks['L']),('R articulated arm',masks['R'])]:
 im=bpy.data.images['Gabriel '+label+' source contour'];pixels=np.ones((1024,1536,4),np.float32);pixels[:,:,:3]=mask[::-1,:,None];im.pixels.foreach_set(pixels.ravel());im.pack()
for a in [*q['D'],q['opp']]:
 masks={}
 for side in 'LR':
  im=bpy.data.images[a['name']+' '+side+' articulated arm source contour'];px=np.empty(1536*1024*4,np.float32);im.pixels.foreach_get(px);mask=px.reshape(1024,1536,4)[:,:,0]>.5
  for i in range(5):mask=mask|np.roll(mask,1,0)|np.roll(mask,-1,0)|np.roll(mask,1,1)|np.roll(mask,-1,1)
  masks[side]=mask
 for label,mask in [('body without overpainted arms',~(masks['L']|masks['R'])),('L articulated arm',masks['L']),('R articulated arm',masks['R'])]:
  im=bpy.data.images[a['name']+' '+label+' source contour'];px=np.ones((1024,1536,4),np.float32);px[:,:,:3]=mask[:,:,None];im.pixels.foreach_set(px.ravel());im.pack();ob=a['skin'] if label.startswith('body') else bpy.data.objects[a['name']+' articulated '+label[0]+' sleeve forearm glove'];bm=bmesh.new();bm.from_mesh(ob.data);uv=bm.loops.layers.uv.active;bad=[]
  for face in bm.faces:
   if not any(mask[min(1023,max(0,int(l[uv].uv.y*1024))),min(1535,max(0,int(l[uv].uv.x*1536)))] for l in face.loops):bad.append(face)
  bmesh.ops.delete(bm,geom=bad,context='FACES');bm.to_mesh(ob.data);bm.free()
 u=a['unit'];cx=q['lib']['LANDMARKS']['football']['x'][6];cy=986;poly=[(913,657),(944,644),(977,642),(1016,649),(1037,678),(1032,733),(1050,790),(997,800),(910,792),(911,731)];me=bpy.data.meshes.new(a['name']+' continuous kit backing');me.from_pydata([((x-cx)*u,(cy-y)*u,-.003) for x,y in poly],[],[list(range(len(poly)))]);ob=bpy.data.objects.new(me.name,me);s.collection.objects.link(ob);ob.parent=a['root'];me.materials.append(q['mat']('#0753b8'));vg=ob.vertex_groups.new(name='torso');vg.add(list(range(len(poly))),1,'REPLACE');mod=ob.modifiers.new('Same fitted chest','ARMATURE');mod.object=a['arm']
for a in [q['G'],*q['D'],q['opp']]:
 for side in 'LR':
  center=a['rest'][side+'shoulder'];me=bpy.data.meshes.new(a['name']+' sleeve overlap '+side);pts=[(center.x+.075*math.cos(i*math.tau/24),center.y+.085*math.sin(i*math.tau/24),.002) for i in range(24)];me.from_pydata(pts,[],[list(range(24))]);ob=bpy.data.objects.new(me.name,me);s.collection.objects.link(ob);ob.parent=a['root'];me.materials.append(q['mat']('#f5f3ee' if a==q['G'] else '#0958b8'));vg=ob.vertex_groups.new(name=side+'upperarm');vg.add(list(range(24)),1,'REPLACE');mod=ob.modifiers.new('Same upper arm','ARMATURE');mod.object=a['arm']
for a in q['actors'].values():
 keys=a['skin'].data.shape_keys
 if keys and 'Blink20' in keys.key_blocks:
  keys.key_blocks['Blink20'].value=0
  for fc in q['curves'](keys):
   if 'Blink20' in fc.data_path:
    for kp in fc.keyframe_points:kp.co.y=0
(O/'cast.json').write_text(json.dumps({name:{'root':a['root'].name,'skin':a['skin'].name,'armature':a['arm'].name,'rest':{k:list(v) for k,v in a['rest'].items()},'controls':{k:v.name for k,v in a['C'].items()}} for name,a in q['actors'].items()},indent=2))
s.frame_set(55);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=55),key=lambda m:m.frame).camera
bpy.data.libraries.write(str(O/'batch02-v020.blend'),{s,q['room']},fake_user=True,compress=True)

# Encoded-frame contact correction: accelerate the forward stroke into the selected sound event.
from mathutils import Vector
s.frame_set(157);a=q['S'];r=a['rest'];start={k:a['C'][k].location.copy() for k in ['Rankle','Rtoe']};s.frame_set(168);end={k:a['C'][k].location.copy() for k in start};l1=(r['Rknee']-r['Rhip']).length;l2=(r['Rankle']-r['Rknee']).length
for f in range(158,169):
 s.frame_set(f);u=((f-157)/11)**2;p={k:start[k].lerp(end[k],u) for k in start};hip=a['C']['Rhip'].location.copy();p['Rknee']=q['b']['ik'](hip,p['Rankle'],l1,l2,hip+Vector((.3,-.2,0)))
 for k,v in p.items():q['key'](a['C'][k],'location',f,v)
s.frame_set(168);bpy.context.view_layer.update();contact=a['root'].matrix_world@a['C']['Rtoe'].location;contact.x+=.085;contact.z=.12;s.frame_set(217);bpy.context.view_layer.update();head=q['G']['root'].matrix_world@q['G']['C']['head'].location;head.z+=.04
for f in range(1,218):
 if f<168:p=contact
 else:u=(f-168)/49;p=contact.lerp(head,u);p.z+=1.25*4*u*(1-u)
 q['key'](q['ball'],'location',f,p)
rows=[]
for f in range(158,169):
 s.frame_set(f);bpy.context.view_layer.update();toe=a['root'].matrix_world@a['C']['Rtoe'].location;rows.append({'frame':f,'toe_ball_m':(toe-q['ball'].location).length})
assert all(row['toe_ball_m']>.11 for row in rows[:-1]),rows
(O/'kick-contact-check.json').write_text(json.dumps({'ball_radius_m':.11,'rows':rows,'release_frame':168,'sound_event_frame':168},indent=2))
bpy.data.libraries.write(str(O/'batch02-v020.blend'),{s,q['room']},fake_user=True,compress=True)
