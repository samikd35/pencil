"""S03 repair in visible Blender: setup, motion, finish_framing, add_turns, save.

Preserves old scenes. Complete individual artwork, fitted regions, corrective
temple drawing and coordinated leg controls. No cut-away/replacement limb patches.
"""
from pathlib import Path
import bpy, json, math
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/repair-v001'
F = {'__file__': str(ROOT / 'scripts/build_full_animatic.py')}
exec(compile(Path(F['__file__']).read_text(), F['__file__'], 'exec'), F)
D, A = F['D'], F['A']
CFG = json.loads((ROOT / 'assets/rashford-v002/landmarks.json').read_text())
CFG.update(json.loads((ROOT / 'assets/rashford-v002/turn-landmarks.json').read_text()))
END = 216


def curves(ob):
    if not ob.animation_data or not ob.animation_data.action:
        return []
    return [fc for layer in ob.animation_data.action.layers for strip in layer.strips
            for bag in strip.channelbags for fc in bag.fcurves]


def fit_surface(a, pointing=False, keeper=False):
    """Regions measured on this drawing; smooth transitions keep its whole surface.

    This calibration belongs to these Rashford drawings and the inspected keeper. Other cast members
    need their own boundaries; do not copy these numbers as anatomical defaults.
    """
    skin, r = a['skin'], a['rest']
    head_bottom, neck_bottom, waist, thigh_start = (253,325,860,945) if keeper else (283,355,820,918)
    segments = {'torso': ('hip', 'neck'), 'head': ('neck', 'head')}
    for side in ('L', 'R'):
        segments.update({side+' upper arm': (side+'shoulder', side+'elbow'),
                         side+' forearm': (side+'elbow', side+'wrist'),
                         side+' hand': (side+'wrist', side+'finger'),
                         side+' thigh': (side+'hip', side+'knee'),
                         side+' calf': (side+'knee', side+'ankle'),
                         side+' foot': (side+'ankle', side+'toe')})
    def clamp(x): return max(0., min(1., x))
    def distance_weights(p, names, sigma=.18):
        rank = sorted((A['segment_distance'](p, r[segments[n][0]], r[segments[n][1]]), n) for n in names)[:2]
        # Subtract the minimum squared distance for stable exponentials.
        d0 = rank[0][0]**2
        weights = [(n, math.exp(-(d*d-d0)/(sigma*sigma))) for d,n in rank]
        total = sum(w for n,w in weights)
        return {n:w/total for n,w in weights}
    # Clear memberships before assigning. VertexGroupElement references change
    # when memberships are removed, so deleting while traversing them skips some.
    indices = list(range(len(skin.data.vertices)))
    for group in skin.vertex_groups:
        group.remove(indices)
    for v in skin.data.vertices:
        i, j = v.index % 73, v.index // 73
        x, y = 1024*i/72, 1536*j/132
        p = v.co
        side = 'L' if x < 520 else 'R'
        arm = [side+' upper arm', side+' forearm', side+' hand']
        point_arm = pointing and x > 610 and y < 465
        if point_arm:
            strength = clamp((x-611)/54) if y > 280 else 1.
            w = distance_weights(p, ['R upper arm','R forearm','R hand'])
            w = {n:value*strength for n,value in w.items()}
            w['torso'] = 1-strength
        elif y < head_bottom:
            w = {'head':1.}
        elif y < neck_bottom:
            h = clamp((neck_bottom-y)/(neck_bottom-head_bottom))
            w = {'head':h, 'torso':1-h}
        elif y < 925 and (x < (310 if y>760 else 393) or x > (730 if y>760 else 655)):
            # The inner sleeve/underarm boundary slopes toward the shirt hem.
            bound = 393 - 24*clamp((y-390)/370) if side == 'L' else 655 + 25*clamp((y-390)/370)
            if keeper:bound = 365-30*clamp((y-420)/370) if side=='L' else 665+20*clamp((y-420)/370)
            strength = clamp(((bound-x) if side == 'L' else (x-bound))/64)
            w = {n:value*strength for n,value in distance_weights(p,arm).items()}
            w['torso'] = 1-strength
        elif y < waist:
            w = {'torso':1.}
        else:
            leg = [side+' thigh',side+' calf',side+' foot']
            w = distance_weights(p,leg,.22)
            torso = clamp((thigh_start-y)/(thigh_start-waist))
            w = {n:value*(1-torso) for n,value in w.items()}
            w['torso'] = torso
        for n,value in w.items():
            if value > 1e-8: skin.vertex_groups[n].add([v.index],value,'REPLACE')
    skin['Construction'] = 'Complete uncut drawing; measured Rashford regions; no replacement arm geometry.'


