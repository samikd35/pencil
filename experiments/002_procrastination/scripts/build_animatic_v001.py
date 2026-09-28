"""Reuse the delivered Blender character for an authored, held-pose story edit.

Run with Blender --background --python-exit-code 1 --python this_file -- --render.
The full edit stays editable; rendering one image per pose avoids 4,320 redundant renders.
"""
import json
import math
from pathlib import Path
import sys
import bpy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/animatic-v001'
SOURCE = ROOT.parent / '001_heavy_box/artifacts/finish-v002/character-and-effects.blend'
FPS = 24
INK, PAPER, TEAL, GOLD, CORAL = '#25394c', '#fff9ed', '#45aaa8', '#efbc61', '#e88a70'
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'panels').mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene = bpy.context.scene
scene.frame_set(1)
scene.sequence_editor_clear()
scene.render.use_compositing = False
scene.render.use_sequencer = False

# Keep the actual character geometry, materials, parenting and limb drivers.
keep = {'Bean torso', 'Head', 'Head_outline', 'Eye_0', 'Eye_1', 'Brow_0', 'Brow_1',
        'Mouth', 'Mouth open', 'CTRL_Body', 'CTRL_Head', 'ANCHOR_Shoulder', 'Fixed camera'}
for side in ('far', 'near'):
    keep.update({f'{part}_{side}' for part in ('Mitten', 'Shoe', 'Arm', 'Leg')})
    keep.update({f'{part}_{side}_outline' for part in ('Mitten', 'Shoe')})
    keep.update({f'CTRL_{part}_{side}' for part in ('Hand', 'Foot', 'Elbow', 'Knee')})
for obj in list(bpy.data.objects):
    if obj.name not in keep:
        bpy.data.objects.remove(obj, do_unlink=True)
for obj in list(bpy.data.objects):
    obj.animation_data_clear()
    if obj.data and obj.data.animation_data:
        obj.data.animation_data.action = None  # Retain the curve endpoint drivers.
for material in bpy.data.materials:
    if material.node_tree:
        material.node_tree.animation_data_clear()
scene.timeline_markers.clear()
scene.name = 'Just One Thing — rough story animatic'
scene.render.resolution_x, scene.render.resolution_y = 1280, 720
scene.render.resolution_percentage = 100
scene.render.fps = FPS
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'
scene.render.film_transparent = False
if hasattr(scene, 'eevee'):
    scene.eevee.taa_render_samples = 16
camera = scene.camera
camera.data.animation_data_clear()
props = bpy.data.collections.new('Story props — original editable vectors')
scene.collection.children.link(props)
materials = {}
groups = {}

def mat(color):
    if color not in materials:
        rgb = [int(color[i:i+2], 16)/255 for i in (1, 3, 5)]
        rgb = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in rgb]
        m = bpy.data.materials.new('Story / '+color)
        m.use_nodes = True
        nodes = m.node_tree.nodes
        nodes.clear()
        output, shader = nodes.new('ShaderNodeOutputMaterial'), nodes.new('ShaderNodeEmission')
        shader.inputs['Color'].default_value = (*rgb, 1)
        m.node_tree.links.new(shader.outputs[0], output.inputs['Surface'])
        materials[color] = m
    return materials[color]

def group(name):
    obj = bpy.data.objects.new(name, None)
    props.objects.link(obj)
    groups[name] = obj
    return obj

def line(name, points, color=INK, width=.035, z=.8, parent=None, closed=False):
    data = bpy.data.curves.new(name, 'CURVE')
    data.dimensions = '3D'
    data.bevel_depth = width/2
    data.bevel_resolution = 2
    spline = data.splines.new('POLY')
    spline.points.add(len(points)-1)
    for p, xy in zip(spline.points, points):
        p.co = (*xy, z, 1)
    spline.use_cyclic_u = closed
    data.materials.append(mat(color))
    obj = bpy.data.objects.new(name, data)
    props.objects.link(obj)
    obj.parent = parent
    return obj

