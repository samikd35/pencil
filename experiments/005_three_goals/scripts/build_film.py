"""Thirty seconds of authored acting. New faces/jerseys on proven editable limb controls."""
from pathlib import Path
import ast, bpy, math, json, sys, hashlib, time, random
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v001'
OUT.mkdir(parents=True,exist_ok=True);(OUT/'stills').mkdir(exist_ok=True)
SOURCE=ROOT.parent/'001_heavy_box/artifacts/finish-v002/character-and-effects.blend'
HELPERS=ROOT.parent/'003_alisson_winner/scripts/build_film.py'
FPS=24;SECONDS=30;FRAMES=720
INK='#101b31';PAPER='#fff3d8';GOLD='#efc979';RED='#d64c61';GREEN='#87cf74';BLACK=INK
MATS={};GROUPS={};actors={}
names={'clamp','ease','mix','vec','track','rgba','mat','add','poly','line','rect','oval','label','disk','empty','visible','key','character','pose','joint','set_actor'}
nodes=[n for n in ast.parse(HELPERS.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names]
assert len(nodes)==len(names)
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(HELPERS),'exec'),globals())
base_pose=pose;base_set=set_actor
scene=bpy.data.scenes.new('Three Goals. One Heartbreak.');bpy.context.window.scene=scene
art=bpy.data.collections.new('Lusail - original illustration');scene.collection.children.link(art)
scene.render.engine='BLENDER_EEVEE';scene.eevee.taa_render_samples=24
scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.render.resolution_percentage=100
scene.render.fps=FPS;scene.frame_start=1;scene.frame_end=FRAMES
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.compression=15
scene.render.use_compositing=False;scene.render.use_sequencer=False
scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
scene.world=bpy.data.worlds.new('Night');scene.world.color=(.005,.01,.025)
camdata=bpy.data.cameras.new('Directed camera');camera=bpy.data.objects.new('Directed camera',camdata);art.objects.link(camera)
camdata.type='ORTHO';camdata.sensor_fit='VERTICAL';camdata.ortho_scale=12;camdata.clip_end=250
camera.location=(0,0,90);scene.camera=camera
font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf');regular=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial.ttf')

# Night stadium: gold lattice, dense stands, banks of white lights and layered green pitch.
rect('Night sky',-80,-30,160,70,'#10172e',-30)
rect('Upper bowl',-60,1.6,120,10,'#222e45',-29)
for i in range(35):
    x=-50+i*3
    line('Lusail roof lattice',[(x,7.2),(x+2,8.3),(x+4,7.2)],'#856a47',.035,-28)
line('Roof gold rim',[(-60,7.18),(60,7.18)],'#b29767',.10,-27)
rng=random.Random(20221218)
for r in range(12):
    y=1.9+r*.41;line('Terrace edge',[(-55,y),(55,y)],'#39495d',.03,-26)
    verts=[];faces=[]
    for i in range(260):
        x=-55+i*.43+(r%2)*.18;n=len(verts);h=rng.uniform(.10,.23)
        verts.extend([(x,y,-25),(x+.16,y,-25),(x+.16,y+h,-25),(x+.04,y+h+.04,-25)])
        faces.append((n,n+1,n+2,n+3))
        n=len(verts);verts.extend([(x+.09+.047*math.cos(k*math.tau/8),y+h+.075+.05*math.sin(k*math.tau/8),-24.99) for k in range(8)]);faces.append(tuple(range(n,n+8)))
    me=bpy.data.meshes.new('Spectators');me.from_pydata(verts,[],faces)
    for c in ('#7f9aa3','#c5c4b0','#5484a5','#5d7084'):me.materials.append(mat(c))
    for p in me.polygons:p.material_index=rng.randrange(4)
    add(bpy.data.objects.new('Packed terrace',me))
for x in (-8,-3,3,8):
    rect('Lightbank housing',x-.9,6.55,1.8,.32,'#73858c',-24)
    for i in range(8):disk('Floodlight',x-.77+i*.22,6.73,.068,PAPER,-23)
rect('Pitchside maroon boards',-60,1.35,120,.4,'#502337',-22)
for x in range(-50,55,5):label('Venue lettering','LUSAIL  /  2022',x,1.54,.14,'#c6a88f',-21)
rect('Night pitch',-65,-50,130,51.35,'#286152',-20)
for i in range(22):rect('Mowing band',-65,-47+i*2.2,130,.95,'#2b6956',-19)
line('Touchline',[(-60,1.3),(60,1.3)],'#acc8b0',.035,-18)
for i in range(70):
    x=-12+rng.random()*24;y=-6+rng.random()*7
    line('Grass blade',[(x,y),(x+.05,y+.04),(x+.1,y)],'#3a785c',.012,-17)

# One goal assembly, intentionally condensed perspective, with animated net response.
net=[];gx=.20;gy=-1.46;gw=2.40;gh=2.13
poly('Goal dark interior',[(gx,gy),(gx+gw,gy),(gx+gw+.30,gy+gh+.23),(gx+.30,gy+gh+.23)],'#193c3a',-12,'goal')
for j in range(17):
    x=gx+j*gw/16;pts=[(x,gy),(x+.3,gy+gh+.23)]
    ob=line('Net vertical',pts,'#779c8e',.012,-11,'goal');net.append((ob,pts))
for j in range(12):
    y=gy+j*gh/11;pts=[(gx,y),(gx+gw+.30,y+.23)]
    ob=line('Net horizontal',pts,'#779c8e',.012,-10.9,'goal');net.append((ob,pts))
