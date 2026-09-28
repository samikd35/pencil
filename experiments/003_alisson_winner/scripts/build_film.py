"""Author and bake the Alisson Short into a self-contained editable Blender film.
Run with Blender --background --factory-startup --python-exit-code 1 --python this_file.
Use -- --samples for review stills or -- --render for the silent master.
"""
from pathlib import Path
import bpy
import math
import json
import sys
import time
import subprocess
import hashlib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/film-v001'
SOURCE=ROOT.parent/'001_heavy_box/artifacts/finish-v002/character-and-effects.blend'
FPS=24; SECONDS=40; FRAMES=FPS*SECONDS
OUT.mkdir(parents=True,exist_ok=True);(OUT/'stills').mkdir(exist_ok=True)
INK='#182c36'; PAPER='#fff6df'; GOLD='#efc563'; RED='#df4a51'; GREEN='#9ad7b8'; BLACK='#18272f'
MATS={}; GROUPS={}; actors={}; changing=[]

def clamp(v,a=0,b=1):return min(b,max(a,v))
def ease(t):t=clamp(t);return t*t*(3-2*t)
def mix(a,b,t):return a+(b-a)*t
def vec(a,b,t):return tuple(mix(x,y,t) for x,y in zip(a,b))
def track(t,keys):
    if t<=keys[0][0]:return keys[0][1:]
    for a,b in zip(keys,keys[1:]):
        if t<=b[0]:return vec(a[1:],b[1:],ease((t-a[0])/(b[0]-a[0])))
    return keys[-1][1:]
def rgba(c):
    v=[int(c[i:i+2],16)/255 for i in (1,3,5)]
    return tuple(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v)+(1,)
def mat(c):
    if c not in MATS:
        m=bpy.data.materials.new('Film '+c);m.use_nodes=True;m.diffuse_color=rgba(c)
        n=m.node_tree.nodes;n.clear();o=n.new('ShaderNodeOutputMaterial');e=n.new('ShaderNodeEmission');e.inputs[0].default_value=rgba(c);m.node_tree.links.new(e.outputs[0],o.inputs['Surface']);MATS[c]=m
    return MATS[c]

scene=bpy.data.scenes.new('The Goalkeeper Who Scored the Winner')
bpy.context.window.scene=scene
art=bpy.data.collections.new('Original stadium and graphic artwork');scene.collection.children.link(art)
scene.render.engine='BLENDER_EEVEE';scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.render.resolution_percentage=100
scene.render.fps=FPS;scene.frame_start=1;scene.frame_end=FRAMES
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.compression=15
scene.render.film_transparent=False;scene.render.use_compositing=False;scene.render.use_sequencer=False
scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
scene.world=bpy.data.worlds.new('Stadium atmosphere');scene.world.color=(.02,.04,.05)
scene.eevee.taa_render_samples=16
camdata=bpy.data.cameras.new('Portrait camera');camera=bpy.data.objects.new('Portrait camera',camdata);art.objects.link(camera)
camdata.type='ORTHO';camdata.sensor_fit='VERTICAL';camdata.ortho_scale=16;camera.location=(0,0,90);scene.camera=camera
font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf')
regular=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial.ttf')

def add(obj,group=None,parent=None):
    art.objects.link(obj);obj.parent=parent
    if group:GROUPS.setdefault(group,[]).append(obj)
    return obj

def poly(name,pts,c,z=0,group=None,parent=None):
    m=bpy.data.meshes.new(name);m.from_pydata([(*p,z) for p in pts],[],[list(range(len(pts)))]);m.materials.append(mat(c))
    return add(bpy.data.objects.new(name,m),group,parent)
def line(name,pts,c=PAPER,w=.035,z=0,group=None,parent=None,closed=False):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=w/2;d.bevel_resolution=2
    s=d.splines.new('POLY');s.points.add(len(pts)-1)
    for p,xy in zip(s.points,pts):p.co=(*xy,z,1)
    s.use_cyclic_u=closed;d.materials.append(mat(c));return add(bpy.data.objects.new(name,d),group,parent)
def rect(name,x,y,w,h,c,z=0,group=None,parent=None):return poly(name,[(x,y),(x+w,y),(x+w,y+h),(x,y+h)],c,z,group,parent)
def oval(x,y,rx,ry,n=40):return [(x+rx*math.cos(i*math.tau/n),y+ry*math.sin(i*math.tau/n)) for i in range(n)]
def label(name,text,x,y,size=.35,c=PAPER,z=20,group=None,parent=None,bold=True,align='CENTER',spacing=1):
    d=bpy.data.curves.new(name,'FONT');d.body=text;d.font=font if bold else regular;d.align_x=align;d.align_y='CENTER';d.size=size;d.space_character=spacing;d.materials.append(mat(c))
    obj=add(bpy.data.objects.new(name,d),group,parent);obj.location=(x,y,z);return obj

