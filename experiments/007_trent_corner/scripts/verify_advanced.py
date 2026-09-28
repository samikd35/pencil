"""Check authored contacts, continuous action, framing, cue sync and packed assets."""
from pathlib import Path
import os
import bpy,json,math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts'/os.environ.get('PENCIL_REVISION','film-v002')
bpy.ops.wm.open_mainfile(filepath=str(OUT/'trent-corner-advanced.blend'));s=bpy.context.scene
plan=json.loads((ROOT/'production.json').read_text())
assert (s.frame_start,s.frame_end,s.render.fps,s.render.fps_base)==(1,912,24,1)
assert (s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage)==(1080,1920,100)
contacts=[]
for f,name in [(403,'Trent'),(433,'Origi'),(633,'Trent'),(673,'Origi')]:
    s.frame_set(f);bpy.context.view_layer.update()
    boot=bpy.data.objects[name+' / Boot 1'];toe=boot.matrix_world@Vector((0,.24,0));ball=bpy.data.objects['Ball / continuous'].location
    gap=(toe-ball).length-.17;assert abs(gap)<1e-5,(f,gap)
    contacts.append({'frame':f,'player':name,'toe_ball_surface_gap_scene_units':gap})
for name,a,b in [('Trent',395,419),('Origi',419,441)]:
    pts=[]
    for f in range(a,b+1):
        s.frame_set(f);pts.append(tuple(bpy.data.objects[name+' / Boot 0'].location))
    assert max(math.dist(pts[0],p) for p in pts)<1e-5,(name,pts)
for sh in plan['shots']:
    for event,offset in sh['events'].items():assert s.timeline_markers[sh['id']+'/'+event].frame==sh['start_frame']+offset
actors=('Trent','Origi','Shaqiri','Defender A','Defender B','Defender C','Keeper')
last=None;maxstep=0;bounds=[1,0,1,0]
for f in range(1,913):
    s.frame_set(f)
    for name in actors:assert sum(not bpy.data.objects[name+' / Head '+str(i)].hide_render for i in range(3))==1,(f,name)
    p=bpy.data.objects['Ball / continuous'].location.copy()
    if last is not None and f!=577:maxstep=max(maxstep,(p-last).length)
    last=p
    if 395<=f<=480 or 577<=f<=744:
        uv=world_to_camera_view(s,s.camera,p)
        assert .04<uv.x<.96 and .08<uv.y<.85,(f,tuple(uv))
        bounds=[min(bounds[0],uv.x),max(bounds[1],uv.x),min(bounds[2],uv.y),max(bounds[3],uv.y)]
assert maxstep<.4,maxstep
for f,expected in [(403,'Score before'),(448,'Score after'),(577,'Score before'),(693,'Score after'),(889,'Score after')]:
    s.frame_set(f);assert not bpy.data.objects[expected].hide_render
for f,expected in [(49,True),(97,False),(145,False),(403,False)]:
    s.frame_set(f);assert (not bpy.data.objects['Fiction / tiny shoulder pillow'].hide_render)==expected
resolved=json.loads((OUT/'audio-v001/resolved-cues.json').read_text())
# Shared mixer checks source hashes, complete duration, and exact event-to-sample placement.
audio_checks=json.loads((OUT/'audio-v001/checks.json').read_text())
assert resolved['samples']==1824000 and len(resolved['cues'])==29
assert all(c['start_sample']+c['onset_samples']==c['event_sample'] for c in resolved['cues'])
assert all(o['decoded'] and o['finite_samples'] and o['samples']==1824000 for o in audio_checks['outputs'])
assert (OUT/'audio-v001/soundtrack.wav').is_file()
seq=s.sequence_editor_create()
for old in list(seq.strips):seq.strips.remove(old)
strip=seq.strips.new_sound('Authoritative final mix',str(OUT/'audio-v001/soundtrack.wav'),channel=1,frame_start=1);strip.sound.pack();s.render.use_sequencer=False
# Keep the observation caption clear of the foreground face.
bpy.data.objects['Open'].location.y=.29
s.frame_set(421);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'trent-corner-advanced.blend'))
assert strip.sound.packed_file
assert all(i.packed_file for i in bpy.data.images if i.source=='FILE')
result={'frames_checked':912,'contacts':contacts,'planted_support_feet_intervals':2,'maximum_ball_step_scene_units':maxstep,'ball_frame_bounds_during_action_and_replay':bounds,'events_match_plan':True,'packed_head_and_stadium_art':True,'packed_authoritative_mix':True,'limits':'Technical checks do not establish exact historical player positions, audience response or listening quality.'}
(OUT/'project-checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PROJECT_CHECKS_PASSED')