def setup():
    global s, p, reaction, keeper, wall, ball
    assert not bpy.app.background and bpy.context.window
    assert not bpy.data.is_dirty, 'Preserve unsaved edits before starting a repair revision.'
    assert 'REPAIR S03 / strike and scratch' not in bpy.data.scenes
    s = D['scene']('REPAIR S03 / strike and scratch', END, (20,-2,7), (1.7,1.2,1.1))
    s.eevee.taa_render_samples = 16
    s['Scope'] = 'Actual S03 repair staging: connected body, strike, temple/scratch and post imitation. Not full film acceptance.'
    D['CONFIG'].update(CFG)
    p = D['actor']('Repair Rashford', 'Rashford', (3.,-9.,.02))
    reaction = D['actor']('Repair Rashford temple', 'RashfordTemple', (3.,-9.,.02))
    for a,pointing in ((p,False),(reaction,True)):
        fit_surface(a,pointing)
        a['root'].rotation_euler = (math.pi/2,0,math.pi/2)
        a['root']['Character'] = 'Marcus Rashford'
        a['root']['Jersey'] = 9
    D['visible_tree'](p['root'],1,41)
    D['visible_tree'](reaction['root'],42,143)
    # Drawings are replaced at a planned cut. Their own joints remain editable.
    keeper = D['actor']('Repair keeper','Donnarumma',(3.5,8.25,.02))
    fit_surface(keeper,keeper=True)
    wall = []
    F['D'].update(s=s,col=D['col'],cam=D['cam'])
    # Whole uncut source drawings stay in their rest pose for background coverage.
    for name,loc,tag in [('Haaland',(2.25,.3,.02),'Repair wall A'),
                         ('Fernandez',(2.9,.3,.02),'Repair wall B'),
                         ('Fernandez',(3.55,.3,.02),'Repair wall C')]:
        a=F['person'](name,loc,tag)
        a['root']['Role']='Representative wall defender; exact identity not asserted.'
        for key,o in a['controls'].items():o.location=a['rest'][key]
        wall.append(a)
    for name,loc,tag in [('Bruno',(4.3,1.1,.02),'Repair supporting Bruno'),
                         ('Mbeumo',(.6,5.4,.02),'Repair supporting Mbeumo')]:
        a=D['actor'](tag,name,loc)
        D['pose'](a,1); D['pose'](a,END)
    ball=D['football']('Repair S03 football',(3.,-8.5,.11))
    s['cast_roles']='Rashford kicker; three representative City wall defenders; Bruno/Mbeumo support; Donnarumma goalkeeper. Compressed distances for readability.'
    s.frame_set(1)
    for area in bpy.context.screen.areas:
        if area.type in {'SEQUENCE_EDITOR','CONSOLE'}:area.type='VIEW_3D'
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_perspective='CAMERA'
            area.spaces.active.shading.type='MATERIAL'
            area.spaces.active.overlay.show_overlays=False
    bpy.context.view_layer.update()
    return {'scene':s.name,'objects':len(s.objects),'characters':'Complete Rashford surfaces plus original suitable supporting artwork'}


def ik_knee(hip,ankle,l1,l2,bend=1):
    d=ankle-hip; length=d.length
    assert 1e-7<length<l1+l2+.15, ('Leg out of reach',length,l1+l2)
    length=min(length,l1+l2-1e-6); axis=d.normalized()
    along=(l1*l1-l2*l2+length*length)/(2*length)
    height=math.sqrt(max(0,l1*l1-along*along))
    perpendicular=Vector((-axis.y,axis.x,0))*bend
    return hip+axis*along+perpendicular*height


