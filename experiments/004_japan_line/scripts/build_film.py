"""Japan's line puzzle: native C animation and a geometrically honest camera reveal."""
from pathlib import Path
import ast, bpy, bmesh, math, json, sys, hashlib, time
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v001'
SOURCE=ROOT.parent/'001_heavy_box/artifacts/finish-v002/character-and-effects.blend'
HELPERS=ROOT.parent/'003_alisson_winner/scripts/build_film.py'
OUT.mkdir(parents=True,exist_ok=True);(OUT/'stills').mkdir(exist_ok=True)
FPS=24;SECONDS=32;FRAMES=FPS*SECONDS;STRIKE=25.375
INK='#102934';PAPER='#fff7dc';GOLD='#ffce64';BLUE='#326be8';RED='#db4050';GREEN='#71edb4';BLACK=INK
MATS={};GROUPS={};actors={}
# Reuse the tested geometry/control functions without executing the old film.
# ponytail: this name-selected reuse is tied to the recorded source; extract a shared module if another film needs the same interface.
names={'clamp','ease','mix','vec','track','rgba','mat','add','poly','line','rect','oval','label','disk','empty','visible','key','character','pose','joint','set_actor'}
nodes=[n for n in ast.parse(HELPERS.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names]
assert len(nodes)==len(names)
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(HELPERS),'exec'),globals())
base_pose=pose
scene=bpy.data.scenes.new('How Was This Ball Still In?');bpy.context.window.scene=scene
art=bpy.data.collections.new('Japan - authored artwork');scene.collection.children.link(art)
scene.render.engine='BLENDER_EEVEE';scene.eevee.taa_render_samples=32
scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.render.resolution_percentage=100
scene.render.fps=FPS;scene.frame_start=1;scene.frame_end=FRAMES
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.compression=15
scene.render.use_compositing=False;scene.render.use_sequencer=False
scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
world=bpy.data.worlds.new('Soft stadium light');world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.18,.24,.27,1);world.node_tree.nodes['Background'].inputs[1].default_value=.45;scene.world=world
camdata=bpy.data.cameras.new('Directed camera');camera=bpy.data.objects.new('Directed camera',camdata);art.objects.link(camera)
camdata.type='ORTHO';camdata.sensor_fit='VERTICAL';camdata.ortho_scale=12;camdata.clip_end=250;scene.camera=camera
font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf')
regular=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial.ttf')

# Full-bleed field, shallow stands and selectively placed foreground detail.
rect('Night sky',-150,-40,300,80,'#123442',-18)
rect('Stand mass',-150,1.85,300,8,'#183b4a',-17)
for row in range(5):
    y=2.25+row*.38
    line('Terrace rail',[(-140,y),(140,y)],'#416172',.025,-16)
    verts=[];faces=[]
    for i in range(510):
        x=-130+i*.51+(row%2)*.18;n=len(verts)
        verts.extend([(x,y+.08,-15),(x+.13,y+.08,-15),(x+.10,y+.24,-15),(x+.02,y+.24,-15)]);faces.append((n,n+1,n+2,n+3))
    me=bpy.data.meshes.new('Audience silhouettes');me.from_pydata(verts,[],faces);me.materials.append(mat(['#778b92','#577482','#718184'][row%3]));add(bpy.data.objects.new('Audience row',me))
rect('Pitch',-140,-40,280,42,'#257c65',-12)
for i in range(18):rect('Turf stripe',-140,-36+i*2.15,280,.9,'#28846b',-11.8)
line('Far sideline',[(-140,1.9),(140,1.9)],'#81b59a',.035,-11.5)
for i in range(75):
    x=-35+i*.68;y=-4.8+(i%7)*.67
    line('Fine grass',[(x,y),(x+.05,y+.06),(x+.1,y)],'#368e70',.012,-11.4)

