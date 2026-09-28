"""Replace the umbrella with a discarded apology and aim the red card at Foden."""
from pathlib import Path
import bpy,ast,json,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/staging-v007'
A={'__file__':str(ROOT/'scripts/build_option_a.py')};exec(compile(Path(A['__file__']).read_text(),A['__file__'],'exec'),A)
keys=A['keys']

def key_arm(scene,person,side,poses):
    cfg=json.loads((ROOT/'assets/action-a-v001/landmarks.json').read_text())[person];unit=6/cfg['body_height'];r={k:Vector(((x-cfg['center_x'])*unit,(cfg['floor_y']-y)*unit,0)) for k,(x,y) in cfg['joints'].items()}
    prefix='A '+('Drama ' if scene.name.startswith('S02') else 'Apology ')+person+' / CTRL '
    for part in ('elbow','wrist','finger'):scene.objects[prefix+side+part].animation_data_clear()
    for f,angles in poses:
        p=r[side+'shoulder'].copy()
        for start,end,t in zip(('shoulder','elbow','wrist'),('elbow','wrist','finger'),angles):
            v=r[side+end]-r[side+start];p+=Vector((math.cos(t)*v.x-math.sin(t)*v.y,math.sin(t)*v.x+math.cos(t)*v.y,0));ob=scene.objects[prefix+side+end];ob.location=p;ob.keyframe_insert(data_path='location',frame=f)

