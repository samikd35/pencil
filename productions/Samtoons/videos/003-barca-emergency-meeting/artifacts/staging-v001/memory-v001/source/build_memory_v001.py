"""S10: supported finish, seated feed, ball match cut. Native baked staging preview.
Existing contours/set/helpers are reused; previous shot choreography is not.
Run setup(), actors(), animate(), review_corrections(), clothing_review(), finish() in visible Blender.
"""
import bpy,json,math,importlib.util
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/staging-v001/memory-v001';END=264
spec=importlib.util.spec_from_file_location('s10_draw',V/'scripts/build_football_v001.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
g.P='S10 / ';g.O=O;g.END=END;g.ART=V/'assets/memory-v001';g.A={};g.M={}
R=g.R;D=g.D;BASE=Vector((-4.7,-4.7,0));CUT=139
EVENTS={'narration':13,'windup':38,'strike':47,'goal':64,'recovery':81,'roll_release':119,'match_cut':CUT,'receive':171,'settled':185,'flick_answer':221}
g.EVENTS=EVENTS
at=g.at;turn=g.turn;key=g.key

def pose_shape_bulk(o,pts,f):
 # One RNA write, avoiding a whole-file dependency update for every coordinate.
 k=o.shape_key_add(name=f'pose {f:03}');k.interpolation='KEY_LINEAR'
 depth=o.data.vertices[0].co.y
 k.data.foreach_set('co',[v for x,z in pts for v in (x,depth,z)])
 o.data.shape_keys.eval_time=k.frame;o.data.shape_keys.keyframe_insert(data_path='eval_time',frame=f)
g.pose_shape=pose_shape_bulk

def visible(o,on,f,children=True):
 for q in [o]+(list(o.children_recursive) if children else []):
  q.hide_render=q.hide_viewport=not on
  for p in ['hide_render','hide_viewport']:q.keyframe_insert(data_path=p,frame=f)
def text(name,body,parent,loc,size,color='#fff2d9'):
 cu=bpy.data.curves.new(g.P+name,'FONT');cu.body=body;cu.size=size;cu.align_x='CENTER';cu.materials.append(g.mat(color));o=bpy.data.objects.new(cu.name,cu);g.C.objects.link(o);o.parent=parent;o.location=loc;return o

def setup():
 global S,CAM,BALL,NEXT,SHADOW,NEXTSH,PAST,NOW
 assert not bpy.app.background
 assert not (O/'memory.blend').exists(),'Preserve delivered revision'
 with bpy.data.libraries.load(str(V/'artifacts/staging-v001/training-set-v001/training-set.blend'),link=False) as (src,dst):dst.scenes=['S003_Training_Set_v001']
 S=dst.scenes[0].copy();S.name='S003_S10_Memory_v001';S.use_fake_user=True;bpy.context.window.scene=S;g.S=S
 g.C=bpy.data.collections.new(g.P+'performance');S.collection.children.link(g.C)
 S.frame_start=1;S.frame_end=END;S.render.fps=24;S.render.resolution_x=1280;S.render.resolution_y=720;S.render.resolution_percentage=100;S.render.use_sequencer=False;S.display.render_aa='16'
 # Own all environment visibility/text/material changes in this scene only.
 environment=bpy.data.collections.new(g.P+'environment');S.collection.children.link(environment)
 originals=list(S.objects)
 for old in originals:
  if old.type=='CAMERA':continue
  q=old.copy();q.name=g.P+'set '+old.name
  if old.data:q.data=old.data.copy()
  environment.objects.link(q)
  if old.type=='FONT' and ('Training boundary identity' in old.name or 'Training centre name' in old.name):
   now=q;past=q.copy();past.data=q.data.copy();environment.objects.link(past)
   past.data.body='FC BAYERN' if 'boundary' in old.name else 'MÜNCHEN · TRAINING'
   visible(past,True,1);visible(past,False,CUT);visible(now,False,1);visible(now,True,CUT)
 # Drop inherited collection links, retaining copies, not destructive to original scene.
 for coll in list(S.collection.children):
  if coll not in [g.C,environment]:S.collection.children.unlink(coll)
 for ob in list(S.collection.objects):S.collection.objects.unlink(ob)
 # Factory board is outside this illustration; keep the complete dimensional pitch/goal.
 for ob in environment.objects:
  if any(s in ob.name.lower() for s in ['goal count','ball belt','ball rack','next','storage','spare ball']):ob.hide_render=ob.hide_viewport=True
 cd=bpy.data.cameras.new(g.P+'director');CAM=bpy.data.objects.new(cd.name,cd);g.C.objects.link(CAM);S.camera=CAM;cd.type='ORTHO';cd.clip_end=300
 def ball(name):
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=.11);o=bpy.context.object;o.name=g.P+name
  for c in list(o.users_collection):c.objects.unlink(o)
  g.C.objects.link(o);o.data.materials.append(g.mat('#fff5da'));o.data.materials.append(g.mat('#203249'))
  for p in o.data.polygons:p.material_index=1 if p.index%7==0 else 0
  sh=g.oval(name+' shadow',0,0,.13,.065,'#59854b');sh.rotation_euler.x=math.pi/2
  return o,sh
 BALL,SHADOW=ball('finish ball');NEXT,NEXTSH=ball('next ball')
 # Physically supported coach: seat under pelvis, feet forward on turf.
 bench=g.empty('training bench');bench.location=BASE-R*2.45;bench.rotation_euler.z=math.atan2(R.y,R.x)
 g.outlined('bench seat',[(-.32,.62),(.31,.62),(.31,.68),(-.32,.68)],'#697b83',bench,-.03)
 g.line('bench feet',[(-.26,.04),(-.26,.63),(.27,.63),(.27,.04)],'#394d59',.027,bench,-.015)
 for area in bpy.context.screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False;area.spaces.active.shading.light='FLAT';area.spaces.active.shading.color_type='MATERIAL'
 return {'scene':S.name,'new_environment_objects':len(environment.objects)}

