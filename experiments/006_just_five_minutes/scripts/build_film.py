"""Reconstruct the supplied notebook characters as editable native Blender artwork.
Blender --background --factory-startup --python-exit-code 1 --python this_file -- --samples
Coordinates for the main face and silhouette were drawn against references/front.png.
"""
from pathlib import Path
import ast
import bpy
import math
import json
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/film-v001'
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'stills').mkdir(exist_ok=True)
SOURCE = ROOT.parent / '001_heavy_box/artifacts/finish-v002/character-and-effects.blend'
HELPERS = ROOT.parent / '003_alisson_winner/scripts/build_film.py'
MATS = {}; GROUPS = {}
INK = '#151515'; PAPER = '#fdfdfd'; RED = '#bc080f'
names = {'clamp', 'ease', 'mix', 'vec', 'rgba', 'mat', 'add', 'poly', 'line', 'rect', 'oval', 'label', 'empty', 'visible', 'key'}
nodes = [n for n in ast.parse(HELPERS.read_text()).body if isinstance(n, ast.FunctionDef) and n.name in names]
assert len(nodes) == len(names)
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(HELPERS), 'exec'), globals())
scene = bpy.data.scenes.new('Just Five Minutes — reference replication')
bpy.context.window.scene = scene
art = bpy.data.collections.new('Editable notebook drawings')
scene.collection.children.link(art)
scene.render.engine = 'BLENDER_EEVEE'
scene.eevee.taa_render_samples = 16
scene.render.resolution_x = 1920; scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100; scene.render.fps = 30
scene.frame_start = 1; scene.frame_end = 900
scene.render.image_settings.file_format = 'PNG'; scene.render.image_settings.color_mode = 'RGB'
scene.render.image_settings.compression = 15
scene.render.use_compositing = False; scene.render.use_sequencer = False
scene.view_settings.view_transform = 'Standard'; scene.view_settings.look = 'None'
scene.world = bpy.data.worlds.new('White paper'); scene.world.color = (1, 1, 1)
cd = bpy.data.cameras.new('Flat artwork camera'); camera = bpy.data.objects.new('Flat artwork camera', cd)
art.objects.link(camera); scene.camera = camera
cd.type = 'ORTHO'; cd.sensor_fit = 'HORIZONTAL'; cd.ortho_scale = 1920
cd.clip_end = 3000; camera.location = (960, -540, 1000)
font = bpy.data.fonts.load('/System/Library/Fonts/MarkerFelt.ttc')
regular = bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf')

# World-space rules continue across white faces/shirts like the supplied paper artwork.
def paper_material(c):
    m = mat(c)
    if m.get('ruled'): return m
    n = m.node_tree.nodes; links = m.node_tree.links
    geo = n.new('ShaderNodeNewGeometry'); xyz = n.new('ShaderNodeSeparateXYZ')
    mod = n.new('ShaderNodeMath'); mod.operation = 'PINGPONG'; mod.inputs[1].default_value = 38
    less = n.new('ShaderNodeMath'); less.operation = 'LESS_THAN'; less.inputs[1].default_value = .65
    blend = n.new('ShaderNodeMixRGB'); blend.blend_type = 'MIX'
    base = rgba(c); blend.inputs[1].default_value = base
    blend.inputs[2].default_value = tuple(v * .85 for v in base[:3]) + (1,)
    links.new(geo.outputs['Position'], xyz.inputs[0]); links.new(xyz.outputs['Y'], mod.inputs[0])
    links.new(mod.outputs[0], less.inputs[0]); links.new(less.outputs[0], blend.inputs[0])
    links.new(blend.outputs[0], next(x for x in n if x.type == 'EMISSION').inputs[0])
    m['ruled'] = True
    return m
paper_material(PAPER); paper_material('#cccccc')

def smooth(points, closed=False, steps=8):
    p = list(points); out = []
    for i in range(len(p) if closed else len(p)-1):
        a = p[(i-1) % len(p)] if closed or i else p[0]
        b = p[i]; c = p[(i+1) % len(p)]
        d = p[(i+2) % len(p)] if closed else p[min(i+2, len(p)-1)]
        for j in range(steps):
            t = j / steps
            out.append(tuple(.5*((2*b[k])+(-a[k]+c[k])*t+(2*a[k]-5*b[k]+4*c[k]-d[k])*t*t+(-a[k]+3*b[k]-3*c[k]+d[k])*t*t*t) for k in (0,1)))
    if not closed: out.append(p[-1])
    return out

