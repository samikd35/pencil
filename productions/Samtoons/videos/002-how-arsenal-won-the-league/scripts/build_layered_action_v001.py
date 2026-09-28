"""Editable eight-second layered-body proof. Live Blender only; preserves all earlier scenes.
Reuses episode 001 native material/polygon primitives and its joint-target convention.
Body surfaces follow explicit limb paths, never a globally weighted illustration.
"""
import bpy, ast, math, json
from pathlib import Path
from mathutils import Vector
ROOT=Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/002-how-arsenal-won-the-league')
WORK=ROOT.parents[3];OUT=ROOT/'artifacts/layered-action-v001';NAME='S002_layered_action_v001'
assert bpy.context.window and not bpy.app.background
assert NAME not in bpy.data.scenes and not OUT.exists()
old=bpy.context.scene
s=bpy.data.scenes.new(NAME);bpy.context.window.scene=s
skin=bpy.data.collections.new(NAME+' artwork');s.collection.children.link(skin)
INK='#25222a'
# Import inspected pure functions only; historical builders have side effects.
for path,names in [(WORK/'experiments/008_cartoon_skin/build_skin.py',{'material','polygon','oval'}),(ROOT.parent/'001-manchester-derby-2026-09-13/scripts/build_staging.py',{'mat','poly','rect','empty','line','text'})]:
 tree=ast.parse(path.read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(path),'exec'))
M={};INK='#25222a';ink=mat(INK);font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf')
s.world=old.world;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=32
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=192
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.use_sequencer=False
s.view_settings.view_transform='Standard';s.view_settings.look='None'
d=bpy.data.cameras.new(NAME+' camera');d.type='ORTHO';d.ortho_scale=16
cam=bpy.data.objects.new(d.name,d);skin.objects.link(cam);cam.location=(0,.65,25);s.camera=cam
# Quiet native stadium. No reused character shadows or unattached props.
rect('Proof / sky',-12,-8,24,18,-10,'#d9e8ed',outline=False)
rect('Proof / stands',-12,-.7,24,4.6,-9,'#a6b7c2',outline=False)
rect('Proof / fascia',-12,3.0,24,.55,-8.8,'#ad2639',outline=False)
for row in range(3):
 for col in range(42):
  x=-12+col*.6;y=.1+row*.66
  poly('Proof / crowd',oval(x,y,.18,.22),-8.5,'#8193a1',outline=False)
rect('Proof / pitch',-12,-8,24,7.3,-8,'#6d9e59',outline=False)
for x in range(-12,12,4):rect('Proof / grass stripe',x,-8,2,7.3,-7.9,'#75a85f',outline=False)
line('Proof / touchline',[(-12,-2.35),(12,-2.35)],-7.5,'#f6f4df',.025)
root=empty('Gyokeres layered / ROOT',(0,0,0))
torso=empty('Gyokeres layered / torso',(0,0,0),root)
controls={}
for name in ['hipL','kneeL','ankleL','hipR','kneeR','ankleR','shoulderL','elbowL','handL','shoulderR','elbowR','handR']:
 controls[name]=empty('Gyokeres layered / CTRL '+name,(0,0,0),root)
# Hermite weights: same three control points generate body, outlines and garment sections.
def basis(t):
 segment=min(1,int(t));u=t-segment
 h00=2*u**3-3*u*u+1;h10=u**3-2*u*u+u;h01=-2*u**3+3*u*u;h11=u**3-u*u
 if segment==0:return (h00-h10-.5*h11,h10+h01,.5*h11)
 return (-.5*h10,h00-h11,.5*h10+h01+h11)
def driver(block,path,index,targets,expression):
 dr=block.driver_add(path,index).driver
 for axis in ['X','Y']:
  for letter,target in zip('abc',targets):
   v=dr.variables.new();v.name=letter+axis.lower();v.type='TRANSFORMS';v.targets[0].id=target;v.targets[0].transform_type='LOC_'+axis;v.targets[0].transform_space='LOCAL_SPACE'
 dr.expression=expression