def actors():
 for who in ['Lewandowski','Raphinha','Flick']:g.create_actor(who,who.lower())
 # Keep selected likeness. Dedicated clean continuous cloth replaces inappropriate crops.
 a=g.A['Flick'];a['shorts'].hide_render=a['shorts'].hide_viewport=True
 shirt=next(q for q in a['torso'].children if 'drawn shirt' in q.name);shirt.hide_render=shirt.hide_viewport=True
 g.outlined('coach jacket',[(-.185,-.04),(.20,-.04),(.195,.38),(.105,.53),(-.08,.53),(-.195,.40)],'#263859',a['torso'],.035)
 g.line('coach zip',[(.035,.0),(.026,.43),(0,.51)],'#8b9aaa',.002,a['torso'],.04)
 g.line('coach collar',[(-.08,.51),(0,.43),(.105,.51)],'#15243b',.005,a['torso'],.042)
 # Colour identifier swaps with place/time; source Barça badge isn't left in the memory.
 badge=g.oval('Bayern badge',.115,.36,.036,.036,'#df3345',a['torso'],.045);g.oval('Bayern badge centre',.115,.36,.019,.024,'#e4e7d9',a['torso'],.046)
 barca=g.outlined('Barca badge',[(.076,.40),(.15,.40),(.147,.345),(.115,.321),(.08,.345)],'#d3aa53',a['torso'],.049)
 for root in [badge]+[q for q in a['torso'].children if 'Bayern badge centre' in q.name]:visible(root,True,1);visible(root,False,CUT)
 visible(barca,False,1);visible(barca,True,CUT)
 # Avoid the discarded source yoke. A seated trouser pelvis is one rounded silhouette.
 g.outlined('seated pelvis',[(-.18,.07),(.15,.07),(.27,-.06),(.23,-.16),(-.16,-.12)],'#233553',a['torso'],.012)
 for who in ['Lewandowski','Raphinha']:
  a=g.A[who]
  for side in ['L','R']:
   for region,col in [('sleeve','#d52231' if who=='Lewandowski' else '#223d77'),('sock','#cf2030' if who=='Lewandowski' else '#203251')]:
    ob=a['limbs'][region+side][1];ob.data.materials.clear();ob.data.materials.append(g.mat(col))
 for a in g.A.values():
  # Voice-over means none of the on-field figures lip-sync the narrator.
  for ob in [a['mouth']]+list(a['mouth'].children_recursive):ob.hide_render=ob.hide_viewport=True
 return {'cast':list(g.A),'construction':'Selected native portraits; separate supported athletic and seated performances'}

