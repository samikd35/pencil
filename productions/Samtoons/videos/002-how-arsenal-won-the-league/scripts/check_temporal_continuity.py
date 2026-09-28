"""Native screen-space regression and contact check. Pass -- v002 to reproduce old failure."""
import bpy,json,sys,statistics,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parents[1];version=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'v003';O=R/('artifacts/pose-action-'+version)
s=bpy.data.scenes['S002_whole_pose_action_'+version];bpy.context.window.scene=s
actor=next(o for o in s.objects if o.name.startswith('Bruno / whole-body pose and travel'));meta=json.loads((R/'artifacts/pose-action-v003/poses.json').read_text());rows=json.loads((O/'motion.json').read_text());samples=[];max_contact_error=0.;max_vertex_correction=0.
for row in rows:
 f=row['frame'];s.frame_set(f);bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get();visible=[o for o in actor.children if o.type=='MESH' and not o.hide_render];assert len(visible)==1
 ob=visible[0];key=row['pose'];nx,nz=meta[key]['neck'];p=world_to_camera_view(s,s.camera,actor.matrix_world@Vector((nx,0,nz)));b=world_to_camera_view(s,s.camera,Vector((0,0,1)))
 samples.append({'frame':f,'neck_screen_x':p.x*1280,'background_screen_x':b.x*1280})
 if version=='v003':
  evalmesh=ob.evaluated_get(dep).to_mesh();basis=ob.data.shape_keys.key_blocks['Basis'].data
  # Contact is in fully compensated bottom zone. Evaluate an actual lowest vertex
  # and compare to its expected unchanged world placement, not only a control key.
  if row['contact_world']:
   fx,fz=meta[key]['foot'];idx=min(range(len(basis)),key=lambda i:(basis[i].co.z-fz)**2+(basis[i].co.x-fx)**2);v=evalmesh.vertices[idx].co
   expected_x=basis[idx].co.x+actor.location.x+row['contact_compensation_x'];expected_z=basis[idx].co.z+actor.location.z
   world=ob.matrix_world@v;err=max(abs(world.x-expected_x),abs(world.z-expected_z));max_contact_error=max(max_contact_error,err)
   assert abs(row['x']+fx+row['contact_compensation_x']-row['contact_world'][0])<1e-5
  for bv,ev in zip(basis,evalmesh.vertices):
   max_vertex_correction=max(max_vertex_correction,abs(bv.co.x-ev.co.x));assert abs(bv.co.z-ev.co.z)<1e-6
   if bv.co.z>=nz-.2:assert abs(bv.co.x-ev.co.x)<1e-6,'Head/chest deformed'
  ob.evaluated_get(dep).to_mesh_clear()
run=samples[28:100];neck_steps=[b['neck_screen_x']-a['neck_screen_x'] for a,b in zip(run,run[1:])];bg_steps=[b['background_screen_x']-a['background_screen_x'] for a,b in zip(run,run[1:])]
prov=json.loads((O/'provenance.json').read_text());assert hashlib.sha256(Path(prov['source_blend']).read_bytes()).hexdigest()==prov['source_sha256']
report={'version':version,'frames':len(samples),'steady_run_frames':[29,100],'neck_screen_step_range_pixels':[min(neck_steps),max(neck_steps)],'background_step_range_pixels':[min(bg_steps),max(bg_steps)],'background_step_stddev_pixels':statistics.pstdev(bg_steps),'maximum_evaluated_contact_error_world_units':max_contact_error if version=='v003' else None,'maximum_vertex_horizontal_correction':max_vertex_correction,'original_delivery_hash_unchanged':True,'creative_status':'temporal revision pending playback review'}
(O/'temporal-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
assert max_contact_error<1e-5
assert max(abs(x) for x in neck_steps)<.1,'REPRODUCED: unintended registered body oscillation during constant-speed run'
assert statistics.pstdev(bg_steps)<.1,'REPRODUCED: tracking camera speed pulses during steady run'
