"""Preserve selected facial contours; repair shared neck and shorts construction.
Visible authoring only. v010 is retained as rejected evidence.
"""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
V=Path(__file__).resolve().parents[1];O=V/'artifacts/cast-coherence-v011';O.mkdir(exist_ok=True)
n=bpy.app.driver_namespace['samtoons_batch01'];b=n['b'];INK='#1e2228'

def vector_part(a,label,rows,parent,origin,scale,z):
 made=[]
 for i,row in enumerate(rows):
  data=bpy.data.curves.new(a['prefix']+'v011 '+label+' '+str(i),'CURVE');data.dimensions='2D';data.fill_mode='BOTH';data.resolution_u=1
  for path in row['paths']:
   sp=data.splines.new('POLY');sp.points.add(len(path)-1);sp.use_cyclic_u=True
   for p,(x,y) in zip(sp.points,path):p.co=((x-origin[0])*scale,(origin[1]-y)*scale,0,1)
  data.materials.append(b['mat'](row['color']));o=bpy.data.objects.new(data.name,data);a['col'].objects.link(o);o.parent=parent;o.location.z=z+i*.001;made.append(o)
 return made

def source_face(name):
 a=n['ACTORS'][name];n['use'](a['scene'],a['col']);C=a['C'];h=C['head'];p=a['prefix'];data=json.loads((V/'assets/native-contours-v011'/(a['kind']+'.json')).read_text());cfg=data['design'];k=cfg['scale'];origin=cfg['origin']
 # Facial motion remains explicit semantic parts, never a whole bitmap posed as talking.
 for ob in list(h.children_recursive):
  if ob.type in ['MESH','CURVE','FONT']:bpy.data.objects.remove(ob,do_unlink=True)
 vector_part(a,'source face',data['parts']['head'],h,origin,k,4)
 def xy(pts):return [((x-origin[0])*k,(origin[1]-y)*k) for x,y in pts]
 for i,side in enumerate(['L','R']):
  eye=cfg['eyes'][i];e=C[side+' eye'];e.location=(*xy([eye['center']])[0],12)
  n['poly'](p+'v011 '+side+' lid backing',xy(eye['outline']),cfg['skin'],3.9,h,False)
  vector_part(a,side+' source eye',data['parts']['eye'+str(i)],e,eye['center'],k,0)
 # Backing occupies only the mouth aperture; no floating oval muzzle or extra chin.
 n['poly'](p+'v011 mouth backing',xy(cfg['mouth_outline']),cfg['skin'],3.9,h,False)
 C['mouth'].location=(*xy([cfg['mouth_center']])[0],15);C['mouth'].scale=(1,1,1)
 groups=a['n']['FAC']['mouth shapes'];width=13 if a['kind']=='gyokeres' else 17
 for label,g in groups.items():
  if label=='rest':
   # Arteta's selected resting smile is a native contour, not a painted replacement head.
   if a['kind']=='arteta':vector_part(a,'rest mouth',data['parts']['source_mouth'],g,cfg['mouth_center'],k,0)
   else:
    n['line'](p+'v011 rest lip',[(-12,-1),(-4,1),(4,1),(12,-1)],'#4b3026',0,.7,g,True)
    n['line'](p+'v011 rest lower lip',[(-8,-4),(0,-5),(8,-4)],'#bc8056',.1,.5,g,True)
  elif label=='MBP':n['line'](p+'v011 MBP lip',[(-width,-1),(-3,-2),(4,-1),(width,0)],'#4b3026',0,.8,g,True)
  else:
   hh={'A':10,'E':6,'O':9,'U':6,'FV':3,'L':7}[label];ww=width*({'O':.59,'U':.45}.get(label,1))
   pts=[(-ww,0),(-ww*.65,2),(0,3),(ww*.7,2),(ww,0),(ww*.75,-hh*.75),(0,-hh),(-ww*.75,-hh*.75)]
   n['poly'](p+'v011 '+label+' aperture',pts,'#412722',0,g,True,.75,True)
   if label not in ['O','U']:
    n['poly'](p+'v011 '+label+' teeth',[(-ww*.8,.9),(0,2),(ww*.8,.9),(ww*.68,-2),(0,-3),(-ww*.7,-2)],'#fff3db',.2,g,False,soft=True)
   if label in ['A','L']:
    n['poly'](p+'v011 '+label+' tongue',[(-ww*.48,-hh*.8),(0,-hh*.65),(ww*.45,-hh*.8),(0,-hh*.93)],'#bf7068',.3,g,False,soft=True)
 # Rebind exact existing expression schedule to new surfaces (Blender action slots included).
 for label,g in groups.items():
  a['scene'].frame_set(1)
  for child in g.children_recursive:
   if child.type not in ['MESH','CURVE']:continue
   child.hide_render=child.hide_viewport=label!='rest';child.keyframe_insert(data_path='hide_render',frame=1);child.keyframe_insert(data_path='hide_viewport',frame=1)
 a['source_face']=cfg
 return {'actor':name,'source_contours':len(data['parts']['head'])}

