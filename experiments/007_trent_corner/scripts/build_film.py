"""Author the corner with editable Pencil puppets and one shared spatial view."""
from pathlib import Path
import os
import ast, bpy, math, json, sys, hashlib, random
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts'/os.environ.get('PENCIL_REVISION','film-v001')
OUT.mkdir(parents=True,exist_ok=True);(OUT/'stills').mkdir(exist_ok=True)
SOURCE=ROOT.parent/'001_heavy_box/artifacts/finish-v002/character-and-effects.blend'
HELPERS=ROOT.parent/'003_alisson_winner/scripts/build_film.py'
FPS=24;FRAMES=864;INK='#15282e';PAPER='#fff2d6';GOLD='#f1cf72';RED='#e95358';GREEN='#c3d87c';BLACK=INK
MATS={};GROUPS={};actors={}
names={'clamp','ease','mix','vec','track','rgba','mat','add','poly','line','rect','oval','label','disk','empty','visible','key','character','pose','joint','set_actor'}
nodes=[n for n in ast.parse(HELPERS.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names]
assert len(nodes)==len(names)
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(HELPERS),'exec'),globals());base_pose=pose
scene=bpy.data.scenes.new("Barcelona wasn't ready. Trent was.");bpy.context.window.scene=scene
art=bpy.data.collections.new('Anfield / authored vector artwork');scene.collection.children.link(art)
scene.render.engine='BLENDER_EEVEE';scene.eevee.taa_render_samples=16
scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.render.resolution_percentage=100
scene.render.fps=FPS;scene.render.fps_base=1;scene.frame_start=1;scene.frame_end=FRAMES
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.compression=15
scene.render.use_compositing=False;scene.render.use_sequencer=False
scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
scene.world=bpy.data.worlds.new('Night');scene.world.color=(.01,.02,.025)
camdata=bpy.data.cameras.new('Shared view');camera=bpy.data.objects.new('Shared view',camdata);art.objects.link(camera)
camdata.type='ORTHO';camdata.sensor_fit='VERTICAL';camdata.ortho_scale=16;camera.location=(0,0,90);scene.camera=camera
font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf');regular=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial.ttf')
# Original restrained stadium illustration. Audience silhouettes share a few batched meshes.
rect('Night',-20,-20,40,40,'#102d35',-40)
rect('Stand',-12,-.5,24,8,'#183b45',-39)
rng=random.Random(20190507)
for row in range(10):
    y=.6+row*.40;line('Terrace', [(-12,y),(12,y)],'#31535a',.025,-38)
    vs=[];fs=[]
    for i in range(90):
        x=-12+i*.28+(row%2)*.12;h=rng.uniform(.10,.20);n=len(vs)
        vs.extend([(x,y,-37),(x+.11,y,-37),(x+.11,y+h,-37),(x,y+h,-37)])
        fs.append((n,n+1,n+2,n+3));n=len(vs)
        vs.extend([(x+.055+.045*math.cos(k*math.tau/8),y+h+.045+.05*math.sin(k*math.tau/8),-36.9) for k in range(8)]);fs.append(tuple(range(n,n+8)))
    me=bpy.data.meshes.new('Supporters');me.from_pydata(vs,[],fs)
    for c in ('#b56361','#759394','#d0bfa1','#436a70'):me.materials.append(mat(c))
    for p in me.polygons:p.material_index=rng.randrange(4)
    add(bpy.data.objects.new('Supporters row',me))
line('Roof', [(-12,4.9),(12,4.9)],'#74908f',.08,-35)
for x in (-3.2,0,3.2):
    rect('Lamp housing',x-.65,4.62,1.3,.22,'#48656b',-34)
    for i in range(7):disk('Lamp',x-.52+i*.17,4.74,.053,PAPER,-33)
# The goal line and corner are the same straight oblique line; distances are compressed.
def end_y(x):return -1.041-.444*x
poly('Pitch',[(-15,7),(-15,-20),(15,-20),(15,-7.95)],'#38735f',-30)
for j in range(12):
    x=-14+j*2.5
    poly('Mowing stripe',[(x,end_y(x)),(x+1.25,end_y(x+1.25)),(x-2.5,-12),(x-3.75,-12)],'#3c7962',-29)
