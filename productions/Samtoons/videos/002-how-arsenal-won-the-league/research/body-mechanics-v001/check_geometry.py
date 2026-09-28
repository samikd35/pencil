"""Check corrected geometry against the actual native rest-pose capture."""
from pathlib import Path
import json, math, sys
R=Path(__file__).resolve().parents[6];sys.path.insert(0,str(R/'pipeline'))
from pose_geometry import two_bone_joint
folder=Path(__file__).resolve().parent
rest=json.loads((folder/'audit.json').read_text())['rest_controls']
report={}
for side in ['L','R']:
 hip,knee,ankle=[rest[side+k][:2] for k in ['hip','knee','ankle']]
 lengths=(math.dist(hip,knee),math.dist(knee,ankle))
 solved=two_bone_joint(hip,ankle,lengths,knee)
 error=math.dist(solved,knee);assert error<1e-6,error
 report[side]={'rest_error':error,'segment_lengths':lengths}
 # Reachable compression retains the chosen bend side and both lengths.
 lowered=(hip[0],hip[1]-.2)
 bend=two_bone_joint(lowered,ankle,lengths,knee)
 assert abs(math.dist(lowered,bend)-lengths[0])<1e-6
 assert abs(math.dist(bend,ankle)-lengths[1])<1e-6
report['scope']='Geometry correction only; rejected animation unchanged and not approved.'
(folder/'geometry-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
