"""Neutral whole-character reconstruction using the accepted v016 fitted-surface recipe.
Run in visible Blender after v020; preserves its selected environment, Arteta/Gyokeres and audio.
"""
import bpy,math,json,ast,bmesh
import numpy as np
from collections import deque
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/defence-v021';O.mkdir(exist_ok=True)
q=bpy.app.driver_namespace['build19'];n=bpy.app.driver_namespace['batch16'];b=bpy.app.driver_namespace['b17'];s=q['s'];room=q['room'];smooth=n['smooth'];rotate=n['rotate'];curves=n['curves'];key=q['key'];actors={}
# Capture the rejected rigs separately; their original saved revision stays intact.
oldactors=dict(q['actors'])
s.name='S002_defence_v021';bpy.context.window.scene=s;s.frame_set(1)

def cfg(box,center,top,floor,hip,neck,head,L,R,edge):
 return dict(box=box,center=center,top=top,floor=floor,hip=hip,neck=neck,head=head,L=L,R=R,edge=edge)
CONFIG={
 'Saka':cfg((55,12,493,798),275,20,795,459,(275,192),(289,97),[(176,229),(149,331),(99,431),(86,480),(227,462),(211,570),(184,732),(145,772)],[(377,229),(410,332),(456,432),(466,482),(327,462),(350,570),(376,732),(425,773)],[(193,47),(240,79),(300,73),(350,70),(410,78),(427,81)]),
 'Gabriel':cfg((521,8,986,798),755,17,795,459,(753,170),(769,90),[(654,226),(607,334),(555,433),(546,481),(703,461),(681,570),(648,732),(605,774)],[(856,226),(904,334),(951,433),(963,481),(807,461),(829,570),(855,732),(907,774)],[(173,49),(226,94),(300,86),(350,79),(400,90),(425,91)]),
 'Raya':cfg((53,770,497,1527),276,773,1520,1200,(281,922),(295,844),[(168,966),(131,1057),(102,1154),(96,1214),(225,1205),(205,1305),(171,1458),(126,1501)],[(389,966),(426,1059),(456,1154),(461,1213),(331,1205),(354,1305),(385,1458),(430,1501)],[(922,44),(970,86),(1050,75),(1115,82),(1170,92)]),
 'Opponent':cfg((536,770,985,1527),754,779,1520,1204,(759,930),(775,851),[(649,970),(604,1070),(571,1171),(569,1230),(704,1208),(681,1310),(651,1460),(602,1503)],[(858,969),(900,1070),(941,1170),(950,1230),(803,1208),(824,1310),(857,1460),(907,1503)],[(932,40),(975,84),(1040,76),(1110,84),(1173,89)])}