def limb(name,targets,widths,color,z,start=0,end=2):
 samples=25
 params=[start+(end-start)*i/(samples-1) for i in range(samples)]
 # Shared path means sleeves/socks cannot drift from their limb. No visible joint discs.
 points=[]
 for sign,ts in [(1,params),(-1,list(reversed(params)))]:
  for t in ts:
   weights=basis(t);e=.0001;lo=max(0,t-e);hi=min(2,t+e)
   dw=[(v-u)/(hi-lo) for u,v in zip(basis(lo),basis(hi))]
   cx='+'.join(f'{w:.8f}*{n}x' for w,n in zip(weights,'abc'));cy='+'.join(f'{w:.8f}*{n}y' for w,n in zip(weights,'abc'))
   dx='+'.join(f'{w:.8f}*{n}x' for w,n in zip(dw,'abc'));dy='+'.join(f'{w:.8f}*{n}y' for w,n in zip(dw,'abc'))
   radius=widths[0]*(1-t/2)+widths[1]*t/2
   den=f'sqrt(({dx})**2+({dy})**2+0.000001)'
   points.append((f'({cx})-({dy})/{den}*{radius*sign}',f'({cy})+({dx})/{den}*{radius*sign}'))
 ob=poly(name,[(0,0)]*len(points),z,color,root)
 edge=next(o for o in skin.objects if o.name==ob.name+' outline')
 for i,(ex,ey) in enumerate(points):
  for axis,expr in enumerate([ex,ey]):
   driver(ob.data.vertices[i],'co',axis,targets,expr)
   driver(edge.data.splines[0].points[i],'co',axis,targets,expr)
 return ob
# Torso is a clean designed shape. Kit graphics stay rigid to its control.
poly('Gyokeres / jersey',[(-.34,-.10),(.38,-.10),(.48,.45),(.48,1.18),(.32,1.50),(-.28,1.52),(-.50,1.19),(-.46,.42)],2.45,'#d91935',torso)
poly('Gyokeres / jersey shade',[(-.46,.42),(-.35,-.10),(.38,-.10),(.43,.17),(-.21,.10)],2.47,'#b91931',torso,False)
text('Gyokeres / Emirates','Emirates',0,.91,2.50,.20,'#fff8ed',torso)
text('Gyokeres / sponsor small','FLY BETTER',0,.68,2.50,.095,'#fff8ed',torso)
poly('Gyokeres / crest',[(.22,1.32),(.36,1.32),(.35,1.16),(.29,1.10),(.23,1.16)],2.50,'#efcb74',torso)
line('Gyokeres / crest cannon',[(.25,1.24),(.34,1.24)],2.53,'#a72336',.012,torso)
for x in [-.32,-.27,-.22]:line('Gyokeres / shoulder stripe',[(x,1.45),(x-.15,1.30)],2.51,'#fff8ed',.012,torso)
# Drawn neck is continuous under the cropped approved jaw/neck artwork.
poly('Gyokeres / neck',[(-.22,1.35),(.24,1.35),(.24,1.94),(-.25,1.94)],2.55,'#efb77f',torso,False)
line('Gyokeres / collar',[(-.28,1.49),(-.15,1.37),(.06,1.35),(.29,1.49)],2.62,'#fff7ee',.048,torso)
# Use original approved image pixels as registered native head artwork, not whole-body deformation.
mathead=bpy.data.materials['TR02 / character artwork'].copy();mathead.name='Gyokeres / approved head pixels'
pts=[(263,0),(465,0),(465,178),(429,205),(428,219),(346,219),(329,182),(282,171),(263,121)]
verts=[((x-387)*.0084,1.73+(219-y)*.0084,2.7) for x,y in pts]
me=bpy.data.meshes.new('Gyokeres / head drawing');me.from_pydata(verts,[],[tuple(range(len(verts)))]);me.materials.append(mathead)
uv=me.uv_layers.new()
for loop in me.loops:
 x,y=pts[loop.vertex_index];uv.data[loop.index].uv=(x/1536,1-y/1024)
