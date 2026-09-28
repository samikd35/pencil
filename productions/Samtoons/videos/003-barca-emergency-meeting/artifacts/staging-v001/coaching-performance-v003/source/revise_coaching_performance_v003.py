"""S07 performance pass: original art/voices, new acting and editorial timing.

Visible Blender batches: setup(), actor(name), animate(name), scene(),
surfaces(), bake(name), finish(). Reuses v002 clothing construction.
"""
import bpy,importlib.util,json,math
from pathlib import Path
from mathutils import Vector

V=Path(__file__).resolve().parents[1];O=V/'artifacts/staging-v001/coaching-performance-v003'
def load(name,file):
    spec=importlib.util.spec_from_file_location(name,V/'scripts'/file)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
M=load('coaching_v3_base','build_coaching_v001.py')
U=load('coaching_v3_surface','revise_coaching_surfaces_v002.py')
original_pose=M.pose
END=300
EVENTS={'assistant':13,'flick':88,'reaction':171,'keeper':202,'watch':238,'clipboard':254,'ball_contact':277,'release':286}

def beat(f,rows):
    """Explicit holds, short attacks and authored settles; no universal easing."""
    if f<=rows[0][0]:return rows[0][1]
    for a,b in zip(rows,rows[1:]):
        if f<=b[0]:
            t=(f-a[0])/(b[0]-a[0]);mode=b[2] if len(b)>2 else 'linear'
            if mode=='out':t=1-(1-t)**3
            elif mode=='in':t=t*t
            if isinstance(a[1],(tuple,list)):return tuple(x+(y-x)*t for x,y in zip(a[1],b[1]))
            return a[1]+(b[1]-a[1])*t
    return rows[-1][1]