def polygon(name, points, color=PAPER, z=.7, parent=None, outline=.03):
    data = bpy.data.meshes.new(name)
    data.from_pydata([(*p, z) for p in points], [], [list(range(len(points)))])
    data.materials.append(mat(color))
    obj = bpy.data.objects.new(name, data)
    props.objects.link(obj)
    obj.parent = parent
    if outline:
        line(name+' outline', points, width=outline, z=z+.01, parent=parent, closed=True)
    return obj

def rect(name, x, y, w, h, color=PAPER, z=.7, parent=None, outline=.03):
    return polygon(name, [(x,y),(x+w,y),(x+w,y+h),(x,y+h)], color, z, parent, outline)

def oval(x, y, rx, ry, n=40):
    return [(x+rx*math.cos(i*math.tau/n), y+ry*math.sin(i*math.tau/n)) for i in range(n)]

def check(x, y, size, parent, z=.85):
    line('check', [(x,y),(x+size*.32,y-size*.3),(x+size,y+size*.5)], TEAL, .045, z, parent)

def flower(parent, x=0, y=0, scale=1, z=.8):
    line('flower stem', [(x,y-.43*scale),(x,y+.08*scale)], TEAL, .038*scale, z, parent)
    polygon('leaf', [(x,y-.2*scale),(x-.27*scale,y-.11*scale),(x-.17*scale,y-.32*scale)], TEAL, z, parent, 0)
    for a in range(8):
        ang = a*math.tau/8
        polygon('petal', oval(x+.20*scale*math.cos(ang), y+.13*scale+.20*scale*math.sin(ang), .11*scale, .11*scale), GOLD, z+.02, parent, 0)
    polygon('flower center', oval(x,y+.13*scale,.105*scale,.105*scale), CORAL, z+.03, parent, 0)

polygon('Warm wall', [(-30,-12),(30,-12),(30,15),(-30,15)], '#f6efdf', -3, outline=0)
rect('Floor', -30,-12,60,12,'#e8d8c3',-2,outline=0)
line('Baseboard',[(-20,0),(20,0)], '#bba98e', .018, -1.8)
hook = group('Hook')
line('Existing wall hook', [(0,.12),(0,-.12),(.06,-.16),(.12,-.12),(.12,-.04)], INK,.045,-.5,hook)
polygon('Hook screw', oval(0,.13,.045,.045), GOLD,-.49,hook,0)
hook.location = (3,3.45,0)

picture = group('Picture')
rect('Teal frame',-.77,-.77,1.54,1.54,TEAL,.62,picture,.045)
rect('Picture paper',-.63,-.63,1.26,1.26,PAPER,.65,picture,.018)
flower(picture, scale=1.1)
line('Hanging wire',[(-.45,.77),(0,.98),(.45,.77)],INK,.022,.58,picture)

ruler = group('Ruler')
rect('Wood ruler',-.1,-.85,.2,1.7,GOLD,.9,ruler,.023)
for i in range(17):
    line('Ruler mark',[(-.1,-.78+i*.095),(-.02 if i%5 else .05,-.78+i*.095)],INK,.013,.93,ruler)

level = group('Level')
rect('Spirit level',-.7,-.09,1.4,.18,GOLD,.9,level,.022)
rect('Level window',-.17,-.055,.34,.11,PAPER,.94,level,.01)
polygon('Bubble',oval(.035,0,.055,.035),TEAL,.95,level,0)

desk = group('Desk')
rect('Desk top',-1.35,1.60,2.7,.13,'#c4a37c',-.35,desk)
for x in (-1.1,1.03):
    rect('Desk leg',x,0,.1,1.6,'#b8966e',-.36,desk)

clipboard = group('Checklist')
rect('Clipboard',-.55,-.76,1.1,1.52,'#c4a37c',.90,clipboard)
rect('Checklist sheet',-.48,-.67,.96,1.32,PAPER,.93,clipboard,.01)
rect('Clip',-.19,.59,.38,.13,INK,.96,clipboard,0)
for i in range(4):
    rect('Empty task box',-.35,.30-i*.25,.13,.13,PAPER,.96,clipboard,.016)
    line('Task line',[(-.11,.35-i*.25),(.31,.35-i*.25)], '#acb0ab',.025,.96,clipboard)
