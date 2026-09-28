"""Next chronological batch: fitted native rigs in one dimensional stadium."""
import bpy,math,json,ast,copy
from pathlib import Path
from mathutils import Vector
import numpy as np
V=Path(__file__).resolve().parents[1];O=V/'artifacts/defence-v019';n=bpy.app.driver_namespace['batch16'];b=bpy.app.driver_namespace['b17'];lib=b['TRAINCAST']['defender_library'];curves=n['curves'];mat=b['mat'];smooth=n['smooth']
assert 'S002_defence_v019' not in bpy.data.scenes
s=bpy.data.scenes.new('S002_defence_v019');bpy.context.window.scene=s;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=24;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_end=1047;s.view_settings.view_transform='Standard';s.view_settings.look='None';s.render.use_sequencer=False
s.world=bpy.data.worlds.new('v019 sky');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.42,.64,.76,1)
env=bpy.data.collections.new('Samtoons match stadium v019');s.collection.children.link(env)
p=V.parent/'001-manchester-derby-2026-09-13/scripts/build_option_a.py';tree=ast.parse(p.read_text());e=dict(bpy=bpy,math=math,Vector=Vector,col=env,mat=mat);exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in ['surface','tube']],type_ignores=[]),str(p),'exec'),e);surface,tube=e['surface'],e['tube']
def key(ob,path,f,val):setattr(ob,path,val);ob.keyframe_insert(data_path=path,frame=f)
def linear(ob):
 for fc in curves(ob):
  for k in fc.keyframe_points:k.interpolation='LINEAR'
