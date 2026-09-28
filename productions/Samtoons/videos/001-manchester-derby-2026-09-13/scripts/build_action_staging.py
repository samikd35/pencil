"""Native S02/S08/S10 representative staging, using the approved S01 construction.
Run setup(), red_contact(), red_decision(), late_save(), ending(), finish() visibly.
These excerpts settle action staging, not full-film timing or final dialogue.
"""
from pathlib import Path
import bpy, ast, math, json, hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'artifacts/staging-v003'
base={'__file__':str(ROOT/'scripts/build_staging.py')}
exec(compile((ROOT/'scripts/build_staging.py').read_text(),base['__file__'],'exec'),base)
# Reuse the approved driver/neck/keying functions without running the old revision.
source=ROOT/'scripts/revise_neck_motion.py'; tree=ast.parse(source.read_text())
keep={'keys','neck'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in keep],type_ignores=[]),str(source),'exec'))
poly,line,empty,mat,rect,text,oval,limb,vis=[base[k] for k in ('poly','line','empty','mat','rect','text','oval','driven_limb','visibility')]
ink='#171e27'; allactors=[]; scenes=[]; maps={}; sheets={}
bounds=json.loads((ROOT/'assets/art-v003/drawing-bounds.json').read_text())

def vis(obj,visible,f):
    base['visibility'](obj,visible,f)
    # The reused polygon helper creates a sibling outline; show/hide both surfaces.
    if obj.type=='MESH':
        stem,sep,suffix=obj.name.rpartition('.')
        name=(stem+' outline.'+suffix) if sep and suffix.isdigit() else obj.name+' outline'
        edge=bpy.data.objects.get(name)
        if edge and edge.parent==obj.parent:base['visibility'](edge,visible,f)

def setup():
    assert bpy.data.filepath.endswith('staging-v002/s01-neck-motion-v003.blend') and not bpy.data.is_dirty
    assert not bpy.app.background and bpy.context.window
    for fn,data in bounds.items():
        im=bpy.data.images.load(str(ROOT/'assets/art-v003'/fn));im.pack()
        m=bpy.data.materials['Registered facial drawings v002'].copy();m.name='S02–S10 '+fn
        next(n for n in m.node_tree.nodes if n.type=='TEX_IMAGE').image=im
        sheets[fn]=m
    OUT.mkdir(exist_ok=True)

def scene(name,frames,goal=False):
    s=bpy.data.scenes.new(name);bpy.context.window.scene=s;scenes.append(s)
    col=bpy.data.collections.new(name+' / artwork');s.collection.children.link(col)
    base.update(s=s,skin=col,ink=mat(ink),font=next(f for f in bpy.data.fonts if f.filepath.endswith('Arial Bold.ttf')))
    old=bpy.data.scenes['Samtoons S01 — Morning Pep']
    # Link only the approved stadium, not its greeting-specific cast or dugout.
    prefixes=('Sky','Roof','Stand rear','Crowd /','Old Trafford ribbon','Stadium sign','Advertising rail','Samtoons original board','Pitch','Mowing stripe','Touchline')
    for o in old.objects:
        if o.name.startswith(prefixes):col.objects.link(o)
    s.world=old.world;s.view_settings.view_transform='Standard';s.view_settings.look='None'
    s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16
    s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=50
    s.render.fps=24;s.render.fps_base=1;s.frame_start=1;s.frame_end=frames;s.render.use_sequencer=False
    s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
    d=bpy.data.cameras.new(name+' camera');d.type='ORTHO';d.ortho_scale=16
    cam=bpy.data.objects.new(name+' camera',d);col.objects.link(cam);cam.location=(0,0,30);s.camera=cam
    rect(name+' / caption strip',-8,-4.5,16,.75,8,'#172732',outline=False)
    text(name+' / review label','ACTION STAGING · DIALOGUE SHOWN AS CAPTIONS',-7.5,4.02,8,.16,'#fff5e5',align='LEFT')
    text(name+' / channel','SAMTOONS',6.9,4.02,8,.20,'#fff5e5')
    s['Review scope']='Representative action staging excerpts; final dialogue and complete 150-second animatic remain pending.'
    if goal:
        # Front view: supporting defenders retain the shot's blocked route to goal.
        for x in [3.0+i*.32 for i in range(17)]:line('Goal / mesh',[(x,-3.05),(x,1.20)],-4.2,'#b2d6b4',.008)
        for y in [-3.05+i*.30 for i in range(15)]:line('Goal / mesh',[(3,y),(8,y)],-4.2,'#b2d6b4',.008)
        line('Goal / frame',[(3,-3.05),(3,1.25),(8,1.25),(8,-3.05)],-3.8,'#fff8e9',.065)
        line('Goal / line',[(2.8,-3.1),(8,-3.1)],-4,'#fff8e9',.025)
    for a in bpy.context.screen.areas:
        if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.shading.type='MATERIAL';a.spaces.active.overlay.show_overlays=False
    return s