def joint(a,b,lengths,pole):return Vector(g.two_bone_joint(tuple(a),tuple(b),lengths,pole))
def pose(name,f):
 coach=name=='Flick';receive=name=='Raphinha'
 if coach:
  hip=Vector((0,.70));lean=at(f,[(1,-.05),(86,-.05),(103,-.12),(115,-.28),(119,-.30),(130,-.28),(159,-.05),(END,-.05)])
  neck=hip+Vector(turn((0,.53),lean));world=BASE-R*2.45
  legs={'L':((-.095,.65),(.22,.48),(.12,.16)),'R':((.095,.65),(.47,.51),(.49,.16))}
  # Foreground hand carries then gently releases from a seat; no standing squat.
  wristR=Vector(at(f,[(1,(.32,.77)),(90,(.32,.77)),(103,(.24,.72)),(112,(.35,.58)),(119,(.49,.45)),(125,(.58,.45)),(139,(.44,.58)),(159,(.32,.75)),(END,(.32,.75))]))
  wrists={'R':wristR,'L':Vector((.12,.79))};angles={'L':0,'R':0}
 else:
  if receive:
   hip=Vector(at(f,[(1,(.06,1.002)),(149,(.06,1.002)),(164,(.09,1.00)),(171,(.11,.999)),(183,(.12,1.002)),(END,(.12,1.002))]))
   lf=at(f,[(1,(-.16,.16)),(149,(-.16,.16)),(162,(-.24,.215)),(171,(-.23,.18)),(178,(-.15,.16)),(185,(-.10,.16)),(END,(-.10,.16))]);rf=(.23,.16)
   lean=at(f,[(1,-.015),(153,-.015),(171,.035),(185,-.015)]);angles={'L':at(f,[(1,0),(164,-.04),(171,0),(185,0)]),'R':0}
   wrists={'L':Vector((-.28,1.0)),'R':Vector((.40,1.03))}
  else:
   hip=Vector(at(f,[(1,(-.07,1.004)),(28,(-.07,1.004)),(38,(-.105,.985)),(47,(-.085,.99)),(56,(-.04,.997)),(70,(.02,1.002)),(81,(.075,1.002)),(END,(.075,1.002))]))
   lf=at(f,[(1,(-.18,.16)),(71,(-.18,.16)),(76,(-.13,.24)),(81,(-.07,.16)),(END,(-.07,.16))]);rf=at(f,[(1,(.16,.16)),(23,(.16,.16)),(31,(-.22,.25)),(38,(-.43,.45)),(42,(-.37,.38)),(47,(.23,.17)),(54,(.68,.48)),(60,(.64,.54)),(70,(.4,.26)),(76,(.22,.16)),(END,(.22,.16))])
   lean=at(f,[(1,0),(25,0),(38,.08),(47,-.08),(56,-.14),(76,0)]);angles={'L':0,'R':at(f,[(1,0),(31,-.2),(38,-.65),(42,-.45),(47,.01),(54,.6),(60,.65),(76,0)])}
   swing=at(f,[(1,0),(25,0),(38,1),(47,-.4),(57,-.7),(81,0)])
   wrists={'L':Vector((-.31-.12*swing,1.0+.12*abs(swing))),'R':Vector((.38+.12*swing,1.01+.10*abs(swing)))}
  neck=hip+Vector(turn((0,.53),lean));world=BASE.copy();legs={}
  for side,sgn,ank in [('L',-1,lf),('R',1,rf)]:
   start=hip+Vector((sgn*.095,-.05));end=Vector(ank)
   assert (end-start).length<=.812,(name,f,side,(end-start).length)
   knee=joint(start,end,(.406,.406),(start.x+.75,start.y-.15));legs[side]=(tuple(start),tuple(knee),tuple(end))
 arms={}
 for side,sgn in [('L',-1),('R',1)]:
  sh=hip+Vector(turn((sgn*.155,.43),lean));wr=wrists[side]
  lengths=(.35,.35) if coach else (.295,.295)
  el=joint(sh,wr,lengths,(sh.x+sgn*.5,sh.y-.20));arms[side]=(tuple(sh),tuple(el),tuple(wr))
 return dict(world=world,hip=hip,neck=neck,lean=lean,headangle=at(f,[(1,0),(29,-.025),(49,-.05),(84,0),(END,0)]) if not coach else -lean*.65,gaze=0,legs=legs,arms=arms,rot=angles,point=0)