def text(body,loc,size=.4,parent=None,color='#fff9e6'):
 d=bpy.data.curves.new('v019 '+body,'FONT');d.body=body;d.size=size;d.align_x='CENTER';d.materials.append(mat(color));o=bpy.data.objects.new(d.name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler.x=math.pi/2;o.parent=parent;return o
def camera(name,f,loc,target,lens=45):
 d=bpy.data.cameras.new(name);d.lens=lens;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();m=s.timeline_markers.new(name,frame=f);m.camera=o;return o
def show(root,a,z):
 scale=tuple(root.scale)
 for f,v in [(1,(0,0,0)),(a,scale),(z+1,(0,0,0))]:key(root,'scale',f,v)
 for fc in curves(root):
  if fc.data_path=='scale':
   for k in fc.keyframe_points:k.interpolation='CONSTANT'
# Full pitch and two goals establish which end is being attacked/defended.
surface('v019 grass run-off',[(-44,-63,-.01),(44,-63,-.01),(44,63,-.01),(-44,63,-.01)],'#56884c')
surface('v019 pitch',[(-34,-52.5,0),(34,-52.5,0),(34,52.5,0),(-34,52.5,0)],'#72a65c')
for y in np.arange(-52.5,52.5,10):surface('v019 mowing stripe',[(-34,y,.002),(34,y,.002),(34,min(y+5,52.5),.002),(-34,min(y+5,52.5),.002)],'#80b468')
tube('v019 boundary',[(-34,-52.5,.015),(34,-52.5,.015),(34,52.5,.015),(-34,52.5,.015),(-34,-52.5,.015)],'#fff8df',.035);tube('v019 halfway',[(-34,0,.016),(34,0,.016)],'#fff8df',.035)
tube('v019 centre circle',[(9.15*math.cos(t),9.15*math.sin(t),.016) for t in np.linspace(0,math.tau,97)],'#fff8df',.035)
for sign in [-1,1]:
 y=sign*52.5;depth=sign*2
 for half,dist in [(9.16,5.5),(20.16,16.5)]:tube('v019 penalty area',[(-half,y,.016),(-half,y-sign*dist,.016),(half,y-sign*dist,.016),(half,y,.016)],'#fff8df',.035)
 tube('v019 goal front',[(-3.66,y,0),(-3.66,y,2.44),(3.66,y,2.44),(3.66,y,0)],'#fffbed',.06)
 for x in [-3.66,3.66]:tube('v019 goal depth',[(x,y,2.44),(x,y+depth,2.44),(x,y+depth,0),(x,y,0)],'#dedfcd',.035)
 for x in np.linspace(-3.66,3.66,31):tube('v019 net strand',[(x,y,2.44),(x,y+depth,2.44),(x,y+depth,0)],'#d2d8c6',.006)
 for z in np.linspace(0,2.44,12):tube('v019 net row',[(-3.66,y,z),(-3.66,y+depth,z),(3.66,y+depth,z),(3.66,y,z)],'#d2d8c6',.006)
 for x in [-34,34]:
  tube('v019 corner flag',[(x,y,0),(x,y,1.5)],'#fff8df',.025);surface('v019 red flag',[(x,y,1.5),(x+.45,y,1.34),(x,y,1.13)],'#cc3645')
  tube('v019 corner arc',[(x+(-1 if x>0 else 1)*math.cos(t),y-sign*math.sin(t),.019) for t in np.linspace(0,math.pi/2,20)],'#fff8df',.027)
 # Layered stands and dense drawn spectators, not an empty training backdrop.
 for tier in range(3):
  yy=sign*(59+tier*3);z=tier*2.0+.6
  surface('v019 stand tier',[(-46,yy,z),(46,yy,z),(46,yy+sign*3,z+1.9),(-46,yy+sign*3,z+1.9)],'#536778' if tier%2 else '#697b89')
  for row in range(4):
   pts=[];faces=[]
   for i in range(145):
    x=-45+i*.63+(row%2)*.25;cy=yy+sign*(.45+row*.6);cz=z+.45+row*.39;idx=len(pts)
    pts.extend([(x+.105*math.cos(t),cy,cz+.13*math.sin(t)) for t in np.linspace(0,math.tau,9)[:-1]]);faces.append(tuple(range(idx,idx+8)))
   me=bpy.data.meshes.new('v019 spectators');me.from_pydata(pts,[],faces)
   for col in ['#d5bd9b','#29343c','#b7424b','#e6dfc9']:me.materials.append(mat(col))
   for po in me.polygons:po.material_index=(po.index*7+row+tier)%4
   ob=bpy.data.objects.new(me.name,me);env.objects.link(ob)
 surface('v019 advertising',[(-43,sign*57,.1),(43,sign*57,.1),(43,sign*57,.95),(-43,sign*57,.95)],'#ac3546')
for side in [-1,1]:surface('v019 side stand',[(side*38,-61,0),(side*38,61,0),(side*48,61,10),(side*48,-61,10)],'#566b79')
# Fit controls to each complete drawing. No portrait replacement or separated clothing.
lib['SCENE']=s;actors={}
def rig(sheet,cell,name,height,loc,face=0,manual=None,arms=False):
 box=lib['sheets'][sheet][2][cell];x0,y0,x1,y1=box[:4];W=x1-x0;H=y1-y0;unit=height/H;root=lib['actor'](sheet,[cell],0,0,height*lib['LANDMARKS'][sheet]['base']/H,0);root.name='v019 '+name;root.location=loc;root.rotation_euler=(math.pi/2,0,face);skin=next(o for o in root.children if o.type=='MESH');skin.data.shape_keys.animation_data_clear()
 for block in skin.data.shape_keys.key_blocks:
  if block.name!='Basis':block.value=0
 # Remove old acting accent driver, keep only component selection.
 skin.data.shape_keys.animation_data_clear()
 cx=lib['LANDMARKS'][sheet]['x'][cell] if lib['LANDMARKS'][sheet]['x'] else (x0+x1)/2;cy=y1
 def xy(p):return Vector(((p[0]-cx)*unit,(cy-p[1])*unit,0))
 default={'hip':(.50,.55),'neck':(.50,.23),'head':(.50,.09),'Lshoulder':(.32,.27),'Lelbow':(.31,.40),'Lwrist':(.48,.49),'Lfinger':(.50,.51),'Rshoulder':(.69,.27),'Relbow':(.70,.40),'Rwrist':(.53,.49),'Rfinger':(.50,.51),'Lhip':(.40,.56),'Lknee':(.29,.76),'Lankle':(.24,.92),'Ltoe':(.12,.985),'Rhip':(.62,.56),'Rknee':(.72,.76),'Rankle':(.78,.92),'Rtoe':(.89,.985)}
 pts=manual or {k:(x0+u*W,y0+v*H) for k,(u,v) in default.items()};r={k:xy(p) for k,p in pts.items()};C={}
 for k,v in r.items():ob=bpy.data.objects.new(name+' '+k,None);s.collection.objects.link(ob);ob.parent=root;ob.location=v;C[k]=ob
 bones={'torso':('hip','neck'),'head':('neck','head')}
 for side in ['L','R']:
  for label,aa,bb in [('upperarm','shoulder','elbow'),('forearm','elbow','wrist'),('hand','wrist','finger'),('thigh','hip','knee'),('calf','knee','ankle'),('foot','ankle','toe')]:
   if label in ['upperarm','forearm','hand'] and not arms:continue
   bones[side+label]=(side+aa,side+bb)
 ad=bpy.data.armatures.new(name+' fitted bones');arm=bpy.data.objects.new(ad.name,ad);s.collection.objects.link(arm);arm.parent=root;bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);bpy.context.view_layer.objects.active=arm;bpy.ops.object.mode_set(mode='EDIT')
 for k,(aa,bb) in bones.items():eb=ad.edit_bones.new(k);eb.head=r[aa];eb.tail=r[bb]
 bpy.ops.object.mode_set(mode='OBJECT')
 for k,(aa,bb) in bones.items():pb=arm.pose.bones[k];co=pb.constraints.new('COPY_LOCATION');co.target=C[aa];co=pb.constraints.new('STRETCH_TO');co.target=C[bb];co.rest_length=(r[bb]-r[aa]).length;co.volume='NO_VOLUME';co.bulge=0
 names=list(bones);weights=np.zeros((len(skin.data.vertices),len(names)))
 def near(p,opts):
  values=[]
  for k in opts:
   aa,bb=[r[t] for t in bones[k]];d=bb-aa;t=max(0,min(1,(p-aa).dot(d)/max(d.length_squared,1e-8)));values.append(((p-(aa+t*d)).length,k))
  values=sorted(values)[:2];ww=[math.exp(-(d*d-values[0][0]**2)/.0016) for d,k in values];return {k:w/sum(ww) for (_,k),w in zip(values,ww)}
 for i,v in enumerate(skin.data.vertices):
  p=v.co;side='L' if p.x<r['hip'].x else 'R'
  if p.y>r['neck'].y+.04:w={'head':1}
  elif p.y>r['neck'].y-.05:t=max(0,min(1,(p.y-r['neck'].y+.05)/.09));w={'head':t,'torso':1-t}
  elif p.y>r['hip'].y+.02:
   if arms and (p.x<r['Lshoulder'].x+.01 or p.x>r['Rshoulder'].x-.01):w=near(p,[side+'upperarm',side+'forearm',side+'hand'])
   else:w={'torso':1}
  else:
   w=near(p,[side+'thigh',side+'calf',side+'foot']);t=max(0,min(1,(p.y-r['hip'].y+.07)/.09));w={k:val*(1-t) for k,val in w.items()};w['torso']=t
  for k,val in w.items():weights[i,names.index(k)]=val
 grid=weights.reshape(101,61,len(names))
 for _ in range(24):grid[1:-1,1:-1]=(.6*grid[1:-1,1:-1]+.1*(grid[:-2,1:-1]+grid[2:,1:-1]+grid[1:-1,:-2]+grid[1:-1,2:]))
 for j,k in enumerate(names):
  vg=skin.vertex_groups.new(name=k)
  for i,w in enumerate(weights[:,j]):
   if w>.0001:vg.add([i],float(w),'REPLACE')
 mod=skin.modifiers.new('Continuous source fitted joints','ARMATURE');mod.object=arm;mod.use_deform_preserve_volume=True
 a=dict(name=name,root=root,skin=skin,C=C,rest=r,arm=arm,s=s);actors[name]=a;return a
