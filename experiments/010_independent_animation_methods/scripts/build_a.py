"""Independent A: new planar armature, authored vector drawings and substitutions.
Only production.json, the selected image (reference-only), and voice.wav are inputs.
Run setup(); environment(); character(); animate(); finish() in visible Blender.
"""
import bpy, math, json
from pathlib import Path
from mathutils import Vector, Matrix
ROOT=Path('/Users/samikd/MyProjects/Pencil/experiments/010_independent_animation_methods')
C=json.loads((ROOT/'production.json').read_text()); OUT=ROOT/'artifacts/a-2d-v002'
INK='#252631';SKIN='#F4B976';SHADE='#D88C50';RED='#C82D29';CREAM='#FFF3D8';WHITE='#FFFBF0'
M={}; actors=[]; handsets=[]; heads=[]; eyecontrols=[]; mouthcontrols=[]
def mat(c):
 if c in M:return M[c]
 m=bpy.data.materials.new('A ink '+c);vals=[int(c[i:i+2],16)/255 for i in (1,3,5)];m.diffuse_color=tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in vals)+(1,);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=m.diffuse_color;o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs[0]);M[c]=m;return m

def line(name,pts,color=INK,w=.009,depth=-.04,closed=False,smooth=True,parent=None):
 cu=bpy.data.curves.new('A '+name,'CURVE');cu.dimensions='3D';cu.bevel_depth=w;cu.bevel_resolution=2;cu.resolution_u=8
 sp=cu.splines.new('BEZIER' if smooth else 'POLY')
 if smooth:
  sp.bezier_points.add(len(pts)-1)
  for p,q in zip(sp.bezier_points,pts):p.co=(q[0],depth,q[1]);p.handle_left_type=p.handle_right_type='AUTO'
 else:
  sp.points.add(len(pts)-1)
  for p,q in zip(sp.points,pts):p.co=(q[0],depth,q[1],1)
 sp.use_cyclic_u=closed
 ob=bpy.data.objects.new('A '+name,cu);S.collection.objects.link(ob);cu.materials.append(mat(color));ob.parent=parent;return ob

def shape(name,pts,color,depth=0,smooth=True,parent=None,edge=True):
 cu=bpy.data.curves.new('A '+name,'CURVE');cu.dimensions='2D';cu.fill_mode='BOTH';cu.resolution_u=8;sp=cu.splines.new('BEZIER' if smooth else 'POLY')
 if smooth:
  sp.bezier_points.add(len(pts)-1)
  for p,q in zip(sp.bezier_points,pts):p.co=(q[0],q[1],0);p.handle_left_type=p.handle_right_type='AUTO'
 else:
  sp.points.add(len(pts)-1)
  for p,q in zip(sp.points,pts):p.co=(q[0],q[1],0,1)
 sp.use_cyclic_u=True;ob=bpy.data.objects.new('A '+name,cu);S.collection.objects.link(ob);ob.rotation_euler[0]=math.pi/2;ob.location.y=depth;cu.materials.append(mat(color));ob.parent=parent
 if edge:line(name+' outline',pts,depth=depth-.008,closed=True,smooth=smooth,parent=parent)
 return ob

def oval(name,x,z,rx,rz,color,depth=-.05,parent=None,edge=True):return shape(name,[(x+rx*math.cos(i*math.tau/24),z+rz*math.sin(i*math.tau/24)) for i in range(24)],color,depth,parent=parent,edge=edge)
def empty(name):
 o=bpy.data.objects.new('A '+name,None);S.collection.objects.link(o);return o

def text(name,body,x,z,size,color,depth=-.1,parent=None):
 cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.align_x='CENTER';cu.size=size;cu.extrude=0;cu.materials.append(mat(color));o=bpy.data.objects.new('A '+name,cu);S.collection.objects.link(o);o.location=(x,depth,z);o.rotation_euler[0]=math.pi/2;o.parent=parent;return o

