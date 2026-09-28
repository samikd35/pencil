"""Restore full source surfaces in affected cast instances; no patch limbs.

Run named scenes visibly and inspect their demanding poses before saving a candidate.
"""
from pathlib import Path
import bpy,json,runpy,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/animatic-v002'
F=runpy.run_path(str(ROOT/'scripts/build_full_animatic.py'))
D,A=F['D'],F['A']
REG=json.loads((ROOT/'artifacts/animatic-v001/cast-registry.json').read_text())
BOUNDARIES=json.loads((ROOT/'assets/film-cast-v001/arm-silhouette-boundaries.json').read_text())
CAST={}

def curves(o):
    if not o.animation_data or not o.animation_data.action:return []
    return [fc for l in o.animation_data.action.layers for st in l.strips for b in st.channelbags for fc in b.fcurves]

def select_scene(name):
    s=bpy.data.scenes[name];bpy.context.window.scene=s
    col=s.collection.children[0]
    D.update(s=s,col=col,cam=s.camera);A.update(s=s,col=col,cam=s.camera)
    A['base'].update(s=s,skin=col,ink=A['mat']('#202329'),font=next(f for f in bpy.data.fonts if f.filepath.endswith('Arial Bold.ttf')))
    return s

def bind(a,person):
    """Garment regions measured for these sheets, separate from bone endpoints."""
    cfg=a['config'];u=6/cfg['body_height'];r=a['rest'];skin=a['skin']
    # Source pixels before crop normalization: underarm and shirt-hem half widths.
    widths={'Haaland':(73,78),'Maresca':(73,76),'Rashford':(72,80),
            'Mainoo':(73,78),'Maguire':(81,89),'Martinez':(77,87),
            'Fernandez':(77,89),'Lammens':(80,91)}
    top,bottom=[x*cfg['coordinate_scale']*u for x in widths[person]]
    hand_boundary={'Haaland':119,'Maresca':106,'Rashford':119,'Mainoo':119,
                   'Maguire':130,'Martinez':130,'Fernandez':130,'Lammens':130}[person]*cfg['coordinate_scale']*u
    bones={b.name:(Vector(b.head_local),Vector(b.tail_local)) for b in a['armature'].data.bones}
    indices=list(range(len(skin.data.vertices)))
    for group in skin.vertex_groups:group.remove(indices)
    def clamp(x):return min(1,max(0,x))
    def weights(p,names):
        ranked=sorted((A['segment_distance'](p,*bones[n]),n) for n in names)[:2]
        vals=[math.exp(-(d*d-ranked[0][0]**2)/.045) for d,n in ranked];total=sum(vals)
        return {n:w/total for (_,n),w in zip(ranked,vals)}
    for v in skin.data.vertices:
        p=v.co;cx=r['hip'].x;hy=r['hip'].y;ny=r['neck'].y
        side='L' if p.x<cx else 'R'
        source_y=(cfg['floor_y']-p.y/u)/cfg['coordinate_scale']
        source_x=(cfg['center_x']+p.x/u)/cfg['coordinate_scale']
        gap=BOUNDARIES[person].get(str(round(source_y)))
        if p.y>ny+.06:w={'head':1.}
        elif p.y>ny-.16:
            h=clamp((p.y-ny+.16)/.22);w={'head':h,'torso':1-h}
        elif gap and (source_x<gap[0] or source_x>gap[1]):
            w=weights(p,[side+' upper arm',side+' forearm',side+' hand'])
        elif gap and p.y>hy-.1:
            w={'torso':1.}
        elif gap:
            w=weights(p,[side+' thigh',side+' calf',side+' foot'])
        elif hy-.1<p.y<hy+.65 and abs(p.x-cx)<bottom+.18:
            w={'torso':1.}
        elif p.y>hy+.12:
            t=clamp((p.y-hy)/(r[side+'shoulder'].y-hy))
            boundary=bottom*(1-t)+top*t
            influence=clamp((abs(p.x-cx)-boundary-.18)/.22)
            w={n:value*influence for n,value in weights(p,[side+' upper arm',side+' forearm',side+' hand']).items()}
            w['torso']=1-influence
        elif abs(p.x-cx)>hand_boundary and p.y>r[side+'finger'].y-.3:
            w=weights(p,[side+' forearm',side+' hand'])
        elif p.y>hy-.1:w={'torso':1.}
        else:
            w=weights(p,[side+' thigh',side+' calf',side+' foot'])
            torso=clamp((p.y-(hy-.36))/.26)
            w={n:value*(1-torso) for n,value in w.items()};w['torso']=torso
        for n,value in w.items():
            if value>1e-8:skin.vertex_groups[n].add([v.index],value,'REPLACE')
    assert all(abs(sum(g.weight for g in v.groups)-1)<1e-5 for v in skin.data.vertices)