saka_pts={'hip':(595,277),'neck':(566,130),'head':(570,79),'Lshoulder':(520,160),'Lelbow':(465,185),'Lwrist':(408,204),'Lfinger':(390,214),'Rshoulder':(631,166),'Relbow':(681,203),'Rwrist':(710,197),'Rfinger':(734,215),'Lhip':(566,279),'Lknee':(563,351),'Lankle':(557,444),'Ltoe':(585,472),'Rhip':(618,279),'Rknee':(668,320),'Rankle':(733,386),'Rtoe':(774,378)}
gab_pts={'hip':(1367,275),'neck':(1375,132),'head':(1378,75),'Lshoulder':(1305,158),'Lelbow':(1260,201),'Lwrist':(1198,262),'Lfinger':(1184,275),'Rshoulder':(1431,151),'Relbow':(1460,209),'Rwrist':(1489,254),'Rfinger':(1507,267),'Lhip':(1334,281),'Lknee':(1284,354),'Lankle':(1237,441),'Ltoe':(1205,471),'Rhip':(1402,282),'Rknee':(1462,358),'Rankle':(1489,440),'Rtoe':(1514,471)}
S=rig('football',1,'Saka',1.78,(-33.4,51.6,0),0,saka_pts,True);G=rig('football',3,'Gabriel',1.90,(0,49.1,0),0,gab_pts,True)
D=[]
for i,(x,y) in enumerate([(-1.8,49.5),(2.1,48.7)]):D.append(rig('football',6,'opposition defender '+str(i),1.83,(x,y,0)))
K=rig('football',7,'opposition goalkeeper',1.86,(1,52,0));R=rig('football',7,'Raya',1.83,(0,-50.7,0),math.pi)
wall=[]
for i in range(9):wall.append(rig('wall',i,'wall '+str(i+1),[1.90,1.92,1.78,1.85,1.78,1.80,1.79,1.82,1.77][i],((i-4)*1.05,-51.7,0),math.pi))
opp=rig('football',6,'opposing attacker',1.82,(-4.5,-47.5,0),math.pi)
A=b['clone_cast']('opening Arteta',s,'v019 Arteta',0,0);A['root'].rotation_euler=(math.pi/2,0,0);A['root'].scale=(1.78/1.8,)*3;A['root'].location=(-35,46,0);actors['Arteta']=A
Y=b['clone_cast']('unveiling Gyokeres',s,'v019 Gyokeres',0,0);Y['root'].rotation_euler=(math.pi/2,0,math.pi);Y['root'].scale=(1.90/1.8,)*3;Y['root'].location=(0,-24,0);actors['Gyokeres']=Y
# Keep clone source rest geometry consistent; remove inherited pointing/phone fragments.
for a in [A,Y]:
 for ob in a['objects']:
  if any(t in ob.name for t in ['pointing','point hand','point silhouette','source left hand','source exposed forearm','restored shoe']):ob.hide_render=ob.hide_viewport=True