def make(name,kind,height,loc,face=0,sheet='football.png'):
 c=CONFIG[kind];im,material=n['old']['image_material'](V/'assets/neutral-cast-v021'/sheet);W,H=im.size;unit=1.8/(c['floor']-c['top']);P='B21 / '+name+' / '
 def xy(p):return Vector(((p[0]-c['center'])*unit,(c['floor']-p[1])*unit,0))
 root=n['empty'](s,P+'character',loc);root.rotation_euler=(math.pi/2,0,face);root.scale=(height/1.8,)*3
 rest={'hip':xy((c['center'],c['hip'])),'neck':xy(c['neck']),'head':xy(c['head'])}
 for side in ['L','R']:
  for k,p in zip(['shoulder','elbow','wrist','finger','hip','knee','ankle','toe'],c[side]):rest[side+k]=xy(p)
 C={k:n['empty'](s,P+'CTRL '+k,p,root) for k,p in rest.items()};bones={'torso':('hip','neck'),'head':('neck','head')}
 for side in ['L','R']:
  for k,a,z in [('upperarm','shoulder','elbow'),('forearm','elbow','wrist'),('hand','wrist','finger'),('thigh','hip','knee'),('calf','knee','ankle'),('foot','ankle','toe')]:bones[side+k]=(side+a,side+z)
 ad=bpy.data.armatures.new(P+'fitted bones');arm=bpy.data.objects.new(ad.name,ad);s.collection.objects.link(arm);arm.parent=root;bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);bpy.context.view_layer.objects.active=arm;bpy.ops.object.mode_set(mode='EDIT')
 for k,(a,z) in bones.items():eb=ad.edit_bones.new(k);eb.head=rest[a];eb.tail=rest[z]
 bpy.ops.object.mode_set(mode='OBJECT')
 for k,(a,z) in bones.items():
  pb=arm.pose.bones[k];co=pb.constraints.new('COPY_LOCATION');co.target=C[a];co=pb.constraints.new('STRETCH_TO');co.target=C[z];co.rest_length=(rest[z]-rest[a]).length;co.volume='NO_VOLUME';co.bulge=0
 nx,ny=90,164;x0,y0,x1,y1=c['box'];pixels=[(x0+(x1-x0)*i/nx,y0+(y1-y0)*j/ny) for j in range(ny+1) for i in range(nx+1)];verts=[xy(p) for p in pixels]
 rgba=np.empty(W*H*4,np.float32);im.pixels.foreach_get(rgba);alpha=rgba.reshape(H,W,4)[::-1,:,3]
 # A grid cell can include the next row's hair between this player's boots.
 # Own only the connected whole character, not every opaque pixel in its box.
 allowed=alpha>.93;owned=np.zeros((H,W),bool);seed=(int(c['hip']-40),int(c['center']));todo=deque([seed]);owned[seed]=True
 while todo:
  yy,xx=todo.popleft()
  for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
   y,x=yy+dy,xx+dx
   if y0<=y<y1 and x0<=x<x1 and not owned[y,x] and allowed[y,x]:owned[y,x]=True;todo.append((y,x))
 alpha=alpha*owned;valid=np.array([alpha[min(H-1,round(py)),min(W-1,round(px))]>.93 for px,py in pixels]).reshape(ny+1,nx+1)
 faces=[]
 for j in range(ny):
  for i in range(nx):
   idx=j*(nx+1)+i
   # Same transparent-grid removal as v016, before rig deformation.
   px0,py0=pixels[idx];px1,py1=pixels[idx+nx+2]
   if alpha[int(py0):min(H,int(py1)+2),int(px0):min(W,int(px1)+2)].max()>.93:faces.extend([(idx,idx+1,idx+nx+2),(idx,idx+nx+2,idx+nx+1)])
 me=bpy.data.meshes.new(P+'complete neutral drawing');me.from_pydata(verts,[],faces);me.materials.append(material);uv=me.uv_layers.new()
 for loop in me.loops:px,py=pixels[loop.vertex_index];uv.data[loop.index].uv=(px/W,1-py/H)
 skin=bpy.data.objects.new(me.name,me);s.collection.objects.link(skin);skin.parent=root;names=list(bones);weights=np.zeros((len(pixels),len(names)));groups=[skin.vertex_groups.new(name=k) for k in names];ratio=(c['floor']-c['top'])/980
 def near(pt,options):
  ds=sorted((n['old']['segment_distance'](pt,rest[bones[k][0]],rest[bones[k][1]]),k) for k in options)[:2];ww=[math.exp(-(d*d-ds[0][0]**2)/.0025) for d,k in ds];return {k:w/sum(ww) for (_,k),w in zip(ds,ww)}
 for i,(pt,(px,py)) in enumerate(zip(verts,pixels)):
  side='L' if px<c['center'] else 'R';neck=c['neck'][1];hip=c['hip'];width=np.interp(py,[r[0] for r in c['edge']],[r[1] for r in c['edge']])
  if py<neck-26*ratio:w={'head':1}
  elif py<neck+6*ratio:t=max(0,min(1,(neck+6*ratio-py)/(32*ratio)));w={'head':t,'torso':1-t}
  elif py<hip-40*ratio:
   t=max(0,min(1,(abs(px-c['center'])-width)/(30*ratio)));w={k:v*t for k,v in near(pt,[side+'upperarm',side+'forearm',side+'hand']).items()};w['torso']=1-t
  elif py<hip+100*ratio and abs(px-c['center'])>.82*abs(c[side][2][0]-c['center']):w=near(pt,[side+'forearm',side+'hand'])
  elif py<hip:w={'torso':1}
  else:
   w=near(pt,[side+'thigh',side+'calf',side+'foot']);t=max(0,min(1,(hip+38*ratio-py)/(38*ratio)));w={k:v*(1-t) for k,v in w.items()};w['torso']=t
  for k,v in w.items():weights[i,names.index(k)]=v
 w=weights.reshape(ny+1,nx+1,-1);prior=w.copy()
 for iteration in range(95):
  total=w.copy();count=np.ones((ny+1,nx+1,1))
  for axis in [0,1]:
   for shift in [-1,1]:
    mask=np.roll(valid[:,:,None],shift,axis)
    if axis==0:mask[0 if shift==1 else -1,:,:]=False
    else:mask[:,0 if shift==1 else -1,:]=False
    total+=np.roll(w,shift,axis)*mask;count+=mask
  w=.35*w+.65*total/count
  w[np.array([y0+(y1-y0)*j/ny<c['neck'][1]-32*ratio for j in range(ny+1)])]=prior[np.array([y0+(y1-y0)*j/ny<c['neck'][1]-32*ratio for j in range(ny+1)])]
 weights=w.reshape(-1,len(names));weights/=weights.sum(1,keepdims=True)
 for i,(px,py) in enumerate(pixels):
  ankle_y=(c['L'][6][1]+c['R'][6][1])/2;t=smooth((py-ankle_y+10*ratio)/(32*ratio))
  if t>0:weights[i]*=1-t;weights[i,names.index(('L' if px<c['center'] else 'R')+'foot')]+=t
  for k,val in enumerate(weights[i]):
   if val>1e-7:groups[k].add([i],float(val),'REPLACE')
  # Same semantic depth layering accepted in batch one.
  me.vertices[i].co.z=sum(weights[i,j]*(.018 if k.endswith('hand') else .013 if k.endswith('forearm') else .006 if k.endswith('upperarm') else 0) for j,k in enumerate(names))
 mod=skin.modifiers.new('v016 continuous source fitted deformation','ARMATURE');mod.object=arm;mod.use_deform_preserve_volume=True
 a=dict(name=name,kind=kind,root=root,skin=skin,C=C,rest=rest,arm=arm,s=s,cfg=c,pixels=pixels,unit=unit,height=height,base=Vector(loc),face=face);actors[name]=a;return a