def resume():
    """Recover this authored scene between short interactive connector batches."""
    global s,p,reaction,keeper,wall,ball
    s=bpy.data.scenes['REPAIR S03 / strike and scratch'];bpy.context.window.scene=s
    D.update(s=s,col=s.collection.children[0],cam=s.camera)
    A.update(s=s,col=D['col'],cam=s.camera)
    A['base'].update(s=s,skin=D['col'],ink=A['mat']('#202329'),font=next(f for f in bpy.data.fonts if f.filepath.endswith('Arial Bold.ttf')))
    def recover(tag):
        prefix='A '+tag+' / ';root=bpy.data.objects[prefix+'ROOT']
        ctl={o.name.split(' / CTRL ')[-1]:o for o in root.children if ' / CTRL ' in o.name}
        if 'Rest controls' not in root:root['Rest controls']=json.dumps({k:list(o.location) for k,o in ctl.items()})
        rest={k:Vector(v) for k,v in json.loads(root['Rest controls']).items()}
        facial={}
        for i in (0,1):
            for key,label in [('eye','eye '),('gaze','gaze '),('brow','brow control ')]:facial[key+str(i)]=bpy.data.objects[prefix+label+str(i)]
        facial['mouth']=bpy.data.objects[prefix+'mouth control']
        return dict(root=root,controls=ctl,rest=rest,facial=facial,skin=bpy.data.objects[prefix+'continuous artwork'],armature=bpy.data.objects[prefix+'skin binding'],face=bpy.data.objects[prefix+'FACE'])
    p=recover('Repair Rashford');reaction=recover('Repair Rashford temple');keeper=recover('Repair keeper')
    wall=[recover('Repair wall '+letter) for letter in 'ABC']
    ball=bpy.data.objects['Repair S03 football']
    return s.name


def full_pose(a,frame,lean=0,offset=(0,0),kick=None,arm=None,kick_side='R'):
    r=a['rest']; pivot=r['hip']; off=Vector((*offset,0))
    pos={k:pivot+off+D['rotate'](v-pivot,lean) for k,v in r.items()}
    assert kick_side in ('L','R')
    plant='L' if kick_side=='R' else 'R'
    pos[plant+'ankle']=r[plant+'ankle'].copy();pos[plant+'toe']=r[plant+'toe'].copy()
    pos[plant+'knee']=ik_knee(pos[plant+'hip'],pos[plant+'ankle'],(r[plant+'knee']-r[plant+'hip']).length,(r[plant+'ankle']-r[plant+'knee']).length,1 if plant=='L' else -1)
    if kick:
        thigh,calf,foot=kick
        for start,end,t in zip((kick_side+k for k in ('hip','knee','ankle')),(kick_side+k for k in ('knee','ankle','toe')),(thigh,calf,foot)):
            pos[end]=pos[start]+D['rotate'](r[end]-r[start],t)
    if arm:
        for side,th,fa in arm:
            for start,end,t in [(side+'shoulder',side+'elbow',th),(side+'elbow',side+'wrist',fa),(side+'wrist',side+'finger',fa)]:
                pos[end]=pos[start]+D['rotate'](r[end]-r[start],t)
    for key,v in pos.items():
        ob=a['controls'][key];ob.location=v;ob.keyframe_insert(data_path='location',frame=frame)
    return pos


def camera(frame,location,target,lens=44):
    cam=D['cam'];cam.location=location
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
    cam.data.lens=lens
    cam.keyframe_insert(data_path='location',frame=frame)
    cam.keyframe_insert(data_path='rotation_euler',frame=frame)
    cam.data.keyframe_insert(data_path='lens',frame=frame)


