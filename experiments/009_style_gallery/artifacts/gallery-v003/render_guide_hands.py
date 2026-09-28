from pathlib import Path
import json,subprocess
root=Path('/Users/samikd/MyProjects/Pencil');out=root/'experiments/009_style_gallery/artifacts/gallery-v003'
options=json.loads((root/'pipeline/styles/catalog.json').read_text())['options']
for i,option in enumerate(options,1):
    folder=out/option['id']
    with (out/(option['id']+'.log')).open('w') as log:
        subprocess.run(['/Applications/Blender.app/Contents/MacOS/Blender','-b','-t','4','--python',str(root/'pipeline/styles/build_samples.py'),'--','--style',option['id'],'--out',str(folder)],stdout=log,stderr=subprocess.STDOUT,check=True,cwd=root)
    check=json.loads((folder/'checks.json').read_text());assert check['status']=='passed' and check['frames']==240
    print(f'{i}/19 {option["id"]}: rendered; 240-frame checks passed',flush=True)