def pose(name,f):
    # Retain the tested approach foot contacts, compressed only before speech.
    base=original_pose(name,min(33,1+(f-1)*2))
    hip=base['hip'].copy();feet={s:base['legs'][s][2] for s in ['L','R']}
    if name=='Flick':
        hip=Vector((beat(f,[(1,0),(258,0),(274,.045),(286,.045),(300,.025)]),beat(f,[(1,.88),(258,.88),(273,.60,'out'),(287,.60),(300,.64)])))
        lean=beat(f,[(1,.025),(77,.025),(87,.065,'out'),(102,.065),(108,.035),(156,.035),(166,.07),(177,.045),(233,.045),(241,.085),(248,.06),(257,.06),(274,.76,'out'),(286,.76),(300,.70)])
        tilt=beat(f,[(1,.09),(73,.09),(79,-.085,'out'),(86,-.055),(97,-.055),(102,.065),(108,-.045),(157,-.045),(163,.04),(170,-.06),(181,-.025),(231,-.025),(237,.19,'out'),(244,.13),(254,.08),(268,.06),(277,.13),(300,.09)])
        gaze=(beat(f,[(1,-.003),(68,-.003),(71,-.013,'out'),(195,-.013),(203,-.004),(231,-.004),(234,-.009),(300,-.009)]),beat(f,[(1,-.006),(69,-.006),(72,.001),(231,.001),(234,-.008),(300,-.008)]))
        wl=beat(f,[(1,(-.24,1.27)),(72,(-.24,1.27)),(81,(-.28,1.43),'out'),(93,(-.28,1.43)),(100,(-.38,1.51),'out'),(107,(-.32,1.45)),(119,(-.30,1.40)),(157,(-.30,1.40)),(163,(-.36,1.47),'out'),(175,(-.29,1.40)),(232,(-.29,1.40)),(238,(-.28,1.47),'out'),(245,(-.42,1.38)),(249,(-.50,1.03)),(254,(.36,1.0)),(261,(.34,.95)),(272,(-.40,.43)),(277,(-.55,.25)),(281,(-.58,.25)),(286,(-.70,.25),'in'),(293,(-.82,.38),'out'),(300,(-.80,.41))])
        if f<65:
            # Three discrete writing strokes, followed by a definite stop.
            stroke=beat(f,[(1,0),(7,0),(10,.014),(13,0),(24,0),(27,.014),(30,0),(43,0),(46,.014),(49,0)])
            wl=(wl[0]+stroke,wl[1]+stroke*.4)
        wr=beat(f,[(1,(.065,1.15)),(242,(.065,1.15)),(246,(.24,1.22)),(254,(.67,1.02),'out'),(259,(.57,.94)),(276,(.28,.71)),(300,(.28,.75))])
        modes={'L':'pen' if f<260 else ('roll' if f>=268 else 'rest'),'R':'grip' if f<=254 else 'rest'}
    else:
        if f>=18:hip=Vector((0,.88))
        lean=beat(f,[(1,-.04),(16,-.075,'out'),(27,-.075),(33,-.12),(40,-.08),(48,-.10),(73,-.10),(81,-.035,'out'),(165,-.035),(173,.09,'out'),(179,.065),(190,.065),(215,.035),(243,.035),(252,.06),(300,.04)])
        tilt=beat(f,[(1,-.025),(17,-.055),(28,-.055),(34,-.10),(40,-.04),(49,-.08),(75,-.08),(82,-.025),(164,-.025),(170,.12,'out'),(177,.08),(192,.08),(204,.035),(236,.035),(242,.10),(300,.075)])
        gaze=(beat(f,[(1,.005),(9,.012,'out'),(165,.012),(168,.003,'out'),(197,.003),(201,-.007),(217,-.007),(221,.011,'out'),(267,.011),(271,-.002),(300,-.002)]),beat(f,[(1,-.002),(9,.002),(166,.002),(170,.005),(231,.005),(235,-.004),(268,-.004),(272,-.012),(300,-.012)]))
        wr=beat(f,[(1,(.07,1.10)),(23,(.07,1.10)),(30,(.065,1.26),'out'),(35,(.06,1.23)),(163,(.06,1.23)),(172,(.045,1.08),'out'),(182,(.06,1.10)),(236,(.06,1.10)),(248,(.06,1.03)),(300,(.06,1.03))])
        wl=beat(f,[(1,(-.36,.97)),(36,(-.36,.97)),(43,(-.50,1.32),'out'),(49,(-.46,1.27)),(71,(-.46,1.27)),(82,(-.35,.98),'in'),(162,(-.35,.98)),(172,(-.43,.92),'out'),(180,(-.39,.96)),(300,(-.39,.96))])
        modes={'L':'ask' if 39<=f<=78 else 'rest','R':'grip'}
    neck=hip+Vector(M.turn((0,.57),lean));arms={};legs={}
    for side,sgn,wrist in [('L',-1,wl),('R',1,wr)]:
        sh=hip+Vector(M.turn((sgn*.14,.49),lean));axis=Vector(wrist)-sh
        # Both authored arms keep their selected bend side through this shot.
        # A fixed world pole crossed the arm axis during the lifted-paper gesture.
        pole=sh+Vector((-axis.y,axis.x))
        el=M.g.two_bone_joint(tuple(sh),tuple(wrist),(.35,.35),tuple(pole))
        arms[side]=(tuple(sh),el,tuple(wrist))
        h=hip+Vector((sgn*.10,-.045));k=M.g.two_bone_joint(tuple(h),feet[side],M.leg_lengths(name,side),(h.x+.4,h.y-.2));legs[side]=(tuple(h),k,feet[side])
    return dict(world=base['world'],hip=hip,neck=neck,lean=lean,tilt=tilt,gaze=gaze,arms=arms,legs=legs,modes=modes)

def board_pose(name,f):
    p=pose(name,min(f,254) if name=='Flick' else f)
    w=Vector(p['arms']['R'][2])+Vector(M.turn((0,.07),M.wrist_angle(p,'R')))
    return p['world']+Vector((w.x,-.02,w.y))

def ball_position(f):
    if f<=277:return M.BASE+Vector((.13,-.08,.11))
    if f<=286:
        p=pose('Flick',f);return p['world']+Vector((p['arms']['L'][2][0]-.10,-.08,.11))
    t=(f-286)/24;return ball_position(286)+Vector((-2*t,-1.05*t,0))