def stroke(name, pts, parent=None, z=1, width=3, color=INK, curved=False, closed=False):
    pts = smooth(pts, closed) if curved else pts
    if width<=6: width*=1.4
    return line(name, [(x,-y) for x,y in pts], color, width, z, parent=parent, closed=closed)

def shape(name, pts, color=PAPER, parent=None, z=0, width=3, curved=False):
    pts = smooth(pts, True) if curved else pts
    obj = poly(name, [(x,-y) for x,y in pts], color, z, parent=parent)
    if width: stroke(name+' / contour', pts, parent, z+.08, width, closed=True)
    return obj

def ellipse(name,x,y,rx,ry,color=PAPER,parent=None,z=0,width=3):
    return shape(name, [(x+rx*math.cos(a*math.tau/48),y+ry*math.sin(a*math.tau/48)) for a in range(48)],color,parent,z,width)

def group(name, parent=None):
    g = empty(name); g.parent = parent; return g

def place(obj,x,y,s=1,angle=0,z=0):
    obj.location=(x,-y,z); obj.scale=(s,s,s); obj.rotation_euler.z=-math.radians(angle)

def children(obj): return list(obj.children_recursive)

def visible(items,on,frame):
    # Each frame is baked independently; never overwrite the preceding pose's visibility.
    for ob in items:
        ob.hide_render=ob.hide_viewport=not on
        ob.keyframe_insert(data_path='hide_render',frame=frame)
        ob.keyframe_insert(data_path='hide_viewport',frame=frame)

def text_group(name, lines, x, y, size=65, color=RED, handwritten=False):
    g = group(name)
    for i,body in enumerate(lines):
        ob = label(name+' / '+body, body, 0, -i*size*1.12, size, color, 80, parent=g, bold=not handwritten)
        ob.rotation_euler.z=math.radians((i%2*2-1)*1.4)
    place(g,x,y)
    return g

shape('Continuous white ruled paper',[(-3000,-3000),(5000,-3000),(5000,4000),(-3000,4000)],PAPER,z=-100,width=0)

# Desk and chair contours reconstructed from the reference's desk view.
desk = group('Desk / grey surface, orange supports and desktop')
shape('Left orange leg',[(-775,0),(-699,0),(-699,435),(-770,438)],'#c96428',desk,0)
shape('Right orange leg',[(672,0),(779,-10),(760,434),(671,434)],'#c96428',desk,0)
shape('Grey tabletop',[(-775,0),(-586,-220),(642,-232),(779,-10),(716,2)],'#cccccc',desk,1)
shape('Monitor foot',[(100,-188),(160,-240),(350,-240),(420,-188)],'#626262',desk,2)
shape('Monitor stem',[(235,-335),(303,-335),(300,-218),(237,-217)],PAPER,desk,3)
shape('Monitor bezel',[(27,-545),(498,-545),(493,-310),(34,-309)],'#626262',desk,4)
shape('Monitor screen',[(50,-520),(467,-520),(468,-336),(60,-334)],PAPER,desk,5)
stroke('Empty document top',[(105,-475),(410,-475)],desk,6,2,color='#aaaaaa')
stroke('Empty document margin',[(105,-459),(105,-375)],desk,6,2,color='#cccccc')
stroke('Waiting cursor',[(123,-447),(123,-424)],desk,6,3)
stroke('Mouse cable',[(485,-224),(494,-196),(451,-163),(420,-132),(429,-100),(398,-69),(357,-56)],desk,3,3,curved=True)
shape('Grey mouse',[(274,-56),(288,-76),(318,-84),(344,-74),(359,-61),(329,-51),(292,-50)],'#646464',desk,5,curved=True)

