"""Read-only native/encoded jitter diagnostic. Run in background Blender."""
import bpy,json,subprocess,statistics
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
s=bpy.data.scenes['S002_whole_pose_action_v002'];bpy.context.window.scene=s
actor=next(o for o in s.objects if o.name.startswith('Bruno / whole-body pose and travel'))
rows=[]
for f in range(1,193):
 s.frame_set(f);bpy.context.view_layer.update()
 p=world_to_camera_view(s,s.camera,actor.matrix_world.translation)
 b=world_to_camera_view(s,s.camera,Vector((0,0,1)))
 rows.append(dict(frame=f,pose=int(actor['pose_index']),root_x=float(actor.location.x),root_z=float(actor.location.z),camera_x=float(s.camera.location.x),actor_screen_x=p.x*1280,background_screen_x=b.x*1280))
for i in range(1,len(rows)):
 for k in ['root_x','camera_x','actor_screen_x','background_screen_x']:
  rows[i]['delta_'+k]=rows[i][k]-rows[i-1][k]
# Steady run away from starting and braking; screen-space probes use actual camera.
run=rows[28:100]
def span(k):return [min(r[k] for r in run),max(r[k] for r in run)]
pts=json.loads(subprocess.check_output(['/opt/homebrew/bin/ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(R/'artifacts/pose-action-v002/pose-action-v002.mp4')]))['frames']
t=[float(x['best_effort_timestamp_time']) for x in pts];dt=[b-a for a,b in zip(t,t[1:])]
# Intervention without changing the file: frozen camera removes background motion,
# but the same measured root positions retain stop/go. Constant-speed camera
# removes background speed ripple; it cannot remove character path discontinuities.
scale=1280/s.camera.data.ortho_scale
world_steps=[r['delta_root_x']*scale for r in run]
mean_step=statistics.mean(world_steps)
report={
 'native_sample_count':len(rows),'encoded_sample_count':len(t),'encoded_frame_interval_seconds':[min(dt),max(dt)],
 'steady_run_frames':[29,100],
 'root_world_step_range':span('delta_root_x'),
 'camera_pixel_step_range':[x*scale for x in span('delta_camera_x')],
 'actor_screen_step_range_pixels':span('delta_actor_screen_x'),
 'background_screen_step_range_pixels':span('delta_background_screen_x'),
 'camera_direction_reversals_during_full_clip':[r['frame'] for r in rows[1:] if r['delta_camera_x'] < -1e-5],
 'frozen_camera_counterfactual':{'background_step_pixels':0,'actor_step_range_pixels':[min(world_steps),max(world_steps)]},
 'constant_speed_camera_counterfactual':{'background_step_pixels':-mean_step,'actor_step_range_pixels':[min(world_steps)-mean_step,max(world_steps)-mean_step]},
 'example_frames':rows[28:37],
 'diagnosis':'Root translation inherits held pose/contact resets; camera chases that discontinuous root. Smooth filtering propagates speed pulses, while character/background update at conflicting cadence. Pose drawings also switch without in-between silhouettes; residual drawing registration is not quantified by these root probes.'}
(O/'audit.json').write_text(json.dumps(report,indent=2)+'\n');(O/'frames.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert len(t)==192 and max(abs(x-1/24) for x in dt)<2e-6
assert max(abs(r['delta_root_x']) for r in run)<.35,'REPRODUCED: root advances abruptly by >80 px/frame during steady run'