flower(clipboard,.13,.49,.20,.98)
checks = group('Checklist ticks')
for i in range(3):
    check(-.34,.36-i*.25,.14,checks,.99)

pencil = group('Pencil')
rect('Pencil shaft',-.035,-.35,.07,.65,GOLD,1.05,pencil,.01)
polygon('Pencil tip',[(-.035,-.35),(.035,-.35),(0,-.48)],INK,1.05,pencil,0)

board = group('Planning board')
rect('Board legs',-.95,0,.1,2,'#ab8966',-.72,board)
rect('Board legs',.95,0,.1,2,'#ab8966',-.72,board)
rect('Cork board',-1.7,1.5,3.4,2.5,'#ddc4a0',-.65,board,.05)
cards = []
for i, (x,y) in enumerate([(-1.27,3.32),(-.20,3.32),(.90,3.32),(-1.27,2.42),(-.20,2.42),(.90,2.42)]):
    g = group('Board card '+str(i))
    rect('Card',x-.35,y-.30,.7,.60,PAPER,-.56,g,.016)
    polygon('Pin',oval(x,y+.22,.045,.045),CORAL,-.51,g,0)
    if i==0:
        flower(g,x,y,.36,-.50)
    elif i in (1,4):
        for j in range(3):
            line('Diagram lines',[(x-.21,y+.10-j*.1),(x+.20,y+.10-j*.1)],TEAL,.024,-.50,g)
    elif i in (2,5):
        line('Diagram triangle',[(x-.19,y-.12),(x+.18,y-.12),(x,y+.12),(x-.19,y-.12)],INK,.023,-.50,g)
    else:
        line('Diagram arrow',[(x-.20,y),(x+.20,y),(x+.09,y+.1),(x+.20,y),(x+.09,y-.1)],TEAL,.03,-.50,g)
    cards.append(g)
thread = group('Red connections')
line('Overcomplicated dependencies',[(-1.27,3.32),(.90,2.42),(-.20,3.32),(-1.27,2.42),(.90,3.32),(-.20,2.42),(-1.27,3.32),(.90,3.32),(-1.27,2.42)],CORAL,.028,-.45,thread)

papers=[]
for i in range(12):
    g=group('Paper pile '+str(i))
    rect('Paper',-.53,0,1.06,.075,PAPER,.88,g,.016)
    papers.append(g)
roll=group('Long checklist')
rect('Unrolled checklist',-.48,0,.96,3.8,PAPER,.92,roll,.023)
for j in range(16):
    rect('More empty boxes',-.35,.15+j*.22,.12,.12,PAPER,.95,roll,.016)
    line('More tasks',[(-.1,.21+j*.22),(.32,.21+j*.22)],'#a6aaa6',.021,.95,roll)

toolbox=group('Toolbox')
rect('Toolbox base',-.65,0,1.3,.56,TEAL,.6,toolbox)
line('Toolbox handle',[(-.20,.56),(-.20,.80),(.20,.80),(.20,.56)],INK,.055,.6,toolbox)
rect('Toolbox latch',-.065,.40,.13,.22,GOLD,.64,toolbox,.016)

clock=group('Clock')
polygon('Clock face',oval(0,0,.41,.41),PAPER,-.8,clock,.025)
for i in range(12):
    a=i*math.tau/12
    line('Clock tick',[(.32*math.sin(a),.32*math.cos(a)),(.36*math.sin(a),.36*math.cos(a))],INK,.018,-.77,clock)
clockhand=group('Clock minute hand')
line('Clock hand',[(0,0),(0,.30)],INK,.022,-.75,clockhand)
clockshort=group('Clock hour hand')
line('Clock short hand',[(0,0),(0,.19)],INK,.036,-.74,clockshort)

sun=group('Sunlight')
polygon('Window light',[(-6.7,4.7),(-5.4,4.7),(1.9,.06),(-.7,.06)],'#fff7df',-2.5,sun,0)
idea=group('Idea rays')
for a in (-.7,0,.7):
    line('Small idea ray',[(.7*math.sin(a),.7*math.cos(a)),(.95*math.sin(a),.95*math.cos(a))],GOLD,.055,1.0,idea)

