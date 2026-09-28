"""Film-specific composition thumbnails. Execute in the live Blender connection.

These editable shapes test framing, not character design or animation quality.
"""
import bpy
import math
from pathlib import Path

ROOT = Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/002-how-arsenal-won-the-league')
OUT = ROOT / 'artifacts/preproduction-v001/boards'
INK, PAPER, RED, WHITE = '#202a33', '#ece7db', '#ce3843', '#fffaf0'
GREEN, GOLD, BLUE, SKIN = '#7e9a81', '#ddaf4e', '#81acbd', '#ddb999'
MATS = {}
SCENE = None

def material(color):
    if color not in MATS:
        m = bpy.data.materials.new('S002_' + color)
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

def actor(name, x, y, s=1, shirt=RED, pose='stand', facing=1, shadow=False):
    # ponytail: independent rough poses, not a reusable rig; replace with reviewed cast assets for motion.
    def pt(a,b): return (x+facing*a*s,y+b*s)
    dark=INK
    skin=dark if shadow else SKIN
    jersey=dark if shadow else shirt
    if pose in ('run','carry'):
        legs=[[(0,1.12),(-.48,.55),(-.85,.5)],[(0,1.12),(.48,.65),(.12,0)]]
        arms=[[(-.2,2),(-.62,1.55),(-.25,1.4)],[(.2,2),(.65,2.15),(.85,2.65)]]
        if pose=='carry':
            arms=[[(-.25,2),(-.55,2.5),(-.55,3.4)],[(.25,2),(.55,2.5),(.55,3.4)]]
    elif pose=='shrug':
        legs=[[(-.18,1.1),(-.25,.5),(-.3,0)],[(.18,1.1),(.25,.5),(.32,0)]]
        arms=[[(-.25,2),(-.65,1.65),(-.95,2.05)],[(.25,2),(.65,1.65),(.95,2.05)]]
    else:
        legs=[[(-.18,1.1),(-.22,.5),(-.35,0)],[(.18,1.1),(.22,.5),(.4,0)]]
        arms=[[(-.25,2),(-.52,1.55),(-.42,1.1)],[(.25,2),(.52,1.55),(.42,1.1)]]
    for i,path in enumerate(legs+arms): line(name+str(i),[pt(*p) for p in path],dark,.08*s,.6)
    poly(name+'_shirt',[pt(-.3,2.12),pt(.3,2.12),pt(.38,1.1),pt(-.38,1.1)],jersey,.75)
    rect(name+'_neck',x-.11*s,y+2.0*s,.22*s,.4*s,skin,.8)
    disc(name+'_head',x,y+2.65*s,.47*s,dark,.9)
    disc(name+'_face',x,y+2.65*s,.41*s,skin,1)
    if not shadow:
        line(name+'_brow',[pt(.0,2.79),pt(.29,2.76)],dark,.028*s,1.15)
        disc(name+'_eye',*pt(.22,2.68),.032*s,dark,1.2)
        line(name+'_mouth',[pt(.09,2.48),pt(.29,2.48)],dark,.022*s,1.2)

def goal(x=-6.8, y=-1.4, w=13.6, h=4.3):
    rect('net',x,y,w,h,'#b4c4b4',.1)
    for i in range(1,18):
        xx=x+w*i/18; line('net_vertical',[(xx,y),(xx,y+h)],'#8b9f90',.012,.2)
    for i in range(1,6):
        yy=y+h*i/6; line('net_horizontal',[(x,yy),(x+w,yy)],'#8b9f90',.012,.2)
    line('goalposts',[(x,y),(x,y+h),(x+w,y+h),(x+w,y)],WHITE,.09,.3)

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