def disk(name,x,y,r,c,z=0,group=None,parent=None):return poly(name,oval(x,y,r,r),c,z,group,parent)
def empty(name):
    obj=bpy.data.objects.new(name,None);art.objects.link(obj);return obj

def visible(items,on,frame):
    for obj in items:
        old=obj.get('last_visible',None)
        if old is None or old!=on:
            if old is not None and frame>1:
                obj.keyframe_insert(data_path='hide_render',frame=frame-1)
                obj.keyframe_insert(data_path='hide_viewport',frame=frame-1)
            obj.hide_render=obj.hide_viewport=not on
            obj.keyframe_insert(data_path='hide_render',frame=frame);obj.keyframe_insert(data_path='hide_viewport',frame=frame)
            obj['last_visible']=on

def key(obj,frame,scale=True):
    obj.keyframe_insert(data_path='location',frame=frame);obj.keyframe_insert(data_path='rotation_euler',frame=frame)
    if scale:obj.keyframe_insert(data_path='scale',frame=frame)

# Broad stadium, empty seats and a soft overcast sky. All original vectors.
rect('Sky',-100,-20,200,60,'#c4d8d0',-16)
rect('Stand shadow',-100,.6,200,6.6,'#173b46',-15)
for i in range(9):
    y=1.2+i*.5
    rect('Terrace riser',-100,y-.09,200,.10,'#244c59',-14)
    pts=[];faces=[]
    for j in range(310):
        x=-100+j*.66+(i%2)*.33;n=len(pts)
        pts.extend([(x,y,-13),(x+.40,y,-13),(x+.37,y+.24,-13),(x+.03,y+.24,-13)]);faces.append((n,n+1,n+2,n+3))
    mesh=bpy.data.meshes.new('Empty blue seats');mesh.from_pydata(pts,[],faces);mesh.materials.append(mat('#416676' if i%2 else '#355967'));add(bpy.data.objects.new('Empty blue seat row',mesh))
rect('Concourse',-100,5.82,200,.34,'#c6d7d0',-12)
line('Roof edge',[(-100,6.58),(100,6.58)],'#758e90',.10,-12)
for x in range(-96,100,6):
    rect('Roof support',x,5.7,.09,1.35,'#768f93',-11)
rect('Pitch',-100,-30,200,33.0,'#337a62',-10)
for i in range(12):
    yy=-28+i*2.8
    if yy<3:rect('Mowing stripe',-100,yy,200,min(1.4,3-yy),'#377f66',-9.9)
line('Far touchline',[(-100,3),(100,3)],'#99c6a7',.045,-9.6)
rect('Pitchside board',-100,3.05,200,.62,'#203e49',-9)
for x in range(-90,100,8):
    label('Stadium name','THE HAWTHORNS',x,3.36,.24,'#8fabae',-8,bold=True,spacing=1.1)
for x in range(-70,75,8):line('Field stripe',[(x,-8),(x+3,3.0)],'#5c9b7b',.025,-8)
# A gradient keeps the lower text readable without enclosing the action in a card.
bottom=rect('Lower vignette',-100,-12,200,7,'#143d3c',-7)

# Goal constructions with a separately deformable net.
netlines=[]
def goal(group,x,y,w,h,scale=1):
    ox=.42*scale;oy=.24*scale
    poly('Inside goal',[(x,y),(x+w,y),(x+w+ox,y+oy),(x+w+ox,y+h+oy),(x+ox,y+h+oy)],'#244f4a',-5,group)
    for j in range(14):
        a=x+j*w/13
        ob=line('Net vertical',[(a,y),(a+ox,y+h+oy)],'#789d90',.018,-4.8,group);netlines.append((ob,[(a,y),(a+ox,y+h+oy)]))
    for j in range(10):
        b=y+j*h/9
        ob=line('Net horizontal',[(x,b),(x+w+ox,b+oy)],'#789d90',.018,-4.7,group);netlines.append((ob,[(x,b),(x+w+ox,b+oy)]))
    line('Goal frame',[(x,y),(x,y+h),(x+w,y+h),(x+w,y)],PAPER,.10,-3.8,group)
    line('Goal depth',[(x,y+h),(x+ox,y+h+oy),(x+w+ox,y+h+oy),(x+w,y+h)],'#bfd5c5',.05,-4,group)
    line('Goal line',[(x-.7,y),(x+w+.7,y)],'#c0d8bd',.055,-4.2,group)
    line('Penalty area',[(x-.9,y),(x-1.65,y-1.7),(x+w+.25,y-1.7),(x+w+.95,y)],'#94bea0',.045,-6,group)