# Opponent keeper uses a distinct blue-purple shirt, not Arsenal's yellow goalkeeper kit.
me=K['skin'];m=me.data.materials[0].copy();me.data.materials[0]=m;nodes=m.node_tree.nodes;links=m.node_tree.links;tex=next(x for x in nodes if x.type=='TEX_IMAGE' and x.image.name.startswith('football.png'));sep=nodes.new('ShaderNodeSeparateColor');links.new(tex.outputs['Color'],sep.inputs[0]);gt=nodes.new('ShaderNodeMath');gt.operation='GREATER_THAN';links.new(sep.outputs['Green'],gt.inputs[0]);gt.inputs[1].default_value=.5;lt=nodes.new('ShaderNodeMath');lt.operation='LESS_THAN';links.new(sep.outputs['Blue'],lt.inputs[0]);lt.inputs[1].default_value=.15;mul=nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';links.new(gt.outputs[0],mul.inputs[0]);links.new(lt.outputs[0],mul.inputs[1]);mix=nodes.new('ShaderNodeMixRGB');links.new(mul.outputs[0],mix.inputs[0]);links.new(tex.outputs['Color'],mix.inputs[1]);mix.inputs[2].default_value=(.09,.15,.35,1);em=next(x for x in nodes if x.type=='EMISSION');links.new(mix.outputs[0],em.inputs[0])
# Root exposure keeps distinct roles at the proper end of the pitch.
for a in [S,G,*D,K]:show(a['root'],1,269)
for a in [R,*wall,opp]:show(a['root'],392,1047)
show(Y['root'],712,855)
# FK for kicking/header silhouettes, projected planted-foot shuffles for wall.
def pose(a,f,lean=0,down=0,ua=(0,0),fa=(0,0),leg=(0,0,0,0)):
 r=a['rest'];p={k:v.copy() for k,v in r.items()};p['hip'].y+=down
 for k in ['neck','head','Lshoulder','Rshoulder']:p[k]=p['hip']+n['rotate'](r[k]-r['hip'],lean)
 for i,side in enumerate(['L','R']):
  p[side+'hip'].y+=down
  for lab,prev,angle in [('elbow','shoulder',ua[i]+lean),('wrist','elbow',ua[i]+fa[i]+lean),('finger','wrist',ua[i]+fa[i]+lean)]:p[side+lab]=p[side+prev]+n['rotate'](r[side+lab]-r[side+prev],angle)
  p[side+'knee']=p[side+'hip']+n['rotate'](r[side+'knee']-r[side+'hip'],leg[i*2]);p[side+'ankle']=p[side+'knee']+n['rotate'](r[side+'ankle']-r[side+'knee'],leg[i*2+1]);p[side+'toe']=p[side+'ankle']+r[side+'toe']-r[side+'ankle']
 # Compression bends the knees while boots stay planted; never sink the whole leg.
 if down:
  for side in ['L','R']:
   p[side+'ankle']=r[side+'ankle'].copy();p[side+'toe']=r[side+'toe'].copy()
   p[side+'knee'].x+=(-1 if side=='L' else 1)*abs(down)*.65;p[side+'knee'].y-=down*.2
 for k,v in p.items():key(a['C'][k],'location',f,v)
