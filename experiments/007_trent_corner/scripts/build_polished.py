"""Advanced stickman revision: editable 2.5D puppets on one coherent 3D field."""
from pathlib import Path
from collections import deque
import bpy, math, json, sys, os, random, ast
import numpy as np
from mathutils import Vector, Quaternion
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts'/os.environ.get('PENCIL_REVISION','film-v004')
OUT.mkdir(parents=True,exist_ok=True);(OUT/'stills').mkdir(exist_ok=True)
FPS=24;FRAMES=912
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.name='Advanced stickman / Trent corner';s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=32
s.render.resolution_x=1080;s.render.resolution_y=1920;s.render.resolution_percentage=100;s.render.fps=FPS;s.render.fps_base=1;s.frame_start=1;s.frame_end=FRAMES
s.render.use_sequencer=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=15
s.view_settings.view_transform='Standard';s.view_settings.look='None'
s.world.color=(.12,.16,.23);s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.11,.15,.22,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.55
M={};INK='#152027';CREAM='#fff1d3';GOLD='#f4ce75'
def rgb(h):
    vals=[int(h[i:i+2],16)/255 for i in (1,3,5)];return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in vals)+(1,)
def mat(c,flat=False):
    if (c,flat) not in M:
        m=bpy.data.materials.new(c+(' / ink' if flat else ''));m.diffuse_color=rgb(c);m.use_nodes=True
        n=m.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');sh=n.new('ShaderNodeEmission' if flat else 'ShaderNodeBsdfDiffuse');sh.inputs[0].default_value=rgb(c);m.node_tree.links.new(sh.outputs[0],out.inputs['Surface']);M[c,flat]=m
    return M[c,flat]
def mesh(name,vs,faces,material):
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],faces);me.materials.append(material);o=bpy.data.objects.new(name,me);s.collection.objects.link(o);return o
def poly(name,vs,c,flat=False):return mesh(name,vs,[list(range(len(vs)))],mat(c,flat))
def line(name,pts,c=CREAM,r=.025,flat=False):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=r;d.bevel_resolution=3;sp=d.splines.new('POLY');sp.points.add(len(pts)-1)
    for p,co in zip(sp.points,pts):p.co=(*co,1)
    d.materials.append(mat(c,flat));o=bpy.data.objects.new(name,d);s.collection.objects.link(o);return o
def sphere(name,loc,scale,c,flat=False):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(mat(c,flat))
    for p in o.data.polygons:p.use_smooth=True
    return o
def boot_mesh(name):
    outline=[(-.11,-.18),(.11,-.18),(.135,.10),(.10,.24),(-.10,.24),(-.135,.10)]
    vs=[(x,y,z) for z in (-.085,.085) for x,y in outline];faces=[tuple(range(5,-1,-1)),tuple(range(6,12))]+[(i,(i+1)%6,(i+1)%6+6,i+6) for i in range(6)]
    ob=mesh(name,vs,faces,mat('#efd9a4',True));bevel=ob.modifiers.new('Rounded boot edges','BEVEL');bevel.width=.025;bevel.segments=3
    sole=poly(name+' / Sole',[(x,y,-.08) for x,y in outline],INK,True);sole.parent=ob
    for y in (-.04,.015,.07):
        lace=line(name+' / Lace',[(-.055,y,.09),(.055,y,.09)],INK,.008,True);lace.parent=ob
    return ob

def empty(name,parent=None):
    o=bpy.data.objects.new(name,None);s.collection.objects.link(o);o.parent=parent;return o
def ease(x):x=min(1,max(0,x));return x*x*(3-2*x)
def lerp(a,b,u):return Vector(a).lerp(Vector(b),u)
def key(o,f):
    for prop in ('location','rotation_euler','scale'):o.keyframe_insert(data_path=prop,frame=f)
def show(o,on,f):
    if o.get('visible')!=on:
        if 'visible' in o and f>1:
            o.keyframe_insert(data_path='hide_render',frame=f-1);o.keyframe_insert(data_path='hide_viewport',frame=f-1)
        o.hide_render=o.hide_viewport=not on;o.keyframe_insert(data_path='hide_render',frame=f);o.keyframe_insert(data_path='hide_viewport',frame=f);o['visible']=on
