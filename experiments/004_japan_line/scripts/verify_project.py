"""Check evaluated contacts, stationary reveal geometry and factual in/out labels."""
from pathlib import Path
import bpy, math, json, hashlib
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v001'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'japan-line.blend'));s=bpy.context.scene
def frame(n):s.frame_set(n);bpy.context.view_layer.update()
def distance(points,p):
    ds=[]
    for a,b in zip(points,points[1:]+points[:1]):
        dx,dy=b[0]-a[0],b[1]-a[1];u=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy)))
        ds.append(math.hypot(p[0]-a[0]-u*dx,p[1]-a[1]-u*dy))
    return min(ds)
ball=bpy.data.objects['Match ball'];macro=bpy.data.objects['Frozen sphere - illustrative, not measured']
frame(64);shoe=bpy.data.objects['Mitoma / Shoe_near'];pts=[(shoe.matrix_world@v.co)[:2] for v in shoe.data.vertices]
boot_gap=distance(pts,ball.location[:2])-.22-.0205;assert abs(boot_gap)<.003,boot_gap
hand_gaps=[]
for side in ('far','near'):
    ob=bpy.data.objects['Mitoma / Mitten_'+side];pts=[(ob.matrix_world@v.co)[:2] for v in ob.data.vertices];hand_gaps.append(distance(pts,ball.location[:2])-.22)
assert min(hand_gaps)>.25,hand_gaps
plant_drifts=[]
for side,frames in [('far',range(1,7)),('near',range(8,14))]:
    pts=[]
    for f in frames:frame(f);pts.append(tuple(bpy.data.objects['Mitoma / CTRL_Foot_'+side].location))
    plant_drifts.append(max(math.dist(p,pts[0]) for p in pts))
assert max(plant_drifts)<2e-5,plant_drifts
frame(610);ob=bpy.data.objects['Tanaka / Leg_near'].evaluated_get(bpy.context.evaluated_depsgraph_get());a,b=ob.data.splines[0].bezier_points;pts=[]
for i in range(1001):
    u=i/1000;v=(1-u)**3*a.co+3*(1-u)**2*u*a.handle_right+3*(1-u)*u*u*b.handle_left+u**3*b.co;pts.append((ob.matrix_world@v)[:2])
knee_gap=min(math.dist(p,ball.location[:2]) for p in pts)-.22-.026*.92
assert abs(knee_gap)<.01,knee_gap
poses=[];cameras=[];label_frames=0
for f in range(97,457):
    frame(f);t=(f-1)/24
    if t<14:poses.append(tuple(macro.location));cameras.append(tuple(s.camera.location))
    edge=macro.location.x-1000-.75
    for name,inside in [('still_in',True),('in_demo',True),('out_demo',False)]:
        if not bpy.data.objects[name].hide_render:
            assert edge<=0 if inside else edge>0,(f,name,edge);label_frames+=1
assert max(math.dist(p,poses[0]) for p in poses)<1e-6
assert math.dist(cameras[0],cameras[150])>4
frame(504);a=ball.rotation_euler.z;frame(505);assert abs(ball.rotation_euler.z-a)<1e-5
frame(565);assert not bpy.data.objects['Goal frame'].hide_render and bpy.data.objects['goal'].hide_render
for ob in s.objects:
    if ob.parent and ob.parent.name=='Screen typography':assert ob.visible_shadow is False
source=ROOT.parent/'001_heavy_box/artifacts/finish-v002/character-and-effects.blend'
source_hash=hashlib.sha256(source.read_bytes()).hexdigest();assert source_hash==json.loads((OUT/'build-checks.json').read_text())['source_sha256']
s.sequence_editor_clear();ed=s.sequence_editor_create();strip=ed.strips.new_sound('Original score and Foley',str(OUT/'audio/soundtrack.wav'),channel=1,frame_start=1)
strip.sound.filepath='//audio/soundtrack.wav';s.render.use_sequencer=False;s.sync_mode='AUDIO_SYNC';s.render.resolution_percentage=100
frame(277);bpy.ops.file.pack_all();assert strip.sound.packed_file is not None
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'japan-line.blend'),relative_remap=False)
report={'boot_surface_gap':boot_gap,'hand_clearances':hand_gaps,'sprint_plant_drifts':plant_drifts,'knee_surface_gap':knee_gap,'macro_stationary_frames':len(poses),'checked_state_label_frames':label_frames,'embedded_soundtrack':True,'frames':768,'source_unchanged_sha256':source_hash,'limits':'Geometric illustration, not measured match reconstruction. Technical checks do not establish audience comprehension or world-class quality.'}
(OUT/'project-checks.json').write_text(json.dumps(report,indent=2)+'\n');print('PROJECT_CHECKS_PASSED',json.dumps(report),flush=True)
