"""Native checks for shared geography and the scope-limited seated rigs."""
import bpy,json
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v005'
room=bpy.data.collections['S002 / Narrator room / shared v005'];scenes=[s for s in bpy.data.scenes if s.name.startswith('S002_v005_')]
assert len(scenes)==7 and all(room in list(s.collection.children) for s in scenes)
dark=bpy.data.scenes['S002_v005_N04_dark'];reveal=bpy.data.scenes['S002_v005_N04_reveal']
assert all(abs(dark.camera.matrix_world[i][j]-reveal.camera.matrix_world[i][j])<1e-6 for i in range(4) for j in range(4))
links={'torso':('hip','neck'),'head':('neck','head'),'L upper arm':('Ls','Le'),'L forearm':('Le','Lw'),'L hand':('Lw','Lf'),'R upper arm':('Rs','Re'),'R forearm':('Re','Rw'),'R hand':('Rw','Rf')}
report=[]
for s in scenes:
 arms=[o for o in s.objects if o.type=='ARMATURE']
 if not arms:continue
 bpy.context.window.scene=s;arm=arms[0];root=arm.parent;controls={n:bpy.data.objects[name] for n,name in json.loads(root['controls']).items()};lengths=json.loads(root['rest_lengths']);skin=next(o for o in root.children if o.type=='MESH');maxerr=0.;s.frame_set(1);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();ev=skin.evaluated_get(dg);me=ev.to_mesh();binderror=max((v.co-skin.data.vertices[i].co).length for i,v in enumerate(me.vertices));ev.to_mesh_clear();assert binderror<1e-4,(s.name,binderror)
 floor_ids=[v.index for v in skin.data.vertices if v.co.y<.05];original={i:skin.data.vertices[i].co.copy() for i in floor_ids};floorerror=0
 for f in range(1,s.frame_end+1):
  s.frame_set(f);bpy.context.view_layer.update()
  for name,(a,b) in links.items():maxerr=max(maxerr,abs((controls[b].location-controls[a].location).length-lengths[name]))
  if f in [1,s.frame_end//2,s.frame_end]:
   dg=bpy.context.evaluated_depsgraph_get();ev=skin.evaluated_get(dg);me=ev.to_mesh();floorerror=max(floorerror,max((me.vertices[i].co-original[i]).length for i in floor_ids));ev.to_mesh_clear()
 assert maxerr<1e-5 and floorerror<1e-5,(s.name,maxerr,floorerror)
 report.append({'scene':s.name,'frames':s.frame_end,'max_chain_length_error':maxerr,'rest_skin_error':binderror,'floor_vertex_error':floorerror});s.frame_set(1)
(O/'native-checks.json').write_text(json.dumps({'shared_environment_scenes':7,'same_collection_identity':True,'dark_reveal_camera_match':True,'seated_rigs':report,'limit':'Seated construction checks only. No claim that rise/throw or the film rebuild is complete.'},indent=2))
result={'checked_seated_rigs':len(report),'shared_room_scenes':7,'status':'technical checks passed; creative motion review remains'}