chair = group('Black office chair')
shape('Chair rounded back',[(-240,-60),(-265,-117),(-240,-255),(-139,-285),(175,-289),(247,-258),(263,-159),(215,-69),(94,-49),(-110,-52)],'#030303',chair,0,curved=True)
shape('Chair seat',[(-226,71),(-210,28),(-122,10),(168,16),(239,45),(221,83),(99,99),(-126,101)],'#030303',chair,1,curved=True)
shape('Chair support',[(-33,-42),(31,-42),(39,104),(-30,104)],'#aaaaaa',chair,2)
for y in range(-20,101,25): stroke('Chair support rib',[(-32,y),(35,y-5)],chair,3,2)
stroke('Chair pedestal',[(0,103),(0,179)],chair,0,18)
stroke('Chair base',[(-127,201),(0,178),(129,200)],chair,0,11)

def facepts(pts): return [(x-460,y-524) for x,y in pts]

hairpts=facepts([(366,378),(340,300),(340,231),(365,191),(417,176),(506,172),(549,184),(575,216),(578,260),(566,318),(548,355),(535,365)])
faceoutline=facepts([(462,272),(426,302),(383,354),(359,404),(353,445),(367,471),(406,488),(458,494),(511,486),(551,467),(565,442),(565,413),(553,379),(521,331),(486,285)])
eyeoutline=facepts([(414,355),(418,338),(432,331),(445,334),(452,339),(458,328),(474,324),(487,334),(491,351),(485,361),(472,368),(459,366),(448,366),(439,377),(425,376),(416,367)])

def actor(name, curly=False):
    root=group(name+' / placement'); head=group(name+' / head',root)
    # A reference-sized shirt and shorts rather than the older bean body.
    shape(name+' shorts',[(-157,381),(-180,523),(-63,525),(-19,429),(42,526),(145,523),(130,381)],PAPER if curly else '#303030',root,3)
    shape(name+' shirt',[(-143,0),(143,0),(129,385),(60,404),(-55,405),(-157,383),(-146,198)],PAPER,root,5)
    shape(name+' neck',[(-23,-35),(5,-35),(5,0),(-23,0)],PAPER,root,5)
    headparts=[]
    if curly:
        pts=[]
        for j in range(72):
            a=j*math.tau/72; r=1+.07*math.cos(a*13)
            pts.append((math.cos(a)*162*r,-230+math.sin(a)*134*r))
        shape(name+' curly black hair',pts,'#030303',head,7,0,curved=True)
    else: shape(name+' tall black hair',hairpts,'#020202',head,7,0,curved=True)
    shape(name+' tapered face',faceoutline,PAPER,head,8,3.5,True)
    normal=group(name+' eyes open',head)
    shape(name+' joined eye outline',eyeoutline,PAPER,normal,9,3.9,True)
    pupils=[]
    for i,(x,y) in enumerate([(-27,-169),(3,-174)]):
        p=ellipse(name+' pupil '+str(i),x,y,5.4,5.8,INK,normal,10,0);pupils.append(p)
    blink=group(name+' eyes closed',head)
    stroke(name+' closed left', [(-48,-171),(-35,-166),(-18,-171)],blink,10,3.8,curved=True)
    stroke(name+' closed right', [(-6,-176),(9,-173),(25,-179)],blink,10,3.8,curved=True)
    brows=[]
    for i,pts in enumerate([[(-47,-204),(-34,-214),(-18,-213)],[(2,-217),(12,-220),(25,-215)]]):
        b=stroke(name+' eyebrow '+str(i),pts,head,10,4.4,curved=True);brows.append(b)
    stroke(name+' nose',facepts([(450,379),(470,368),(486,374),(480,383),(455,394)]),head,10,4,curved=True)
    mouths={}
    for state in ('happy','guilty','open','tired','earnest'):
        g=group(name+' mouth / '+state,head); mouths[state]=g
        if state=='happy':
            shape(name+' smile',facepts([(407,416),(433,411),(479,409),(501,408),(493,431),(474,446),(449,451),(428,446),(415,434)]),PAPER,g,11,4,True)
            stroke(name+' teeth line',facepts([(412,433),(448,430),(492,426)]),g,11.2,3)
        elif state=='open':
            ellipse(name+' open mouth',-6,-100,35,27,INK,g,11,3)
            shape(name+' tongue',[(-32,-89),(-14,-96),(14,-94),(25,-87),(7,-76),(-16,-77)],'#e61720',g,11.1,0,True)
            shape(name+' top teeth',[(-34,-111),(18,-115),(23,-103),(-36,-101)],PAPER,g,11.2,1.5)
        elif state=='guilty':
            stroke(name+' awkward smile',[(-50,-102),(-28,-87),(1,-86),(27,-105)],g,11,4,curved=True)
            stroke(name+' awkward corner',[(26,-113),(30,-103),(25,-96)],g,11,2.5,curved=True)
        elif state=='tired':
            stroke(name+' tired mouth',[(-39,-89),(-16,-98),(9,-96),(30,-86)],g,11,4,curved=True)
        else:
            stroke(name+' slight smile',[(-47,-103),(-20,-94),(8,-96),(29,-105)],g,11,3.7,curved=True)
    back=group(name+' back view hair',head)
    shape(name+' back hair silhouette',[(-114,-315),(-68,-348),(30,-352),(98,-331),(119,-255),(107,-162),(59,-83),(3,-58),(-59,-86),(-109,-168)],'#020202',back,15,0,True)
    arms=[]; hands=[]; legs=[]; shoes=[]
    for side in (-1,1):
        arm=[]
        for c,w,z in [(INK,16,6),(PAPER,10.5,10)]:
            ob=stroke(name+f' arm {side} {c}',[(0,0)]*17,root,z,w,c);arm.append(ob)
        arms.append(arm)
        hand=group(name+f' hand {side}',root)
        ellipse(name+' simple palm',0,0,9,15,PAPER,hand,18,2.7)
        hands.append(hand)
        leg=[]
        for c,w,z in [(INK,15,1),(PAPER,9,5)]:
            ob=stroke(name+f' leg {side} {c}',[(0,0)]*17,root,z,w,c);leg.append(ob)
        legs.append(leg)
        shoe=group(name+f' black shoe {side}',root)
        shape(name+' foot',[(-23,-7),(-36,8),(-28,23),(5,27),(28,12),(20,-4)],'#020202',shoe,2,2,True);shoes.append(shoe)
    finger=group(name+' raised index finger',hands[0])
    stroke(name+' index outline',[(0,-4),(1,-39),(6,-48),(11,-43),(10,-3)],finger,19,9,INK,True)
    stroke(name+' index white',[(0,-4),(1,-39),(6,-44),(8,-40),(7,-3)],finger,22,4,PAPER,True)
    return dict(root=root,head=head,normal=normal,blink=blink,pupils=pupils,brows=brows,mouths=mouths,back=back,arms=arms,hands=hands,legs=legs,shoes=shoes,finger=finger,all=children(root))

