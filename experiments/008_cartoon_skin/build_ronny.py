"""Reference-led character identity on the saved, working cartoon surface proof."""
import argparse
import ast
from collections import deque
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
import numpy as np

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets/ronny-v001'
SOURCE = ROOT / 'artifacts/proof-v002/cartoon-skin.blend'
sys.path.insert(0, str(ROOT.parent / '001_heavy_box'))
from journal import append_event

parser = argparse.ArgumentParser()
parser.add_argument('--out', required=True)
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
assert Path(args.out).name == args.out
OUT = ROOT / 'artifacts' / args.out
OUT.mkdir(parents=True, exist_ok=False)
(OUT / 'source-build_ronny.py').write_bytes(Path(__file__).read_bytes())

# Reuse the existing helpers without running that script's build/render side effects.
names = {'digest', 'controllers', 'contact_geometry', 'material', 'polygon', 'oval', 'verify'}
definitions = [n for n in ast.parse((ROOT / 'build_skin.py').read_text()).body
               if isinstance(n, ast.FunctionDef) and n.name in names]
assert len(definitions) == len(names)
exec(compile(ast.Module(body=definitions, type_ignores=[]), str(ROOT / 'build_skin.py'), 'exec'))
append_event(ROOT, stage='ronny-native-build', status='started',
    intent='Put the supplied identity and kit on the existing box-pushing character',
    method='Whole-head sprite expressions and native kit artwork driven by existing controls',
    inputs=['build_ronny.py', 'build_skin.py', 'assets/ronny-v001/heads.png',
            'assets/ronny-v001/reference.jpg', 'artifacts/proof-v002/cartoon-skin.blend'],
    result='Source archived before building. Motion, hand/foot contours, stage and audio remain inputs.')
source_hash = digest(SOURCE)
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene = bpy.context.scene
_, baseline = controllers()
contact_baseline = contact_geometry()
skin = bpy.data.collections.new('Reference character / kit and whole-head drawings')
scene.collection.children.link(skin)
ink = material('Reference kit / ink', '#202c34')
white = material('Reference kit / white', '#f4f5ef')
warm_skin = material('Reference character / skin', '#e9a16c')
red = material('Reference kit / red', '#c9414f')
green = material('Reference kit / green', '#429f82')
navy = material('Reference kit / captain band', '#152c51')
section_specs = []


def assign(name, mat):
    obj = bpy.data.objects[name]
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def curve_section(name, source, a, b, radius, mat, dz):
    """Exact Bezier subcurve, kept live through source-coordinate drivers."""
    assert 0 <= a < b <= 1
    obj = source.copy()
    obj.data = source.data.copy()
    obj.name = name
    obj.data.animation_data_clear()
    skin.objects.link(obj)
    obj.location.z += dz
    obj.data.bevel_depth = radius
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    paths = ['splines[0].bezier_points[0].co', 'splines[0].bezier_points[0].handle_right',
             'splines[0].bezier_points[1].handle_left', 'splines[0].bezier_points[1].co']
    for point, t, sign in ((0, a, 1), (1, b, -1)):
        weights = [(1-t)**3, 3*(1-t)**2*t, 3*(1-t)*t*t, t**3]
        derivative = [-3*(1-t)**2, 3*(1-t)**2-6*(1-t)*t, 6*(1-t)*t-3*t*t, 3*t*t]
        handles = [v+sign*(b-a)*dv/3 for v, dv in zip(weights, derivative)]
        for prop in ('co', 'handle_left', 'handle_right'):
            coefficients = weights if prop == 'co' else handles
            for axis in range(2):
                d = obj.data.driver_add(f'splines[0].bezier_points[{point}].{prop}', axis).driver
                for j, path in enumerate(paths):
                    v = d.variables.new()
                    v.name = 'p'+str(j)
                    v.type = 'SINGLE_PROP'
                    v.targets[0].id_type = 'CURVE'
                    v.targets[0].id = source.data
                    v.targets[0].data_path = f'{path}[{axis}]'
                d.expression = '+'.join(f'({w:.12f})*p{j}' for j, w in enumerate(coefficients))
    section_specs.append((obj.name, source.name, a, b))
    return obj


body = bpy.data.objects['CTRL_Body']
head_control = bpy.data.objects['CTRL_Head']
for obj in list(bpy.data.objects):
    if obj.parent == head_control:
        obj.hide_render = obj.hide_viewport = True
        # Existing eye/mouth animation remains preserved in the hidden source drawings.
for name in ('Full shirt', 'Trouser waist'):
    assign(name, white)
