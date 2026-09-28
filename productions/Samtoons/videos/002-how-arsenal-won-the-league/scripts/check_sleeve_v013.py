"""Actual sleeve deformation regression, on the saved scene at the reported pose."""
import bpy,json
from pathlib import Path
V=Path(__file__).resolve().parents[1]
s=next(s for s in bpy.data.scenes if s.name.startswith('S002_B01_') and s.name.endswith('_unveiling'));bpy.context.window.scene=s
old=bpy.data.objects.get('B01 / unveiling Arteta / v012 illustrated skin')
skin=old if old and not old.hide_render else bpy.data.objects['B01 / unveiling Arteta / connected upper body']
me=skin.data
if skin==old:
 uvs={l.vertex_index:me.uv_layers.active.data[l.index].uv.copy() for l in me.loops}
 polygons=[tuple(p.vertices) for p in me.polygons if sum(uvs[i].x*1536 for i in p.vertices)/len(p.vertices)<1030 and 340<sum((1-uvs[i].y)*1024 for i in p.vertices)/len(p.vertices)<500]
 reference=[v.co.copy() for v in me.vertices]
else:
 # The middle of the screen-right sleeve, excluding the authored shoulder fan.
 polygons=[tuple(p.vertices) for p in me.polygons if len(p.vertices)==4 and all(28<=i<80 for i in p.vertices)]
 s.frame_set(1);bpy.context.view_layer.update();ev=skin.evaluated_get(bpy.context.evaluated_depsgraph_get());base=ev.to_mesh();reference=[v.co.copy() for v in base.vertices];ev.to_mesh_clear()
def area(a,b,c):return (b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x)
s.frame_set(315);bpy.context.view_layer.update();ev=skin.evaluated_get(bpy.context.evaluated_depsgraph_get());out=ev.to_mesh();ratios=[]
for p in polygons:
 for j in range(1,len(p)-1):
  ids=[p[0],p[j],p[j+1]];base=area(*(reference[i] for i in ids))
  if abs(base)>1e-6:ratios.append(area(*(out.vertices[i].co for i in ids))/base)
ev.to_mesh_clear()
result={'file':bpy.data.filepath,'sample':'Arteta, frame315, sleeve interior','triangles':len(ratios),'flipped':sum(r<0 for r in ratios),'more_than_double_area':sum(r>2 for r in ratios),'minimum_area_ratio':min(ratios),'maximum_area_ratio':max(ratios),'scope':'A deformation check, not likeness or normal-speed acting acceptance.'}
print(json.dumps(result),flush=True)
assert result['flipped']==0 and result['maximum_area_ratio']<2,'Sleeve folds over or stretches locally beyond twice its reference area'