def update_line(o,pts,f):
    for p,co in zip(o.data.splines[0].points,pts):p.co=(*co,1);p.keyframe_insert(data_path='co',frame=f)
# Pitch lighting and restrained material texture.
grass=mat('#3c794c');nt=grass.node_tree;n=nt.nodes;diff=next(x for x in n if x.type=='BSDF_DIFFUSE');tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=120;tex.inputs['Detail'].default_value=2
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.15;ramp.color_ramp.elements[0].color=rgb('#356c43');ramp.color_ramp.elements[1].position=.85;ramp.color_ramp.elements[1].color=rgb('#528958');nt.links.new(tex.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],diff.inputs[0])
mesh('Continuous turf plane',[(-55,-10,-.035),(55,-10,-.035),(55,75,-.035),(-55,75,-.035)],[(0,1,2,3)],grass)
for j in range(12):
    y=j*4
    if j%2:poly('Mowing band',[(-40,y,-.023),(40,y,-.023),(40,y+4,-.023),(-40,y+4,-.023)],'#39754d')
# Compressed endline width preserves the causal geometry within a portrait frame.
line('Endline',[(-18,0,.009),(12,0,.009)],CREAM,.035)
line('Touchline',[(12,0,.009),(12,45,.009)],CREAM,.035)
line('Penalty box',[(-7,0,.01),(-7,9,.01),(7,9,.01),(7,0,.01)],'#d6dfbe',.027)
line('Six yard box',[(-4,0,.012),(-4,3.8,.012),(4,3.8,.012),(4,0,.012)],CREAM,.026)
line('Corner arc',[(12-.75*math.cos(a),.75*math.sin(a),.012) for a in np.linspace(0,math.pi/2,25)],CREAM,.025)
line('Corner flag pole',[(12,0,0),(12,0,1.9)],CREAM,.026)
flag=poly('Red corner pennant',[(12,0,1.9),(12.65,.03,1.68),(12,.02,1.48)],'#e8474d')
# Goal has one consistent frame and editable mesh net.
line('Goal frame',[(-3,0,0),(-3,0,2.8),(3,0,2.8),(3,0,0)],CREAM,.045)
for x in (-3,3):line('Goal support',[(x,0,2.8),(x,-1.3,2.8),(x,-1.5,0)],'#cdd8c8',.03)
net=[]
for x in np.linspace(-3,3,27):
    pts=[(x,-1.45,0),(x,-1.3,2.8),(x,0,2.8)];net.append((line('Net vertical',pts,'#b0c8b7',.009),pts))
for z in np.linspace(0,2.8,13):
    pts=[(-3,-1.45,z),(0,-1.45,z),(3,-1.45,z)];net.append((line('Net cross',pts,'#a8c2b0',.009),pts))
for x in (-3,3):
    for z in np.linspace(0,2.8,13):line('Net side',[(x,0,z),(x,-1.45,z)],'#acc4b4',.009)
# Original painted panorama on coherent distant stadium walls.
panorama=bpy.data.images.load(str(ROOT/'design/treatment-v003/stadium.png'));panorama.pack()
backmat=bpy.data.materials.new('Painted stadium');backmat.use_nodes=True;n=backmat.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');tex=n.new('ShaderNodeTexImage');tex.image=panorama;backmat.node_tree.links.new(tex.outputs['Color'],em.inputs[0]);backmat.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
for name,vertices in [('Rear terrace',[(-35,-8,0),(35,-8,0),(35,-8,23.333),(-35,-8,23.333)]),('Left terrace',[(-35,48,0),(-35,-8,0),(-35,-8,23.333),(-35,48,23.333)]),('Right terrace',[(35,-8,0),(35,48,0),(35,48,23.333),(35,-8,23.333)]),('Far terrace',[(35,48,0),(-35,48,0),(-35,48,23.333),(35,48,23.333)])]:
    o=mesh(name,vertices,[(0,1,2,3)],backmat);uv=o.data.uv_layers.new()
    for i,xy in enumerate(((0,0),(1,0),(1,1),(0,1))):uv.data[i].uv=xy