def face(name,who,i,head,flip=False):
    fn=next(fn for fn,d in bounds.items() if who in d['rows']);data=bounds[fn];W,H=data['size'];boxes=data['rows'][who]
    l,t,r,b=boxes[i]
    # Skull-top and left edge are registration landmarks. Crop width/height is fixed per person.
    wpx=max(q[2]-q[0] for q in boxes)+4;hpx=max(q[3]-q[1] for q in boxes)+2
    l-=2;t-=1;r=l+wpx;b=t+hpx
    height=1.76;w=height*wpx/hpx
    vs=[(-w/2,-.32,.65),(w/2,-.32,.65),(w/2,1.44,.65),(-w/2,1.44,.65)]
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],[(0,1,2,3)]);me.materials.append(sheets[fn]);uv=me.uv_layers.new()
    u0,u1=l/W,r/W;v0,v1=1-b/H,1-t/H
    coords=[(u0,v0),(u1,v0),(u1,v1),(u0,v1)]
    if flip:coords=[(u1,v0),(u0,v0),(u0,v1),(u1,v1)]
    for k,xy in enumerate(coords):uv.data[k].uv=xy
    ob=bpy.data.objects.new(name,me);base['skin'].objects.link(ob);ob.parent=head;return ob

def expression(a,changes):
    for f,index in changes:
        for i,o in enumerate(a['faces']):vis(o,index==i,f)

def actor(tag,who,x,y,scale=1,kit='city',flip=False):
    skincolor={'Bruno':'#eeb28b','Foden':'#efb58c','Oliver':'#e7ae8b','Carrick':'#e0a787','Donnarumma':'#d7986f','Mbeumo':'#a96038'}[who]
    shirt={'city':'#8fcee4','united':'#cb3442','ref':'#e1ed45','coach':'#293747','keeper':'#c63caa'}[kit]
    root=empty(tag+' / ROOT',(x,y,0));root.scale=(scale,scale,scale)
    upper=empty(tag+' / upper',(0,0,0),root);head=empty(tag+' / HEAD',(0,1.96,0),upper)
    a={'name':tag,'who':who,'root':root,'upper':upper,'head':head,'kit':kit,'scale':scale}
    a['faces']=[face(tag+' / face '+str(i),who,i,head,flip) for i in range(3)]
    expression(a,[(1,0)])
    torso=[(-.25,1.67),(.25,1.67),(.72,1.4),(.70,1.05),(.51,.9),(.46,-.23),(.48,-.57),(.08,-.61),(0,-.26),(-.08,-.61),(-.48,-.57),(-.46,-.23),(-.51,.9),(-.70,1.05),(-.72,1.4)]
    poly(tag+' / torso',torso,.24,shirt,upper)
    shorts='#293747' if kit in ('ref','coach') else ('#be36a3' if kit=='keeper' else '#f3f1e7')
    poly(tag+' / shorts',[(-.46,.02),(.46,.02),(.48,-.57),(.08,-.61),(0,-.26),(-.08,-.61),(-.48,-.57)],.265,shorts,upper,False)
    if kit in ('city','united','keeper'):
        text(tag+' / kit sponsor','SNAPDRAGON' if kit=='united' else 'ETIHAD',0,.9,.32,.13 if kit=='united' else .17,'#ffffff',upper)
        number={'Bruno':'8','Foden':'47','Donnarumma':'1','Mbeumo':'19'}.get(who,'')
        text(tag+' / number',number,-.28,-.28,.32,.21,ink,upper)
    else:
        line(tag+' / zip',[(0,.1),(0,1.5)],.32,'#677786',.012,upper)
    poly(tag+' / crest',oval(.32,1.28,.10,.10),.33,'#eadbb0' if kit=='united' else '#d0e9ee',upper)
    if kit=='united':
        rect(tag+' / captain band',-.88,1.03,.22,.25,.37,'#f4ede0',upper,False) if who=='Bruno' else None
    a['neck_anchors'],a['neck']=neck(tag,upper,head,skincolor)
    # Reused world-anchor neck follows scaled/rotated actors; Z follows the actor as well.
    for ob in [a['neck'],*[o for o in base['skin'].objects if o.name.startswith(tag+' / neck ') and o.type=='CURVE']]:
        depth=.48 if ob==a['neck'] else .50
        ob.location.z=scale*depth-depth
    line(tag+' / collar',[(-.32,1.65),(-.22,1.52),(0,1.45),(.22,1.52),(.32,1.65)],.73,'#f4eeeb' if kit in ('city','united') else '#243243',.032,upper)
    for side in (-1,1):
        for part,loc,parent in [('hip',(side*.25,-.37,0),root),('knee',(side*.31,-1.18,0),root),('foot',(side*.39,-2.22,0),root),('shoulder',(side*.58,1.25,0),upper),('elbow',(side*.85,.63,0),upper),('hand',(side*.79,.04,0),upper)]:
            a[f'{part}{side}']=empty(tag+f' / {part} {side}',loc,parent)
        limb(tag+f' / leg {side}',[a[f'hip{side}'],a[f'knee{side}'],a[f'foot{side}']],.145,skincolor if kit in ('city','united','ref') else shorts,root,.05)
        # Shin follows knee/ankle controls, avoiding the old fixed sock path during kicks.
        mid=empty(tag+f' / sock top {side}',parent=root)
        for axis in (0,1):
            d=mid.driver_add('location',axis).driver
            for vname,target in [('k',a[f'knee{side}']),('f',a[f'foot{side}'])]:
                v=d.variables.new();v.name=vname;v.type='TRANSFORMS';v.targets[0].id=target;v.targets[0].transform_type=('LOC_X','LOC_Y')[axis];v.targets[0].transform_space='LOCAL_SPACE'
            d.expression='.7*k+.3*f'
        sock='#a7d9e7' if kit=='city' else ('#bd36a3' if kit=='keeper' else '#232936')
        limb(tag+f' / sock {side}',[mid,a[f'foot{side}'],a[f'foot{side}']],.15,sock,root,.15)
        poly(tag+' / boot',[(-.22,-.1),(.10,-.1),(.34,-.15),(.38,-.24),(-.24,-.24)],.3,'#f3eade' if kit=='keeper' else '#242b38',a[f'foot{side}'])
        line(tag+' / sole',[(-.21,-.23),(.35,-.23)],.34,'#f47a9d',.022,a[f'foot{side}'])
        limb(tag+f' / arm {side}',[a[f'shoulder{side}'],a[f'elbow{side}'],a[f'hand{side}']],.125,shirt if kit in ('coach','keeper') else skincolor,upper,.13)
        poly(tag+' / sleeve',[(side*.40,1.53),(side*.77,1.4),(side*.84,1.07),(side*.55,1.00)],.32,shirt,upper)
        hand=a[f'hand{side}'];hc='#dceaf0' if kit=='keeper' else skincolor
        poly(tag+' / hand',[(-.10,.10),(.07,.10),(.13,-.02),(.13,-.17),(.08,-.24),(0,-.25),(-.07,-.20),(-.09,-.10),(-.13,-.02)],.75,hc,hand)
        poly(tag+' / thumb',oval(-.10,-.01,.06,.10),.79,hc,hand)
        for xx in (-.02,.03,.08):line(tag+' / finger',[(xx,-.08),(xx,-.19)],.80,'#714c40' if kit!='keeper' else '#556b7c',.008,hand)
    allactors.append(a);return a