line('Goal frame',[(gx,gy),(gx,gy+gh),(gx+gw,gy+gh),(gx+gw,gy)],PAPER,.064,-10,'goal')
line('Goal depth',[(gx,gy+gh),(gx+.30,gy+gh+.23),(gx+gw+.30,gy+gh+.23),(gx+gw,gy+gh)],'#adbcaf',.04,-10.1,'goal')
line('Penalty box',[(gx-.5,gy),(gx-1.7,gy-1.35),(gx+gw-.25,gy-1.35),(gx+gw+.4,gy)],'#8fb098',.025,-14,'goal')
disk('Penalty spot',-.45,-2.85,.075,PAPER,-13,'spot')

# Only the simple endpoint controls and limb mechanics are reused. Identity art is new.
keep={'Bean torso','Head','Head_outline','Eye_0','Eye_1','Brow_0','Brow_1','Mouth','Mouth open','CTRL_Body','CTRL_Head','ANCHOR_Shoulder'}
for side in ('far','near'):
    keep.update(f'{p}_{side}' for p in ('Mitten','Shoe','Arm','Leg'))
    keep.update(f'{p}_{side}_outline' for p in ('Mitten','Shoe'))
    keep.update(f'CTRL_{p}_{side}' for p in ('Hand','Foot','Elbow','Knee'))
with bpy.data.libraries.load(str(SOURCE),link=False) as (src,dst):
    assert keep.issubset(src.objects);dst.objects=list(keep)
template={o.name:o for o in dst.objects}

def replace_mesh(ob,pts,color,z):
    me=bpy.data.meshes.new(ob.name+' revised silhouette');me.from_pydata([(*p,z) for p in pts],[],[list(range(len(pts)))]);me.materials.append(mat(color));ob.data=me;ob.scale=(1,1,1)

def curve_points(ob,pts,z=.56):
    spl=ob.data.splines[0]
    if len(spl.points)!=len(pts):
        ob.data.splines.clear();spl=ob.data.splines.new('POLY');spl.points.add(len(pts)-1)
    for p,xy in zip(spl.points,pts):p.co=(*xy,z,1)

