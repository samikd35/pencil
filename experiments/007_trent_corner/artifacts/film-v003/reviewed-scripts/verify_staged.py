"""Verify staging coverage, visibility and contact before presenting the checkpoint."""
from pathlib import Path
import bpy,json,math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v003'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'trent-corner-advanced.blend'));s=bpy.context.scene
cast=json.loads((ROOT/'staging-v004.json').read_text())['cast'];s.frame_set(403);bpy.context.view_layer.update()
assert sum(a['team']=='Liverpool' for a in cast)==7
assert sum(a['team']=='Barcelona' for a in cast)==8
visible=[]
for spec in cast:
    name=spec['id'];body=bpy.data.objects[name+' / Jersey'];p=body.matrix_world@Vector((0,-.012,.3));uv=world_to_camera_view(s,s.camera,p)
    assert .04<uv.x<.96 and .1<uv.y<.85,(name,tuple(uv))
    direction=p-s.camera.location;hit,where,normal,index,obj,matrix=s.ray_cast(bpy.context.evaluated_depsgraph_get(),s.camera.location,direction.normalized(),distance=direction.length+.02)
    visible.append({'player':name,'team':spec['team'],'torso_frame_xy':[uv.x,uv.y],'first_ray_hit':obj.name if hit else None})
# Camera rays demonstrate the newly added red teammates are not merely present behind defenders.
assert all(v['first_ray_hit'] and v['first_ray_hit'].startswith(v['player']+' /') for v in visible if v['player'].startswith('Attacker'))
contacts=[]
for f,name in [(403,'Trent'),(433,'Origi'),(633,'Trent'),(673,'Origi')]:
    s.frame_set(f);bpy.context.view_layer.update();toe=bpy.data.objects[name+' / Boot 1'].matrix_world@Vector((0,.24,0));ball=bpy.data.objects['Ball / continuous'].location
    gap=(toe-ball).length-.17;assert abs(gap)<1e-5,(f,gap);contacts.append({'frame':f,'player':name,'gap':gap})
for name,a,b in [('Trent',395,419),('Origi',419,441)]:
    points=[]
    for f in range(a,b+1):s.frame_set(f);points.append(bpy.data.objects[name+' / Boot 0'].location.copy())
    assert max((p-points[0]).length for p in points)<1e-5
for f in range(395,481):
    s.frame_set(f);uv=world_to_camera_view(s,s.camera,bpy.data.objects['Ball / continuous'].location)
    assert .04<uv.x<.96 and .08<uv.y<.85
report={'role_count':{'Liverpool':7,'Barcelona_including_keeper':8},'staging':visible,'contacts':contacts,'added_teammates_visible_by_camera_ray':True,'interpretation':'Representative corner arrangement, not exact tracked historic positions. Frame visibility and geometry checks remain separate from user creative review.'}
(OUT/'staging-checks.json').write_text(json.dumps(report,indent=2)+'\n');print('STAGING_CHECKS_PASSED')