# Load the original editable C shape/control set.
keep={'Bean torso','Head','Head_outline','Eye_0','Eye_1','Brow_0','Brow_1','Mouth','Mouth open','CTRL_Body','CTRL_Head','ANCHOR_Shoulder'}
for side in ('far','near'):
    keep.update(f'{p}_{side}' for p in ('Mitten','Shoe','Arm','Leg'))
    keep.update(f'{p}_{side}_outline' for p in ('Mitten','Shoe'))
    keep.update(f'CTRL_{p}_{side}' for p in ('Hand','Foot','Elbow','Knee'))
with bpy.data.libraries.load(str(SOURCE),link=False) as (src,dst):
    assert keep.issubset(src.objects);dst.objects=list(keep)
template={o.name:o for o in dst.objects}
for name,color,num in [('Mitoma',BLUE,'9'),('Tanaka',BLUE,'17'),('Spain defender',RED,'5'),('Unai Simon','#89bb9b','23')]:
    a=character(name,color,num)
    a['m']['Bean torso'].scale.x=1.30
    a['number'].data.size=.34
    a['number'].data.materials[0]=mat(PAPER if color!=BLUE else '#fff0a7')
    for side in ('far','near'):a['m']['Shoe_'+side].data.materials[0]=mat('#f06c64' if color==BLUE else '#dbe7cf')
    # A small white waistband preserves the established bean body while identifying Japan's kit.
    if color==BLUE:
        ob=poly(name+' white shorts',[(-.17,.14),(.17,.14),(.16,.36),(-.16,.36)],PAPER,.27,parent=a['m']['CTRL_Body']);a['all'].append(ob)

def blend_pose(a,b,u):
    u=ease(u);p={}
    for k,v in a.items():
        if k in ('hands','feet'):p[k]=[vec(x,y,u) for x,y in zip(v,b[k])]
        elif isinstance(v,tuple):p[k]=vec(v,b[k],u)
        else:p[k]=mix(v,b[k],u)
    return p

def pose(mode,t=0):
    if mode=='chase':
        p=base_pose('run',t/.53);p['focus']=.85;p['tilt']=-.32;p['headtilt']=-.10
        q=base_pose('ready',0);q.update(hip=(-.10,.84),tilt=-.90,headtilt=-.36,feet=[(-1.26,.25,.35),(1.52,.12,0)],hands=[(-.72,1.28,.4),(1.24,1.30,-.4)],focus=.9)
        if t>1.45:p=blend_pose(p,q,(t-1.45)/1.15)
        return p
    if mode=='hook':
        p=pose('chase',2.6)
        q=base_pose('ready',0);q.update(hip=(.30,.66),tilt=-.70,headtilt=-.15,feet=[(-.57,.19,.2),(.66,.66,-.6)],hands=[(-.13,.38,0),(.95,.12,-.2)],focus=.85)
        if t<.45:return blend_pose(p,q,t/.45)
        r=base_pose('ready',t);r.update(hip=(.46,1.38),feet=[(.06,.12,0),(.90,.12,0)],tilt=-.25,focus=.75)
        return blend_pose(q,r,(t-.45)/.9)
    if mode=='knee_finish':
        p=base_pose('ready',t);p['focus']=.9
        q=base_pose('ready',0);q.update(hip=(.0,1.21),tilt=-.24,headtilt=-.16,feet=[(-.40,.12,0),(.56,.80,-.6)],hands=[(-.83,2.10,.25),(.95,2.29,-.45)],focus=.95)
        r=base_pose('ready',0);r.update(hip=(.28,1.05),tilt=-.55,feet=[(-.05,.12,0),(.88,.25,-.1)],hands=[(-.50,.80,.2),(.86,.83,-.4)],focus=.6)
        if t<0:return blend_pose(p,q,(t+.75)/.75)
        return blend_pose(q,r,t/.5)
    return base_pose(mode,t)