def apply():
    global scene,ball,bin_ob,card
    assert not bpy.app.background
    OUT.mkdir(exist_ok=True)
    shot=bpy.data.scenes['S02 / kick and overreaction'];bpy.context.window.scene=shot
    key_arm(shot,'Oliver','R',[(1,(.05,.08,.08)),(336,(.05,.08,.08))])
    key_arm(shot,'Oliver','L',[(1,(-.1,-.1,-.1)),(260,(-.1,-.1,-.1)),(276,(-2,-2.4,-2.4)),(283,(-1.95,-2.4,-2.4)),(336,(-1.95,-2.4,-2.4))])
    card=shot.objects['S02 / red decision'];card.parent=shot.objects['A Drama Oliver / CTRL Lfinger']
    events=json.loads(shot['events']);events['red_card']=276;shot['events']=json.dumps(events)
    shot['red_card_direction']='Left hand nearest the players, raised toward Foden.'
    scene=bpy.data.scenes['S10 / tears and umbrella'];bpy.context.window.scene=scene
    # Remove only this revision's umbrella objects, with the earlier native file retained.
    umbrella=next(o for o in scene.objects if o.type=='EMPTY' and o.name.startswith('S10 / umbrella.'))
    for ob in list(umbrella.children_recursive)+[umbrella]:bpy.data.objects.remove(ob,do_unlink=True)
    key_arm(scene,'Carrick','R',[(1,(.08,.1,.1)),(150,(.08,.1,.1)),(205,(.08,.1,.1)),(221,(.25,.9,.9)),(264,(.25,.9,.9))])
    col=scene.collection.children[0];A.update(s=scene,col=col,cam=scene.camera);A['base'].update(s=scene,skin=col,ink=A['mat']('#202329'),font=next(f for f in bpy.data.fonts if f.filepath.endswith('Arial Bold.ttf')))
    letter=scene.objects['S10 / apology letter'];children=list(letter.children);width=max(v.co.x for v in scene.objects['S10 / apology stationery'].data.vertices)
    pivot=A['empty']('S10 / crumple into held corner',(width,0,0),letter)
    for ob in children:ob.parent=pivot;ob.location.x-=width
    keys(pivot,'scale',[(1,(1,1,1)),(140,(1,1,1)),(151,(.8,.85,1)),(160,(.35,.5,1)),(170,(.02,.04,1)),(174,(0,0,0)),(264,(0,0,0))])
    hand=scene.objects['A Apology Carrick / CTRL Lfinger'];wrist=scene.objects['A Apology Carrick / CTRL Lwrist'];scene.frame_set(140);bpy.context.view_layer.update();rest=hand.location.copy();wrist_rest=wrist.location.copy()
    for f,factor in [(140,1),(151,.75),(160,.45),(170,.35),(177,.35),(186,1),(264,1)]:hand.location=wrist_rest+(rest-wrist_rest)*factor;hand.keyframe_insert(data_path='location',frame=f)
    scene.frame_set(172);bpy.context.view_layer.update();start=hand.matrix_world.translation.copy()+Vector((0,-.09,.07))
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=.09,location=start);ball=bpy.context.object;ball.name='S10 / crumpled apology'
    for c in list(ball.users_collection):c.objects.unlink(ball)
    col.objects.link(ball);ball.data.materials.append(A['mat']('#fff0cd'));ball.data.materials.append(A['mat']('#d3c8ae'))
    for i,v in enumerate(ball.data.vertices):v.co*=1+.09*math.sin(i*4.3)
    for i,p in enumerate(ball.data.polygons):p.material_index=1 if i%5==0 else 0
    keys(ball,'scale',[(1,(0,0,0)),(158,(0,0,0)),(170,(1,1,1)),(264,(1,1,1))])
    bx=start.x;by=start.y+.12
    keys(ball,'location',[(1,start),(177,start),(187,start+Vector((0,.04,-.18))),(197,(bx,by,.52)),(204,(bx,by,.25)),(264,(bx,by,.25))])
    # The paper is occluded once it passes below the bin rim.
    for f,hidden in [(1,False),(202,True)]:
        ball.hide_render=hidden;ball.hide_viewport=hidden
        ball.keyframe_insert(data_path='hide_render',frame=f);ball.keyframe_insert(data_path='hide_viewport',frame=f)
    bin_ob=A['empty']('S10 / apology bin',(bx,by-.05,.012));bin_ob.rotation_euler.x=math.pi/2
    A['poly']('S10 / bin body',[(-.27,0),(.27,0),(.36,.57),(-.36,.57)],0,'#415565',bin_ob)
    A['poly']('S10 / bin opening',A['oval'](0,.57,.36,.045),-.03,'#23313c',bin_ob,False)
    A['text']('S10 / bin label','APOLOGIES',0,.29,.025,.065,'#fff4dc',bin_ob)
    for x in (-.21,-.105,0,.105,.21):A['line']('S10 / bin ribs',[(x*.8,.07),(x,.23)],.021,'#748691',.006,bin_ob)
    # Carrick reads the letter, narrows his eyes, then looks back at Oliver.
    for i in (0,1):
        gaze=scene.objects['A Apology Carrick / gaze '+str(i)]
        keys(gaze,'location',[(1,(-.02,0,.014)),(135,(-.02,-.01,.014)),(175,(-.02,-.014,.014)),(215,(-.022,0,.014)),(264,(-.022,0,.014))])
        eye=scene.objects['A Apology Carrick / eye '+str(i)];keys(eye,'scale',[(140,(1,1,1)),(156,(1,.65,1)),(205,(1,.65,1)),(221,(1,1,1)),(264,(1,1,1))])
    events=json.loads(scene['events']);events.pop('umbrella',None);events.update(crumple=151,discard=178,bin_landing=204);scene['events']=json.dumps(events)
    scene['authored_exaggeration']='Apology letter handed over, crying, Carrick crumples and discards the useless apology, then asks about points.'
    scene.frame_set(190);bpy.context.view_layer.update()

def verify_save():
    shot=bpy.data.scenes['S02 / kick and overreaction'];assert card.parent.name.endswith('CTRL Lfinger')
    bpy.context.window.scene=shot;shot.frame_set(283);bpy.context.view_layer.update();assert card.matrix_world.translation.x<shot.objects['A Drama Oliver / ROOT'].matrix_world.translation.x
    assert not any(o.name.startswith('S10 / umbrella') for o in scene.objects)
    scene.frame_set(177);before=ball.location.z;scene.frame_set(204);after=ball.location.z;assert before>after+.5 and ball.hide_render
    report={'card_hand':'left, nearest players','umbrella_objects':0,'paper_drop_m':before-after,'apology_events':json.loads(scene['events']),'film_duration_range_seconds':[150,180],'preview_seconds':32,'audio':'silent','scene_events':{s.name:json.loads(s['events']) for s in (shot,bpy.data.scenes['S08 / hope and parry'],scene)}}
    (OUT/'native-checks.json').write_text(json.dumps(report,indent=2)+'\n');bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'clear-reactions-v001.blend'));return report