def retire(a):
 for ob in [a['root'],*a['root'].children_recursive]:
  ob.hide_render=True;ob.hide_viewport=True
  for prop in ['hide_render','hide_viewport']:
   try:ob.driver_remove(prop)
   except Exception:pass
  for fc in curves(ob):
   if fc.data_path in ['hide_render','hide_viewport']:
    for k in fc.keyframe_points:k.co.y=1
 for ob in s.objects:
  if 'contact shadow' in ob.name and any(getattr(co,'target',None)==a['root'] for co in ob.constraints):
   ob.hide_render=ob.hide_viewport=True
   for prop in ['hide_render','hide_viewport']:
    try:ob.driver_remove(prop)
    except Exception:pass

def show(a,start,end):
 q['show'](a['root'],start,end)

def write_pose(a,f,p,loc=None):
 for k,v in p.items():key(a['C'][k],'location',f,v)
 if loc is not None:key(a['root'],'location',f,loc)

def pose(a,lean=0,down=0,ua=(0,0),fa=(0,0),hands=(0,0),head=0,shift=0):
 r=a['rest'];p={k:v.copy() for k,v in r.items()};p['hip']+=Vector((shift,down,0))
 for k in ['neck','Lshoulder','Rshoulder']:p[k]=p['hip']+rotate(r[k]-r['hip'],lean)
 p['head']=p['neck']+rotate(r['head']-r['neck'],lean+head)
 for i,side in enumerate(['L','R']):
  p[side+'hip']+=p['hip']-r['hip']
  for lab,prev,ang in [('elbow','shoulder',ua[i]),('wrist','elbow',ua[i]+fa[i]),('finger','wrist',ua[i]+fa[i]+hands[i])]:p[side+lab]=p[side+prev]+rotate(r[side+lab]-r[side+prev],ang+lean)
  projected_knee(a,p,side)
 return p