def setup():
 global S
 S=bpy.data.scenes.new('METHOD A - new 2D construction');bpy.context.window.scene=S;S.render.engine='CYCLES';S.cycles.samples=8;S.cycles.use_denoising=False
 S.render.resolution_x=C['width'];S.render.resolution_y=C['height'];S.render.resolution_percentage=100;S.render.fps=C['fps'];S.frame_start=1;S.frame_end=C['frames'];S.view_settings.view_transform='Standard';S.world=bpy.data.worlds.new('A world');S.world.color=(.5,.5,.5)
 cd=bpy.data.cameras.new('A camera');cam=bpy.data.objects.new('A camera',cd);S.collection.objects.link(cam);cam.location=C['camera']['location'];cam.rotation_euler=(Vector(C['camera']['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cd.type='ORTHO';cd.ortho_scale=C['camera']['ortho_scale'];S.camera=cam
 S['method']='New native planar vector drawings + armature deformation + authored hand/head substitutions. Not raster cutouts; not Grease Pencil.'
 S['independence']=C['independence'];S['reference']='inputs/reference.png, left subject; not rendered as a plane'
 for area in bpy.context.screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL'

def environment():
 shape('wall',[(-5,.3),(5,.3),(5,6),(-5,6)],'#D9C4A0',2,False,edge=False)
 shape('window',[(-3.6,2.3),(-2.2,2.3),(-2.2,4.9),(-3.6,4.9)],'#263F4D',1.8,False)
 shape('window light',[(-3.45,2.5),(-2.35,2.5),(-2.35,4.75),(-3.45,4.75)],'#8BACB5',1.75,False,edge=False)
 line('window divider',[(-2.9,2.5),(-2.9,4.75)],'#FFF3D8',.035,1.7,False,False)
 for x in [-1.7,0,1.7,3.4]:line('wall panel',[(x,1.2),(x,5.6)],'#B99E77',.012,1.7,False,False)
 shape('cabinet',[(2.05,1.3),(3.35,1.3),(3.35,3),(2.05,3)],'#816548',1.5,False)
 for i in range(6):shape('book',[(2.15+i*.15,1.8),(2.25+i*.15,1.8),(2.25+i*.15,2.55),(2.15+i*.15,2.55)],['#A85242','#EFE1BE','#617A77'][i%3],1.4,False)
 oval('pot',2.72,3.12,.23,.2,'#4B6E6C',1.4)
 for x,z in [(2.48,3.6),(2.85,3.66),(2.73,3.76)]:shape('plant',[(2.72,3.22),(x-.07,z),(x+.05,z+.04)],'#427B65',1.4,False)
 shape('table top',[(-4,.88),(4,.88),(4,1.5),(-4,1.5)],'#BA8C5B',-.7,False)
 line('table rim',[(-4,1.51),(4,1.51)],'#F2CB95',.022,-.72,False,False)

# New planar sleeve mesh, shared skinning for fill/shadow/contour.
def arm(name,x,z,side):
 length=.78;ad=bpy.data.armatures.new('A '+name);rig=bpy.data.objects.new('A '+name,ad);S.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
 prev=None
 for bn,a,b in [('upper',(x,0,z),(x,0,z-length)),('fore',(x,0,z-length),(x,0,z-2*length)),('hand',(x,0,z-2*length),(x,0,z-2*length-.3))]:
  eb=ad.edit_bones.new(bn);eb.head=a;eb.tail=b
  if prev:eb.parent=prev;eb.use_connect=True
  prev=eb
 bpy.ops.object.mode_set(mode='OBJECT');rig.select_set(False)
 verts=[];faces=[];N=33
 for i in range(N):
  t=i/(N-1);width=.245*(1-t)+.137*t
  verts.extend([(x-width,0,z-2*length*t),(x+width,0,z-2*length*t)])
 for i in range(N-1):faces.append((2*i,2*i+1,2*i+3,2*i+2))
 mesh=bpy.data.meshes.new(name+' surface');mesh.from_pydata(verts,[],faces);mesh.update();ob=bpy.data.objects.new('A '+name+' continuous sleeve',mesh);S.collection.objects.link(ob);ob.data.materials.append(mat(RED))
 def bind(o):
  groups={n:o.vertex_groups.new(name=n) for n in ['upper','fore']}
  for v in o.data.vertices:
   t=(z-v.co.z)/length;w=max(0,min(1,(t-.78)/.44));w=w*w*(3-2*w)
   if w<1:groups['upper'].add([v.index],1-w,'REPLACE')
   if w>0:groups['fore'].add([v.index],w,'REPLACE')
  mod=o.modifiers.new('Armature - continuous sleeve','ARMATURE');mod.object=rig;mod.use_deform_preserve_volume=True
 bind(ob)
 for j in [0,1]:
  path=[(verts[i*2+j][0],verts[i*2+j][2]) for i in range(N)]
  o=line(name+' outer ink '+str(j),path,w=.009,depth=-.02,smooth=False);bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o=bpy.context.object;o.select_set(False);bind(o)
 # Long white tracks follow the actual surface rather than an independent pose.
 for j in range(3):
  o=line(name+' kit stripe',[(x-.14+j*.052,z-.09),(x-.14+j*.052,z-.42),(x-.14+j*.052,z-.68)],WHITE,.014,-.035,False,False);bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o=bpy.context.object;o.select_set(False);bind(o)
 return {'rig':rig,'x':x,'z':z,'len':length,'side':side}

def hand_draw(root,mode):
 # Local +Z runs from wrist towards fingertips; each state is a fresh silhouette.
 group=[];before=set(S.objects)
 if mode=='open':
  pts=[(-.115,-.07),(-.18,.17),(-.20,.34),(-.18,.43),(-.14,.42),(-.09,.25),(-.12,.55),(-.08,.60),(-.045,.56),(0,.31),(-.015,.67),(.03,.70),(.065,.65),(.085,.34),(.11,.59),(.155,.61),(.18,.55),(.18,.29),(.22,.41),(.27,.40),(.285,.34),(.225,.13),(.12,-.07)]
  shape('open hand',pts,SKIN,-.37,True,root)
  line('open palm crease',[(-.09,.14),(.015,.19),(.12,.15)],SHADE,.009,-.39,parent=root)
 elif mode=='closing':
  pts=[(-.12,-.08),(-.19,.11),(-.17,.29),(-.19,.43),(-.15,.49),(-.1,.45),(-.05,.27),(-.04,.48),(.02,.52),(.075,.43),(.09,.28),(.13,.41),(.19,.40),(.21,.28),(.25,.29),(.27,.20),(.20,.08),(.12,-.08)]
  shape('closing hand',pts,SKIN,-.38,True,root)
  for z in [.15,.26,.36]:line('closing finger crease',[(-.09,z),(.04,z+.03),(.12,z-.02)],INK,.009,-.4,parent=root)
 else:
  # Fingers lie over the left edge of the frame; the thumb wraps below.
  pts=[(-.13,-.08),(-.2,.04),(-.22,.19),(-.17,.35),(-.09,.43),(.02,.43),(.115,.40),(.14,.36),(.11,.32),(.16,.28),(.15,.22),(.12,.18),(.155,.12),(.10,.07),(.06,.025),(.08,-.08)]
  shape('grip hand',pts,SKIN,-.44,True,root)
  for z in [.13,.23,.33]:line('curled finger',[(-.13,z),(-.03,z+.045),(.095,z+.035)],INK,.011,-.46,parent=root)
  line('thumb fold',[(-.12,.08),(-.04,.03),(.05,.08)],SHADE,.010,-.46,parent=root)
 group=list(set(S.objects)-before);handsets.append((mode,group))

def reference_heads(root):
 # Fresh vectors from the new turnaround, not a contour or rig from the film.
 data=json.loads((ROOT/'inputs/head-drawings.json').read_text())
 for row,yaw in zip(data,[-25,0,30]):
  before=set(S.objects);lo,top,hi,bottom=row['bbox'];cx=(lo+hi)/2;scale=1.60/(bottom-top)
  for index,path in enumerate(row['paths']):
   points=[pt for loop in path['loops'] for pt in loop];xs=[v[0] for v in points];ys=[v[1] for v in points]
   if len(points)<3 or max(xs)<lo or min(xs)>hi or max(ys)<top or min(ys)>bottom:continue
   cu=bpy.data.curves.new('A fresh head contour','CURVE');cu.dimensions='2D';cu.fill_mode='BOTH'
   for loop in path['loops']:
    if len(loop)<3:continue
    sp=cu.splines.new('POLY');sp.points.add(len(loop)-1)
    for pt,(x,y) in zip(sp.points,loop):pt.co=((x-cx)*scale,3.34+(bottom-y)*scale,0,1)
    sp.use_cyclic_u=True
   ob=bpy.data.objects.new('A reference '+row['view']+' path '+str(index),cu);S.collection.objects.link(ob);cu.materials.append(mat(path['color']));ob.rotation_euler[0]=math.pi/2;ob.location.y=-.18-index*.00012;ob.parent=root
   # Only wholly contained feature paths move; skin and skull never share these weights.
   center=((min(xs)+max(xs))/2,(min(ys)+max(ys))/2)
   if min(ys)>310 and max(ys)<384 and max(xs)-min(xs)<100:
    ec=empty('eye blink');ec.parent=root;z=3.34+(bottom-center[1])*scale;x=(center[0]-cx)*scale;ec.location=(x,0,z);ob.parent=ec;ob.matrix_parent_inverse=Matrix.Translation((-x,0,-z));eyecontrols.append(ec)
   elif min(ys)>440 and max(ys)<502 and max(xs)-min(xs)>20:
    mc=empty('mouth expression');mc.parent=root;z=3.34+(bottom-473)*scale;x=0;mc.location=(x,0,z);ob.parent=mc;ob.matrix_parent_inverse=Matrix.Translation((-x,0,-z));mouthcontrols.append(mc)
  heads.append((yaw,list(set(S.objects)-before)))

def character():
 global left,right,handroot,headroot,proot,bodyroot
 left=arm('near arm',-.64,3.22,-1);right=arm('far arm',.64,3.20,1)
 bodyroot=empty('torso acting');headroot=empty('head acting');handroot=empty('wrist and hand');proot=empty('picture')
 oval('near shoulder cap',-.64,3.22,.245,.245,RED,.015,edge=False);oval('far shoulder cap',.64,3.20,.245,.245,RED,.015,edge=False)
 shape('complete jacket',[(-.64,3.3),(-.23,3.51),(.25,3.48),(.64,3.25),(.71,2.8),(.56,1.38),(-.55,1.38),(-.68,2.7)],RED,-.07,parent=bodyroot)
 shape('jacket side shadow',[(.42,3.2),(.61,3.2),(.53,1.43),(.30,1.43)],'#A72126',-.08,parent=bodyroot,edge=False)
 shape('neck',[(-.20,3.34),(-.25,3.82),(.25,3.85),(.23,3.38),(.0,3.24)],SKIN,-.09,parent=bodyroot)
 line('neck shade',[(-.23,3.75),(.03,3.65),(.23,3.68)],SHADE,.025,-.12,parent=bodyroot)
 for sx in [-1,1]:
  x=sx*.26;pts=[(x-.11,3.43),(x+.13,3.43),(x+.14,2.08),(x-.13,2.02)]
  shape('scarf',pts,WHITE,-.14,False,parent=bodyroot)
  for z in [2.25,2.65,3.04]:shape('scarf band',[(x-.115,z),(x+.14,z+.03),(x+.14,z+.22),(x-.115,z+.19)],'#BD2929',-.17,False,bodyroot,False)
  for i in range(7):line('scarf fringe',[(x-.10+i*.032,2.08),(x-.10+i*.032,1.97)],CREAM,.013,-.18,False,False,parent=bodyroot)
 oval('club badge',.46,2.91,.13,.14,WHITE,-.14,bodyroot)
 oval('badge red',.46,2.91,.106,.117,'#BD2929',-.15,bodyroot,False)
 oval('badge blue',.46,2.91,.070,.080,'#408FBC',-.16,bodyroot,False)
 for i in range(3):shape('badge diamond',[(.43+i*.024,2.85),(.405+i*.024,2.90),(.43+i*.024,2.95),(.455+i*.024,2.90)],WHITE,-.17,False,bodyroot,False)
 for i in range(4):oval('star',.385+i*.048,3.09,.017,.017,'#E6BC56',-.15,bodyroot,False)
 line('jacket folds',[(-.53,1.80),(-.16,1.69),(.20,1.82)],'#AE2429',.014,-.14,parent=bodyroot)
 for mode in ['open','closing','grip']:hand_draw(handroot,mode)
 # Separate right hand, made new, visible resting beyond cuff.
 shape('resting hand',[(.64,1.83),(.49,1.60),(.49,1.49),(.55,1.48),(.65,1.63),(.68,1.42),(.73,1.40),(.78,1.46),(.81,1.69),(.79,1.85)],SKIN,-.34)
 reference_heads(headroot)
 # Framed picture: left edge and low grip, face forward.
 shape('picture frame',[(0,.03),(.89,.03),(.89,1.05),(0,1.05)],'#745238',-.28,False,proot)
 shape('picture paper',[(.065,.10),(.825,.10),(.825,.985),(.065,.985)],CREAM,-.30,False,proot)
 text('score','8 - 2',.445,.59,.26,INK,-.33,proot);text('year','2020',.445,.34,.10,INK,-.33,proot)
 text('room caption','MÜNCHEN',2.70,2.78,.10,CREAM,1.3)

def lerp_state(f):
 beats=C['beats'];a=beats[0];b=beats[-1]
 for p,q in zip(beats,beats[1:]):
  if p['frame']<=f<=q['frame']:a,b=p,q;break
 t=max(0,min(1,(f-a['frame'])/max(1,b['frame']-a['frame'])));t=t*t*(3-2*t)
 return {k:([a[k][i]*(1-t)+b[k][i]*t for i in range(3)] if k=='wrist' else a[k]*(1-t)+b[k]*t) for k in ['wrist','roll','head_yaw','grip']}

def solve(actor,wr):
 sh=Vector((actor['x'],0,actor['z']));d=wr-sh;L=actor['len'];D=d.length
 if D>=2*L:wr=sh+d.normalized()*(2*L-.001);d=wr-sh;D=d.length
 unit=d.normalized();perp=Vector((unit.z,0,-unit.x))*(-1);el=(sh+wr)/2+perp*math.sqrt(max(0,L*L-D*D/4))
 for bn,start,end in [('upper',sh,el),('fore',el,wr)]:
  bone=actor['rig'].pose.bones[bn];rest=actor['rig'].data.bones[bn];r=(rest.tail_local-rest.head_local).rotation_difference(end-start)
  bone.matrix=Matrix.Translation(start)@r.to_matrix().to_4x4()@rest.matrix_local.to_3x3().to_4x4();bpy.context.view_layer.update();bone.keyframe_insert('rotation_quaternion') if bone.rotation_mode=='QUATERNION' else bone.keyframe_insert('rotation_euler');bone.keyframe_insert('location')
 return wr

def animate():
 global checks
 checks=[]
 for a in [left,right]:
  for b in a['rig'].pose.bones:b.rotation_mode='QUATERNION'
 for f in range(1,C['frames']+1):
  S.frame_set(f);s=lerp_state(f);w=Vector(s['wrist']);w=solve(left,w);solve(right,Vector((.72,0,1.84)))
  handroot.location=w;handroot.rotation_euler[1]=math.radians(s['roll']);handroot.keyframe_insert('location');handroot.keyframe_insert('rotation_euler')
  propw=Vector(C['beats'][2]['wrist']) if f<34 else w
  proot.location=propw;proot.rotation_euler[1]=0 if f<34 else math.radians(s['roll']);proot.keyframe_insert('location');proot.keyframe_insert('rotation_euler')
  mode='open' if s['grip']<.28 else 'closing' if s['grip']<.88 else 'grip'
  for state,group in handsets:
   for ob in group:ob.hide_render=state!=mode;ob.hide_viewport=state!=mode;ob.keyframe_insert('hide_render');ob.keyframe_insert('hide_viewport')
  chosen=min(heads,key=lambda h:abs(h[0]-s['head_yaw']))[0]
  for yaw,group in heads:
   for ob in group:ob.hide_render=yaw!=chosen;ob.hide_viewport=yaw!=chosen;ob.keyframe_insert('hide_render');ob.keyframe_insert('hide_viewport')
  headroot.location=(.035*math.sin(f*.035),0,.02*math.sin(f*.05));headroot.keyframe_insert('location')
  checks.append({'frame':f,'wrist':list(w),'hand':mode,'head_drawing':chosen,'prop_root_error':(proot.location-handroot.location).length if f>=34 else None})
  pulse=sum(math.exp(-((f-k)/2.2)**2)*a for k,a in [(66,.7),(74,.4),(83,.6),(102,.35),(108,.45),(116,.7),(125,.4)])
  for mc in mouthcontrols:mc.scale.z=1+pulse*.6;mc.keyframe_insert('scale')
  blink=1-.94*max(math.exp(-((f-k)/1.7)**2) for k in [16,56,110])
  for ec in eyecontrols:ec.scale.z=blink;ec.keyframe_insert('scale')
 # A single untouched voice file; full audio span fits this proof.
 seq=S.sequence_editor_create();seq.strips.new_sound('Same selected Muller take',str(ROOT/'inputs/voice.wav'),channel=1,frame_start=61)

def finish():
 OUT.mkdir(parents=True,exist_ok=True)
 S.frame_set(69);bpy.context.view_layer.update();S.render.image_settings.file_format='PNG';S.render.filepath=str(OUT/'frame-0069.png');S['input_contract_sha']=__import__('hashlib').sha256((ROOT/'production.json').read_bytes()).hexdigest()
 bpy.data.libraries.write(str(OUT/'experiment-a.blend'),{S},fake_user=True)
 (OUT/'construction-check.json').write_text(json.dumps({'method':S['method'],'new_scene':True,'old_assets_imported':False,'reference_only_images':True,'head_drawings':len(heads),'hand_drawings':len(handsets),'frames':checks},indent=2))
 return {'scene':S.name,'objects':len(S.objects),'path':str(OUT/'experiment-a.blend')}
if __name__=='__main__':
 setup();environment();character();animate();finish()