def camera(f):
    if f<77:x=-.12;z=1.04;width=4.55
    elif f<161:x=.71;z=1.45;width=2.35
    elif f<206:x=-.99;z=1.42;width=1.97
    else:x=.16;z=1.0;width=4.20
    target=M.BASE+Vector((x,0,z));M.CAM.location=target+Vector((0,-25,2));M.CAM.rotation_euler=(target-M.CAM.location).to_track_quat('-Z','Y').to_euler();M.CAM.data.ortho_scale=width;M.key(M.CAM,f);M.CAM.data.keyframe_insert(data_path='ortho_scale',frame=f)

def setup():
    assert not (O/'coaching-performance.blend').exists(),'Create a new revision after delivery'
    M.END=END;M.g.END=END;M.EVENTS=EVENTS;M.pose=pose;M.board_pose=board_pose;M.ball_position=ball_position;M.camera=camera
    M.O=O;M.g.O=O;O.mkdir(exist_ok=True);M.setup();M.S.name='S003_S07_Coaching_v003'
    p=board_pose('Flick',254);M.STAND.location.x=p.x-.181*.74;M.STAND.scale.z=(p.z-.16*.74)/.91
    return {'scene':M.S.name,'frames':END,'clipboard_support_height':M.STAND.scale.z*.91}

def actor(name):return M.actor(name)

def animate(name):
    M.animate_actor(name)
    a=M.A[name];env=M.speech_envelope(name);start=EVENTS['flick' if name=='Flick' else 'assistant']
    for f in range(1,END+1):
        for eye,pupil,lid in a['eyes']:
            eye.scale.z=beat(f,[(1,1),(26,1),(32,1.12),(163,1.12),(171,1.30),(183,1.12),(193,.88),(300,.9)]) if name=='Assistant' else beat(f,[(1,.9),(72,.9),(80,1),(110,.9),(230,.9),(237,1),(300,.94)])
            M.key(eye,f)
            blink=f in ([79,80,188,189,244,245] if name=='Assistant' else [74,75,184,185,243,244])
            M.visibility(lid,blink,f)
        amp=env[f-start] if 0<=f-start<len(env) else 0
        if name=='Assistant' and 171<=f<=190:amp=beat(f,[(171,.1),(174,.52),(182,.52),(190,0)])
        aperture,teeth,rest=a['mouth'];M.visibility(aperture,amp>.09,f);M.visibility(teeth,amp>.35 and not(name=='Assistant' and f>=171),f);M.visibility(rest,amp<=.09,f)
        aperture.scale.z=.12+amp*.86
        aperture.scale.x=beat(f,[(1,1),(170,1),(174,.55),(185,.55),(191,.9),(300,.9)]) if name=='Assistant' else 1
        M.key(aperture,f)
        # Closed smile flattens into disappointment after the punchline.
        if name=='Assistant':
            sad=beat(f,[(1,0),(165,0),(178,1,'out'),(300,1)])
            for i,pt in enumerate(rest.data.splines[0].points):
                pt.co.z=[0,-.005,-.004,.003][i]*(1-sad)+[-.008,.001,.001,-.008][i]*sad
                pt.keyframe_insert(data_path='co',frame=f)
    return {'actor':name,'timing':'speech unchanged; authored attacks, holds, overlap and reaction'}

def scene():
    for f in range(1,END+1):
        camera(f);M.BALL.location=ball_position(f);M.BALL.rotation_euler=(0,-max(0,f-277)*.10,0);M.key(M.BALL,f);M.BALLSHADOW.location=(M.BALL.location.x,M.BALL.location.y,.024);M.key(M.BALLSHADOW,f)
    for label,f in EVENTS.items():M.S.timeline_markers.new(label,frame=f)
    M.S['events']=json.dumps(EVENTS)
    lines=[(13,76,'ASSISTANT: We scored seven. Can we slow down now?'),(88,122,'FLICK: We did slow down.'),(123,182,'FLICK: That is why it was only seven.'),(202,231,'BARÇA KEEPER (OFFSCREEN): Can we have a break?')]
    for start,end,words in lines:
        root=M.empty('caption '+str(start),M.CAM);bg=M.poly('caption panel',[(-.455,-.019),(.455,-.019),(.455,.019),(-.455,.019)],'#172432',root);bg.rotation_euler.x=-math.pi/2
        tx=M.text('subtitle',words,root,(0,-.007,.02),.021,'#fff3d7');tx.rotation_euler.x=0
        for f in range(1,END+1):
            M.S.frame_set(f);w=M.CAM.data.ortho_scale;root.location=(0,-w*9/32+w*.043,-1);root.scale=(w,w,w);M.key(root,f);M.visibility(root,start<=f<=end,f)
    return {'frames':END,'cuts':[77,161,206]}