poly('Pitchside board',[(-40,-3.4,0),(40,-3.4,0),(40,-3.4,.65),(-40,-3.4,.65)],'#274d5d')
for name,loc,power,size in [('Key',(-8,1,14),2300,10),('Rim',(9,-5,11),2600,8)]:
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((3,2,0))-o.location).to_track_quat('-Z','Y').to_euler()
d=bpy.data.lights.new('Soft stadium fill','SUN');d.energy=1.25;d.angle=.16;o=bpy.data.objects.new('Soft stadium fill',d);s.collection.objects.link(o);o.rotation_euler=(.4,-.5,-.4)
# The generated sheet supplied RGB with a checker pattern. Preserve its pixels; build
# editable silhouette meshes per cell so the checker is outside the actual artwork.
def load_heads(path):
    image=bpy.data.images.load(str(path));image.pack();W,H=image.size
    pixels=np.asarray(image.pixels[:],dtype=np.float32).reshape(H,W,4)
    headmat=bpy.data.materials.new('Original illustrated head art');headmat.use_nodes=True;n=headmat.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');im=n.new('ShaderNodeTexImage');im.image=image;headmat.node_tree.links.new(im.outputs['Color'],em.inputs[0]);headmat.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
    headmeshes=[]
    for row in range(3):
        for col in range(3):
            x0=col*W//3;x1=(col+1)*W//3;y0=(2-row)*H//3;y1=(3-row)*H//3;a=pixels[y0:y1,x0:x1,:3];hh,ww=a.shape[:2]
            if np.min(pixels[:,:,3]) < .5:
                outside=pixels[y0:y1,x0:x1,3] < .35
            else:
                candidate=(a.max(2)-a.min(2)<.13)&(a.mean(2)>.48);outside=np.zeros((hh,ww),bool);queue=deque()
                for x in range(ww):queue.extend(((0,x),(hh-1,x)))
                for y in range(hh):queue.extend(((y,0),(y,ww-1)))
                while queue:
                    y,x=queue.popleft()
                    if not(0<=y<hh and 0<=x<ww) or outside[y,x] or not candidate[y,x]:continue
                    outside[y,x]=True;queue.extend(((y-1,x),(y+1,x),(y,x-1),(y,x+1)))
            inside=~outside
            # Keep the main connected silhouette; discard stray marks in the cell margins.
            seen=np.zeros_like(inside);components=[]
            for yy,xx in zip(*np.where(inside)):
                if seen[yy,xx]:continue
                group=[];queue=deque([(yy,xx)]);seen[yy,xx]=True
                while queue:
                    y,x=queue.popleft();group.append((y,x))
                    for ny,nx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
                        if 0<=ny<hh and 0<=nx<ww and inside[ny,nx] and not seen[ny,nx]:seen[ny,nx]=True;queue.append((ny,nx))
                components.append(group)
            inside[:]=False
            for y,x in max(components,key=len):inside[y,x]=True
            vs=[];faces=[];uvs=[]
            for y in range(hh):
                edges=np.diff(np.r_[False,inside[y],False].astype(np.int8));starts=np.where(edges==1)[0];ends=np.where(edges==-1)[0]
                for xa,xb in zip(starts,ends):
                    i=len(vs);coords=[(xa,y),(xb,y),(xb,y+1),(xa,y+1)];vs.extend([((x/ww-.5)*1.15,(yy/hh-.5)*1.15,0) for x,yy in coords]);faces.append((i,i+1,i+2,i+3));uvs.extend([((x0+x)/W,(y0+yy)/H) for x,yy in coords])
            me=bpy.data.meshes.new(f'Head silhouette {row}-{col}');me.from_pydata(vs,[],faces);me.materials.append(headmat);uv=me.uv_layers.new()
            for p in me.polygons:
                for li in p.loop_indices:uv.data[li].uv=uvs[me.loops[li].vertex_index]
            headmeshes.append(me)
    return headmeshes