hero=actor('Protagonist'); friend=actor('Curly-haired friend',True)

phone=group('Phone / rigid editable prop')
shape('Phone body',[(-23,-105),(23,-105),(28,-100),(28,-1),(23,4),(-23,4),(-28,-1),(-28,-100)],PAPER,phone,30,3,True)
shape('Phone screen',[(-22,-90),(22,-90),(22,-15),(-22,-15)],PAPER,phone,31,2)
shape('Phone screen header',[(-22,-90),(22,-90),(22,-76),(-22,-76)],'#454545',phone,32,0)
for yy in (-69,-44):
    for xx in (-17,4): shape('Screen thumbnail',[(xx,yy),(xx+13,yy),(xx+13,yy+17),(xx,yy+17)],'#cccccc',phone,32,1)
ellipse('Phone home button',0,-5,4,4,PAPER,phone,32,1.5)
grip=group('Phone grip and scrolling thumb',phone)
ellipse('Gripping fingers',-25,-5,9,14,PAPER,grip,33,2.5)
thumb=stroke('Scrolling thumb',[(-22,-6),(-11,-15),(3,-33)],grip,34,11,PAPER,True)
thumbedge=stroke('Thumb upper contour',[(-22,-11),(-12,-22),(3,-37)],grip,34.1,2.4,INK,True)

clockroot=group('Fast clock graphic')
ellipse('Clock face',0,0,106,106,PAPER,clockroot,50,3.2)
for i in range(12):
    a=i*math.tau/12
    stroke('Clock tick',[(90*math.sin(a),-90*math.cos(a)),(98*math.sin(a),-98*math.cos(a))],clockroot,51,2.5)
