"""Video003 rough composition layouts, executed in the visible Blender instance.

Native curves/meshes, no imported picture cards. These layouts are NOT finished
character art, acting, contact proof or a combined animatic.
Primitive drawing functions copied from the inspected Video002 board builder;
no old film builder is executed/imported. Only new S003 scenes are written.
"""
import bpy, math, json
from pathlib import Path
ROOT = Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/003-barca-emergency-meeting')
OUT = ROOT / 'artifacts/staging-v001/layouts'
INK, PAPER, RED, WHITE = '#252b38', '#f5edda', '#a52d44', '#fffcf3'
GREEN, GOLD, BLUE, SKIN = '#659477', '#edbd60', '#7296b0', '#dbb89c'
MATS = {}
SCENE = None
def material(color):
    if color not in MATS:
        m = bpy.data.materials.new('S003_' + color)
        rgb = [int(color[i:i+2], 16)/255 for i in (1,3,5)]
        m.diffuse_color = tuple(v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in rgb) + (1,)
        MATS[color] = m
    return MATS[color]

def obj(name, data, color):
    o = bpy.data.objects.new(SCENE.name + '_' + name, data)
    SCENE.collection.objects.link(o)
    data.materials.append(material(color))
    return o

def poly(name, pts, color, z=0):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([(x,y,z) for x,y in pts], [], [list(range(len(pts)))])
    return obj(name, mesh, color)

def rect(name, x, y, w, h, color, z=0):
    return poly(name, [(x,y),(x+w,y),(x+w,y+h),(x,y+h)], color, z)

def line(name, pts, color=INK, width=.045, z=.5):
    c = bpy.data.curves.new(name, 'CURVE')
    c.dimensions = '3D'
    c.bevel_depth = width
    c.bevel_resolution = 2
    p = c.splines.new('POLY')
    p.points.add(len(pts)-1)
    for v,(x,y) in zip(p.points,pts):
        v.co = (x,y,z,1)
    return obj(name,c,color)

def disc(name, x, y, r, color, z=.6):
    return poly(name,[(x+r*math.cos(i*math.tau/40),y+r*math.sin(i*math.tau/40)) for i in range(40)],color,z)

def text(body, x, y, size=.35, color=INK, z=2):
    c=bpy.data.curves.new('label','FONT'); c.body=body; c.size=size
    o=obj('label',c,color); o.location=(x,y,z)
    return o

def scene(name, bg=PAPER):
    global SCENE
    existing=bpy.data.scenes.get(name)
    assert not existing or len(existing.objects)==0, 'Do not overwrite authored boards'
    SCENE=existing or bpy.data.scenes.new(name)
    SCENE.render.engine='BLENDER_WORKBENCH'
    SCENE.render.resolution_x=1280; SCENE.render.resolution_y=720; SCENE.render.resolution_percentage=100
    SCENE.render.image_settings.file_format='PNG'
    shading=SCENE.display.shading
    shading.light='FLAT'; shading.color_type='MATERIAL'; shading.show_shadows=False
    shading.show_cavity=False; shading.show_specular_highlight=False
    shading.background_type='WORLD'
    SCENE.world=bpy.data.worlds.new(name+'_world'); SCENE.world.color=(.1,.1,.1)
    SCENE.view_settings.view_transform='Standard'
    cam=bpy.data.cameras.new(name+'_camera'); cam.type='ORTHO'; cam.ortho_scale=16
    o=bpy.data.objects.new(name+'_camera',cam); SCENE.collection.objects.link(o); o.location=(0,0,25)
    SCENE.camera=o
    rect('paper',-8,-4.5,16,9,bg,-1)
    if bpy.context.window:
        bpy.context.window.scene=SCENE
        for area in bpy.context.screen.areas:
            if area.type=='VIEW_3D': area.spaces.active.region_3d.view_perspective='CAMERA'
    return SCENE

def ellipse(name,x,y,rx,ry,color,z=.6):
    return poly(name,[(x+rx*math.cos(i*math.tau/40),y+ry*math.sin(i*math.tau/40)) for i in range(40)],color,z)

