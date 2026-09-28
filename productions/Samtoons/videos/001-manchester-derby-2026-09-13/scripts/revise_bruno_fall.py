"""Add Bruno's fall/get-up to the approved S02, leaving the other scenes intact.
Run apply() in visible Blender, inspect selected frames, then save().
"""
from pathlib import Path
import bpy,ast,json,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/staging-v006'
# Reuse the approved pose helpers without rebuilding any characters or scenery.
source=ast.parse((ROOT/'scripts/build_dramatic_actions.py').read_text())
exec(compile(ast.Module(body=[n for n in source.body if isinstance(n,ast.FunctionDef) and n.name in ('pose','rotate','smooth_actor')],type_ignores=[]),'approved_pose_helpers','exec'))

def curves(action):
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                yield from bag.fcurves

def apply():
    global s,bruno
    assert not bpy.app.background
    assert bpy.data.filepath.endswith('staging-v005/dramatic-actions-v002.blend')
    s=bpy.data.scenes['S02 / kick and overreaction'];assert s.frame_end==288
    bpy.context.window.scene=s;OUT.mkdir(exist_ok=True)
    # Insert two seconds after the contact, preserving the approved complaint/cuts.
    seen=set()
    for ob in s.objects:
        if not ob.animation_data or not ob.animation_data.action:continue
        action=ob.animation_data.action
        if action.as_pointer() in seen:continue
        if action.users>1:action=action.copy();ob.animation_data.action=action
        seen.add(action.as_pointer())
        for fc in curves(action):
            for k in fc.keyframe_points:
                if k.co.x>=84:
                    k.co.x+=48;k.handle_left.x+=48;k.handle_right.x+=48
            fc.update()
    config=json.loads((ROOT/'assets/option-a-v001/landmarks.json').read_text())['Bruno']
    unit=6/config['body_height'];nx,ny=config['joints']['neck']
    def xy(p):
        x,y=p;growth=.35*max(0,min(1,(ny-y)/50))
        return Vector(((x-config['center_x']+growth*(x-nx))*unit,(config['floor_y']-y+growth*(ny-y))*unit,0))
    bruno={'root':s.objects['A Drama Bruno / ROOT'],'controls':{k:s.objects['A Drama Bruno / CTRL '+k] for k in config['joints']},'rest':{k:xy(p) for k,p in config['joints'].items()}}
    arms=lambda l,r:[('L',['shoulder','elbow','wrist','finger'],l),('R',['shoulder','elbow','wrist','finger'],r)]
    for f,t,off in [(83,-.03,(0,0)),(90,-.40,(.3,-.2)),(101,-1.0,(.85,-1.0)),(110,-1.22,(1.10,-1.38)),(121,-1.20,(1.10,-1.38)),(131,-.75,(.65,-.65)),(141,-.15,(.10,-.04)),(148,-.03,(0,0))]:
        if 101<=f<=121:
            limbs=[('L',['hip','knee','ankle','toe'],[-1.65,-1.7,-1.7]),('R',['hip','knee','ankle','toe'],[-.85,-1.6,-1.6])]+arms([-1.22,-1.22,-1.22],[-1.05,-1.4,-1.9])
        else:limbs=arms([-.3,-.6,-.6],[.2,.2,.2])
        pose(bruno,f,t,off,limbs)
        if f>=131 or f==83:
            for k in ('Lankle','Rankle','Ltoe','Rtoe'):
                bruno['controls'][k].location=bruno['rest'][k];bruno['controls'][k].keyframe_insert(data_path='location',frame=f)
    smooth_actor(bruno)
    mouth=s.objects['A Drama Bruno / mouth control']
    for f,v in [(83,.05),(93,.8),(110,1.1),(121,.6),(141,.05),(148,.05)]:mouth['open']=v;mouth.keyframe_insert(data_path='["open"]',frame=f)
    s.frame_end=336
    events=json.loads(s['events']);events={k:v+48 if v>=84 else v for k,v in events.items()};events.update(bruno_fall=90,bruno_ground_contact=110,bruno_rise=131,bruno_standing=148);s['events']=json.dumps(events)
    s['authored_exaggeration']='After Foden kicks out, Bruno falls theatrically, gets up, then resumes the approved appeal, halo and complaint.'
    s.frame_set(110);bpy.context.view_layer.update()
    return {'events':events,'frames':336}