clockhands=[]
for n,length,w in [('minute',80,4),('hour',55,6)]:
    g=group('Clock '+n,clockroot);stroke(n,[(0,7),(0,-length)],g,52,w);clockhands.append(g)
ellipse('Clock pin',0,0,5,5,INK,clockroot,53,0)
work=text_group('Opening / WORK STARTS NOW', ['WORK STARTS','NOW.'],1270,180,95)
five=text_group('Excuse / JUST FIVE MINUTES',['JUST 5','MINUTES.'],1440,160,95)
later=text_group('Elapsed time / THREE HOURS',['3 HOURS','LATER'],1390,260,76)
need=text_group('Punchline / I NEED A BREAK',['I NEED','A BREAK.'],1320,235,76)
vibration=group('Phone vibration marks')
for side in (-1,1):
    stroke('Vibration',[(side*48,-80),(side*57,-57),(side*46,-30)],vibration,40,3,curved=True)
    stroke('Vibration echo',[(side*66,-84),(side*74,-57),(side*63,-23)],vibration,40,2.5,curved=True)
dust=group('Retreat dust puff')
shape('Grey dust cloud',[(-50,6),(-59,-12),(-47,-26),(-33,-28),(-26,-43),(-6,-46),(9,-34),(26,-37),(37,-21),(52,-17),(54,1),(34,9),(-17,12)],'#cccccc',dust,20,2.5,True)
for x,y in [(-31,-13),(-4,-25),(27,-7)]:stroke('Puff curl',[(x-8,y+3),(x-5,y-4),(x+3,y-6),(x+7,y)],dust,21,2,curved=True)

def curve_set(obj,pts,frame):
    spl=obj.data.splines[0]
    assert len(spl.points)==len(pts)
    for p,(x,y) in zip(spl.points,pts):
        p.co=(x,-y,p.co.z,1);p.keyframe_insert(data_path='co',frame=frame)

def quadratic(a,b,c):
    return [((1-u)**2*a[0]+2*(1-u)*u*b[0]+u*u*c[0],(1-u)**2*a[1]+2*(1-u)*u*b[1]+u*u*c[1]) for u in [i/16 for i in range(17)]]

def pose_actor(a,f,t,x,y,s,angle=0,state='happy',gaze=0,left='down',right=(195,450),seated=False,back=False,run=0,headtilt=0):
    place(a['root'],x,y,s,angle,10 if a is hero else 40);key(a['root'],f)
    place(a['head'],0,0,1,headtilt);key(a['head'],f)
    hands=[(-233,450),right]
    elbows=[(-176,220),(188,220)]
    if left=='point':hands[0]=(-255,-100);elbows[0]=(-251,190)
    if left=='palm':hands[0]=(-284,-33);elbows[0]=(-240,207)
    if left=='stretch':hands[0]=(-282,-127);elbows[0]=(-310,25)
    if left=='support':hands[0]=(210,105);elbows[0]=(-73,273)
    if isinstance(left,tuple):hands[0]=left;elbows[0]=(-130,230)
    if right[0]>280:elbows[1]=(right[0]*.54,180)
    if back:
        hands=[(-235,130+65*math.sin(run)),(235,130-65*math.sin(run))]
        elbows=[(-200,70),(200,70)]
    for i,side in enumerate((-1,1)):
        pts=quadratic((side*143,7),elbows[i],hands[i])
        for obj in a['arms'][i]:curve_set(obj,pts,f)
        place(a['hands'][i],*hands[i]);key(a['hands'][i],f)
        foot=(side*82+(math.sin(run)*45*side if back else 0),655-(70*max(0,math.sin(run)*side) if back else 0))
        knee=(side*80,588)
        if seated:foot=(side*78,594);knee=(side*115,563)
        for ob in a['legs'][i]:curve_set(ob,quadratic((side*82,518),knee,foot),f)
        place(a['shoes'][i],*foot,angle=-side*10);key(a['shoes'][i],f)
    closed=((t+(1.1 if a is friend else 0))%3.7<.13 and t>.2) or state=='tired'
    visible(children(a['normal']),not closed and not back,f)
    visible(children(a['blink']),closed and not back,f)
    visible(children(a['back']),back,f)
    for name,g in a['mouths'].items():visible(children(g),name==state and not back,f)
    for pupil in a['pupils']:
        pupil.location.x=gaze*7;pupil.location.y=12 if a is friend and t>8.4 else (2 if state=='guilty' else 0);key(pupil,f)
    for i,brow in enumerate(a['brows']):
        brow.location.y=7 if state=='open' else (-6 if state=='tired' else (7 if state=='guilty' and i==0 else 0))
        brow.rotation_euler.z=0
        key(brow,f)
    visible(children(a['finger']),left=='point' and not back,f)
    return hands

