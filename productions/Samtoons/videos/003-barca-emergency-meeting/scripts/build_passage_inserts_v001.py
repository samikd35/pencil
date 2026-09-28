"""Two rough editorial inserts for S05–S08; run in the visible Blender session.

Reuse the selected native layout primitives. These inserts establish the plan
and the call, not new approved character performances.
"""
import importlib.util, math
from pathlib import Path
import bpy

V=Path(__file__).resolve().parents[1]
O=V/'artifacts/staging-v001/passage-v001'
spec=importlib.util.spec_from_file_location('passage_layout',V/'scripts/build_layouts_v001.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
INK,CREAM,GOLD,RED,NAVY='#202f40','#fff3d6','#eeb957','#be374a','#253e58'

def key(o,prop,values):
    for f,val in values:
        setattr(o,prop,val);o.keyframe_insert(data_path=prop,frame=f)

def appear(o,start,end):
    for f,hide in [(1,True),(start,False),(end+1,True)]:
        o.hide_render=hide;o.hide_viewport=hide
        o.keyframe_insert(data_path='hide_render',frame=f)
        o.keyframe_insert(data_path='hide_viewport',frame=f)

def label(body,x,y,size=.35,color=CREAM,z=3):
    o=d.text(body,x,y,size,color,z);o.data.align_x='CENTER';return o

def caption(body,start,end):
    bar=d.rect('dialogue strip',-8,-4.5,16,.63,INK,5)
    tx=label(body,0,-4.27,.265,CREAM,5.1)
    appear(bar,start,end);appear(tx,start,end)

def scene(name,frames,bg):
    s=d.scene(name,bg);s.name=name;s.frame_end=frames;s.render.fps=24
    s['purpose']='Rough story coverage for continuous passage; not character performance approval'
    return s

def marker(name,x,y,color,number):
    root=bpy.data.objects.new(name+' control',None);d.SCENE.collection.objects.link(root)
    for o in [d.disc(name+' edge',0,0,.34,INK,1.5),d.disc(name,0,0,.29,color,1.6),label(number,0,-.10,.27,CREAM,1.7)]:o.parent=root
    root.location=(x,y,0);return root

def build_plan():
    s=scene('S003_Passage_S05_Plan_v001',168,NAVY)
    d.rect('board frame',-7.2,-3.1,14.4,6.65,'#bd9862',0)
    d.rect('magnetic surface',-7,-2.9,14,6.25,'#264e49',.1)
    label('HOW TO BEAT BARCELONA',0,2.72,.5)
    d.line('pitch outline',[(-6.5,-2.5),(-6.5,2),(6.5,2),(6.5,-2.5),(-6.5,-2.5)],CREAM,.023,.2)
    d.line('halfway',[(0,-2.5),(0,2)],CREAM,.017,.2)
    d.line('goal',[(5.75,-1.1),(5.75,.6),(6.5,.6)],CREAM,.023,.2)
    marker('Raphinha',-3,.25,RED,'11');label('RAPHINHA',-3,-1.02,.27)
    marker('Pedri',-1.3,-1.52,RED,'8');label('PEDRI',-1.3,-2.13,.25)
    marker('Yamal',3,.2,RED,'19');label('YAMAL',3,-.48,.27)
    for i,(start,end) in enumerate([((-5.2,1.22),(-3.8,.7)),((-1.3,1.32),(-2.35,.8)),((-4.7,-1.5),(-3.65,-.42))]):
        o=marker('Defender '+str(i+1),*start,'#5f96ba','D')
        key(o,'location',[(1,(*start,0)),(55+i*7,(*start,0)),(95+i*7,(*end,0)),(168,(*end,0))])
    ring=d.line('circle Raphinha',[(-3+.56*math.cos(i*math.tau/64),.25+.56*math.sin(i*math.tau/64)) for i in range(65)],GOLD,.027,1.9)
    appear(ring,45,168)
    channel=d.line('unwatched channel',[(1.7,-1.75),(4.4,-1.75),(4.4,1.3),(1.7,1.3),(1.7,-1.75)],GOLD,.025,1.1)
    appear(channel,126,168)
    caption('PÉREZ (OFFSCREEN): Simple. Stop Raphinha. Put everyone on him.',19,126)
    s.frame_set(140);return s

def build_call_link():
    s=scene('S003_Passage_S08_Call_Link_v001',192,'#667c8c')
    for x in [-7,-3,1,5]:d.line('office wall seam',[(x,-4.5),(x,4.5)],'#415668',.017,-.5)
    d.poly('desk',[(-8,-4.5),(8,-4.5),(8,-.9),(-8,-.9)],'#b58c61',-.1)
    # ponytail: prop insert covers the missing decision; ensemble acting remains a later shot pass.
    d.rect('failed plan frame',1.4,-.1,5.7,3.5,INK,.2)
    d.rect('failed plan paper',1.59,.08,5.32,3.12,CREAM,.3)
    label('STOP RAPHINHA',4.25,2.65,.37,INK)
    for x,y,col in [(3.55,1.2,RED),(2.85,1.62,NAVY),(4.2,1.65,NAVY),(3.65,.4,NAVY),(6.15,1.,RED)]:d.disc('plan magnet',x,y,.21,col,.5)
    for pts in [[(2.15,.4),(6.45,2.2)],[(2.15,2.2),(6.45,.4)]]:
        o=d.line('cross out plan',pts,RED,.075,.8);appear(o,14,192)
    d.rect('archive result',1.4,-2.95,5.7,2.0,'#dfc596',.3)
    label('BAYERN 8 – 2 BARCELONA',4.25,-1.7,.36,INK)
    label('2020',4.25,-2.45,.35,INK)
    d.rect('call monitor bezel',-7.4,-2.7,8.1,6.1,INK,1)
    d.rect('call monitor screen',-7.2,-2.5,7.7,5.7,'#152936',1.1)
    d.rect('monitor stand',-3.8,-3.25,.9,.55,INK,1.1)
    d.rect('monitor foot',-5.1,-3.4,3.5,.16,INK,1.1)
    label('BAYERN',-3.35,.65,.6,CREAM,1.5)
    label('Connecting',-3.35,-.32,.35,GOLD,1.5)
    for i in range(3):
        o=d.disc('connection dot',-3.85+.5*i,-1.1,.06,GOLD,1.5);appear(o,138+9*i,192)
    # Small camera push commits attention to the call before the performance cut.
    key(s.camera,'location',[(1,(0,0,25)),(114,(0,0,25)),(184,(-.22,-.08,25))])
    key(s.camera.data,'ortho_scale',[(1,16),(114,16),(184,15.2)])
    caption("PÉREZ (OFFSCREEN): Call Bayern. They beat Barcelona eight–two.",19,113)
    caption("PÉREZ (OFFSCREEN): They'll know what to do.",114,169)
    s.frame_set(150);return s

def save(scenes):
    O.mkdir(parents=True,exist_ok=True);path=O/'passage-inserts.blend'
    assert not path.exists(),'Do not overwrite a delivered revision'
    bpy.data.libraries.write(str(path),set(scenes),fake_user=True,compress=True)
    return str(path)