headmeshes=load_heads(ROOT/'design/treatment-v003/heads.png')+load_heads(ROOT/'design/treatment-v004/supporting-heads.png')
# Cinematic camera and camera-parented native text overlays.
camd=bpy.data.cameras.new('Directed camera');cam=bpy.data.objects.new('Directed camera',camd);s.collection.objects.link(cam);s.camera=cam;camd.lens=35;camd.sensor_fit='VERTICAL';camd.sensor_height=36;camd.clip_end=250
font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf')
def text(name,body,loc,size,c=CREAM,parent=None):
    d=bpy.data.curves.new(name,'FONT');d.body=body;d.font=font;d.align_x='CENTER';d.align_y='CENTER';d.size=size;d.materials.append(mat(c,True));o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.parent=parent;return o
ui=empty('Screen typography',cam);ui.location=(0,0,-.2);height=4*math.tan(math.radians(2*math.degrees(math.atan(36/70)))/2);ui.scale=(height*.1,height*.1,height*.1)
scorebox=poly('Compact scoreboard',[(-.235,.362,0),(.235,.362,0),(.235,.451,0),(-.235,.451,0)],'#152733',True);scorebox.parent=ui
score_before=text('Score before',"79'   LIV 3 - 0 BAR",(0,.418,.002),.026,parent=ui)
score_after=text('Score after',"LIV 4 - 0 BAR",(0,.418,.002),.028,GOLD,ui)
agg_before=text('Aggregate before','AGGREGATE  3 - 3',(0,.381,.002),.016,parent=ui)
agg_after=text('Aggregate after','AGGREGATE  4 - 3',(0,.381,.002),.016,GOLD,ui)
caption_specs=[('Who','WHO IS READY?',.041),('Nap','CARTOON TIME',.026),('Knees','KNEES: ASLEEP.',.030),('Open','ORIGI HAS SPACE.',.031),('Fast','CORNER TAKEN QUICKLY.',.029),('Goal','ORIGI!',.055),('Replay','SLOW REPLAY',.029),('Title',"BARCELONA WASN'T READY.",.029),('Trent','TRENT WAS.',.049),('Through','LIVERPOOL THROUGH.  4 - 3.',.027)]
captions={name:text(name,body,(0,-.397,.003),size,GOLD if name in ('Goal','Trent') else CREAM,ui) for name,body,size in caption_specs}
captions['Open'].location.y=.29
CAST=json.loads((ROOT/'staging-v005.json').read_text())['cast']
# Native stick puppets: one narrow jersey and four articulated ink limbs per player.
actors={}
for spec in CAST:
    name,row,kit,number=spec['id'],spec['head_row'],spec['kit'],spec['number']
    a={};a['torso']=poly(name+' / Jersey',[(-.24,0,.60),(.24,0,.60),(.18,0,0),(-.18,0,0)],kit,True)
    a['trim']=line(name+' / Jersey outline',[(-.24,-.002,.6),(.24,-.002,.6),(.18,-.002,0),(-.18,-.002,0),(-.24,-.002,.6)],INK,.018,True);a['trim'].parent=a['torso']
    a['number']=text(name+' / Number',number,(0,-.011,.30),.25,parent=a['torso']);a['number'].rotation_euler=(math.pi/2,0,0)
    a['stripes']=[]
    a['neck']=line(name+' / Neck',[(0,0,0)]*2,INK,.033,True)
    a['arms']=[line(name+f' / Arm {i}',[(0,0,0)]*3,INK,.032,True) for i in range(2)]
    a['legs']=[line(name+f' / Leg {i}',[(0,0,0)]*3,INK,.035,True) for i in range(2)]
    a['hands']=[sphere(name+f' / Hand {i}',(0,0,0),(.075,.05,.11),INK,True) for i in range(2)]
    a['boots']=[boot_mesh(name+f' / Boot {i}') for i in range(2)]
    a['socks']=[line(name+f' / Sock {i}',[(0,0,0)]*2,kit,.045) for i in range(2)]
    a['heads']=[]
    for j in range(3):
        o=bpy.data.objects.new(name+f' / Head {j}',headmeshes[row*3+j]);s.collection.objects.link(o);a['heads'].append(o)
    a['row']=row;a['team']=spec['team'];actors[name]=a