head=bpy.data.objects.new(me.name,me);skin.objects.link(head);head.parent=torso
for side,z in [('L',2.15),('R',2.75)]:
 leg=[controls[p+side] for p in ['hip','knee','ankle']]
 arm=[controls[p+side] for p in ['shoulder','elbow','hand']]
 limb('Gyokeres / '+side+' leg',leg,(.18,.105),'#efb77f',z)
 limb('Gyokeres / '+side+' shorts',leg,(.27,.22),'#fff8ed',z+.04,0,.47)
 limb('Gyokeres / '+side+' sock',leg,(.18,.13),'#d91935',z+.06,1.10,2)
 limb('Gyokeres / '+side+' sock cuff',leg,(.19,.14),'#fff8ed',z+.08,1.10,1.19)
 limb('Gyokeres / '+side+' arm',arm,(.145,.095),'#efb77f',z+.12)
 limb('Gyokeres / '+side+' sleeve',arm,(.23,.17),'#fff8ed',z+.15,0,.57)
 limb('Gyokeres / '+side+' cuff',arm,(.235,.175),'#d91935',z+.18,.50,.60)
 ankle=controls['ankle'+side];hand=controls['hand'+side]
 # Art is attached to the endpoint that drives the limb, as in episode 001.
 poly('Gyokeres / '+side+' boot',[(-.18,.10),(.10,.08),(.19,-.04),(.40,-.12),(.42,-.22),(-.20,-.22)],z+.12,'#f9efcf',ankle)
 line('Gyokeres / '+side+' sole',[(-.18,-.19),(.39,-.19)],z+.16,'#d91935',.035,ankle)
 for x in [-.04,.025,.09]:line('Gyokeres / boot lace',[(x,-.03),(x+.06,-.08)],z+.16,'#806d52',.009,ankle)
 poly('Gyokeres / '+side+' hand',[(-.105,.05),(-.12,-.10),(-.055,-.21),(.07,-.21),(.13,-.11),(.12,.02),(.06,.07)],z+.3,'#efb77f',hand)
 line('Gyokeres / '+side+' knuckles',[(-.07,-.10),(.07,-.10)],z+.32,'#b2774d',.008,hand)
shadow=poly('Gyokeres / contact shadow',oval(0,-2.33,.7,.10),-7.2,'#4b783e',outline=False)

def rotate(p,a):return Vector((p[0]*math.cos(a)-p[1]*math.sin(a),p[0]*math.sin(a)+p[1]*math.cos(a),0))
def ik(h,a,length=1.20):
 delta=a-h;dist=delta.length
 assert dist<2*length, (dist,h,a)
 middle=(h+a)*.5;normal=Vector((-delta.y,delta.x,0)).normalized()
 return middle+normal*math.sqrt(max(0,length*length-dist*dist/4))
def smooth(t):return t*t*(3-2*t)
def foot_run(f,offset):
 q=(f-1+offset)/20;cycle=math.floor(q);phase=q-cycle
 plant=-4.8+cycle*1.4+.45-offset*.07
 if phase<.60:return Vector((plant,-2.10,0)),0
 u=(phase-.60)/.40
 return Vector((plant+1.4*smooth(u),-2.10+.88*math.sin(math.pi*u),0)),-.55*math.sin(math.pi*u)
