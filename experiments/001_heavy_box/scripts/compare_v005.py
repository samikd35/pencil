"""Check independently rendered revision frames against the previous delivery."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'artifacts/rough-v003'
NEW=ROOT/'artifacts/rough-v005'
unchanged=[]
changed=[]
manifest=[]
for frame in range(1,241):
    name=f'frame-{frame:04}.png'
    a=(OLD/'frames'/name).read_bytes()
    path=NEW/'frames'/name
    b=path.read_bytes()
    (unchanged if a==b else changed).append(frame)
    manifest.append({'path':str(path.relative_to(ROOT)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
protected=list(range(1,89))+list(range(193,241))
assert all(f in unchanged for f in protected), 'The revision changed protected opening/ending frames'
assert 110 in changed and 118 in changed and 162 in changed, 'Expected acting and recovery revisions are absent'
report={'status':'passed','base':'rough-v003','revision':'rough-v005',
        'comparison':'Exact PNG byte equality on independently rendered frames',
        'protected_intervals':[[1,88],[193,240]],'protected_frames_identical':len(protected),
        'changed_frames':changed,'unchanged_frames':unchanged}
(NEW/'revision-comparison.json').write_text(json.dumps(report,indent=2)+'\n')
(NEW/'frames-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'{len(protected)} protected frames identical; {len(changed)} revised frames; all 240 accounted for.')