def surfaces():
    U.prepare(M);M.O=O;M.g.O=O;M.S.name='S003_S07_Coaching_v003'
    return {'surface_revision':'reuse v002 connected contours for the new poses'}

def bake(name):
    report=U.bake(name)
    if name=='Assistant':foreground_forearm()
    return report

def foreground_forearm():
    # The paper-holding forearm crosses the shirt in the new pose. The original
    # skin pass was behind the shirt and therefore made this arm look severed.
    a=M.A['Assistant']
    for f in range(1,END+1):
        sh,el,wr=map(Vector,pose('Assistant',f)['arms']['R'])
        q=[tuple(el.lerp(sh,.10)),tuple(el.lerp(wr,.44)),tuple(wr)]
        contour=M.g.ribbon(q,[.045,.037,.028],segments=24)
        U.native('AssistantR front skin '+str(f),U.soft(contour,.010),a['c']['skin'],a['root'],.084,f,False)
        for tag,pts in [('outer',contour[:49]),('inner',contour[49:])]:
            o=M.line('AssistantR front '+tag+str(f),pts,M.g.INK,.0018,a['root'],.085)
            for frame,hide in [(1,True),(max(1,f-1),True),(f,False),(f+1,True)]:
                o.hide_render=hide;o.hide_viewport=hide;o.keyframe_insert(data_path='hide_render',frame=frame);o.keyframe_insert(data_path='hide_viewport',frame=frame)

def finish():
    max_error=0;max_elbow_step=0;previous={}
    for f in range(1,END+1):
        for name in M.A:
            p=pose(name,f)
            for side in ['L','R']:
                elbow=Vector(p['arms'][side][1]);identity=(name,side)
                if identity in previous:
                    step=(elbow-previous[identity]).length;max_elbow_step=max(max_elbow_step,step)
                    assert step<.19,(name,f,side,'elbow jump',step)
                previous[identity]=elbow
                for chain,lengths in [(p['arms'][side],(.35,.35)),(p['legs'][side],M.leg_lengths(name,side))]:
                    error=max(abs((Vector(chain[i+1])-Vector(chain[i])).length-lengths[i]) for i in [0,1]);max_error=max(max_error,error);assert error<1e-5,(name,f,side,error)
                if f>=18:
                    anchor=p['world']+Vector((p['legs'][side][2][0],0,p['legs'][side][2][1]));q=pose(name,18);reference=q['world']+Vector((q['legs'][side][2][0],0,q['legs'][side][2][1]));assert (anchor-reference).length<1e-6
        if 277<=f<=286:
            p=pose('Flick',f);assert (ball_position(f)-p['world']-Vector((p['arms']['L'][2][0]-.10,-.08,.11))).length<1e-5
    for start,duration in [(13,2.64),(88,3.92),(202,1.2)]:assert (start-1)/24+duration<END/24
    M.g.linear_keys();M.g.sync_preview_visibility();U.save()
    M.S['performance_revision']='v003: 12.5 seconds; unchanged speech speed; short gesture attacks and settled holds; eyes lead head; early listener cut; coordinated roll.'
    bpy.ops.wm.save_as_mainfile(filepath=str(O/'coaching-performance.blend'))
    report={'frames':END,'fps':24,'seconds':12.5,'max_chain_length_error':max_error,'max_elbow_step_metres':max_elbow_step,'feet_planted_from':18,'ball_contact_frames':[277,286],'cuts':[77,161,206],'events':EVENTS,'speech_rate_changed':False,'normal_speed_creative_acceptance':False}
    (O/'construction-check.json').write_text(json.dumps(report,indent=2)+'\n');return report