def animate_faces():
 phrases={'opening Arteta':[(67,127,'E U MBP FV E E A MBP L A MBP'),(213,239,'A O E E A MBP'),(346,386,'E MBP E A E A MBP O')],'unveiling Gyokeres':[(301,339,'E A MBP A E')],'unveiling Arteta':[(351,376,'U E MBP A O E')]}
 for name,rows in phrases.items():n['mouths'](n['ACTORS'][name],rows)
 return {'scheduled':list(phrases)}

def neck(name):
 a=n['ACTORS'][name];s=a['scene'];n['use'](s,a['col']);C=a['C'];p=a['prefix'];ch=C['chest'];head=C['head'];cfg=a['source_face'];skin=cfg['skin']
 for ob in a['col'].objects:
  if any(ob.name==p+x or ob.name==p+x+' outline' for x in ['neck','neck shade','collar','jumper neckline','neckline highlight','finish red collar edge','finish white collar']):ob.hide_render=ob.hide_viewport=True
 # Cut the actual garment neckline down to the crew neck; the white torso no longer fills it.
 body=bpy.data.objects[p+'connected upper body']
 for key in body.data.shape_keys.key_blocks:key.data[14].co.y=176
 # Hide the old outline's closing top segment; a correctly fitted collar is authored below.
 edge=bpy.data.objects[p+'garment exterior'];edge.data.polygons.foreach_set('use_smooth',[False]*len(edge.data.polygons))
 # The original exterior's last 3 neck points are stored in a quad ribbon.
 for key in edge.data.shape_keys.key_blocks:
  for idx in [284,285]:key.data[idx].co.y=176
 skinpts=[];frames=[]
 for f in range(1,s.frame_end+1):
  s.frame_set(f);bpy.context.view_layer.update();inv=ch.matrix_world.inverted();left=inv@(head.matrix_world@Vector((-33,43,0) if a['kind']=='gyokeres' else (-29,36,0)));right=inv@(head.matrix_world@Vector((55,14,0) if a['kind']=='gyokeres' else (48,11,0)))
  if left.x>right.x:left,right=right,left
  baseL=Vector((-29,185,0));baseR=Vector((29,185,0));pts=[]
  for j in range(5):
   t=j/4;pts.extend([baseL.lerp(left,t),baseR.lerp(right,t)])
  if f==1:
   me=bpy.data.meshes.new(p+'v011 connected neck');me.from_pydata([(v.x,v.y,8.5) for v in pts],[],[(2*j,2*j+1,2*j+3,2*j+2) for j in range(4)]);me.materials.append(b['mat'](skin));ob=bpy.data.objects.new(p+'v011 connected neck',me);a['col'].objects.link(ob);ob.parent=ch
  key=ob.shape_key_add(name=f'Frame {f:03}');ob.data.shape_keys.use_relative=False
  for d,v in zip(key.data,pts):d.co=(v.x,v.y,8.5)
  key.interpolation='KEY_LINEAR';ks=ob.data.shape_keys;ks.eval_time=(f-1)*10;ks.keyframe_insert(data_path='eval_time',frame=f)
 # One continuous crew-neck line sits in front of the skin, without a filled neck cap.
 collar=[(-30,199),(-27,187),(-17,179),(0,176),(17,179),(27,190),(30,199)]
 n['line'](p+'v011 collar edge',collar,'#1b232c',11,2.4,ch,True)
 n['line'](p+'v011 collar fabric',collar,'#fff8e8' if a['kind']=='gyokeres' else '#283343',11.1,1.25,ch,True)
 s.frame_set(315 if s.frame_end==432 else 226)
 return {'connected_neck':name,'frames':s.frame_end}