line('Endline',[(-10,end_y(-10)),(3.05,end_y(3.05))], '#bad1a5',.045,-26)
line('Touchline',[(3.05,end_y(3.05)),(8,-14)],'#bad1a5',.045,-26)
line('Penalty area',[(-5.3,end_y(-5.3)),(-6.5,-4.1),(.9,-6.7),(2.1,end_y(2.1))],'#82ad89',.034,-26)
line('Six-yard area',[(-3.9,end_y(-3.9)),(-4.7,-1.9),(-.12,-3.95),(.65,end_y(.65))],'#b0cba1',.035,-26)
line('Corner arc',[(3.05-.47*math.cos(a),end_y(3.05)-.44*math.sin(a)+.21*math.cos(a)) for a in [i*math.pi/24 for i in range(13)]],PAPER,.036,-25)
# Goal: all four corners and a separately keyed net.
A=(-3.15,end_y(-3.15));B=(-.55,end_y(-.55));H=1.65;D=(.22,.45)
poly('Goal interior',[A,B,(B[0]+D[0],B[1]+H+D[1]),(A[0]+D[0],A[1]+H+D[1])],'#234c48',-23)
net=[]
for i in range(15):
    p=vec(A,B,i/14);pts=[p,(p[0]+D[0],p[1]+H+D[1])];net.append((line('Net vertical',pts,'#86a99b',.014,-22),pts))
for i in range(11):
    h=H*i/10;pts=[(A[0],A[1]+h),(B[0]+D[0],B[1]+h+D[1])];net.append((line('Net horizontal',pts,'#86a99b',.014,-21.9),pts))
line('Goal frame',[A,(A[0],A[1]+H),(B[0],B[1]+H),B],PAPER,.07,-20)
line('Goal depth',[(A[0],A[1]+H),(A[0]+D[0],A[1]+H+D[1]),(B[0]+D[0],B[1]+H+D[1]),(B[0],B[1]+H)],'#c0d0b6',.042,-20.1)
line('Corner pole',[(3.05,end_y(3.05)),(3.05,end_y(3.05)+1.46)],PAPER,.045,-5)
flag=poly('Red pennant',[(3.05,end_y(3.05)+1.46),(2.59,end_y(3.05)+1.33),(3.05,end_y(3.05)+1.10)],RED,-4.9)
# Actual editable endpoint mechanics from the preserved Heavy Box source.
keep={'Bean torso','Head','Head_outline','Eye_0','Eye_1','Brow_0','Brow_1','Mouth','Mouth open','CTRL_Body','CTRL_Head','ANCHOR_Shoulder'}
for side in ('far','near'):
    keep.update(f'{p}_{side}' for p in ('Mitten','Shoe','Arm','Leg'))
    keep.update(f'{p}_{side}_outline' for p in ('Mitten','Shoe'))
    keep.update(f'CTRL_{p}_{side}' for p in ('Hand','Foot','Elbow','Knee'))
with bpy.data.libraries.load(str(SOURCE),link=False) as (src,dst):
    assert keep.issubset(src.objects);dst.objects=list(keep)
template={o.name:o for o in dst.objects}

def redraw(ob,pts,color,z):
    me=bpy.data.meshes.new(ob.name+' artwork');me.from_pydata([(*p,z) for p in pts],[],[list(range(len(pts)))]);me.materials.append(mat(color));ob.data=me;ob.scale=(1,1,1)