goal('home_goal',-2.6,-2.8,4.7,3.35)
goal('away_goal',.1,-1.7,3.9,2.8,.8)
cornerroot=empty('Corner flag assembly')
line('Corner touchline',[(-4,-3.65),(1.45,-3.65),(4.8,-.8)],PAPER,.05,-4,'corner')
line('Corner arc',[(1.45-.65*math.cos(a),-3.65+.65*math.sin(a)) for a in [i*math.pi/24 for i in range(13)]],PAPER,.035,-3.8,'corner')
line('Flag pole',[(1.45,-3.65),(1.45,-1.1)],'#d6dbc3',.055,-3,'corner')
flag=poly('Corner pennant',[(1.45,-1.1),(2.25,-1.36),(1.45,-1.62)],GOLD,-2.9,'corner')

# Import and duplicate the actual C character. Curves retain the original editable endpoint drivers.
keep={'Bean torso','Head','Head_outline','Eye_0','Eye_1','Brow_0','Brow_1','Mouth','Mouth open','CTRL_Body','CTRL_Head','ANCHOR_Shoulder'}
for side in ('far','near'):
    keep.update(f'{p}_{side}' for p in ('Mitten','Shoe','Arm','Leg'))
    keep.update(f'{p}_{side}_outline' for p in ('Mitten','Shoe'))
    keep.update(f'CTRL_{p}_{side}' for p in ('Hand','Foot','Elbow','Knee'))
with bpy.data.libraries.load(str(SOURCE),link=False) as (src,dst):
    assert keep.issubset(set(src.objects));dst.objects=list(keep)
template={o.name:o for o in dst.objects}

def character(name,color,number,striped=False):
    col=bpy.data.collections.new(name+' - C character');scene.collection.children.link(col)
    mapping={}
    for n,old in template.items():
        obj=old.copy();obj.name=name+' / '+n;obj.animation_data_clear()
        if old.data:
            obj.data=old.data.copy()
            if obj.data.animation_data:obj.data.animation_data.action=None
        col.objects.link(obj);mapping[n]=obj
    for n,obj in mapping.items():
        if template[n].parent:obj.parent=mapping[template[n].parent.name]
        if obj.data and obj.data.animation_data:
            for fc in obj.data.animation_data.drivers:
                for v in fc.driver.variables:
                    for target in v.targets:
                        if target.id and target.id.name in mapping:target.id=mapping[target.id.name]
        if obj.data and hasattr(obj.data,'materials'):
            obj.data.materials.clear();obj.data.materials.append(mat(PAPER if n in ('Head','Mitten_far','Mitten_near') else INK))
    for n in ('Shoe_far','Shoe_near'):
        mapping[n].data.materials[0]=mat('#e87d63' if color==BLACK else color)
    mapping['Bean torso'].data.materials[0]=mat(color)
    mapping['Bean torso'].scale.x=1.55
    for i in range(2):
        eye=mapping[f'Eye_{i}'];eye.location=( -.03+i*.32,.055,0)
        br=mapping[f'Brow_{i}']
        for j,p in enumerate(br.data.splines[0].points):p.co=(-.15+i*.32+.24*j/(len(br.data.splines[0].points)-1),.30+.05*math.sin(j/(len(br.data.splines[0].points)-1)*math.pi),.45,1)
    for j,p in enumerate(mapping['Mouth'].data.splines[0].points):
        u=j/(len(mapping['Mouth'].data.splines[0].points)-1);p.co=(.005+.25*u,-.24-.08*math.sin(math.pi*u),.45,1)
    extra=[]
    focused=line(name+' focused mouth',[(.015+.23*u/16,-.28+.045*math.sin(math.pi*u/16)) for u in range(17)],INK,.034,.45,parent=mapping['CTRL_Head']);extra.append(focused)
    mapping['Mouth focused']=focused
    num=label(name+' shirt number',number,0,.41,.29,PAPER if not striped else INK,.25,parent=mapping['CTRL_Body']);extra.append(num)
    if striped:
        for x in (-.10,.10):extra.append(line(name+' kit stripe',[(x,.12),(x,.75)],INK,.055,.24,parent=mapping['CTRL_Body']))
    shadow=poly(name+' contact shadow',oval(0,0,.68,.12),'#235b4d',-3.5)
    objects=list(mapping.values())+extra+[shadow]
    actors[name]={'m':mapping,'all':objects,'shadow':shadow,'extra':extra,'number':num}
    return actors[name]
character('Alisson',BLACK,'1')
character('Trent',RED,'66')
character('Liverpool A',RED,'11')
character('Liverpool B',RED,'9')
character('West Brom A',PAPER,'5',True)
character('West Brom B',PAPER,'6',True)
character('Johnstone',GREEN,'1')

