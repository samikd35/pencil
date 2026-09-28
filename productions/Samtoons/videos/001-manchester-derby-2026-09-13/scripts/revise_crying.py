"""Cheek tears and detached falling drops for the existing apology performance."""
from pathlib import Path
import bpy,json,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/staging-v008'
A={'__file__':str(ROOT/'scripts/build_option_a.py')};exec(compile(Path(A['__file__']).read_text(),A['__file__'],'exec'),A)

def apply():
    assert not bpy.app.background
    OUT.mkdir(exist_ok=True)
    s=bpy.data.scenes['S10 / tears and umbrella'];bpy.context.window.scene=s;col=s.collection.children[0]
    A.update(s=s,col=col,cam=s.camera);A['base'].update(s=s,skin=col,ink=A['mat']('#202329'))
    for jet in [o for o in s.objects if o.name.startswith('S10 / tear jet')]:
        for ob in list(jet.children_recursive)+[jet]:bpy.data.objects.remove(ob,do_unlink=True)
    face=s.objects['A Apology Oliver / FACE'];endpoints=[];drops=[]
    for i in (0,1):
        eye=s.objects[f'A Apology Oliver / eye {i}'];ex,ey=eye.location.x,eye.location.y
        A['keys'](eye,'scale',[(1,(1,1,1)),(112,(1,1,1)),(123,(1,.48,1)),(143,(1,.65,1)),(151,(1,.25,1)),(159,(1,.55,1)),(174,(1,.28,1)),(184,(1,.6,1)),(203,(1,.32,1)),(218,(1,.55,1)),(241,(1,.3,1)),(264,(1,.55,1))])
        brow=s.objects[f'A Apology Oliver / brow control {i}'];A['keys'](brow,'rotation_euler',[(1,(0,0,0)),(113,(0,0,0)),(123,(0,0,.30 if i==0 else -.30)),(264,(0,0,.30 if i==0 else -.30))])
        outlet=Vector((ex,ey-.025,.077));trail=A['empty'](f'S10 / cheek tears {i}',outlet,face)
        pts=[];centers=[]
        for n in range(17):
            t=n/16;x=(.035 if i==0 else -.025)*math.sin(t*math.pi*.75);y=-.53*t
            width=.016+.012*math.sin(t*math.pi)+.005*math.cos(t*7)
            centers.append((x,y));pts.append((x-width,y))
        pts += [(x+.016+.012*math.sin(n/16*math.pi)+.005*math.cos(n/16*7),y) for n,(x,y) in reversed(list(enumerate(centers)))]
        A['poly'](f'S10 / wet cheek {i}',pts,0,'#6cb6d0',trail,False)
        A['line'](f'S10 / tear glint {i}',[(x-.006,y) for x,y in centers],.004,'#d9f6ff',.005,trail)
        A['poly'](f'S10 / lower lid pool {i}',A['oval'](0,0,.06,.025),.007,'#bde9f3',trail,False)
        A['keys'](trail,'scale',[(1,(0,0,1)),(118,(0,0,1)),(123,(1,.2,1)),(134,(1,1,1)),(264,(1,1,1))])
        endpoint=outlet+Vector((centers[-1][0],centers[-1][1],0));endpoints.append(list(endpoint))
        for spawn in range(136+i*5,251,13):
            s.frame_set(spawn);bpy.context.view_layer.update();origin=face.matrix_world@endpoint
            drop=A['empty'](f'S10 / falling tear {i}-{spawn}',origin);drop.rotation_euler=s.camera.rotation_euler.copy()
            A['poly'](drop.name+' water',[(0,.026),(-.011,.003),(-.012,-.008),(-.007,-.015),(.003,-.017),(.011,-.010),(.01,.002)],0,'#79c1da',drop,False)
            A['line'](drop.name+' shine',[(-.004,.009),(-.005,-.004)],.002,'#e4faff',.002,drop)
            # Once detached, each drop falls in world space rather than following the face.
            life=math.ceil(math.sqrt(2*max(origin.z-.02,.01)/9.8)*24)
            drop.scale=(0,0,0);drop.keyframe_insert(data_path='scale',frame=spawn-1)
            for n in range(life+1):
                t=n/24;drop.location=origin+Vector((.025*t,0,-4.9*t*t));drop.location.z=max(.021,drop.location.z)
                drop.keyframe_insert(data_path='location',frame=spawn+n)
                drop.scale=(1,1+.6*n/life,1) if n<life else (0,0,0);drop.keyframe_insert(data_path='scale',frame=spawn+n)
            for layer in drop.animation_data.action.layers:
                for strip in layer.strips:
                    for bag in strip.channelbags:
                        for fc in bag.fcurves:
                            for k in fc.keyframe_points:k.interpolation='LINEAR'
            drops.append(drop.name)
    events=json.loads(s['events']);events.update(tears=119,cheek_flow=123,first_falling_drop=136);s['events']=json.dumps(events)
    s['crying_treatment']='Tears gather at lower lids, follow cheeks, detach at the jaw and fall under gravity; squeezed eyes and raised inner brows.'
    shot=bpy.data.scenes['S02 / kick and overreaction'];events=json.loads(shot['events']);events['red_card']=276;shot['events']=json.dumps(events)
    assert len(drops)==18 and not any(o.name.startswith('S10 / tear jet') for o in s.objects)
    s.frame_set(118);assert all(s.objects[f'S10 / cheek tears {i}'].scale.y==0 for i in (0,1))
    s.frame_set(150);assert all(s.objects[f'S10 / cheek tears {i}'].scale.y>.9 for i in (0,1))
    report=json.loads((ROOT/'artifacts/staging-v007/native-checks.json').read_text());report.update(apology_events=json.loads(s['events']),crying_treatment=s['crying_treatment'],detached_droplets=len(drops),scene_events={scene.name:json.loads(scene['events']) for scene in (shot,bpy.data.scenes['S08 / hope and parry'],s)})
    (OUT/'native-checks.json').write_text(json.dumps(report,indent=2)+'\n')
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'natural-tears-v001.blend'))
    for f in (118,134,150,177,198,225):s.frame_set(f);s.render.filepath=str(OUT/f'apology-{f:03}.png');bpy.ops.render.render(write_still=True)
    return report