cast=[('Trent',RED,'66','#bb805c','crop'),('Origi',RED,'27','#88573e','twists'),('Shaqiri',RED,'23','#d3a27f','crop'),('Defender A','#28527c','', '#d6a880','sweep'),('Defender B','#28527c','', '#bd8d6c','crop'),('Defender C','#28527c','', '#d0a17c','sweep'),('ter Stegen',GREEN,'1','#d8ad86','sweep')]
for name,col,num,skin,hair in cast:
    a=character(name,col,num);m=a['m'];head=m['CTRL_Head'];body=m['CTRL_Body'];ex=[]
    face=oval(0,0,.48,.55)
    redraw(m['Head'],face,skin,.37)
    sp=m['Head_outline'].data.splines[0];m['Head_outline'].data.splines.clear();sp=m['Head_outline'].data.splines.new('POLY');sp.points.add(len(face)-1)
    for p,xy in zip(sp.points,face):p.co=(*xy,.39,1)
    sp.use_cyclic_u=True;m['Head_outline'].data.bevel_depth=.023
    def p(n,pts,c,z=.5,par=head):
        ob=poly(name+' / '+n,pts,c,z,parent=par);ex.append(ob);return ob
    def l(n,pts,c=INK,w=.026,z=.57,par=head):
        ob=line(name+' / '+n,pts,c,w,z,parent=par);ex.append(ob);return ob
    for x in (-.48,.48):p('Ear',oval(x,-.03,.075,.13,16),skin,.38)
    p('Hair',[(-.48,.14),(-.45,.39),(-.25,.57),(.16,.58),(.42,.42),(.48,.12),(.28,.30),(-.18,.33)],'#272d2c')
    if hair=='twists':
        for x in (-.36,-.18,0,.18,.36):p('Short twist',oval(x,.49,.13,.16,12),'#272d2c',.52)
    if hair=='sweep':p('Hair sweep',[(-.44,.3),(-.5,.54),(-.22,.67),(.15,.64),(.38,.47),(.12,.47),(-.18,.30)],'#4b3c31',.52)
    l('Nose',[(.18,.04),(.29,-.07),(.17,-.1)],'#654c3d',.026)
    for i in range(2):
        x=-.19+i*.36
        p('Eye white',oval(x,.10,.12,.10,20),PAPER,.52)
        redraw(m['Eye_'+str(i)],oval(x+.04,.1,.047,.062,16),INK,.55);m['Eye_'+str(i)].location=(0,0,0)
    jersey=[(-.29,.04),(-.30,.53),(-.44,.61),(-.36,.84),(-.17,.91),(.17,.91),(.36,.84),(.44,.61),(.30,.53),(.29,.04)]
    redraw(m['Bean torso'],jersey,col,.23)
    if name.startswith('Defender'):
        for x in (-.22,.02):p('Maroon stripe',[(x,.1),(x+.12,.1),(x+.12,.82),(x,.88)],'#ad4556',.245,body)
    p('Shorts',[(-.30,.13),(.30,.13),(.32,-.12),(.05,-.14),(0,-.02),(-.05,-.14),(-.32,-.12)],'#a93943' if col==RED else '#203e65' if name.startswith('Defender') else '#98ad63',.26,body)
    l('Collar',[(-.16,.9),(0,.8),(.16,.9)],PAPER,.035,.28,body)
    a['number'].data.size=.35;a['number'].location=(0,.43,.29)
    for side in ('far','near'):
        m['Mitten_'+side].data.materials[0]=mat(PAPER if name=='ter Stegen' else skin)
        m['Shoe_'+side].data.materials[0]=mat('#efcf87' if col==RED else '#f3e8cf')
    a['all']+=ex

def pose(mode,t=0):
    p=base_pose(mode,t)
    if mode=='organise':
        p=base_pose('watch',t);p['hands']=[(-.53,1.42,.1),(1.02,2.04,-.4)];p['headtilt']=-.12
    if mode=='notice':
        p=base_pose('ready',t);p['headtilt']=.1;p['focus']=.8
    if mode=='settle':
        p=base_pose('watch',t);p['hands']=[(-.48,1.2,0),(.5,1.2,0)]
    return p
# Scene time pauses and replays editorially. Named contacts below use this same map.
def match_time(t):
    if t<2:return t
    if t<7:return 2
    if t<10:return t-5
    if t<14:return 5
    if t<23:return t-9
    if t<29:return 5+(t-23)*2/3
    return t-15
