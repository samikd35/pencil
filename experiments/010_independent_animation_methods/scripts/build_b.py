"""Independent B: fresh 3D volumes, skinned sleeve geometry and graphic face.
Does not import A, an older builder, traced art, or a saved scene.
"""
import bpy,math,json,bmesh
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path('/Users/samikd/MyProjects/Pencil/experiments/010_independent_animation_methods');C=json.loads((ROOT/'production.json').read_text());OUT=ROOT/'artifacts/b-3d-v002'
INK='#29252A';SKIN='#F3B271';RED='#C92725';CREAM='#FFF1D5';WHITE='#FFF9ED';M={}
def rgb(c):
 vals=[int(c[i:i+2],16)/255 for i in (1,3,5)];return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in vals)+(1,)
def material(color,flat=False):
 key=(color,flat)
 if key in M:return M[key]
 m=bpy.data.materials.new('B '+color+str(flat));m.diffuse_color=rgb(color);m.use_nodes=True;n=m.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');em.inputs[0].default_value=rgb(color);m.node_tree.links.new(em.outputs[0],out.inputs[0])
 if not flat:
  diffuse=n.new('ShaderNodeBsdfDiffuse');diffuse.inputs[0].default_value=(1,1,1,1);srgb=n.new('ShaderNodeShaderToRGB');r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.28;r.color_ramp.elements[0].color=tuple(v*.67 for v in rgb(color)[:3])+(1,);r.color_ramp.elements[1].position=.65;r.color_ramp.elements[1].color=rgb(color);r.color_ramp.interpolation='CONSTANT';mid=r.color_ramp.elements.new(.45);mid.color=tuple(v*.87 for v in rgb(color)[:3])+(1,);m.node_tree.links.new(diffuse.outputs[0],srgb.inputs[0]);m.node_tree.links.new(srgb.outputs[0],r.inputs[0]);m.node_tree.links.new(r.outputs[0],em.inputs[0])
 M[key]=m;return m

