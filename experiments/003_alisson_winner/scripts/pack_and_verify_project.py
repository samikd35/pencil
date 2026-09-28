"""Embed the soundtrack, set a useful opening view and inspect the saved motion."""
from pathlib import Path
import bpy
import math
import json
import hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v001'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'alisson-winner.blend'))
s=bpy.context.scene
s.sequence_editor_clear();ed=s.sequence_editor_create()
sound=ed.strips.new_sound('Original instrumental score and football Foley',str(OUT/'audio/soundtrack.wav'),channel=1,frame_start=1)
sound.sound.filepath='//audio/soundtrack.wav';s.render.use_sequencer=False
s.sync_mode='AUDIO_SYNC'
if hasattr(s,'use_audio_scrub'):s.use_audio_scrub=True
s.frame_set(541);bpy.context.view_layer.update()

def distance_to_outline(obj,point):
    pts=[(obj.matrix_world@v.co)[:2] for v in obj.data.vertices]
    ds=[]
    for a,b in zip(pts,pts[1:]+pts[:1]):
        dx,dy=b[0]-a[0],b[1]-a[1];u=max(0,min(1,((point[0]-a[0])*dx+(point[1]-a[1])*dy)/(dx*dx+dy*dy)))
        ds.append(math.hypot(point[0]-a[0]-u*dx,point[1]-a[1]-u*dy))
    return min(ds)
ball=bpy.data.objects['Match ball - continuous trajectory']
head=bpy.data.objects['Alisson / Head']
head_gap=distance_to_outline(head,ball.location[:2])-.024*.86-.22
assert abs(head_gap)<.006,head_gap
s.frame_set(409);bpy.context.view_layer.update()
shoe=bpy.data.objects['Trent / Shoe_near']
boot_gap=distance_to_outline(shoe,ball.location[:2])-.0205*1.08-.22
assert abs(boot_gap)<.003,boot_gap
# The support boot must remain planted through the corner's release.
planted=[]
for f in range(400,419):
    s.frame_set(f);bpy.context.view_layer.update();planted.append(tuple(bpy.data.objects['Trent / CTRL_Foot_far'].matrix_world.translation))
drift=max(math.dist(p,planted[0]) for p in planted);assert drift<1e-6
positions=[]
for f in range(577,649):
    s.frame_set(f);positions.append(tuple(ball.location[:2]))
assert max(math.dist(a,b) for a,b in zip(positions,positions[1:]))<.16
source=ROOT.parent/'001_heavy_box/artifacts/finish-v002/character-and-effects.blend'
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
assert source_hash==json.loads((OUT/'build-checks.json').read_text())['source_sha256']
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False
            area.spaces.active.shading.type='MATERIAL'
s.frame_set(541)
s.render.filepath='//stills/'
s['Delivery']='40 seconds, 1080x1920, 24 fps. All visible motion and graphics are editable. Original soundtrack is embedded. Final H.264/AAC master sits beside this file.'
bpy.ops.file.pack_all()
assert sound.sound.packed_file is not None
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'alisson-winner.blend'),relative_remap=False)
(OUT/'project-checks.json').write_text(json.dumps({'header_surface_gap':head_gap,'boot_surface_gap':boot_gap,'support_foot_drift':drift,'source_unchanged_sha256':source_hash,'embedded_soundtrack':True,'timeline_frames':s.frame_end,'audio_duration':sound.frame_final_duration,'notes':'Checks compare evaluated editable artwork against ball and foot motion. Stylized reconstruction, not an exact match-footage tracing; creative acceptance remains with the user.'},indent=2)+'\n')
assert sound.frame_final_duration==960
print('PACKED_PROJECT_VERIFIED',flush=True)