TR=(3.4,-2.50,.48);OR=(-.15,-2.25,.50)
# Match the actual shoe surface once, then reuse that exact continuous-ball contact.
def boot_contact(x,y,s):
    boot=[(x-s*(.64+v.co.x),y+s*(.12+v.co.y)) for v in template['Shoe_near'].data.vertices]
    by=y+.12
    def clearance(bx):
        ds=[]
        for a,b in zip(boot,boot[1:]+boot[:1]):
            dx,dy=b[0]-a[0],b[1]-a[1];u=clamp(((bx-a[0])*dx+(by-a[1])*dy)/(dx*dx+dy*dy));ds.append(math.hypot(bx-a[0]-u*dx,by-a[1]-u*dy))
        return min(ds)-.12-.0205*s
    lo,hi=x-1.3*s,x-.3*s
    for _ in range(50):
        mid=(lo+hi)/2
        if clearance(mid)>0:lo=mid
        else:hi=mid
    return ((lo+hi)/2,by)
C=boot_contact(*TR);R=boot_contact(*OR);N=(-2.40,.89)
ball=empty('Match ball / continuous');disk('Ball face',0,0,.12,PAPER,.1,parent=ball)
line('Ball contour',oval(0,0,.12,.12),INK,.018,.11,parent=ball,closed=True)
poly('Ball panel',[(.052*math.cos(i*math.tau/5),.052*math.sin(i*math.tau/5)) for i in range(5)],INK,.12,parent=ball)
for i in range(5):
    a=i*math.tau/5;line('Ball seam',[(.05*math.cos(a),.05*math.sin(a)),(.12*math.cos(a),.12*math.sin(a))],INK,.008,.13,parent=ball)
def ball_at(q):
    if q<=6:return C
    if q<=7:
        u=q-6;xy=vec(C,R,u);return (xy[0],xy[1]+.16*math.sin(math.pi*u))
    if q<=7.5:
        u=(q-7)*2;xy=vec(R,N,u);return (xy[0],xy[1]+.18*math.sin(math.pi*u))
    u=clamp((q-7.5)/.9);return (N[0]+.12*math.sin(u*math.pi),mix(N[1],-.05,ease(u)))
trails=[disk('Ball motion trail',0,0,.08*(1-i*.18),['#d5d29b','#a1b58a','#709b79'][i],7.8) for i in range(3)]
# Editorial overlays occupy dedicated screen margins; the action remains unobstructed.
rect('Top dark margin',-8,5.0,16,6,INK,30)
label('Series kicker','MOMENTS THAT CHANGED THE GAME',0,7.02,.235,'#98b8b1',31,spacing=1.1)
label('Match identification','ANFIELD  /  7 MAY 2019',0,6.49,.24,PAPER,31)
label('Score before','LIV  3 - 0  BAR',0,5.88,.52,PAPER,31,'before')
label('Score after','LIV  4 - 0  BAR',0,5.88,.52,GOLD,31,'after')
label('Aggregate before',"79'    AGGREGATE  3 - 3",0,5.28,.25,'#b9cbc1',31,'before')
label('Aggregate after',"79'    AGGREGATE  4 - 3",0,5.28,.25,GOLD,31,'after')
rect('Bottom dark margin',-8,-11,16,6.05,INK,30)
label('Reconstruction footer','ANIMATED RECONSTRUCTION  /  POSITIONS SIMPLIFIED',0,-7.03,.16,'#8faeaa',31)
line('Footer rule',[(-3.8,-6.73),(3.8,-6.73)],'#3c615f',.015,31)
captions=[
 ('c0',"A CORNER.","A PLACE IN THE FINAL AT STAKE."),
 ('c1',"WHO'S READY?","FREEZE. LOOK AT THE WHOLE PICTURE."),
 ('c2',"TRENT WALKS AWAY.","SHAQIRI IS COMING TO TAKE IT."),
 ('c3',"THEN HE SEES IT.","ORIGI HAS SPACE. BARÇA ARE STILL ORGANISING."),
 ('c4',"ONE QUICK CORNER.",""),
 ('c5',"ORIGI!","THE GOAL THAT COMPLETES THE COMEBACK."),
 ('c6',"WATCH WHEN THEY TURN.","SLOW REPLAY"),
 ('c7',"BARCELONA WASN'T READY.","TRENT WAS."),
 ('c8',"LIVERPOOL THROUGH.","4 - 3 ON AGGREGATE.")]