def pose(a,part,values):keys(a[part],'location',[(f,(*xy,0)) for f,xy in values])
def rot(a,part,values):keys(a[part],'rotation_euler',[(f,(0,0,angle)) for f,angle in values])
def caption(s,lines):
    for begin,end,message in lines:
        o=text(s.name+' / dialogue',message,0,-4.10,8.2,.29,'#fff5e5')
        vis(o,False,1);vis(o,True,begin);vis(o,False,end+1)
def score(s,label):text(s.name+' / clock',label,0,3.46,8,.26,'#fff8e9')
def ball(name,x,y,z=.85,parent=None):
    e=empty(name,(x,y,z),parent);poly(name+' / white',oval(0,0,.23,.23),0,'#fff9e9',e)
    poly(name+' / panel',[(.09*math.cos(i*math.tau/5),.09*math.sin(i*math.tau/5)) for i in range(5)],.01,ink,e)
    for t in range(5):
        ang=t*math.tau/5;line(name+' / seam',[(.09*math.cos(ang),.09*math.sin(ang)),(.22*math.cos(ang),.22*math.sin(ang))],.015,ink,.01,e)
    return e
def rod(name,parent):
    r=empty(name,(0,0,0),parent)
    line(name+' / pole',[(0,0),(.5,1.2),(1,2.5),(1.45,3.6)],.9,'#725a36',.025,r)
    poly(name+' / reel',oval(.14,.35,.13,.13),.91,'#98a8b5',r)
    return r