def mitoma_motion(t,f):
    u=min(2.6,max(0,t))
    speed=2.56/.53
    x=(-.65-speed*(1.45-u)) if u<1.45 else mix(-.65,.76,ease((u-1.45)/1.15))
    result=set_actor('Mitoma',x,-2.3,1,1,'chase',u,f,depth=1.5)
    for i in range(2):
        ob=actors['Mitoma']['m']['Eye_'+str(i)];ob.location=(-.03+i*.32+.06,.04-.10*ease((u-1.45)/1.15),0);key(ob,f,False)
    return result

# Accurate tangency against the real shoe drawing at the frozen hook.
mitoma_motion(2.6,1);scene.frame_set(1);bpy.context.view_layer.update()
shoe=actors['Mitoma']['m']['Shoe_near'];boot=[(shoe.matrix_world@v.co)[:2] for v in shoe.data.vertices]
def contour_distance(points,p):
    ds=[]
    for a,b in zip(points,points[1:]+points[:1]):
        dx,dy=b[0]-a[0],b[1]-a[1];u=clamp(((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy))
        ds.append(math.hypot(p[0]-a[0]-u*dx,p[1]-a[1]-u*dy))
    return min(ds)
R2=.22;lo,hi=1.2,2.2
for _ in range(50):
    mid=(lo+hi)/2
    if contour_distance(boot,(mid,-2.08))>R2+.0205:lo=mid
    else:hi=mid
TOUCH=((lo+hi)/2,-2.08);EDGE=TOUCH[0]-.18
assert abs(contour_distance(boot,TOUCH)-R2-.0205)<1e-6
poly('Goal line at the cutback',[(EDGE-.095,-7),(EDGE,-7),(EDGE+2.05,1.88),(EDGE+1.955,1.88)],PAPER,-10,'byline')
# Shift the line so its outside edge at the ball's ground projection is EDGE.
line_shift=( -2.08+7)/8.88*2.05
for ob in GROUPS['byline']:ob.location.x=-line_shift

ball=empty('Match ball');disk('Ball face',0,0,R2,PAPER,2.4,parent=ball)
line('Ball ink',oval(0,0,R2,R2),INK,.025,2.42,parent=ball,closed=True)
poly('Ball central panel',[(.082*math.cos(i*math.tau/5),.082*math.sin(i*math.tau/5)) for i in range(5)],INK,2.43,parent=ball)
for i in range(5):
    a=i*math.tau/5;line('Ball seam',[(.075*math.cos(a),.075*math.sin(a)),(.21*math.cos(a),.21*math.sin(a))],INK,.017,2.44,parent=ball)
ballobjs=[ball]+list(ball.children)
ballshadow=poly('Ball contact shadow',oval(0,0,.22,.055),'#164f45',-6)
speedlines=[]
for i in range(10):speedlines.append(line('Sprint streak',[(-1,0),(0,0)],'#77b59a',.025,-5))
impact=empty('Cutback contact accent')
for i in range(6):
    a=i*math.tau/6;line('Contact ray',[(.30*math.cos(a),.30*math.sin(a)),(.49*math.cos(a),.49*math.sin(a))],GOLD,.032,2.5,'impact',impact)

# Opposite-post finish, a deliberately condensed second camera setup.
gx=-11.9;gy=-2.40;gw=3.1;gh=2.75;net=[]
poly('Goal shade',[(gx,gy),(gx+gw,gy),(gx+gw-.45,gy+gh+.25),(gx-.45,gy+gh+.25)],'#1c554c',-7,'goal_art')
for i in range(13):
    x=gx+i*gw/12;ob=line('Net vertical',[(x,gy),(x-.45,gy+gh+.25)],'#88af9a',.018,-6,'goal_art');net.append((ob,[(x,gy),(x-.45,gy+gh+.25)]))
for i in range(10):
    y=gy+i*gh/9;ob=line('Net horizontal',[(gx,y),(gx+gw,y)],'#88af9a',.018,-5.9,'goal_art');net.append((ob,[(gx,y),(gx+gw,y)]))
line('Goal frame',[(gx,gy),(gx,gy+gh),(gx+gw,gy+gh),(gx+gw,gy)],PAPER,.085,-5.5,'goal_art')
line('Goal depth',[(gx,gy+gh),(gx-.45,gy+gh+.25),(gx+gw-.45,gy+gh+.25),(gx+gw,gy+gh)],'#bdccbb',.04,-5.6,'goal_art')
line('Finish goal line',[(gx-1,gy),(gx+gw+1,gy)],PAPER,.04,-8,'goal_art')
line('Six yard area',[(gx-1,gy),(gx-.1,gy-2),(gx+gw+2,gy-2),(gx+gw+1,gy)],'#80b597',.04,-8,'goal_art')

# Macro scene. Its sphere is fixed throughout the camera orbit.
MX=1000.;R=.75;CX=R-.055
macro=bpy.data.collections.new('Illustrative rule geometry');scene.collection.children.link(macro)
def macro_obj(ob):
    for c in list(ob.users_collection):c.objects.unlink(ob)
    macro.objects.link(ob);return ob
def physical(name,color,rough=.5):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=rgba(color);n.inputs['Roughness'].default_value=rough;return m
grass=physical('Macro turf','#164b40',.95)
n=grass.node_tree.nodes;noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=85;noise.inputs['Detail'].default_value=2
bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.16;bump.inputs['Distance'].default_value=.025;grass.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height']);grass.node_tree.links.new(bump.outputs['Normal'],n.get('Principled BSDF').inputs['Normal'])
bpy.ops.mesh.primitive_plane_add(size=200,location=(MX,0,-.003));ground=macro_obj(bpy.context.object);ground.name='Illustrative turf';ground.data.materials.append(grass)
bpy.ops.mesh.primitive_plane_add(size=2,location=(MX-.10,0,.001));stripe=macro_obj(bpy.context.object);stripe.name='Line - outer edge x=0';stripe.scale=(.10,80,1);stripe.data.materials.append(physical('Chalk','#f5f1da',.98))
for name,pos,power,size in [('Key',(-3,-4,7),350,5),('Fill',(4,-1,5),160,4),('Rim',(0,4,6),200,3)]:
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;ob=bpy.data.objects.new(name,d);macro.objects.link(ob);ob.location=(MX+pos[0],pos[1],pos[2]);ob.rotation_euler=(Vector((MX+.4,0,.3))-ob.location).to_track_quat('-Z','Y').to_euler()
macroball=bpy.data.objects.new('Frozen sphere - illustrative, not measured',None);macro.objects.link(macroball);macroball.location=(MX+CX,0,R)
bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,radius=R);sphere=macro_obj(bpy.context.object);sphere.name='Whole sphere';sphere.parent=macroball;sphere.location=(0,0,0)
sphere.data.materials.append(physical('Ball ivory','#fff8e6',.43))
for p in sphere.data.polygons:p.use_smooth=True
# Spherical pentagons and seams derived from a truncated icosahedron.
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1)
ico=bpy.context.object;vs=[v.co.normalized() for v in ico.data.vertices];edges=[tuple(e.vertices) for e in ico.data.edges];triangles=[tuple(p.vertices) for p in ico.data.polygons];bpy.data.objects.remove(ico,do_unlink=True)
directed={}
for a,b in edges:
    directed[a,b]=(2*vs[a]+vs[b]).normalized();directed[b,a]=(2*vs[b]+vs[a]).normalized()