for group,a,b in captions:
    label(group+' title',a,0,-5.55,.43 if len(a)>22 else .54,PAPER,31,group)
    if b:label(group+' detail',b,0,-6.20,.22 if len(b)>38 else .29,GOLD,31,group)
label('Freeze badge','II  FREEZE',-2.9,3.99,.25,GOLD,25,'freeze')
label('Replay badge','SLOW REPLAY',-2.82,3.99,.25,GOLD,25,'replay')
# Gaze/lane annotations never imply a private thought or a fully reconstructed formation.
label('Trent tag','TRENT  66',3.0,-.43,.25,GOLD,24,'tags')
label('Origi tag','ORIGI  27',-.3,.0,.25,GOLD,24,'tags')
line('Origi space ring',oval(OR[0],OR[1]-.025,.6,.19),GOLD,.028,-2,'lane',closed=True)
for i in range(11):
    a=vec(C,R,i/11);b=vec(C,R,(i+.53)/11);line('Open delivery lane',[a,b],GOLD,.028,-3,'lane')
for x,y in ((-2.5,-.86),(.75,.69),(1.03,-2.67)):
    line('Attention tick',[(x+.38,y+.02),(x+.71,y+.14)],'#e4ad89',.033,10,'attention')
    line('Attention tick',[(x+.37,y-.12),(x+.69,y-.16)],'#e4ad89',.025,10,'attention')
# One event table exported from the authored timeline into production.json and native markers.
shots=[{'id':'setup','start_frame':1,'events':{'start':0}},
 {'id':'freeze','start_frame':49,'events':{'hold':0}},
 {'id':'swap','start_frame':169,'events':{'resume':0,'step_a':43,'step_b':48}},
 {'id':'opening','start_frame':241,'events':{'notice':0,'lane':24}},
 {'id':'action','start_frame':337,'events':{'resume':0,'plant':14,'corner_contact':24,'origi_contact':48,'net_contact':60,'cheer':64}},
 {'id':'goal','start_frame':433,'events':{'celebrate':0}},
 {'id':'replay','start_frame':553,'events':{'start':0,'corner_contact':36,'origi_contact':72,'net_contact':90}},
 {'id':'payoff','start_frame':697,'events':{'title':0,'result':84,'fade':144}}]
for shot in shots:
    for n,offset in shot['events'].items():scene.timeline_markers.new(shot['id']+'/'+n,frame=shot['start_frame']+offset)
