"""Extract the actual delivered scene, with unchanged artwork, rig and animation."""
import bpy,json,hashlib
from pathlib import Path
ROOT=Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/002-how-arsenal-won-the-league')
OUT=ROOT/'artifacts/video-001-baseline-v001'
source=ROOT.parent/'001-manchester-derby-2026-09-13/artifacts/delivery-v001/samtoons-final.blend'
assert not (OUT/'baseline.blend').exists()
if bpy.data.is_dirty:
 bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'artifacts/layered-action-v002/rejected-working-state.blend'))
with bpy.data.libraries.load(str(source),link=False) as (available,loaded):
 assert 'S02 / kick and overreaction' in available.scenes
 loaded.scenes=['S02 / kick and overreaction']
s=loaded.scenes[0];bpy.context.window.scene=s;s.frame_set(77)
# Native library write copies only this scene and its dependencies; source remains untouched.
bpy.data.libraries.write(str(OUT/'baseline.blend'),{s},fake_user=True)
report={'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scene':s.name,'scope':'Actual episode 001 kick/fall/protest construction, unchanged. Baseline reference, not Gyokeres or a new approved action.','frame':77,'objects':len(s.objects),'native':'baseline.blend'}
(OUT/'provenance.json').write_text(json.dumps(report,indent=2)+'\n')
result=report