def animate_actor(name):
 a=g.A[name];coach=name=='Flick'
 for f in range(1,END+1):
  p=pose(name,f);a['root'].location=p['world'];key(a['root'],f)
  a['torso'].location=(p['hip'].x,0,p['hip'].y);a['torso'].rotation_euler.y=-p['lean'];key(a['torso'],f)
  a['head'].location=(p['neck'].x,-.006,p['neck'].y);a['head'].rotation_euler.y=-(p['lean']+p['headangle']);key(a['head'],f)
  if f%2 or f in EVENTS.values() or f==END:
   pts=[tuple(p['neck']+Vector(turn(q,p['lean']))) for q in [(-.072,-.04),(.075,-.04),(.095,.10),(-.08,.10)]];g.pose_shape(a['neck'],pts,f)
  for side in ['L','R']:
   arm=p['arms'][side];leg=p['legs'][side]
   if f%2 or f in EVENTS.values() or f==END:
    regions=[('arm',arm,[.070,.062,.032] if coach else [.053,.047,.028]),('sleeve',(arm[0],tuple(Vector(arm[0]).lerp(Vector(arm[1]),.35)),tuple(Vector(arm[0]).lerp(Vector(arm[1]),.70))),[.083,.079,.062]),('leg',leg,[.104,.088,.045] if coach else [.078,.057,.037]),('sock',(tuple(Vector(leg[1]).lerp(Vector(leg[0]),.04)),tuple(Vector(leg[1]).lerp(Vector(leg[2]),.48)),leg[2]),[.058,.060,.041])]
    for region,joints,widths in regions:
     edge,fill=a['limbs'][region+side]
     if coach and region in ['sock','sleeve']:edge.hide_render=edge.hide_viewport=fill.hide_render=fill.hide_viewport=True;continue
     if coach:fill.data.materials.clear();fill.data.materials.append(g.mat('#263859' if region=='arm' else '#233553'))
     g.pose_shape(edge,g.ribbon(joints,[w+.003 for w in widths]),f);g.pose_shape(fill,g.ribbon(joints,widths),f)
   hand=a['hand'+side];w=Vector(arm[2]);fore=w-Vector(arm[1]);ang=math.atan2(fore.y,fore.x)+math.pi/2
   hand.location=(w.x,-.033 if coach else -.006,w.y);hand.rotation_euler.y=-ang;key(hand,f)
   foot=a['boots'][0 if side=='L' else 1];ank=Vector(leg[2]);foot.location=(ank.x,-.018 if side=='L' else .018,ank.y);foot.rotation_euler.y=-p['rot'][side];key(foot,f)
   for bone,points in [(side+' thigh',leg[:2]),(side+' shin',leg[1:]),(side+' upper',arm[:2]),(side+' fore',arm[1:])]:
    for target,pt in zip(a['targets'][bone],points):target.location=(pt[0],0,pt[1]);key(target,f)
  for target,pt in zip(a['targets']['spine'],[p['hip'],p['neck']]):target.location=(pt[0],0,pt[1]);key(target,f)
  for i,(pupil,lid) in enumerate(a['eyes']):
   pupil.location.x=at(f,[(1,.003),(27,.003),(31,.010),(65,.010),(91,-.004 if coach else .003),(150,.010),(END,.010)]);pupil.location.z=-.005 if 26<f<62 and not coach else 0;key(pupil,f)
   blink=f in ([17,18,193,194] if coach else [13,14,212,213]);visible(lid,blink,f,False)
  a['shadow'].location=(p['world'].x,p['world'].y,.023);key(a['shadow'],f)
 # Scope time-period visibility to the actual drawing objects, keeping rejected parts hidden.
 for ob in [a['root']]+list(a['root'].children_recursive)+[a['shadow']]:
  if ob.hide_render or ob.type=='ARMATURE' or 'lid' in ob.name:continue
  if name in ['Lewandowski','Raphinha']:
   visible(ob,name=='Lewandowski',1,False);visible(ob,name=='Raphinha',CUT,False)
 if name=='Raphinha':
  for ob in [a['point']]+list(a['point'].children_recursive):ob.hide_render=ob.hide_viewport=True;ob.animation_data_clear()
 # Source shorts follow the thigh near the hem, retaining a continuous hip region.
 if not coach:
  ob=a['shorts'];ob.shape_key_add(name='Waist');ob.data.shape_keys.use_relative=False;base=[v.co.copy() for v in ob.data.vertices]
  for f in sorted(set([1,END,CUT]+list(range(23,84,2))+list(range(149,188,2)))):
   p=pose(name,f);k=ob.shape_key_add(name=f'fabric {f}');k.interpolation='KEY_LINEAR';coords=[]
   for co in base:
    side='L' if co.x<0 else 'R';hp,kn,_=p['legs'][side];d=Vector(kn)-Vector(hp);ang=math.atan2(d.y,d.x)+math.pi/2-p['lean'];w=max(0,min(1,(-co.y-.02)/.20));pivot=Vector((-.095 if side=='L' else .095,-.045));pt=pivot+Vector(turn(Vector((co.x,co.y))-pivot,ang*w));coords.extend((pt.x,pt.y,co.z))
   k.data.foreach_set('co',coords)
   ob.data.shape_keys.eval_time=k.frame;ob.data.shape_keys.keyframe_insert(data_path='eval_time',frame=f)