def restore_scene(scene_name):
    s=select_scene(scene_name);changed=[]
    for tag,row in REG.items():
        prefix='A '+tag+' / ';oldroot=bpy.data.objects.get(prefix+'ROOT')
        if not oldroot or oldroot.name not in s.objects or not row['config'].get('crop'):continue
        if oldroot.get('Restored source surface'):continue
        person=next(k for k,c in F['SOURCES'].items() if c['image']==row['config']['image'] and c['crop']==row['config']['crop'])
        for c in F['SOURCES'].values():c['active']=False
        cfg=F['SOURCES'][person];cfg['active']=True
        new=A['actor']('Restored '+tag,cfg,oldroot.location)
        cfg['active']=False
        x0,y0,x1,y1=cfg['crop'];W,H=cfg['sheet_size']
        for uv in new['skin'].data.uv_layers.active.data:uv.uv=((x0+uv.uv.x*(x1-x0))/W,1-(y0+(1-uv.uv.y)*(y1-y0))/H)
        # Reuse original control names/animation/prop parents and facial performances.
        oldarm=next(o for o in oldroot.children if o.type=='ARMATURE')
        new['skin'].modifiers[0].object=oldarm
        new['skin'].parent=oldroot
        new['root'].scale=oldroot.scale
        new['rest']={k:Vector(v) for k,v in row['rest'].items()}
        bind(new,person)
        oldskin=next(o for o in oldroot.children if o!=new['skin'] and o.type=='MESH' and any(m.type=='ARMATURE' for m in o.modifiers))
        for ob in list(oldroot.children_recursive):
            if ob==new['skin']:continue
            if ob==oldskin or any(token in ob.name for token in (' native ',' upper ',' palm ','ROOT hand ',' joint outline ',' joint fill ')):
                for col in list(ob.users_collection):
                    if col in list(s.collection.children):col.objects.unlink(ob)
        # The temporary construction rig is discarded; full artwork remains on the existing rig.
        for ob in [new['root'],*new['root'].children_recursive]:
            if ob==new['skin']:continue
            for col in list(ob.users_collection):col.objects.unlink(ob)
        sh=bpy.data.objects['A Restored '+tag+' / ground shadow']
        for col in list(sh.users_collection):col.objects.unlink(sh)
        oldroot['Restored source surface']=person
        new.update(root=oldroot,armature=oldarm,controls={k:bpy.data.objects[prefix+'CTRL '+k] for k in row['rest']})
        new['facial']={key:bpy.data.objects[prefix+label] for key,label in [('mouth','mouth control'),('eye0','eye 0'),('eye1','eye 1'),('gaze0','gaze 0'),('gaze1','gaze 1')]}
        CAST[tag]=new;changed.append(tag)
    s.frame_set(min(120,s.frame_end));bpy.context.view_layer.update()
    return changed

def save():
    OUT.mkdir(exist_ok=True)
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'cast-repair-working.blend'))
    (OUT/'cast-restoration.json').write_text(json.dumps({tag:{'person':a['root']['Restored source surface'],'vertices':len(a['skin'].data.vertices)} for tag,a in CAST.items()},indent=2)+'\n')
    return {'file':bpy.data.filepath,'restored':len(CAST),'status':'Needs rendered pose inspection; not full animatic acceptance.'}

def mainoo_action():
    s=select_scene('FILM S04 / Post saves again');a=CAST['Mainoo 5']
    R=runpy.run_path(str(ROOT/'scripts/repair_rashford.py'))
    for ob in a['controls'].values():ob.animation_data_clear()
    a['root'].rotation_euler=(math.pi/2,0,math.pi/2)
    for f,lean,off,kick in [(1,-.04,(0,-.03),(0,0,0)),(14,-.09,(-.04,-.12),(-.3,-.7,-.4)),
        (26,-.12,(-.10,-.18),(-.55,-1.3,-.8)),(32,-.09,(-.02,-.12),(-.32,-.9,-.5)),
        (37,.09,(.08,-.06),(.10,.28,.03)),(41,.14,(.10,-.07),(.7,1.0,.5)),
        (51,.06,(.10,-.04),(.35,.5,.2)),(64,0,(0,-.03),(0,0,0)),(288,0,(0,-.03),(0,0,0))]:
        R['full_pose'](a,f,lean,off,kick,[('L',-.15,-.6),('R',.2,.6)])
    D['smooth_actor'](a)
    for ob in a['controls'].values():
        for fc in curves(ob):
            for k in fc.keyframe_points:
                if 26<=k.co.x<=41:k.interpolation='LINEAR'
    s.frame_set(37);bpy.context.view_layer.update()
    start=a['controls']['Rtoe'].matrix_world.translation.copy()+Vector((0,.17,0));start.z=.11
    ball=s.objects['S04 ball'];ball.animation_data_clear();hit=Vector((-.16,9,1.0))
    keys=[(1,start),(36,start),(37,start)]
    for f in range(38,53):
        u=(f-37)/15;p=start.lerp(hit,u);p.z+=.7*math.sin(math.pi*u);keys.append((f,p))
    keys.extend([(60,(1.2,7.8,.65)),(68,(2.,7.2,.12)),(83,(2.5,7.0,.11)),(288,(2.5,7.0,.11))])
    D['keys'](ball,'location',keys)
    for fc in curves(ball):
        for k in fc.keyframe_points:k.interpolation='LINEAR'
    D['keys'](ball,'rotation_euler',[(1,(0,0,0)),(37,(0,0,0)),(68,(0,9,2)),(288,(0,9,2))])
    # Defender's existing three-quarter artwork remains readable in this planned wide.
    CAST['Chasing defender corrected']['root'].rotation_euler=(math.pi/2,0,.30)
    for ob in bpy.data.scenes['REPAIR S03 / strike and scratch'].objects:
        if ob.name.startswith('Repair sideline') and ob.name not in s.objects:D['col'].objects.link(ob)
    shadow=s.objects['A Mainoo 5 / ground shadow']
    if not shadow.get('Aligned'):
        from mathutils import Matrix
        center=Vector((3,2.8,0));rot=Matrix.Rotation(math.pi/2,4,'Z')
        for v in shadow.data.vertices:v.co=center+rot@(v.co-center)
        shadow['Aligned']=True
    # Bruno enters the post conversation after the shot has finished, not in the ball path.
    D['visible_tree'](s.objects['A Post Bruno / ROOT'],108,288)
    cam=s.camera;cam.animation_data_clear();cam.data.animation_data_clear()
    for f,loc,target,lens in [(1,(14,-4,5),(3.3,5.0,1),42),(17,(9.3,2.8,2.1),(3,2.9,1),47),
        (49,(5,3.0,2.7),(.6,8.7,1.2),49),(108,(-.2,4.7,1.9),(0,8.8,1.25),44),
        (236,(.5,4.2,2),(1.1,8,1.5),44)]:
        cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
        for path in ('location','rotation_euler'):cam.keyframe_insert(data_path=path,frame=f)
        cam.data.keyframe_insert(data_path='lens',frame=f)
    for obj in (cam,cam.data):
        for fc in curves(obj):
            for k in fc.keyframe_points:k.interpolation='CONSTANT'
    ev=json.loads(s.get('events','{}'));ev.update(strike=37,post_hit=52);s['events']=json.dumps(ev)
    s['Repair']='Continuous source art; knee-driven strike F37, post F52; planted left foot. Preserve contract and Bruno voice timing.'
    s.frame_set(37)
    return {'strike':37,'post_hit':52,'frames':s.frame_end}


