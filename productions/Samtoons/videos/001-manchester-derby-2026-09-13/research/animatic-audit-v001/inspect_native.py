"""Read-only saved-scene audit. Never saves or changes production artwork."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'artifacts/animatic-v001/combined-animatic-v006.blend'))
def curves(o):
 if not o.animation_data or not o.animation_data.action:return []
 return [fc for layer in o.animation_data.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
edit=json.loads((R/'artifacts/animatic-v001/edit.json').read_text());report=[]
for row in edit:
 s=bpy.data.scenes[row['scene']];bpy.context.window.scene=s
 camera=[dict(path=fc.data_path,index=fc.array_index,keys=[dict(frame=k.co.x,value=k.co.y,interpolation=k.interpolation) for k in fc.keyframe_points]) for fc in curves(s.camera)]
 actors=[]
 for root in [o for o in s.objects if o.name.endswith('/ ROOT')]:
  skins=[o for o in root.children if o.type=='MESH' and any(m.type=='ARMATURE' for m in o.modifiers)]
  if not skins:continue
  skin=skins[0];arm=next(m.object for m in skin.modifiers if m.type=='ARMATURE')
  s.frame_set(1);n=root.matrix_world.to_quaternion()@Vector((0,0,1));v=(s.camera.location-root.matrix_world.translation).normalized();ang=math.degrees(math.acos(min(1,abs(n.dot(v)))))
  angles=[]
  keyframes=sorted(set(int(k.co.x) for fc in curves(s.camera) for k in fc.keyframe_points)) or [1]
  for fr in keyframes:
   s.frame_set(fr);n=root.matrix_world.to_quaternion()@Vector((0,0,1));v=(s.camera.location-root.matrix_world.translation).normalized();angles.append([fr,round(math.degrees(math.acos(min(1,abs(n.dot(v))))),2)])
  actors.append(dict(name=root.name,skin_vertices=len(skin.data.vertices),skin_faces=len(skin.data.polygons),native_arm_objects=[o.name for o in root.children if any(x in o.name for x in (' native ',' upper ',' palm '))],bone_parent_count=sum(b.parent is not None for b in arm.data.bones),bone_count=len(arm.data.bones),camera_to_art_plane_normal_degrees=angles))
 report.append(dict(**row,fps=s.render.fps/s.render.fps_base,camera=camera,actors=actors))
(O/'native-inspection.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps([dict(scene=r['scene'],actors=len(r['actors']),camera_key_frames=sorted(set(k['frame'] for fc in r['camera'] for k in fc['keys']))) for r in report],indent=2))