def projected_knee(a,p,side):
 r=a['rest'];t=(r[side+'knee'].y-r[side+'hip'].y)/(r[side+'ankle'].y-r[side+'hip'].y);p[side+'knee']=p[side+'hip'].lerp(p[side+'ankle'],t);p[side+'knee'].x+=(-.007 if side=='L' else .007)

def step(a,p,rootx,rooty,side,footx,footlift):
 r=a['rest'];sgn=-1 if a['face'] else 1;scale=a['height']/1.8;p[side+'ankle']=r[side+'ankle']+Vector(((footx-rootx)*sgn/scale,footlift/scale,0));p[side+'toe']=p[side+'ankle']+r[side+'toe']-r[side+'ankle'];projected_knee(a,p,side)

def sample(fr,knots):
 for (f0,v0),(f1,v1) in zip(knots,knots[1:]):
  if fr<=f1:return v0+(v1-v0)*smooth((fr-f0)/(f1-f0))
 return knots[-1][1]

def preview(f,path):
 s.frame_set(f);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=f),key=lambda m:m.frame).camera;s.render.resolution_percentage=100;s.render.use_sequencer=False;s.render.use_border=False;s.render.image_settings.file_format='PNG';s.render.filepath=str(O/path);bpy.ops.render.render(write_still=True);return str(O/path)

bpy.app.driver_namespace['cast21']=globals()

def animate_saka():
 a=actors['Saka'];r=a['rest'];base=a['base'];scale=a['height']/1.8
 # Whole performance: look up, signal, lower arms, three approach steps,
 # planted support, backswing, sharp contact, follow-through, balanced recovery.
 for f in range(1,270):
  signal=sample(f,[(1,0),(20,0),(34,1),(55,1),(72,0),(269,0)])
  x=sample(f,[(1,-.70),(86,-.70),(99,-.90),(112,-.90),(127,-.59),(144,-.29),(160,0),(269,0)])
  wind=smooth((f-150)/10)*(1-smooth((f-160)/8));strike=smooth((f-160)/8);follow=smooth((f-168)/8);recover=smooth((f-179)/17)
  lean=sample(f,[(1,0),(25,-.025),(52,0),(112,0),(154,-.045),(168,.04),(178,.065),(196,0),(269,0)])
  balance=max(wind,.85*strike*(1-recover));p=pose(a,lean=lean,down=-.015*wind,ua=(-1.05*signal-.65*balance,.11*signal+.33*wind-.25*strike*(1-recover)),fa=(-1.05*signal-.30*balance,-.25*wind-.20*strike*(1-recover)),head=.04*math.sin(f*.05)*(1-smooth((f-110)/12)))
  for side,knots,swings in [('L',[(1,-.70),(87,-.70),(99,-.90),(113,-.90),(127,-.59),(145,-.59),(160,0),(269,0)],[(87,99),(113,127),(145,160)]),('R',[(1,-.70),(99,-.70),(110,-.90),(128,-.90),(144,-.29),(156,-.29),(165,0),(269,0)],[(99,110),(128,144),(156,165)])]:
   foot=sample(f,knots);lift=sum(.05*math.sin(math.pi*(f-a)/(z-a)) for a,z in swings if a<f<z);step(a,p,base.x+x,base.y,side,base.x+foot,lift)
  if f>=150:
   dx=sample(f,[(150,0),(160,-.13),(168,.17),(176,.35),(187,.15),(198,0),(269,0)]);dy=sample(f,[(150,0),(160,.13),(168,.015),(176,.24),(187,.09),(198,0),(269,0)])
   p['Rankle']=r['Rankle']+Vector((dx,dy,0));p['Rtoe']=p['Rankle']+rotate(r['Rtoe']-r['Rankle'],.12*follow*(1-recover));projected_knee(a,p,'R')
   p['Relbow']=p['Rshoulder']+rotate(r['Relbow']-r['Rshoulder'],.33*wind-.40*follow*(1-recover)+lean);p['Rwrist']=p['Relbow']+rotate(r['Rwrist']-r['Relbow'],.10*wind-.50*follow*(1-recover)+lean);p['Rfinger']=p['Rwrist']+rotate(r['Rfinger']-r['Rwrist'],.10*wind-.50*follow*(1-recover)+lean)
  write_pose(a,f,p,base+Vector((x,0,0)))
 for ob in [a['root'],*a['C'].values()]:
  for fc in curves(ob):
   if fc.data_path!='scale':
    for k in fc.keyframe_points:k.interpolation='LINEAR'
 return {'frames':269,'contact':168,'rest_frames':[1,205,269]}

