"""Check evaluated pose visibility and native prop contacts in the authored batch."""
import bpy,json,math
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v004';batch=json.loads((O/'batch.json').read_text());samples=0;roots_count=0
for sid in batch['shots']:
 s=bpy.data.scenes['S002_fullmotion_'+sid];bpy.context.window.scene=s
 roots=[o for o in s.objects if 'cells' in o];roots_count+=len(roots)
 for frame in range(1,s.frame_end+1):
  s.frame_set(frame);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
  for root in roots:
   cells=json.loads(root['cells']);index=int(root.evaluated_get(deps)['pose']);assert 0<=index<len(cells),(sid,frame,root.name,index)
   children=[o for o in root.children if o.type=='MESH'];visible=[o for o in children if not o.evaluated_get(deps).hide_render]
   assert len(visible)==1,(sid,frame,root.name,len(visible));samples+=1
 for o in s.objects:
  if o.type=='EMPTY' and o.name.endswith('bottle delivery truck'):
   for frame in [1,s.frame_end//2,s.frame_end]:
    s.frame_set(frame);assert abs(o.location.y-2.1-.55+3.5)<1e-5
 s.frame_set(1)
assert samples>1000
(O/'pose-checks.json').write_text(json.dumps({'native_scenes':len(batch['shots']),'actors':roots_count,'evaluated_actor_frames':samples,'one_complete_pose_visible_per_actor_frame':True,'truck_ground_contact':True,'creative_quality':'Not established by technical checks'},indent=2))
print('NATIVE_POSE_CHECKS_PASSED',samples,flush=True)