assign('Collar', ink)
bpy.data.objects['Chest patch'].hide_render = True
for side in ('far', 'near'):
    assign('Arm_'+side+' fill', white)
    assign('Leg_'+side+' fill', warm_skin)
    assign('Mitten_'+side, warm_skin)
    assign('Shoe_'+side, ink)
    leg = bpy.data.objects['Leg_'+side]
    curve_section('Shorts '+side+' outline', leg, 0, .33, .185, ink, .05)
    curve_section('Shorts '+side, leg, 0, .33, .166, white, .085)
    curve_section('Socks '+side, leg, .72, 1, .15, white, .055)
curve_section('Captain armband', bpy.data.objects['Arm_near'], .18, .36, .116, navy, .045)

# Collar covers a simple native neck; detailed head drawings never share arm geometry.
polygon('Neck', [(-.11,.68),(.13,.68),(.13,1.12),(-.11,1.12)], .46, warm_skin, body)
font = bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf')
number = bpy.data.curves.new('Kit number 7', 'FONT')
number.body = '7'
number.font = font
number.align_x = 'CENTER'
number.align_y = 'CENTER'
number.size = .48
number.materials.append(ink)
obj = bpy.data.objects.new('Kit number 7', number)
skin.objects.link(obj)
obj.parent = body
obj.location = (.015,.35,.565)
polygon('Simplified Portugal badge', [(.12,.70),(.24,.69),(.23,.58),(.18,.54),(.12,.59)], .56, red, body, False)
polygon('Badge center', [(.155,.67),(.205,.67),(.205,.59),(.155,.59)], .565, white, body, False)
polygon('Badge cross vertical', [(.173,.66),(.187,.66),(.187,.60),(.173,.60)], .57, green, body, False)
polygon('Badge cross horizontal', [(.158,.627),(.202,.627),(.202,.639),(.158,.639)], .57, green, body, False)
for side in (-1, 1):
    for i in range(13):
        y = .04+i*.052
        x = side*(.20+.045*math.sin(i*.6))
        polygon(f'Kit print {side} {i}', oval(x,y,.012,.008), .555,
                green if i%3 else red, body, False)

# Reuse the whole-head silhouette method from build_advanced.py. The generated sheet
# has an RGB checker backdrop; keep its pixels intact and exclude only exterior mesh.
image = bpy.data.images.load(str(ASSETS / 'heads.png'))
image.pack()
W, H = image.size
pixels = np.asarray(image.pixels[:], dtype=np.float32).reshape(H,W,4)
headmat = bpy.data.materials.new('Reference / illustrated head sheet')
headmat.use_nodes = True
n = headmat.node_tree.nodes
n.clear()
output = n.new('ShaderNodeOutputMaterial')
emission = n.new('ShaderNodeEmission')
texture = n.new('ShaderNodeTexImage')
texture.image = image
headmat.node_tree.links.new(texture.outputs['Color'], emission.inputs['Color'])
headmat.node_tree.links.new(emission.outputs[0], output.inputs['Surface'])
heads = []
head_bounds = []
for row in range(2):
    for col in range(2):
        x0, x1 = col*W//2, (col+1)*W//2
        y0, y1 = (1-row)*H//2, (2-row)*H//2
        a = pixels[y0:y1,x0:x1,:3]
        hh, ww = a.shape[:2]
        background = (a.max(2)-a.min(2)<.13) & (a.mean(2)>.35)
        outside = np.zeros((hh,ww), bool)
        queue = deque([(0,x) for x in range(ww)]+[(hh-1,x) for x in range(ww)]
                      +[(y,0) for y in range(hh)]+[(y,ww-1) for y in range(hh)])
        while queue:
            y,x = queue.popleft()
            if not(0<=y<hh and 0<=x<ww) or outside[y,x] or not background[y,x]:
                continue
            outside[y,x] = True
            queue.extend(((y-1,x),(y+1,x),(y,x-1),(y,x+1)))
        inside = ~outside
        yy,xx = np.where(inside)
        xmin,xmax,ymin,ymax = int(xx.min()),int(xx.max()),int(yy.min()),int(yy.max())
        assert min(xmin,ww-1-xmax,ymin,hh-1-ymax)>8, 'Head touches cell boundary'
        assert .30 < inside.mean() < .8, 'Unexpected head/background separation'
        height = ymax-ymin+1
        scale = 1.42/height
        center = (xmin+xmax+1)/2
        vertices,faces,uvs = [],[],[]
        for y in range(ymin,ymax+1):
            edges = np.diff(np.r_[False,inside[y],False].astype(np.int8))
            for xa,xb in zip(np.where(edges==1)[0],np.where(edges==-1)[0]):
                i = len(vertices)
                coords = [(xa,y),(xb,y),(xb,y+1),(xa,y+1)]
                vertices.extend([((x-center)*scale,(v-ymin)*scale-.66,.80) for x,v in coords])
                faces.append((i,i+1,i+2,i+3))
                uvs.extend([((x0+x)/W,(y0+v)/H) for x,v in coords])
        mesh = bpy.data.meshes.new(f'Whole head drawing {row}-{col}')
        mesh.from_pydata(vertices,[],faces)
        mesh.materials.append(headmat)
        uv = mesh.uv_layers.new()
        for poly in mesh.polygons:
            for li in poly.loop_indices:
                uv.data[li].uv = uvs[mesh.loops[li].vertex_index]
        obj = bpy.data.objects.new(('Neutral','Effort','Surprise','Skeptical')[len(heads)]+' head', mesh)
        skin.objects.link(obj)
        obj.parent = head_control
        heads.append(obj)
        head_bounds.append({'cell':[row,col],'bbox':[xmin,ymin,xmax,ymax],
                            'mesh_vertices':len(vertices),'foreground_fraction':float(inside.mean())})