def red_contact():
    s=scene('S02a · grounded kick',72);score(s,"23′   UNITED 0–0 CITY")
    f=actor('S02a Foden','Foden',-1.75,-2.85,.62,'city')
    b=actor('S02a Bruno','Bruno',.0,-1.75,.68,'united',True)
    # Seated on turf: legs fold separately; head counter-rotates toward Bruno.
    rot(f,'root',[(1,1.02),(14,1.00),(25,.92),(34,.96),(48,1.02),(72,1.02)])
    rot(f,'head',[(1,-.30),(28,-.18),(43,-.28),(72,-.30)])
    pose(f,'knee-1',[(1,(-.35,-.9)),(26,(-.55,-1.1)),(40,(-.35,-.9)),(72,(-.35,-.9))])
    pose(f,'foot-1',[(1,(-.20,-1.3)),(26,(-.6,-2.05)),(38,(-.25,-1.4)),(72,(-.20,-1.3))])
    pose(f,'knee1',[(1,(.3,-1.0)),(24,(.05,-.7)),(30,(.65,-1.05)),(38,(.3,-.95)),(72,(.3,-1.0))])
    pose(f,'foot1',[(1,(.25,-1.4)),(22,(.75,-1.2)),(30,(1.1,-1.9)),(35,(1.05,-1.85)),(47,(.30,-1.4)),(72,(.25,-1.4))])
    pose(f,'hand-1',[(1,(-.7,.0)),(72,(-.7,.0))]);pose(f,'hand1',[(1,(.7,.30)),(29,(1,.6)),(55,(.8,.45)),(72,(.8,.45))])
    expression(f,[(1,0),(24,1),(44,0)])
    rot(b,'upper',[(1,-.13),(23,-.18),(34,-.32),(46,.15),(72,.12)])
    pose(b,'hand-1',[(1,(-.75,.4)),(29,(-.9,.75)),(41,(-1.20,1.2)),(72,(-1.2,1.2))])
    pose(b,'hand1',[(1,(.79,.04)),(34,(.9,.6)),(46,(1.18,1.2)),(72,(1.18,1.2))])
    expression(b,[(1,0),(32,2),(45,1)])
    ball('S02a / loose ball',-2.7,-3.3)
    caption(s,[(1,27,'23′ · The tussle'),(28,72,'BRUNO: “REF!”')]);maps['S02a']={'Bruno':b,'Foden':f}
    s['events']=json.dumps({'kick_out':30,'reaction':34})

def red_decision():
    s=scene('S02b · resolved',120);score(s,"23′   UNITED 0–0 CITY   ·   11 v 10")
    b=actor('S02b Bruno','Bruno',-3.4,-1.30,.72,'united')
    o=actor('S02b Oliver','Oliver',.1,-1.3,.72,'ref',True)
    f=actor('S02b Foden','Foden',4.6,-1.35,.68,'city',True)
    for a in (b,o,f):
        rot(a,'upper',[(1,0),(33,-.03),(53,.02),(75,0),(120,0)])
    # Complaint is held from its wrist, so it cannot slide away from the fingers.
    paper=empty('S02b / complaint form',(0,.05,.1),b['hand1'])
    rect('S02b / paper',-.26,-.12,.87,1.16,.9,'#fff6df',paper)
    text('S02b / form title','COMPLAINT',.18,.81,.95,.115,ink,paper)
    for y in (.62,.48,.34,.20):line('S02b / writing',[(-.1,y),(.47,y)],.95,'#869299',.009,paper)
    pose(b,'hand1',[(1,(.85,.40)),(21,(1.05,.8)),(41,(1.10,.87)),(120,(1.10,.87))])
    expression(b,[(1,1),(36,0),(78,1),(100,0)])
    card=empty('S02b / red card',(0,.1,.1),o['hand1']);rect('S02b / card',-.18,-.02,.36,.56,.9,'#f63b48',card)
    pose(o,'hand1',[(1,(.80,.1)),(20,(1.0,2.30)),(28,(1.05,2.25)),(57,(1.05,2.25)),(82,(.9,.7)),(120,(.9,.7))])
    pose(o,'elbow1',[(1,(.85,.63)),(20,(1.1,1.7)),(57,(1.1,1.7)),(82,(1.05,1)),(120,(1.05,1))])
    stamp=empty('S02b / RESOLVED',(0,2.10,3));rect('S02b / stamp block',-1.05,-.25,2.1,.5,.01,'#e5f1d9',stamp)
    text('S02b / stamp word','RESOLVED',0,0,.05,.28,'#338253',stamp)
    for ob in [stamp,*stamp.children]:vis(ob,False,1);vis(ob,True,38)
    keys(stamp,'scale',[(38,(1.25,1.25,1)),(44,(.98,.98,1)),(52,(1,1,1))])
    fishing=rod('S02b / fishing rod',f['hand1'])
    for ob in [fishing,*fishing.children]:vis(ob,False,1);vis(ob,True,79)
    pose(f,'hand1',[(1,(.79,.04)),(76,(.79,.04)),(88,(1.0,.42)),(98,(.90,.35)),(120,(.90,.35))])
    expression(f,[(1,0),(80,1),(103,2)])
    caption(s,[(1,37,'BRUNO: “One less problem.”'),(38,77,'RESOLVED.'),(78,120,'FODEN: “Fine. I’m going fishing.”')]);maps['S02b']={'Bruno':b,'Oliver':o,'Foden':f}
    s['events']=json.dumps({'red_card':20,'stamp':38,'fishing_prop':79})

