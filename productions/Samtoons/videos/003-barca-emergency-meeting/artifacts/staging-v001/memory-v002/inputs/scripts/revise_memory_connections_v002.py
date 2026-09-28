"""Repair both S10 players on the selected native file; retain all shot motion/audio.
Visible Blender: setup(); prepare(name); bake(name); finish().
No old action is regenerated. New silhouettes own all shoulder/wrist boundaries.
"""
import bpy,sys,json,math,importlib.util,shutil
from pathlib import Path
from types import SimpleNamespace
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/staging-v001/memory-v002';P='S10v2 / '
sp=importlib.util.spec_from_file_location('memory_connections_base',V/'scripts/build_memory_v001.py');M=importlib.util.module_from_spec(sp);sp.loader.exec_module(M);g=M.g
sp=importlib.util.spec_from_file_location('memory_connections_union',V/'scripts/revise_coaching_surfaces_v002.py');u=importlib.util.module_from_spec(sp);sp.loader.exec_module(u)
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely import affinity
A={};CHECK=[]
NECK_OPENING=[(-.078,.65),(.075,.65),(.075,.597),(.06,.57),(0,.537),(-.065,.572),(-.085,.599)]
BODY=[(-.20,-.012),(.20,-.012),(.207,.34),(.195,.50),(.13,.578),(.08,.609),(-.10,.609),(-.15,.577),(-.195,.50),(-.207,.34)]

def load_actor(name):
 prefix='S10 / '+name
 a={'root':bpy.data.objects[prefix+' world'],'torso':bpy.data.objects[prefix+' torso'],'head':bpy.data.objects[prefix+' head'],'shorts':bpy.data.objects[prefix+' drawn shorts'],'shirt':bpy.data.objects[prefix+' drawn shirt']}
 a['data']=json.loads((V/'assets/memory-v001'/(name.lower()+'.json')).read_text());a['c']=a['data']['design'];a['hands']=json.loads((V/'assets/memory-v002'/(name.lower()+'-hands.json')).read_text())['rows']
 return a

def setup():
 global S,C
 assert not bpy.app.background
 assert Path(bpy.data.filepath).name=='memory.blend' and bpy.context.scene.name=='S003_S10_Memory_v001'
 assert not (O/'memory.blend').exists(),'Use another revision for delivered output'
 O.mkdir(exist_ok=True)
 for item in ['render-selection.json','construction-check.json']:
  shutil.copy2(V/'artifacts/staging-v001/memory-v001'/item,O/item)
 shutil.copytree(V/'artifacts/staging-v001/memory-v001/audio',O/'audio',dirs_exist_ok=True)
 shutil.copy2(V/'production.json',O/'production-before.json')
 S=bpy.context.scene;S.name='S003_S10_Memory_v002';C=bpy.data.collections.new(P+'player construction');S.collection.children.link(C);g.C=C;g.S=S;g.P=P;g.M={}
 u.P=P;u.M=SimpleNamespace(g=g,C=C,line=g.line,turn=g.turn)
 for name in ['Lewandowski','Raphinha']:A[name]=load_actor(name)
 return {'scene':S.name,'scope':'player artwork connections only; retained existing S10 animation'}

def valid(pg):return pg if pg.is_valid else pg.buffer(0)
def row_geo(row):
 # Traced compound paths use winding to represent holes.
 pieces=[valid(Polygon(path)) for path in row['paths'] if len(path)>2]
 return unary_union(pieces)
def transform(pg,origin,scale):return affinity.translate(affinity.scale(pg,xfact=scale,yfact=-scale,origin=(0,0)),xoff=-origin[0]*scale,yoff=origin[1]*scale)
def hidden(o):
 # Old visibility actions must not turn retired edges back on at the period cut.
 o.animation_data_clear();o.hide_render=o.hide_viewport=True

def prepare(name):
 a=A[name];prefix='S10 / '+name
 hidden(a['shirt'])
 for ob in list(S.objects):
  if ob.name.startswith(prefix+' ') and any(x in ob.name[len(prefix)+1:] for x in ['armL','armR','sleeveL','sleeveR','relaxed hand','fingers']):hidden(ob)
 a['hand_geo']=[];a['hand_details']=[]
 for rows in a['hands']:
  polygons=[row_geo(row) for row in rows];a['hand_geo'].append(unary_union(polygons));a['hand_details'].append(polygons)
 # Copy source interior into a clean body without copying cut edges.
 rows=a['data']['parts']['shirt'];polys=[transform(row_geo(row),(a['c']['cx'],577),g.SCALE) for row in rows];source_shell=unary_union(polys)
 clip=source_shell.buffer(-.007).intersection(u.soft(BODY).buffer(-.006))
 for i,(row,pg) in enumerate(zip(rows,polys)):
  hit=pg.intersection(clip)
  if not hit.is_empty:u.native(name+' shirt detail '+str(i),hit,row['color'],a['torso'],.043+i*.00002,ink=False)
 # Clear the old shape animation too: shape_key_clear alone leaves old timeline
 # keys, which would select the wrong new drawing during holds.
 # Rebind the actual selected shorts mesh to the thigh frames. Waist stays with
 # torso; cuff vertices use full thigh rotation, not angle multiplied by a weight.
 a['shorts'].data.shape_keys.animation_data_clear();a['shorts'].shape_key_clear();a['shorts'].shape_key_add(name='Source waist');a['shorts'].data.shape_keys.use_relative=False
 a['short_base']=[tuple(v.co) for v in a['shorts'].data.vertices]
 return {'name':name,'short_vertices':len(a['short_base']),'source_hands':len(a['hands'])}