# Ball is one coherent animated object; seams rotate with it.
ball=empty('Match ball - continuous trajectory')
disk('Ball face',0,0,.22,PAPER,.7,parent=ball)
line('Ball outline',oval(0,0,.22,.22),INK,.035,.72,parent=ball,closed=True)
poly('Ball central panel',[(.082*math.cos(i*math.tau/5),.082*math.sin(i*math.tau/5)) for i in range(5)],INK,.73,parent=ball)
for i in range(5):
    a=i*math.tau/5
    line('Ball panel seam',[(.08*math.cos(a),.08*math.sin(a)),(.21*math.cos(a),.21*math.sin(a))],INK,.015,.735,parent=ball)
ballobjects=[ball]+list(ball.children)
trail=[]
for i in range(6):
    ob=disk('Ball trail '+str(i),0,0,.15*(1-i*.1),['#e7d39b','#bfc5a0','#9bb895','#79a582','#58936f','#438564'][i],.65);trail.append(ob)

# Portrait graphics follow the camera; names and score remain clear on a phone.
ui=empty('Screen graphics');changing.append(ui)
rect('Score dark band',-4.10,5.43,8.20,1.02,INK,28,parent=ui)
rect('WBA color tab',-4.10,5.43,.09,1.02,'#9faebb',28.1,parent=ui)
rect('Liverpool color tab',4.01,5.43,.09,1.02,RED,28.1,parent=ui)
label('WBA team','WBA',-2.72,5.94,.48,PAPER,28.2,parent=ui)
label('Liverpool team','LIV',2.72,5.94,.48,PAPER,28.2,parent=ui)
label('Score tied','1 : 1',0,5.94,.65,PAPER,28.2,'score_tied',ui)
label('Score winner','1 : 2',0,5.94,.65,GOLD,28.2,'score_winner',ui)
label('Late clock',"90 +5'",0,4.98,.35,GOLD,28.2,parent=ui)
label('Date footer','THE HAWTHORNS  /  16 MAY 2021',0,-6.33,.22,'#bad0bf',28.2,parent=ui,bold=False,spacing=1.1)

progress=line('Film progress',[(-3.85,-6.8),(3.85,-6.8)],'#527d69',.025,28.2,parent=ui)
bar=rect('Film progress fill',0,0,1,.035,GOLD,28.3,parent=ui);bar.location=(-3.85,-6.817,0)
for group,title,subtitle in [
 ('caption0','THE GOALKEEPER','WHO SCORED THE WINNER'),
 ('caption1','HIS GOAL CAN WAIT.','ONE LAST CORNER.'),
 ('caption2','ONE LAST CHANCE.','LIVERPOOL NEED A WINNER.'),
 ('caption3','TRENT DELIVERS.','ALEXANDER-ARNOLD  /  66'),
 ('caption4','ALISSON RISES.',''),
 ('caption5','THE KEEPER. THE WINNER.','WEST BROM 1 - 2 LIVERPOOL'),
 ('caption6','ALISSON BECKER',"THE WINNER.  90+5'."),
]:
    label(group+' main',title,0,-4.72,.46 if len(title)<24 else .40,PAPER,28.3,group,ui)
    if subtitle:label(group+' sub',subtitle,0,-5.35,.245,GOLD,28.3,group,ui,bold=False,spacing=1.05)
hero_name=label('Alisson identity','ALISSON  /  GOALKEEPER',0,2.48,.27,GOLD,22,'hero_name')
# Contact accent is a brief radial drawing, not a full-screen flash.
impactroot=empty('Header impact accent')
for i in range(7):
    a=math.tau*i/7;line('Impact ray',[(.32*math.cos(a),.32*math.sin(a)),(.52*math.cos(a),.52*math.sin(a))],GOLD,.035,.8,'impact',impactroot)