def build(group):
    if group==1:
        scene('S002_01_shadow','#17232e')
        poly('tv_spill',[(-6,2),(-1,3),(3,-4),(-6,-2)],'#314855',-.5)
        rect('tv',-6.5,-.5,4.1,2.8,INK,.1); rect('screen',-6.25,-.25,3.6,2.3,GREEN,.2)
        line('pitch',[(-6,-.05),(-3,-.05),(-3,1.8),(-6,1.8),(-6,-.05)],WHITE,.02,.3)
        actor('anonymous',2,-3,1.45,shadow=True)
        rect('chair',.55,-3.7,3,3.2,'#101921',1.2)
        rect('desk',3.4,-1.7,3.8,.2,'#627780',1.3)
        line('lamp_off',[(5,-1.5),(5,.7),(4.2,.7)],INK,.09,1.4)
        poly('shade',[(3.8,.4),(4.7,.4),(4.45,1),(4.1,1)],INK,1.4)

        scene('S002_02_flag')
        rect('ground',-8,-4.5,16,3.9,'#c4c2ac',-.5)
        poly('carpet',[(-7,-4),(1.8,-4),(5.6,-.9),(3.7,-.9)],RED,0)
        actor('gyokeres',-4,-2.6,1.35,RED,'shrug')
        actor('arteta',1.1,-2.2,1.1,INK)
        line('flagpole',[(5,-1),(5,3)],INK,.05,.5)
        poly('flag',[(5,3),(6.4,2.5),(5,2.2)],RED,.6)
        poly('number_nine_shirt',[(4.4,1.9),(5.6,1.9),(6,1.3),(5.55,1.05),(5.45,-.2),(4.55,-.2),(4.45,1.05),(4,1.3)],RED,.8)
        text('9',4.73,.5,.85,WHITE)
        text('GYOKERES',-5,-3.55,.3); text('ARTETA',.4,-3.05,.3)

        scene('S002_03_wall',GREEN)
        goal()
        for i in range(9): actor('wall_%02d'%(i+1),-5.8+i*1.45,-1.15,.96,RED)
        actor('raya',0,-3.65,1.05,GOLD,'shrug')
        text('RAYA',-.52,-4.12,.3)
        text('1 - 0',5.2,3.45,.55,WHITE)

        scene('S002_04_isolation',GREEN)
        line('touchline',[(-7.4,-3.5),(7.4,-3.5),(7.4,3.5),(-7.4,3.5),(-7.4,-3.5)],WHITE,.035,.1)
        line('halfway',[(.5,-3.5),(.5,3.5)],WHITE,.025,.1)
        line('circle',[(.5+1.5*math.cos(i*math.tau/60),1.5*math.sin(i*math.tau/60)) for i in range(61)],WHITE,.025,.1)
        goal(-7,.3,4,1.65)
        for i in range(9): actor('wall_%02d'%(i+1),-6.75+i*.43,.3,.31,RED)
        actor('raya',-5,-.8,.42,GOLD)
        actor('gyokeres',5,-2,1.05,RED,'shrug',-1)
        text('GYOKERES',4.0,-2.65,.32)
    elif group==2:
        scene('S002_05_chase','#e0e5df')
        rect('road',-8,-4.5,16,2.5,'#b7b7a7',-.4)
        for x in [-7,-3,1,5]: rect('road_mark',x,-3.5,2,.07,PAPER,0)
        line('may_post',[(6,-2),(6,2.9)],INK,.045)
        rect('may',5.2,2,2.1,.8,GOLD,.6); text('MAY',5.6,2.23,.4)
        actor('pep',-5.5,-2.4,1.1,INK)
        actor('gabriel',-.5,-2.4,.9,RED,'carry')
        actor('saliba',1.3,-2.4,.9,RED,'carry')
        actor('gyokeres',3,-2.4,.9,RED,'carry')
        actor('arteta',5,-2.25,1,INK,'run')
        rect('podium',-1.5,.65,5.4,1.5,GOLD,1.5); text('1st',.15,.9,1,INK,1.7)
        for x in [-1,1,3]: line('speed',[(x-1.2,-.8),(x-.65,-.8)],INK,.03)
        text('PEP',-6.1,-3.05,.35); text('ARTETA',4.3,-3.05,.35)

        scene('S002_06_hotline')
        rect('desk',-8,-2.4,16,2.2,'#b8a991',.1)
        actor('operator',1,-2.5,1.5,BLUE)
        rect('pending',-6.9,-1.8,4.3,.65,'#969a97',1.6)
        text('PENDING',-6.4,-1.58,.36,WHITE,1.8)
        line('grey_phone',[(-6.2,-.65),(-5.9,-.35),(-4.2,-.35),(-3.9,-.65)],'#666e74',.2,1.9)
        rect('gold_base',3.7,-1.35,2.7,.5,GOLD,1.7)
        line('gold_receiver',[(3.9,-.4),(4.1,-.1),(5.9,-.1),(6.1,-.4)],GOLD,.22,1.8)
        text('MIKEL',4.25,-1.03,.4,INK,2)
        for x in [3.1,6.7]: line('ring',[(x,.1),(x,.8)],GOLD,.055,1.8)
        rect('button',-.8,-1.8,2.3,.6,RED,1.7); text('PLAY ON',-.55,-1.62,.32,WHITE,2)

        scene('S002_07_winner',GREEN)
        goal(4.3,-2.4,3,4.9)
        actor('keeper',5.3,-2.1,1.1,GOLD,'run',-1)
        actor('defender',-2.8,-1.7,.85,BLUE)
        actor('gabriel',-4.5,-.5,1.0,RED,'shrug')
        actor('gyokeres',1,-2.1,1.08,RED,'shrug',-1)
        text('GABRIEL',-5.6,-1.5,.29); text('GYOKERES',-.25,-2.8,.29)
        disc('ball_contact',1.46,-.65,.21,WHITE,2)
        for pts in [[(-7,2.8),(-5,3.45),(-2.8,2.8),(-.4,1.0),(1.45,-.65)],[(1.45,-.65),(3,-1),(4.8,-1.35),(6.2,-1.45)]]:
            line('planned_ball_path',pts,GOLD,.048,1.8)
        for i in range(7):
            a=i*math.tau/7; line('contact',[(1.46+.3*math.cos(a),-.65+.3*math.sin(a)),(1.46+.55*math.cos(a),-.65+.55*math.sin(a))],WHITE,.03,2)

        scene('S002_08_reveal','#17232e')
        poly('lamp_pool',[(4,1.7),(1.4,3.3),(-2.3,2.5),(-3.5,-3.9),(4.5,-3.9)],'#877c61',-.5)
        rect('chair_back',-2.1,-4.5,4.2,4.4,'#101921',.3)
        actor('identity_placeholder',0,-6,3,INK)
        rect('desk',-6,-2.4,12,.25,'#a7987c',1.3)
        line('lamp_on',[(4,-2.15),(4,1.2),(3.3,1.5)],INK,.09,1.4)
        poly('shade',[(2.7,1.2),(4,1.2),(3.65,2),(3.1,2)],GOLD,1.5)
        poly('crumpled_notes',[(-3,-2.1),(-3.2,-1.8),(-2.8,-1.4),(-2.2,-1.6),(-2,-2.1)],PAPER,1.6)
    else:
        raise ValueError(group)
    bpy.context.view_layer.update()
    return [s.name for s in bpy.data.scenes if s.name.startswith('S002_')]

def save():
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/'composition-boards-v001.blend'
    assert not path.exists(), 'Preserve existing saved revision'
    boards=[s for s in bpy.data.scenes if s.name.startswith('S002_')]
    assert len(boards)==8
    wall=bpy.data.scenes['S002_03_wall']
    assert len([o for o in wall.objects if o.name.endswith('_head') and o.name.startswith('S002_03_wall_wall_')])==9
    for s in boards:
        assert s.camera and s.render.resolution_x*9==s.render.resolution_y*16
    bpy.ops.wm.save_as_mainfile(filepath=str(path))
    return str(path)
