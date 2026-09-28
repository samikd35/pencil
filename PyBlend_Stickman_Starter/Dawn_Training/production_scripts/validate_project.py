"""Saved-file checks for editability, shot coverage, rig motion and packed assets."""
from pathlib import Path
import bpy,json,math,struct,hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'artifacts/dawn_training'
s=bpy.data.scenes['DT_03_DAWN_TRAINING'];bpy.context.window.scene=s
checks={}
assert s.frame_start==1 and s.frame_end==720 and s.render.fps==24
assert (s.render.resolution_x,s.render.resolution_y)==(1920,1080)
checks['timeline']={'frames':720,'fps':24,'seconds':30,'resolution':[1920,1080]}
markers=sorted([(m.frame,m.name,m.camera.name if m.camera else None) for m in s.timeline_markers])
assert [m[0] for m in markers]==[1,121,241,361,481,601]
assert all(m[2] for m in markers);checks['camera_cuts']=markers
assets={}
for name in ['FRONT','BACK','FOCUS','RUN','CROUCH','POWER','SIT']:
 o=bpy.data.objects['DT_GP_'+name];rig=bpy.data.objects['DT_RIG_'+name]
 assert o.type=='GREASEPENCIL' and rig.type=='ARMATURE'
 count=0
 for l in o.data.layers:
  assert l.parent==rig,(name,l.name,'unparented')
  assert l.parent_bone in rig.pose.bones,(name,l.name,'missing bone')
  for f in l.frames:
   for stroke in f.drawing.strokes:
    count+=1
    for p in stroke.points:assert all(math.isfinite(v) for v in p.position)
 assert count>50
 assets[name]={'layers':len(o.data.layers),'bones':len(rig.pose.bones),'editable_curves':count}
checks['native_grease_pencil']=assets
coverage={}
for f,expected in [(1,'BACK'),(120,'BACK'),(121,'FOCUS'),(240,'FOCUS'),(241,'RUN'),(360,'RUN'),(361,'POWER'),(480,'POWER'),(481,'RUN'),(600,'RUN'),(601,'CROUCH'),(648,'CROUCH'),(649,'FRONT'),(720,'FRONT')]:
 s.frame_set(f)
 visible=[name for name in assets if not bpy.data.objects['DT_GP_'+name].hide_render]
 assert visible==[expected],(f,visible,expected)
 coverage[f]=visible
checks['character_exposure_boundaries']=coverage
# Run root travel and changing limb rotations are independent facts.
r=bpy.data.objects['DT_RIG_RUN'];samples={}
for f in [241,245,249,253,357]:
 s.frame_set(f);samples[f]={'root':list(r.location),'leg_z':r.pose.bones['pants.L'].rotation_euler.z,'arm_z':r.pose.bones['upper_arm.R'].rotation_euler.z}
assert samples[357]['root'][0]-samples[241]['root'][0]>14
assert max(x['leg_z'] for x in samples.values())-min(x['leg_z'] for x in samples.values())>.5
checks['run_motion']=samples
# Native drivers must evaluate the actual visible eye layers.
focus=bpy.data.objects['DT_RIG_FOCUS'];art=bpy.data.objects['DT_GP_FOCUS'];face={}
for f in [121,193,219]:
 s.frame_set(f);bpy.context.view_layer.update()
 vals={name:art.data.layers[name].opacity for name in ['eyes.L','eyes.R','Closed_eyes.L','Closed_eyes.R']}
 face[f]={'blink':focus['Blink'],'layers':vals}
assert face[193]['layers']['eyes.L']<.01 and face[193]['layers']['Closed_eyes.L']>.99
assert face[219]['layers']['eyes.L']>.99
checks['blink_driver']=face
# The neutral studio is editable without carrying film root placement or actions.
studio=bpy.data.scenes['DT_01_CHARACTER_STUDIO'];bpy.context.window.scene=studio;studio.frame_set(1)
r=bpy.data.objects['DT_STUDIO_RIG_FRONT'];o=bpy.data.objects['DT_STUDIO_GP_FRONT']
assert not r.animation_data or r.animation_data.action is None
assert r.location.length<.00001 and not o.hide_render
checks['independent_neutral_studio']=True
reference_images=[im for im in bpy.data.images if im.name in ['im-1.png','im_2.png','im_3.png','im_4.png','im_5.png']]
assert len(reference_images)==5 and all(im.packed_file for im in reference_images)
assert all(sound.packed_file for sound in bpy.data.sounds)
checks['packed_references']=len(reference_images);checks['packed_sounds']=len(bpy.data.sounds)
# All final image headers and content must be present; verify exact raster dimensions.
files=[OUT/'frames'/f'frame_{i:04}.png' for i in range(1,721)]
hashes=[]
for p in files:
 assert p.is_file() and p.stat().st_size>1000,p
 with p.open('rb') as h:header=h.read(24)
 assert header[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',header[16:24])==(1920,1080),p
 hashes.append(hashlib.sha256(p.read_bytes()).hexdigest())
assert len(set(hashes))>500
checks['rendered_frames']={'count':len(files),'unique':len(set(hashes)),'all_dimensions_valid':True}
checks['artistic_status']='Complete first cut; no user approval or platform-wide character certification claimed.'
checks['blender_version']=bpy.app.version_string;checks['build_hash']=bpy.app.build_hash.decode()
(OUT/'validation.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks),flush=True)
