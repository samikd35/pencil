"""Place soles on the visible touchline surface and smooth the tracking camera."""
import bpy,json,hashlib
from pathlib import Path
R=Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/002-how-arsenal-won-the-league');src=R/'artifacts/pose-action-v001';out=R/'artifacts/pose-action-v002';name='S002_whole_pose_action_v002'
assert not out.exists() and name not in bpy.data.scenes
with bpy.data.libraries.load(str(src/'pose-action-v001.blend'),link=False) as (a,l):l.scenes=['S002_whole_pose_action_v001']
s=l.scenes[0];s.name=name;bpy.context.window.scene=s
actor=next(o for o in s.objects if o.name.startswith('Bruno / whole-body pose and travel'))
rows=json.loads((src/'motion.json').read_text());camera_x=rows[0]['x']
for row in rows:
 f=row['frame'];row['z']+=.05
 if row['contact_world']:row['contact_world'][1]=.05
 actor.location=(row['x'],-.02,row['z']);actor.keyframe_insert(data_path='location',frame=f)
 camera_x+=(row['x']-camera_x)*.35
 s.camera.location.x=camera_x;s.camera.keyframe_insert(data_path='location',frame=f)
# One exposed, keyable pose selector instead of sixteen independent visibility tracks.
pose_names=['run'+str(i) for i in range(8)]+['jump'+str(i) for i in range(8)]
actor['pose_index']=0;actor.id_properties_ui('pose_index').update(min=0,max=15,description='0-7 run; 8 ready,9 load,10 extension,11 rise,12 tuck,13 reach,14 absorb,15 recover')
for i,key in enumerate(pose_names):
 label='Bruno / '+('run' if i<8 else 'jump')+' pose '+str((i%8)+1)
 ob=next(o for o in s.objects if o.name==label or o.name.startswith(label+'.'))
 ob.animation_data_clear()
 for prop in ['hide_render','hide_viewport']:
  driver=ob.driver_add(prop).driver;driver.expression='pose != '+str(i)
  v=driver.variables.new();v.name='pose';v.type='SINGLE_PROP';v.targets[0].id=actor;v.targets[0].data_path='["pose_index"]'
for row in rows:
 actor['pose_index']=pose_names.index(row['pose']);actor.keyframe_insert(data_path='["pose_index"]',frame=row['frame'])
 if row['frame']==138:row['phase']='landing_contact';row['contact_world']=rows[138]['contact_world']
for layer in actor.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    if fc.data_path=='["pose_index"]':
     for kp in fc.keyframe_points:kp.interpolation='CONSTANT'
s['Events']=json.dumps({'run_start':13,'gather':109,'load':117,'last_grounded_takeoff':122,'first_airborne':123,'first_landing_contact':138,'compression':141,'recovered':153})

s['Review status']='Whole-pose blocking candidate; native timing/contact/flight controls. Pending normal-speed review.'
s.frame_set(19)
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_overlays=False
out.mkdir(parents=True)
for file in ['poses.json','provenance.json']:(out/file).write_bytes((src/file).read_bytes())
(out/'motion.json').write_text(json.dumps(rows,indent=2)+'\n')
bpy.data.libraries.write(str(out/'pose-action-v002.blend'),{s},fake_user=True)
result={'scene':name,'file':str(out/'pose-action-v002.blend')}
