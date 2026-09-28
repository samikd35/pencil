"""Actual evaluated scene checks, independent of encoded cadence checks."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v001/CP03_pep';s=bpy.data.scenes['S002_CP03_pep_body_v001'];bpy.context.window.scene=s
rows=json.loads((O/'motion.json').read_text());poses=json.loads((O/'poses.json').read_text());root=next(o for o in s.objects if 'Pep travel' in o.name);screen=[];camera=[];error=0.;bounds=[1,0,1,0];minimum_z=1
for r in rows:
 s.frame_set(r['frame']);bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get();active=[o for o in root.children if not o.hide_render];assert root['pose_index']==r['pose'],(r['frame'],root['pose_index'],r['pose']);assert len(active)==1;ob=active[0];ev=ob.evaluated_get(dep);me=ev.to_mesh();basis=ob.data.shape_keys.key_blocks['Basis'].data;fx,fz=poses[r['pose']]['foot_local'];dx,dz=r['correction']
 for b,v in zip(basis,me.vertices):
  if b.co.z<=fz+.1:
   candidate=max(abs((v.co.x-b.co.x)-dx),abs((v.co.z-b.co.z)-dz))
   if candidate>error:
    error=candidate;worst=dict(frame=r['frame'],pose=r['pose'],object=ob.name,dx=dx,dz=dz,actual=[v.co.x-b.co.x,v.co.z-b.co.z],values=[k.value for k in ob.data.shape_keys.key_blocks])
  pt=world_to_camera_view(s,s.camera,ob.matrix_world@v.co);bounds=[min(bounds[0],pt.x),max(bounds[1],pt.x),min(bounds[2],pt.y),max(bounds[3],pt.y)]
 ev.to_mesh_clear();pt=world_to_camera_view(s,s.camera,root.matrix_world.translation);screen.append(pt.x*1280);camera.append(s.camera.location.x)
assert error<1e-5,(error,worst)
assert max(screen)-min(screen)<.01
assert max(abs((b-a)-1.14/24) for a,b in zip(camera,camera[1:]))<1e-5
assert bounds[0]>0 and bounds[1]<1 and bounds[2]>0 and bounds[3]<1,bounds
report=dict(frames=96,evaluated_lower_support_error=error,horizontal_registration_range_pixels=max(screen)-min(screen),camera_uniform_travel=True,full_pose_bounds=bounds,limitations='Checks verify deformation and tracking implementation, not anatomical leg-role correctness, normal-speed gait appeal or mouth acting.')
(O/'native-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
