import bpy,json,hashlib,sys
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parents[1];version=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'v001';O=R/('artifacts/chase-'+version);s=bpy.data.scenes['S002_CP_chase_'+version];bpy.context.window.scene=s
rows=json.loads((O/'motion.json').read_text());meta=json.loads((O/'poses.json').read_text());byframe={f:[r for r in rows if r['frame']==f] for f in range(1,193)};last={};maxstep=0.;maxerr=0.;worst_bound=[1.,0.,1.,0.]
for f in range(1,193):
 s.frame_set(f);bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get()
 for row in byframe[f]:
  name=row['actor'];root=next(o for o in s.objects if o.name.split('.')[0]=='CP / '+name+' travel');active=[o for o in root.children if not o.hide_render];assert len(active)==1
  ob=active[0];p=world_to_camera_view(s,s.camera,root.matrix_world.translation);key=(name,f<=120)
  if key in last:maxstep=max(maxstep,abs(p.x-last[key])*1280)
  last[key]=p.x
  ev=ob.evaluated_get(dep);mesh=ev.to_mesh();basis=ob.data.shape_keys.key_blocks['Basis'].data
  for v in mesh.vertices:
   pt=world_to_camera_view(s,s.camera,ob.matrix_world@v.co);worst_bound=[min(worst_bound[0],pt.x),max(worst_bound[1],pt.x),min(worst_bound[2],pt.y),max(worst_bound[3],pt.y)]
  if row['contact']:
   fx,fz=meta[name]['feet'][row['pose']];dx,dz=row['correction'];assert abs(root.location.x+fx+dx-row['plant_x'])<1e-5;assert abs(root.location.z+fz+dz-.025)<1e-5
   i=min(range(len(basis)),key=lambda i:abs(basis[i].co.z-fz));v=mesh.vertices[i].co;maxerr=max(maxerr,abs(v.x-basis[i].co.x-dx),abs(v.z-basis[i].co.z-dz))
  ev.to_mesh_clear()
assert maxstep<.01,maxstep
assert maxerr<1e-5,maxerr
assert worst_bound[0]>0 and worst_bound[1]<1 and worst_bound[2]>0 and worst_bound[3]<1,worst_bound
prov=json.loads((O/'provenance.json').read_text());assert hashlib.sha256((R/'script-v003.md').read_bytes()).hexdigest()==prov['script_sha256']
report={'frames':192,'actors_in_sprint_shot':4,'actors_in_pep_cutaway':1,'cut_frame':121,'maximum_horizontal_registration_step_pixels':maxstep,'maximum_evaluated_support_error':maxerr,'full_body_mesh_bounds_normalized':worst_bound,'script_unchanged':True,'silence':'intentional motion review','creative_status':'pending user review; numerical checks do not certify likeness or comedy'}
(O/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
for f in [13,121]:
 s.frame_set(f);s.render.image_settings.file_format='PNG';s.render.filepath=str(O/f'preview-{f:03}.png');bpy.ops.render.render(write_still=True)