cast=[('Mbappe','#14264b','10','#a96948','crop'),('Thuram','#14264b','26','#8f5a42','crop'),('Kolo Muani','#14264b','12','#81503a','crop'),('Messi','#edf0df','10','#d79b77','beard'),('Montiel','#edf0df','4','#c28b69','sweep'),('Argentina teammate','#edf0df','7','#c58d6b','sweep'),('Martinez','#83bd58','23','#d09873','sweep'),('Lloris','#e9bf58','1','#c99b7b','beard')]
for name,col,num,skin,hair in cast:
    a=character(name,col,num);m=a['m'];head=m['CTRL_Head'];body=m['CTRL_Body'];extra=[]
    dark={'#a96948':'#754632','#8f5a42':'#643b30','#81503a':'#5d382e'}.get(skin,'#a97056')
    face=[(-.48,.31),(-.41,.52),(-.20,.64),(.18,.64),(.43,.48),(.52,.20),(.48,-.25),(.27,-.48),(.03,-.56),(-.25,-.50),(-.44,-.31)]
    face=[r for p,q in zip(face,face[1:]+face[:1]) for r in (vec(p,q,.25),vec(p,q,.75))]
    replace_mesh(m['Head'],face,skin,.37);curve_points(m['Head_outline'],face+[face[0]],.39);m['Head_outline'].data.bevel_depth=.021
    def p(n,pts,c,z=.48,par=head):
        ob=poly(name+' / '+n,pts,c,z,parent=par);extra.append(ob);return ob
    def l(n,pts,c=INK,w=.025,z=.55,par=head):
        ob=line(name+' / '+n,pts,c,w,z,parent=par);extra.append(ob);return ob
    p('Face shadow',[(-.46,.27),(-.30,.32),(-.28,-.24),(-.04,-.53),(-.24,-.47),(-.41,-.28)],dark,.40)
    for x in (-.49,.50):
        p('Ear',oval(x,-.04,.10,.17,20),skin,.38);l('Ear fold',[(x-.025,.02),(x+.025,-.04),(x,-.12)],dark,.021,.45)
    if hair=='crop':
        p('Close cropped hair',[(-.48,.29),(-.44,.48),(-.25,.65),(.16,.68),(.41,.54),(.50,.30),(.39,.39),(.23,.44),(-.20,.43),(-.38,.34)],'#24262b',.48)
        for i in range(19):
            x=-.34+(i%7)*.105;y=.46+(i//7)*.055
            l('Hair grain',[(x,y),(x+.018,y+.023)],'#424039',.012,.50)
        l('Hairline', [(-.37,.35),(-.21,.43),(.25,.44),(.40,.36)],INK,.027)
    else:
        p('Swept hair',[(-.50,.19),(-.53,.47),(-.34,.63),(-.49,.69),(-.05,.77),(.24,.73),(.46,.56),(.49,.30),(.29,.40),(.12,.53),(-.12,.42),(-.36,.36)],'#382f2b',.49)
        l('Hair part',[(-.25,.48),(.02,.60),(.24,.61)],'#655040',.022)
    if hair=='beard':
        p('Beard',[(-.45,-.16),(-.32,-.33),(-.17,-.27),(.13,-.28),(.33,-.16),(.46,-.20),(.34,-.50),(.04,-.64),(-.24,-.54),(-.42,-.33)],'#45332b',.49)
        for i in range(6):l('Beard strand',[(-.21+i*.10,-.43),(-.19+i*.10,-.51)],'#73523c',.014)
    # Small almond eyes, pupils and brows provide focus rather than the original dot face.
    a['whites']=[];a['sweat']=[];a['fingers']=[]
    for i,x in enumerate((-.21,.22)):
        a['whites'].append(p('Eye white',[(x-.115,.085),(x-.075,.13),(x+.065,.125),(x+.11,.075),(x+.03,.032),(x-.06,.04)],'#e9d8c2',.52))
        m['Eye_'+str(i)].location=(0,0,0);replace_mesh(m['Eye_'+str(i)],oval(x+.025,.083,.042,.056,20),INK,.55)
        curve_points(m['Brow_'+str(i)],[(x-.12,.23),(x-.02,.25),(x+.12,.22)],.56);m['Brow_'+str(i)].data.bevel_depth=.023
        drop=p('Sweat',[(x+.24,-.02),(x+.208,-.13),(x+.228,-.17),(x+.252,-.14)],'#d7c7a4',.60);a['sweat'].append(drop)
    l('Nose bridge',[(.025,.06),(.01,-.09),(.075,-.14)],dark,.024)
    l('Nose base',[(-.02,-.17),(.08,-.19),(.18,-.16)],'#663f32' if hair=='crop' else dark,.026)
    l('Lower lip',[(-.055,-.37),(.11,-.39),(.22,-.355)],dark,.026)
    for n in ('Mouth','Mouth focused'):curve_points(m[n],[(-.11,-.30),(.07,-.31),(.23,-.31)],.59);m[n].data.bevel_depth=.020
    replace_mesh(m['Mouth open'],oval(.07,-.32,.14,.095),INK,.58)
    # New angular jersey silhouette, collar, sleeves, number and shorts.
    jersey=[(-.30,.06),(-.33,.55),(-.47,.63),(-.37,.86),(-.18,.94),(.18,.94),(.37,.86),(.47,.63),(.33,.55),(.30,.06)]
    replace_mesh(m['Bean torso'],jersey,col,.22)
    p('Neck',[(-.11,.81),(-.12,1.0),(.13,1.0),(.12,.81)],skin,.21,body)
    if col=='#edf0df':
        for x in (-.22,.04):p('Argentina stripe',[(x,.15),(x+.13,.15),(x+.13,.88),(x,.91)],'#6ab0ce',.24,body)
    else:
        p('Shirt side shade',[(-.30,.06),(-.33,.55),(-.20,.71),(-.16,.1)],'#10213c' if col=='#14264b' else '#6f994d' if name=='Martinez' else '#b89845',.235,body)
    l('Collar',[(-.17,.91),(0,.80),(.17,.91)],GOLD if col=='#14264b' else INK,.036,.26,body)
    p('Shorts',[(-.32,.16),(.32,.16),(.34,-.12),(.05,-.14),(0,-.02),(-.05,-.14),(-.33,-.12)],col,.27,body)
    a['number'].location=(0,.43,.30);a['number'].data.size=.34;a['number'].data.materials[0]=mat(GOLD if col=='#14264b' else INK)
    p('Chest badge',[(.19,.67),(.28,.67),(.28,.77),(.19,.77)],GOLD if col=='#14264b' else '#d2b46b',.27,body)
    for side in ('far','near'):
        anchor=empty(name+' / Shoulder '+side);anchor.parent=body;anchor.location=((-1 if side=='far' else 1)*.31,.76,0);extra.append(anchor)
        for fc in m['Arm_'+side].data.animation_data.drivers:
            for variable in fc.driver.variables:
                for target in variable.targets:
                    if target.id==m['ANCHOR_Shoulder']:target.id=anchor
        m['Mitten_'+side].data.materials[0]=mat(skin if name not in ('Martinez','Lloris') else '#e9e6cb')
        m['Shoe_'+side].data.materials[0]=mat('#ed976d' if col=='#14264b' else '#e6d68e')
        for j in range(3):
            ob=l('Finger '+side+str(j),[(.025+j*.035,-.025),(.025+j*.035,-.10)],dark,.012,.37,m['CTRL_Hand_'+side]);a['fingers'].append(ob)
    a['all']+=extra
    a['skin']=skin

def blend_pose(a,b,u):
    u=ease(u);p={}
    for k,v in a.items():
        if k in ('hands','feet'):p[k]=[vec(x,y,u) for x,y in zip(v,b[k])]
        elif isinstance(v,tuple):p[k]=vec(v,b[k],u)
        else:p[k]=mix(v,b[k],u)
    return p

def pose(mode,t=0):
    p=base_pose('ready',t)
    if mode in ('kick','run','celebrate','keeper','watch'):return base_pose(mode,t)
    if mode=='resolve':
        p.update(hip=(0,1.70+.018*math.sin(t*3.2)),tilt=-.025,headtilt=-.035,hands=[(-.51,1.11,0),(.51,1.14,0)],focus=.9)
    elif mode=='exhausted':
        p.update(hip=(0,1.56+.04*math.sin(t*5)),tilt=-.16,headtilt=-.10,hands=[(-.46,1.02,0),(.50,1.05,0)],focus=.75)
    elif mode=='rise':
        p.update(hip=(-.04,1.20),tilt=-.57,headtilt=-.37,hands=[(-.45,.88,0),(.50,.85,0)],focus=.60)
        p=blend_pose(p,pose('exhausted',t),clamp((t-.35)/.95))
    elif mode=='urgent':
        p.update(hip=(0,1.66),tilt=.12,headtilt=.08,hands=[(-.5,1.45,.2),(1.02,2.14,-.4)],focus=.90)
        p['hands'][1]=(1.03-.30*math.sin(t*9),2.10+.08*math.sin(t*9),-.5)
    elif mode=='volley':
        p.update(hip=track(t,[(-1,-.35,1.65),(-.35,-.12,1.42),(0,.1,1.73),(.25,.19,1.65),(.7,.35,1.48),(1.3,.4,1.72)]),tilt=track(t,[(-1,.10),(-.3,.28),(0,.16),(.3,-.42),(.9,-.08)])[0],headtilt=-.08,focus=.9)
        p['feet']=[track(t,[(-1,-.35,.12,0),(-.3,-.24,.12,0),(0,-.36,.20,.12),(.3,-.33,.25,.14),(.70,.10,.12,0)]),track(t,[(-1,.35,.12,0),(-.4,-.6,.65,.65),(0,1.1,.83,-.12),(.2,1.20,1.30,-.4),(.65,.85,.22,0),(1.2,.88,.12,0)])]
        p['hands']=[(-.95,2.15,.4),(.64,2.61,-.5)]
    elif mode=='broken':
        p.update(hip=(0,1.67-.08*ease(t/2)),tilt=-.02-.13*ease(t/2),headtilt=-.32*ease(t/1.8),hands=[(-.49,1.12,0),(.52,1.09,0)],focus=.30,joy=0)
    elif mode=='lift':
        p=base_pose('celebrate',t);p['hands']=[(-.31,3.22,.2),(.31,3.22,-.2)];p['focus']=0;p['joy']=1
    return p

used=set()
def act(name,x,y,s,mode,pt,f,d=1,depth=0,roll=0,jump=0):
    a=actors[name];used.add(name)
    result=base_set(name,x,y,s,d,mode,pt,f,jump,depth)
    p=pose(mode,pt);ang=p['tilt']
    for i,side in enumerate(('far','near')):
        ax=(-1 if i==0 else 1)*.31
        sh=(p['hip'][0]+ax*math.cos(ang)-.76*math.sin(ang),p['hip'][1]+ax*math.sin(ang)+.76*math.cos(ang))
        hand=p['hands'][i]
        elbow=(min(sh[0],hand[0])-.11 if i==0 else max(sh[0],hand[0])+.11,(sh[1]+hand[1])*.5)
        ob=a['m']['CTRL_Elbow_'+side];ob.location=(x+d*s*elbow[0],y+s*elbow[1]+jump,depth);key(ob,f)
    # Entire puppet rotates around its hip for saves, preserving connected geometry.
    if roll:
        pivot=(x,y+s*1.45)
        for n,ob in a['m'].items():
            if n.startswith('CTRL_') and not ob.parent:
                dx,dy=ob.location.x-pivot[0],ob.location.y-pivot[1]
                ob.location.x=pivot[0]+dx*math.cos(roll)-dy*math.sin(roll);ob.location.y=pivot[1]+dx*math.sin(roll)+dy*math.cos(roll);ob.rotation_euler.z+=roll;key(ob,f)
    for i,ob in enumerate(a['whites']):
        blink=max(0,1-abs((pt+len(name)*.23)%3.4-3.12)/.095)
        focus=pose(mode,pt)['focus'];ob.scale.y=(1-.45*focus)*(1-.82*blink);ob.keyframe_insert(data_path='scale',frame=f)
    for side in ('far','near'):
        for kind in ('Arm','Leg'):
            ob=a['m'][kind+'_'+side];ob.data.bevel_depth=.036*s;ob.data.keyframe_insert(data_path='bevel_depth',frame=f)
    for i in range(2):
        ob=a['m']['Brow_'+str(i)];ob.rotation_euler.z=(-.14 if i==0 else .14)*pose(mode,pt)['focus'];ob.keyframe_insert(data_path='rotation_euler',frame=f)
        ob=a['m']['Eye_'+str(i)];ob.location.y=-.045*ease(pt/1.5) if mode=='broken' else 0;ob.keyframe_insert(data_path='location',frame=f)
    for n in ('Mouth','Mouth focused'):
        ob=a['m'][n]
        for i,p in enumerate(ob.data.splines[0].points):
            p.co.y=(-.35 if i!=1 else -.30) if mode=='broken' else -.31
            p.keyframe_insert(data_path='co',frame=f)
    if mode=='broken':
        for i in range(2):
            ob=a['m']['Brow_'+str(i)];ob.rotation_euler.z=(.22 if i==0 else -.22)*ease(pt/1.5);ob.keyframe_insert(data_path='rotation_euler',frame=f)
        for ob in a['fingers']:ob.scale.y=1+.75*ease(pt/1.5);ob.keyframe_insert(data_path='scale',frame=f)
    return result

# World ball and contact rays. Children move as a coherent object, never detached panels.
ball=empty('Continuous match ball');disk('Ball',0,0,.16,PAPER,5,parent=ball)
line('Ball outline',oval(0,0,.16,.16),INK,.021,5.01,parent=ball,closed=True)
poly('Ball gold panel',[(.062*math.cos(i*math.tau/5),.062*math.sin(i*math.tau/5)) for i in range(5)],'#b5a079',5.02,parent=ball)
for i in range(5):
    a=i*math.tau/5;line('Ball panel',[(.055*math.cos(a),.055*math.sin(a)),(.157*math.cos(a),.157*math.sin(a))],INK,.012,5.03,parent=ball)
ballitems=[ball]+list(ball.children)
trail=[disk('Moving ball streak',0,0,.11*(1-i*.12),['#d5cca2','#b3b995','#8ca988','#659777'][i],4.9) for i in range(4)]
impact=empty('Kick accent');rays=[]
for i in range(7):
    a=i*math.tau/7;rays.append(line('Kick ray',[(.22*math.cos(a),.22*math.sin(a)),(.39*math.cos(a),.39*math.sin(a))],GOLD,.026,5.2,parent=impact))

# Trophy held by both hands, and a restrained black/gold presentation robe.
trophy=empty('World Cup trophy');tro=[]
def tp(n,pts,c,z=.6):ob=poly(n,pts,c,z,parent=trophy);tro.append(ob);return ob
tp('Trophy base',[(-.23,0),(.23,0),(.19,.16),(-.19,.16)],'#bd8c3f')
tp('Green base band',[(-.22,.04),(.22,.04),(.21,.085),(-.21,.085)],'#488f65',.62)
tp('Trophy rising figures',[(-.18,.14),(.17,.14),(.11,.49),(.24,.79),(.1,.92),(-.05,.69),(-.22,.84),(-.29,.72),(-.11,.47)],'#e3b34d',.63)
tp('Globe',oval(0,.95,.30,.31),'#e6bc56',.64)
tp('Globe light',oval(-.08,1.04,.17,.16),'#ffe2a0',.65)
tp('Globe land',[(-.21,1.09),(-.06,1.17),(.05,1.11),(.01,.98),(.17,.87),(.12,.73),(-.05,.82),(-.09,.97)],'#b6893d',.66)
robe=poly('Messi presentation bisht',[(-.48,.02),(-.49,.77),(-.20,.95),(0,.72),(.20,.95),(.49,.77),(.48,.02)],'#242b31',.285,parent=actors['Messi']['m']['CTRL_Body'])
robelines=[line('Bisht gold edge',[(-.20,.95),(0,.72),(0,.04)],GOLD,.035,.30,parent=actors['Messi']['m']['CTRL_Body']),line('Bisht shoulder',[(.20,.95),(0,.72)],GOLD,.035,.30,parent=actors['Messi']['m']['CTRL_Body'])]
confetti=[]
for i in range(65):
    ob=rect('Gold confetti',-.02,-.065,.04,.13,[GOLD,'#ad843f','#fff1bd'][i%3],7);confetti.append((ob,rng.uniform(-3.7,3.7),rng.uniform(-4,6),rng.uniform(.7,1.7)))

# Every score/time is a separate native text object so the saved project scrubs faithfully.
ui=empty('Screen type');rect('Scoreboard',-2.25,4.42,4.5,.73,'#111d32',30,'scoreframe',ui)
rect('Argentina indicator',-2.25,4.42,.05,.73,'#82c4df',30.1,'scoreframe',ui);rect('France indicator',2.20,4.42,.05,.73,'#3f659f',30.1,'scoreframe',ui)
label('ARG','ARG',-1.47,4.78,.27,PAPER,30.2,'scoreframe',ui);label('FRA','FRA',1.47,4.78,.27,PAPER,30.2,'scoreframe',ui)
for txt in ('0 - 0','0 - 1','2 - 0','2 - 1','2 - 2','3 - 2','3 - 3','4 - 2'):
    label('Score '+txt,txt,0,4.78,.43,GOLD,30.2,'score '+txt,ui)
for txt in ("79′","80′","81′","108′","118′","PENALTIES","FINAL · PENALTIES","LATER · PRESENTATION"):
    label('Clock '+txt,txt,0,4.03,.24,'#ddd6bf',30.2,'clock '+txt,ui)
for group,txt,y,size,col in [('title','THREE GOALS.',-3.80,.47,PAPER),('title','ONE HEARTBREAK.',-4.33,.47,GOLD),('name','KYLIAN MBAPPÉ',-3.43,.25,GOLD),('ending','He gave everything.',-3.83,.38,PAPER),('hat','HAT-TRICK',-3.60,.29,GOLD),('shoot','SHOOTOUT',-3.80,.27,PAPER)]:label(group,txt,0,y,size,col,30.3,group,ui)
label('Opening context','WORLD CUP FINAL  /  LUSAIL 2022',0,3.52,.16,'#c8bda6',30.2,'opening',ui)
label('Final subtitle','ARGENTINA WIN 4–2 ON PENALTIES',0,-4.30,.19,'#c6cabf',30.3,'result',ui)
indicators={}
for team,y in [('FRA',3.55),('ARG',3.14)]:
    for i in range(4):
        for state,col in [('blank','#495469'),('goal','#88c798'),('miss','#d87779')]:
            ob=disk(team+' kick '+str(i+1)+' '+state,-.62+i*.43,y,.095,col,30.4,parent=ui);indicators[(team,i,state)]=ob
    label('Kick row '+team,team,-1.16,y,.18,PAPER,30.4,'dotslabels',ui)
# Fade is an animated material, avoiding a pile of opaque overlay cards.
fade=rect('Fade to black',-4,-7,8,14,'#000000',40,parent=ui)
fm=bpy.data.materials.new('Dissolve');fm.use_nodes=True;n=fm.node_tree.nodes;n.clear()
o=n.new('ShaderNodeOutputMaterial');tr=n.new('ShaderNodeBsdfTransparent');em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(0,0,0,1);mx=n.new('ShaderNodeMixShader');fm.node_tree.links.new(tr.outputs[0],mx.inputs[1]);fm.node_tree.links.new(em.outputs[0],mx.inputs[2]);fm.node_tree.links.new(mx.outputs[0],o.inputs[0]);fm.surface_render_method='DITHERED';fade.data.materials[0]=fm

shots=[(0,'still fighting'),(3,'first penalty'),(4.25,'return to halfway'),(6,'Thuram return and volley'),(8.55,'hope'),(10,'Messi rebound'),(11.15,'rise again'),(13,'exhausted resolve'),(15,'third goal'),(16.65,'relief'),(18,'shootout first kick'),(20.2,'deciding kick'),(23,'stillness'),(25,'presentation'),(27,'heartbreak')]
for t,nm in shots:scene.timeline_markers.new(nm,frame=round(t*FPS)+1)

# Kick contact from the actual boot outline; no guessed ball-to-foot connection.
T=3;act('Mbappe',-1.3,-2.8,.83,'kick',0,1)
scene.frame_set(1);bpy.context.view_layer.update()
ob=actors['Mbappe']['m']['Shoe_near'];boot=[(ob.matrix_world@v.co)[:2] for v in ob.data.vertices]
def distance(pts,p):
    ds=[]
    for a,b in zip(pts,pts[1:]+pts[:1]):
        dx,dy=b[0]-a[0],b[1]-a[1];u=clamp(((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy))
        ds.append(math.hypot(p[0]-a[0]-u*dx,p[1]-a[1]-u*dy))
    return min(ds)
by=-2.8+.16;lo=max(p[0] for p in boot);hi=lo+.5
for _ in range(45):
    mid=(lo+hi)/2
    if distance(boot,(mid,by))<.16+.0205*.83:lo=mid
    else:hi=mid
CONTACT=((lo+hi)/2,by)
# Volley uses its own elevated right boot surface at the authored strike pose.
T=7.5;act('Mbappe',-1.35,-2.6,.82,'volley',0,1);scene.frame_set(1);bpy.context.view_layer.update()
ob=actors['Mbappe']['m']['Shoe_near'];vv=[(ob.matrix_world@v.co)[:2] for v in ob.data.vertices]
vy=-2.6+.82*.83;lo=max(p[0] for p in vv);hi=lo+.5
for _ in range(45):
    mid=(lo+hi)/2
    if distance(vv,(mid,vy))<.16+.0205*.82:lo=mid
    else:hi=mid
VOLLEY=((lo+hi)/2,vy)
T=10.25;act('Messi',-.70,-2.4,.75,'kick',0,1);scene.frame_set(1);bpy.context.view_layer.update()
ob=actors['Messi']['m']['Shoe_near'];mv=[(ob.matrix_world@v.co)[:2] for v in ob.data.vertices]
my=-2.4+.16;lo=max(p[0] for p in mv);hi=lo+.5
for _ in range(45):
    mid=(lo+hi)/2
    if distance(mv,(mid,my))<.16+.0205*.75:lo=mid
    else:hi=mid
MESSI_CONTACT=((lo+hi)/2,my)
GOAL=(2.38,-1.21)

def flight(start,end,u,arc=.1):return (mix(start[0],end[0],clamp(u)),mix(start[1],end[1],clamp(u))+arc*math.sin(math.pi*clamp(u)))

started=time.monotonic();checks={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'helper_sha256':hashlib.sha256(HELPERS.read_bytes()).hexdigest(),'penalty_contact':CONTACT,'volley_contact':VOLLEY,'messi_contact':MESSI_CONTACT,'frames':720,'fps':24,'duration':30,'new_identity_art':True,'contact_times':[3,7.5,10.25,15.25,18.625,21.25]}
for f in range(1,FRAMES+1):
    T=t=(f-1)/FPS
    used.clear()
    showgoal=False;showball=False;bp=CONTACT;active=None;score='2 - 0';clock='79′';cx=.20;cy=-.65;v=9.2;hit=None;target=None
    if t<2.45:
        act('Mbappe',0,-2.7,1,'resolve',t,f);cx=.04;cy=mix(1.3,.37,ease(t/.90));v=track(t,[(0,14.6),(.90,3.95),(2.45,3.65)])[0]
    elif t<4.25:
        showgoal=showball=True;score='2 - 1' if t>=3.45 else '2 - 0';clock='80′' if t>=3 else '79′'
        act('Mbappe',-1.3,-2.8,.83,'kick',t-3,f)
        u=ease((t-3.08)/.65);act('Martinez',1.45+.26*u,-1.45-.20*u,.56,'keeper',t,f,roll=-1.25*u,depth=-7)
        bp=CONTACT if t<=3 else flight(CONTACT,GOAL,(t-3)/.45);hit=3;target=CONTACT
    elif t<6:
        score='2 - 1';clock='80′';act('Mbappe',.20,-2.45,.95,'urgent',t-4.25,f,d=-1)
        act('Thuram',-2.5+ease((t-4.25)/1.3)*.8,-2.35,.80,'watch',t,f,depth=-1);v=10
    elif t<8.55:
        showgoal=showball=True;clock='81′';score='2 - 2' if t>=7.95 else '2 - 1'
        act('Mbappe',-1.35,-2.6,.82,'volley',t-7.5,f)
        if t<6.55:act('Thuram',1.95,-2.5,.59,'kick',t-6.3,f,d=-1,depth=-2)
        else:act('Thuram',1.95+3.02*(t-6.55),-2.5,.59,'run',(t-6.55)/.50,f,depth=-2)
        u=ease((t-7.5)/.6);act('Martinez',1.45+.26*u,-1.45-.2*u,.56,'keeper',t,f,roll=-1.2*u,depth=-7)
        bp=flight((1.30,-2.36),VOLLEY,(t-6.3)/1.2,.80) if t<7.5 else flight(VOLLEY,GOAL,(t-7.5)/.45)
        hit=7.5;target=VOLLEY
    elif t<10:
        score='2 - 2';clock='81′';act('Mbappe',0,-2.7,.98,'celebrate',t-8.55,f);v=9.5
        act('Thuram',-2.2+.7*ease(t-8.55),-2.65,.79,'celebrate',t,f,depth=-1)
        act('Kolo Muani',2.3-.85*ease(t-8.55),-2.60,.8,'celebrate',t+.3,f,depth=-1)
    elif t<11.15:
        showgoal=showball=True;clock='108′';score='3 - 2' if t>=10.6 else '2 - 2';v=9.2
        act('Messi',-.70,-2.4,.75,'kick',t-10.25,f)
        act('Lloris',1.8,-1.6,.56,'keeper',t,f,roll=-1.18,depth=-7)
        start=MESSI_CONTACT;bp=flight((1.1,-1.5),start,(t-10)/.25,.08) if t<10.25 else flight(start,GOAL,(t-10.25)/.35);hit=10.25;target=start
    elif t<13:
        score='3 - 2';clock='108′';act('Mbappe',0,-2.5,1,'rise',t-11.15,f);cx=.08;cy=.14;v=5.2
    elif t<14.8:
        score='3 - 2';clock='118′';act('Mbappe',0,-2.7,1,'exhausted',t-13,f);cx=.08;cy=.25;v=mix(3.95,3.65,ease((t-13)/1.8))
    elif t<16.65:
        showgoal=showball=True;score='3 - 3' if t>=15.70 else '3 - 2';clock='118′'
        act('Mbappe',-1.3,-2.8,.83,'kick',t-15.25,f)
        u=ease((t-15.32)/.65);act('Martinez',1.45-.50*u,-1.45-.15*u,.56,'keeper',t,f,roll=1.25*u,depth=-7)
        bp=CONTACT if t<=15.25 else flight(CONTACT,GOAL,(t-15.25)/.45);hit=15.25;target=CONTACT
    elif t<18:
        score='3 - 3';clock='118′';v=9.4
        act('Mbappe',0,-2.7,.98,'celebrate',(t-16.65)*.55,f)
        act('Thuram',-2.2+ease(t-16.65)*.85,-2.65,.79,'celebrate',t,f,depth=-1)
        act('Kolo Muani',2.2-ease(t-16.65)*.85,-2.65,.79,'celebrate',t+.3,f,depth=-1)
    elif t<20.2:
        showgoal=showball=True;score='0 - 1' if t>=19.075 else '0 - 0';clock='PENALTIES'
        act('Mbappe',-1.3,-2.8,.83,'kick',t-18.625,f)
        u=ease((t-18.70)/.65);act('Martinez',1.45+.26*u,-1.45-.15*u,.56,'keeper',t,f,roll=-1.2*u,depth=-7)
        bp=CONTACT if t<=18.625 else flight(CONTACT,GOAL,(t-18.625)/.45);hit=18.625;target=CONTACT
    elif t<23:
        showgoal=showball=True;score='4 - 2' if t>=21.75 else '3 - 2';clock='FINAL · PENALTIES' if t>=21.75 else 'PENALTIES'
        act('Montiel',-1.3,-2.8,.83,'kick',t-21.25,f)
        u=ease((t-21.32)/.65);act('Lloris',1.45-.50*u,-1.45-.2*u,.56,'keeper',t,f,roll=1.25*u,depth=-7)
        bp=CONTACT if t<=21.25 else flight(CONTACT,GOAL,(t-21.25)/.45);hit=21.25;target=CONTACT
    elif t<25:
        score='4 - 2';clock='FINAL · PENALTIES';v=11.4
        act('Mbappe',-.8,-2.45,.95,'broken',t-23,f,depth=1)
        act('Martinez',2,-.40,.46,'celebrate',t,f,depth=-4)
        for i,name in enumerate(('Messi','Montiel','Argentina teammate')):
            x=mix(-2.6+i*.45,1.1+i*.4,ease((t-23)/1.5));act(name,x,-.47-i*.08,.43,'run',(t-23)/.42,f,depth=-5)
    elif t<27:
        score='4 - 2';clock='LATER · PRESENTATION';v=10.6;cy=.42
        lift=.15*ease((t-25)/.6);act('Messi',0,-2.55+lift,.91,'lift',t-25,f)
        for i,name in enumerate(('Montiel','Argentina teammate','Martinez')):
            act(name,[-1.72,1.72,2.6][i],-2.6,.70,'celebrate',t+i,f,depth=-1)
        trophy.location=(0,-2.55+lift+.91*3.22,1);trophy.scale=(.91,.91,.91);key(trophy,f)
    else:
        score='4 - 2';clock='FINAL · PENALTIES';q=t-27;act('Mbappe',0,-2.70,1,'broken',q+.45,f)
        cy=mix(.10,-.15,ease(q/2.4));cx=.04;v=mix(3.65,6.8,ease(q/2.4))
    for name,a in actors.items():
        visible([ob for ob in a['all'] if ob not in a['sweat']],name in used,f)
        visible(a['sweat'],name in used and name=='Mbappe' and (10<=t<18 or t>=23),f)
    for group,items in GROUPS.items():
        on=(group=='goal' and showgoal) or (group=='spot' and showball and not 6<=t<11.15)
        if group.startswith('score '):on=group[6:]==score and not 25<=t<27 and t<29.6
        elif group.startswith('clock '):on=group[6:]==clock and t<29.6
        elif group=='title':on=t<2.45
        elif group=='name':on=t<2.45
        elif group=='opening':on=t<2.45
        elif group=='hat':on=16.65<=t<18
        elif group=='shoot':on=18<=t<23
        elif group=='ending':on=t>=28.3
        elif group=='result':on=23<=t<25
        elif group=='dotslabels':on=18<=t<23
        elif group=='scoreframe':on=not 25<=t<27 and t<29.6
        visible(items,on,f)
    visible([robe]+robelines,25<=t<27,f);visible([trophy]+tro,25<=t<27,f)
    for ob,x,y,s in confetti:
        visible([ob],25<=t<27,f);ob.location=(x+.25*math.sin(t*2+x),((y-(t-25)*s+7)%12)-5,0);ob.rotation_euler.z=t*3+x;key(ob,f)
    for (team,i,state),ob in indicators.items():
        expected='blank'
        if t>=20.2:expected=('goal' if team=='ARG' and (i<3 or t>=21.75) else 'goal' if team=='FRA' and i in (0,3) else 'miss' if team=='FRA' else 'blank')
        elif team=='FRA' and i==0 and t>=19.075:expected='goal'
        visible([ob],18<=t<23 and state==expected,f)
    visible(ballitems,showball,f);ball.location=(*bp,0);ball.rotation_euler.z=-t*9;key(ball,f)
    for i,ob in enumerate(trail):
        running=showball and hit is not None and hit<t<hit+.45
        visible([ob],running,f)
        if running:ob.location=(*flight(target,GOAL,max(0,(t-hit-.024*(i+1))/.45)),0);key(ob,f)
    visible(rays,hit is not None and 0<=t-hit<.13,f)
    if target:impact.location=(*target,0);impact.scale=(1+max(0,t-hit)*2,)*3;key(impact,f)
    for ob,pts in net:
        u=t-hit-(.35 if hit==10.25 else .45) if hit is not None else -1;k=.10*math.exp(-u*7)*math.sin(u*35) if 0<u<.7 else 0
        for p,(x,y) in zip(ob.data.splines[0].points,pts):p.co=(x+k,y,-11,1);p.keyframe_insert(data_path='co',frame=f)
    # Mild contact impulse; restrained enough to preserve the exact contact reading.
    if hit is not None and .04<t-hit<.17:cx+=.022*math.sin((t-hit)*70)
    camera.location=(cx,cy,90);key(camera,f,False);camdata.ortho_scale=v;camdata.keyframe_insert(data_path='ortho_scale',frame=f)
    ui.location=(cx,cy,0);ui.scale=(v/12,)*3;key(ui,f)
    # The stadium recedes after the winning kick; the face stays readable in its own light.
    dusk=.55*ease((t-23)/.9) if 23<=t<25 else .62*ease((t-27)/.9) if t>=27 else 0
    for c in ('#286152','#2b6956','#3a785c','#222e45','#7f9aa3','#c5c4b0','#5484a5','#5d7084','#39495d','#502337'):
        e=next(n for n in MATS[c].node_tree.nodes if n.type=='EMISSION')
        col=rgba(c);e.inputs[0].default_value=(col[0]*(1-dusk),col[1]*(1-dusk*.9),col[2]*(1-dusk*.65),1);e.inputs[0].keyframe_insert(data_path='default_value',frame=f)
    fac=ease((t-29.35)/.58);mx.inputs[0].default_value=fac;mx.inputs[0].keyframe_insert(data_path='default_value',frame=f)
    if f%120==0:print('BAKE',f,FRAMES,flush=True)

for action in bpy.data.actions:
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path in ('hide_render','hide_viewport') else 'LINEAR'
scene.frame_set(34);bpy.context.view_layer.update()
valid=sum(1 for a in actors.values() for ob in a['m'].values() if ob.data and ob.data.animation_data for fc in ob.data.animation_data.drivers if fc.driver.is_valid)
assert valid==48*len(actors),valid
checks.update(valid_limb_drivers=valid,actors=len(actors),bake_seconds=time.monotonic()-started)
(OUT/'build-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
scene['Historical basis']='FIFA match report: 18 December 2022. 3-3 AET, Argentina 4-2 PSO. Mbappe 80,81,118; Messi108.'
scene['Interpretation']='Original compressed dramatization. Expressions/cameras/positions are illustrative. Shootout is distinct from three match goals.'
scene['Artwork']='New original player faces and kit artwork; simple limb controls reused. Not a fixed C visual identity.'
for ob in template.values():
    if not ob.users_collection:bpy.data.objects.remove(ob)
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False
scene.render.filepath='//stills/';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'three-goals.blend'))
if '--samples' in sys.argv:
    scene.render.resolution_percentage=50
    for t in [0,1.5,2.7,3,3.55,4.8,6.6,7.5,8.1,9,10.65,12.1,13.8,15.25,16,17.1,18.625,19.4,21.25,22,23.8,25.7,27.4,28.8,29.8]:
        scene.frame_set(round(t*FPS)+1);scene.render.filepath=str(OUT/f'stills/sample-{round(t*FPS)+1:04}.png');bpy.ops.render.render(write_still=True)
print('FILM_BUILD_READY',flush=True)