def supporting_back(name,x,y,number):
    r=empty(name,(x,y,-1.5));r.scale=(.42,.42,.42)
    poly(name+' / head',oval(0,1.45,.35,.43),.2,'#d1a07c',r)
    poly(name+' / hair',oval(0,1.66,.36,.24),.3,'#302d2e',r)
    poly(name+' / shirt',[(-.25,1.1),(.25,1.1),(.62,.8),(.40,-.30),(-.40,-.30),(-.62,.8)],.4,'#8fcee4',r)
    text(name+' / number',str(number),0,.45,.45,.45,ink,r)
    for side in (-1,1):
        line(name+' / shorts',[(side*.2,-.25),(side*.23,-.7)],.3,'#f4f1e6',.18,r)
        line(name+' / leg',[(side*.23,-.7),(side*.4,-1.6)],.2,'#d1a07c',.13,r)
        line(name+' / sock',[(side*.31,-1.1),(side*.4,-1.65)],.3,'#a7d9e7',.13,r)
        line(name+' / arm',[(side*.5,.85),(side*.75,.1)],.25,'#d1a07c',.12,r)
    return r

def late_save():
    s=scene('S08 · last hope',144,goal=True);score(s,"90+5′   UNITED 0–1 CITY")
    supporting_back('S08 Gvardiol 24',-.1,-.50,24);supporting_back('S08 Dias 3',1.2,.00,3)
    m=actor('S08 Mbeumo','Mbeumo',-3.8,-1.52,.63,'united')
    d=actor('S08 Donnarumma','Donnarumma',5.15,-1.48,.70,'keeper',True)
    b=actor('S08 Bruno','Bruno',-6.2,-1.3,.43,'united')
    rot(m,'upper',[(1,.06),(13,.20),(25,-.20),(41,-.12),(70,.02),(144,.02)])
    pose(m,'foot1',[(1,(.39,-2.22)),(14,(-.8,-1.7)),(25,(1.15,-2.15)),(36,(1.4,-1.6)),(57,(.55,-2.22)),(144,(.55,-2.22))])
    pose(m,'knee1',[(1,(.31,-1.18)),(14,(-.40,-1.2)),(25,(.6,-1.28)),(36,(.70,-.85)),(57,(.4,-1.18)),(144,(.4,-1.18))])
    pose(m,'hand-1',[(1,(-.79,.04)),(20,(-1.15,.95)),(40,(-.8,.5)),(68,(-1.1,1.2)),(144,(-1.1,1.2))])
    expression(m,[(1,0),(16,1),(53,2)])
    expression(d,[(1,0),(30,1),(67,2)])
    pose(d,'root',[(1,(5.15,-1.48)),(24,(5.15,-1.6)),(33,(4.75,-1.72)),(43,(3.60,-2.10)),(56,(3.32,-2.95)),(68,(3.35,-2.90)),(144,(3.35,-2.90))])
    rot(d,'root',[(1,0),(25,.05),(36,.65),(46,1.30),(56,1.42),(67,1.38),(144,1.38)])
    rot(d,'head',[(1,0),(35,-.20),(53,-.48),(74,-.35),(144,-.35)])
    for side in (-1,1):
        pose(d,f'hand{side}',[(1,(side*.79,.25)),(25,(side*.85,.45)),(44,(side*.20,1.72)),(52,(side*.18,1.48)),(72,(side*.23,1.40)),(144,(side*.23,1.40))])
        pose(d,f'elbow{side}',[(1,(side*.85,.80)),(44,(side*.4,1.3)),(72,(side*.6,.92)),(144,(side*.6,.92))])
    target=empty('S08 / ball grip',(0,1.44,1.0),d['upper'])
    ba=ball('S08 / match ball',-3.05,-2.94)
    # World-space ball flight and captured ball share the same animated contact target.
    for axis in (0,1):
        dr=ba.driver_add('location',axis).driver
        v=dr.variables.new();v.name='g';v.type='TRANSFORMS';v.targets[0].id=target;v.targets[0].transform_type=('LOC_X','LOC_Y')[axis];v.targets[0].transform_space='WORLD_SPACE'
        start=(-3.05,-2.94)[axis];contact=(2.23,-2.27)[axis]
        dr.expression=f'{start} if frame<=25 else ({start}+({contact}-{start})*(frame-25)/19 if frame<44 else g)'
    keys(ba,'rotation_euler',[(1,(0,0,0)),(25,(0,0,0)),(44,(0,0,-8)),(64,(0,0,-8.4)),(144,(0,0,-8.4))])
    # Brief ears are an explicit cartoon overlay; keeper still makes the actual save.
    ears=[]
    for side in (-1,1):
        ears.append(poly('S08 / wolf ears',[(side*.28,.92),(side*.70,1.80),(side*.73,.70)],.60,'#303641',d['head']))
    for ear in ears:vis(ear,False,1);vis(ear,True,68);vis(ear,False,101)
    pose(b,'hand1',[(1,(.79,.04)),(19,(1,1.2)),(37,(1,1.2)),(62,(.79,.04)),(144,(.79,.04))])
    expression(b,[(1,0),(12,1),(60,2)])
    caption(s,[(1,43,'BRUNO: “SURELY NOW—”'),(44,89,'Saved. Again.'),(90,144,'HAALAND (offscreen): “Good wolf.”')]);maps['S08']={'Mbeumo':m,'Donnarumma':d,'Bruno':b,'ball':ba,'grip':target}
    s['events']=json.dumps({'kick':25,'save':44,'wolf':68})