plan_path=ROOT/'production.json'
plan=json.loads(plan_path.read_text()) if plan_path.exists() else {'version':1,'assets':{},'cues':[],'mix_gain_db':-3}
plan.update(title="Barcelona wasn't ready. Trent was.",timeline={'fps':'24','start_frame':1,'frames':864,'sample_rate':48000},shots=shots)
plan_path.write_text(json.dumps(plan,indent=2)+'\n')
# Bake every frame: editable controls, independently editable ball, net and graphics.
for f in range(1,FRAMES+1):
    t=(f-1)/FPS;q=match_time(t);replay=23<=t<29
    if q<2:
        tr=set_actor('Trent',TR[0],TR[1],TR[2],-1,'settle',q,f,depth=2)
    elif q<4:
        elapsed=q-2;v=.31
        tr=set_actor('Trent',TR[0]+v*elapsed,TR[1],TR[2],1,'run',elapsed*v/(2.56*TR[2]),f,depth=2)
    elif q<5.1:
        tr=set_actor('Trent',TR[0]+.62,TR[1],TR[2],-1,'notice',q,f,depth=2)
    elif q<5.55:
        u=ease((q-5.1)/.45);tr=set_actor('Trent',TR[0]+.62*(1-u),TR[1],TR[2],-1,'run',u*.62/(2.56*TR[2]),f,depth=2)
    elif q<8.7:tr=set_actor('Trent',*TR,-1,'kick',q-6,f,depth=2)
    else:tr=set_actor('Trent',*TR,-1,'celebrate',q-8.7,f,depth=2)
    if q<6.3:mode='watch';pt=q
    elif q<8.2:mode='kick';pt=q-7
    else:mode='celebrate';pt=q-8.2
    set_actor('Origi',*OR,-1,mode,pt,f,depth=3)
    sq=clamp((q-2)/4);sx=1.15+1.25*sq
    set_actor('Shaqiri',sx,-4.12,.44,1,'run' if 2<q<6 else 'celebrate' if q>8.3 else 'watch',(q-2)*(.3125/(2.56*.44)) if 2<q<6 else q,f,depth=4)
    for i,(name,x,y,s) in enumerate([('Defender A',-2.5,-2.65,.43),('Defender B',.65,-.75,.43),('Defender C',.95,-4.14,.42)]):
        turning=clamp((q-(6.18+i*.10))/.3)
        mode='organise' if q<6.2 else 'ready' if q<7.6 else 'disbelief'
        set_actor(name,x,y,s,1 if turning<.5 else -1,mode,q+i,f,depth=1+i*.1)
    kp=set_actor('ter Stegen',-1.86,-.45,.41,-1,'keeper' if q<7.6 else 'disbelief',q,f,depth=-10)
    if 7.10<q<8.3:
        u=clamp((q-7.1)/.45);a=actors['ter Stegen'];roll=.70*ease(u);pivot=(-1.86,-.45)
        for n,ob in a['m'].items():
            if n.startswith('CTRL_') and not ob.parent:
                dx,dy=ob.location.x-pivot[0],ob.location.y-pivot[1]
                ob.location.x=pivot[0]+dx*math.cos(roll)-dy*math.sin(roll)-.45*ease(u);ob.location.y=pivot[1]+dx*math.sin(roll)+dy*math.cos(roll);ob.rotation_euler.z+=roll;key(ob,f)
    bp=ball_at(q);ball.location=(*bp,8);ball.rotation_euler.z=-q*7 if 6<q<8.4 else 0;key(ball,f)
    for i,ob in enumerate(trails):
        ob.location=(*ball_at(q-(i+1)*.025),7.8);key(ob,f);visible([ob],6.02<q<7.48,f)
    for ob,pts in net:
        r=q-7.5;wig=.065*math.sin(r*30)*math.exp(-r*3) if 0<r<1.5 else 0
        for j,(p,xy) in enumerate(zip(ob.data.splines[0].points,pts)):
            p.co.x=xy[0]+wig*(j+.3);p.keyframe_insert(data_path='co',frame=f)
    for group,items in GROUPS.items():
        if group in ('before','after'):on=(q<7.5)==(group=='before')
        elif group=='freeze':on=2<=t<7 or 10<=t<14
        elif group=='replay':on=replay
        elif group=='tags':on=2<=t<16 or 23<=t<26
        elif group=='lane':on=11<=t<14 or 23<=t<24.5
        elif group=='attention':on=10<=t<14 or 23<=t<25.25
        elif group.startswith('c'):
            idx=0 if t<2 else 1 if t<7 else 2 if t<10 else 3 if t<14 else 4 if t<16.5 else 5 if t<23 else 6 if t<29 else 7 if t<32.5 else 8
            on=group=='c'+str(idx)
        else:continue
        visible(items,on,f)
    if f%144==0:print('BAKE',f,flush=True)
# Linear keyed motion prevents Bezier overshoot at contact; editorial holds are identical values.
for obj in scene.objects:
    if obj.animation_data and obj.animation_data.action:
        for layer in obj.animation_data.action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for fc in bag.fcurves:
                        for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path.startswith('hide_') else 'LINEAR'
for old in list(bpy.data.scenes):
    if old!=scene:bpy.data.scenes.remove(old)
scene.frame_set(277);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'trent-corner.blend'))
(OUT/'build-checks.json').write_text(json.dumps({'blender':bpy.app.version_string,'frames':FRAMES,'seconds':36,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'contacts':{'corner':C,'receiver':R,'net':N},'scene_objects':len(scene.objects)},indent=2)+'\n')
if '--samples' in sys.argv:
    scene.render.resolution_percentage=65
    for t in (0,3,9,11.5,14.8,15,15.5,16,16.5,19,25,30,34):
        scene.frame_set(round(t*24)+1);scene.render.filepath=str(OUT/f'stills/layout-{round(t*24)+1:04}.png');bpy.ops.render.render(write_still=True)
print('BUILD_COMPLETE',flush=True)