def contact(name,f,side,direction):
 from mathutils.bvhtree import BVHTree
 S.frame_set(f);bpy.context.view_layer.update();a=g.A[name];o=next(q for q in a['boots'][0 if side=='L' else 1].children if q.type=='MESH');ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();vs=[ev.matrix_world@v.co for v in me.vertices];tree=BVHTree.FromPolygons(vs,[tuple(p.vertices) for p in me.polygons]);p=pose(name,f);ank=p['legs'][side][2];base=p['world']+R*ank[0]+Vector((0,0,.11));d=R*direction;lo=max((v-base).dot(d) for v in vs);hi=lo+.2
 for _ in range(35):
  mid=(lo+hi)/2
  if tree.find_nearest(base+d*mid)[3]<.11:lo=mid
  else:hi=mid
 point=base+d*((lo+hi)/2);gap=tree.find_nearest(point)[3]-.11;ev.to_mesh_clear();return point,gap

def camera(f):
 # Establish action; small follow after the shot, then match position across the period cut.
 if f<87:
  start=BASE+R*.35+Vector((0,0,.85));target=start.lerp(Vector((.3,.7,1.0)),at(f,[(1,0),(48,0),(66,1),(86,1)]));scale=8.7
 elif f<221:
  target=BASE-R*.85+Vector((0,0,.89));scale=5.7
 else:target=BASE-R*2.40+Vector((0,0,1.22));scale=2.8
 CAM.location=target-D*29+Vector((0,0,5.1));CAM.rotation_euler=(target-CAM.location).to_track_quat('-Z','Y').to_euler();CAM.data.ortho_scale=scale;key(CAM,f);CAM.data.keyframe_insert(data_path='ortho_scale',frame=f)

