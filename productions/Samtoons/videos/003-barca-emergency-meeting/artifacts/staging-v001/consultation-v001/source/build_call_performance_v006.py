"""S08 reconstructed skeleton-first; art assets and audio are reused, motion is new.

In visible Blender: setup(); foundation(); attach_art(); finish(). The foundation
is saved before any caricature artwork is attached. No earlier pose/animate
function is called. The selected drawing determines proportions, not motion.
"""
import bpy, hashlib, json, math, struct
from pathlib import Path
from mathutils import Vector, Matrix

V=Path(__file__).resolve().parents[1]
O=V/'artifacts/staging-v001/call-performance-v006'
p=V/'scripts/build_call_performance_v005.py'
asset={'__file__':str(p)}
exec(compile(p.read_text().replace('v005','v006').replace('C3V5','C3V6'),str(p),'exec'),asset)
n=asset['n'];B=n['B'];interp=n['interp'];xy=n['xy'];rot=n['rot'];PREFIX='C3V6 / '
A={};proof=[];errors=[]

# New performance authored in wrist targets and body/head angles. These keys
# belong to this scene; no prior joint trajectories or animation are transferred.
BEATS={
 'Muller':{
  'torso':[(1,0),(20,-1),(39,-2.8),(61,-1.4),(85,-2),(111,-.5),(145,0),(171,2.2),(211,3.8),(240,3)],
  'head':[(1,1),(20,3),(37,-5),(59,-1),(81,-3),(110,0),(143,0),(155,4),(181,6),(218,3),(240,3)],
  'wrist':[(1,(18,-24)),(20,(25,-40)),(38,(-30,38)),(61,(-19,21)),(84,(-26,30)),(106,(-14,14)),(151,(-14,14)),(167,(-8,21)),(207,(31,-115)),(225,(39,-130)),(240,(36,-123))],
  'hand':[(1,3),(20,7),(38,-9),(63,-4),(84,-7),(110,-2),(164,-2),(215,13),(240,10)],
  'gaze':[(1,0),(14,-5),(29,0),(140,0),(150,-12),(173,-12),(205,-6),(240,-6)],
  'blink':[(1,0),(18,0),(20,1),(23,0),(137,0),(139,1),(142,0),(240,0)],
  'brow':[(1,0),(30,0),(40,-4),(100,0),(149,0),(170,17),(240,17)]},
 'Perez':{
  'torso':[(1,0),(37,-1.1),(72,0),(102,.8),(123,-4),(153,-5.3),(181,-3.2),(209,-1.4),(240,-1.4)],
  'head':[(1,1),(36,3),(65,0),(106,0),(121,-3),(147,-5),(176,0),(208,3),(240,3)],
  'wrist':[(1,(0,0)),(42,(-8,5)),(77,(0,0)),(103,(10,-8)),(124,(-32,22)),(150,(-69,12)),(173,(-54,7)),(199,(-9,15)),(220,(0,10)),(240,(0,10))],
  'hand':[(1,0),(100,0),(125,-12),(151,-23),(173,-20),(203,2),(240,2)],
  'gaze':[(1,-2),(73,-2),(84,1),(99,-2),(195,-2),(211,2),(240,2)],
  'blink':[(1,0),(78,0),(80,1),(83,0),(200,0),(202,1),(205,0),(240,0)],
  'brow':[(1,0),(105,0),(125,5),(153,10),(179,6),(240,3)]}}


def setup():
    global s
    n['setup']();s=n['s'];O.mkdir(parents=True,exist_ok=True)
    s['construction']='Fresh connected skeleton and newly authored performance; caricature attached after body proof.'
    return {'scene':s.name,'stage':'new skeleton first'}