def ending():
    s=scene('S10 · any points with that',336);score(s,'LATER   ·   UNITED 0–1 CITY')
    o=actor('S10 Oliver','Oliver',-2.9,-2.0,.72,'ref')
    c=actor('S10 Carrick','Carrick',1.2,-1.25,.76,'coach',True)
    f=actor('S10 Foden','Foden',6.0,-2.50,.56,'city',True)
    # Kneeling, feet folded behind with both knees planted. Upper body does the sobbing.
    for side in (-1,1):
        o[f'knee{side}'].location=(side*.43,-1.15,0);o[f'foot{side}'].location=(side*.85,-1.1,0)
        f[f'knee{side}'].location=(side*.55,-.8,0);f[f'foot{side}'].location=(side*.85,-1.05,0)
    rot(o,'upper',[(1,-.05),(19,-.15),(29,.04),(41,-.14),(53,.02),(65,-.15),(77,.01),(93,-.13),(109,.01),(125,-.13),(141,.01),(157,-.13),(173,.01),(193,-.12),(217,.0),(245,-.12),(269,.0),(301,-.1),(336,.0)])
    rot(o,'head',[(1,0),(18,.10),(30,-.08),(42,.12),(54,-.06),(66,.10),(90,-.08),(114,.10),(138,-.08),(162,.1),(186,-.08),(210,.10),(240,-.08),(276,.10),(306,-.08),(336,.1)])
    for side in (-1,1):
        pose(o,f'hand{side}',[(1,(side*.6,.7)),(24,(side*.65,1.4)),(45,(side*.56,1.22)),(75,(side*.62,1.42)),(115,(side*.55,1.23)),(155,(side*.63,1.4)),(195,(side*.55,1.24)),(235,(side*.6,1.4)),(275,(side*.55,1.23)),(336,(side*.60,1.4))])
    expression(o,[(1,1),(20,2)]);expression(c,[(1,0),(88,1),(142,0),(160,2),(164,0)])
    pose(c,'hand1',[(1,(.79,.04)),(39,(.79,.04)),(58,(.84,1.03)),(68,(.80,.98)),(336,(.80,.98))])
    umb=empty('S10 / umbrella',(0,0,.9),c['hand1'])
    line('S10 / umbrella shaft',[(0,-.1),(0,2.40)],.03,'#b0bfcb',.025,umb)
    canopy=empty('S10 / canopy',(0,2.15,0),umb)
    points=[(-1.65,0)]+[(1.65*math.cos(i*math.pi/32),.88*math.sin(i*math.pi/32)) for i in range(32,-1,-1)]+[(1.65,0),(.83,.13),(0,0),(-.83,.13)]
    poly('S10 / umbrella fabric',points,.05,'#c53b48',canopy)
    for xx in (-1.65,-.83,0,.83,1.65):line('S10 / umbrella ribs',[(0,.88),(xx,.08)],.07,'#7a2535',.012,canopy)
    keys(canopy,'scale',[(1,(.02,1,1)),(47,(.02,1,1)),(57,(1.05,1,1)),(64,(.98,1,1)),(72,(1,1,1)),(336,(1,1,1))])
    for ob in [umb,*umb.children,canopy,*canopy.children]:vis(ob,False,1);vis(ob,True,45)
    # Two continuously deforming water streams start at the head's actual eye anchors.
    streams=[]
    for side in (-1,1):
        eye=empty('S10 / eye fountain '+str(side),(side*.30,.55,0),o['head'])
        ob=line('S10 / tears '+str(side),[(0,0)]*18,1.1,'#a9e7f1',.05)
        for i,p in enumerate(ob.data.splines[0].points):
            t=i/17
            for ax,letter in enumerate('XY'):
                dr=p.driver_add('co',ax).driver;v=dr.variables.new();v.name='eye';v.type='TRANSFORMS';v.targets[0].id=eye;v.targets[0].transform_type='LOC_'+letter;v.targets[0].transform_space='WORLD_SPACE'
                dr.expression=f'eye+{side}*{t}*2.2' if ax==0 else f'eye+{2.4*t-5.3*t*t}+.035*sin(frame*.65+{i})'
        vis(ob,False,1);vis(ob,True,23);streams.append(ob)
    # Pool grows under the tears; native ripples continue into the fishing payoff.
    pool=empty('S10 / flood',(0,-3.50,-.8));poly('S10 / flood water',oval(0,0,7.8,.7),0,'#82c8dd',pool)
    keys(pool,'scale',[(1,(.01,.1,1)),(25,(.10,.25,1)),(96,(.6,.7,1)),(180,(1,1,1)),(336,(1,1,1))])
    for j in range(10):
        ripple=line('S10 / ripple',[(-.38,0),(0,.035),(.38,0)],.02,'#d4f3f3',.012,pool);ripple.location=( -6.7+j*1.40,(-1)**j*.28,0)
        keys(ripple,'location',[(1,(-6.7+j*1.4,(-1)**j*.28,0)),(160,(-6.4+j*1.4,(-1)**j*.31,0)),(336,(-6.7+j*1.4,(-1)**j*.28,0))])
    pose(f,'hand-1',[(1,(-.65,.62)),(336,(-.65,.62))]);pose(f,'hand1',[(1,(.6,.58)),(250,(.6,.58)),(278,(.6,.68)),(296,(.6,.59)),(336,(.6,.59))])
    fishing=rod('S10 / fishing rod',f['hand-1']);fishing.rotation_euler.z=1.1
    floatob=empty('S10 / float',(3.4,-3.3,1.5));poly('S10 / float red',oval(0,0,.09,.17),0,'#eb5262',floatob)
    line('S10 / fishing line',[(4.2,-.6),(3.4,-3.3)],1.4,'#f8eed8',.012)
    keys(floatob,'location',[(1,(3.4,-3.3,1.5)),(216,(3.4,-3.3,1.5)),(241,(3.4,-3.34,1.5)),(248,(3.4,-3.50,1.5)),(259,(3.4,-3.27,1.5)),(278,(3.4,-3.32,1.5)),(309,(3.4,-3.35,1.5)),(336,(3.4,-3.32,1.5))])
    expression(f,[(1,2),(238,1),(255,2),(262,1),(282,2),(289,1),(314,2)])
    # Start medium on apology; reveal the fishing gag only after the question lands.
    keys(s.camera,'location',[(1,(-1.3,-.1,30)),(151,(-1.3,-.1,30)),(217,(0,0,30)),(336,(0,0,30))])
    keys(s.camera.data,'ortho_scale',[(1,12.2),(151,12.2),(217,16),(336,16)])
    caption(s,[(1,85,'OLIVER: “I’m so, SO sorry!”'),(86,158,'CARRICK: “Any points with that?”'),(159,231,'Still 0–1.'),(232,321,'FODEN: “Keep going, ref. They’re biting.”'),(322,336,'SAMTOONS')])
    # HUD follows the camera translation and scale so captions are always inside frame.
    for ob in list(base['skin'].objects):
        if ob.name.startswith(s.name+' /'):
            ob.parent=s.camera;ob.location.z-=30
    maps['S10']={'Oliver':o,'Carrick':c,'Foden':f}
    s['events']=json.dumps({'tears':23,'umbrella':57,'question':86,'fishing_reveal':217,'float_dip':248})

