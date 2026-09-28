"""Read-only inventory of the exact episode 001 delivered native file."""
import bpy,json
from pathlib import Path
out=Path(__file__).parent
edit=json.loads((Path(bpy.data.filepath).parent/'edit.json').read_text())
rows=[]
for shot in edit:
 s=bpy.data.scenes[shot['scene']]
 skins=[o for o in s.objects if o.type=='MESH' and any(m.type=='ARMATURE' for m in o.modifiers)]
 rows.append({'scene':s.name,'armature_skins':len(skins),'grease_pencil_objects':sum(o.type=='GREASEPENCIL' for o in s.objects),'examples':[{'name':o.name,'vertices':len(o.data.vertices),'groups':len(o.vertex_groups),'preserve_volume':[m.use_deform_preserve_volume for m in o.modifiers if m.type=='ARMATURE'],'image_textures':sorted({n.image.name for mat in o.data.materials if mat and mat.use_nodes for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image})} for o in skins[:3]]})
(out/'delivery-native-inventory.json').write_text(json.dumps({'file':bpy.data.filepath,'blender':bpy.app.version_string,'shots':rows},indent=2)+'\n')
print('INSPECTED',len(rows),'shots;',sum(x['armature_skins'] for x in rows),'skinned object appearances')