# Every state below is episode-specific. Held poses are intentional animatic timing.
panels=[]
state=dict(x=-3.8,pose='idle',face='happy',gaze=1,cam=[0,2.25,12.8],pic=[3,.80,-.06],
           ruler=None,level=None,desk=False,clip=None,ticks=False,pencil=None,board=0,
           strings=False,pile=0,roll=False,tools=False,clock=0,light=False,idea=False)
def panel(seconds, beat, description, cue=None, **changes):
    state.update(changes)
    panels.append(dict(state, nominal_seconds=seconds, beat=beat, description=description,cue=cue))

panel(4,'The tiny task','An empty wall hook. One framed flower rests directly below it. He notices the picture.')
panel(2,'The tiny task','Insert: the flower picture waiting on the floor.',cam=[3,1.0,3.5])
panel(2,'The tiny task','Insert: the empty hook above it.',cam=[3,3.35,3.5])
panel(3,'The tiny task','He approaches with an easy smile.',cue='step',x=1.6,cam=[1.5,2.25,7.6])
panel(2,'The tiny task','He bends and takes the left edge of the frame.',cue='tap',pose='pickup')
panel(3,'The tiny task','He lifts the picture. This should be easy.',cue='lift',pose='carry',pic=[3,2.05,-.06])
panel(3,'The tiny task','Almost at the hook, he notices a slight tilt.',pose='hang',pic=[3,2.65,-.12],face='suspicious')
panel(2,'First detour','He pauses, thinking. Perhaps he should measure first.',pose='think',pic=[3,.80,-.06],idea=True)
panel(3,'First detour','A ruler appears in his hand. He is delighted with this sensible preparation.',cue='pop',pose='measure',ruler=[2.45,3.2,0],idea=False,face='happy')
panel(2,'First detour','He carefully measures the existing hook.',cam=[2.8,3.25,4.0],ruler=[2.7,3.3,0])
panel(2,'First detour','He adjusts the ruler by a tiny amount.',cue='tick',ruler=[2.74,3.3,0],face='effort')
panel(3,'First detour','Now he checks the ruler with a spirit level.',cue='pop',cam=[1.5,2.55,7.5],level=[2.70,4.14,0])
panel(2,'First detour','Close: the bubble is already in the middle.',cam=[2.7,4.10,3.0])
panel(3,'First detour','He lowers his tools and looks pleased. The picture is still on the floor.',cam=[0,2.25,12.8],pose='proud',ruler=None,level=None,face='happy')
panel(3,'First detour','He reaches for the picture again, then stops to remember something.',cam=[1.5,2.1,7.6],pose='pickup',face='suspicious')
panel(2,'A list for the task','Another idea. He needs a checklist.',pose='think',idea=True)
panel(3,'A list for the task','He sets up a desk on the other side of the room.',cue='thud',x=-3.8,pose='desk',desk=True,idea=False,cam=[0,2.25,12.8],clip=[-2.8,2.15,0],pencil=[-3.30,2.25,-.5])
panel(3,'A list for the task','He writes a short list with careful concentration.',cue='scribble',cam=[-3.0,2.6,6.5],face='effort')
panel(2,'A list for the task','Insert: three preparation steps checked; the flower task remains empty.',cue='tick',cam=[-2.8,2.15,2.65],ticks=True)
panel(3,'A list for the task','He admires his progress.',cam=[-3.1,2.5,6.7],pose='proud',face='happy',pencil=None)
panel(3,'A list for the task','Wide: the picture has not moved.',cam=[0,2.25,12.8],clock=1)
panel(2,'A list for the task','He looks at the picture, then back at his list.',pose='think',face='suspicious',gaze=1)
panel(3,'A list for the task','He writes a second list to improve the first.',cue='scribble',pose='desk',pencil=[-3.30,2.25,-.5],pile=3,face='effort')
panel(2,'A list for the task','A third revision.',cue='paper',pile=6,clock=2)
panel(2,'A list for the task','Then another. Preparation is growing.',cue='paper',pile=10,clock=3)
panel(3,'A list for the task','He raises his perfect checklist. It unrolls almost to the floor.',cue='unroll',pose='raise',clip=None,ticks=False,pencil=None,roll=True,cam=[-2.7,2.2,7.5],face='surprise')
panel(2,'A list for the task','He peers around the long list, still trying to look satisfied.',pose='peek',face='happy')
panel(3,'Planning the preparation','He needs a way to organize all of this.',pose='think',roll=False,face='suspicious',idea=True)
panel(3,'Planning the preparation','A large planning board takes its place between him and the task.',cue='thud',board=1,cam=[0,2.25,12.8],idea=False,pose='present')
panel(2,'Planning the preparation','First, the flower card: the original goal.',cam=[-.95,3.28,3.7],pose='point')
panel(3,'Planning the preparation','He adds a card for the measuring step.',cue='pin',board=2,cam=[-1.7,2.55,7.5],x=-2.8,pose='board')
panel(2,'Planning the preparation','Then the tools.',cue='pin',board=3,tools=True)
panel(2,'Planning the preparation','Then how to choose the tools.',cue='pin',board=4)
panel(2,'Planning the preparation','Then how to organize the choosing.',cue='pin',board=5,clock=4)
panel(3,'Planning the preparation','The board is full. He draws connections everywhere.',cue='scribble',board=6,strings=True,face='effort')
panel(3,'Planning the preparation','Close: the route from the flower card is now a tangle.',cam=[0,2.9,4.8])
panel(3,'Planning the preparation','He proudly unveils his system. The little picture still waits.',cam=[0,2.25,12.8],pose='present',face='happy')
panel(2,'The system takes over','He starts following the connections with his finger.',cam=[-1.6,2.6,7.3],pose='board',face='suspicious')
panel(2,'The system takes over','The route takes him back to the same card.',cue='tick',pose='point',gaze=-1)
panel(3,'The system takes over','He consults the checklist again.',cue='paper',pose='read',clip=[-2.15,2.4,0],ticks=True,gaze=1)
panel(2,'The system takes over','The checklist points him back to the board.',pose='board',clip=None,ticks=False,face='effort')
panel(2,'The system takes over','He checks the ruler again.',cue='tick',pose='measure',ruler=[-1.95,3.2,0])
panel(2,'The system takes over','Then checks the checklist again.',cue='paper',pose='read',ruler=None,clip=[-2.15,2.4,0],ticks=True,clock=5)
panel(3,'The system takes over','His eyes droop. He is tired, but nothing is done.',cam=[-2.7,3.1,4.6],pose='tired',face='tired',clip=None,ticks=False)
panel(2,'The system takes over','The clock has marched on.',cam=[-5.0,4.2,2.8],clock=7)
panel(4,'The system takes over','Wide: a room full of preparation. The picture is still in exactly the same place.',cam=[0,2.25,12.8],pose='slump',x=-3.3,light=True)
panel(3,'A quiet realization','He sits back against the desk, drained.',cam=[-2.6,1.9,7.0],pose='sit',face='tired',clock=8)
panel(3,'A quiet realization','His eyes find the flower picture across the room.',pose='sitlook',gaze=1)
panel(3,'A quiet realization','Insert: warm light on the small, uncomplicated picture.',cam=[3,1.0,3.8])
panel(2,'A quiet realization','He looks up to the hook. The task has never changed.',cam=[3,3.35,3.6])
panel(3,'A quiet realization','He looks at the tangled board one last time.',cam=[-2.5,2.45,7.0],pose='think',face='suspicious',x=-3.3)
panel(3,'A quiet realization','He sets the pencil down. No new plan.',cue='tap',pose='desk',pencil=[-3.0,1.82,1.55],face='neutral')
panel(2,'Just do the thing','He stands and turns toward the picture.',pose='idle',gaze=1,cam=[0,2.25,12.8])
panel(2,'Just do the thing','He walks away from the desk.',cue='step',x=-1.7,pose='walk')
panel(2,'Just do the thing','Past the board, toward the task.',cue='step',x=.1,pose='walk2')
panel(2,'Just do the thing','He stops at the picture.',cue='step',x=1.6,pose='idle',cam=[1.65,2.2,7.6])
panel(2,'Just do the thing','He bends and grips the frame.',cue='tap',pose='pickup')
panel(2,'Just do the thing','He lifts it.',cue='lift',pose='carry',pic=[3,2.05,-.06])
panel(2,'Just do the thing','He places the wire over the hook.',cue='click',pose='hang',pic=[3,2.47,-.04])
panel(3,'Just do the thing','He lets go. It stays there.',pose='idle',face='happy')
panel(3,'The last temptation','He steps back to admire it.',cue='step',x=.55,cam=[1.3,2.5,8.1],pose='proud')
panel(2,'The last temptation','The picture is slightly crooked.',cam=[3,2.75,3.7])
panel(2,'The last temptation','His eyes flick back toward the ruler and planning board.',cam=[.55,3.1,4.5],pose='think',face='suspicious',gaze=-1)
panel(2,'The last temptation','He almost reaches for the old solution.',cam=[0,2.25,12.8],pose='tempted',gaze=-1)
panel(2,'The last temptation','Then he smiles, turns and nudges the frame with one hand.',cue='tap',x=1.6,pose='nudge',face='happy',gaze=1,pic=[3,2.47,0],cam=[1.65,2.6,7.2])
panel(3,'Done','He drops his hand. That was all it needed.',pose='idle')
panel(3,'Done','He walks away from the finished picture, leaving the elaborate system behind.',cue='step',x=.1,pose='walk2',gaze=-1,cam=[0,2.25,12.8])
panel(4,'Done','Final image: one picture on the wall; a huge planning apparatus for a tiny completed task.',x=-5.1,pose='idle',face='happy')

