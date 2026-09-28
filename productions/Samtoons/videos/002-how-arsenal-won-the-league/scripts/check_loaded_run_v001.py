"""Reopen-and-evaluate check for CP01; numerical checks do not judge gait appeal."""
import bpy,json
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v002/CP01'
s=bpy.data.scenes['S002_CP01_loaded_run_v001'];bpy.context.window.scene=s
rows=json.loads((O/'motion.json').read_text());meta=json.loads((O/'poses.json').read_text())
roots={n:next(o for o in s.objects if o.name.startswith('CP / '+n+' travel')) for n in meta}
screen={n:[] for n in roots};error=0.;bounds=[1,0,1,0]
for f in range(1,217):
 s.frame_set(f);bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get()
 for row in (r for r in rows if r['frame']==f):
  name=row['actor'];root=roots[name];active=[o for o in root.children if not o.hide_render]
  assert len(active)==1 and root['pose_index']==row['pose']
  ob=active[0];ev=ob.evaluated_get(dep);mesh=ev.to_mesh();basis=ob.data.shape_keys.key_blocks['Basis'].data
  fz=meta[name]['poses'][row['pose']]['foot_local'][1];dx,dz=row['correction']
  for b,v in zip(basis,mesh.vertices):
   if b.co.z<=fz+.1:error=max(error,abs(v.co.x-b.co.x-dx),abs(v.co.z-b.co.z-dz))
  for i in [0,24,40*25,41*25-1]:
   pt=world_to_camera_view(s,s.camera,ob.matrix_world@mesh.vertices[i].co)
   bounds=[min(bounds[0],pt.x),max(bounds[1],pt.x),min(bounds[2],pt.y),max(bounds[3],pt.y)]
  ev.to_mesh_clear();pt=world_to_camera_view(s,s.camera,root.matrix_world.translation);screen[name].append(pt.x*1280)
assert error<1e-5,error
ranges={n:max(v)-min(v) for n,v in screen.items()};assert max(ranges.values())<.01,ranges
assert 0<bounds[0]<bounds[1]<1 and 0<bounds[2]<bounds[3]<1,bounds
(O/'evaluated-checks.json').write_text(json.dumps(dict(frames=216,actors=4,actual_mesh_support_error=error,horizontal_registration_ranges_px=ranges,pose_surface_screen_bounds=bounds,limitations='No automated judgment of pose anatomy, natural timing, expression or audible fit.'),indent=2))
print('All216frames: evaluated deformation, selectors, independent camera and full-pose framing pass.')