C=Vector((11.70,.27,.17));R=Vector((2.0,3.30,.17));N=Vector((-.8,-1.30,1.72))
TR=Vector((12.45,.65,0));OR=Vector((2.55,3.80,0))
ball=sphere('Ball / continuous',C,(.17,.17,.17),'#fbf5df');ball.data.materials.append(mat('#283b45'))
for p in ball.data.polygons:
    if (p.index//20)%3==1 and p.index%5<2:p.material_index=1
bpy.ops.mesh.primitive_cube_add(size=1);pillow=bpy.context.object;pillow.name='Fiction / tiny shoulder pillow';pillow.scale=(.48,.19,.25);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);pillow.data.materials.append(mat('#fff1d7',True));bevel=pillow.modifiers.new('Soft pillow corners','BEVEL');bevel.width=.07;bevel.segments=4
# Sleep puffs and knee eyelids are separate editable gag artwork.
puffs=[sphere('Fiction / sleep puff',(0,0,0),(.03,.03,.03),'#e3e4de',True) for _ in range(3)]
knee_lids=[line('Fiction / sleepy knee eyelid',[(0,0,0)]*5,INK,.016,True) for _ in range(2)]
knee_eyes=[sphere('Fiction / knee eye',(0,0,0),(.14,.04,.09),CREAM,True) for _ in range(2)]
knee_z=text('Fiction / knee zzz','z z z',(0,0,0),.17,CREAM)
def qtime(t):
    if t<2:return t
    if t<9:return 2
    if t<12:return t-7
    if t<15:return 5
    if t<24:return t-10
    if t<31:return 5+(t-24)*.75
    return t-17

def shoot_ball(q):
    if q<=6.75:return C.copy()
    if q<=8:
        u=(q-6.75)/1.25;p=C.lerp(R,u);p.z+=.22*math.sin(math.pi*u);return p
    if q<=8.625:
        u=(q-8)/.625;p=R.lerp(N,u);p.z+=.35*math.sin(math.pi*u);return p
    u=ease((q-8.625)/1);return N.lerp(Vector((-.9,-1.08,.17)),u)

def cam_at(t):
    if t<2:return (14.5,4.4,1.7),(11.85,.4,.80)
    if t<4:return (8.4,9.5,3.0),(5.7,5.5,1.45)
    if t<6:return (-.5,5.0,1.4),(-1.8,3.9,.65)
    if t<9:return (20,-2,15),(5,2.5,1)
    if t<12:return (16,6.8,3.1),(12.7,1.3,1.2)
    if t<14:return (15.7,.1,3.6),(4.5,3.0,1.3)
    if t<15:return (15.7,4.1,3.0),(13.35,.65,2.0)
    if t<16.4:return (14.7,3.4,1.4),(11.9,.5,.52)
    if t<20:return (20,-2,15),(5,2.5,1)
    if t<22:return (4.8,5.8,2.8),(2.7,3.8,1.25)
    if t<24:return (8.4,9.5,3.0),(5.7,5.5,1.45)
    if t<31:return (20,-2,15),(5,2.5,1)
    return (8.8,12,3.6),(3.8,4.0,1.3)