def cuts(s,shots):
    cam=s.camera;cam.animation_data_clear();cam.data.animation_data_clear()
    for f,loc,target,lens in shots:
        cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
        for path in ('location','rotation_euler'):cam.keyframe_insert(data_path=path,frame=f)
        cam.data.keyframe_insert(data_path='lens',frame=f)
    for ob in (cam,cam.data):
        for fc in curves(ob):
            for k in fc.keyframe_points:k.interpolation='CONSTANT'


def unlink_tree(root,s):
    for ob in [root,*root.children_recursive]:
        for col in list(ob.users_collection):
            if col in list(s.collection.children):col.objects.unlink(ob)


def seated(name,loc,kind):
    if kind=='maresca':
        cfg=dict(image=str(ROOT/'assets/ending-v002/maresca-reclining.png'),center_x=900,floor_y=1000,body_height=980,head_growth=0,
          joints={'hip':[900,570],'neck':[992,250],'head':[996,68],
          'Lshoulder':[894,295],'Lelbow':[715,438],'Lwrist':[740,337],'Lfinger':[772,283],
          'Rshoulder':[1178,325],'Relbow':[1250,451],'Rwrist':[1107,471],'Rfinger':[1057,540],
          'Lhip':[830,560],'Lknee':[588,593],'Lankle':[428,818],'Ltoe':[305,905],
          'Rhip':[929,594],'Rknee':[788,645],'Rankle':[567,876],'Rtoe':[490,962]},
          eyes=[[966,117,35,19]],brows=[[968,95,37]],mouth=[947,190,25])
    else:
        cfg=dict(image=str(ROOT/'assets/ending-v002/foden-seated.png'),center_x=530,floor_y=1494,body_height=1464,head_growth=0,
          joints={'hip':[610,865],'neck':[530,363],'head':[511,154],
          'Lshoulder':[339,478],'Lelbow':[287,651],'Lwrist':[310,717],'Lfinger':[347,749],
          'Rshoulder':[699,492],'Relbow':[704,702],'Rwrist':[461,734],'Rfinger':[409,754],
          'Lhip':[560,832],'Lknee':[236,836],'Lankle':[258,1280],'Ltoe':[162,1420],
          'Rhip':[658,858],'Rknee':[667,953],'Rankle':[711,1360],'Rtoe':[652,1476]},
          eyes=[[482,163,42,24],[407,161,18,22]],brows=[[483,139,44],[410,138,20]],mouth=[423,285,39])
    a=A['actor'](name,cfg,loc);a['root'].rotation_euler=(math.pi/2,0,0)
    # These are authored held sitting poses, with a neck turn and facial acting.
    # Keep crossed seated limbs in the complete drawing; do not rebind them with standing regions.
    skin=a['skin'];indices=list(range(len(skin.data.vertices)))
    for group in skin.vertex_groups:group.remove(indices)
    ny=a['rest']['neck'].y
    for v in skin.data.vertices:
        h=min(1,max(0,(v.co.y-ny)/.22));skin.vertex_groups['head'].add([v.index],h,'REPLACE');skin.vertex_groups['torso'].add([v.index],1-h,'REPLACE')
    a['root']['Pose']='Purpose-drawn seated pose; held body with articulated head and native facial acting.'
    return a