for f in range(1,1048):
 s.frame_set(f)
 if f<=197:
  wind=smooth((f-146)/12);strike=smooth((f-158)/10);follow=smooth((f-168)/9);relax=smooth((f-177)/17)
  angle=(-.48-.42*wind+.9*strike+.18*follow)*(1-relax);pose(S,f,lean=-.015*wind,ua=(-.05*wind,.08*strike),fa=(0,.08*strike),leg=(0,0,angle,angle-.12*wind))
 if f<=269:
  prep=smooth((f-194)/7)*(1-smooth((f-201)/6));u=(f-204)/27;jump=.42*4*u*(1-u) if 0<u<1 else 0;land=-.065*math.sin(math.pi*max(0,min(1,(f-231)/9))) if 231<=f<=240 else 0
  G['root'].location=(0,49.1,jump);key(G['root'],'location',f,G['root'].location);pose(G,f,lean=.10*smooth((f-214)/4)*(1-smooth((f-221)/8)),down=-.07*prep+land,ua=(-.20*prep,.15*prep))
  for a in D:pose(a,f,lean=.025*math.sin(max(0,f-205)*.2) if 205<f<240 else 0)
  pose(K,f,lean=-.09*smooth((f-221)/9),ua=(-.1,.1))
 if f>=392:
  for i,a in enumerate(wall):
   start=400+i*3;u=smooth((f-start)/61);x0=(i-4)*1.05;x1=(i-4)*.70;root=a['root'];key(root,'location',f,(x0+(x1-x0)*u,-51.7,0));r=a['rest'];p={k:v.copy() for k,v in r.items()};p['hip'].x+=.010*math.sin(u*math.tau);p['hip'].y-=.015*math.sin(u*math.pi)
   for k in ['neck','head','Lshoulder','Rshoulder']:p[k]+=p['hip']-r['hip']
   for side,offset in [('L',0),('R',28)]:
    step=smooth((f-start-offset)/25);lift=.035*math.sin(math.pi*max(0,min(1,(f-start-offset)/25)));travel=x0+(x1-x0)*step;rootx=x0+(x1-x0)*u
    p[side+'ankle'].x-=travel-rootx;p[side+'ankle'].y+=lift;p[side+'toe']+=p[side+'ankle']-r[side+'ankle'];p[side+'hip']+=p['hip']-r['hip'];t=(r[side+'knee'].y-r[side+'hip'].y)/(r[side+'ankle'].y-r[side+'hip'].y);p[side+'knee']=p[side+'hip'].lerp(p[side+'ankle'],t)
   for k,v in p.items():key(a['C'][k],'location',f,v)
  pr=smooth((f-475)/14);key(R['root'],'location',f,(0,-51.2+.85*pr,0));pose(R,f,lean=.015*pr)
  pose(opp,f,lean=.08*smooth((f-515)/12)*(1-smooth((f-555)/12)))
 # Same selected Arteta/Gyokeres controls and whole drawing.
 command=smooth((f-274)/6)*(1-smooth((f-355)/10));proud=smooth((f-905)/7)*(1-smooth((f-985)/8));ping=smooth((f-992)/7)
 b['pose_actor'](A,f,ua=(.12*command,-.48*command),fa=(.25*command,-.55*command),lean=-.025*command+.02*proud-.025*ping)
 loc=(-35,46,0) if f<392 else (-5,-50.5,0);key(A['root'],'location',f,loc);key(A['root'],'rotation_euler',f,(math.pi/2,0,0 if f<392 else math.pi))
 ask=smooth((f-716)/7)*(1-smooth((f-794)/12));b['pose_actor'](Y,f,ua=(-.16*ask,.16*ask),fa=(-.45*ask,.45*ask),lean=.016*ask)
