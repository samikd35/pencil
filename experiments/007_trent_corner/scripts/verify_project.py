"""Check real boot contacts, planted feet, continuous travel, freezes and native events."""
from pathlib import Path
import os
import bpy, json, math, hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts'/os.environ.get('PENCIL_REVISION','film-v001')
bpy.ops.wm.open_mainfile(filepath=str(OUT/'trent-corner.blend'));s=bpy.context.scene
plan=json.loads((ROOT/'production.json').read_text());build=json.loads((OUT/'build-checks.json').read_text())
assert (s.frame_start,s.frame_end,s.render.fps,s.render.fps_base)==(1,864,24,1)
source=ROOT.parent/'001_heavy_box/artifacts/finish-v002/character-and-effects.blend'
assert hashlib.sha256(source.read_bytes()).hexdigest()==build['source_sha256']
def at(t):s.frame_set(round(t*24)+1);bpy.context.view_layer.update()
def gap(pts,p):
    ds=[]
    for a,b in zip(pts,pts[1:]+pts[:1]):
        dx,dy=b[0]-a[0],b[1]-a[1];u=min(1,max(0,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy)));ds.append(math.hypot(p[0]-a[0]-u*dx,p[1]-a[1]-u*dy))
    return min(ds)
corner=build['contacts']['corner']
assert corner[1] < -1.041-.444*corner[0]  # Ball is inside the field side of the endline.
assert math.dist(corner,(3.05,-1.041-.444*3.05)) < .47
contacts=[]
for t,name,scale in [(15,'Trent',.48),(16,'Origi',.5),(24.5,'Trent',.48),(26,'Origi',.5)]:
    at(t);boot=bpy.data.objects[name+' / Shoe_near'];pts=[(boot.matrix_world@v.co)[:2] for v in boot.data.vertices];ball=bpy.data.objects['Match ball / continuous'].location[:2]
    d=gap(pts,ball)-.12-.0205*scale
    assert abs(d)<.003,(t,d)
    contacts.append({'seconds':t,'player':name,'surface_gap':d})
# A planted boot must remain stationary during the kick, across successive authored frames.
for name,a,b in [('Trent',14.6,15.8),('Origi',15.35,16.7)]:
    pts=[]
    for f in range(round(a*24)+1,round(b*24)+2):
        s.frame_set(f);pts.append(tuple(bpy.data.objects[name+' / CTRL_Foot_far'].location))
    assert max(math.dist(pts[0],p) for p in pts)<1e-5,name
at(16);keeper_start=bpy.data.objects['ter Stegen / CTRL_Head'].location.x
at(16.5);assert bpy.data.objects['ter Stegen / CTRL_Head'].location.x < keeper_start-.2
# Continuous ball travel and all seven actors remain visible through both tellings.
last=None;max_step=0
for f in range(1,865):
    s.frame_set(f);heads=[o for o in s.objects if o.name.endswith(' / Head') and not o.hide_render]
    assert len(heads)==7,(f,len(heads))
    pos=tuple(bpy.data.objects['Match ball / continuous'].location)
    if last is not None and f not in (553,697):max_step=max(max_step,math.dist(last,pos))
    last=pos
    for name in ('Trent','Origi'):
        for side in ('far','near'):
            assert all(d.driver.is_valid for d in bpy.data.objects[name+' / Arm_'+side].data.animation_data.drivers)
assert max_step<.45,max_step
for a,b in [(2,6.9),(10,13.9)]:
    at(a);p=tuple(bpy.data.objects['Trent / CTRL_Body'].location)
    at(b);assert tuple(bpy.data.objects['Trent / CTRL_Body'].location)==p
for shot in plan['shots']:
    for n,offset in shot['events'].items():assert s.timeline_markers[shot['id']+'/'+n].frame==shot['start_frame']+offset
for t,expected in [(15.9,'Score before'),(16.5,'Score after'),(23.0,'Score before'),(26.75,'Score after'),(34,'Score after')]:
    at(t);assert not bpy.data.objects[expected].hide_render
mix=OUT/'audio-v002/soundtrack.wav';assert mix.exists()
seq=s.sequence_editor_create()
for old in list(seq.strips):seq.strips.remove(old)
strip=seq.strips.new_sound('Authoritative final mix',str(mix),channel=1,frame_start=1)
strip.sound.pack();s.render.use_sequencer=False
s.frame_set(277);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'trent-corner.blend'))
result={'frames_checked':864,'contacts':contacts,'planted_boot_intervals':2,'maximum_ball_step_scene_units':max_step,'embedded_soundtrack':bool(strip.sound.packed_file),'original_source_unchanged':True,'events_match_plan':True,'limits':'Geometry and format checks do not establish viewer understanding, exact historic positioning or listening quality.'}
assert result['embedded_soundtrack'];(OUT/'project-checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PROJECT_CHECKS_PASSED')