def person(name,x,y,s=1,color=BLUE,face=1,pose='listen',mood='neutral',seated=False):
    # ponytail: shot-specific rough silhouettes only; final likeness and motion need constructed assets.
    def p(a,b):return x+a*s,y+b*s
    body=[(-.38,1.5),(-.40,2.4),(.38,2.4),(.40,1.5)]
    if pose=='lean':body=[(-.30,1.5),(-.06,2.42),(.66,2.42),(.42,1.5)]
    poly(name+'_body',[p(*q) for q in body],color,.7)
    neckx=.25 if pose=='lean' else 0
    line(name+'_neck',[p(neckx,2.35),p(neckx,2.73)],SKIN,.13*s,.72)
    headx=neckx
    ellipse(name+'_face',*p(headx,2.98),.39*s,.48*s,SKIN,.9)
    line(name+'_nose',[p(headx+face*.25,3.06),p(headx+face*.45,2.93),p(headx+face*.25,2.9)],INK,.025*s,1.1)
    eyex=headx+face*.17
    disc(name+'_eye',*p(eyex,3.08),.055*s,INK,1.1)
    slope=.13 if mood=='worry' else (-.10 if mood=='confident' else 0)
    line(name+'_brow',[p(eyex-.14,3.27+slope),p(eyex+.12,3.27)],INK,.035*s,1.1)
    if mood=='shock':ellipse(name+'_mouth',*p(headx+face*.12,2.76),.1*s,.13*s,INK,1.1)
    elif mood=='smile':line(name+'_mouth',[p(headx-.14,2.8),p(headx,2.7),p(headx+.2,2.8)],INK,.028*s,1.1)
    else:line(name+'_mouth',[p(headx-.08,2.78),p(headx+.17,2.78)],INK,.024*s,1.1)
    if name.lower().startswith('perez'):
        for a in [-.14,.14]:line(name+'_glasses',[p(headx+a-.09,3.17),p(headx+a+.09,3.17),p(headx+a+.09,3.0),p(headx+a-.09,3.0),p(headx+a-.09,3.17)],INK,.025*s,1.15)
        poly(name+'_tie',[p(-.06,2.34),p(.06,2.34),p(.12,1.8),p(0,1.7),p(-.12,1.8)],GOLD,1)
        line(name+'_hair',[p(headx-.35,3.24),p(headx-.18,3.4),p(headx+.18,3.4)],'#a7a59b',.09*s,1.04)
    else:
        line(name+'_hair',[p(headx-.35,3.18),p(headx-.22,3.4),p(headx+.2,3.4),p(headx+.34,3.23)],INK,.085*s,1.04)
    arms={'listen': [[(-.37,2.3),(-.62,1.94),(-.28,1.7)],[(.37,2.3),(.65,1.87),(.61,1.46)]],
          'point':[[(-.37,2.3),(-.65,1.9),(-.5,1.55)],[(.37,2.3),(.92,2.18),(1.5,2.48)]],
          'shrug':[[(-.37,2.3),(-.77,1.91),(-1.05,2.22)],[(.37,2.3),(.85,1.94),(1.13,2.26)]],
          'push':[[(-.37,2.3),(.07,2.05),(.96,2.25)],[(.37,2.3),(.72,2.12),(.98,2.55)]],
          'lean':[[(-.18,2.3),(.07,1.98),(.6,1.78)],[(.57,2.3),(.93,1.99),(1.1,1.83)]],
          'phone':[[(-.37,2.3),(-.74,2.12),(-.57,2.98)],[(.37,2.3),(.8,1.75),(.65,1.6)]],
          'celebrate':[[(-.37,2.3),(-.76,2.7),(-.8,3.47)],[(.37,2.3),(.76,2.7),(.8,3.47)]],
          'kick':[[(-.37,2.3),(-.85,2.05),(-1.1,2.3)],[(.37,2.3),(.7,2.2),(.94,1.78)]]}
    for i,chain in enumerate(arms[pose]):
        line(name+'_arm_'+str(i),[p(*q) for q in chain],INK,.1*s,.81)
        disc(name+'_hand_'+str(i),*p(*chain[-1]),.13*s,SKIN,1.3)
    if seated:
        legs=[[(-.2,1.5),(-.6,.88),(-.36,.12)],[(.2,1.5),(.63,.95),(.8,.1)]]
    elif pose=='kick':legs=[[(-.18,1.5),(-.30,.7),(-.18,.12)],[(.18,1.5),(.68,.75),(1.30,.9)]]
    elif pose=='push':legs=[[(-.18,1.5),(-.56,.70),(-.96,.12)],[(.18,1.5),(.63,.82),(.52,.12)]]
    else:legs=[[(-.18,1.5),(-.28,.73),(-.40,.12)],[(.18,1.5),(.27,.73),(.39,.12)]]
    for i,chain in enumerate(legs):
        line(name+'_leg_'+str(i),[p(*q) for q in chain],INK,.11*s,.66)
        a,b=chain[-1];ellipse(name+'_shoe_'+str(i),*p(a+.08,b),.23*s,.10*s,INK,.75)
    return text(name.upper(),x-.62*s,y-.36*s,.20*s,INK,2)