for a in actors.values():
 for ob in [a['root'],*a['C'].values()]:
  for fc in curves(ob):
   if fc.data_path!='scale':
    for k in fc.keyframe_points:k.interpolation='LINEAR'
# Ball contact is derived from fitted toe/head controls, then travels in world space.
# Reuse the already-authored native football and materials, clear its previous flight.
src=next(o for o in bpy.data.scenes['S002_B02_v017_training'].objects if o.name.startswith('B17 dimensional football')) if any(o.name.startswith('B17 dimensional football') for o in bpy.data.scenes['S002_B02_v017_training'].objects) else None
if src is None:
 src=bpy.app.driver_namespace['env17'].get('ball')
ball=src.copy();ball.data=src.data.copy() if src.data else None;ball.animation_data_clear();s.collection.objects.link(ball);ball.parent=None;ball.name='v019 match ball'
for child in src.children_recursive:
 cp=child.copy();cp.data=child.data.copy() if child.data else None;s.collection.objects.link(cp);cp.parent=ball;cp.animation_data_clear()
s.frame_set(168);bpy.context.view_layer.update();contact=S['root'].matrix_world@S['C']['Rtoe'].location;contact.z=.12
s.frame_set(217);bpy.context.view_layer.update();head=G['root'].matrix_world@G['C']['head'].location;head.z+=.04;end=Vector((2.2,53.15,1.15))
for f in range(1,270):
 if f<168:p=contact
 elif f<=217:u=(f-168)/49;p=contact.lerp(head,u);p.z+=1.25*4*u*(1-u)
 elif f<=238:u=(f-217)/21;p=head.lerp(end,u);p.z+=.08*math.sin(math.pi*u)
 else:u=min(1,(f-238)/18);p=end.lerp(Vector((2.2,53.45,.11)),u)
 key(ball,'location',f,p);key(ball,'rotation_euler',f,(0,(f-168)*.2,0))
show(ball,1,269);linear(ball)
# Ground contact shadows, tracked roots rather than floating image-plane ellipses.
for a in [S,G,*D,K,R,*wall,opp,A,Y]:
 root=a['root'];sh=surface('v019 contact shadow',[(.38*math.cos(t),.16*math.sin(t),.008) for t in np.linspace(0,math.tau,33)[:-1]],'#527b46')
 co=sh.constraints.new('COPY_LOCATION');co.target=root;co.use_z=False
 for prop in ['hide_render','hide_viewport']:
  dr=sh.driver_add(prop).driver;dr.expression='v < .001';q=dr.variables.new();q.name='v';q.type='TRANSFORMS';q.targets[0].id=root;q.targets[0].transform_type='SCALE_X';q.targets[0].transform_space='LOCAL_SPACE'
# Cameras guide attention; the same dimensional stadium remains behind every shot.
camera('v019 corner taker',1,(-35,43.3,2.3),(-33.1,51.5,1.0),48)
camera('v019 follow the cross',177,(15,32,10),(0,49.5,1.2),43)
camera('v019 header contact',198,(5,40,3.2),(0,50.7,1.45),44)
camera('v019 Arteta command',270,(-35,41.9,1.9),(-35,46,1),48)
camera('v019 nine-player shuffle',392,(0,-39.6,3.0),(0,-51.8,1.1),43)
camera('v019 Raya protects wall',512,(1.0,-42.5,2.65),(0,-51.6,1.1),42)
camera('v019 isolated striker',712,(4,-12,3.8),(0,-33,1.1),38)
camera('v019 striker question',722,(.4,-19.6,1.9),(0,-24,1),46)
camera('v019 Arteta reply',779,(-5,-46.2,1.8),(-5,-50.5,1),47)
camera('v019 proud Arteta',904,(-5,-46.2,1.8),(-5,-50.5,1),47)
camera('v019 City result',988,(-5,-46.2,1.8),(-5,-50.5,1),47)
# Metadata and reusable live registry.
s['environment']='105x68m pitch; both goals 7.32x2.44m; flags at corners';s['cast accounting']='Nine wall players + Raya + Gyokeres = eleven';s.camera=next(m.camera for m in s.timeline_markers if m.frame==392);s.frame_set(490)
bpy.app.driver_namespace['defence19']=dict(s=s,actors=actors,wall=wall,A=A,Y=Y,R=R,S=S,G=G,ball=ball,contact=contact,header_contact=head,O=O,env=env)
result={'scene':s.name,'objects':len(s.objects),'cast':list(actors),'ball_boot':list(contact),'header_contact':list(head)}