# Local poses reuse the original proportions; their timing is authored for this film.
def pose(mode,t=0):
    p={'hip':(0,1.72),'tilt':0.,'feet':[(-.38,.12,0),(.38,.12,0)],'hands':[(-.50,1.35,0),(.62,1.40,0)],'headtilt':0.,'joy':0.,'focus':0.}
    if mode=='ready':
        p['hip']=(0,1.60+.025*math.sin(t*3));p['tilt']=-.07;p['hands']=[(-.72,1.65,.2),(.79,1.55,-.2)];p['focus']=.5
    elif mode=='run':
        phase=t%1.;p['hip']=(0,1.57+.075*math.cos(phase*math.tau*2));p['tilt']=-.20;p['headtilt']=-.08;p['focus']=.35
        for i in range(2):
            q=(phase+i*.5)%1
            if q<.5:x=.64-2.56*q;y=.12;angle=0
            else:u=(q-.5)*2;x=mix(-.64,.64,ease(u));y=.12+.66*math.sin(math.pi*u);angle=.5*math.sin(math.tau*u)
            p['feet'][i]=(x,y,angle)
            swing=math.sin(phase*math.tau+i*math.pi);p['hands'][i]=(-.10+.72*swing,1.74+.16*abs(swing),-.30*swing)
    elif mode=='kick':
        # Time relative to strike. Plant remains fixed through release.
        h=track(t,[(-2.,-.70,1.62),(-.8,-.34,1.62),(-.25,-.13,1.55),(0,0,1.6),(.22,.18,1.55),(.8,.35,1.67),(2,.45,1.72)])
        p['hip']=h;p['tilt']=track(t,[(-2,-.12),(-.3,.23),(0,-.15),(.3,-.36),(1,-.05)])[0]
        p['feet'][0]=(-.15,.12,0)
        p['feet'][1]=track(t,[(-2,-.95,.16,0),(-.55,-1.12,.57,.5),(-.20,-.55,.30,.2),(0,.64,.12,0),(.24,1.05,1.03,-.45),(.7,.50,.24,0),(1.1,.73,.12,0)])
        p['hands']=[(-.72,2.0,.5),(.90,2.16,-.5)];p['focus']=.65
    elif mode=='header':
        h=track(t,[(-4,0,1.70),(-2.0,.03,1.70),(-1.0,.18,1.35),(-.55,.22,1.24),(-.10,.32,1.65),(0,.34,1.71),(.18,.57,1.61),(.70,.76,1.42),(1.3,.82,1.62),(2,.90,1.72)])
        p['hip']=h;p['tilt']=track(t,[(-4,-.03),(-1,.15),(-.35,.27),(0,.06),(.16,-.42),(.5,-.20),(1.4,0)])[0]
        p['headtilt']=track(t,[(-4,.0),(-1,.06),(-.4,.13),(0,-.02),(.15,-.24),(.7,0)])[0]
        p['feet']=[(-.30,.12,0),(.44,.12,0)]
        if t>-.5 and t<.63:
            u=clamp((t+.5)/1.13);lift=.30*math.sin(math.pi*u)
            p['feet']=[(-.15,.15+lift,.10),(.48,.35+lift,.38)]
        elif t>=.63:p['feet']=[(.5,.12,0),(1.2,.12,0)]
        p['hands']=[(-.98,2.27,.3),(.93,2.52,-.4)];p['focus']=.7
    elif mode=='celebrate':
        p['hip']=(0,1.72+.06*math.sin(t*4));p['hands']=[(-.83,3.06+.11*math.sin(t*4),.9),(.87,3.12+.12*math.cos(t*3.3),-.9)];p['headtilt']=-.06*math.sin(t*2);p['joy']=1
        p['feet']=[(-.47,.12,0),(.52,.12,0)]
    elif mode=='watch':
        p['hip']=(0,1.65+.015*math.sin(t*2));p['headtilt']=.08;p['focus']=.25;p['hands']=[(-.60,1.55,.1),(.63,1.75,-.1)]
    elif mode=='disbelief':
        p['hands']=[(-.61,2.80,.5),(.70,2.86,-.5)];p['hip']=(0,1.60);p['focus']=.15
    elif mode=='keeper':
        p['hip']=(0,1.48);p['feet']=[(-.63,.12,0),(.65,.12,0)];p['hands']=[(-.85,1.73,.2),(.92,1.73,-.2)];p['focus']=.4
    return p

def joint(a,b,length,side,bend=.55):
    dx,dy=b[0]-a[0],b[1]-a[1];d=math.hypot(dx,dy);h=bend*math.sqrt(max(0,length*length-d*d/4))
    return ((a[0]+b[0])/2-side*dy*h/max(d,.001),(a[1]+b[1])/2+side*dx*h/max(d,.001))

