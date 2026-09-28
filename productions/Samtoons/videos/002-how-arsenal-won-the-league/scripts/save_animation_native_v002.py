"""Give rendered scene libraries usable startup scenes, without touching the live window."""
import bpy,json,os
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v002'
reports=[]
for relative,scene,frame in [('CP01/CP01-v001.blend','S002_CP01_loaded_run_v001',1),('arsenal-progress-v002.blend','S002_animation_progress_v002',2369)]:
 target=O/relative;library=target.with_name(target.stem+'-library.blend')
 assert target.exists() and not library.exists();target.rename(library)
 bpy.ops.wm.open_mainfile(filepath=str(library));s=bpy.data.scenes[scene];bpy.context.window.scene=s;s.frame_set(frame)
 for area in bpy.context.screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_overlays=False
 if s.sequence_editor:
  pictures=[q for q in s.sequence_editor.strips if q.name.startswith('Picture / ')]
  assert len(pictures)==56 and sum(int(q.frame_final_duration) for q in pictures)==5954
  assert all(os.path.exists(bpy.path.abspath(q.filepath)) for q in pictures)
  assert next(q.filepath for q in pictures if q.name=='Picture / CP03_pep').endswith('CP03_pep-v002-silent.mp4')
 bpy.ops.wm.save_as_mainfile(filepath=str(target))
 reports.append(dict(path=str(target),startup_scene=s.name,frame=frame))
(O/'native-package-checks.json').write_text(json.dumps(reports,indent=2))
print('Native startup scenes saved;56picture dependencies and unchanged Pep checked.')
