"""Video 1 dimensional pitch/goal mechanism, adapted to the current training ground."""
import bpy,math,ast,json
from mathutils import Vector
from pathlib import Path
V=Path(__file__).resolve().parents[1];ns=bpy.app.driver_namespace['b17'];s=ns['TRAIN'];cast=ns['TRAINCAST'];O=ns['O'];bpy.context.window.scene=s
# Borrow only the proven native geometry helpers, not the first film's stadium identity.
P=V.parent/'001-manchester-derby-2026-09-13';tree=ast.parse((P/'scripts/build_option_a.py').read_text());env={'bpy':bpy,'math':math,'Vector':Vector,'col':s.collection,'mat':ns['mat']};exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in ['surface','tube']],type_ignores=[]),'Video 1 geometry','exec'),env);surface,tube=env['surface'],env['tube']
if s.collection.children.get('B01 / training ground shared'):s.collection.children.unlink(bpy.data.collections['B01 / training ground shared'])
keep={o for a in [cast['Arteta'],cast['Gyokeres']] for o in a['objects']}|{cast['defender'],*cast['defender'].children_recursive}
for ob in list(s.objects):
 if ob not in keep and ob.type!='CAMERA':ob.hide_render=ob.hide_viewport=True
# Existing rigs remain in their local drawing coordinates, mounted upright in one world.
for who,loc,height in [('Arteta',(-3.8,.2,0),1.78),('Gyokeres',(-.9,1,0),1.9)]:
 a=cast[who];root=a['root'];root.location=loc;root.scale=(height/1.8,)*3;root.rotation_euler=(math.pi/2,0,0)
d=cast['defender'];d.location=(1.7,3,0);d.scale=(-1.82/4.7,1.82/4.7,1.82/4.7);d.rotation_euler=(math.pi/2,0,0)
# Native field is 68 metres wide; goal, six-yard/penalty areas and corner share coordinates.
gx,gy=3.,8.;w,h,depth=7.32,2.44,2.;left,right=gx-34,gx+34
surface('B17 field',[(left,-97,0),(right,-97,0),(right,gy,0),(left,gy,0)],'#73a45b')
for y in range(-97,9,8):surface('B17 mowing bands',[(left,y,.002),(right,y,.002),(right,min(gy,y+4),.002),(left,min(gy,y+4),.002)],'#80af65')
surface('B17 grass run-off',[(-50,-105,-.006),(55,-105,-.006),(55,16,-.006),(-50,16,-.006)],'#6d985c')
tube('B17 byline',[(left,gy,.015),(right,gy,.015)],'#fff8dd',.032)
for x in [left,right]:tube('B17 touchline',[(x,-97,.015),(x,gy,.015)],'#fff8dd',.032)
for half,dist in [(9.16,5.5),(20.16,16.5)]:tube('B17 penalty geometry',[(gx-half,gy,.015),(gx-half,gy-dist,.015),(gx+half,gy-dist,.015),(gx+half,gy,.015)],'#fff8dd',.032)
def p(x,y,z):return gx+x,gy+y,z
tube('B17 goal front',[p(-w/2,0,0),p(-w/2,0,h),p(w/2,0,h),p(w/2,0,0)],'#fffbed',.06)
for side in [-1,1]:tube('B17 goal depth',[p(side*w/2,0,h),p(side*w/2,depth,h),p(side*w/2,depth,0),p(side*w/2,0,0)],'#dedfcd',.035)
tube('B17 goal rear bar',[p(-w/2,depth,h),p(w/2,depth,h)],'#dedfcd',.028)
for i in range(31):
 x=-w/2+w*i/30;tube('B17 rear vertical net',[p(x,0,h),p(x,depth,h),p(x,depth,0)],'#d8ddcd',.006)
for j in range(11):
 z=h*j/10;tube('B17 side and back net',[p(-w/2,0,z),p(-w/2,depth,z),p(w/2,depth,z),p(w/2,0,z)],'#d8ddcd',.006)
for j in range(1,9):
 y=depth*j/8;tube('B17 roof net',[p(-w/2,y,h),p(w/2,y,h)],'#d8ddcd',.006)