def arrow(points,color=GOLD):
    line('attention/action arrow',points,color,.045,2)
    a,b=points[-2:];ang=math.atan2(b[1]-a[1],b[0]-a[0])
    for d in [-.5,.5]:line('arrow head',[b,(b[0]-.3*math.cos(ang+d),b[1]-.3*math.sin(ang+d))],color,.04,2)

def label(top,bottom):
    rect('review header',-8,3.73,16,.77,INK,3)
    text(top,-7.64,4.02,.27,WHITE,3.1)
    rect('review footer',-8,-4.5,16,.57,PAPER,3)
    text(bottom,-7.65,-4.27,.22,INK,3.1)

def room():
    rect('wall',-8,-1,16,5,PAPER,-.9)
    poly('floor',[(-8,-4.5),(8,-4.5),(8,-.8),(-8,-.8)],'#bcb2a0',-.8)
    rect('door left',-7.45,-.7,2.05,3.6,'#737b82',-.3)
    rect('curtained window',-4.85,.55,2.1,2.5,INK,-.2)
    rect('call screen',-2.0,.15,4.2,2.6,INK,-.2)
    rect('call screen glass',-1.88,.29,3.96,2.32,'#7797a5',-.1)
    rect('plan board',3.6,.0,3.9,3.35,WHITE,-.2)
    text('HOW TO BEAT',3.86,2.65,.27)
    text('BARCELONA',3.9,2.21,.38)
    rect('archive',-7.3,-2.6,1.8,1.1,'#8d7060',.1);text('ARCHIVE',-7.13,-2.1,.23,WHITE)
    poly('table',[(-4.8,-3.55),(3.7,-3.55),(2.2,-1.6),(-3.55,-1.6)],'#957967',1.5)

def field():
    rect('sky',-8,.25,16,4.25,'#c9dce1',-.9)
    rect('turf',-8,-4.5,16,4.9,GREEN,-.8)
    for x in [-6,-2,2,6]:poly('mow strip',[(x-2,-4.5),(x,-4.5),(x+2,.4),(x+1,.4)],'#719e7d',-.75)
    rect('perimeter',-8,.2,16,.55,'#233c58',-.6)
    text('BARCA TRAINING  /  GOAL FACTORY',-7.3,.4,.22,WHITE,-.5)
    line('penalty box',[(-.2,-3.4),(7.6,-3.4),(7.6,.2)],WHITE,.035,-.5)
    # Same rough perspective and readable goal depth; not a mechanics proof.
    poly('back net',[(4.7,.1),(7.6,.1),(7.1,2.2),(4.3,2.2)],'#8eb4a4',-.3)
    line('goal front',[(3.6,-.7),(3.6,2.55),(7.35,2.55),(7.35,-.7)],WHITE,.075,-.1)
    for k in range(1,8):
        x=3.6+k*3.75/8;line('net',[(x,-.7),(x,2.55)],'#e8eadb',.012,-.15)
    line('goal depth',[(3.6,2.55),(4.3,2.2),(7.1,2.2),(7.35,2.55)],WHITE,.035,0)
    line('return belt',[(-7.4,-3.65),(7,-3.65)],'#37414c',.15,-.2)
    for x in [-7,-6.1,-5.2]:disc('returned ball',x,-3.45,.16,WHITE,-.1)