def motion():
    global contact
    for f,lean,off,kick in [
        (1,-.02,(0,-.03),(0,0,0)),(18,-.06,(-.05,-.10),(-.15,-.35,-.3)),
        (27,-.10,(-.12,-.18),(-.50,-1.2,-.75)),(32,-.14,(-.08,-.20),(-.65,-1.55,-.9)),
        (35,-.08,(.03,-.14),(-.20,-.65,-.30)),(39,.10,(.09,-.08),(.10,.30,.05)),
        (43,.17,(.14,-.08),(.80,1.15,.62)),(49,.09,(.15,-.08),(.40,.6,.28)),
        (58,.02,(.03,-.04),(0,0,0)),(END,0,(0,-.03),(0,0,0))]:
        full_pose(p,f,lean,off,kick,[('L',-.15,-.6),('R',.25,.65)])
    D['smooth_actor'](p)
    # Preserve the sharp striking interval rather than applying uniform soft ease.
    for ob in p['controls'].values():
        for fc in curves(ob):
            for k in fc.keyframe_points:
                if 32<=k.co.x<=43:k.interpolation='LINEAR'
    # The corrective full-body drawing already contains physical temple contact.
    # Gentle scratching changes the hand and head together, avoiding a floating hand.
    for f,tilt,dy in [(1,0,0),(42,0,0),(56,0,0),(73,0,0),(79,-.035,0),
                      (89,-.045,0),(97,-.04,.035),(104,-.045,-.025),
                      (111,-.035,.025),(118,-.045,-.025),(130,-.045,0),(143,-.045,0),(END,-.045,0)]:
        r=reaction['rest']; pivot=r['neck'];delta=Vector((0,dy,0))
        for key in reaction['controls']:
            v=r[key].copy()
            if key=='head':v=pivot+D['rotate'](v-pivot,tilt)
            if key in ('Rwrist','Rfinger'):v=pivot+D['rotate'](v-pivot,tilt)+delta
            if key=='Relbow':v+=Vector((-.03 if f>=79 else 0,-.025 if f>=79 else 0,0))
            ob=reaction['controls'][key];ob.location=v;ob.keyframe_insert(data_path='location',frame=f)
    D['smooth_actor'](reaction)
    for a in (p,reaction):
        D['face_keys'](a,[(1,.025),(56,.03),(73,.03),(79,.6),(90,.15),(106,.04),(END,.04)],[(1,.8),(73,.8),(79,-.65),(95,-.5),(END,-.4)])
        for i in (0,1):
            D['keys'](a['facial']['eye'+str(i)],'scale',[(1,(1,1,1)),(74,(1,1,1)),(78,(1,1.25,1)),(90,(1,1,1)),(104,(1,.35,1)),(110,(1,.9,1)),(END,(1,.9,1))])
    s.frame_set(39);bpy.context.view_layer.update()
    # The toe control is inside the painted boot. Place the ball's near surface
    # at its visible toe edge, not its centre at the internal control.
    contact=p['controls']['Rtoe'].matrix_world.translation.copy()+Vector((0,.18,0))
    contact.z=.11
    post=Vector((-.16,9.,.85))
    flight=[(1,contact),(38,contact),(39,contact)]
    for f in range(40,59):
        u=(f-39)/19
        v=contact.lerp(post,u);v.z+=2.4*math.sin(math.pi*u)
        flight.append((f,v))
    flight.extend([(64,(-1.6,6.8,.65)),(73,(-2.1,5.8,.14)),(88,(-1.9,5.0,.11)),(END,(-1.9,5.0,.11))])
    D['keys'](ball,'location',flight)
    D['keys'](ball,'rotation_euler',[(1,(0,0,0)),(39,(0,0,0)),(58,(0,math.tau*2,2)),(88,(0,math.tau*3,3)),(END,(0,math.tau*3,3))])
    for fc in curves(ball):
        for k in fc.keyframe_points:k.interpolation='LINEAR'
    for a in wall:
        root=a['root'];start=root.location.copy()
        D['keys'](root,'location',[(1,start),(40,start),(45,start+Vector((0,0,.18))),(50,start+Vector((0,0,.22))),(55,start),(END,start)])
    # Keeper attempts a save toward the post, then recovers for the comic tag.
    for f,tilt,off in [(1,0,(0,0)),(38,0,(0,-.1)),(45,.1,(-.08,-.1)),(53,.35,(-.4,.1)),(60,.75,(-.95,.1)),(70,1.05,(-1.2,-.5)),(81,1.2,(-1.2,-1.25)),(130,1.2,(-1.2,-1.25)),(155,.35,(-.3,-.2)),(175,0,(0,0)),(END,0,(0,0))]:
        arms=[[-.5,-1.6,-1.6],[.4,1.1,1.1]] if 45<=f<=155 else [[-.12,-.35,-.35],[.12,.35,.35]]
        D['pose'](keeper,f,tilt,off,[(side,['shoulder','elbow','wrist','finger'],angles) for side,angles in zip(('L','R'),arms)])
    D['smooth_actor'](keeper)
    D['face_keys'](keeper,[(1,.02),(END,.02)],[(1,0),(175,.65),(END,.65)])
    for i in (0,1):D['keys'](keeper['facial']['gaze'+str(i)],'location',[(1,(0,0,.014)),(175,(-.028,0,.014)),(END,(-.028,0,.014))])
    camera(1,(24,-15,9),(2.,-.4,1.0),38)
    camera(19,(8.6,-9,2.0),(3.,-8.85,1.0),47)
    camera(42,(6.65,-9,1.70),(3.,-9,1.49),55)
    camera(57,(7.6,2.4,2.6),(.4,8.0,1.1),48)
    camera(73,(6.65,-9,1.70),(3.,-9,1.49),55)
    camera(144,(2.8,4.4,1.7),(-.1,8.9,1.15),85)
    camera(189,(5.8,1.5,2.7),(2.3,8.9,1.15),52)
    for ob in (D['cam'],D['cam'].data):
        for fc in curves(ob):
            for k in fc.keyframe_points:k.interpolation='CONSTANT'
    # One purposeful widening reveal; all other framing changes are intentional cuts.
    for fc in curves(D['cam']):
        for k in fc.keyframe_points:
            if k.co.x==144:k.interpolation='BEZIER';k.handle_right_type='AUTO_CLAMPED'
    for fc in curves(D['cam'].data):
        for k in fc.keyframe_points:
            if k.co.x==144:k.interpolation='BEZIER';k.handle_right_type='AUTO_CLAMPED'
    if 'Repair post face' not in bpy.data.objects:post_gag()
    s['events']=json.dumps({'strike':39,'premature_celebration':42,'post_hit':58,'realisation':79,'scratch':97,'post_imitation':156})
    s.timeline_markers.clear()
    for name,f in json.loads(s['events']).items():s.timeline_markers.new(name,frame=f)
    s.frame_set(32);bpy.context.view_layer.update()
    return {'frames':END,'strike_frame':39,'post_frame':58,'reaction':'Complete corrective drawing; small editable hand/head motion'}