def to_world(x,y,s,p):return (x+s*p[0],y+s*p[1])

contacts=[]
for f in range(1,901):
    t=(f-1)/30
    # Default layout and stable held pose.
    x=480.;y=460.;s=.67;left='point';right=(195,450);state='happy';gaze=0;seated=False;back=False;tilt=0
    dx=1230;dy=690;ds=.60
    phonepos=(925.,600.);phoneangle=-75.;phonescale=.7;held=False
    cx=960.;cy=540.;cw=1920.
    if 3<=t<6:
        u=ease((t-3.55)/.65);x=mix(480,610,u);left='down';state='guilty';gaze=1
        pickup=((925-x)/s,(600-y)/s)
        right=vec((195,450),pickup,ease((t-3.8)/.6))
        if t>=4.4:
            right=vec(pickup,(245,90),ease((t-4.4)/1.05));held=True
            phonepos=to_world(x,y,s,right);phoneangle=mix(-75,-9,ease((t-4.4)/1.05));phonescale=s
    elif 6<=t<10:
        x=900;y=470;s=.72;right=(235,110);left='point';state='guilty' if t<7 else 'earnest';gaze=-1
        held=True;phonepos=to_world(x,y,s,right);phoneangle=-9;phonescale=s
    elif 10<=t<23:
        x=780;y=475;s=.72;left='support';right=(220,105);seated=True
        dx=1200;dy=760;ds=.75;state='happy';gaze=1
        held=True;phonepos=to_world(x,y,s,right);phoneangle=-10;phonescale=s
        if t>=17.2:state='guilty';gaze=1
        if t>=18:state='open'
        if 19<=t<21:
            cx=790;cy=390;cw=960;state='open' if t<20.15 else 'tired';tilt=0 if t<20.15 else 8
        elif 21<=t<23:
            u=ease((t-21)/.75);cx=mix(790,960,u);cy=mix(390,540,u);cw=mix(960,1920,u)
            state='tired';left='stretch' if t>21.6 else 'support';tilt=8
    elif 23<=t<27:
        x=780;y=465;s=.72;dx=1200;dy=760;ds=.75;left='down';state='tired';gaze=1
        target=((1150-x)/s,(650-y)/s)
        if t<24.1:
            u=ease((t-23.15)/.8);right=vec((220,105),target,u);held=True
            phonepos=to_world(x,y,s,right);phoneangle=mix(-10,-75,u);phonescale=s
        else:
            phonepos=(1150,650);right=vec(target,(195,450),ease((t-24.1)/.55));phoneangle=-75;phonescale=s
            state='earnest';gaze=0;left='palm' if t>=24.65 else 'down'
    elif t>=27:
        dx=1200;dy=760;ds=.75;phonepos=(1150,650);phonescale=.72
        u=ease((t-27)/1.20);x=mix(400,470,u);y=mix(465,405,u);s=mix(.72,.06,u)
        back=True;left='down'
    place(desk,dx,dy,ds,z=0);key(desk,f)
    place(chair,790,760,.61,z=4);key(chair,f)
    visible(children(chair),t>=10,f)
    visible(hero['all'],t<28.22,f)
    hands=pose_actor(hero,f,t,x,y,s,state=state,gaze=gaze,left=left,right=right,seated=seated,back=back,run=(t-27)*22,headtilt=tilt)
    # Facial visibility is set by pose_actor; hide the entire departed actor afterwards.
    if t>=28.22:visible(hero['all'],False,f)
    friend_on=6<=t<9.7
    fx=mix(-630,35,ease((t-6)/.48)) if t<8.9 else mix(35,-650,ease((t-8.9)/.65))
    pose_actor(friend,f,t,fx,580,1.25,angle=57,state='guilty',gaze=1 if t<8.5 else -1)
    visible(friend['all'],friend_on,f)
    # Reapply the expression after whole-group visibility on entry.
    if friend_on:pose_actor(friend,f,t,fx,580,1.25,angle=57,state='guilty',gaze=1 if t<8.5 else -1)
    jitter=3*math.sin(t*90) if 3.05<t<3.65 else 0
    place(phone,phonepos[0]+jitter,phonepos[1],phonescale,phoneangle,35);key(phone,f)
    visible(children(grip),held,f)
    thumbshift=8*math.sin(t*9) if 10<=t<17.6 else 0
    for ob in (thumb,thumbedge):ob.location.y=thumbshift;key(ob,f)
    place(vibration,*phonepos,phonescale,phoneangle,35);key(vibration,f)
    visible(children(vibration),3.05<t<3.65,f)
    if held:
        hp=to_world(x,y,s,hands[1]);contacts.append({'frame':f,'hand':hp,'phone_grip':phonepos,'error_px':math.dist(hp,phonepos)})
    place(clockroot,1700,220,1 if t>10.45 else ease((t-10)/.45));key(clockroot,f)
    visible(children(clockroot),10<=t<15,f)
    for i,g in enumerate(clockhands):g.rotation_euler.z=-(t-10)**2*(5 if i==0 else .7);key(g,f)
    for g,on in [(work,t<3 or t>=27),(five,6.8<=t<10),(later,15<=t<19),(need,24.9<=t<27)]:visible(children(g),on,f)
    pop=1+.12*math.sin((t-15)*15)*math.exp(-(t-15)*7) if t>=15 else 1
    place(later,1390,210,pop);key(later,f)
    place(dust,470,453,1+2*max(0,t-28.22));key(dust,f)
    visible(children(dust),28.22<=t<28.7,f)
    camera.location=(cx,-cy,1000);cd.ortho_scale=cw;key(camera,f);cd.keyframe_insert(data_path='ortho_scale',frame=f)
    if f%150==0:print('BAKED',f,flush=True)