panels=[]
for i,v in enumerate(vs):
    neigh=[b for a,b in directed if a==i];u=(directed[i,neigh[0]]-v*directed[i,neigh[0]].dot(v)).normalized();w=v.cross(u)
    neigh.sort(key=lambda b:math.atan2(directed[i,b].dot(w),directed[i,b].dot(u)))
    panels.append(([directed[i,b] for b in neigh],True))
for a,b,c in triangles:panels.append(([directed[a,b],directed[b,a],directed[b,c],directed[c,b],directed[c,a],directed[a,c]],False))
navy=physical('Ball navy panels',INK,.48)
def spherical_tri(a,b,c,level,points,faces):
    if level:
        ab=(a+b).normalized();bc=(b+c).normalized();ca=(c+a).normalized()
        for p,q,r in [(a,ab,ca),(ab,b,bc),(ca,bc,c),(ab,bc,ca)]:spherical_tri(p,q,r,level-1,points,faces)
    else:
        i=len(points);points.extend([tuple(a*R*1.002),tuple(b*R*1.002),tuple(c*R*1.002)]);faces.append((i,i+1,i+2))
for idx,(points,dark) in enumerate(panels):
    if dark:
        center=sum(points,Vector()).normalized();verts=[];faces=[]
        for a,b in zip(points,points[1:]+points[:1]):spherical_tri(center,a,b,2,verts,faces)
        me=bpy.data.meshes.new('Curved panel');me.from_pydata(verts,[],faces)
        bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
        me.materials.append(navy);ob=bpy.data.objects.new('Pentagon '+str(idx),me);macro.objects.link(ob);ob.parent=macroball
        for p in me.polygons:p.use_smooth=True
    for a,b in zip(points,points[1:]+points[:1]):
        d=bpy.data.curves.new('Panel seam','CURVE');d.dimensions='3D';d.bevel_depth=.004;d.bevel_resolution=1;s=d.splines.new('POLY');s.points.add(8)
        for p,u in zip(s.points,[i/8 for i in range(9)]):p.co=(*(a.lerp(b,u).normalized()*R*1.003),1)
        d.materials.append(navy);ob=bpy.data.objects.new('Spherical seam',d);macro.objects.link(ob);ob.parent=macroball