# Preserve relative authored pacing while fitting the approved 180-second experiment.
total = sum(p['nominal_seconds'] for p in panels)
boundaries = [0]
elapsed=0
for p in panels:
    elapsed += p['nominal_seconds']
    boundaries.append(round(elapsed/total*180*FPS))
assert boundaries[-1] == 4320 and all(b>a for a,b in zip(boundaries,boundaries[1:]))
for i,p in enumerate(panels):
    if p['cam'][2] == 7.6:
        p['cam'] = [p['cam'][0], 2.1, 7.6]  # Keep floor contact visible in task shots.
    if p['pose'] in ('raise','peek'):
        p['cam'] = [p['cam'][0], 2.05, 7.7]
    p.update(index=i+1,frame=boundaries[i]+1,frames=boundaries[i+1]-boundaries[i],
             start_seconds=boundaries[i]/FPS,seconds=(boundaries[i+1]-boundaries[i])/FPS,
             image=f'panels/panel-{i+1:03}.png')
(OUT/'story.json').write_text(json.dumps({'title':'Just One Thing','fps':FPS,'frames':4320,
    'character_source':str(SOURCE),'format':'Authored held-pose animatic; not full animation','panels':panels},indent=2)+'\n')
lines=['# Just One Thing — timed story edit','', 'An original wordless procrastination story. Rough held poses; exact duration 03:00.','', '| Time | Beat | Visible action |','| --- | --- | --- |']
for p in panels:
    t=p['start_seconds']
    lines.append(f"| {int(t)//60:02}:{t%60:04.1f} | {p['beat']} | {p['description']} |")