def set_actor(name,x,y,s,d,mode,pt,frame,jump=0,depth=0):
    a=actors[name];m=a['m'];p=pose(mode,pt)
    hip=p['hip'];ang=p['tilt'];sh=(hip[0]-.84*math.sin(ang),hip[1]+.84*math.cos(ang));hp=(sh[0]-.02,sh[1]+.68)
    def world(v):return (x+d*s*v[0],y+s*v[1]+jump)
    def tr(n,xy,rot=0):
        ob=m[n];ob.location=(*world(xy),depth);ob.rotation_euler.z=d*rot;ob.scale=(s*d,s,s);key(ob,frame)
    tr('CTRL_Body',hip,ang);tr('CTRL_Head',hp,p['headtilt'])
    for i,side in enumerate(('far','near')):
        foot=p['feet'][i];hand=p['hands'][i];tr('CTRL_Foot_'+side,foot[:2],foot[2]);tr('CTRL_Hand_'+side,hand[:2],hand[2])
        tr('CTRL_Elbow_'+side,joint(sh,hand[:2],.93,-1 if hand[0]>sh[0] else 1,.62))
        tr('CTRL_Knee_'+side,joint(hip,foot[:2],1.08,-1 if i==0 else 1,.55))
        for kind in ('Arm','Leg'):
            ob=m[kind+'_'+side];ob.location.z=depth;ob.data.bevel_depth=.026*s;ob.keyframe_insert(data_path='location',frame=frame)
            ob.data.keyframe_insert(data_path='bevel_depth',frame=frame)
    blink=max(0,1-abs((pt+name.__len__()*.23)%3.4-3.12)/.095)
    for i in range(2):
        ob=m['Eye_'+str(i)];ob.scale=(1,max(.06,1-p['focus']*.40-blink*.95),1);ob.keyframe_insert(data_path='scale',frame=frame)
        ob=m['Brow_'+str(i)];ob.rotation_euler.z=(.18 if i==0 else -.18)*p['focus'];ob.keyframe_insert(data_path='rotation_euler',frame=frame)
    for n,on in [('Mouth',p['joy']<.5 and p['focus']<.2 and mode!='disbelief'),('Mouth focused',p['joy']<.5 and p['focus']>=.2),('Mouth open',p['joy']>=.5 or mode=='disbelief')]:
        ob=m[n];ob.scale=(1,1,1) if on else (.001,.001,.001);ob.keyframe_insert(data_path='scale',frame=frame)
    ob=a['shadow'];ob.location=(x+s*.15,y-.04,0);ob.scale=(s*(1+.15*jump),s,1);key(ob,frame)
    # Numbers face the viewer even when the pose is mirrored.
    a['number'].scale.x=d;a['number'].keyframe_insert(data_path='scale',frame=frame)
    return {'head':world(hp),'headtilt':d*p['headtilt'],'scale':s,'feet':[world(f[:2]) for f in p['feet']]}

def header_actor(t,f):
    rel=(t-22.5)
    jump=track(rel,[(-4,0),(-.62,0),(-.12,.76),(0,.81),(.25,.67),(.65,0),(3,0)])[0]
    return set_actor('Alisson',-.92,-2.52,.86,1,'header',rel,f,jump,2.0)

def header_contact():
    p=pose('header',0);h=p['hip'];a=p['tilt'];sh=(h[0]-.84*math.sin(a),h[1]+.84*math.cos(a));hp=(sh[0]-.02,sh[1]+.68)
    center=(-.92+.86*hp[0],-2.52+.86*hp[1]+.81)
    theta=math.radians(55);rot=p['headtilt'];ex=.57*.86*math.cos(theta);ey=.66*.86*math.sin(theta)
    edge=(ex*math.cos(rot)-ey*math.sin(rot),ex*math.sin(rot)+ey*math.cos(rot))
    nx=math.cos(theta)/.57;ny=math.sin(theta)/.66;nn=math.hypot(nx,ny);nx,ny=nx/nn,ny/nn
    normal=(nx*math.cos(rot)-ny*math.sin(rot),nx*math.sin(rot)+ny*math.cos(rot));r=.22+.024*.86
    return center, (center[0]+edge[0]+r*normal[0],center[1]+edge[1]+r*normal[1])
CONTACT=header_contact()[1]
# Locate a tangent to the real boot contour while the ball rests on the pitch.
boot=[(-.15+1.08*(.64+v.co.x),-3.65+1.08*(.12+v.co.y)) for v in template['Shoe_near'].data.vertices]
def boot_clearance(center):
    distances=[]
    for a,b in zip(boot,boot[1:]+boot[:1]):
        dx,dy=b[0]-a[0],b[1]-a[1];u=clamp(((center[0]-a[0])*dx+(center[1]-a[1])*dy)/(dx*dx+dy*dy))
        distances.append(math.hypot(center[0]-a[0]-u*dx,center[1]-a[1]-u*dy))
    return min(distances)-.0205*1.08-.22
lo,hi=.6,1.6
for _ in range(45):
    mid=(lo+hi)/2
    if boot_clearance((mid,-3.43))>0:hi=mid
    else:lo=mid
KICK_START=((lo+hi)/2,-3.43)
assert abs(boot_clearance(KICK_START))<1e-8

def ball_at(t):
    if t<17:return KICK_START
    if t<19:
        u=(t-17)/2;return (KICK_START[0]+4.0*u,KICK_START[1]+9*u-2*u*u)
    if t<=22.5:
        u=(t-19)/3.5
        # Ease into readable contact; incoming ball remains continuous within this shot.
        u=1-(1-u)**1.7
        return (mix(4.8,CONTACT[0],u),mix(3.45,CONTACT[1],u)+.45*math.sin(math.pi*u))
    if t<=24:
        u=(t-22.5)/1.5;return (mix(CONTACT[0],3.60,u),mix(CONTACT[1],.72,u)+.18*math.sin(math.pi*u))
    if t<25:
        u=t-24;return (3.60-.34*ease(u),.72-2.75*u+.55*u*u)
    u=min(t-25,2);return (3.26-.25*u,-1.48+.12*abs(math.sin(u*7))*math.exp(-u*2))