def set_puppet(name,pos,mode,pt,focus,f,walk=None,kick=None,tilt=0):
    a=actors[name];pos=Vector(pos);right=Vector((math.cos(cam.rotation_euler.z),math.sin(cam.rotation_euler.z),0));right.normalize()
    # Camera's horizontal direction projected onto the ground keeps thin jerseys legible.
    right=cam.rotation_euler.to_quaternion()@Vector((1,0,0));right.z=0;right.normalize();forward=Vector((-right.y,right.x,0));up=Vector((0,0,1))
    hip=pos+up*(.97+.017*math.sin(pt*3));feet=[pos+right*(-.17 if i==0 else .17)+up*.085 for i in range(2)]
    hands=[hip+right*(-.48 if i==0 else .48)+up*.20 for i in range(2)]
    if mode in ('organise','legs-sleep'):hands[1]=hip+right*.67+up*.62
    if mode=='celebrate':hands=[hip+right*(-.66 if i==0 else .66)+up*(1.05+.05*math.sin(pt*4+i)) for i in range(2)];hip.z+=.035*math.sin(pt*4)
    if mode=='shock':hands=[hip+right*(-.51 if i==0 else .51)+up*.94 for i in range(2)]
    if walk:
        direction,distance=walk;phase=distance%1;hip.z+=.035*math.cos(phase*math.tau*2)
        for i in range(2):
            u=(phase+i*.5)%1
            if u<.5:off=.25-u;lift=0
            else:v=(u-.5)*2;off=-.25+.5*ease(v);lift=.24*math.sin(math.pi*v)
            feet[i]+=direction*off+up*lift;hands[i]+=direction*(.23*math.sin(phase*math.tau+i*math.pi))
    direction=None
    if kick:
        contact,relative,direction=kick;strike=Vector(contact)-direction*.41
        rest=feet[1].copy();back=pos-direction*.42+up*.43;end=rest
        if relative<-.38:feet[1]=rest.lerp(back,ease((relative+.60)/.22))
        elif relative<0:feet[1]=back.lerp(strike,ease((relative+.38)/.38))
        elif relative<.24:feet[1]=strike.lerp(strike+direction*.50+up*.58,ease(relative/.24))
        else:feet[1]=(strike+direction*.50+up*.58).lerp(end,ease((relative-.24)/.6))
        hip+=direction*(.12*ease((relative+.5)/.5));hands=[hip+right*(-.58 if i==0 else .58)+up*(.70 if i==0 else .63) for i in range(2)]
    if mode=='sleep':hip+=right*.10;hip.z-=.04;hands=[hip+right*(-.31 if i==0 else .31)-up*.11 for i in range(2)]
    if mode=='legs-sleep':hip.z-=.16*ease((pt-4)/1.3)
    if name=='Keeper' and 8.10<pt<9.65:
        amt=ease((pt-8.1)/.4)*(1-ease((pt-9.0)/.65));hip+=Vector((-.9*amt,0,-.25*amt));hands=[hip+Vector((-.65,-.1,.7)),hip+Vector((-.4,-.3,1.1))]
    shoulders=[hip+up*.57+right*(-.21 if i==0 else .21) for i in range(2)]
    headpos=hip+up*1.02+right*tilt
    torso=a['torso'];torso.location=hip;torso.rotation_euler=(0,0,math.atan2(right.y,right.x));key(torso,f)
    update_line(a['neck'],[hip+up*.60,headpos-up*.30],f)
    for i in range(2):
        h=hands[i];elbow=(shoulders[i]+h)*.5+right*(-.075 if i==0 else .075)-up*.075
        update_line(a['arms'][i],[shoulders[i],elbow,h],f);a['hands'][i].location=h;key(a['hands'][i],f)
        v=feet[i]-hip;mid=(hip+feet[i])*.5;axis=(direction if direction is not None else forward).copy();axis-=v*(axis.dot(v)/max(v.length_squared,.01));axis.normalize();bend=math.sqrt(max(0,.67**2-v.length_squared/4))
        knee=mid+axis*bend*.65
        update_line(a['legs'][i],[hip+right*(-.09 if i==0 else .09),knee,feet[i]],f)
        boot=a['boots'][i];boot.location=feet[i];boot.rotation_euler=(0,0,math.atan2(-direction.x,direction.y) if direction is not None else math.atan2(-forward.x,forward.y));key(boot,f)
        sockend=feet[i].lerp(knee,.31);update_line(a['socks'][i],[feet[i]+up*.06,sockend],f)
        if name=='Defender A':
            facing=(cam.location-knee).normalized();knee_eyes[i].location=knee+facing*.055;knee_eyes[i].rotation_euler=(0,0,math.atan2(right.y,right.x));key(knee_eyes[i],f)
            eyelid=knee+facing*.12;pts=[eyelid+right*((j-2)*.048)+up*(.012*(j-2)**2-.033) for j in range(5)];update_line(knee_lids[i],pts,f)
            if i==1:knee_z.location=knee+right*.30+up*(.15+.03*math.sin(pt*4));knee_z.rotation_euler=cam.rotation_euler.copy();key(knee_z,f)
    # Graphic heads are editable silhouette geometry with camera-facing expression replacements.
    target=Vector(focus);look_sign=-1 if (target-headpos).dot(right)>0 else 1
    state=2 if mode in ('celebrate','shock') else 1 if mode=='sleep' or kick or mode=='notice' else 0
    if a['row']>=2 and mode=='notice':state=0
    for j,o in enumerate(a['heads']):
        o.location=headpos;o.rotation_euler=cam.rotation_euler.copy();o.rotation_euler.rotate_axis('Z',-.34 if mode=='sleep' else tilt*.3);o.scale=(look_sign,1,1);key(o,f);show(o,j==state,f)
    return headpos,feet,hip

