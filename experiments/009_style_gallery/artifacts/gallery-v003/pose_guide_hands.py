from pathlib import Path
import sys,json,bpy
root=Path('/Users/samikd/MyProjects/Pencil');sys.path.insert(0,str(root/'pipeline/styles'))
from build_samples import render_sample
out=root/'experiments/009_style_gallery/artifacts/gallery-v003'
ids=sys.argv[sys.argv.index('--')+1:]
options=json.loads((root/'pipeline/styles/catalog.json').read_text())['options']
for option in options:
    if ids and option['id'] not in ids:continue
    folder=out/option['id'];assert not (folder/'guide.png').exists()
    bpy.ops.wm.open_mainfile(filepath=str(folder/'character.blend'))
    render_sample(folder/'guide.png',option)
    (folder/'guide-builder.py').write_bytes((root/'pipeline/styles/build_samples.py').read_bytes())
    print('GUIDE POSE: '+option['id'],flush=True)