(ROOT/'storyboard-v001.md').write_text('\n'.join(lines)+'\n')

def transform(obj, x, y, angle=0, scale=1):
    obj.location=(x,y,0)
    obj.rotation_euler.z=angle
    obj.scale=(scale,scale,scale)

def joint(a,b,length,side,bend=.55):
    dx,dy=b[0]-a[0],b[1]-a[1]
    d=max(math.hypot(dx,dy),.001)
    h=bend*math.sqrt(max(0,length*length-d*d/4))
    return ((a[0]+b[0])/2-side*dy*h/d,(a[1]+b[1])/2+side*dx*h/d)

def show(g, on):
    for obj in [g,*g.children_recursive]:
        obj.hide_render=not on
        obj.hide_viewport=not on

def expression(name, gaze):
    squint={'effort':.55,'tired':.72,'suspicious':.4}.get(name,0)
    for i in range(2):
        eye=bpy.data.objects[f'Eye_{i}']
        eye.location.x=(-.15+i*.30)+.12*gaze
        eye.location.y=.055
        eye.scale=(1,max(.12,1-squint),1)
        points=bpy.data.objects[f'Brow_{i}'].data.splines[0].points
        for j,p in enumerate(points):
            u=j/(len(points)-1)
            y=.31+.045*math.sin(u*math.pi)
            if name=='effort': y+=.09*(1-2*u)*(1 if i==0 else -1)
            if name in ('suspicious','tired'):y-=.10
            if name=='surprise':y+=.08
            p.co.x=(-.25+i*.31)+.10*gaze+.23*u
            p.co.y=y
    mouth=bpy.data.objects['Mouth']
    for j,p in enumerate(mouth.data.splines[0].points):
        u=j/(len(mouth.data.splines[0].points)-1)
        p.co.x=-.075+.1*gaze+.23*u
        p.co.y=-.29+({'happy':-.085,'tired':.045,'effort':.04}.get(name,0))*math.sin(u*math.pi)
    mouth.scale=(.001,.001,.001) if name=='surprise' else (1,1,1)
    opened=bpy.data.objects['Mouth open']
    opened.scale=(1,1,1) if name=='surprise' else (.001,.001,.001)

