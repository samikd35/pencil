"""Verify staging coverage, visibility and contact before presenting the checkpoint."""
from pathlib import Path
import bpy,json,math,os,sys,hashlib
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts'/os.environ.get('PENCIL_REVISION','film-v003')
bpy.ops.wm.open_mainfile(filepath=str(OUT/'trent-corner-advanced.blend'));s=bpy.context.scene
plan=json.loads((OUT/'production.json' if (OUT/'production.json').exists() else ROOT/'production.json').read_text())
cast=json.loads((ROOT/plan.get('staging','staging-v004.json')).read_text())['cast'];s.frame_set(403);bpy.context.view_layer.update()
assert sum(a['team']=='Liverpool' for a in cast)==7
assert sum(a['team']=='Barcelona' for a in cast)==8
visible=[]
for spec in cast:
    name=spec['id'];body=bpy.data.objects[name+' / Jersey'];p=body.matrix_world@Vector((0,-.012,.3));uv=world_to_camera_view(s,s.camera,p)
    assert .04<uv.x<.96 and .1<uv.y<.85,(name,tuple(uv))
    direction=p-s.camera.location;hit,where,normal,index,obj,matrix=s.ray_cast(bpy.context.evaluated_depsgraph_get(),s.camera.location,direction.normalized(),distance=direction.length+.02)
    visible.append({'player':name,'team':spec['team'],'torso_frame_xy':[uv.x,uv.y],'first_ray_hit':obj.name if hit else None})
# Camera rays demonstrate the newly added red teammates are not merely present behind defenders.
assert all(v['first_ray_hit'] and v['first_ray_hit'].startswith(v['player']+' /') for v in visible if v['player'].startswith('Attacker'))
contacts=[]
for f,name in [(403,'Trent'),(433,'Origi'),(633,'Trent'),(673,'Origi')]:
    s.frame_set(f);bpy.context.view_layer.update();toe=bpy.data.objects[name+' / Boot 1'].matrix_world@Vector((0,.24,0));ball=bpy.data.objects['Ball / continuous'].location
    gap=(toe-ball).length-.17;assert abs(gap)<1e-5,(f,gap);contacts.append({'frame':f,'player':name,'gap':gap})
for name,a,b in [('Trent',395,419),('Origi',419,441)]:
    points=[]
    for f in range(a,b+1):s.frame_set(f);points.append(bpy.data.objects[name+' / Boot 0'].location.copy())
    assert max((p-points[0]).length for p in points)<1e-5
for f in range(395,481):
    s.frame_set(f);uv=world_to_camera_view(s,s.camera,bpy.data.objects['Ball / continuous'].location)
    assert .04<uv.x<.96 and .08<uv.y<.85
report={'role_count':{'Liverpool':7,'Barcelona_including_keeper':8},'staging':visible,'contacts':contacts,'added_teammates_visible_by_camera_ray':True,'interpretation':'Representative corner arrangement, not exact tracked historic positions. Frame visibility and geometry checks remain separate from user creative review.'}
if '--delivery' in sys.argv:
    assert (s.frame_start,s.frame_end,s.render.fps,s.render.fps_base)==(1,912,24,1)
    assert (s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage)==(1080,1920,100)
    last=None;maxstep=0
    for f in range(1,913):
        s.frame_set(f)
        for actor in cast:
            assert sum(not bpy.data.objects[actor['id']+' / Head '+str(i)].hide_render for i in range(3))==1,(f,actor['id'])
        p=bpy.data.objects['Ball / continuous'].location.copy()
        if last is not None and f!=577:maxstep=max(maxstep,(p-last).length)
        last=p
        if 395<=f<=480 or 577<=f<=744:
            uv=world_to_camera_view(s,s.camera,p);assert .04<uv.x<.96 and .08<uv.y<.85,(f,tuple(uv))
    assert maxstep<.4,maxstep
    for shot in plan['shots']:
        for event,offset in shot['events'].items():assert s.timeline_markers[shot['id']+'/'+event].frame==shot['start_frame']+offset
    for f,expected in [(403,'Score before'),(448,'Score after'),(577,'Score before'),(693,'Score after'),(889,'Score after')]:
        s.frame_set(f);assert not bpy.data.objects[expected].hide_render
    for f,expected in [(49,True),(97,False),(145,False),(403,False)]:
        s.frame_set(f);assert (not bpy.data.objects['Fiction / tiny shoulder pillow'].hide_render)==expected
    resolved=json.loads((OUT/'audio-v001/resolved-cues.json').read_text())
    checks=json.loads((OUT/'audio-v001/checks.json').read_text())
    assert resolved['samples']==1824000
    assert resolved['plan_sha256']==hashlib.sha256((ROOT/'production.json').read_bytes()).hexdigest()
    assert all(c['start_sample']+c['onset_samples']==c['event_sample'] for c in resolved['cues'])
    assert all(o['decoded'] and o['finite_samples'] and o['samples']==1824000 for o in checks['outputs'])
    rejected=set(plan['rejected_audio'].values())
    assert not any(asset['sha256'] in rejected for asset in plan['assets'].values())
    assert not any(c['asset']=='crowd-bed' for c in plan['cues']), 'Selected A has no continuous crowd bed'
    seq=s.sequence_editor_create()
    for old in list(seq.strips):seq.strips.remove(old)
    strip=seq.strips.new_sound('Selected A / authoritative soundtrack',str(OUT/'soundtrack.wav'),channel=1,frame_start=1)
    strip.sound.pack();s.render.use_sequencer=False
    s.frame_set(421);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'trent-corner-advanced.blend'))
    assert strip.sound.packed_file and all(i.packed_file for i in bpy.data.images if i.source=='FILE')
    report.update(frames_checked=912,maximum_ball_step=maxstep,all_actor_expressions_valid=True,events_match_plan=True,
                  selected_audio='A — sparse sound',rejected_audio_absent=True,packed_images_and_soundtrack=True)
(OUT/'staging-checks.json').write_text(json.dumps(report,indent=2)+'\n');print('STAGING_CHECKS_PASSED')