def source_shorts():
 import bmesh
 a=n['ACTORS']['unveiling Gyokeres'];s=a['scene'];n['use'](s,a['col']);p=a['prefix'];C=a['C'];hip=C['pelvis'];data=json.loads((V/'assets/native-contours-v011/gyokeres.json').read_text())
 # One original garment and its original folds/logos; no independent thigh caps.
 for ob in a['col'].objects:
  if any(t in ob.name for t in ['hip cloth','shorts number','shorts crest','shorts stripe','finish shorts','shorts fold','shorts hem','shorts side stripe']):ob.hide_render=ob.hide_viewport=True
 made=vector_part(a,'single shorts',data['parts']['shorts'],hip,(0,0),1,7)
 bpy.ops.object.select_all(action='DESELECT')
 for ob in made:ob.select_set(True)
 bpy.context.view_layer.objects.active=made[0];bpy.ops.object.convert(target='MESH');bpy.ops.object.join();ob=bpy.context.object;ob.name=p+'v011 single source shorts';ob.data.name=ob.name
 # Fixed explicit triangles stay stable through the fitted garment deformation.
 bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
 source=[(296,493),(395,506),(505,488),(548,637),(418,660),(392,555),(382,652),(267,647)];tris=[(0,1,5),(1,2,5),(0,5,7),(5,6,7),(2,3,5),(3,4,5)]
 def bary(pt,t):
  ax,ay=source[t[0]];bx,by=source[t[1]];cx,cy=source[t[2]];x,y=pt;det=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
  u=((by-cy)*(x-cx)+(cx-bx)*(y-cy))/det;v=((cy-ay)*(x-cx)+(ax-cx)*(y-cy))/det;return u,v,1-u-v
 fitted=[]
 for v in ob.data.vertices:
  choices=[(sum(max(0,-w) for w in bary((v.co.x,-v.co.y),t)),t,bary((v.co.x,-v.co.y),t)) for t in tris];error,t,weights=min(choices,key=lambda x:x[0]);assert error<.7,error;fitted.append((t,weights,v.co.z))
 for f in list(range(1,117))+[s.frame_end]:
  s.frame_set(f);bpy.context.view_layer.update();inv=hip.matrix_world.inverted()
  def hem(side,x):return inv@(C[side+' thigh'].matrix_world@Vector((x,-84,0)))
  target=[Vector((-64,12,0)),Vector((0,7,0)),Vector((64,12,0)),hem('R',36),hem('R',-31),Vector((0,-35,0)),hem('L',31),hem('L',-36)]
  key=ob.shape_key_add(name=f'Garment {f:03}');ob.data.shape_keys.use_relative=False
  for v,(t,weights,z) in zip(key.data,fitted):
   pt=sum((target[i]*w for i,w in zip(t,weights)),Vector());v.co=(pt.x,pt.y,z)
  key.interpolation='KEY_LINEAR';ks=ob.data.shape_keys;ks.eval_time=(len(ks.key_blocks)-1)*10;ks.keyframe_insert(data_path='eval_time',frame=f)
 for side in ['L','R']:
  # Underlying thighs are skin. Their old white section must not form another shorts layer.
  for obj in a['col'].objects:
   if side+' leg cloth' in obj.name:obj.data.materials[0]=b['mat']('#ffc38b')
   if side+' leg shade' in obj.name:obj.data.materials[0]=b['mat']('#d29970')
 ob['construction']='One selected shorts illustration, native triangulated color geometry; one shared waist/crotch/hem cage follows both thigh controls.'
 s.frame_set(70);return {'single_shorts':ob.name,'vertices':len(ob.data.vertices),'deformation_keys':len(ob.data.shape_keys.key_blocks)}
