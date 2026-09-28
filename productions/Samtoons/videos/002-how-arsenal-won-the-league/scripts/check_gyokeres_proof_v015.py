"""All-frame source-surface regression check. Appearance still requires playback review."""
import bpy,json,numpy as np
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/gyokeres-proof-v015'
s=bpy.data.scenes['S002_Gyokeres_complete_proof_v015'];bpy.context.window.scene=s
skin=next(o for o in s.objects if o.name=='G15 / complete source surface')
im=next(n.image for n in skin.data.materials[0].node_tree.nodes if n.type=='TEX_IMAGE');pix=np.empty(im.size[0]*im.size[1]*4,dtype=np.float32);im.pixels.foreach_get(pix);alpha=pix.reshape(im.size[1],im.size[0],4)[:,:,3]
uvs={l.vertex_index:skin.data.uv_layers.active.data[l.index].uv[:] for l in skin.data.loops}
def visible(poly):
 uv=np.mean([uvs[i] for i in poly.vertices],axis=0);return alpha[min(1023,int(uv[1]*1024)),min(1535,int(uv[0]*1536))]>.95
base=np.array([v.co[:2] for v in skin.data.vertices]);tri=np.array([p.vertices[:] for p in skin.data.polygons if visible(p)]);ab=base[tri[:,1]]-base[tri[:,0]];ac=base[tri[:,2]]-base[tri[:,0]];area=ab[:,0]*ac[:,1]-ab[:,1]*ac[:,0];rows=[]
for f in range(1,145):
 s.frame_set(f);bpy.context.view_layer.update();ev=skin.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();pts=np.array([v.co[:2] for v in me.vertices]);ab=pts[tri[:,1]]-pts[tri[:,0]];ac=pts[tri[:,2]]-pts[tri[:,0]];r=(ab[:,0]*ac[:,1]-ab[:,1]*ac[:,0])/area;ev.to_mesh_clear()
 rows.append({'frame':f,'flips':int((r<=0).sum()),'minimum_area_ratio':float(r.min()),'maximum_area_ratio':float(r.max())})
result={'worst_flips':max(r['flips'] for r in rows),'minimum_area_ratio':min(r['minimum_area_ratio'] for r in rows),'maximum_area_ratio':max(r['maximum_area_ratio'] for r in rows),'frames':rows,'scope':'Source mesh deformation only; does not approve appearance or acting.'}
(O/'deformation-check.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='frames'}),flush=True)
assert result['worst_flips']==0,'Source surface folded during the proof'