# Training identity stays consistent: trees, mesh fencing, red club boards, low building.
surface('B17 training board',[(-48,14,0),(52,14,0),(52,14,.9),(-48,14,.9)],'#b94450')
for x in range(-48,53,4):tube('B17 fence posts',[(x,14,0),(x,14,4.5)],'#a0b2b0',.035)
for z in [1.4,2.3,3.2,4.2]:tube('B17 fence wires',[(-48,14,z),(52,14,z)],'#a7baba',.008)
for x in range(-48,53,2):tube('B17 fence mesh',[(x,14,.9),(x,14,4.2)],'#a7baba',.007)
for x in range(-48,53,5):
 for offset,rx,z,rz,col in [(0,3.1,4.0,2.2,'#628765'),(1.,2.5,4.8,1.6,'#80a76b')]:surface('B17 tree canopy',[(x+offset+rx*math.cos(i*math.tau/32),16,z+rz*math.sin(i*math.tau/32)) for i in range(32)],col)
for x in [-14,-4,7,19,31,42]:
 cd=bpy.data.curves.new('B17 Arsenal lettering','FONT');cd.body='ARSENAL';cd.size=.52;cd.align_x='CENTER';cd.materials.append(ns['mat']('#fff8e9'));ob=bpy.data.objects.new(cd.name,cd);s.collection.objects.link(ob);ob.location=(x,13.98,.22);ob.rotation_euler.x=math.pi/2
surface('B17 training pavilion front',[(-20,15,0),(-9,15,0),(-9,15,3.0),(-20,15,3.0)],'#bfcace');surface('B17 pavilion roof',[(-20.3,14.8,3),(-8.7,14.8,3),(-8.7,18,3.3),(-20.3,18,3.3)],'#45566a')
for x in range(-19,-9,2):surface('B17 pavilion glazing',[(x,14.97,.7),(x+1.1,14.97,.7),(x+1.1,14.97,2.5),(x,14.97,2.5)],'#83acba')
# Flags are at the actual corners, never in front of the goal mouth.
for xx in [left,right]:
 tube('B17 corner pole',[(xx,gy,0),(xx,gy,1.5)],'#fff8e9',.023);surface('B17 corner cloth',[(xx,gy,1.5),(xx+.48,gy,1.37),(xx,gy,1.10)],'#d7464b')
 sign=1 if xx==left else -1;tube('B17 corner arc',[(xx+sign*math.cos(t*math.pi/32),gy-math.sin(t*math.pi/32),.018) for t in range(17)],'#fff8dd',.025)
# Supporting goalkeeper supplies depth/scale and leaves the comic choice legible.
lib=cast['defender_library'];lib['SCENE']=s;keeper=lib['actor']('football',[7],0,0,4.7,1);keeper.location=(3.8,7.4,0);keeper.scale=(-1.85/4.7,1.85/4.7,1.85/4.7);keeper.rotation_euler=(math.pi/2,0,0);cast['keeper']=keeper
# Soft drawn contact shadows live on the ground, not on each character's picture plane.
for name,x,y,rx,ry in [('Arteta',-3.8,.2,.42,.18),('Gyokeres',-.9,1,.45,.19),('defender',1.7,3,.51,.22),('keeper',3.8,7.4,.49,.19)]:surface('B17 '+name+' contact shadow',[(x+rx*math.cos(i*math.tau/40),y+ry*math.sin(i*math.tau/40),.008) for i in range(40)],'#60824a')
# Native round ball from the first film. No flat prop sliding through a goal overlay.
tree=ast.parse((P/'scripts/build_dramatic_actions.py').read_text());benv={'bpy':bpy,'math':math,'Vector':Vector,'col':s.collection,'A':{'mat':ns['mat']}};exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='football'],type_ignores=[]),'Video 1 football','exec'),benv);ball=benv['football']('B17 native football',(0,1,.11))
s.frame_set(112);bpy.context.view_layer.update();boot=cast['Gyokeres']['root'].matrix_world@cast['Gyokeres']['C']['Rtoe'].location;start=Vector((boot.x+.08,boot.y+.05,.11));contact=Vector((1.12,3.0,.16));end=Vector((8.,8.55,.11))
for f in range(1,301):
 if f<=112:p=start.copy()
 elif f<=124:u=(f-112)/12;p=start.lerp(contact,u);p.z+=.06*math.sin(math.pi*u)
 elif f<=145:u=(f-124)/21;p=contact.lerp(end,u);p.z+=.27*math.sin(math.pi*u)
 else:p=end.copy()
 ns['keys'](ball,'location',[(f,p)]);ns['keys'](ball,'rotation_euler',[(f,(0,0,0) if f<=112 else ((f-112)*.13,(f-112)*.21,0))])