def worldpoly(pg,p):return affinity.translate(affinity.rotate(pg,p['lean'],origin=(0,0),use_radians=True),p['hip'].x,p['hip'].y)
def show_interval(obs,start,end):
 for ob in obs:
  for f,on in [(1,False),(start,True),(end+1,False)]:
   ob.hide_render=ob.hide_viewport=not on;ob.keyframe_insert(data_path='hide_render',frame=f);ob.keyframe_insert(data_path='hide_viewport',frame=f)

def shorts_frame(name,p,f):
 a=A[name];ob=a['shorts'];key=ob.shape_key_add(name=f'thigh fitted {f}');key.interpolation='KEY_LINEAR';coords=[]
 # Native contour mesh is in XY; its object rotates it into the drawing plane.
 co=math.cos(p['lean']);si=math.sin(p['lean']);frames={}
 for side,sgn in [('L',-1),('R',1)]:
  hp,kn,_=map(Vector,p['legs'][side]);down=(kn-hp).normalized();normal=Vector((-down.y,down.x));frames[side]=(hp,down,normal,sgn)
 for x,z,depth in a['short_base']:
  side='L' if x<0 else 'R';hp,d,n,sgn=frames[side];along=-z-.05;across=x-sgn*.095
  wx=hp.x+n.x*across+d.x*along-p['hip'].x;wy=hp.y+n.y*across+d.y*along-p['hip'].y
  tx=co*wx+si*wy;tz=-si*wx+co*wy;w=max(0,min(1,(-z-.035)/.11));w=w*w*(3-2*w)
  coords.extend((x+(tx-x)*w,z+(tz-z)*w,depth))
 key.data.foreach_set('co',coords);ob.data.shape_keys.eval_time=key.frame;ob.data.shape_keys.keyframe_insert(data_path='eval_time',frame=f)

def bake(name):
 a=A[name];start,end=(1,138) if name=='Lewandowski' else (139,264)
 # Each rendered frame gets its correct contour; holds reuse identical drawings.
 last_signature=None;groups=[];samples=[]
 for f in range(start,end+1):
  p=M.pose(name,f);signature=tuple(round(v,6) for pts in [p['hip'],[p['lean']],*p['arms']['L'],*p['arms']['R'],*p['legs']['L'],*p['legs']['R']] for v in pts)
  if signature!=last_signature:samples.append(f);last_signature=signature
 for idx,f in enumerate(samples):
  last=samples[idx+1]-1 if idx+1<len(samples) else end;p=M.pose(name,f);body=worldpoly(u.soft(BODY),p);cloth=[body];made=[]
  for side,i,sgn in [('L',0,-1),('R',1,1)]:
   sh,el,wr=map(Vector,p['arms'][side]);fore=(wr-el).normalized();angle=math.atan2(fore.y,fore.x)+math.pi/2
   hg=affinity.translate(affinity.rotate(a['hand_geo'][i],angle,origin=(0,0),use_radians=True),wr.x,wr.y)
   # Wrist width comes from the source hand at the registration, not a separate
   # generic stroke. Both enter one silhouette, so no wrist crossbar is drawn.
   arm=u.soft(g.ribbon([sh,el,wr],[.054,.047,.030],segments=24),.008)
   skin=unary_union([arm,hg]);assert skin.geom_type=='Polygon',(name,f,side,'wrist disconnected')
   made+=u.native(name+' skin '+side+str(f),skin,a['c']['skin'],a['root'],.025,ink=True)
   interior=a['hand_geo'][i].buffer(-.003)
   for j,(row,geo) in enumerate(zip(a['hands'][i],a['hand_details'][i])):
    hit=geo.intersection(interior)
    if hit.is_empty:continue
    hit=affinity.translate(affinity.rotate(hit,angle,origin=(0,0),use_radians=True),wr.x,wr.y)
    made+=u.native(name+' fingers '+side+str(f)+' '+str(j),hit,row['color'],a['root'],.027+j*.00002,ink=False)
   sleeve=u.soft(g.ribbon([sh,sh.lerp(el,.35),sh.lerp(el,.70)],[.085,.081,.068],segments=24),.012);cloth.append(sleeve)
   shoulder=unary_union([u.soft(g.ribbon([sh,sh.lerp(el,.16),sh.lerp(el,.36)],[.085,.083,.079],segments=12),.01),worldpoly(Polygon([(sgn*.078,.598),(sgn*.135,.57),(sgn*.19,.49),(sgn*.08,.43)]),p)]).convex_hull;cloth.append(shoulder)
   CHECK.append({'actor':name,'frame':f,'region':side+' wrist','components':1})
  shirt=unary_union(cloth).difference(worldpoly(Polygon(NECK_OPENING),p));assert shirt.geom_type=='Polygon',(name,f,'shirt disconnected')
  made+=u.native(name+' continuous shirt '+str(f),shirt,'#d8222a' if name=='Lewandowski' else '#233e78',a['root'],.039)
  show_interval(made,f,last);shorts_frame(name,p,f)
  CHECK.append({'actor':name,'frame':f,'region':'shirt','components':1})
 # Source interiors follow the unchanged torso, and respect the club cut.
 for ob in C.objects:
  if ob.name.startswith(P+name+' shirt detail'):show_interval([ob],start,end)
 return {'actor':name,'authored_surface_frames':len(samples),'range':[start,end]}