def build_remaining():
 for name,kind,height,loc,face in [('Gabriel','Gabriel',1.90,(0,49.1,0),0),('opposition defender 0','Opponent',1.83,(-1.8,49.5,0),0),('opposition defender 1','Opponent',1.83,(2.1,48.7,0),0),('opposition goalkeeper','Raya',1.86,(1,52,0),0),('Raya','Raya',1.83,(.35,-50.35,0),math.pi),('opposing attacker','Opponent',1.82,(-4.5,-47.5,0),math.pi)]:
  a=make(name,kind,height,loc,face);retire(oldactors[name]);show(a,1 if face==0 else 392,269 if face==0 else 1047)
 # Neutral wall drawings: individually measured row/cell centres, source-connected silhouettes.
 for i,(cx,top,floor) in enumerate([(197,15,530),(520,14,530),(851,23,530),(194,525,1037),(512,528,1037),(847,535,1037),(190,1039,1528),(509,1030,1528),(847,1038,1528)]):
  h=floor-top;u=h/515
  def pt(x,y):return (cx+x*u,top+y*u)
  c=cfg((cx-145*u,top-4,cx+145*u,min(1535,floor+3)),cx,top,floor,top+313*u,pt(0,129),pt(12,65),[pt(-69,164),pt(-89,229),pt(-109,304),pt(-112,337),pt(-34,315),pt(-53,382),pt(-73,477),pt(-103,503)],[pt(69,164),pt(89,229),pt(109,304),pt(112,337),pt(34,315),pt(53,382),pt(73,477),pt(103,503)],[(top+y*u,w*u) for y,w in [(130,28),(171,49),(219,49),(273,53),(288,55)]])
  kind='wall-'+str(i);CONFIG[kind]=c;name='wall '+str(i+1);height=[1.90,1.92,1.78,1.85,1.78,1.80,1.79,1.82,1.77][i]
  # Same hero identity/construction in the corner and the wall.
  usekind='Gabriel' if i==0 else 'Saka' if i==2 else kind
  a=make(name,usekind,height,((i-4)*1.05,-51.7,0),math.pi,'football.png' if i in [0,2] else 'wall.png');retire(oldactors[name]);show(a,392,1047)
 # Opposing goalkeeper has a separate purple uniform while retaining complete drawn body.
 skin=actors['opposition goalkeeper']['skin'];m=skin.data.materials[0];nodes=m.node_tree.nodes;links=m.node_tree.links;tex=next(nd for nd in nodes if nd.type=='TEX_IMAGE');sep=nodes.new('ShaderNodeSeparateColor');links.new(tex.outputs['Color'],sep.inputs[0]);gt=nodes.new('ShaderNodeMath');gt.operation='GREATER_THAN';links.new(sep.outputs['Green'],gt.inputs[0]);gt.inputs[1].default_value=.5;lt=nodes.new('ShaderNodeMath');lt.operation='LESS_THAN';links.new(sep.outputs['Blue'],lt.inputs[0]);lt.inputs[1].default_value=.15;mul=nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';links.new(gt.outputs[0],mul.inputs[0]);links.new(lt.outputs[0],mul.inputs[1]);mix=nodes.new('ShaderNodeMixRGB');links.new(mul.outputs[0],mix.inputs[0]);links.new(tex.outputs['Color'],mix.inputs[1]);mix.inputs[2].default_value=(.17,.12,.35,1);em=next(nd for nd in nodes if nd.type=='EMISSION');links.new(mix.outputs[0],em.inputs[0])
 return list(actors)