def finish_framing():
    from mathutils import Matrix
    # Extend the same dimensional stand to the sideline exposed by the new camera.
    if 'Repair sideline stand' not in bpy.data.objects:
        root=D['empty']('Repair sideline stand',(0,0,0))
        root.rotation_euler.z=math.pi/2
        for ob in list(s.objects):
            if ob.name.startswith(('A / crowd tier','A / red tier fascia','A / quiet crowd mark','A / roof','A / stadium lettering')):
                copy=ob.copy();D['col'].objects.link(copy);copy.name='Repair sideline '+ob.name;copy.parent=root
    # Align the flat ground shadow with the character's actual screen-facing plane.
    sh=bpy.data.objects['A Repair Rashford / ground shadow']
    if not sh.get('Aligned'):
        center=Vector((3.,-9.,0));rot=Matrix.Rotation(math.pi/2,4,'Z')
        for v in sh.data.vertices:v.co=center+rot@(v.co-center)
        sh['Aligned']=True
    other=bpy.data.objects['A Repair Rashford temple / ground shadow'];other.hide_render=True;other.hide_viewport=True


def add_turns():
    """Matched full-body views: readable facing changes without spinning a card."""
    D['CONFIG'].update(CFG)
    assert 'A Repair Rashford front / ROOT' not in bpy.data.objects
    mid=D['actor']('Repair Rashford turn','RashfordTurn',(3.,-9.,.02))
    front=D['actor']('Repair Rashford front','RashfordFront',(3.,-9.,.02))
    D['visible_tree'](reaction['root'],42,85)
    for a,first,last in ((mid,86,89),(front,90,143)):
        fit_surface(a,True);a['root'].rotation_euler=p['root'].rotation_euler
        a['root']['Facing']='Interpolated drawing toward front' if a is mid else 'Facing viewer after looking toward goal'
        for f in (1,86,90,96,101,106,111,116,124,143,END):
            s.frame_set(f);bpy.context.view_layer.update()
            for key,ob in a['controls'].items():
                ob.location=a['rest'][key]+(reaction['controls'][key].location-reaction['rest'][key])
                ob.keyframe_insert(data_path='location',frame=f)
        D['smooth_actor'](a)
        D['face_keys'](a,[(1,.03),(86,.1),(90,.08),(98,.03),(END,.03)],[(1,-.45),(END,-.45)])
        D['visible_tree'](a['root'],first,last)
        sh=bpy.data.objects[a['root'].name.replace('ROOT','ground shadow')];sh.hide_render=True;sh.hide_viewport=True
    left=D['actor']('Repair keeper left','KeeperLeft',(3.5,8.25,.02))
    # Only a small whole-body nod is needed here; preserve this drawing's binding
    # by using one consistent transform for its controls.
    for f,angle in ((1,0),(144,0),(181,0),(188,-.035),(196,0),(END,0)):
        D['pose'](left,f,angle)
    D['smooth_actor'](left)
    D['face_keys'](left,[(1,.02),(END,.02)],[(1,.45),(END,.45)])
    left['root'].rotation_euler=(math.pi/2,0,.35)
    left['root']['Facing']='Head, torso and feet toward post; readable left-facing drawing'
    # Replace while the keeper is outside the post close-up, then reveal him.
    D['visible_tree'](keeper['root'],1,143);D['visible_tree'](left['root'],144,END)
    sh=bpy.data.objects['A Repair keeper left / ground shadow'];sh.hide_render=True;sh.hide_viewport=True
    s['facing_plan']='Rashford watches goal, turns through matched views F86–90 for embarrassed reaction; keeper left-facing in post reveal. Flat assets support planned views, not unrestricted orbit.'
    s.timeline_markers.new('turn toward viewer',frame=86)
    return {'new_views':[a['root'].name for a in (mid,front,left)]}