# Export shot-local event names, shared by native markers and pipeline/audio.py.
shots=[{'id':'opening','start_frame':1,'events':{'start':0,'freeze':48}}, {'id':'gags','start_frame':49,'events':{'head_sleep':0,'knee_sleep':48,'back_to_match':96}}, {'id':'read','start_frame':145,'events':{'wide':0,'walk':72,'notice':144,'eye':192}}, {'id':'play','start_frame':361,'events':{'pivot':0,'corner_contact':42,'origi_contact':72,'net_contact':87,'cheer':90}}, {'id':'celebrate','start_frame':481,'events':{'start':0,'wake':48}}, {'id':'replay','start_frame':577,'events':{'start':0,'corner_contact':56,'origi_contact':96,'net_contact':116}}, {'id':'payoff','start_frame':745,'events':{'title':0,'trent':48,'through':96,'fade':156}}]
for sh in shots:
    for ev,n in sh['events'].items():s.timeline_markers.new(sh['id']+'/'+ev,frame=sh['start_frame']+n)
plan_path=ROOT/'production.json'
# The selected mix is already versioned; this polish preserves its event timing.
plan=json.loads(plan_path.read_text())
assert plan['shots']==shots, 'Polish unexpectedly changed audio event timing'
plan.update(revision='film-v004',staging='staging-v005.json',script='script-v005.md',review_status='User delegated remaining reviews for this film; producer review in progress')
plan_path.write_text(json.dumps(plan,indent=2)+'\n')
(OUT/'production.json').write_text(json.dumps(plan,indent=2)+'\n')
for f in range(1,FRAMES+1):
    t=(f-1)/24;q=qtime(t);cl,ct=cam_at(t);cam.location=cl;cam.rotation_euler=(Vector(ct)-cam.location).to_track_quat('-Z','Y').to_euler();key(cam,f)
    tr=TR.copy();walk=None;mode='watch';kick=None
    if 2<q<5:
        tr.x+=.3*(q-2);walk=(Vector((1,0,0)),.3*(q-2))
    elif 5<=q<5.6:tr.x+=.9;mode='notice'
    elif 5.6<=q<6.15:
        d=.9*ease((q-5.6)/.55);tr.x+=.9-d;walk=(Vector((-1,0,0)),d)
    elif 6.15<=q<8.2:
        dr=R-C;dr.z=0;dr.normalize();kick=(C,q-6.75,dr)
    elif q>=9.7:
        u=min(1,(q-9.7)/4.3);goal=OR+Vector((1.2,.35,0));tr=TR.lerp(goal,u);delta=goal-TR;walk=(delta.normalized(),delta.length*u) if u<1 else None;mode='watch' if u<1 else 'celebrate'
    set_puppet('Trent',tr,mode,q,R,f,walk,kick)
    dr=N-R;dr.z=0;dr.normalize();kick=(R,q-8,dr) if 7.4<=q<9.3 else None
    set_puppet('Origi',OR,'celebrate' if q>9.3 else 'watch',q,C if q<8 else N,f,kick=kick)
    sh0=Vector((10,5.6,0));sh1=Vector((12.1,2.0,0));u=ease((q-2)/4);sp=sh0.lerp(sh1,u);delta=sh1-sh0
    set_puppet('Shaqiri',sp,'celebrate' if q>9.3 else 'watch',q,C,f,(delta.normalized(),delta.length*u) if 2<q<6 else None)
    for name,pos in [('Defender A',(-1.8,3.9,0)),('Defender B',(4.4,7.3,0)),('Defender C',(5.7,5.5,0))]:
        mode='organise' if q<7.1 else 'watch' if q<8.9 else 'shock'
        if 2<=t<4 and name=='Defender C':mode='sleep'
        if 4<=t<6 and name=='Defender A':mode='legs-sleep'
        hp,feet,hip=set_puppet(name,pos,mode,t if 2<=t<6 else q,(10,6,2) if q<7.1 else R,f,tilt=.1 if mode=='sleep' else 0)
        if name=='Defender C':
            pillow.location=hp+(cam.rotation_euler.to_quaternion()@Vector((.20,.0,0)))+Vector((0,0,-.47));pillow.rotation_euler=(0,.2,.2);key(pillow,f)
            for i,p in enumerate(puffs):
                phase=(t*.8+i*.28)%1;p.location=hp+Vector((-.25-.25*phase,.0,.05+.45*phase));p.scale=(.03+.06*phase,)*3;key(p,f)
    for i,spec in enumerate(CAST[7:]):
        name=spec['id'];is_red=spec['team']=='Liverpool'
        mode=('celebrate' if is_red else 'shock') if q>9.3 else ('watch' if is_red or q>7.1 else 'organise')
        position=Vector(spec['position'])
        # Distinct held attention and breathing phases keep the supporting group alive.
        focus=Vector(spec['position'])+Vector((1.0,-1.0,1.8)) if q<7.1 else R
        set_puppet(name,position,mode,q+i*.39,focus,f)
    set_puppet('Keeper',(0,-.2,0),'watch' if q<8.7 else 'shock',q,R,f)
    ball.location=shoot_ball(q);ball.rotation_euler=(q*2,q*7,q*3);key(ball,f)
    for o,pts in net:
        dt=q-8.625;wig=.13*math.sin(dt*24)*math.exp(-dt*3) if 0<dt<1.5 else 0
        update_line(o,[Vector(p)+Vector((0,-wig,0)) for p in pts],f)
    show(pillow,2<=t<4,f)
    for o in puffs:show(o,2<=t<4 or 22<=t<23,f)
    for o in knee_lids+knee_eyes+[knee_z]:show(o,4<=t<6,f)
    scored=q>=8.625
    for o in (score_before,agg_before):show(o,scored is False and t>=6,f)
    for o in (score_after,agg_after):show(o,scored and t>=6,f)
    show(scorebox,t>=6,f)
    wanted='Who' if t<2 else 'Nap' if t<4 else 'Knees' if t<6 else 'Open' if 12<=t<14 else 'Fast' if 16.4<=t<18 else 'Goal' if 18.625<=t<22 else 'Replay' if 24<=t<31 else 'Title' if 31<=t<33 else 'Trent' if 33<=t<35 else 'Through' if t>=35 else None
    for name,o in captions.items():show(o,name==wanted,f)
    if f%144==0:print('ADVANCED_BAKE',f,flush=True)
for action in bpy.data.actions:
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path.startswith('hide_') else 'LINEAR'
s.frame_set(421);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'trent-corner-advanced.blend'))
(OUT/'build-checks.json').write_text(json.dumps({'blender':bpy.app.version_string,'frames':FRAMES,'fps':24,'seconds':38,'construction':'Thin native 3D ink limbs and narrow jerseys; textured editable silhouette heads; shared 3D field','contact_centers':{'corner':list(C),'receiver':list(R),'net':list(N)},'cast':CAST,'head_assets':['design/treatment-v003/heads.png','design/treatment-v004/supporting-heads.png'],'head_background':'Original RGB pixels retained; native silhouette geometry excludes checker background.'},indent=2)+'\n')
if '--samples' in sys.argv:
    s.render.resolution_percentage=50
    for t in (3,5,7.5,12.5,16.75,18,18.625,34):
        s.frame_set(round(t*24)+1);s.render.filepath=str(OUT/f'stills/pose-{round(t*24)+1:04}.png');bpy.ops.render.render(write_still=True)
print('ADVANCED_BUILD_COMPLETE',flush=True)