def animate_remaining():
 G=actors['Gabriel'];K=actors['opposition goalkeeper'];R=actors['Raya'];D=[actors['opposition defender '+str(i)] for i in range(2)]
 for f in range(1,270):
  # Gabriel tracks the cross, dips, jumps, heads, absorbs landing then celebrates.
  prep=smooth((f-194)/8)*(1-smooth((f-202)/3));t=(f-204)/27;jump=.42*4*t*(1-t) if 0<t<1 else 0;land=math.sin(math.pi*(f-231)/12) if 231<f<243 else 0;hit=smooth((f-214)/3)*(1-smooth((f-219)/7));celebrate=smooth((f-246)/9)
  reach=smooth((f-201)/8)*(1-smooth((f-224)/12));p=pose(G,lean=-.04*prep-.10*hit,down=-.085*prep-.065*land,ua=(-.48*reach-.7*celebrate,.43*reach+.62*celebrate),fa=(-.6*reach-.45*celebrate,.55*reach+.35*celebrate),head=.06*prep-.12*hit)
  if jump>0:
   for side in ['L','R']:
    p[side+'ankle'].y+=.07*jump/.42;p[side+'toe'].y+=.07*jump/.42;projected_knee(G,p,side)
  write_pose(G,f,p,G['base']+Vector((.07*hit,0,jump)))
  for i,a in enumerate(D):
   anticipation=smooth((f-182-i*3)/12);block=smooth((f-206-i*3)/6)*(1-smooth((f-222)/8));recoil=smooth((f-227)/6)*(1-smooth((f-242)/12));p=pose(a,lean=(-.035 if i==0 else .035)*anticipation+.05*recoil,down=-.045*block,ua=(-.30*anticipation-.45*block,.28*anticipation+.5*block),fa=(-.28*block,.25*block),head=-.06*anticipation+.07*recoil);write_pose(a,f,p)
  ready=smooth((f-181)/13);save=smooth((f-218)/9)*(1-smooth((f-238)/14));despair=smooth((f-245)/10);p=pose(K,lean=-.10*save,down=-.04*ready,ua=(-.35*ready-.75*save-.28*despair,.3*ready+.5*save+.28*despair),fa=(-.25*ready-.4*save,.25*ready+.4*save),head=-.06*save);
  reach=smooth((f-221)/9)*(1-smooth((f-239)/13));p=pose(K,lean=.08*reach,down=-.055*smooth((f-215)/6)*(1-smooth((f-222)/5)),ua=(-.22*ready,.35*ready+.85*reach),fa=(-.35*ready,.28*ready+.40*reach),head=-.055*reach);write_pose(K,f,p,K['base']+Vector((.32*smooth((f-222)/12),0,0)))
 for f in range(392,1048):
  for i in range(9):
   a=actors['wall '+str(i+1)];base=a['base'];start=398+i*3;dx=-(i-4)*.35;count=max(1,math.ceil(abs(dx)/.28));duration=count*14;phase=max(0,min(count*2,(f-start)/7));pair=min(count,math.floor(phase/2));local=phase-2*pair
   lead='L' if dx>0 else 'R';travel={};lifts={}
   for side in ['L','R']:
    frac=max(0,min(1,local-(0 if side==lead else 1)));travel[side]=dx/count*(pair+smooth(frac));lifts[side]=.035*math.sin(math.pi*frac) if pair<count else 0
   x=base.x+(travel['L']+travel['R'])/2;t=smooth((f-start)/duration);guard=smooth((f-start-duration+3)/12);flinch=smooth((f-585-i*2)/6)*(1-smooth((f-598-i*2)/10));p=pose(a,lean=(-.014 if i%2 else .014)*math.sin(t*math.pi),down=-.012*math.sin(phase*math.pi)-.035*flinch,ua=(.36*guard-.10*flinch,-.36*guard+.10*flinch),fa=(.22*guard,-.22*guard),head=.025*math.sin((f-i*5)*.045)*guard)
   for side in ['L','R']:step(a,p,x,base.y,side,base.x+travel[side],lifts[side])
   write_pose(a,f,p,(x,base.y,0))
  # Raya steps out in front and gestures back at the absurdly large protective wall.
  t=smooth((f-469)/28);base=R['base'];x=base.x+.32*t;present=smooth((f-527)/10)*(1-smooth((f-559)/12));look=smooth((f-571)/9)*(1-smooth((f-618)/10));settle=smooth((f-632)/10)*(1-smooth((f-676)/12));p=pose(R,lean=.025*present,down=-.012*math.sin(t*math.pi),ua=(-.55*present-.15*settle,.50*present+.18*settle),fa=(-.70*present,.70*present),head=-.075*look)
  for side,first,last in [('L',469,481),('R',484,497)]:
   u=smooth((f-first)/(last-first));lift=.04*math.sin(math.pi*max(0,min(1,(f-first)/(last-first))));step(R,p,x,base.y,side,base.x+.32*u,lift)
  write_pose(R,f,p,(x,base.y,0))
  a=actors['opposing attacker'];reaction=smooth((f-535)/10)*(1-smooth((f-570)/14));p=pose(a,ua=(-.38*reaction,.38*reaction),fa=(-.65*reaction,.65*reaction),lean=-.035*reaction,head=.035*reaction);write_pose(a,f,p)
 for a in actors.values():
  for ob in [a['root'],*a['C'].values()]:
   for fc in curves(ob):
    if fc.data_path!='scale':
     for kp in fc.keyframe_points:kp.interpolation='LINEAR'
 return {'reconstructed_players':len(actors),'kept_performances':['Arteta','Gyokeres']}