def post_gag():
    face=D['empty']('Repair post face',(-.16,8.92,1.20));face.rotation_euler=(math.pi/2,0,.65)
    for x in (-.06,.06):
        D['poly']('Post eye',D['oval'](x,.09,.052,.067),.02,'#fff8eb',face)
        D['poly']('Post pupil',D['oval'](x+.014,.095,.018,.03),.035,'#233039',face,False)
    D['line']('Post smirk',[(-.075,-.04),(-.015,-.065),(.08,-.035)],.04,'#26313a',.009,face)
    arm=D['empty']('Post mimicking arm',(0,0,.02),face)
    D['line']('Post arm outline',[(.03,-.32),(.36,-.32),(.43,-.14),(.23,.18)],.035,'#26313a',.043,arm)
    D['line']('Post arm fill',[(.03,-.32),(.36,-.32),(.43,-.14),(.23,.18)],.047,'#fff8e9',.031,arm)
    D['poly']('Post pointing hand',[(.20,.14),(.28,.16),(.27,.23),(.18,.28),(.08,.21),(.09,.18),(.18,.20)],.06,'#fff8e9',arm)
    D['visible_tree'](face,144,END);D['visible_tree'](arm,156,END)
    D['keys'](arm,'scale',[(1,(.01,.01,1)),(155,(.01,.01,1)),(161,(1.08,1.08,1)),(165,(1,1,1)),(END,(1,1,1))])


def checks():
    result={'scope':'Technical construction checks; visual review is separate.','frames':END,'fps':24}
    # Continuous complete surfaces, normalized weights, and the full planted interval.
    for a in (p,reaction,keeper):
        assert len(a['skin'].data.vertices)==73*133
        for v in a['skin'].data.vertices:assert abs(sum(g.weight for g in v.groups)-1)<1e-5
    for tag in ('Repair Rashford turn','Repair Rashford front','Repair keeper left'):
        skin=bpy.data.objects.get('A '+tag+' / continuous artwork')
        if skin:
            assert len(skin.data.vertices)==73*133
            assert all(abs(sum(g.weight for g in v.groups)-1)<1e-5 for v in skin.data.vertices),tag
    values=[]
    for f in range(1,42):
        s.frame_set(f);bpy.context.view_layer.update()
        values.append(p['controls']['Ltoe'].matrix_world.translation.copy())
    drift=max((v-values[0]).length for v in values);assert drift<1e-6,drift
    s.frame_set(39);bpy.context.view_layer.update()
    result['planted_toe_drift_m']=drift
    result['ball_to_toe_control_m']=(ball.matrix_world.translation-p['controls']['Rtoe'].matrix_world.translation).length
    result['note']='A toe control distance cannot clear visible boot contact; inspect consecutive frames.'
    return result


def save():
    report=checks();s.frame_set(79)
    (OUT/'technical-checks.json').write_text(json.dumps(report,indent=2)+'\n')
    (OUT/'native-events.json').write_text(s['events']+'\n')
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'rashford-repair-v001.blend'))
    return {'file':bpy.data.filepath,'checks':report}
