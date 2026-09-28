from pathlib import Path
import sys,json,bpy
root=Path('/Users/samikd/MyProjects/Pencil');sys.path.insert(0,str(root/'pipeline/styles'))
from build_samples import verify_sample_pose
out=root/'experiments/009_style_gallery/artifacts/gallery-v003'
for o in json.loads((root/'pipeline/styles/catalog.json').read_text())['options']:
    folder=out/o['id'];bpy.ops.wm.open_mainfile(filepath=str(folder/'guide-pose.blend'))
    checks=verify_sample_pose();(folder/'guide-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(o['id']+': reopened still hand connections and framing pass',flush=True)