# Highlight the actual cap that remains over x<=0, with no invented dimension label.
capverts=[];capfaces=[];theta=math.acos(CX/R)
for i in range(13):
    ang=theta*i/12
    for j in range(65):
        a=math.tau*j/64;capverts.append((-R*math.cos(ang)*1.006,R*math.sin(ang)*math.cos(a)*1.006,R*math.sin(ang)*math.sin(a)*1.006))
for i in range(12):
    for j in range(64):k=i*65+j;capfaces.append((k,k+1,k+66,k+65))
me=bpy.data.meshes.new('Overlapping spherical cap');me.from_pydata(capverts,[],capfaces);me.materials.append(mat(GREEN));cap=bpy.data.objects.new('Actual overlap highlight',me);macro.objects.link(cap);cap.parent=macroball
boundary=line('Illustrated outer boundary',[(0,-1.1),(0,1.1)],GOLD,.014,R*2+.10,'boundary');boundary.location.x=MX
arrow=line('Overlap pointer',[(-.58,.75),(-.58,.12),(-.05,.12)],GOLD,.019,R*2+.11,'boundary');arrow.location.x=MX
arrowhead=poly('Overlap arrowhead',[(-.05,.12),(-.17,.18),(-.17,.06)],GOLD,R*2+.12,'boundary');arrowhead.location.x=MX

# Camera-attached typography. The action stays full bleed.
hud=empty('Screen typography');hud.parent=camera;hud.location=(0,0,-4)
def title(group,text,y,size=1.05,c=PAPER):
    shadow=label(group+' shadow',text,.025,y-.025,size,INK,-.002,group,hud)
    ob=label(group,text,0,y,size,c,0,group,hud)
    ob.visible_shadow=False;shadow.visible_shadow=False
    bpy.context.view_layer.update()
    factor=min(1,7.8/max(.001,ob.dimensions.x))
    ob.data.size*=factor;shadow.data.size*=factor
    return ob