for action in bpy.data.actions:
    for slot in action.slots:
        for layer in action.layers:
            for strip in layer.strips:
                bag=strip.channelbag(slot)
                if bag:
                    for fc in bag.fcurves:
                        for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path in ('hide_render','hide_viewport') else 'LINEAR'
for f,title in [(1,'Work starts now'),(91,'Phone distraction'),(181,'Just five minutes'),(301,'Scrolling'),(451,'Three hours later'),(571,'Realization'),(691,'I need a break'),(811,'Retreat')]:scene.timeline_markers.new(title,frame=f)
assert len(contacts)>400 and max(c['error_px'] for c in contacts)<1e-6
scene['Reference']='/Users/samikd/Downloads/Meesha Final.mp4'
scene['Direction']='Direct reconstruction of supplied character/environment designs; original 30-second story. Editable flat curves, fills, expressions and transforms.'
scene['Source character SHA256']=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
scene['Pipeline helpers SHA256']=hashlib.sha256(HELPERS.read_bytes()).hexdigest()
scene.frame_set(1)
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'just-five-minutes.blend'))
(OUT/'build-checks.json').write_text(json.dumps({'frames':900,'fps':30,'width':1920,'height':1080,'hand_phone_samples':len(contacts),'maximum_contact_error_px':max(c['error_px'] for c in contacts),'source_character_sha256':scene['Source character SHA256'],'helper_sha256':scene['Pipeline helpers SHA256'],'objects':len(art.objects)},indent=2)+'\n')
(OUT/'phone-contacts.json').write_text(json.dumps(contacts,indent=2)+'\n')
if '--samples' in sys.argv:
    for f in [31,112,165,225,345,465,555,600,657,759,828,881]:
        scene.frame_set(f);scene.render.filepath=str(OUT/f'stills/frame-{f:04}.png');bpy.ops.render.render(write_still=True)
print('BUILD_COMPLETE',flush=True)