# Pose schedule is baked to simple editable controls; limb surfaces remain live through drivers.
records=[]
for f in range(1,193):
 if f<=61:
  x=-4.8+(f-1)*.07;y=.05+.07*math.cos((f-1)*math.tau/10);lean=-.16
  ankles={side:foot_run(f,offset) for side,offset in [('L',10),('R',0)]}
 elif f<=78:
  u=(f-61)/17;x=-.60+.4*smooth(u);y=.12-.66*math.sin(u*math.pi/2);lean=-.16-.13*u
  ankles={side:(Vector((-.2+dx,-2.10,0)),0) for side,dx in [('L',-.3),('R',.3)]}
 elif f<=104:
  u=(f-78)/26;x=-.2+3.0*u;y=-.54+1.9*4*u*(1-u)+.54*u;lean=-.29+.25*u
  ankles={side:(Vector((x+dx,-2.10+(y+.54*(1-u))+.40*math.sin(math.pi*u),0)),0) for side,dx in [('L',-.3),('R',.3)]}
 elif f<=122:
  u=(f-104)/18;x=2.8;y=-.50*math.sin(math.pi*u);lean=-.04-.15*math.sin(math.pi*u)
  ankles={side:(Vector((x+dx,-2.10,0)),0) for side,dx in [('L',-.3),('R',.3)]}
 else:
  x=2.8;y=0;lean=.025*math.sin((f-122)*math.pi/70)
  ankles={side:(Vector((x+dx,-2.10,0)),0) for side,dx in [('L',-.3),('R',.3)]}
 root.location=(x,y,0);root.keyframe_insert(data_path='location',frame=f)
 torso.rotation_euler.z=lean;torso.keyframe_insert(data_path='rotation_euler',frame=f)
 for side,offset in [('L',10),('R',0)]:
  hip=Vector((-.12 if side=='L' else .17,0,0));ankle,roll=ankles[side];ankle-=Vector((x,y,0))
  shoulder=rotate((-.35 if side=='L' else .34,1.30),lean)
  if f<=61:angle=-math.pi/2+.85*math.sin((f-1+offset)*math.tau/20)
  elif f<=78:angle=-math.pi/2-.55*(f-61)/17
  elif f<=104:angle=-2.12+2.45*math.sin(math.pi*(f-78)/26)
  elif f<=122:angle=-1.57+.30*math.sin(math.pi*(f-104)/18)
  else:angle=-1.57+(1.1 if side=='R' else -.75)*smooth(min(1,(f-122)/28))
  elbow=shoulder+Vector((.69*math.cos(angle),.69*math.sin(angle),0))
  hand=elbow+Vector((.69*math.cos(angle+1.25),.69*math.sin(angle+1.25),0))
  values={'hip':hip,'knee':ik(hip,ankle),'ankle':ankle,'shoulder':shoulder,'elbow':elbow,'hand':hand}
  for part,p in values.items():
   o=controls[part+side];o.location=p;o.keyframe_insert(data_path='location',frame=f)
  controls['ankle'+side].rotation_euler.z=roll;controls['ankle'+side].keyframe_insert(data_path='rotation_euler',frame=f)
  controls['hand'+side].rotation_euler.z=angle+1.25+math.pi/2;controls['hand'+side].keyframe_insert(data_path='rotation_euler',frame=f)
 shadow.location.x=x;shadow.scale.x=max(.55,1-max(0,y)*.12);shadow.keyframe_insert(data_path='location',frame=f);shadow.keyframe_insert(data_path='scale',frame=f)
 records.append({'frame':f,'root':[x,y],'feet':{side:list(ankles[side][0]+Vector((x,y,0))) for side in ['L','R']}})
# Per-frame authored motion is linear between samples; no blanket automatic slow easing.
for ob in s.objects:
 ad=ob.animation_data
 if ad and ad.action:
  for layer in ad.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='LINEAR'
s['Scope']='Eight-second silent construction proof: run, crouch, jump, landing, recovery. Registered approved head; newly designed simpler body. Facial/dialogue acting and other views not tested.'
s['Events']=json.dumps({'run_end':61,'takeoff':78,'apex':91,'landing':104,'recovery':122})
s.frame_set(91);bpy.context.view_layer.update()
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_overlays=False
OUT.mkdir(parents=True);(OUT/'authored-motion.json').write_text(json.dumps(records)+'\n')
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'layered-action-v001.blend'))
result={'scene':NAME,'file':bpy.data.filepath,'controls':len(controls),'frames':192}