def mesh(name,verts,faces,color,parent=None,smooth=True):
 me=bpy.data.meshes.new('B '+name);me.from_pydata(verts,[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new('B '+name,me);S.collection.objects.link(o);me.materials.append(material(color));o.parent=parent
 for p in me.polygons:p.use_smooth=smooth
 return o

def curve(name,pts,color=INK,r=.012,parent=None):
 cu=bpy.data.curves.new('B '+name,'CURVE');cu.dimensions='3D';cu.resolution_u=10;cu.bevel_depth=r;cu.bevel_resolution=2;sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
 for p,q in zip(sp.bezier_points,pts):p.co=q;p.handle_left_type=p.handle_right_type='AUTO'
 o=bpy.data.objects.new('B '+name,cu);S.collection.objects.link(o);cu.materials.append(material(color,True));o.parent=parent;return o

def sphere(name,loc,scale,color,parent=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=loc);o=bpy.context.object;o.name='B '+name;o.scale=scale;o.data.materials.append(material(color));o.parent=parent
 for p in o.data.polygons:p.use_smooth=True
 return o

def box(name,loc,scale,color,parent=None,bevel=.0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name='B '+name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material(color));o.parent=parent
 if bevel:m=o.modifiers.new('soft edges','BEVEL');m.width=bevel;m.segments=2
 return o

def empty(name):
 o=bpy.data.objects.new('B '+name,None);S.collection.objects.link(o);return o

def text(name,body,loc,size,color,parent=None):
 cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.align_x='CENTER';cu.size=size;cu.materials.append(material(color,True));o=bpy.data.objects.new('B '+name,cu);S.collection.objects.link(o);o.location=loc;o.rotation_euler[0]=math.pi/2;o.parent=parent;return o

def loft(name,rings,color,parent=None):
 N=40;verts=[];faces=[]
 for z,w,d,cy in rings:
  for j in range(N):
   t=math.tau*j/N;verts.append((w*math.cos(t),cy+d*math.sin(t),z))
 for i in range(len(rings)-1):
  for j in range(N):faces.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
 faces.extend([tuple(reversed(range(N))),tuple((len(rings)-1)*N+j for j in range(N))]);o=mesh(name,verts,faces,color,parent);sub=o.modifiers.new('surface smoothing','SUBSURF');sub.levels=1;sub.render_levels=1;return o

def setup():
 global S
 S=bpy.data.scenes.new('METHOD B - new 3D construction');bpy.context.window.scene=S;S.render.engine='CYCLES' if False else 'BLENDER_EEVEE';S.eevee.taa_render_samples=32;S.render.resolution_x=C['width'];S.render.resolution_y=C['height'];S.render.resolution_percentage=100;S.render.fps=C['fps'];S.frame_start=1;S.frame_end=C['frames'];S.view_settings.view_transform='Standard';S.world=bpy.data.worlds.new('B world');S.world.use_nodes=True;S.world.node_tree.nodes['Background'].inputs[0].default_value=(.35,.35,.35,1);S.world.node_tree.nodes['Background'].inputs[1].default_value=.7
 cd=bpy.data.cameras.new('B camera');cam=bpy.data.objects.new('B camera',cd);S.collection.objects.link(cam);cam.location=C['camera']['location'];cam.rotation_euler=(Vector(C['camera']['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cd.type='ORTHO';cd.ortho_scale=C['camera']['ortho_scale'];S.camera=cam
 ld=bpy.data.lights.new('B key','AREA');lo=bpy.data.objects.new('B key',ld);S.collection.objects.link(lo);lo.location=(-3,-5,7);lo.rotation_euler=(Vector((0,0,3))-lo.location).to_track_quat('-Z','Y').to_euler();ld.energy=650;ld.size=5
 ld=bpy.data.lights.new('B fill','AREA');lo=bpy.data.objects.new('B fill',ld);S.collection.objects.link(lo);lo.location=(4,-4,4);lo.rotation_euler=(Vector((0,0,3))-lo.location).to_track_quat('-Z','Y').to_euler();ld.energy=350;ld.size=5
 S['method']='New 3D modeled body/head/limbs/hands; native armature; drawn geometric facial features; toon shading. No image planes.';S['independence']=C['independence']
 for area in bpy.context.screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL'

def environment():
 box('wall',(0,2,3.1),(10,.12,5.8),'#D9C4A0')
 box('window frame',(-2.9,1.82,3.6),(1.4,.10,2.6),'#263F4D');box('window',(-2.9,1.74,3.62),(1.15,.06,2.3),'#8BACB5');box('window divider',(-2.9,1.66,3.62),(.045,.05,2.3),CREAM)
 for x in [-1.7,0,1.7,3.4]:box('wall trim',(x,1.86,3.4),(.025,.04,4.6),'#B99E77')
 box('cabinet',(2.7,1.4,2.15),(1.3,.65,1.7),'#816548')
 for i in range(6):box('book',(2.19+i*.15,1.04,2.2),(.105,.1,.75),['#A85242','#EFE1BE','#617A77'][i%3])
 sphere('pot',(2.72,1.35,3.12),(.23,.21,.2),'#4B6E6C')
 for x,z in [(2.48,3.6),(2.85,3.66),(2.73,3.76)]:
  o=sphere('leaf',((x+2.72)/2,1.3,(z+3.25)/2),(.065,.035,(z-3.25)/2),'#427B65');o.rotation_euler[1]=-(x-2.72)
 box('table',(0,-.55,1.16),(8,1.5,.68),'#BA8C5B',bevel=.025);box('table lip',(0,-1.3,1.50),(8,.07,.04),'#F2CB95')
 text('room caption','MÜNCHEN',(2.7,.985,2.78),.10,CREAM)

# Continuous tubular sleeve skin, actual volume through the elbow.
def limb(side,x,z):
 L=.85;ad=bpy.data.armatures.new('B '+side+' rig');rig=bpy.data.objects.new('B '+side+' rig',ad);S.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT');prev=None
 for name,za,zb in [('upper',z,z-L),('fore',z-L,z-2*L),('hand',z-2*L,z-2*L-.28)]:
  b=ad.edit_bones.new(name);b.head=(x,0,za);b.tail=(x,0,zb)
  if prev:b.parent=prev;b.use_connect=True
  prev=b
 bpy.ops.object.mode_set(mode='OBJECT');rig.select_set(False)
 N=32;R=17;verts=[];faces=[]
 for i in range(R):
  t=i/(R-1);rad=.245*(1-t)+.137*t
  for j in range(N):
   a=j*math.tau/N;verts.append((x+rad*math.cos(a),rad*.9*math.sin(a),z-t*2*L))
 for i in range(R-1):
  for j in range(N):faces.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
 faces.extend([tuple(reversed(range(N))),tuple((R-1)*N+j for j in range(N))]);o=mesh(side+' sleeve',verts,faces,RED)
 vg=[o.vertex_groups.new(name=n) for n in ['upper','fore']]
 for i,v in enumerate(verts):
  t=(z-v[2])/L;w=max(0,min(1,(t-.73)/.54));w=w*w*(3-2*w)
  if w<1:vg[0].add([i],1-w,'REPLACE')
  if w>0:vg[1].add([i],w,'REPLACE')
 mod=o.modifiers.new('continuous volume skin','ARMATURE');mod.object=rig;mod.use_deform_preserve_volume=True;sub=o.modifiers.new('soft silhouette','SUBSURF');sub.levels=1
 return {'rig':rig,'x':x,'z':z,'side':-1 if x<0 else 1,'len':L,'mesh':o}

def finger(name,base,lengths,width,parent):
 a=empty(name+' base');a.parent=parent;a.location=base;b=empty(name+' tip');b.parent=a;b.location.z=lengths[0]
 sphere(name+' upper',(0,0,lengths[0]/2),(width,width*.82,lengths[0]/2+width*.35),SKIN,a)
 sphere(name+' lower',(0,0,lengths[1]/2),(width*.86,width*.74,lengths[1]/2+width*.3),SKIN,b)
 return a,b

def head():
 global hr,eyes,mouth
 hr=empty('head pivot');hr.location=(0,0,3.45);hr.scale=(1.10,1.10,1.10)
 # Head geometry authored in local coordinates around the skull/neck junction.
 loft('angular caricature head',[(0,.14,.19,0),(.04,.25,.26,-.015),(.16,.34,.31,0),(.36,.39,.33,0),(.68,.405,.32,0),(1.01,.40,.30,0),(1.18,.28,.24,0),(1.27,.08,.09,0)],SKIN,hr)
 for sx in [-1,1]:
  sphere('ear',(sx*.435,-.01,.46),(.16,.10,.205),SKIN,hr)
  curve('ear fold',[(sx*.49,-.075,.55),(sx*.40,-.085,.57),(sx*.405,-.09,.41),(sx*.47,-.08,.38)],'#A9633D',.011,hr)
 # Quiff cap with an irregular hairline; solid volume, not a picture.
 N=48;verts=[];faces=[]
 for ring in range(9):
  t=ring/8
  for j in range(N):
   a=j*math.tau/N;front=max(0,-math.sin(a));rim=.64+.36*front+.025*math.sin(9*a)+.018*math.sin(17*a)
   z=rim+(1.39-rim)*math.sin(t*math.pi/2);rad=(1-t)**.46;verts.append((.48*math.cos(a)*rad-.035*t,.34*math.sin(a)*rad+.025,z))
 for r in range(8):
  for j in range(N):faces.append((r*N+j,r*N+(j+1)%N,(r+1)*N+(j+1)%N,(r+1)*N+j))
 mesh('hair mass',verts,faces,'#4A3528',hr)
 # Soft side-swept locks are actual volume, with small pointed ends.
 for j in range(9):
  x=-.35+j*.085
  o=sphere('hair lock',(x,-.23,1.11+.07*math.sin(j*.4)),(.17,.12,.14),'#4A3528',hr);o.rotation_euler[1]=-.5
  curve('swept hair',[(x-.08,-.337,1.075),(x+.01,-.338,1.16),(x+.11,-.28,1.22)],'#614A37',.007,hr)
 eyes=[]
 for x in [-.205,.205]:
  eye_white=sphere('eye white',(x,-.302,.64),(.126,.038,.10),WHITE,hr)
  eye=sphere('iris',(x+.018,-.344,.64),(.052,.018,.066),'#373B38',hr);pupil=sphere('pupil',(x+.024,-.361,.64),(.034,.014,.045),INK,hr);glint=sphere('eye light',(x+.010,-.373,.66),(.012,.006,.015),WHITE,hr);eyes.append((eye_white,eye,pupil,glint))
  curve('upper lid',[(x-.12,-.32,.65),(x,-.35,.737),(x+.117,-.32,.66)],INK,.010,hr)
  curve('eyebrow',[(x-.12,-.29,.82),(x-.018,-.34,.856),(x+.108,-.29,.82)],'#4A3528',.026,hr)
 # Actual projecting bridge and hooked tip rather than a flat line following the head.
 sphere('nose bridge',(0,-.342,.52),(.055,.10,.22),SKIN,hr)
 sphere('nose tip',(.01,-.437,.405),(.125,.108,.066),SKIN,hr)
 curve('nose contour',[(.037,-.423,.65),(.063,-.44,.51),(.11,-.485,.42),(.08,-.523,.38),(-.045,-.505,.379)],INK,.010,hr)
 curve('nostril',[(-.07,-.454,.385),(-.035,-.492,.375),(.052,-.48,.376)],'#9D5C37',.009,hr)
 mouth=empty('graphic mouth');mouth.parent=hr;mouth.location=(0,-.333,.225)
 # Smiling mouth is a designed graphic surface anchored to a dimensional face.
 verts=[(-.225,0,.044),(-.12,-.022,.016),(0,-.025,.011),(.12,-.02,.03),(.225,0,.072),(.15,-.012,-.047),(0,-.025,-.075),(-.12,-.02,-.049)]
 mesh('mouth dark',verts,[tuple(range(8))],'#382820',mouth,False)
 verts=[(-.205,-.004,.040),(-.1,-.03,.018),(0,-.03,.015),(.12,-.025,.03),(.203,-.004,.066),(.13,-.028,-.006),(0,-.038,-.025),(-.115,-.032,-.012)]
 mesh('teeth',verts,[tuple(range(8))],WHITE,mouth,False)
 for i in range(5):curve('teeth division',[(i*.057-.11,-.04,.01),(i*.057-.11,-.04,-.018)],'#AD9173',.003,mouth)
 for x in [-.26,.26]:curve('cheek crease',[(x,-.24,.38),(x*1.04,-.255,.30),(x*.96,-.25,.24)],'#BD8151',.007,hr)


def character():
 global near,far,handroot,proot,fingers,thumb
 near=limb('near arm',-.64,3.22);far=limb('far arm',.64,3.20)
 sphere('near sleeve shoulder',(-.64,0,3.22),(.246,.22,.246),RED);sphere('far sleeve shoulder',(.64,0,3.20),(.246,.22,.246),RED)
 loft('jacket torso',[(1.3,.49,.23,.05),(1.5,.57,.28,.04),(2.2,.58,.31,.03),(2.85,.66,.28,.02),(3.19,.66,.23,.01),(3.4,.24,.16,0)],RED)
 loft('neck',[(3.25,.20,.19,0),(3.4,.215,.20,0),(3.7,.21,.195,0)],SKIN)
 for x in [-.27,.27]:
  # Ribbon is continuous and follows the chest surface, with explicit band faces.
  verts=[];faces=[]
  for i in range(17):
   z=2.02+i*1.43/16;y=-.345+.035*math.sin((z-2)*2)
   verts.extend([(x-.115,y,z),(x+.115,y,z)])
  for i in range(16):faces.append((2*i,2*i+1,2*i+3,2*i+2))
  scarf=mesh('scarf ribbon',verts,faces,WHITE);scarf.data.materials.append(material(RED));solid=scarf.modifiers.new('scarf thickness','SOLIDIFY');solid.thickness=.025
  for poly in scarf.data.polygons:poly.material_index=1 if (poly.index//3)%2 else 0
  for j in range(7):curve('scarf fringe',[(x-.096+j*.032,-.35,2.04),(x-.096+j*.032,-.35,1.94)],CREAM,.012)
 sphere('club badge',(.46,-.253,2.91),(.13,.018,.14),WHITE);sphere('badge red',(.46,-.274,2.91),(.105,.012,.115),RED);sphere('badge blue',(.46,-.288,2.91),(.07,.008,.08),'#3C91BF')
 for i in range(3):mesh('badge diamond',[(.427+i*.024,-.30,2.855),(.406+i*.024,-.30,2.90),(.427+i*.024,-.30,2.946),(.448+i*.024,-.30,2.90)],[(0,1,2,3)],WHITE)
 for i in range(4):sphere('badge star',(.385+i*.048,-.21,3.09),(.017,.01,.017),'#E4BA53')
 head()
 handroot=empty('hand wrist');sphere('palm',(0,-.045,.12),(.133,.075,.19),SKIN,handroot)
 fingers=[]
 for i,(x,ln) in enumerate([(-.11,.23),(-.035,.29),(.045,.27),(.12,.215)]):fingers.append(finger('finger '+str(i),(x,-.04,.24),[ln*.58,ln*.42],.042 if i<3 else .036,handroot))
 thumb=finger('thumb',(-.12,-.085,.03),[.15,.10],.052,handroot)
 sphere('resting right palm',(.73,-.05,1.70),(.13,.07,.18),SKIN)
 for i in range(4):sphere('resting finger',(.62+i*.07,-.10,1.56),(.032,.04,.13),SKIN)
 proot=empty('picture');box('wood frame',(.445,.045,.54),(.89,.08,1.02),'#745238',proot,bevel=.008);box('paper',(.445,-.002,.54),(.76,.016,.89),CREAM,proot)
 text('score','8 - 2',(.445,-.019,.59),.26,INK,proot);text('year','2020',(.445,-.021,.34),.1,INK,proot)


def state_at(frame):
 seq=C['beats'];a=seq[0];b=seq[-1]
 for p,q in zip(seq,seq[1:]):
  if p['frame']<=frame<=q['frame']:a,b=p,q;break
 t=max(0,min(1,(frame-a['frame'])/max(1,b['frame']-a['frame'])));t=t*t*(3-2*t)
 return {k:([a[k][i]+(b[k][i]-a[k][i])*t for i in range(3)] if k=='wrist' else a[k]+(b[k]-a[k])*t) for k in ['wrist','roll','head_yaw','grip']}

def pose_arm(a,wr):
 sh=Vector((a['x'],0,a['z']));d=wr-sh;L=a['len'];D=d.length
 if D>=2*L:wr=sh+d.normalized()*(2*L-.001);d=wr-sh;D=d.length
 n=d.normalized();perp=Vector((n.z,0,-n.x)).normalized()*(-1);el=(sh+wr)*.5+perp*math.sqrt(max(0,L*L-D*D/4))
 for name,st,en in [('upper',sh,el),('fore',el,wr)]:
  p=a['rig'].pose.bones[name];rb=a['rig'].data.bones[name];q=(rb.tail_local-rb.head_local).rotation_difference(en-st);p.matrix=Matrix.Translation(st)@q.to_matrix().to_4x4()@rb.matrix_local.to_3x3().to_4x4();bpy.context.view_layer.update();p.keyframe_insert('rotation_quaternion');p.keyframe_insert('location')
 return wr

def animate():
 global checks
 checks=[]
 for group in eyes:
  for eye in group:eye['base_z']=eye.scale.z
 for a in [near,far]:
  for b in a['rig'].pose.bones:b.rotation_mode='QUATERNION'
 for f in range(1,C['frames']+1):
  S.frame_set(f);v=state_at(f);target=Vector(v['wrist']);target.y=-.52;w=pose_arm(near,target);pose_arm(far,Vector((.72,0,1.84)))
  handroot.location=w;handroot.rotation_euler=(0,math.radians(v['roll']),0);handroot.keyframe_insert('location');handroot.keyframe_insert('rotation_euler')
  grip=v['grip']
  for i,(a,b) in enumerate(fingers):
   a.rotation_euler[0]=math.radians(-60*grip);a.rotation_euler[1]=math.radians((i-1.5)*6*(1-grip));b.rotation_euler[0]=math.radians(-105*grip);a.keyframe_insert('rotation_euler');b.keyframe_insert('rotation_euler')
  thumb[0].rotation_euler=(math.radians(-22*grip),math.radians(40-78*grip),math.radians(-18*grip));thumb[1].rotation_euler[0]=math.radians(-42*grip);thumb[0].keyframe_insert('rotation_euler');thumb[1].keyframe_insert('rotation_euler')
  proot.location=Vector((C['beats'][2]['wrist'][0],-.52,C['beats'][2]['wrist'][2])) if f<34 else w;proot.rotation_euler[1]=0 if f<34 else math.radians(v['roll']);proot.keyframe_insert('location');proot.keyframe_insert('rotation_euler')
  hr.rotation_euler[2]=math.radians(v['head_yaw']);hr.rotation_euler[1]=math.radians(-1.5*math.sin(f*.045));hr.keyframe_insert('rotation_euler')
  # Different mouth shapes on the same timing as the unchanged spoken line.
  pulse=sum(math.exp(-((f-k)/2.2)**2)*a for k,a in [(66,.7),(74,.4),(83,.6),(102,.35),(108,.45),(116,.7),(125,.4)])
  mouth.scale.z=1+pulse*.6;mouth.keyframe_insert('scale')
  blink=1-.94*max(math.exp(-((f-k)/1.7)**2) for k in [16,56,110])
  for components in eyes:
   for eye in components:eye.scale.z=eye.get('base_z',eye.scale.z)*blink;eye.keyframe_insert('scale')
  checks.append({'frame':f,'wrist':list(w),'grip':grip,'head_yaw':v['head_yaw'],'prop_root_error':(proot.location-handroot.location).length if f>=34 else None})
 seq=S.sequence_editor_create();seq.strips.new_sound('Same selected Muller take',str(ROOT/'inputs/voice.wav'),channel=1,frame_start=61)

def outlines():
 ink=material(INK,True);ink.use_backface_culling=True
 for o in list(S.objects):
  if o.type!='MESH' or any(k in o.name for k in ['wall','window','book','badge','star','table','paper','mouth','teeth','hair tuft','scarf ribbon']):continue
  o.data.materials.append(ink);m=o.modifiers.new('drawn silhouette','SOLIDIFY');m.thickness=.011;m.offset=1;m.use_flip_normals=True;m.material_offset=len(o.data.materials)-1;m.material_offset_rim=len(o.data.materials)-1

def finish():
 OUT.mkdir(parents=True,exist_ok=True)
 S.frame_set(69);bpy.context.view_layer.update();S.render.image_settings.file_format='PNG';S.render.filepath=str(OUT/'frame-0069.png');S['input_contract_sha']=__import__('hashlib').sha256((ROOT/'production.json').read_bytes()).hexdigest();bpy.data.libraries.write(str(OUT/'experiment-b.blend'),{S},fake_user=True)
 (OUT/'construction-check.json').write_text(json.dumps({'method':S['method'],'new_scene':True,'old_assets_imported':False,'images_in_character':0,'frames':checks},indent=2))
 return {'scene':S.name,'objects':len(S.objects),'path':str(OUT/'experiment-b.blend')}
if __name__=='__main__':
 setup();environment();character();animate();outlines();finish()