def open_neck_outline(ob,p):
 # The collar supplies the neckline; a closed garment outline would draw an
 # artificial horizontal seam across the exposed neck.
 sp=ob.data.splines[0];pts=[tuple(q.co) for q in sp.points];keep=[]
 co=math.cos(p['lean']);si=math.sin(p['lean'])
 for x,y,z,w in pts:
  dx=x-p['hip'].x;dz=z-p['hip'].y;lx=co*dx+si*dz;lz=-si*dx+co*dz
  keep.append(not (lz>.596 and abs(lx)<.12))
 if all(keep):return
 cut=keep.index(False);ordered=[(pts[(cut+1+i)%len(pts)],keep[(cut+1+i)%len(pts)]) for i in range(len(pts))]
 run=[q for q,ok in ordered if ok];ob.data.splines.clear();sp=ob.data.splines.new('POLY');sp.points.add(len(run)-1);sp.use_cyclic_u=False
 for dst,q in zip(sp.points,run):dst.co=q

def finish():
 for ob in C.objects:
  if ' continuous shirt ' in ob.name and ' outline ' in ob.name:
   name=ob.name[len(P):].split(' continuous shirt ')[0];f=int(ob.name.split(' continuous shirt ')[1].split()[0]);open_neck_outline(ob,M.pose(name,f))
 # Blender can reattach the object's shared Action slot during key insertion.
 # Replace that slot's eval_time curve, retaining the object's visibility curves.
 for a in A.values():
  keys=a['shorts'].data.shape_keys;action=keys.animation_data.action
  for layer in action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in list(bag.fcurves):
      if fc.data_path=='eval_time':bag.fcurves.remove(fc)
  for k in keys.key_blocks:
   if k.name.startswith('thigh fitted '):
    keys.eval_time=k.frame;keys.keyframe_insert(data_path='eval_time',frame=int(k.name.rsplit(' ',1)[1]))
 g.linear_keys()
 for a in A.values():
  for layer in a['shorts'].data.shape_keys.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT'
 # Draw visibility is discrete. Dynamic shape interpolation remains linear.
 for ob in C.objects:
  if ob.animation_data and ob.animation_data.action:
   for layer in ob.animation_data.action.layers:
    for strip in layer.strips:
     for bag in strip.channelbags:
      for fc in bag.fcurves:
       if fc.data_path.startswith('hide_'):
        for k in fc.keyframe_points:k.interpolation='CONSTANT'
 for name,a in A.items():
  keys=a['shorts'].data.shape_keys
  authored=[(int(k.name.rsplit(' ',1)[1]),k.frame) for k in keys.key_blocks if k.name.startswith('thigh fitted ')]
  for f in range(1,265):
   expected=next((value for frame,value in reversed(authored) if frame<=f),authored[0][1])
   S.frame_set(f);assert abs(keys.eval_time-expected)<.002,(name,f,keys.eval_time,expected)
   assert a['shorts'].hide_render==((f>=139) if name=='Lewandowski' else (f<139)),(name,f,'period visibility')
 S['player_connections_revision']='v002: continuous shirt/sleeve and arm/hand silhouettes; selected reference hands; shorts cuff coordinates bound to actual thighs.'
 S.frame_set(171);bpy.ops.wm.save_as_mainfile(filepath=str(O/'memory.blend'))
 (O/'surface-check.json').write_text(json.dumps({'samples':CHECK,'scope':'Connected surface geometry only. Visual close-up review also required; not general extreme-pose certification.'},indent=2)+'\n')
 return {'native':str(O/'memory.blend'),'connected_surface_checks':len(CHECK)}
