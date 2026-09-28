"""Evaluated native checks; neither these nor stills establish motion acceptance."""
import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'artifacts/pose-action-v002'
s=bpy.data.scenes['S002_whole_pose_action_v002'];bpy.context.window.scene=s
actor=next(o for o in s.objects if o.name.startswith('Bruno / whole-body pose and travel'))
poses=[o for o in actor.children if o.type=='MESH'];assert len(poses)==16
rows=json.loads((O/'motion.json').read_text());meta=json.loads((O/'poses.json').read_text());max_error=0
for row in rows:
 s.frame_set(row['frame']);bpy.context.view_layer.update();visible=[o for o in poses if not o.hide_render]
 assert len(visible)==1,(row['frame'],[o.name for o in visible])
 kind='run' if row['pose'].startswith('run') else 'jump'
 expected=f"Bruno / {kind} pose {int(row['pose'][len(kind):])+1}"
 assert visible[0].name.split('.')[0]==expected,(row['frame'],visible[0].name,expected)
 if row['contact_world']:
  fx,fz=meta[row['pose']]['foot'];actual=(actor.location.x+fx,actor.location.z+fz)
  max_error=max(max_error,*(abs(a-b) for a,b in zip(actual,row['contact_world'])))
assert max_error<1e-5,max_error
for i in range(123,137):
 a,b,c=rows[i-2],rows[i-1],rows[i]
 assert abs((c['z']-2*b['z']+a['z'])*24**2+9.81)<1e-5
prov=json.loads((O/'provenance.json').read_text());assert hashlib.sha256(Path(prov['source_blend']).read_bytes()).hexdigest()==prov['source_sha256']
report={'frames':192,'visible_complete_poses_per_frame':1,'maximum_contact_anchor_error_world_units':max_error,'jump_proxy_acceleration_world_units_per_second_squared':-9.81,'gravity_applies_to':'uniform-area silhouette mass proxy; not anatomical COM','original_delivery_unchanged':True,'pose_selector_keyed':True,'creative_review':'pending; no normal-speed acceptance inferred'}
(O/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
s.frame_set(19);s.render.image_settings.file_format='PNG';s.render.filepath=str(O/'selector-check-frame-019.png');bpy.ops.render.render(write_still=True)
print(json.dumps(report))