def character(p):
    x=p['x'];pose=p['pose']; y=1.83; angle=0; tilt=0
    feet=[(x-.32,.13),(x+.33,.13)]
    hands=[(x-.45,1.42),(x+.48,1.42)]
    if pose in ('think','tempted'):
        hands[1]=(x+.23,3.06);tilt=-.10
        if pose=='tempted':hands[0]=(x-.95,2.2)
    elif pose=='proud':hands=[(x-.22,2.05),(x+.28,2.05)];tilt=.04
    elif pose=='measure':hands=[(x-.38,1.9),(x+.88,3.18)];tilt=.10
    elif pose=='pickup':
        y=1.15;angle=-.56;hands=[(2.23,1.23),(2.27,.64)];feet=[(x-.5,.13),(x+.48,.13)];tilt=-.20
    elif pose=='carry':hands=[(2.22,2.36),(2.23,1.77)];angle=-.06
    elif pose=='hang':hands=[(2.22,p['pic'][1]+.33),(2.23,p['pic'][1]-.28)];angle=-.08;tilt=.1
    elif pose=='nudge':hands[1]=(2.23,2.55)
    elif pose=='desk':hands=[(-3.40,1.83),(-3.30,2.12)];angle=-.23;tilt=-.17
    elif pose in ('raise','peek'):
        hands=[(x-.5,2.1),(-2.50,3.74)];tilt=.14
        if pose=='peek':angle=-.22
    elif pose in ('present','point','board'):
        hands=[(x-.55,1.65),(x+1.15,3.15 if pose=='board' else 2.65)]
        if pose=='present':hands[0]=(x-.85,2.5)
    elif pose=='read':hands=[(x+.23,2.0),(x+.72,2.28)];tilt=-.13
    elif pose in ('tired','slump'):
        y=1.60;angle=-.16;tilt=-.15;hands=[(x-.30,1.23),(x+.55,1.23)]
    elif pose in ('sit','sitlook'):
        y=.85;angle=.1;feet=[(x+.55,.13),(x+1.05,.13)]
        hands=[(x+.30,.75),(x+.70,.62)];tilt=-.16 if pose=='sit' else .05
    elif pose in ('walk','walk2'):
        sign=1 if pose=='walk' else -1
        feet=[(x-.48,.13),(x+.43,.29)] if sign==1 else [(x-.35,.29),(x+.45,.13)]
        hands=[(x-.5*sign,1.45),(x+.55*sign,1.55)]
    body=bpy.data.objects['CTRL_Body'];transform(body,x,y,angle)
    sh=(x-.84*math.sin(angle),y+.84*math.cos(angle))
    transform(bpy.data.objects['CTRL_Head'],sh[0]-.02,sh[1]+.68,tilt)
    for i,side in enumerate(('far','near')):
        transform(bpy.data.objects['CTRL_Foot_'+side],*feet[i])
        transform(bpy.data.objects['CTRL_Hand_'+side],*hands[i],angle=-.2 if pose=='pickup' else 0)
        transform(bpy.data.objects['CTRL_Elbow_'+side],*joint(sh,hands[i],.93,-1 if hands[i][0]>sh[0] else 1))
        transform(bpy.data.objects['CTRL_Knee_'+side],*joint((x,y),feet[i],1.08,-1 if i==0 else 1,.4))
    expression(p['face'],p['gaze'])
    return sh