def verify():
    heights={}
    for f in (77,110,148):
        s.frame_set(f);bpy.context.view_layer.update();heights[f]=bruno['controls']['hip'].matrix_world.translation.z
    assert heights[110]<heights[77]-.35,heights
    assert abs(heights[148]-heights[77])<.02,heights
    assert json.loads(s['events'])['complaint']==225
    report={'hip_height_m':heights,'S02_frames':336,'fps':24,'sequence':'kick 77 -> fall 90 -> grounded 110 -> rise 131 -> upright 148 -> appeal 154 -> complaint 225','other_scenes':'S08 parry unchanged; S10 revised with letter handoff before tears','audio':'silent picture revision'}
    apology=bpy.data.scenes['S10 / tears and umbrella'];bpy.context.window.scene=apology
    letter=apology.objects['S10 / apology letter'];positions={}
    for f in (74,75,118,119,169,170):
        apology.frame_set(f);bpy.context.view_layer.update()
        positions[f]=letter.matrix_world.translation.copy()
        if f in (118,119):assert apology.objects['S10 / eye-anchored water 0'].hide_render==(f==118)
        if f in (169,170):assert apology.objects['S10 / umbrella canopy'].hide_render==(f==169)
    jump=(positions[75]-positions[74]).length;assert jump<.04,jump
    assert not any(o.name.startswith(('A / goal','A / area line')) for o in s.objects)
    assert any(o.name.startswith('A / goal') for o in bpy.data.scenes['S08 / hope and parry'].objects)
    report.update(letter_handoff_displacement_m=jump,apology_events=json.loads(apology['events']),touchline_verified=True,goal_preserved_in_parry=True)
    (OUT/'native-checks.json').write_text(json.dumps(report,indent=2)+'\n');return report

def save():
    verify();s.frame_set(110);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'revised-actions-v001.blend'))

