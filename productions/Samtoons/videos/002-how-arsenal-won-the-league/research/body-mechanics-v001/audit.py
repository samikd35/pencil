"""Read-only reproduction against the rejected saved Blender scene.

Run Blender -b bruno-action-v006.blend --python-exit-code 1 --python audit.py.
Expected failure: neutral-pose knee drift. This cannot score animation quality.
"""
import bpy
import json
from pathlib import Path

out = Path(__file__).resolve().parent
s = bpy.data.scenes['S002_Bruno_action_v006']
bpy.context.window.scene = s
root = next(o for o in s.objects if o.name.startswith('A Drama Bruno / ROOT'))
arm = next(o for o in root.children_recursive if o.type == 'ARMATURE')
controls, rest = {}, {}
for bone in arm.pose.bones:
    for kind, point in [('COPY_LOCATION', bone.bone.head_local), ('STRETCH_TO', bone.bone.tail_local)]:
        target = next(c.target for c in bone.constraints if c.type == kind)
        key = target.name.split('CTRL ')[1].split('.')[0]
        controls[key], rest[key] = target, point.copy()
s.frame_set(192)
bpy.context.view_layer.update()
errors = {k: (o.location.xy - rest[k].xy).length for k, o in controls.items()}
report = {
    'scene': s.name,
    'neutral_frame': 192,
    'neutral_planar_errors': errors,
    'rest_controls': {k: list(v) for k, v in rest.items()},
    'gravity_setting': list(s.gravity),
    'body_rigid_body': any(o.rigid_body for o in root.children_recursive),
    'root_scale': list(root.scale),
    'prior_contact_check': json.loads((out.parents[1] / 'artifacts/bruno-action-v006/verification.json').read_text()),
    'creative_verdict': 'rejected; contact checks do not establish believable motion',
}
fps = s.render.fps / s.render.fps_base
positions = {}
for f in range(90, 111):
    s.frame_set(f)
    bpy.context.view_layer.update()
    positions[f] = list(controls['hip'].matrix_world.translation)
report['flight_hip_samples'] = positions
report['flight_hip_vertical_acceleration'] = [
    (positions[f+1][2] - 2*positions[f][2] + positions[f-1][2])*fps**2
    for f in range(92, 110)
]
report['caution'] = 'Hip is not true COM. Effective acceleration is diagnostic, not a universal realism threshold.'
(out / 'audit.json').write_text(json.dumps(report, indent=2) + '\n')
print('NEUTRAL_POSE maximum planar error:', max(errors.values()), flush=True)
assert max(errors.values()) < 1e-4, 'REPRODUCED: supposedly neutral pose changes original knee bend'