def refine():
    """Apply the staging inspection corrections; retained for reproducible builds."""
    s=bpy.data.scenes['S10 · any points with that'];bpy.context.window.scene=s
    for ob in s.objects:
        if ob.parent==s.camera:
            # Keep the caption and clock safely framed through the pull-back.
            for prop,axis,initial in [('location',0,ob.location.x),('location',1,ob.location.y),('scale',0,1.),('scale',1,1.)]:
                if ob.animation_data and ob.animation_data.drivers and any(d.data_path==prop and d.array_index==axis for d in ob.animation_data.drivers):continue
                dr=ob.driver_add(prop,axis).driver;v=dr.variables.new();v.name='zoom';v.type='SINGLE_PROP';v.targets[0].id_type='CAMERA';v.targets[0].id=s.camera.data;v.targets[0].data_path='ortho_scale';dr.expression=f'{initial}*zoom/16'
    s=bpy.data.scenes['S08 · last hope'];bpy.context.window.scene=s
    a=maps['S08'];d=a['Donnarumma'];target=a['grip'];ba=a['ball']
    keys(target,'location',[(1,(-.6,3.8,1)),(44,(-.6,3.8,1)),(52,(-.3,2.1,1)),(67,(0,.95,1)),(79,(0,1.05,1)),(144,(0,1.05,1))])
    for side in (-1,1):
        pose(d,f'hand{side}',[(1,(side*.79,.25)),(25,(side*.85,.45)),(44,(-.6+side*.30,3.90)),(52,(-.3+side*.30,2.2)),(67,(side*.30,1.05)),(79,(side*.30,1.15)),(144,(side*.30,1.15))])
        pose(d,f'elbow{side}',[(1,(side*.85,.80)),(25,(side*.8,.90)),(44,(-.3+side*.4,2.3)),(67,(side*.62,.83)),(144,(side*.62,.83))])
    pose(d,'knee1',[(1,(.31,-1.18)),(25,(.55,-1.03)),(44,(.61,-1.05)),(56,(.75,-1)),(80,(.52,-1.20)),(144,(.52,-1.20))])
    pose(d,'foot1',[(1,(.39,-2.22)),(25,(.65,-2.00)),(44,(1.25,-1.66)),(56,(1.30,-1.4)),(80,(1,-1.60)),(144,(1,-1.60))])
    s.frame_set(44);bpy.context.view_layer.update();contact=target.matrix_world.translation.copy()
    for axis in (0,1):
        dr=ba.animation_data.drivers.find('location',index=axis).driver;start=(-3.05,-2.94)[axis]
        dr.expression=f'{start} if frame<=25 else ({start}+({contact[axis]}-{start})*(frame-25)/19 if frame<44 else g)'
    # The fishing line shares the rod's tip and float endpoints through movement.
    s=bpy.data.scenes['S10 · any points with that'];bpy.context.window.scene=s
    tip=empty('S10 / fishing tip',(1.45,3.6,0),bpy.data.objects['S10 / fishing rod'])
    ln=bpy.data.objects['S10 / fishing line'];fl=bpy.data.objects['S10 / float']
    for i,target in enumerate((tip,fl)):
        for axis,letter in enumerate('XY'):
            dr=ln.data.splines[0].points[i].driver_add('co',axis).driver;v=dr.variables.new();v.name='end';v.type='TRANSFORMS';v.targets[0].id=target;v.targets[0].transform_type='LOC_'+letter;v.targets[0].transform_space='WORLD_SPACE';dr.expression='end'
    # Crop distant empty pitch in the incident, while retaining full foot contact.
    s=bpy.data.scenes['S02a · grounded kick'];bpy.context.window.scene=s
    s.camera.data.ortho_scale=13.8;s.camera.location=(-1.25,-.70,30)
    for ob in s.objects:
        if ob.name.startswith(s.name+' /'):
            ob.parent=s.camera;ob.location.x*=.8625;ob.location.y*=.8625;ob.location.z-=30;ob.scale=(.8625,.8625,1)
    # Native ground shadows establish contact; they don't follow head/upper acting.
    for sn in scenes:
        bpy.context.window.scene=sn;base['skin']=next(c for c in sn.collection.children if c.name.startswith(sn.name))
        for a in allactors:
            if a['root'].name not in sn.objects:continue
            if a['who']=='Donnarumma':continue
            x=a['root'].location.x;y=a['root'].location.y-a['scale']*(1.2 if (sn.name.startswith('S10') and a['who'] in ('Oliver','Foden')) else 2.42)
            if sn.name.startswith('S02a') and a['who']=='Foden':x=-1.1;y=-3.55
            poly(a['name']+' / turf contact shadow',oval(x,y,.62*a['scale'],.085),-1.4,'#438b60',outline=False)
    return {'save_contact':list(contact),'fishing_line_attached':True}