def ball_contacts():
 ball=q['ball'];a=actors['Saka'];s.frame_set(168);bpy.context.view_layer.update()
 foot=a['arm'].pose.bones['Rfoot'];point=Vector(((470-a['cfg']['center'])*a['unit'],(a['cfg']['floor']-776)*a['unit'],0));toe=a['root'].matrix_world@(foot.matrix@foot.bone.matrix_local.inverted()@point)
 # Fix the physical location first: centre well inside the 1m corner quadrant.
 contact=Vector((-33.48,51.98,.11));dx=math.sqrt(.11**2-(contact.z-toe.z)**2);delta=Vector((contact.x-toe.x-dx,contact.y-toe.y,0))
 a['base']+=delta
 for fc in curves(a['root']):
  if fc.data_path=='location':
   for kp in fc.keyframe_points:
    kp.co.y+=delta[fc.array_index];kp.handle_left.y+=delta[fc.array_index];kp.handle_right.y+=delta[fc.array_index]
 s.frame_set(168);bpy.context.view_layer.update();toe=a['root'].matrix_world@(foot.matrix@foot.bone.matrix_local.inverted()@point)
 # Contact is on the visible upper forehead, transformed by the actual head bone.
 # The old head-control centre sat inside the skull and made the ball overlap the face.
 g=actors['Gabriel'];s.frame_set(217);bpy.context.view_layer.update();c=g['cfg'];pt=Vector(((801-c['center'])*g['unit'],(c['floor']-60)*g['unit'],0))
 pb=g['arm'].pose.bones['head'];surface=g['root'].matrix_world@(pb.matrix@pb.bone.matrix_local.inverted()@pt)
 normal=Vector((.27,-.12,.955)).normalized();head=surface+.11*normal;end=Vector((2.9,54.39,1.15))
 for f in range(1,270):
  if f<168:p=contact
  elif f<=217:
   u=(f-168)/49;p=contact.lerp(head,u);p.z+=1.65*4*u*(1-u);p.y+=1.20*math.sin(math.pi*u)
  elif f<=238:
   u=(f-217)/21;p=head.lerp(end,u);p.z+=.08*math.sin(math.pi*u)
  else:
   dt=(f-238)/24;p=Vector((2.9,54.39-.37*min(1,dt/.5),max(.11,1.15-4.905*dt*dt)))
  key(ball,'location',f,p)
 camera=next(m.camera for m in s.timeline_markers if m.frame==1);camera.data.lens=43;camera.rotation_euler=(Vector((-33.95,51.98,1.0))-camera.location).to_track_quat('-Z','Y').to_euler()
 for a in actors.values():
  root=a['root'];sh=q['surface']('v021 contact shadow',[(.34*math.cos(t),.14*math.sin(t),.008) for t in np.linspace(0,math.tau,33)[:-1]],'#527b46');co=sh.constraints.new('COPY_LOCATION');co.target=root;co.use_z=False
  for prop in ['hide_render','hide_viewport']:
   dr=sh.driver_add(prop).driver;dr.expression='abs(v) < .001';v=dr.variables.new();v.name='v';v.type='TRANSFORMS';v.targets[0].id=root;v.targets[0].transform_type='SCALE_X';v.targets[0].transform_space='LOCAL_SPACE'
 checks={'kick_frame':168,'ball_start':list(contact),'corner_radius':math.hypot(contact.x+34,contact.y-52.5),'boot_to_ball_center':(toe-contact).length,'header_frame':217,'forehead_surface':list(surface),'header_ball_center':list(head),'header_surface_distance':(head-surface).length}
 assert checks['corner_radius']+.11<1 and abs(checks['boot_to_ball_center']-.11)<.015
 assert abs(checks['header_surface_distance']-.11)<1e-5
 (O/'contact-checks.json').write_text(json.dumps(checks,indent=2));return checks