def animate():
 global STRIKE,RECEIVE,GAPS
 for who in g.A:animate_actor(who)
 STRIKE,gap1=contact('Lewandowski',47,'R',1);RECEIVE,gap2=contact('Raphinha',171,'L',-1);GAPS={'strike':gap1,'receive':gap2}
 release=BASE-R*2.45+R*.54+Vector((0,0,.31));land=release+R*.22;land.z=.11
 for f in range(1,END+1):
  if f<=47:b=STRIKE.copy()
  elif f<=64:
   t=(f-47)/17;b=STRIKE.lerp(Vector((1.1,.12,.55)),t);b.z+=.32*4*t*(1-t)
  elif f<=69:b=Vector((1.1,.12,.55)).lerp(Vector((1.3,2.13,.35)),(f-64)/5)
  else:
   t=min(1,(f-69)/20);b=Vector((1.3,2.13,.35)).lerp(Vector((1.2,1.65,.11)),t)
  BALL.location=b;BALL.rotation_euler=(0,(f-47)*.6 if f>47 else 0,0);key(BALL,f);SHADOW.location=(b.x,b.y,.025);key(SHADOW,f)
  if f<=119:
   wr=Vector(pose('Flick',f)['arms']['R'][2]);n=BASE-R*2.45+R*(wr.x+.05)+Vector((0,0,wr.y-.14))
  elif f<=124:
   t=(f-119)/5;n=release.lerp(land,t);n.z=.31-.20*t*t
  elif f<=171:n=land.lerp(RECEIVE,(f-124)/47)
  else:n=RECEIVE+R*at(f,[(171,0),(177,.08),(185,.12),(END,.12)])
  NEXT.location=n;NEXT.rotation_euler=(0,0,0);distance=(n-land).dot(R);NEXT.rotation_euler.x=D.x*distance/.11;NEXT.rotation_euler.y=D.y*distance/.11;key(NEXT,f);NEXTSH.location=(n.x,n.y,.025);NEXTSH.scale=(.75 if f<124 else 1,)*3;key(NEXTSH,f)
  camera(f)
 visible(BALL,True,1);visible(BALL,False,CUT);visible(SHADOW,True,1);visible(SHADOW,False,CUT)
 # Coach's unaffected expression is the visual punchline, not another line.
 for label,first,last,words in [('past',1,CUT-1,'BAYERN · 2020'),('now',CUT,END,'BARCELONA · NOW')]:
  root=g.empty('period '+label,CAM);ob=text(label,words,root,(0,0,0),.027)
  for f in range(1,END+1):
   w=8.7 if f<87 else 5.7 if f<221 else 2.8;root.location=(0,w*.225,-1);root.scale=(w,w,w);key(root,f)
  visible(root,first==1,1);visible(root,True,first);visible(root,False,last+1)
 for start,end,words in [(13,66,'LEWANDOWSKI: At Bayern, he told us to keep scoring'),(67,111,'against Barcelona.'),(112,155,"Now he's at Barcelona,"),(156,216,'telling them to score against everyone else.')]:
  root=g.empty('caption',CAM);cu=text('words',words,root,(0,-.006,.02),.019)
  me=bpy.data.meshes.new(g.P+'caption bed');me.from_pydata([(-.46,-.019,0),(.46,-.019,0),(.46,.023,0),(-.46,.023,0)],[],[(0,1,2,3)]);me.materials.append(g.mat('#172a38'));ob=bpy.data.objects.new(me.name,me);g.C.objects.link(ob);ob.parent=root
  for f in range(1,END+1):
   w=8.7 if f<87 else 5.7 if f<221 else 2.8;root.location=(0,-w*.241,-.8);root.scale=(w,w,w);key(root,f)
  visible(root,False,1);visible(root,True,start);visible(root,False,end+1)
 for name,f in EVENTS.items():S.timeline_markers.new(name,frame=f)
 g.linear_keys()
 return {'events':EVENTS,'boot_ball_gaps':GAPS}

