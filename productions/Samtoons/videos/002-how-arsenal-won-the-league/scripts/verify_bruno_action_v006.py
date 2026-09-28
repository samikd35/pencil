"""Read-only checks of the saved proof, not a creative motion approval."""
import bpy, json, hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]; O=R/'artifacts/bruno-action-v006'
s=bpy.data.scenes['S002_Bruno_action_v006'];bpy.context.window.scene=s
root=next(o for o in s.objects if o.name.startswith('A Drama Bruno / ROOT'))
controls={o.name.split('CTRL ')[1].split('.')[0]:o for o in root.children_recursive if 'CTRL ' in o.name}
records=json.loads((O/'motion.json').read_text()); previous={}; drift=0; planted_samples=0
samples=[]
for f in range(1,193):
 s.frame_set(f);bpy.context.view_layer.update()
 row={'frame':f,'controls':{k:list(o.location) for k,o in controls.items()}}
 for side in ['L','R']:
  stance=f>=13 and records[f-1]['contacts'][side]['stance']
  toe=controls[side+'toe'].matrix_world.translation.copy()
  if stance and side in previous:
   drift=max(drift,(toe-previous[side]).length);planted_samples+=1
  if stance:previous[side]=toe
  else:previous.pop(side,None)
 samples.append(row)
assert drift<.00001,(drift,planted_samples)
assert planted_samples>200
prov=json.loads((O/'provenance.json').read_text())
assert hashlib.sha256(Path(prov['source']).read_bytes()).hexdigest()==prov['source_sha256']
assert prov['surface_binding_sha256_before']==prov['surface_binding_sha256_after']
assert len(controls)==19
report={'maximum_planted_toe_drift_world_units':drift,'consecutive_planted_samples':planted_samples,'original_delivery_unchanged':True,'vertex_coordinates_weights_and_bones_preserved':True,'transparent_grid_faces_removed':prov['invisible_faces_removed'],'controls':len(controls),'creative_motion_approval':False}
(O/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
(O/'sampled-controls.json').write_text(json.dumps(samples)+'\n')
print(json.dumps(report))