def head_act(a,values,end):
    neck=a['rest']['neck'];d=a['rest']['head']-neck
    for f,t in values:
        p=neck+Vector((d.x*math.cos(t)-d.y*math.sin(t),d.x*math.sin(t)+d.y*math.cos(t),0))
        A['control_key'](a,'head',f,p)
    eye=a['facial']['eye0'];D['keys'](eye,'scale',[(1,(1,1,1)),(end//3,(1,1,1)),(end//3+2,(1,.08,1)),(end//3+5,(1,1,1)),(end,(1,1,1))])
    D['keys'](a['facial']['gaze0'],'location',[(1,(-.014,0,.014)),(end,(-.014,0,.014))])
    D['smooth_actor'](a)


def reclining():
    s=select_scene('FILM S09 / Pep two point oh')
    old=CAST['Maresca 14'];oldmouth=old['facial']['mouth'];action=oldmouth.animation_data.action if oldmouth.animation_data else None
    unlink_tree(old['root'],s)
    for ob in list(s.objects):
        if ob.name.startswith(('Maresca lounger','Lounger','A Maresca 14 / ground shadow')):
            for col in list(ob.users_collection):
                if col in s.collection.children[:]:col.objects.unlink(ob)
    m=seated('Reclining Maresca',(1.05,.15,.02),'maresca');m['root'].scale=(.36,.36,.36)
    if action:
        mouth=m['facial']['mouth'];mouth.animation_data_create();mouth.animation_data.action=action.copy();mouth.animation_data.action_slot=mouth.animation_data.action.slots[0]
    head_act(m,[(1,0),(103,0),(107,.065),(117,-.07),(128,.02),(174,0),(190,-.04),(224,.02),(288,0)],288)
    # Chair follows the seated drawing's hip and reclined back, rather than a standing rectangle.
    chair=D['empty']('Reclined deckchair',(.2,.40,.02));chair.rotation_euler.x=math.pi/2
    D['poly']('Deckchair canvas',[(.15,.62),(1.24,.98),(1.82,1.70),(1.38,1.80),(.89,1.04),(.04,.75)],-.05,'#9acdde',chair)
    for pts in [[(.06,.02),(.83,1.02),(1.83,1.78)],[(1.75,.02),(.85,1.02),(.15,.68)]]:
        D['line']('Deckchair frame',pts,.0,'#f2f0df',.03,chair)
    D['line']('Deckchair armrest',[(1.15,.87),(1.87,.93)],.01,'#f2f0df',.035,chair)
    h=CAST['Haaland 14'];h['root'].location=(-1.25,0,.02)
    cuts(s,[(1,(.4,-7.8,2.8),(.15,.15,1.02),43),(102,(1.0,-3.5,1.9),(1.15,.15,1.22),48),(178,(.2,-6.8,2.4),(.1,.1,1.1),45)])
    s['Repair']='Maresca genuinely reclines; purpose-drawn seated surface, left-facing eye; original voice timing retained.'
    s.frame_set(120)
    return {'scene':s.name,'mouth':m['facial']['mouth'].name}


def fishing_ending():
    s=D['scene']('REPAIR S10 / roof waterfall and fishing',312,(6,-8,6),(0,11,3.5))
    # Roof spill is based on the May 2024 leak; the fishable pitch pool is explicit comic fantasy.
    for ob in list(D['col'].objects):
        if ob.name.startswith(('A / goal','A / net','A / top net','A / side net','A / area line')):D['col'].objects.unlink(ob)
    surface=A['surface'];tube=A['tube']
    tube('Broken roof gutter',[(-3,14,7.3),(0,14,7.3),(0,13.7,7.1)],'#d3dbe0',.11)
    surface('Roof runoff ribbon',[(-.31,13.65,7.1),(.25,13.65,7.1),(.74,13.12,.05),(-.65,13.12,.05)],'#95d5e8')
    # Water cascades from roof to stand apron, then runs downhill toward the fishable pool.
    surface('Runoff across apron',[(-.65,13.1,.055),(.74,13.1,.055),(1.7,5,.055),(-1.2,5,.055)],'#83c8de')
    pool=surface('Comic pitch puddle',[(.1+3.0*math.cos(i*math.tau/80),4.9+1.7*math.sin(i*math.tau/80),.058) for i in range(80)],'#81c9e0')
    for k in range(13):
        x=-.25+.044*k
        ob=tube('Falling water highlight',[(x,13.58,0),(x+.04,13.56,.55+(k%3)*.11)],'#d8f4fa',.018)
        for f in range(1,313):
            ob.location.z=7.05-((f*.21+k*.57)%6.8);ob.keyframe_insert(data_path='location',frame=f)
        for fc in curves(ob):
            for key in fc.keyframe_points:key.interpolation='LINEAR'
    for k in range(5):
        pts=[(.5*math.cos(j*math.tau/32),.18*math.sin(j*math.tau/32),.025) for j in range(33)]
        ob=tube('Spill splash ripple',pts,'#e4f6ee',.015);ob.location=(.06,13.02,.06)
        for f in range(1,313):
            t=((f+k*8)%40)/40;ob.scale=(.1+t*2,.1+t*2,1);ob.keyframe_insert(data_path='scale',frame=f)
    f=seated('Fishing Foden',(2.4,4.1,.04),'foden');f['root'].scale=(.36,.36,.36)
    head_act(f,[(1,0),(128,0),(169,-.035),(183,.02),(211,-.035),(249,0),(312,0)],312)
    # Low stool behind hips and under the drawn sitting pose.
    stool=D['empty']('Foden stool',(2.4,4.36,.02));stool.rotation_euler.x=math.pi/2
    D['rect']('Stool seat',-.26,.90,.66,.09,0,'#806a51',stool)
    for x in (-.20,.33):D['line']('Stool leg',[(x,.90),(x*1.3,.02)],0,'#5c4b3c',.028,stool)
    hand=f['controls']['Lfinger'];rod=D['empty']('Held fishing rod',(.02,.02,.075),hand)
    D['line']('Fishing bamboo',[(0,0),(-2.3,2.4),(-2.9,2.7)],0,'#674e37',.035,rod)
    D['line']('Fishing taut line',[(-2.9,2.7),(-3.6,.65),(-3.6,-3.25)],.025,'#f4f0d7',.013,rod)
    # All parts share the hand anchor; the line lands in the pool on this planned three-quarter view.
    floatroot=D['empty']('Fishing float',(1.60,3.99,.14))
    floatroot.rotation_euler.x=math.pi/2
    D['poly']('Float cork',D['oval'](0,0,.045,.09),.0,'#ec6546',floatroot)
    D['line']('Float stem',[(0,.04),(0,.14)],.01,'#fff6dc',.012,floatroot)
    D['keys'](floatroot,'location',[(1,(1.60,3.99,.14)),(182,(1.60,3.99,.14)),(190,(1.60,3.99,.06)),(199,(1.60,3.99,.14)),(211,(1.60,3.99,.055)),(220,(1.60,3.99,.13)),(312,(1.60,3.99,.13))])
    D['face_keys'](f,[(1,.025),(223,.025),(230,.6),(238,.18),(246,.6),(254,.025),(312,.025)],[(1,0),(225,.55),(270,.6)])
    D['label']('OLD TRAFFORD WATER FEATURE',1,105,.42,.032)
    D['label']('Comic fantasy · inspired by the 2024 roof leak',1,105,.37,.021)
    D['label']('At least they’re biting.',228,284,-.42,.035)
    cuts(s,[(1,(3,5.2,7.9),(0,14,7.1),46),(42,(5,-5,7),(0,10,3.4),39),(114,(4,-2.7,2.55),(1.3,4.8,1.05),45),(222,(2.5,.3,1.95),(2.35,4.1,1.45),51),(278,(4,-2.7,2.55),(1.3,4.8,1.05),45)])
    s['events']=json.dumps({'roof_reveal':1,'cascade':42,'float_plop':189,'biting':230,'whistle_tail':288})
    s['Reference']='Real Old Trafford leak 12 May 2024; pitch pool and Foden fishing authored fantasy. research/old-trafford-roof-waterfall-v001.md'
    s['Repair']='Roof source, waterfall, runoff and seated fisherman shown in connected spatial coverage.'
    s.frame_set(160)
    return {'scene':s.name,'frames':312,'mouth':f['facial']['mouth'].name}


def finish_ending_layout():
    s=select_scene('FILM S09 / Pep two point oh');D['visible_tree'](s.objects['Perfect record'],1,85)
    cuts(s,[(1,(.4,-7.8,2.8),(.15,.15,1.02),43),(102,(1,-4.5,2.25),(1.15,.15,1.67),48),(178,(.2,-6.8,2.4),(.1,.1,1.1),45)])
    s=select_scene('REPAIR S10 / roof waterfall and fishing')
    cuts(s,[(1,(3,5.2,7.9),(0,14,7.1),46),(42,(6,-9,6),(1,9,3.7),35),(114,(4,-2.7,2.55),(1.3,4.8,1.05),45),(222,(2.5,.3,2.15),(2.35,4.1,1.60),46),(278,(4,-2.7,2.55),(1.3,4.8,1.05),45)])
    ob=s.objects['Fishing taut line'];flo=s.objects['Fishing float'];point=ob.data.splines[0].points[-1]
    for fr in [1,182,190,199,211,220,312]:
        s.frame_set(fr);bpy.context.view_layer.update();v=ob.matrix_world.inverted()@flo.matrix_world.translation;point.co=(*v,1);point.keyframe_insert(data_path='co',frame=fr)
    s.objects['A Fishing Foden / eye 0'].rotation_euler.z=-.13


def finish_actions():
    R=runpy.run_path(str(ROOT/'scripts/repair_rashford.py'))
    # Fernandez's shot now contains the kick itself, and reaches the glove decisively.
    s=select_scene('FILM S06 / Ours works too');a=CAST['Fernandez 9']
    for ob in a['controls'].values():ob.animation_data_clear()
    a['root'].rotation_euler=(math.pi/2,0,1.0)
    for f,lean,off,kick in [(1,-.03,(0,-.03),(0,0,0)),(14,-.1,(-.08,-.13),(-.4,-1.1,-.6)),(20,-.1,(-.1,-.16),(-.55,-1.3,-.8)),(24,.08,(.06,-.07),(.08,.3,.05)),(29,.15,(.09,-.07),(.7,1,.5)),(39,.06,(.1,-.04),(.3,.5,.2)),(52,0,(0,-.03),(0,0,0)),(168,0,(0,-.03),(0,0,0))]:
        R['full_pose'](a,f,lean,off,kick,[('L',-.15,-.6),('R',.2,.6)])
    D['smooth_actor'](a)
    s.frame_set(24);bpy.context.view_layer.update();start=a['controls']['Rtoe'].matrix_world.translation+Vector((0,.16,0));start.z=.12
    g=CAST['Lammens 9'];s.frame_set(43);bpy.context.view_layer.update();glove=g['controls']['Rfinger'].matrix_world.translation.copy()
    # Keep the established goalkeeper contact pose, compress its preparation into a spring.
    for ob in g['controls'].values():
        for fc in curves(ob):
            for k in fc.keyframe_points:
                old=k.co.x;new={30:31,56:43,71:50,94:76}.get(round(old),old);delta=new-old;k.co.x=new;k.handle_left.x+=delta;k.handle_right.x+=delta
    s.frame_set(43);bpy.context.view_layer.update();glove=g['controls']['Rfinger'].matrix_world.translation.copy()
    ball=s.objects['Other end shot'];ball.animation_data_clear()
    D['keys'](ball,'location',[(1,start),(24,start),(43,glove),(50,(7.16,9,1.7)),(65,(8.2,7.4,.5)),(78,(8.6,7.2,.12)),(168,(8.6,7.2,.12))])
    for ob in [ball,*a['controls'].values()]:
        for fc in curves(ob):
            for k in fc.keyframe_points:
                if ob==ball or 20<=k.co.x<=29:k.interpolation='LINEAR'
    cuts(s,[(1,(11,-3,3.6),(4,5.1,1.0),44),(36,(6,4.1,2.7),(4.1,8.5,1.45),43),(94,(3.7,4.6,2.1),(3.5,8.1,1.45),44)])
    s['events']=json.dumps({'strike':24,'tip':43,'post_hit':50})
    # Replace the obsolete number-10 corner drawing with the already approved repaired source.
    s=select_scene('FILM S07 / Square head');old=CAST['Corner 1'];cfg=json.loads((ROOT/'assets/rashford-v002/landmarks.json').read_text())['Rashford']
    cfg['image']=str(ROOT/'assets/rashford-v002/neutral.png');cfg['head_growth']=0
    a=A['actor']('Corner Rashford corrected',cfg,old['root'].location);a['root'].rotation_euler=old['root'].rotation_euler
    R['fit_surface'](a);unlink_tree(old['root'],s)
    # Shorter ball flight after the header; the reaction gets its own close frame.
    ball=s.objects['Corner ball']
    for fc in curves(ball):
        for k in fc.keyframe_points:
            old=k.co.x;new={93:84,118:100}.get(round(old),old);delta=new-old;k.co.x=new;k.handle_left.x+=delta;k.handle_right.x+=delta;k.interpolation='LINEAR'
    cuts(s,[(1,(5,-3,3.5),(4,6.7,1.2),46),(50,(5,2,2.5),(4,6.5,1.4),41),(88,(6,1.5,3),(5,9,1.5),40),(127,(4.2,3,2.1),(4,6.5,1.5),44)])
    events=json.loads(s['events']);events['wide']=84;s['events']=json.dumps(events)
    return {'Fernandez':{'strike':24,'tip':43,'post':50},'header_outcome':84,'corner_Rashford':'approved number 9 full-body source'}


def goal_action():
    R=runpy.run_path(str(ROOT/'scripts/repair_rashford.py'))
    s=select_scene('FILM S05 / Goal then flag');a=CAST['Haaland 6']
    for ob in a['controls'].values():ob.animation_data_clear()
    D['keys'](a['root'],'rotation_euler',[(1,(math.pi/2,0,0)),(94,(math.pi/2,0,math.pi/2)),(145,(math.pi/2,0,0))])
    for fc in curves(a['root']):
        if fc.data_path=='rotation_euler':
            for k in fc.keyframe_points:k.interpolation='CONSTANT'
    for f,lean,off,kick in [(1,0,(0,-.03),(0,0,0)),(89,0,(0,-.03),(0,0,0)),(101,-.08,(-.04,-.12),(-.25,-.65,-.3)),(107,-.09,(-.04,-.16),(-.4,-.8,-.5)),(110,.08,(.02,-.07),(.12,.28,.08)),(114,.13,(.05,-.08),(.5,.75,.4)),(126,.04,(.03,-.03),(.15,.25,.1)),(139,0,(0,-.03),(0,0,0)),(264,0,(0,-.03),(0,0,0))]:
        R['full_pose'](a,f,lean,off,kick,[('L',-.15,-.45),('R',.2,.5)])
    D['smooth_actor'](a)
    for ob in a['controls'].values():
        for fc in curves(ob):
            for k in fc.keyframe_points:
                if 107<=k.co.x<=114:k.interpolation='LINEAR'
    s.frame_set(110);bpy.context.view_layer.update();boot=a['controls']['Rtoe'].matrix_world.translation+Vector((0,.03,.05))
    ball=s.objects['Goal ball'];ball.animation_data_clear()
    D['keys'](ball,'location',[(1,(-2,3.7,.2)),(28,(-2,3.7,.2)),(48,(-.3,5,1.5)),(68,(1.9,6.8,1)),(92,(3.6,7.3,.65)),(110,boot),(120,(5.8,10,.4)),(134,(5.9,10.4,.12)),(264,(5.9,10.4,.12))])
    for fc in curves(ball):
        for k in fc.keyframe_points:k.interpolation='LINEAR'
    cuts(s,[(1,(12,-3,5),(3.5,6,1),43),(94,(10,7.5,2.7),(5.7,7.8,1.05),44),(145,(5.8,3.3,2.1),(5.7,7.5,1.4),44)])
    s.objects['Offside flag'].location=(-.42,.24,-2);s.objects['Offside flag'].scale=(.48,.48,.48)
    shadow=s.objects['A Haaland 6 / ground shadow']
    if not shadow.get('Contact shadow corrected'):
        for v in shadow.data.vertices:v.co.x=5.7+(v.co.x-5.7)*.6;v.co.y=7.5+(v.co.y-7.5)*1.7
        shadow['Contact shadow corrected']=True
    return {'strike':110,'net':120,'plant':'left foot'}


def contact_coverage():
    s=select_scene('FILM S06 / Ours works too')
    cuts(s,[(1,(11,-3,3.6),(4,5.1,1.0),44),(36,(6,4.1,2.7),(4.1,8.5,1.45),43),(48,(9,4.5,2.5),(7.16,9,1.4),45),(94,(3.7,4.6,2.1),(3.5,8.1,1.45),44)])
    s=select_scene('FILM S07 / Square head');s.frame_set(74);bpy.context.view_layer.update()
    head=s.objects['A Maguire 10 / CTRL head'].matrix_world.translation.copy()+Vector((-.08,0,.17))
    ball=s.objects['Corner ball'];ball.location=head;ball.keyframe_insert(data_path='location',frame=74)
    for fc in curves(ball):
        for k in fc.keyframe_points:k.interpolation='LINEAR'
    return {'post_camera':48,'header_contact':list(head)}


def facing_wolf():
    s=select_scene('FILM S08 / Good wolf')
    old=s.objects['A Donnarumma 13 / ROOT'];unlink_tree(old,s)
    cfg=json.loads((ROOT/'assets/rashford-v002/turn-landmarks.json').read_text())['KeeperLeft']
    cfg['image']=str(ROOT/'assets/rashford-v002/keeper-left.png');cfg['head_growth']=0
    cfg['eyes']=[[430,119,30,16]];cfg['brows']=[[431,92,39]]
    a=A['actor']('Wolf keeper left',cfg,(4.65,8,.02));a['root'].rotation_euler=(math.pi/2,0,0)
    R=runpy.run_path(str(ROOT/'scripts/repair_rashford.py'));R['fit_surface'](a,keeper=True)
    # Preserve the drawn profile mouth; this listener does not speak.
    unlink_tree(a['facial']['mouth'],s)
    head_act(a,[(1,0),(50,0),(64,.04),(80,-.02),(101,0),(120,0)],120)
    a['facial']['eye0'].rotation_euler.z=-.10
    for sign in (-1,1):D['poly']('Repaired wolf ear',[(sign*.34,.80),(sign*.43,1.42),(sign*.08,1.07)],-.03,'#394650',a['face'])
    h=CAST['Haaland 13'];h['root'].location=(2.95,8,.02);h['root'].rotation_euler=(math.pi/2,0,0)
    # Move their ground contact shadows with the new screen positions.
    for name,dx in [('A Donnarumma 13 / ground shadow',1.65),('A Haaland 13 / ground shadow',-1.65)]:
        sh=s.objects.get(name)
        if sh:sh.location.x+=dx
    newshadow=s.objects['A Wolf keeper left / ground shadow']
    for col in list(newshadow.users_collection):col.objects.unlink(newshadow)
    cuts(s,[(1,(3.8,3.3,2.2),(3.8,8,1.25),43),(83,(4.55,4.7,2.1),(4.65,8,1.55),44)])
    return {'facing':'Haaland faces right toward keeper; keeper uses true left-facing artwork.'}


def profile_features(a):
    cfg=a['config'];d=a['rest']['head']-a['rest']['neck'];theta=math.atan2(-d.x,d.y)
    def local(p):
        v=a['xy'](p)-a['rest']['neck'];c,sn=math.cos(-theta),math.sin(-theta)
        return(v.x*c-v.y*sn,v.x*sn+v.y*c)
    unit=6/cfg['body_height']*(1+cfg.get('head_growth',.35))
    for index,(x,y,w,h) in enumerate(cfg['eyes']):
        eye=a['facial']['eye'+str(index)];eye.location=(*local((x,y)),.024);eye.rotation_euler.z=-theta+.06
        for ob in eye.children:
            if ob.type=='MESH' and ('sclera' in ob.name or 'eye rim' in ob.name):
                inflate=1.05 if 'rim' in ob.name else 1
                for i,v in enumerate(ob.data.vertices):
                    t=math.tau*i/len(ob.data.vertices);v.co.x=math.cos(t)*w*unit*.5*inflate;v.co.y=math.sin(t)*h*unit*.5*inflate*(.72+.28*math.sin(t)**2)
        gaze=a['facial']['gaze'+str(index)];gaze.animation_data_clear();gaze.location=(-w*unit*.10,0,.014);gaze.scale=(.60 if w<h else .78,.78,1)
        brow=a['facial']['brow'+str(index)];brow.animation_data_clear();brow.location=(*local(cfg['brows'][index][:2]),.04);brow.rotation_euler.z=-theta+.04
    return {'visible_eyes':len(cfg['eyes']),'rest_face_angle':theta}


def foden_face_correction():
    s=select_scene('REPAIR S10 / roof waterfall and fishing');a=A['actors']['Fishing Foden']
    mouth=a['facial']['mouth'];mouth_action=mouth.animation_data.action.copy();eye_action=a['facial']['eye0'].animation_data.action.copy()
    for ob in list(a['facial'].values()):unlink_tree(ob,s)
    a['config']['eyes']=[[482,163,42,24],[407,161,18,22]]
    a['config']['brows']=[[483,139,44],[410,138,20]]
    A['face_art']('Fishing Foden');profile_features(a)
    for key,action in [('mouth',mouth_action),('eye0',eye_action),('eye1',eye_action.copy())]:
        ob=a['facial'][key];ob.animation_data_create();ob.animation_data.action=action;ob.animation_data.action_slot=action.slots[0]
    a['facial']['mouth']['smile']=.55
    a['root']['Facial view']='Three-quarter left: two separately fitted eyes; far eye smaller, both above nasal contour.'
    return {'eyes':a['config']['eyes'],'brows':a['config']['brows']}


def tidy_endings():
    for name in ('Fishing Foden','Reclining Maresca','Wolf keeper left'):profile_features(A['actors'][name])
    s=select_scene('REPAIR S10 / roof waterfall and fishing');ob=s.objects['Fishing taut line'];points=ob.data.splines[0].points
    # A hanging line, with one gentle sag between rod and float, not a disconnected kink.
    for fr in [1,182,190,199,211,220,312]:
        s.frame_set(fr);bpy.context.view_layer.update();a=Vector(points[0].co[:3]);b=Vector(points[-1].co[:3]);p=a.lerp(b,.45);p.x-=.08
        points[1].co=(*p,1);points[1].keyframe_insert(data_path='co',frame=fr)
    for ob in s.objects:
        if ob.type=='CURVE' and ob.name.startswith('Float cork'):ob.data.bevel_depth=.005
    # Extend the waterfall's animated white foam over the pool, with small expanding rings.
    for k in range(3):
        ob=A['tube']('Pool ripple',[(.25*math.cos(j*math.tau/32),.10*math.sin(j*math.tau/32),0) for j in range(33)],'#bde7ef',.012);ob.location=(.7+k*.4,5.0-k*.4,.064)
        for fr in range(1,313):
            scale=.3+((fr+k*12)%50)/50;ob.scale=(scale,scale,1);ob.keyframe_insert(data_path='scale',frame=fr)
    # The complete chair reads as support below the seated hips.
    s=select_scene('FILM S09 / Pep two point oh');root=D['empty']('Front deckchair support',(.2,-.12,.02));root.rotation_euler.x=math.pi/2
    D['line']('Deckchair front leg',[(.78,1.02),(.03,.02)],.0,'#f2f0df',.024,root)
    s.frame_set(1)


def export_edit():
    edit=json.loads((ROOT/'artifacts/animatic-v001/edit.json').read_text())
    edit[3].update(scene='REPAIR S03 / strike and scratch',frames=216)
    edit[15].update(scene='REPAIR S10 / roof waterfall and fishing',frames=312)
    start=1
    for row in edit:row['start_frame']=start;start+=row['frames']
    assert start-1==3624
    (OUT/'edit.json').write_text(json.dumps(edit,indent=2)+'\n')
    (OUT/'native-events.json').write_text(json.dumps({row['scene']:json.loads(bpy.data.scenes[row['scene']].get('events','{}')) for row in edit},indent=2)+'\n')
    # Rebind the existing performance envelope to the newly drawn sitting face.
    mouth=bpy.data.objects['A Fishing Foden / mouth control'];mouth.animation_data_clear()
    timing=json.loads((ROOT/'artifacts/animatic-v001/mouth-timing.json').read_text())
    row=next(x for x in timing if x['id']=='biting')
    for fr,value in row['jaw_keys']:
        mouth['open']=value;mouth.keyframe_insert(data_path='["open"]',frame=fr+170)
    mouth['smile']=.55
    return {'seconds':151,'frames':3624,'shots':len(edit)}


def save_candidate():
    s=select_scene('REPAIR S10 / roof waterfall and fishing')
    for ob in s.objects:
        if ob.type=='FONT' and ob.data.body=='At least they’re biting.':ob.data.body="Keep going, ref. They’re biting."
    edit=json.loads((OUT/'edit.json').read_text())
    s=bpy.data.scenes.new('SAMTOONS / repaired complete animatic');bpy.context.window.scene=s
    s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100
    s.render.fps=24;s.render.fps_base=1;s.frame_start=1;s.frame_end=3624;s.render.use_sequencer=True;s.sync_mode='AUDIO_SYNC'
    ed=s.sequence_editor_create()
    for row in edit:
        strip=ed.strips.new_scene(row['scene'],bpy.data.scenes[row['scene']],1,row['start_frame']);strip.scene_input='CAMERA';strip.frame_final_duration=row['frames']
    mix=OUT/'mix-review.wav'
    assert mix.exists()
    sound=ed.strips.new_sound('Repaired review mix',str(mix),2,1)
    assert round(sound.frame_final_duration)==3624
    s['Review']='151-second repaired combined animatic. User review pending. Not final delivery.'
    # Keep the visible instance on the repaired keeper shot rather than a blank VSE viewport.
    select_scene('REPAIR S03 / strike and scratch').frame_set(210)
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'combined-animatic-v002.blend'))
    return {'file':bpy.data.filepath,'frames':3624,'seconds':151}


def check_candidate():
    edit=json.loads((OUT/'edit.json').read_text());assert sum(row['frames'] for row in edit)==3624
    report={'frames':3624,'fps':24,'contacts':{},'profiles':{},'limitations':'Numerical checks supplement rendered-frame and user playback review.'}
    for sn,fr,ballname,control in [('FILM S04 / Post saves again',37,'S04 ball','A Mainoo 5 / CTRL Rtoe'),('FILM S05 / Goal then flag',110,'Goal ball','A Haaland 6 / CTRL Rtoe'),('FILM S06 / Ours works too',24,'Other end shot','A Fernandez 9 / CTRL Rtoe'),('FILM S06 / Ours works too',43,'Other end shot','A Lammens 9 / CTRL Rfinger')]:
        s=select_scene(sn);s.frame_set(fr);bpy.context.view_layer.update()
        distance=(s.objects[ballname].matrix_world.translation-s.objects[control].matrix_world.translation).length
        assert distance<(.025 if 'finger' in control else .24),(sn,fr,distance)
        report['contacts'][sn+' / '+str(fr)]=distance
    for sn,tag in [('FILM S09 / Pep two point oh','Reclining Maresca'),('REPAIR S10 / roof waterfall and fishing','Fishing Foden'),('FILM S08 / Good wolf','Wolf keeper left')]:
        s=select_scene(sn);s.frame_set(54);root=s.objects['A '+tag+' / ROOT'];eye=[o for o in root.children_recursive if o.name in s.objects and ' / eye ' in o.name and o.type=='EMPTY']
        assert len(eye)==(2 if tag=='Fishing Foden' else 1),(tag,len(eye));report['profiles'][tag]=len(eye)
    s=select_scene('REPAIR S10 / roof waterfall and fishing');ob=s.objects['Fishing taut line'];floatob=s.objects['Fishing float'];errors=[]
    for fr in [1,182,190,199,211,220,312]:
        s.frame_set(fr);bpy.context.view_layer.update();p=ob.matrix_world@Vector(ob.data.splines[0].points[-1].co[:3]);distance=(p-floatob.matrix_world.translation).length;assert distance<1e-5;errors.append(distance)
    report['fishing_line_max_endpoint_error']=max(errors)
    for row in edit:
        s=select_scene(row['scene']);assert s.frame_end==row['frames'] and s.render.fps==24
        # Replacement arm fragments cannot survive in the reviewed scene's linked cast.
        for root in s.objects:
            if root.get('Restored source surface'):
                bad=[o.name for o in root.children_recursive if o.name in s.objects and any(t in o.name for t in (' native ',' palm ','ROOT hand ',' joint outline ',' joint fill '))]
                assert not bad,bad
    (OUT/'construction-checks.json').write_text(json.dumps(report,indent=2)+'\n')
    return report