def finish():
 assert max(abs(x) for x in GAPS.values())<.001
 # Planted foot is checked separately from changing hip pose, not assumed by bone lengths.
 assert max((Vector(pose('Lewandowski',f)['legs']['L'][2])-Vector(pose('Lewandowski',1)['legs']['L'][2])).length for f in range(1,72))<1e-7
 assert all(abs(pose('Flick',f)['hip'].y-.70)<1e-7 for f in range(1,END+1))
 S['scope']='S10 staging candidate. Supported kick/recovery, seated feed, ball continuity cut. Not full-film quality acceptance.'
 S.frame_set(47);bpy.ops.wm.save_as_mainfile(filepath=str(O/'memory.blend'))
 report={'frames':END,'fps':24,'events':EVENTS,'contact_gaps_m':GAPS,'support':'Lewandowski left foot fixed through strike/follow-through; Flick pelvis fixed over seat; no reused S07 squat','limits':['Numerical contact does not certify visual acting','Current source drawings support this view; other turns need drawings','Voice candidate not heard by agent']}
 (O/'construction-check.json').write_text(json.dumps(report,indent=2)+'\n');return report

def review_corrections():
 """Source masks and period visibility must follow the actual chosen drawing."""
 a=g.A['Flick'];a['head'].scale.x=-1
 # Coaching source has a mouth opening; fill it with a restrained closed expression.
 mx,my,mw=a['c']['mouth'];m=g.empty('coach quiet mouth',a['head']);m.location=((mx-a['c']['neck'][0])*g.SCALE,-.13,(a['c']['neck'][1]-my)*g.SCALE)
 g.oval('coach mouth skin',0,0,(mw+3)*g.SCALE,.023,'#c79971',m)
 g.line('coach closed mouth',[(-.038,0),(-.015,-.002),(.025,-.002),(.043,.001)],'#554333',.002,m,.003)
 for f in range(1,END+1):
  camera(f)
  for who in ['Lewandowski','Raphinha']:
   for pupil,lid in g.A[who]['eyes']:
    visible(lid,f in [13,14,212,213] and ((f<CUT)==(who=='Lewandowski')),f,False)
 g.linear_keys()
 return {'head_facing':'Flick toward the field','time_period_lids':'scoped','camera':'follows finish, held across ball cut'}