title('match_tag','JAPAN  /  SPAIN  /  2022',6.35,.33,'#d6e6d5')
title('macro_tag','RULE ILLUSTRATION',6.35,.34,'#d6e6d5')
title('question','IN OR OUT?',4.95,1.30)
title('looks_out','LOOKS OUT...',4.95,1.14)
title('angle','CHANGE THE ANGLE.',4.95,.95)
title('still_in','STILL IN.',4.95,1.32,GREEN)
title('overlap_text','PART OF THE BALL',-4.45,.65)
title('overlap_text','IS STILL OVER THE LINE.',-5.22,.65)
title('rule','THE WHOLE BALL',4.95,1.00)
title('rule','MUST CROSS THE LINE.',-4.9,.74)
title('out_demo','NOW IT IS OUT.',4.95,1.12,'#ff897a')
title('in_demo','THIS IS STILL IN.',4.95,1.12,GREEN)
title('demo_note','ILLUSTRATIVE COMPARISON',-5.75,.29,'#d6e6d5')
title('resolved','IN.',4.9,1.75,GREEN)
title('play_on','MITOMA KEEPS IT ALIVE.',4.95,.95)
title('tanaka','TANAKA!',4.95,1.35)
title('goal','GOAL STOOD.',4.95,1.3,GREEN)
title('end','JAPAN  2 - 1  SPAIN',4.95,1.1)
title('end','1 DECEMBER 2022',-4.9,.38,'#d6e6d5')
title('end','THE WHOLE BALL. THE WHOLE LINE.',-5.65,.46)
for ob in GROUPS['boundary']:ob.visible_shadow=False

def set_camera(x,y,height,f,shake=0):
    camera.location=(x+shake,y,70);camera.rotation_euler=(0,0,0);camdata.ortho_scale=height
    key(camera,f,False);camdata.keyframe_insert(data_path='ortho_scale',frame=f)
    hud.scale=(height/16,)*3;key(hud,f)
def macro_camera(t,f):
    u=ease((t-5.0)/4.0);theta=mix(math.radians(22),math.pi/2,u);az=mix(.58,0,u)
    target=Vector((MX+.50,0,.25*(1-u)))
    camera.location=target+Vector((7*math.cos(theta)*math.sin(az),-7*math.cos(theta)*math.cos(az),7*math.sin(theta)))
    camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();camdata.ortho_scale=mix(4.7,4.2,u)
    key(camera,f,False);camdata.keyframe_insert(data_path='ortho_scale',frame=f)
    hud.scale=(camdata.ortho_scale/16,)*3;key(hud,f)

def opening_ball(t):
    if t<=2.6:
        x=(-.65-(2.56/.53)*(1.45-t)+1.85) if t<1.45 else mix(1.20,TOUCH[0],ease((t-1.45)/1.15))
        return (x,-2.08+.05*abs(math.sin(t*8))*(1-clamp(t/2.6)))
    return TOUCH

# Knee contact is taken from the evaluated animated leg at the authored finish pose.
set_actor('Tanaka',-8.38,-2.40,.92,1,'knee_finish',0,1,depth=1)
scene.frame_set(1);bpy.context.view_layer.update()
leg=actors['Tanaka']['m']['Leg_near'].evaluated_get(bpy.context.evaluated_depsgraph_get())
bp=leg.data.splines[0].bezier_points
a,b=bp[0],bp[1]
curve=[]
for i in range(101):
    u=i/100;v=(1-u)**3*a.co+3*(1-u)**2*u*a.handle_right+3*(1-u)*u*u*b.handle_left+u**3*b.co
    curve.append((leg.matrix_world@v)[:2])
# The incoming cutback meets the rightmost visible bend of the near leg.
KNEE=max(curve,key=lambda p:p[0]);FINISH=(KNEE[0]+R2+.026*.92,KNEE[1])

