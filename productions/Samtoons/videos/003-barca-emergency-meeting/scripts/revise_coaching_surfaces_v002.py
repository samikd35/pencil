"""S07: continuous clothing silhouettes evaluated from the existing motion.
Run prepare(sys.modules['s07']); bake(name) per actor in visible Blender.
Native per-frame drawings retain exact silhouette unions through crossing poses.
No runtime dependency is needed by the saved Blender movie.
"""
import bpy,sys,math,json
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(V.parents[3]/'.runtime/vector-art'))
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.geometry.polygon import orient
P='S07 continuous / '

def soft(points,r=.012):
 p=Polygon(points)
 if not p.is_valid:p=p.buffer(0)
 return p.buffer(r,quad_segs=5).buffer(-r,quad_segs=5)

def pieces(geo):
 return [geo] if geo.geom_type=='Polygon' else [p for p in geo.geoms if p.geom_type=='Polygon']

def native(n,geo,color,parent,depth,f=None,ink=True):
 cu=bpy.data.curves.new(P+n,'CURVE');cu.dimensions='2D';cu.fill_mode='BOTH';cu.resolution_u=1;cu.materials.append(M.g.mat(color))
 contours=[]
 for pg in pieces(geo):
  pg=orient(pg,sign=1)
  for ring in [pg.exterior,*pg.interiors]:
   pts=list(ring.coords)[:-1];contours.append(pts);sp=cu.splines.new('POLY');sp.points.add(len(pts)-1);sp.use_cyclic_u=True
   for dst,(x,z) in zip(sp.points,pts):dst.co=(x,z,0,1)
 ob=bpy.data.objects.new(cu.name,cu);M.C.objects.link(ob);ob.parent=parent;ob.rotation_euler.x=math.pi/2;ob.location.y=-depth
 obs=[ob]
 if ink:
  for i,pts in enumerate(contours):obs.append(M.line(n+f' outline {i}',pts,M.g.INK,.0023,parent,depth+.0002,True))
 if f is not None:
  for o in obs:
   for frame,hidden in [(1,True),(max(1,f-1),True),(f,False),(f+1,True)]:
    o.hide_render=hidden;o.hide_viewport=hidden;o.keyframe_insert(data_path='hide_render',frame=frame);o.keyframe_insert(data_path='hide_viewport',frame=frame)
 return obs

def world(points,p):return [tuple(p['hip']+Vector(M.turn(q,p['lean']))) for q in points]
BODY=[(-.21,-.01),(.21,-.01),(.214,.18),(.219,.35),(.198,.49),(.12,.55),(.082,.586),(-.074,.586),(-.125,.55),(-.20,.49),(-.222,.35),(-.21,.16)]


def prepare(m):
 global M
 M=m;assert not bpy.app.background
 M.O=V/'artifacts/staging-v001/coaching-performance-v002';M.O.mkdir(exist_ok=True);M.g.O=M.O
 M.S.name='S003_S07_Coaching_v002';M.S.use_fake_user=True;bpy.context.window.scene=M.S
 for name,a in M.A.items():
  for ob in list(a['torso'].children_recursive):bpy.data.objects.remove(ob,do_unlink=True)
  for value in a['limbs'].values():
   for ob in value if isinstance(value,tuple) else [value]:bpy.data.objects.remove(ob,do_unlink=True)
  # Keep the approved interior drawing; remove the old cut-out silhouette edges.
  data=json.loads((M.ART/(name.lower()+'.json')).read_text());c=data['design'];clip=soft(BODY).buffer(-.010)
  for i,row in enumerate(data['parts']['body']):
   paths=[]
   for path in row['paths']:
    pts=[((x-c['hip'][0])*M.SCALE,(c['hip'][1]-y)*M.SCALE) for x,y in path]
    pg=Polygon(pts)
    if not pg.is_valid:pg=pg.buffer(0)
    hit=pg.intersection(clip)
    if hit.is_empty:continue
    # Each original traced path keeps its winding, including hole paths.
    sign=1 if Polygon(pts).exterior.is_ccw else -1
    for pp in pieces(hit):
     pp=orient(pp,sign=sign)
     for ring in [pp.exterior,*pp.interiors]:paths.append(list(ring.coords)[:-1])
   if paths:
    cu=bpy.data.curves.new(P+name+f' garment detail {i}','CURVE');cu.dimensions='2D';cu.fill_mode='BOTH';cu.resolution_u=1;cu.materials.append(M.g.mat(row['color']))
    for path in paths:
     sp=cu.splines.new('POLY');sp.points.add(len(path)-1);sp.use_cyclic_u=True
     for pt,(x,z) in zip(sp.points,path):pt.co=(x,z,0,1)
    ob=bpy.data.objects.new(cu.name,cu);M.C.objects.link(ob);ob.parent=a['torso'];ob.rotation_euler.x=math.pi/2;ob.location.y=-.044-i*.000045
 return {'prepared':list(M.A),'revision':str(M.O)}