def apply(p):
    sh=character(p)
    transform(picture,*p['pic'])
    for name,key in [('Ruler','ruler'),('Level','level'),('Checklist','clip'),('Pencil','pencil')]:
        g=groups[name];show(g,p[key] is not None)
        if p[key]:transform(g,*p[key])
    show(checks,p['ticks'] and p['clip'] is not None)
    if p['clip']:transform(checks,*p['clip'])
    show(desk,p['desk']);transform(desk,-2.8,0)
    show(board,p['board']>0);transform(board,0,0)
    for i,g in enumerate(cards):show(g,p['board']>i)
    show(thread,p['strings'])
    for i,g in enumerate(papers):
        show(g,i<p['pile']);transform(g,-2.1+(.025 if i%2 else -.025),1.75+i*.082)
    show(roll,p['roll']);transform(roll,-2.45,.05)
    show(toolbox,p['tools']);transform(toolbox,.90,0)
    for g in (clock,clockhand,clockshort):
        show(g,p['clock']>0);transform(g,-5,4.2)
    clockhand.rotation_euler.z=-p['clock']*1.5
    clockshort.rotation_euler.z=-.5-p['clock']*.13
    show(sun,p['light'])
    show(idea,p['idea']);transform(idea,sh[0],sh[1]+.83)
    camera.location=(p['cam'][0],p['cam'][1],30)
    camera.data.ortho_scale=p['cam'][2]

# Constant keys make the Blender timeline agree exactly with the delivered edit.
for p in panels:
    f=p['frame'];scene.frame_set(f);apply(p)
    for obj in bpy.data.objects:
        for key in ('location','rotation_euler','scale','hide_render','hide_viewport'):
            obj.keyframe_insert(data_path=key,frame=f)
    camera.data.keyframe_insert(data_path='ortho_scale',frame=f)
    for name in ('Brow_0','Brow_1','Mouth'):
        for point in bpy.data.objects[name].data.splines[0].points:
            point.keyframe_insert(data_path='co',frame=f)
    scene.timeline_markers.new(f"{p['index']:02} · {p['beat']}",frame=f)
for action in bpy.data.actions:
    for slot in action.slots:
        for layer in action.layers:
            for strip in layer.strips:
                bag=strip.channelbag(slot)
                if bag:
                    for fc in bag.fcurves:
                        for k in fc.keyframe_points:k.interpolation='CONSTANT'
scene.frame_start,scene.frame_end=1,4320
scene['Notes']='Original 180-second wordless story. Actual C character reused. Held-pose animatic, not finished animation. Storyboard and JSON are the edit record.'
scene.render.filepath='//panels/'
scene.frame_set(1)
bpy.context.view_layer.update()
drivers=[fc for obj in bpy.data.objects if obj.type=='CURVE' and obj.data.animation_data for fc in obj.data.animation_data.drivers]
assert len(drivers)==48 and all(d.driver.is_valid for d in drivers)
assert bpy.data.objects['Head'].data.vertices.__len__()==64
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'just-one-thing.blend'))
(OUT/'build-checks.json').write_text(json.dumps({'seconds':180,'frames':4320,'fps':24,'panels':len(panels),'preserved_limb_drivers':len(drivers),'character_source':str(SOURCE),'status':'passed','scope':'Timing, reused native character and valid endpoint drivers. Creative review is separate.'},indent=2)+'\n')
if '--render' in sys.argv or '--samples' in sys.argv:
    selected=panels if '--render' in sys.argv else [panels[i] for i in (0,5,17,25,35,45,56,64,67)]
    for p in selected:
        scene.frame_set(p['frame'])
        scene.render.filepath=str(OUT/p['image'])
        bpy.ops.render.render(write_still=True)
        print(f"PANEL {p['index']}/{len(panels)} {p['beat']}",flush=True)