caption_spans={'match_tag':[(0,4),(19,32)],'macro_tag':[(4,14)],'question':[(.4,4)],'looks_out':[(4,5.4)],'angle':[(5.4,9.2)],'still_in':[(9.2,14)],'overlap_text':[(10,14)],'rule':[(14,15.75)],'out_demo':[(15.75,17.35)],'in_demo':[(17.7,19)],'demo_note':[(14,19)],'resolved':[(19,21)],'play_on':[(21,24.5)],'tanaka':[(24.5,26.3)],'goal':[(26.3,29)],'end':[(29,32)]}
started=time.monotonic();checks={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'helper_sha256':hashlib.sha256(HELPERS.read_bytes()).hexdigest(),'boot_gap':contour_distance(boot,TOUCH)-R2-.0205,'touch':TOUCH,'finish':FINISH,'macro_radius':R,'macro_in_center_x':CX,'macro_out_center_x':R+.13,'in_overlap':R-CX,'out_clearance':.13,'geometry_units':'Illustrative, not an authentic measurement of the incident.'}
for f in range(1,FRAMES+1):
    t=(f-1)/FPS;macro_on=4<=t<19
    for g,spans in caption_spans.items():visible(GROUPS[g],any(a<=t<b for a,b in spans),f)
    visible(GROUPS['byline'],t<4 or 19<=t<23.1,f)
    visible(GROUPS['goal_art'],t>=23.1,f)
    visible([cap],9.5<=t<14 or 18.1<=t<19,f)
    visible(GROUPS['boundary'],9.5<=t<14,f)
    visible([macroball]+[o for o in macroball.children if o!=cap],macro_on,f)
    visible(ballobjs+[ballshadow],not macro_on,f)
    show_mitoma=t<4 or 19<=t<23.1 or t>=28
    visible(actors['Mitoma']['all'],show_mitoma,f)
    visible(actors['Tanaka']['all'],t>=23.1,f)
    visible(actors['Spain defender']['all'],23.1<=t<28.3,f)
    visible(actors['Unai Simon']['all'],23.1<=t<28.3,f)
    visible(GROUPS['impact'],(2.60<=t<2.78) or (21<=t<21.18) or (STRIKE<=t<25.55),f)
    if t<4:
        mitoma_motion(min(t,2.6),f)
        x=(-.65-(2.56/.53)*(1.45-t)+1.65) if t<1.30 else track(t,[(1.3,.2755),(2.6,.58),(4,.62)])[0]
        h=track(t,[(0,9.4),(1.4,9.4),(2.6,8.3),(4,8.1)])[0]
        set_camera(x,-.30,h,f)
        pos=opening_ball(t)
    elif macro_on:
        macro_camera(t,f)
        c=CX
        if t>=14:c=track(t,[(14,CX),(15.5,R+.13),(16.7,R+.13),(18.1,CX),(19,CX)])[0]
        macroball.location=(MX+c,0,R);key(macroball,f)
        pos=TOUCH
    elif t<21:
        mitoma_motion(2.6,f);set_camera(.62,-.30,8.1,f);pos=TOUCH
    elif t<23.1:
        u=t-21;set_actor('Mitoma',.76,-2.3,1,1,'hook',u,f,depth=1.5)
        pos=vec(TOUCH,(-4.9,-1.40),clamp(u/2.1));pos=(pos[0],pos[1]+.28*math.sin(math.pi*clamp(u/2.1)))
        set_camera(mix(.62,-2.5,ease(u/2.1)),-.25,mix(8.1,9.0,ease(u/2.1)),f)
    elif t<28.3:
        if t<STRIKE:pos=vec((-4.9,-1.40),FINISH,clamp((t-23.1)/(STRIKE-23.1)))
        elif t<26.25:pos=vec(FINISH,(-11.60,-1.70),clamp((t-STRIKE)/(26.25-STRIKE)))
        else:
            u=t-26.25;pos=(-11.60+.25*(1-math.exp(-u*3)),-2.18+.48*math.exp(-u*2.7)*abs(math.cos(u*5)))
        set_actor('Tanaka',-8.38,-2.40,.92,1,'knee_finish' if t<26.1 else 'celebrate',t-STRIKE,f,depth=1)
        set_actor('Spain defender',-6.70,-2.80,.74,-1,'watch' if t<26.25 else 'disbelief',t,f,depth=.4)
        set_actor('Unai Simon',-10.55,-2.27,.76,1,'keeper' if t<26.25 else 'watch',t,f,depth=-1)
        set_camera(track(t,[(23.1,-6.5),(24.8,-9.05),(STRIKE,-9.5),(26.25,-9.65),(28.3,-9.5)])[0],-.20,10.2,f,.03*math.sin((t-26.25)*70)*math.exp(-(t-26.25)*13) if 26.25<=t<26.6 else 0)
    else:
        u=t-28.3;set_actor('Tanaka',-9.55,-2.1,1.03,1,'celebrate',u,f,depth=1)
        set_actor('Mitoma',mix(-6.6,-7.85,ease(u/1.4)),-2.1,.98,-1,'run' if u<1.1 else 'celebrate',u/.6 if u<1.1 else u,f,depth=.8)
        set_camera(-8.65,-.10,8.8,f);pos=(-11.3,-2.18)
    ball.location=(*pos,0);ball.rotation_euler.z=-min(t,2.6)*8 if t<21 else -2.6*8+(t-21)*9;key(ball,f)
    ballshadow.location=(pos[0],-2.28,0);ballshadow.scale=(1,max(.4,1-(pos[1]+2.08)*.35),1);key(ballshadow,f)
    impact.location=(*(FINISH if t>24 else TOUCH),0);key(impact,f)
    for i,ob in enumerate(speedlines):
        visible([ob],t<2.25 or 21.10<t<22.75,f)
        ob.location=(pos[0]-1-(i%4)*.36,-2.00+i*.24,0);ob.scale=(.55+(i%3)*.3,1,1);key(ob,f)
    for ob,pts in net:
        for p,(x,y) in zip(ob.data.splines[0].points,pts):
            u=max(0,t-26.25);kick=.16*math.exp(-u*4)*math.sin(u*28) if t>=26.25 else 0;p.co=(x+kick,y,-6,1)
            p.keyframe_insert(data_path='co',frame=f)