def clothing_review():
 """Reuse the tested silhouette union helper, not its earlier choreography."""
 from types import SimpleNamespace
 sp=importlib.util.spec_from_file_location('s10_cloth',V/'scripts/revise_coaching_surfaces_v002.py');u=importlib.util.module_from_spec(sp);sp.loader.exec_module(u)
 u.P=g.P+'continuous / ';u.M=SimpleNamespace(g=g,C=g.C,line=g.line,turn=g.turn)
 from shapely.geometry import Polygon
 from shapely.ops import unary_union
 a=g.A['Flick'];a['head'].scale.x=-1
 for f in range(1,END+1):a['head'].keyframe_insert(data_path='scale',frame=f)
 # Hide replaced shell and all independent sleeve/trouser caps.
 for ob in a['torso'].children:
  if any(x in ob.name for x in ['coach jacket','seated pelvis','coach collar','coach zip']):ob.hide_render=ob.hide_viewport=True
 for region in ['arm','leg']:
  for side in ['L','R']:
   for ob in a['limbs'][region+side]:ob.hide_render=ob.hide_viewport=True
 # Selected jacket interior is clipped to the continuous shell. Remove club badge
 # from this shared art: period-specific badge drawings own that small region.
 source=json.loads((V/'assets/coaches-v001/flick.json').read_text());clip=u.soft(u.BODY).buffer(-.016).difference(Polygon([(-.19,.31),(.21,.31),(.21,.565),(-.19,.565)]))
 for i,row in enumerate(source['parts']['body']):
  for path in row['paths']:
   pg=Polygon([((x-406)*g.SCALE,(569-y)*g.SCALE) for x,y in path])
   if not pg.is_valid:pg=pg.buffer(0)
   hit=pg.intersection(clip)
   if not hit.is_empty:u.native('coat detail '+str(i),hit,row['color'],a['torso'],.046+i*.000025,ink=False)
 samples=[1,86]+list(range(88,161,2))+[221,264]
 for i,f in enumerate(samples):
  end=samples[i+1]-1 if i+1<len(samples) else END;p=pose('Flick',f);root=a['root'];cloth=[u.soft(u.world(u.BODY,p))];pants=[u.soft(u.world([(-.19,.025),(.19,.025),(.22,-.12),(-.18,-.12)],p))]
  for side,sgn in [('L',-1),('R',1)]:
   arm=p['arms'][side];leg=p['legs'][side];cloth.append(u.soft(g.ribbon(arm,[.083,.065,.035],segments=24),.016));pants.append(u.soft(g.ribbon(leg,[.102,.087,.049],segments=24),.015))
   sh,el,wr=map(Vector,arm);cap=u.soft(g.ribbon([tuple(sh),tuple(sh.lerp(el,.18)),tuple(sh.lerp(el,.38))],[.086,.083,.079],segments=12),.014);neckpatch=Polygon(u.world([(sgn*.07,.59),(sgn*.13,.57),(sgn*.17,.46),(sgn*.09,.43)],p));cloth.append(unary_union([cap,neckpatch]).convex_hull)
  shell=unary_union(cloth);trousers=unary_union(pants);assert shell.geom_type=='Polygon' and trousers.geom_type=='Polygon'
  obs=u.native('Flick jacket '+str(f),shell,'#263859',root,.040)+u.native('Flick trousers '+str(f),trousers,'#233553',root,.013)
  for side in ['L','R']:
   sh,el,wr=map(Vector,p['arms'][side]);q=[tuple(el.lerp(sh,.1)),tuple(el.lerp(wr,.44)),tuple(wr)];pg=u.soft(g.ribbon(q,[.062,.05,.035],segments=24),.012)
   obs+=u.native('Flick front forearm '+side+str(f),pg,'#263859',root,.09,ink=False)
   path=g.ribbon(q,[.062,.05,.035],segments=24)
   for pts in [path[:49],path[49:]]:obs.append(g.line('sleeve edge',pts,g.INK,.0018,root,.091))
  for ob in obs:
   visible(ob,False,1,False);visible(ob,True,f,False);visible(ob,False,end+1,False)
 # Hands are in front of the sleeves, attached at the same wrist endpoints.
 for side in ['L','R']:
  hand=a['hand'+side]
  for f in range(1,END+1):hand.location.y=-.10;hand.keyframe_insert(data_path='location',frame=f,index=1)
 # Native keyed head never left/right flips between evaluated frames.
 for f in range(1,END+1):a['head'].location.y=-.12;a['head'].keyframe_insert(data_path='location',frame=f,index=1)
 g.linear_keys();return {'continuous_coach_poses':len(samples),'reused':'revise_coaching_surfaces_v002 silhouette primitives'}