def apology_letter():
    global apology,letter
    apology=bpy.data.scenes['S10 / tears and umbrella'];assert apology.frame_end==192
    bpy.context.window.scene=apology
    seen=set()
    for ob in apology.objects:
        if not ob.animation_data or not ob.animation_data.action:continue
        action=ob.animation_data.action
        if action.as_pointer() in seen:continue
        if action.users>1:action=action.copy();ob.animation_data.action=action
        seen.add(action.as_pointer())
        for fc in curves(action):
            for k in fc.keyframe_points:
                if k.co.x>=2:k.co.x+=72;k.handle_left.x+=72;k.handle_right.x+=72
            fc.update()
    config=json.loads((ROOT/'assets/action-a-v001/landmarks.json').read_text())
    def existing(person):
        cfg=config[person];unit=6/cfg['body_height'];nx,ny=cfg['joints']['neck']
        rest={}
        for k,(x,y) in cfg['joints'].items():
            growth=.35*max(0,min(1,(ny-y)/50));rest[k]=Vector(((x-cfg['center_x']+growth*(x-nx))*unit,(cfg['floor_y']-y+growth*(ny-y))*unit,0))
        return {'root':apology.objects['A Apology '+person+' / ROOT'],'rest':rest,'controls':{k:apology.objects['A Apology '+person+' / CTRL '+k] for k in rest}}
    r=existing('Oliver');c=existing('Carrick')
    arms=lambda l,rr:[('L',['shoulder','elbow','wrist','finger'],l),('R',['shoulder','elbow','wrist','finger'],rr)]
    for control in c['controls'].values():control.animation_data_clear()
    for f,reach in ((1,.55),(30,.55),(55,1.55),(75,1.55),(82,1.55)):pose(r,f,limbs=arms([-.08,-.15,-.15],[.18,reach,reach]))
    for f,reach in ((1,-.1),(30,-.1),(55,-1.6),(75,-1.6),(95,-1.6),(150,-1.6)):pose(c,f,limbs=arms([-.08,reach,reach],[.08,.1,.1]))
    for f in (170,184,264):pose(c,f,limbs=arms([-.08,-1.6,-1.6],[.12,1.6,1.6]))
    smooth_actor(r);smooth_actor(c)
    for person in ('Oliver','Carrick'):
        mouth=apology.objects['A Apology '+person+' / mouth control']
        for f,v in [(1,.03),(55,.03),(65,.20 if person=='Oliver' else .03),(75,.03),(82,.03)]:mouth['open']=v;mouth.keyframe_insert(data_path='["open"]',frame=f)
    # Reuse the native shape and type helpers from the approved scene builder.
    A={'__file__':str(ROOT/'scripts/build_option_a.py')};exec(compile(Path(A['__file__']).read_text(),A['__file__'],'exec'),A)
    col=apology.collection.children[0];A.update(s=apology,col=col,cam=apology.camera);A['base'].update(s=apology,skin=col,ink=A['mat']('#202329'),font=next(f for f in bpy.data.fonts if f.filepath.endswith('Arial Bold.ttf')))
    apology.frame_set(75);bpy.context.view_layer.update()
    giver=r['controls']['Rfinger'];receiver=c['controls']['Lfinger'];right=Vector((1,0,0));width=receiver.matrix_world.translation.x-giver.matrix_world.translation.x
    assert .2<width<.9,width
    letter=A['empty']('S10 / apology letter',(0,0,0));letter.rotation_euler.x=math.pi/2
    # Each hand holds one lower corner. Constant ownership switch occurs at contact.
    letter['recipient']=0.
    for f,value in [(1,0.),(74,0.),(75,1.),(264,1.)]:letter['recipient']=value;letter.keyframe_insert(data_path='["recipient"]',frame=f)
    for fc in curves(letter.animation_data.action):
        for k in fc.keyframe_points:k.interpolation='CONSTANT'
    for axis in range(3):
        driver=letter.driver_add('location',axis).driver
        for name,target in [('g',giver),('r',receiver)]:
            v=driver.variables.new();v.name=name;v.type='TRANSFORMS';v.targets[0].id=target;v.targets[0].transform_type=('LOC_X','LOC_Y','LOC_Z')[axis];v.targets[0].transform_space='WORLD_SPACE'
        v=driver.variables.new();v.name='t';v.type='SINGLE_PROP';v.targets[0].id=letter;v.targets[0].data_path='["recipient"]'
        offset=width if axis==0 else 0
        driver.expression=f'(1-t)*g+t*(r-{offset})'+('-.06' if axis==1 else '')
    A['rect']('S10 / apology stationery',0,0,width,.49,0,'#fff3d5',letter)
    for ob in letter.children:
        if ob.type=='CURVE':ob.data.bevel_depth=.004
    A['text']('S10 / SORRY heading','SORRY',width/2,.34,.025,width*.23,'#b32739',letter)
    A['text']('S10 / apology explanation','OUR MISTAKE',width/2,.245,.025,width*.074,'#263a48',letter)
    for y in (.16,.10):A['line']('S10 / letter rule',[(width*.15,y),(width*.85,y)],.024,'#9e9d97',.004,letter)
    umbrella=next(o for o in apology.objects if o.name.startswith('S10 / umbrella.') and o.type=='EMPTY');umbrella.parent=c['controls']['Rfinger'];umbrella.scale.x=-1
    # Keep the document and handoff large enough to read before returning to the wide crying shot.
    cam=apology.camera;wide=cam.location.copy();wide_rot=cam.rotation_euler.copy()
    for f,loc,target in [(1,(.25,-4.7,2.05),(.10,0,1.35)),(82,(.25,-4.7,2.05),(.10,0,1.35)),(83,wide,None)]:
        cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler() if target else wide_rot
        cam.keyframe_insert(data_path='location',frame=f);cam.keyframe_insert(data_path='rotation_euler',frame=f)
    for fc in curves(cam.animation_data.action):
        for k in fc.keyframe_points:k.interpolation='CONSTANT'
    apology.frame_end=264
    events=json.loads(apology['events']);events={k:v+72 for k,v in events.items()};events.update(letter_presented=1,letter_handoff=75);apology['events']=json.dumps(events)
    apology['authored_exaggeration']='Fictional apology: visible SORRY letter, handed to Carrick, then sobbing; Carrick responds with umbrella.'
    apology.frame_set(75);bpy.context.view_layer.update()
    return {'letter_width_m':width,'events':events}


def touchline():
    # Unlink the reused penalty-area set from S02 only; preserve it in the save scene.
    scene=bpy.data.scenes['S02 / kick and overreaction'];col=scene.collection.children[0]
    removed=[]
    for ob in list(col.objects):
        if ob.name.startswith(('A / goal','A / net','A / top net','A / side net','A / area line')):removed.append(ob.name);col.objects.unlink(ob)
    assert removed
    d=bpy.data.curves.new('S02 / touchline','CURVE');d.dimensions='3D';d.bevel_depth=.032;d.bevel_resolution=2
    sp=d.splines.new('POLY');sp.points.add(1);sp.points[0].co=(-40,-.80,.019,1);sp.points[1].co=(40,-.80,.019,1)
    d.materials.append(next(m for m in bpy.data.materials if m.name.startswith('#f7f5e7')) if any(m.name.startswith('#f7f5e7') for m in bpy.data.materials) else bpy.data.objects['A / goal front'].data.materials[0])
    ob=bpy.data.objects.new(d.name,d);col.objects.link(ob)
    scene['Location']='Touchline tussle, referenced to adjacent wide match frames. No nearby goal or penalty-area lines.'
    assert not any(o.name.startswith(('A / goal','A / area line')) for o in scene.objects)
    return {'removed_goal_and_area_objects':len(removed),'touchline_y':-.8}