def build(group):
    made=[]
    def new(name,bg=PAPER):made.append(scene(name,bg));return made[-1]
    if group==1:
        new('S003_L01_score_reveal',GREEN)
        rect('stands',-8,.3,16,4,BLUE,-.7)
        rect('score box',-3.4,1.7,7.2,1.7,INK,.3)
        text('BARCELONA 7 - 2 RACING',-2.95,2.6,.40,WHITE)
        text('FULL TIME',-1.15,2.03,.30,GOLD)
        person('Racing keeper',-4,-3.0,1.05,GOLD,pose='celebrate',mood='smile')
        person('Racing',0,-3.0,.95,BLUE,pose='celebrate',mood='smile')
        person('Racing',3.45,-3.0,.75,BLUE,pose='shrug',mood='smile',seated=True)
        label('S01  /  RELIEF IS MISREAD AS VICTORY','Rough composition only. Pull back reveals the losing score after the whistle.')

        new('S003_L02_meeting_entry');room()
        # Cupboard blocks the same established door, not the archive.
        rect('door cupboard',-6.4,-1.6,2.05,1.7,'#927057',.35)
        person('Perez',-7.0,-2.1,.88,INK,pose='push',mood='confident')
        person('Valencia',-2.5,-2.02,.75,WHITE,face=-1,pose='lean',mood='worry',seated=True)
        person('Sevilla',1,-1.9,.75,RED,face=-1,mood='neutral',seated=True)
        text('7 - 2',-4.5,2.8,.35,RED);text('0 - 5',-4.5,2.2,.35,RED);text('1 - 3',-4.5,1.6,.35,RED)
        arrow([(-7.3,-.8),(-6.35,-.8)])
        label('S03  /  PEREZ SAYS CALM, HIS ACTION SAYS PANIC','Door left; screen centre; board right. Preserve this geography for the ending.')

        new('S003_L03_listening_reversal')
        rect('wall',-8,-4.5,16,9,'#dcd2bb',-.7)
        person('Sevilla',-3.3,-3.1,1.7,RED,pose='shrug',mood='neutral')
        person('Perez',2.5,-3.0,1.65,INK,face=-1,pose='lean',mood='smile')
        text('They only scored three.',-6.7,3.02,.38)
        text('Hope -> answer -> smile dies',.7,-3.7,.29)
        label('S04  /  TWO DIFFERENT ATTITUDES','Key-pose layout, not performance proof. Listener expression must change after the answer.')

        new('S003_L04_failed_plan');field()
        person('Raphinha',-4.7,-2.85,.98,RED,pose='point',mood='smile')
        for i,x in enumerate([-6.1,-5.1,-3.8]):person('D'+str(i+1),x,-2.3,.70,BLUE,face=-1,pose='listen')
        person('Pedri',-1.7,-2.7,.78,RED,pose='kick')
        person('Yamal',2,-2.55,.79,RED,pose='kick',mood='smile')
        disc('ball',-.63,-1.99,.15,WHITE,1.3)
        arrow([(-.5,-2),(1.4,-2),(2.8,-1.5),(4.4,.0)])
        label('S05-S06  /  THE EMPTY CHANNEL','Spatial sketch: defenders cluster on Raphinha; Pedri finds Yamal. Ball contacts still untested.')
    elif group==2:
        new('S003_L05_flick_response');field()
        person('Assistant',-4.2,-2.7,1.32,BLUE,pose='point',mood='smile')
        person('Flick',1.0,-2.9,1.40,INK,face=-1,pose='listen')
        rect('clipboard',.48,-.2,.75,1.1,PAPER,1.6)
        text('7',.69,.09,.6)
        text('Can we have a break?',4.1,-2.25,.29,WHITE)
        label('S07  /  EXPECTATION MEETS A CALM ANSWER','Flick reads before looking up. Assistant smile drops. Keeper remains offscreen.')

        new('S003_L06_bayern_call');room()
        rect('call closeup surround',-5.9,-2.9,8.9,6.4,INK,1.6)
        rect('call closeup',-5.62,-2.63,8.32,5.89,'#b79b78',1.7)
        # Separate call portrait composed in front of the screen, all editable geometry.
        before=set(SCENE.objects)
        person('Muller',-1.3,-2.3,1.48,RED,face=-1,pose='shrug',mood='smile')
        for o in set(SCENE.objects)-before:o.location.z+=2
        rect('2020 frame',-5.2,.8,2.4,1.5,PAPER,3.2);text('8 - 2',-4.77,1.57,.61,INK,3.3);text('2020',-4.42,1.08,.28,INK,3.3)
        before=set(SCENE.objects);person('Perez',5,-3.15,1.45,INK,face=-1,pose='lean',mood='confident')
        for o in set(SCENE.objects)-before:o.location.z+=2
        label('S08  /  MULLER REMEMBERS EIGHT GOALS','Call screen and reaction share a clear eye-line. Smugness must visibly collapse on Flick\'s name.')

        new('S003_L07_transfer');field()
        person('Flick',-2.4,-2.9,1.65,INK,pose='phone')
        line('handset',[(-3.43,2.4),(-3.43,1.45)],INK,.12,2.0)
        person('Raphinha',3.3,-2.7,1.16,RED,pose='lean',mood='smile')
        rect('delivery box',3.1,-2.85,3,1.55,GOLD,1.4)
        text('REAL MADRID',3.36,-2.24,.30,INK,1.5)
        disc('packing ball',4.75,-.47,.23,WHITE,1.5)
        label('S14  /  THE RESCUE CALL REACHES THE PROBLEM','Grip and release need authored hand drawings. Raphinha packs; Flick stays matter-of-fact.')

        new('S003_L08_support_group');room()
        rect('moved cupboard',-5.0,-1.8,1.3,1.55,'#927057',.35)
        rect('board correction',3.81,2.5,3.5,.48,WHITE,.4)
        text('HOW TO SURVIVE',3.90,2.68,.27,RED,.6)
        person('Keeper',-6.35,-2.6,.94,GOLD,pose='listen',mood='worry')
        person('Perez',3.1,-2.65,.93,INK,face=-1,pose='listen',seated=True)
        person('Racing',-.6,-1.8,.82,BLUE,face=-1,pose='point',mood='neutral',seated=True)
        line('offered chair',[(-3.8,-2.9),(-3.8,-1.2),(-2.7,-1.2),(-2.7,-2.9)],INK,.08,1.9)
        line('chair seat',[(-3.8,-2.03),(-2.7,-2.03)],INK,.12,2)
        label('S16  /  THEY MAKE ROOM FOR THEIR OPPONENT','Same room, door reopened, cupboard moved. The chair offer completes the final joke.')
    else:raise ValueError('Choose group 1 or 2')
    for s in made:
        s['purpose']='Rough composition only; not approved art or motion evidence'
        s.render.resolution_x=960;s.render.resolution_y=540
    return [s.name for s in made]

def save_layouts():
    target=OUT/'layouts.blend'
    assert not target.exists(), 'Use a versioned output; do not overwrite the selected source'
    scenes={s for s in bpy.data.scenes if s.name.startswith('S003_L')}
    assert len(scenes)==8
    bpy.data.libraries.write(str(target),scenes,path_remap='RELATIVE_ALL',fake_user=True,compress=True)
    return {'native':str(target),'scenes':[s.name for s in sorted(scenes,key=lambda s:s.name)]}