def skeleton(who):
    data=json.loads((V/f'assets/reference-redraw-v003/{who.lower()}-contours.json').read_text());c=data['design'];c['who']=who
    root=B['control'](who+' foundation root',c['location']);root.scale=(c['scale'],)*3
    points={'hip':c['hip'],'neck':c['neck'],'head':[c['neck'][0],c['neck'][1]-220]}
    bones={'torso':('hip','neck'),'head':('neck','head')}
    for side in ['L','R']:
        for label,pt in zip(['shoulder','elbow','wrist'],c[side]):points[side+' '+label]=pt
        points[side+' finger']=[c[side][2][0],c[side][2][1]-75]
        bones.update({side+' '+name:(side+' '+u,side+' '+v) for name,u,v in [('upper','shoulder','elbow'),('fore','elbow','wrist'),('hand','wrist','finger')]})
    rest={name:xy(pt,c['origin']) for name,pt in points.items()}
    ad=bpy.data.armatures.new(PREFIX+who+' fitted drawing rig');rig=bpy.data.objects.new(ad.name,ad);n['col'].objects.link(rig);rig.parent=root;rig.show_in_front=True;ad.display_type='STICK'
    bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT')
    for name,(u,v) in bones.items():
        eb=ad.edit_bones.new(name);eb.head=rest[u];eb.tail=rest[v];eb.align_roll(Vector((0,0,1)))
        parent='torso' if name=='head' or name.endswith('upper') else name.split()[0]+' '+('upper' if name.endswith('fore') else 'fore') if name!='torso' else None
        if parent:eb.parent=ad.edit_bones[parent];eb.use_connect=not name.endswith('upper')
    bpy.ops.object.mode_set(mode='OBJECT')
    for pb in rig.pose.bones:pb.rotation_mode='XYZ'
    a={'c':c,'data':data,'root':root,'rig':rig,'rest':rest,'bones':bones,'surfaces':[],'controls':{}}
    a['heading']={name:math.atan2((rest[v]-rest[u]).y,(rest[v]-rest[u]).x) for name,(u,v) in bones.items()};A[who]=a
    return a


def pose(a,f):
    who=a['c']['who'];k=BEATS[who];r=a['rest'];hip=r['hip'];angle=interp(f,k['torso']);head=interp(f,k['head'])
    def torso(v):return hip+rot(v-hip,angle)
    points={'hip':hip,'neck':torso(r['neck'])};points['head']=points['neck']+rot(r['head']-r['neck'],angle+head)
    for side in ['L','R']:
        sh=torso(r[side+' shoulder']);wr=r[side+' wrist'].copy()
        if side=='L':
            dx,dy=interp(f,k['wrist']);wr+=Vector((dx,dy,0));hand=interp(f,k['hand'])
        elif who=='Perez':hand=0 # Table contact stays fixed while the torso leans.
        else:wr=torso(wr);hand=angle
        pole=n['transported_pole'](tuple(r[side+' shoulder'][:2]),tuple(r[side+' wrist'][:2]),tuple(r[side+' elbow'][:2]),tuple(sh[:2]),tuple(wr[:2]))
        lengths=((r[side+' elbow']-r[side+' shoulder']).length,(r[side+' wrist']-r[side+' elbow']).length)
        elbow=Vector((*n['two_bone_joint'](tuple(sh[:2]),tuple(wr[:2]),lengths,pole),0))
        if side=='L':
            fore=wr-elbow;fa=math.degrees(math.atan2(fore.y,fore.x));delta=(90+hand-fa+180)%360-180
            hand=fa+max(-40,min(40,delta))-90
        for key,pt in [('shoulder',sh),('elbow',elbow),('wrist',wr),('finger',wr+rot(Vector((0,75,0)),hand))]:points[side+' '+key]=pt
    delta={}
    for name,(u,v) in a['bones'].items():
        d=points[v]-points[u];angle=math.atan2(d.y,d.x)-a['heading'][name];delta[name]=(angle+math.pi)%(2*math.pi)-math.pi
    for name,pb in a['rig'].pose.bones.items():
        pb.rotation_euler=(0,0,delta[name]-(delta[pb.parent.name] if pb.parent else 0));pb.keyframe_insert(data_path='rotation_euler',frame=f)
    bpy.context.view_layer.update()
    for name,(u,v) in a['bones'].items():errors.extend([(a['rig'].pose.bones[name].head-points[u]).length,(a['rig'].pose.bones[name].tail-points[v]).length])