# Native interpolation is linear between the densely authored frames; visibility cuts stay discrete.
for action in bpy.data.actions:
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path in ('hide_render','hide_viewport') else 'LINEAR'
scene.frame_set(63);bpy.context.view_layer.update()
valid=sum(1 for a in actors.values() for ob in a['m'].values() if ob.data and ob.data.animation_data for fc in ob.data.animation_data.drivers if fc.driver.is_valid)
assert valid==48*len(actors),valid
assert CX-R<0 and R+.13-R>0
checks.update(frames=FRAMES,fps=FPS,seconds=SECONDS,valid_limb_drivers=valid,bake_seconds=time.monotonic()-started)
(OUT/'build-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
scene['Reconstruction']='Stylized Japan-Spain 2022. Macro geometry demonstrates Law 9; not an exact measured reconstruction.'
scene['Sources']='FIFA goal and match account; RTVE replay analysis; IFAB Law 9.'
for ob in template.values():
    if not ob.users_collection:bpy.data.objects.remove(ob)
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False
scene.render.filepath='//stills/';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'japan-line.blend'))
if '--samples' in sys.argv:
    scene.render.resolution_percentage=60
    for t in [0,.7,1.8,2.625,3.5,4.7,6.5,9.8,11.5,14.5,16.0,18.3,20,21.5,23.5,STRIKE,26.3,28,30.5]:
        f=round(t*FPS)+1;scene.frame_set(f);scene.render.filepath=str(OUT/f'stills/sample-{f:04}.png');bpy.ops.render.render(write_still=True)
print('JAPAN_BUILD_READY',flush=True)