shot = json.loads((ROOT.parent / '001_heavy_box/shot-v005.json').read_text())
source_tree = ast.parse((ROOT.parent / '001_heavy_box/scripts/build_v005.py').read_text())
exec(compile(ast.Module(body=[n for n in source_tree.body if isinstance(n,ast.FunctionDef) and n.name=='sample'],type_ignores=[]),'existing-sample','exec'))
for f in range(1,241):
    squint,effort,surprise,suspicious = sample(shot['face'],f)
    selection = 2 if surprise>=.5 else 3 if suspicious>=.5 else 1 if effort>=.4 else 0
    for i,obj in enumerate(heads):
        obj.hide_render = obj.hide_viewport = i!=selection
        obj.keyframe_insert(data_path='hide_render',frame=f)
        obj.keyframe_insert(data_path='hide_viewport',frame=f)
scene['Character source'] = 'User supplied Ronny.jpg; stylized head and simplified reference kit.'
scene['Fiction'] = 'Character/motion experiment, not a claim that this real person pushed this box.'
scene['Representation'] = 'Live curve-driven 2D body, native kit details, four whole-head illustration replacements.'
scene['Review status'] = 'Small identity/movement proof for playback review.'
scene.frame_set(1)
head_names = [o.name for o in heads]
skin_name = skin.name
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / 'cartoon-skin.blend'))
bpy.ops.wm.open_mainfile(filepath=str(OUT / 'cartoon-skin.blend'))
scene = bpy.context.scene
checks = verify(baseline)
assert contact_geometry()==contact_baseline
assert digest(SOURCE)==source_hash
section_gap = 0
for f in range(1,241):
    scene.frame_set(f)
    assert sum(not bpy.data.objects[name].hide_render for name in head_names)==1
    for obj in bpy.data.collections[skin_name].objects:
        if obj.type=='CURVE' and obj.data.animation_data:
            assert all(d.driver.is_valid for d in obj.data.animation_data.drivers)
    graph = bpy.context.evaluated_depsgraph_get()
    for name, source_name, a, b in section_specs:
        src = bpy.data.objects[source_name].evaluated_get(graph).data.splines[0].bezier_points
        points = (src[0].co,src[0].handle_right,src[1].handle_left,src[1].co)
        segment = bpy.data.objects[name].evaluated_get(graph).data.splines[0].bezier_points
        for point, t in ((0,a),(1,b)):
            weights = ((1-t)**3,3*(1-t)**2*t,3*(1-t)*t*t,t**3)
            target = [sum(w*p[axis] for w,p in zip(weights,points)) for axis in range(2)]
            error = math.dist(segment[point].co[:2],target)
            section_gap = max(section_gap,error)
            assert error<1e-5, (f,name,error)
checks.update(source_preserved=True,source_sha256=source_hash,
              projected_hand_shoe_geometry='unchanged on all 240 frames',
              head_drawings=head_bounds,one_head_per_frame=True,max_clothing_section_error=section_gap,
              likeness='Generated from supplied reference; perceived likeness awaits user review')
(OUT / 'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
for f in (1,54,104,118,138,154,158,162,167,170,179,220):
    scene.frame_set(f)
    scene.render.filepath=str(OUT/f'pose-{f:03}.png')
    bpy.ops.render.render(write_still=True)
append_event(ROOT,stage='ronny-geometry-checks',status='passed',
    intent='Check identity artwork while preserving known motion and contacts',
    method='Reopened project, 240 controller/geometry frames and head visibility/driver checks',
    outputs=[str((OUT/n).relative_to(ROOT)) for n in ('cartoon-skin.blend','checks.json')],
    result='Original controls and hand/shoe geometry preserved. One head expression per frame. Technical checks do not establish visual likeness or final creative acceptance.')
print('RONNY_BUILD_COMPLETE',OUT,flush=True)