def proof_drawing(a):
    """Renderable skeleton: the same bone action will drive the finished art."""
    def surface(label,pts,color,bone,z=10):
        ob=B['shape'](a['c']['who']+' foundation '+label,pts,z,color,a['root'],False,False)
        vg=ob.vertex_groups.new(name=bone);vg.add(list(range(len(ob.data.vertices))),1,'REPLACE')
        mod=ob.modifiers.new('Foundation skeleton','ARMATURE');mod.object=a['rig'];proof.append(ob)
    for name,(u,v) in a['bones'].items():
        if name=='head':continue
        start,end=a['rest'][u],a['rest'][v];d=end-start;normal=Vector((-d.y,d.x,0)).normalized()*10
        surface(name,[tuple(pt[:2]) for pt in [start-normal,start+normal,end+normal,end-normal]],'#202332',name)
        for point in [start,end]:surface(name+' joint',[(point.x+14*math.cos(i*math.tau/20),point.y+14*math.sin(i*math.tau/20)) for i in range(20)],'#f3ce79',name,11)
    neck=a['rest']['neck'];center=neck+Vector((0,138,0))
    surface('head',[(center.x+95*math.cos(i*math.tau/48),center.y+137*math.sin(i*math.tau/48)) for i in range(48)],'#f3ce79','head',12)
    for side in [-1,1]:surface('eye',[(center.x+side*31+10*math.cos(i*math.tau/16),center.y+22+13*math.sin(i*math.tau/16)) for i in range(16)],'#202332','head',13)
    for side in ['L','R']:
        p=a['rest'][side+' shoulder'];q=a['rest']['neck'];d=p-q;normal=Vector((-d.y,d.x,0)).normalized()*7
        surface('shoulder tie',[tuple(pt[:2]) for pt in [p-normal,p+normal,q+normal,q-normal]],'#202332','torso',9)
    before=set(bpy.data.objects);n['carried_prop'](a)
    proof.extend(ob for ob in bpy.data.objects if ob not in before)


def captions():
    for start,end,words in [(25,96,'MÜLLER: Eight goals. A very good night.'),(113,198,'PÉREZ: Good. How do we stop Flick doing that to us?')]:
        ob=B['text']('subtitle',words,0,-334,181,22,'#f5efdf')
        for f,visible in [(1,False),(start,True),(end,False)]:
            ob.hide_render=ob.hide_viewport=not visible
            for prop in ['hide_render','hide_viewport']:ob.keyframe_insert(data_path=prop,frame=f)
    B['rect']('call desk',-581,-197,656,23,25,'#9b704b',outline=False)
    B['rect']('monitor lower bevel',-594,-219,682,22,27,'#263448',outline=False)
    B['text']('call name','THOMAS MÜLLER · BAYERN LEGEND',-268,-207,29,12,'#d2dce5')


def interpolation():
    for action in bpy.data.actions:
        if not action.name.startswith(PREFIX):continue
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for fc in bag.fcurves:
                        for key in fc.keyframe_points:key.interpolation='CONSTANT' if 'hide_' in fc.data_path else 'LINEAR'


def foundation():
    for who in ['Muller','Perez']:proof_drawing(skeleton(who))
    for f in range(1,241):
        s.frame_set(f)
        for a in A.values():pose(a,f)
    assert errors and max(errors)<.005,max(errors)
    captions();interpolation();s.frame_set(38)
    bpy.ops.wm.save_as_mainfile(filepath=str(O/'stickman-foundation.blend'))
    (O/'movement-beats.json').write_text(json.dumps(BEATS,indent=2)+'\n')
    (O/'foundation-check.json').write_text(json.dumps({'motion_sha256':motion_digest(),'max_joint_error_source_pixels':max(errors),'prior_motion_called':False},indent=2)+'\n')
    return {'foundation':str(O/'stickman-foundation.blend'),'max_joint_error_source_pixels':max(errors),'prior_motion_called':False}


def motion_digest():
    digest=hashlib.sha256()
    for f in range(1,241):
        s.frame_set(f);bpy.context.view_layer.update()
        for a in A.values():
            for name in a['bones']:
                values=[value for row in a['rig'].pose.bones[name].matrix for value in row]
                digest.update(struct.pack('<16f',*values))
    return digest.hexdigest()