def bake(name,frames=None):
 a=M.A[name];c=a['c'];frames=frames or range(1,M.END+1)
 for f in frames:
  p=M.pose(name,f);root=a['root'];torso=soft(world(BODY,p));cloth=[torso]
  pelvis=soft(world([(-.205,.025),(.205,.025),(.205,-.10),(.075,-.175),(0,-.14),(-.075,-.175),(-.205,-.10)],p))
  trousers=[pelvis]
  for side in ['L','R']:
   arm=p['arms'][side];leg=p['legs'][side]
   # Smooth curves and one union boundary remove the independent shoulder/hip caps.
   armshape=soft(M.g.ribbon(arm,[.082,.065,.036] if name=='Flick' else [.057,.046,.028],segments=24),.016)
   trousers.append(soft(M.g.ribbon(leg,[.105,.081,.064],segments=24),.019))
   # A shoulder is a shoulder-to-collar transition, not the square cap of a
   # swept arm. Join its upper arc to the collar before forming the silhouette.
   sh,el,wr=map(Vector,arm);sgn=-1 if side=='L' else 1
   cap=soft(M.g.ribbon([tuple(sh),tuple(sh.lerp(el,.18)),tuple(sh.lerp(el,.38))],[.086,.083,.079],segments=12),.014)
   neck_patch=Polygon(world([(sgn*.07,.59),(sgn*.13,.57),(sgn*.17,.46),(sgn*.09,.43)],p))
   cloth.append(unary_union([cap,neck_patch]).convex_hull)
   if name=='Flick':cloth.append(armshape)
   else:
    native(name+side+f' skin {f}',armshape,c['skin'],root,.034,f)
    sleeve=[arm[0],tuple(Vector(arm[0]).lerp(Vector(arm[1]),.35)),tuple(Vector(arm[0]).lerp(Vector(arm[1]),.70))]
    cloth.append(soft(M.g.ribbon(sleeve,[.090,.084,.069],segments=24),.010))
  pants=unary_union(trousers)
  jacket=unary_union(cloth)
  assert pants.geom_type=='Polygon' and jacket.geom_type=='Polygon',(name,f,'disconnected garment')
  native(name+f' trousers {f}',pants,'#233553',root,.013,f)
  native(name+f' clothing {f}',jacket,c['cloth'],root,.040,f)
  # Forearms may cross the front of the torso. Draw the two sides, never a cap
  # across a shoulder. This preserves readable occlusion without detached tubes.
  if name=='Flick':
   for side in ['L','R']:
    sh,el,wr=map(Vector,p['arms'][side]);q=[tuple(el.lerp(sh,.10)),tuple(el.lerp(wr,.44)),tuple(wr)]
    pg=soft(M.g.ribbon(q,[.062,.051,.036],segments=24),.012)
    native(name+side+f' front sleeve {f}',pg,c['cloth'],root,.082,f,False)
    path=M.g.ribbon(q,[.062,.051,.036],segments=24)
    for tag,pts in [('outer',path[:49]),('inner',path[49:])]:
     ob=M.line(name+side+tag+str(f),pts,M.g.INK,.0018,root,.083)
     for frame,hide in [(1,True),(max(1,f-1),True),(f,False),(f+1,True)]:
      ob.hide_render=hide;ob.hide_viewport=hide;ob.keyframe_insert(data_path='hide_render',frame=frame);ob.keyframe_insert(data_path='hide_viewport',frame=frame)
  # A short fly seam is a clothing detail; no horizontal line separates hips/legs.
  seam=world([(0,-.012),(.012,-.082),(0,-.14)],p)
  ob=M.line(name+' fly'+str(f),seam,'#17273e',.0014,root,.015)
  for frame,hide in [(1,True),(max(1,f-1),True),(f,False),(f+1,True)]:
   ob.hide_render=hide;ob.hide_viewport=hide;ob.keyframe_insert(data_path='hide_render',frame=frame);ob.keyframe_insert(data_path='hide_viewport',frame=frame)
 return {'actor':name,'frames':len(frames),'construction':'one connected trouser silhouette and one connected torso/sleeve silhouette per frame'}


def save():
 # The neck/portrait owns the neckline overlap. Trace row count must not make
 # a shirt detail accidentally render in front of the lower head.
 for f in range(1,M.END+1):
  M.S.frame_set(f)
  for name,a in M.A.items():
   p=M.pose(name,f);a['head'].location=(p['neck'].x,-.080,p['neck'].y+.0048);M.key(a['head'],f)
 M.S['surface_revision']='Continuous native clothing unions and smooth limb contours, 24 drawings/second. No independent shoulder or hip caps. Existing authored motion, faces, dialogue and camera retained.'
 M.S.frame_set(140);bpy.ops.wm.save_as_mainfile(filepath=str(M.O/'coaching-performance.blend'))
 return {'saved':str(M.O/'coaching-performance.blend')}