def finish(native_name='action-staging-v001.blend'):
    # One runnable check covers all moving contacts on every staging frame.
    worst=0.;limb_gap=0.;handle_error=0.;grip_error=0.
    for s in scenes:
        bpy.context.window.scene=s
        actors=[a for a in allactors if a['root'].name in s.objects]
        for frame in range(1,s.frame_end+1):
            s.frame_set(frame);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
            for a in actors:
                ne=a['neck'].evaluated_get(dg)
                for i,k in [(0,'Lbase'),(3,'Ltop'),(4,'Rtop'),(7,'Rbase')]:worst=max(worst,(ne.data.vertices[i].co.xy-a['neck_anchors'][k].matrix_world.translation.xy).length)
                assert sum(not f.hide_render for f in a['faces'])==1,(s.name,frame,a['who'])
                for side in (-1,1):
                    ob=bpy.data.objects[a['name']+f' / arm {side} fill'].evaluated_get(dg)
                    tip=ob.matrix_world@ob.data.splines[0].bezier_points[-1].co
                    limb_gap=max(limb_gap,(tip.xy-a[f'hand{side}'].matrix_world.translation.xy).length)
                    p=ob.data.splines[0].bezier_points
                    expected=p[1].co+(p[2].co-p[0].co)/6
                    handle_error=max(handle_error,(expected-p[1].handle_right).length)
            if s.name.startswith('S08') and frame>=44:
                grip_error=max(grip_error,(maps['S08']['ball'].location.xy-maps['S08']['grip'].matrix_world.translation.xy).length)
        assert all(o.type!='IMAGE' for o in s.objects)
    assert max(worst,limb_gap,handle_error,grip_error)<1e-5,(worst,limb_gap,handle_error,grip_error)
    bpy.context.window.scene=scenes[-1];scenes[-1].frame_set(115)
    assert not (OUT/native_name).exists(),'Preserve the saved staging revision.'
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/native_name))
    checks={'scenes':[{ 'name':s.name,'frames':s.frame_end,'events':json.loads(s['events'])} for s in scenes], 'new_drawings':18,'neck_max_gap':worst,'arm_wrist_max_gap':limb_gap,'handle_driver_error':handle_error,'captured_ball_gap':grip_error,'scope':'Representative S02, S08 and S10 staging, not the complete animatic','sound':'B sparse foreground retained; new cues are audition candidates; final dialogue pending'}
    (OUT/'native-checks.json').write_text(json.dumps(checks,indent=2)+'\n');return checks