def save():
 rows=json.loads((V/'artifacts/defence-v020/edit.json').read_text())
 for row in rows:row['scene']=row['scene'].replace('defence_v020','defence_v021')
 (O/'edit.json').write_text(json.dumps(rows,indent=2));s.frame_set(35);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=35),key=lambda m:m.frame).camera
 bpy.data.libraries.write(str(O/'batch02-v021.blend'),{s,room},fake_user=True)
 (O/'cast.json').write_text(json.dumps({k:{'root':a['root'].name,'skin':a['skin'].name,'armature':a['arm'].name,'controls':{k:v.name for k,v in a['C'].items()},'rest':{k:list(v) for k,v in a['rest'].items()},'cfg':a['cfg'],'construction':'neutral full-body drawing; v016 fitted continuous mesh; alpha-aware weights; rigid shoes; semantic depth'} for k,a in actors.items()},indent=2));return str(O/'batch02-v021.blend')

def finish_uniform_and_scene():
 # Uniform selection is a source-space clothing mask, not a brightness guess.
 sk=actors['opposition goalkeeper']['skin'];m=sk.data.materials[0];nd=m.node_tree.nodes;lk=m.node_tree.links;tex=next(x for x in nd if x.type=='TEX_IMAGE');mix=next(x for x in nd if x.type=='MIX_RGB');hue=next((x for x in nd if x.type=='HUE_SAT'),None) or nd.new('ShaderNodeHueSaturation');hue.inputs['Hue'].default_value=.08;hue.inputs['Saturation'].default_value=.72;lk.new(tex.outputs['Color'],hue.inputs['Color']);lk.new(hue.outputs[0],mix.inputs[2]);tc=nd.new('ShaderNodeTexCoord');sep=nd.new('ShaderNodeSeparateXYZ');lk.new(tc.outputs['UV'],sep.inputs[0])
 def mathnode(op,a,z):
  out=nd.new('ShaderNodeMath');out.operation=op
  for i,v in enumerate([a,z]):
   if isinstance(v,(int,float)):out.inputs[i].default_value=v
   else:lk.new(v,out.inputs[i])
  return out.outputs[0]
 y=sep.outputs['Y'];torso=mathnode('MULTIPLY',mathnode('GREATER_THAN',y,1-1272/1536),mathnode('LESS_THAN',y,1-932/1536));socks=mathnode('MULTIPLY',mathnode('GREATER_THAN',y,1-1462/1536),mathnode('LESS_THAN',y,1-1320/1536));lk.new(mathnode('MAXIMUM',torso,socks),mix.inputs[0])
 # Unlink superseded trial rigs from this revision; their saved v020 file remains.
 keep={a['root'] for a in actors.values()};oldroots={a['root'] for k,a in oldactors.items() if k not in ['Arteta','Gyokeres']};oldroots|={o for o in s.objects if o.name.startswith('B21 / ') and o.name.split(' / ')[-1].startswith('character') and o not in keep};dead=set()
 for root in oldroots:dead.update([root,*root.children_recursive])
 seen=set()
 for ob in list(s.objects):
  if 'contact shadow' not in ob.name:continue
  target=next((co.target for co in ob.constraints if co.type=='COPY_LOCATION'),None)
  if target in oldroots or target in seen:dead.add(ob)
  else:seen.add(target)
 for ob in dead:
  for col in list(ob.users_collection):
   if col==s.collection:col.objects.unlink(ob)
 return {'superseded_objects_unlinked':len(dead)}