SAMPLES=[1,72,150,240,288,360,406,409,420,480,526,541,548,566,577,620,710,800,885,948]
contacts=[];footplants=[]
start=time.monotonic()
for f in range(1,FRAMES+1):
    t=(f-1)/FPS
    active={};groups=set();camx=0;camheight=16
    if t<4:
        groups.update(['home_goal','caption0','hero_name']);active['Alisson']=(0,-2.80,1.13,1,'ready',t,0,1)
        camheight=mix(14.8,14.3,ease(t/4));hero_name.location.x=0
    elif t<10:
        tt=t-4;x=tt*3.20;camx=x-.20;camheight=14.3
        groups.add('caption1');active['Alisson']=(x,-2.80,1.04,1,'run',tt/(2.56*1.04/3.20),0,1)
        if t<5:groups.add('home_goal')
    elif t<14:
        groups.update(['away_goal','caption2']);u=ease((t-10)/2)
        active['Alisson']=(-3.5+2.6*u,-2.55,.86,1,'run' if t<11.9 else 'ready',(t-10)*1.7,0,2)
    elif t<19:
        groups.update(['corner','caption3']);active['Trent']=(-.15,-3.65,1.08,1,'kick',t-17,0,1)
        camheight=15.0
    elif t<25:
        groups.update(['away_goal','caption4']);camx=.25;camheight=15.0;header_actor(t,f);active['Alisson']=None
    elif t<29:
        groups.update(['away_goal','caption5']);active['Alisson']=(-.12,-2.52,.86,1,'celebrate',t-25,0,2)
    elif t<36:
        groups.add('caption5');active['Alisson']=(.0,-2.62,1.08,1,'celebrate',t-29,0,2)
        for name,side,offset in [('Liverpool A',-1,0),('Liverpool B',1,.35)]:
            u=ease((t-29-offset)/2.8);x=side*mix(5,1.52,u)
            active[name]=(x,-2.50,.91,-side,'run' if u<.99 else 'celebrate',t*1.6+offset,0,1.5 if side==-1 else 2.3)
    else:
        groups.add('caption6');active['Alisson']=(0,-2.75,1.20,1,'celebrate',(t-36)*.5,0,2)
        for name,side in [('Liverpool A',-1),('Liverpool B',1)]:active[name]=(side*2.2,-2.60,.78,-side,'celebrate',t,0,1)
        camheight=mix(16,15.1,ease((t-36)/4))
    if 10<=t<14 or 19<=t<29:
        active['Johnstone']=(2.18,-1.60,.65,-1,'keeper' if t<23 else 'watch',t,0,-2)
        active['West Brom A']=(-2.45,-2.30,.70,1,'watch' if t<24 else 'disbelief',t,0,.2)
        active['West Brom B']=(.9,-2.1,.69,-1,'watch' if t<24 else 'disbelief',t+.7,0,.4)
        active['Liverpool A']=(-3.3,-1.5,.59,1,'ready' if t<24 else 'celebrate',t,0,-1)
    groups.add('score_tied' if t<24.13 else 'score_winner')
    for name,a in actors.items():
        visible(a['all'],name in active,f)
        if name in active and active[name] is not None:
            info=set_actor(name,*active[name][:6],f,*active[name][6:])
            if name=='Trent' and 16.6<=t<=17.4:footplants.append(info['feet'][0])
    for name,objs in GROUPS.items():visible(objs,name in groups or name=='impact' and 22.5<=t<22.73,f)
    camera.location=(camx,-.45,90);key(camera,f);camdata.ortho_scale=camheight;camdata.keyframe_insert(data_path='ortho_scale',frame=f)
    ui.location=(camx,-.45,0);ui.scale=(camheight/16,camheight/16,1);key(ui,f)
    bar.scale.x=7.70*(f/FRAMES);bar.keyframe_insert(data_path='scale',frame=f)
    showball=14<=t<29
    visible(ballobjects,showball,f)
    bp=ball_at(t);ball.location=(*bp,4.0);ball.rotation_euler.z=-(t-17)*4.0 if t>17 else .2;key(ball,f)
    for i,ob in enumerate(trail):
        on=17<t<18.95 or 22.55<t<24
        visible([ob],on,f)
        b=ball_at(t-.035*(i+1));ob.location=(*b,4.0-.015*(i+1));key(ob,f)
    impactroot.location=(*CONTACT,5);amount=max(0,1-(t-22.5)/.23);impactroot.scale=(amount,amount,1);key(impactroot,f)
    # Net moves only after the ball reaches it.
    ripple=0 if t<24 else .10*math.sin((t-24)*24)*math.exp(-(t-24)*3.2)
    for ob,pts in netlines:
        if ob in GROUPS['away_goal']:
            ob.location.x=ripple;ob.keyframe_insert(data_path='location',frame=f)
    if f==541:contacts.append({'frame':f,'seconds':t,'kind':'header','ball_center':bp,'head_center':header_contact()[0],'contact_design':'Ball tangent to the upper forehead at the direction change.'})
    if f==409:contacts.append({'frame':f,'seconds':t,'kind':'corner kick','ball_center':bp,'boot_surface_gap':boot_clearance(bp),'contact_design':'Right boot contour tangent to the stationary ball before release; ball rests on the pitch.'})
    if f%120==0:print('BAKED',f,'/',FRAMES,flush=True)