# The same world is viewed through real cameras. No independent decorative goal scaling.
def aim(cam,loc,target,lens):cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='PERSP';cam.data.lens=lens
for marker in s.timeline_markers:
 c=marker.camera;c.animation_data_clear();c.data.animation_data_clear()
 if marker.frame==1:aim(c,(2,-13,4.1),(1.8,3.5,1),40)
 elif marker.frame==97:aim(c,(3.5,-9,3.1),(2.6,4,.75),43)
 elif marker.frame==169:aim(c,(-3.1,-4.8,1.65),(-3.8,.2,1.03),49)
 else:aim(c,(right+1,gy-4,1.8),(right,gy,1),48)
s.world=bpy.data.worlds.new('B17 pale training sky');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.51,.70,.77,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.8
s['Environment']='Native dimensional pitch, goal 7.32 x 2.44 x 2m; 1.78-1.90m cast; corner at touchline/byline intersection; same training identity as unveiling.'
assert max(1.78,1.9,1.82,1.85)<h and right-(gx+w/2)>25
(O/'environment-and-contact-checks.json').write_text(json.dumps({'goal_metres':[w,h,depth],'cast_metres':[1.78,1.9,1.82,1.85],'goal_line_y':gy,'corner':[right,gy,0],'ball_start':list(start),'boot':list(boot),'deflection':list(contact),'ball_outside_post_at_byline':end.x>gx+w/2,'reference':'Video 1 build_option_a.environment / build_dramatic_actions.football','creative_acceptance':False},indent=2))
s.frame_set(40);s.camera=next(m.camera for m in s.timeline_markers if m.frame==1)
# Separate coplanar foliage layers; otherwise overlapping illustrated canopies z-fight.
for i,ob in enumerate(sorted([o for o in s.objects if o.name.startswith('B17 tree canopy')],key=lambda ob:ob.name)):ob.location.y=-.006*i
wide=next(m.camera for m in s.timeline_markers if m.frame==1);aim(wide,(1.2,-13,3.6),(1.1,3.5,1.1),39)
# Mirroring a defender must not mirror his shirt/shorts typography. Correct those
# source UV islands in the native material, leaving face/body UVs unchanged.
me=next(o for o in d.children if o.type=='MESH');material=me.data.materials[0];nodes=material.node_tree.nodes;links=material.node_tree.links;tex=next(t for t in nodes if t.type=='TEX_IMAGE' and t.image.name.startswith('football.png'))
uv=nodes.new('ShaderNodeTexCoord');sep=nodes.new('ShaderNodeSeparateXYZ');links.new(uv.outputs['UV'],sep.inputs[0]);x=sep.outputs['X'];y=sep.outputs['Y']
def mathnode(op,a,b):
 nd=nodes.new('ShaderNodeMath');nd.operation=op
 for i,v in enumerate([a,b]):
  if isinstance(v,(int,float)):nd.inputs[i].default_value=v
  else:links.new(v,nd.inputs[i])
 return nd.outputs[0]
shift=0
for x0,y0,x1,y1 in [(951,686,978,724),(1026,781,1050,812)]:
 mask=mathnode('MULTIPLY',mathnode('MULTIPLY',mathnode('GREATER_THAN',x,x0/1536),mathnode('LESS_THAN',x,x1/1536)),mathnode('MULTIPLY',mathnode('GREATER_THAN',y,1-y1/1024),mathnode('LESS_THAN',y,1-y0/1024)));delta=mathnode('MULTIPLY',mask,mathnode('SUBTRACT',(x0+x1)/1536,mathnode('MULTIPLY',x,2)));shift=mathnode('ADD',shift,delta)
combine=nodes.new('ShaderNodeCombineXYZ');links.new(mathnode('ADD',x,shift),combine.inputs['X']);links.new(y,combine.inputs['Y']);links.new(combine.outputs[0],tex.inputs['Vector'])
