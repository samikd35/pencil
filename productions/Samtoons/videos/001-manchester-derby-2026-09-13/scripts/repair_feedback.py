"""Repair v002: preserve source anatomy and draw a profile eye on a profile face."""
from pathlib import Path
import bpy, runpy, math, json
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/repair-v002'
R=runpy.run_path(str(ROOT/'scripts/repair_rashford.py'))
R['resume']()
D,A=R['D'],R['A']
s=bpy.context.scene

def rest_from_bones(arm):
    endpoints={'torso':('hip','neck'),'head':('neck','head')}
    for side in ('L','R'):
        endpoints.update({side+' '+bone:(side+a,side+b) for bone,a,b in [
            ('upper arm','shoulder','elbow'),('forearm','elbow','wrist'),
            ('hand','wrist','finger'),('thigh','hip','knee'),
            ('calf','knee','ankle'),('foot','ankle','toe')]})
    rest={}
    for bone,(a,b) in endpoints.items():
        rest[a]=arm.data.bones[bone].head_local.copy()
        rest[b]=arm.data.bones[bone].tail_local.copy()
    return rest

def replace_raised_views():
    for old,new,person,start,end in [
        ('Repair Rashford temple','Fixed Rashford temple','RashfordTemple',42,85),
        ('Repair Rashford turn','Fixed Rashford turn','RashfordTurn',86,89),
        ('Repair Rashford front','Fixed Rashford front','RashfordFront',90,143)]:
        prefix='A '+old+' / '
        oldroot=bpy.data.objects[prefix+'ROOT']
        oldrest=rest_from_bones(bpy.data.objects[prefix+'skin binding'])
        cfg=dict(R['CFG'][person],head_growth=0)
        a=A['actor'](new,cfg,oldroot.location)
        R['fit_surface'](a,True)
        a['root'].rotation_euler=oldroot.rotation_euler
        for f in [1,42,56,73,79,86,89,90,97,104,111,118,130,143,216]:
            s.frame_set(f);bpy.context.view_layer.update()
            for key,ob in a['controls'].items():
                delta=bpy.data.objects[prefix+'CTRL '+key].location-oldrest[key]
                ob.location=a['rest'][key]+delta/(1.35 if key in ('head','Rwrist','Rfinger') else 1)
                ob.keyframe_insert(data_path='location',frame=f)
        D['smooth_actor'](a)
        # Keep the already reviewed performance on the new matching face coordinates.
        for key,obj in a['facial'].items():
            label={'mouth':'mouth control'}.get(key)
            if label is None:
                label=next((p+' '+key[-1] for p in ('eye','gaze','brow control') if key.startswith(p.split()[0])),None)
            src=bpy.data.objects.get(prefix+label) if label else None
            if src and src.animation_data and src.animation_data.action:
                obj.animation_data_create();obj.animation_data.action=src.animation_data.action.copy()
                obj.animation_data.action_slot=obj.animation_data.action.slots[0]
        D['visible_tree'](a['root'],start,end)
        # Unlink superseded objects only from this scene, retaining v001 on disk.
        for ob in [oldroot,*oldroot.children_recursive]:
            for col in list(ob.users_collection):
                if col in list(s.collection.children):col.objects.unlink(ob)
        sh=bpy.data.objects['A '+new+' / ground shadow'];sh.hide_render=True;sh.hide_viewport=True
        a['root']['Construction correction']='Source proportions preserved: no horizontal head-growth warp across raised forearm.'

def profile_eye():
    prefix='A Repair keeper left / '
    face=bpy.data.objects[prefix+'FACE']
    # A true profile has one visible eye. The far eye is occluded by the nose.
    for name in ('eye 0','brow control 0','mouth control'):
        root=bpy.data.objects[prefix+name]
        for ob in [root,*root.children_recursive]:
            if ob.animation_data:
                for fc in R['curves'](ob):
                    if fc.data_path in ('hide_render','hide_viewport'):fc.mute=True
            ob.hide_render=True;ob.hide_viewport=True
    cfg=R['CFG']['KeeperLeft'];unit=6/cfg['body_height']*1.35
    neck=Vector(cfg['joints']['neck']);head=Vector(cfg['joints']['head'])
    # Same coordinate conversion as face_art, including its rest orientation.
    delta=Vector(((head.x-neck.x),-(head.y-neck.y)))
    theta=math.atan2(-delta.x,delta.y)
    def local(x,y):
        v=Vector(((x-neck.x)*unit,(neck.y-y)*unit))
        return (v.x*math.cos(-theta)-v.y*math.sin(-theta),v.x*math.sin(-theta)+v.y*math.cos(-theta))
    eye=bpy.data.objects[prefix+'eye 1'];eye.location=(*local(430,119),.024)
    eye.animation_data_clear();eye.rotation_euler.z=-theta+.07
    # Almond silhouette points toward the nose, following the profile's brow plane.
    for label,inflate in [('sclera',1),('eye rim',1.08)]:
        ob=bpy.data.objects[prefix+label+' 1'];n=len(ob.data.vertices)
        for i,v in enumerate(ob.data.vertices):
            t=math.tau*i/n;v.co.x=math.cos(t)*20*unit*inflate
            v.co.y=math.sin(t)*9*unit*inflate*(.72+.28*math.sin(t)**2)
    gaze=bpy.data.objects[prefix+'gaze 1'];gaze.animation_data_clear()
    gaze.location=(-7*unit,0,.014);gaze.scale=(.68,.72,1)
    brow=bpy.data.objects[prefix+'brow control 1'];brow.animation_data_clear()
    brow.location=(*local(430,98),.04);brow.rotation_euler.z=-theta+.06;brow.scale=(.85,.7,1)
    face['View check']='Single near profile eye; far eye occluded; pupil directed toward post; source mouth preserved.'

def check():
    report={}
    for tag in ('Fixed Rashford temple','Fixed Rashford turn','Fixed Rashford front'):
        skin=bpy.data.objects['A '+tag+' / continuous artwork']
        # Source grid spacing stays affine through the arm, including neck height.
        for j in range(9,42):
            a,b,c=[skin.data.vertices[k*73+60].co for k in (j-1,j,j+1)]
            assert ((b-a)-(c-b)).length<1e-5,(tag,j)
        assert all(abs(sum(g.weight for g in v.groups)-1)<1e-5 for v in skin.data.vertices)
        report[tag]='Uniform source mapping through raised arm; normalized binding.'
    s.frame_set(210)
    assert bpy.data.objects['A Repair keeper left / sclera 0'].hide_render
    assert not bpy.data.objects['A Repair keeper left / sclera 1'].hide_render
    report['profile']='One visible eye; final eye shape/gaze requires rendered review.'
    (OUT/'construction-checks.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

def apply():
    assert 'A Fixed Rashford front / ROOT' not in bpy.data.objects
    replace_raised_views();profile_eye();report=check()
    for ar in bpy.context.screen.areas:
        if ar.type=='VIEW_3D':ar.spaces.active.region_3d.view_perspective='CAMERA'
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'rashford-repair-v002.blend'))
    return report