# Dense authored samples use linear interpolation; visibility switches must stay discrete.
for action in bpy.data.actions:
    for slot in action.slots:
        for layer in action.layers:
            for strip in layer.strips:
                bag=strip.channelbag(slot)
                if bag:
                    for fc in bag.fcurves:
                        for k in fc.keyframe_points:k.interpolation='CONSTANT' if 'hide_' in fc.data_path else 'LINEAR'
for seconds,title in [(0,'Late clock'),(4,'Keeper goes forward'),(10,'Into the box'),(14,'Corner'),(17,'Boot contact'),(19,'Find the header'),(22.5,'Forehead contact'),(24,'Into the net'),(29,'Teammates'),(36,'Alisson Becker')]:scene.timeline_markers.new(title,frame=round(seconds*FPS)+1)
scene['Story']='Condensed original stick-figure reconstruction of Alisson\'s winner: West Brom 1-2 Liverpool, 16 May 2021. No narration or broadcast assets.'
scene['Source character']=str(SOURCE.relative_to(ROOT.parent.parent))
scene['Source URL']='https://www.liverpoolfc.com/news/first-team/434274-alisson-becker-west-brom-premier-league-match-report'
scene.frame_set(541);bpy.context.view_layer.update()
valid_drivers=0
for a in actors.values():
    for ob in a['m'].values():
        if ob.data and ob.data.animation_data:
            for fc in ob.data.animation_data.drivers:
                assert fc.driver.is_valid,(ob.name,fc.data_path);valid_drivers+=1
assert valid_drivers==48*len(actors),valid_drivers
assert max(math.dist(p,footplants[0]) for p in footplants)<1e-8
assert math.dist(ball_at(22.5),CONTACT)<1e-9
assert max(math.dist(ball_at(t/24),ball_at((t+1)/24)) for t in range(576,648))<.16
assert abs(ball_at(27)[1]-.22-(-1.7))<.003
assert math.dist(ball_at(22.5-1e-6),ball_at(22.5+1e-6))<1e-4
# Check evaluated endpoint geometry against the live remapped control.
for name in ('Alisson','Trent'):
    a=actors[name]['m'];ob=a['Arm_near'].evaluated_get(bpy.context.evaluated_depsgraph_get());tip=ob.data.splines[0].bezier_points[1].co
    assert math.dist(tip[:2],a['CTRL_Hand_near'].matrix_world.translation[:2])<1e-4
checks={'duration':SECONDS,'fps':FPS,'frames':FRAMES,'resolution':[1080,1920],'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'actors':len(actors),'valid_original_limb_drivers':valid_drivers,'corner_support_foot_max_drift':max(math.dist(p,footplants[0]) for p in footplants),'contacts':contacts,'bake_seconds':time.monotonic()-start,'limits':'Spatial staging and slow motion are authored. Technical contact checks do not establish audience comprehension or creative acceptance.'}
(OUT/'build-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
# Purge only unused data in this isolated process. Original files and open Blender remain untouched.
for sc in list(bpy.data.scenes):
    if sc!=scene:bpy.data.scenes.remove(sc)
for ob in template.values():
    if not ob.users_collection:bpy.data.objects.remove(ob)
bpy.ops.file.pack_all()
scene.render.filepath='//stills/'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'alisson-winner.blend'))
print('SAVED',flush=True)
if '--samples' in sys.argv:
    for f in SAMPLES:
        scene.frame_set(f);scene.render.filepath=str(OUT/f'stills/frame-{f:04}.png');bpy.ops.render.render(write_still=True)
if '--render' in sys.argv:
    exec(compile(Path(__file__).with_name('render_film.py').read_text(),str(Path(__file__).with_name('render_film.py')),'exec'))
