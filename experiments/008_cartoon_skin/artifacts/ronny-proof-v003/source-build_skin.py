"""Put a continuous cartoon surface on Heavy Box's existing editable controls."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[1]
BASE = ROOT.parent / '001_heavy_box/artifacts/finish-v002'
sys.path.insert(0, str(ROOT.parent / '001_heavy_box'))
from journal import append_event

parser = argparse.ArgumentParser()
parser.add_argument('--out', required=True)
parser.add_argument('--render', action='store_true')
args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
assert Path(args.out).name == args.out, 'Use a single revision directory name'
OUT = ROOT / 'artifacts' / args.out


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def controllers():
    names = sorted(o.name for o in bpy.data.objects if o.name.startswith(('CTRL_', 'ANCHOR_')))
    frames = []
    for f in range(1, 241):
        bpy.context.scene.frame_set(f)
        bpy.context.view_layer.update()
        values = [(n, [list(row) for row in bpy.data.objects[n].matrix_world]) for n in names]
        frames.append(hashlib.sha256(json.dumps(values).encode()).hexdigest())
    return names, frames


def contact_geometry():
    frames = []
    for f in range(1, 241):
        bpy.context.scene.frame_set(f)
        bpy.context.view_layer.update()
        points = []
        for name in ('Mitten_far', 'Mitten_near', 'Shoe_far', 'Shoe_near'):
            obj = bpy.data.objects[name]
            points.append([list((obj.matrix_world @ v.co)[:2]) for v in obj.data.vertices])
        frames.append(hashlib.sha256(json.dumps(points).encode()).hexdigest())
    return frames


def material(name, color):
    rgb = [int(color[i:i+2], 16)/255 for i in (1, 3, 5)]
    rgba = tuple(v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in rgb) + (1,)
    m = bpy.data.materials.new(name)
    m.diffuse_color = rgba
    m.use_nodes = True
    nodes = m.node_tree.nodes
    nodes.clear()
    output = nodes.new('ShaderNodeOutputMaterial')
    shader = nodes.new('ShaderNodeEmission')
    shader.inputs['Color'].default_value = rgba
    m.node_tree.links.new(shader.outputs[0], output.inputs['Surface'])
    return m


def polygon(name, points, z, mat, parent, outline=True):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([(*p, z) for p in points], [], [list(range(len(points)))])
    mesh.materials.append(mat)
    obj = bpy.data.objects.new(name, mesh)
    skin.objects.link(obj)
    obj.parent = parent
    if outline:
        curve = bpy.data.curves.new(name + ' outline', 'CURVE')
        curve.dimensions = '3D'
        curve.bevel_depth = .018
        curve.bevel_resolution = 3
        curve.materials.append(ink)
        spline = curve.splines.new('POLY')
        spline.points.add(len(points)-1)
        spline.use_cyclic_u = True
        for point, xy in zip(spline.points, points):
            point.co = (*xy, z+.008, 1)
        edge = bpy.data.objects.new(name + ' outline', curve)
        skin.objects.link(edge)
        edge.parent = parent
    return obj


def oval(cx, cy, rx, ry):
    return [(cx+rx*math.cos(i*math.tau/64), cy+ry*math.sin(i*math.tau/64)) for i in range(64)]


def verify(expected):
    names, actual = controllers()
    assert actual == expected, 'Existing control motion changed'
    max_gap = 0
    for f in range(1, 241):
        bpy.context.scene.frame_set(f)
        graph = bpy.context.evaluated_depsgraph_get()
        for side in ('far', 'near'):
            for part, control in (('Arm', 'Hand'), ('Leg', 'Foot')):
                for suffix in ('', ' fill'):
                    obj = bpy.data.objects[part+'_'+side+suffix]
                    evaluated = obj.evaluated_get(graph)
                    endpoint = evaluated.matrix_world @ evaluated.data.splines[0].bezier_points[1].co
                    target = bpy.data.objects['CTRL_'+control+'_'+side].matrix_world.translation
                    gap = math.dist(endpoint[:2], target[:2])
                    max_gap = max(max_gap, gap)
                    assert gap < 1e-5, (f, obj.name, gap)
                    assert all(fc.driver.is_valid for fc in obj.data.animation_data.drivers)
    # Prove live editability after reopening, rather than only baked-frame agreement.
    bpy.context.scene.frame_set(110)
    hand = bpy.data.objects['CTRL_Hand_near']
    original = hand.location.copy()
    hand.location.x += .2
    bpy.context.view_layer.update()
    arm = bpy.data.objects['Arm_near fill'].evaluated_get(bpy.context.evaluated_depsgraph_get())
    tip = arm.matrix_world @ arm.data.splines[0].bezier_points[1].co
    assert math.dist(tip[:2], hand.matrix_world.translation[:2]) < 1e-5
    mitten = bpy.data.objects['Mitten_near']
    assert mitten.parent == hand
    hand.location = original
    bpy.context.scene.frame_set(1)
    return {'status': 'passed', 'frames': 240, 'controllers': len(names),
            'identical_controller_frame_hashes': actual, 'max_endpoint_gap': max_gap,
            'saved_project_hand_edit': 'passed',
            'limits': 'Endpoint/driver evidence does not certify every visible overlap or cartoon appeal.'}


if args.render:
    bpy.ops.wm.open_mainfile(filepath=str(OUT / 'cartoon-skin.blend'))
    scene = bpy.context.scene
    assert not (OUT / 'cartoon-picture.mp4').exists(), 'Preserve existing renders'
    # Short 640x360 mechanism proof; not a full-quality film render.
    scene.render.resolution_percentage = 50
    scene.eevee.taa_render_samples = 16
    scene.render.image_settings.media_type = 'VIDEO'
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH'
    scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
    scene.render.ffmpeg.audio_codec = 'NONE'
    scene.render.filepath = str(OUT / 'cartoon-picture.mp4')
    bpy.ops.render.render(animation=True)
    sys.exit(0)

OUT.mkdir(parents=True, exist_ok=False)
baseline_hash = digest(BASE / 'character-and-effects.blend')
append_event(ROOT, stage='skin-proof', status='started',
    intent='Test fuller cartoon surfaces on unchanged working stickman motion',
    method='Existing native curves plus filled curve copies and named flat artwork',
    inputs=['README.md', 'build_skin.py'],
    sources=[{'path': str(BASE / 'character-and-effects.blend'), 'sha256': baseline_hash}],
    result='Source saved before build. User authorized exploration and a small experiment.')
bpy.ops.wm.open_mainfile(filepath=str(BASE / 'character-and-effects.blend'))
scene = bpy.context.scene
names, baseline = controllers()
baseline_contacts = contact_geometry()
skin = bpy.data.collections.new('Cartoon surface / same stickman controls')
scene.collection.children.link(skin)
ink = material('Cartoon ink', '#25394c')
shirt = material('Coral shirt', '#df775e')
trousers = material('Blue trousers', '#517b98')
paper = material('Collar', '#fff9ed')

# Each visible limb is one continuous curve. The copied drivers keep live control links.
# ponytail: constant-width elastic limbs; use authored tapered contours for anatomical styles.
for side in ('far', 'near'):
    for part, radius, mat in (('Arm', .112, shirt), ('Leg', .15, trousers)):
        obj = bpy.data.objects[part+'_'+side]
        obj.data.bevel_depth = radius + .018
        obj.data.use_fill_caps = True
        obj.data.materials.clear()
        obj.data.materials.append(ink)
        fill = obj.copy()
        fill.data = obj.data.copy()
        fill.name = obj.name + ' fill'
        skin.objects.link(fill)
        fill.data.bevel_depth = radius
        fill.location.z += .035
        fill.data.materials.clear()
        fill.data.materials.append(mat)

body = bpy.data.objects['CTRL_Body']
bpy.data.objects['Bean torso'].hide_render = True
shirt_points = [(-.10,.92),(.14,.90),(.26,.72),(.33,.25),(.30,-.02),
                (.12,-.11),(-.16,-.10),(-.31,.02),(-.30,.36),(-.24,.72)]
polygon('Full shirt', shirt_points, .50, shirt, body)
polygon('Trouser waist', [(-.28,.03),(.29,.03),(.28,-.18),(-.27,-.18)], .48, trousers, body)
polygon('Collar', [(-.10,.90),(.13,.88),(.05,.75),(-.04,.77)], .54, paper, body)
polygon('Chest patch', [(.04,.58),(.19,.56),(.20,.41),(.06,.42)], .54, paper, body, False)

# Keep projected hand/shoe geometry unchanged; bring their drawings in front of the sleeves.
for obj in bpy.data.objects:
    if obj.parent and obj.parent.name.startswith(('CTRL_Hand_', 'CTRL_Foot_')):
        obj.location.z += .25
    elif obj.parent and obj.parent.name == 'CTRL_Head':
        obj.location.z += .30

for sound in bpy.data.sounds:
    sound.filepath = str(BASE / 'audio/soundtrack.wav')
bpy.ops.file.pack_all()
scene['Experiment'] = 'Cartoon surface on unchanged Heavy Box motion; native curves/meshes, not Grease Pencil.'
scene['Review status'] = 'Low-resolution mechanism proof; not accepted cartoon identity.'
scene.render.resolution_percentage = 50
scene.eevee.taa_render_samples = 16
scene.frame_set(110)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / 'cartoon-skin.blend'))
bpy.ops.wm.open_mainfile(filepath=str(OUT / 'cartoon-skin.blend'))
scene = bpy.context.scene
checks = verify(baseline)
assert contact_geometry() == baseline_contacts, 'Projected hand/shoe geometry changed'
checks['projected_hand_and_shoe_geometry'] = 'exact equality across 240 frames'
assert digest(BASE / 'character-and-effects.blend') == baseline_hash
checks['source_project_sha256'] = baseline_hash
checks['source_preserved'] = True
(OUT / 'checks.json').write_text(json.dumps(checks, indent=2)+'\n')
for f in (1, 54, 104, 118, 138, 154, 158, 162, 167, 170, 179, 220):
    scene.frame_set(f)
    scene.render.filepath = str(OUT / f'pose-{f:03}.png')
    bpy.ops.render.render(write_still=True)
append_event(ROOT, stage='skin-technical-check', status='passed',
    intent='Verify controller preservation and live limb endpoints in the reopened candidate',
    method='All-frame comparison and a temporary hand-control edit',
    inputs=['build_skin.py'], outputs=[str((OUT / n).relative_to(ROOT)) for n in ('cartoon-skin.blend', 'checks.json')],
    result='240 controller frames match; all eight limb curves follow endpoints; saved hand edit works. Visual review remains separate.')
print('CARTOON_SKIN_BUILD_COMPLETE', OUT, flush=True)