def attach_art():
    # Reuse the selected art-construction helper, never its pose or animation.
    # Its temporary rest armature is discarded; every surface is retargeted to
    # the already animated foundation with identical rest coordinates.
    s.frame_set(1)
    for ob in proof:bpy.data.objects.remove(ob,do_unlink=True)
    for who,a in A.items():
        n['actor'](who);drawing=n['A'][who];old_root=drawing['root'];old_rig=drawing['rig']
        for ob in list(old_root.children):
            if ob!=old_rig:ob.parent=a['root']
        for ob in drawing['surfaces']:
            for mod in ob.modifiers:
                if mod.type=='ARMATURE':mod.object=a['rig']
        for ob in drawing['controls'].values():bpy.data.objects.remove(ob,do_unlink=True)
        bpy.data.objects.remove(old_rig,do_unlink=True);bpy.data.objects.remove(old_root,do_unlink=True)
        for key in ['surfaces','face','eyes','brows','mouths']:a[key]=drawing[key]
        n['A'][who]=a;asset['bound_wrist'](a)
        face=a['face'];anchor=B['control'](who+' head attachment',parent=a['root'])
        co=anchor.constraints.new('COPY_TRANSFORMS');co.target=a['rig'];co.subtarget='head';co.target_space='POSE';co.owner_space='LOCAL'
        face.parent=anchor;face.matrix_parent_inverse=Matrix.Identity(4);face.matrix_basis=a['rig'].data.bones['head'].matrix_local.inverted()@Matrix.Translation(a['rest']['neck'])
    return {'bound_to_original_foundation':True,'prior_body_motion_imported':False}


def finish():
    phrases={'Muller':[(1,'smile'),(26,'E'),(31,'A'),(35,'rest'),(38,'O'),(49,'rest'),(61,'A'),(65,'FV'),(70,'E'),(77,'O'),(83,'A'),(89,'E'),(95,'smile'),(156,'tight')],
             'Perez':[(1,'rest'),(114,'O'),(122,'rest'),(132,'A'),(139,'O'),(145,'E'),(151,'O'),(156,'FV'),(161,'E'),(166,'O'),(174,'E'),(180,'A'),(186,'O'),(193,'A'),(196,'rest')]}
    for f in range(1,241):
        s.frame_set(f)
        for who,a in A.items():
            k=BEATS[who];c=a['c'];blink=interp(f,k['blink']);brow=interp(f,k['brow'])
            for i,(gaze,closed,line,top,bottom) in enumerate(a['eyes']):
                gaze.location.x=c['eyes'][i]['pupil'][0]-c['eyes'][i]['center'][0]+interp(f,k['gaze']);gaze.keyframe_insert(data_path='location',frame=f)
                closed.value=blink;closed.keyframe_insert(data_path='value',frame=f);line.hide_render=line.hide_viewport=blink<.9
                for prop in ['hide_render','hide_viewport']:line.keyframe_insert(data_path=prop,frame=f)
                a['brows'][i].rotation_euler.z=math.radians(brow*(1 if i==0 else -1));a['brows'][i].keyframe_insert(data_path='rotation_euler',frame=f)
    for who,rows in phrases.items():
        for f,label in rows:
            for name,group in A[who]['mouths'].items():
                for ob in group.children_recursive:
                    ob.hide_render=ob.hide_viewport=name!=label
                    for prop in ['hide_render','hide_viewport']:ob.keyframe_insert(data_path=prop,frame=f)
    interpolation()
    for a in A.values():
        assert all(not pb.constraints for pb in a['rig'].pose.bones)
        for ob in a['surfaces']:
            assert len([m for m in ob.modifiers if m.type=='ARMATURE' and m.object==a['rig']])==1,ob.name
            assert all(abs(sum(g.weight for g in v.groups)-1)<1e-5 for v in ob.data.vertices),ob.name
            assert not ob.data.shape_keys,ob.name
    digest=motion_digest();assert digest==json.loads((O/'foundation-check.json').read_text())['motion_sha256'],'Attaching artwork changed the foundation motion'
    s.frame_set(38);s['construction']='New connected stickman foundation authored and saved first; existing vector likeness bound afterward. New body/head/gaze/brow performance; same audio-aligned mouth drawings. Not Grease Pencil.'
    s['scope']='10-second S08 call; current view and grips. Extreme new views still need drawings.'
    bpy.ops.wm.save_as_mainfile(filepath=str(O/'call-performance.blend'))
    report={'frames':240,'foundation_saved_before_art':True,'prior_pose_or_animate_called':False,'new_body_and_head_motion':True,'one_skeleton_per_actor':True,'independent_joint_objects':0,'wrist_shape_keys':0,'max_joint_error_source_pixels':max(errors),'foundation_motion_unchanged_after_binding':True,'motion_sha256':digest,'audio':'Exact v004 track reused'}
    (O/'binding-check.json').write_text(json.dumps(report,indent=2)+'\n');return report


def build():
    setup();foundation();attach_art();return finish()
