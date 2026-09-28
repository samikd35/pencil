"""Same design/action as coherent-proof-v003, with native Grease Pencil character art."""
import argparse
import ast
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import time

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT/'artifacts/coherent-proof-v003/cartoon-skin.blend'
sys.path.insert(0, str(ROOT.parent/'001_heavy_box'))
from journal import append_event

parser = argparse.ArgumentParser()
parser.add_argument('--out', required=True)
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
assert Path(args.out).name == args.out
OUT = ROOT/'artifacts'/args.out
OUT.mkdir(exist_ok=False)
(OUT/'source-build_gp.py').write_bytes(Path(__file__).read_bytes())
started = time.monotonic()
names = {'digest', 'controllers'}
defs = [n for n in ast.parse((ROOT/'build_skin.py').read_text()).body
        if isinstance(n, ast.FunctionDef) and n.name in names]
exec(compile(ast.Module(body=defs,type_ignores=[]),str(ROOT/'build_skin.py'),'exec'))
source_hash = digest(SOURCE)
append_event(ROOT,stage='gp-comparison-build',status='started',
    intent='User-authorized comparison of native Grease Pencil and the current curve/mesh character',
    method='Same controls, native stroke/fill geometry, explicit point drivers and native face animation',
    inputs=['build_gp.py','artifacts/coherent-proof-v003/cartoon-skin.blend'],
    result='Small same-design, same-action proof. Existing camera, staging and soundtrack retained. No full-quality new film or likeness redesign.')
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene = bpy.context.scene
_, baseline = controllers()
scene.frame_set(1)
art_collections = {'Cartoon surface / same stickman controls','Unified body fills','Flat native face'}
sources = [o for o in bpy.data.objects if
    any(c.name in art_collections for c in o.users_collection) or
    re.fullmatch(r'(Arm|Leg|Mitten|Shoe)_(far|near)(_outline)?',o.name)]
assert sources and all(o.type in {'MESH','CURVE','FONT'} for o in sources)
source_names = [o.name for o in sources]
animated_polys = []
limb_tests = []
mapping = {}
materials = {}


def gp_material(source, fill):
    key = (source.name,fill)
    if key not in materials:
        mat = bpy.data.materials.new('GP / '+source.name+(' fill' if fill else ' ink'))
        bpy.data.materials.create_gpencil_data(mat)
        mat.grease_pencil.show_fill = fill
        mat.grease_pencil.show_stroke = not fill
        mat.grease_pencil.fill_color = source.diffuse_color
        mat.grease_pencil.color = source.diffuse_color
        materials[key] = mat
    return materials[key]


def point_path(index):
    return f'layers[0].frames[0].drawing.attributes["position"].data[{index}].vector'


def add_stroke(obj, points, source_material, fill=False, cyclic=False, radius=.01):
    drawing = obj.data.layers[0].frames[0].drawing
    index = len(drawing.attributes['position'].data) if drawing.attributes.get('position') else 0
    drawing.add_strokes([len(points)])
    stroke = drawing.strokes[-1]
    stroke.cyclic = cyclic
    stroke.fill_id = 1 if fill else 0
    stroke.fill_opacity = 1
    stroke.hide_stroke = fill
    # Flat ends match the existing beveled-curve sections. Hands/feet cover limb ends.
    stroke.start_cap = stroke.end_cap = 1
    mat = gp_material(source_material,fill)
    obj.data.materials.append(mat)
    stroke.material_index = len(obj.data.materials)-1
    for p,co in zip(stroke.points,points):
        p.position = co
        p.radius = radius
        p.opacity = 1
    return index


def transform_driver(data, point, axis, targets, expression):
    driver = data.driver_add(point_path(point),axis).driver
    for name,target in targets:
        v=driver.variables.new();v.name=name;v.type='TRANSFORMS'
        v.targets[0].id=bpy.data.objects[target]
        v.targets[0].transform_type='LOC_'+'XYZ'[axis]
        v.targets[0].transform_space='WORLD_SPACE'
    driver.expression=expression


def font_boundaries(source):
    evaluated=source.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh=evaluated.to_mesh()
    # The supplied 7 has one simple contour and no counters. Weld tessellated glyph vertices.
    coords=[];weld={};indices={}
    for v in mesh.vertices:
        key=tuple(round(x,7) for x in v.co)
        if key not in weld:weld[key]=len(coords);coords.append(tuple(v.co))
        indices[v.index]=weld[key]
    counts=Counter(tuple(sorted((indices[a],indices[b]))) for p in mesh.polygons for a,b in p.edge_keys)
    edges={edge for edge,count in counts.items() if count==1}
    loops=[]
    while edges:
        a,b=edges.pop();loop=[a,b]
        while loop[-1]!=loop[0]:
            edge=next(e for e in edges if loop[-1] in e)
            edges.remove(edge);loop.append(edge[1] if edge[0]==loop[-1] else edge[0])
        loops.append([coords[i] for i in loop[:-1]])
    evaluated.to_mesh_clear()
    assert len(loops)==1,'The comparison only contains the single-contour digit 7'
    return loops


for source in sources:
    data=bpy.data.grease_pencils.new('GP / '+source.name)
    data.stroke_depth_order='3D'
    layer=data.layers.new(source.name,set_active=True);layer.use_lights=False;layer.frames.new(1)
    obj=bpy.data.objects.new('GP / '+source.name,data)
    for collection in source.users_collection:collection.objects.link(obj)
    obj.use_grease_pencil_lights=False
    obj.parent=source.parent
    obj.matrix_parent_inverse=source.matrix_parent_inverse.copy()
    obj.matrix_basis=source.matrix_basis.copy()
    obj.hide_render=source.hide_render;obj.hide_viewport=source.hide_viewport
    if source.animation_data and source.animation_data.action:
        obj.animation_data_create().action=source.animation_data.action
        obj.animation_data.action_slot=source.animation_data.action_slot
    obj['Source design part']=source.name
    mapping[source.name]=obj.name
    if source.type=='MESH':
        for poly in source.data.polygons:
            add_stroke(obj,[tuple(source.data.vertices[i].co) for i in poly.vertices],
                source.data.materials[poly.material_index],True,True)
    elif source.type=='FONT':
        for points in font_boundaries(source):add_stroke(obj,points,source.data.materials[0],True,True)
    else:
        assert len(source.data.splines)==1
        spline=source.data.splines[0]
        if spline.type=='POLY':
            add_stroke(obj,[tuple(p.co[:3]) for p in spline.points],source.data.materials[0],
                cyclic=spline.use_cyclic_u,radius=source.data.bevel_depth)
            if source.data.animation_data:
                if source.data.animation_data.action:animated_polys.append((source.name,obj.name))
                for fc in source.data.animation_data.drivers:
                    match=re.fullmatch(r'splines\[0\].points\[(\d+)\].co',fc.data_path)
                    assert match and fc.array_index<3
                    targets=[(v.name,v.targets[0].id.name) for v in fc.driver.variables]
                    assert all(v.type=='TRANSFORMS' for v in fc.driver.variables)
                    transform_driver(data,int(match[1]),fc.array_index,targets,fc.driver.expression)
        else:
            assert spline.type=='BEZIER' and len(spline.bezier_points)==2
            if source.name.startswith(('Arm_','Leg_')):
                part,side=source.name.split()[0].split('_');a,b=0,1
            elif source.name.startswith('Shorts fill '):part,side='Leg',source.name.split()[-1];a,b=0,.34
            elif source.name.startswith('White socks '):part,side='Leg',source.name.split()[-1];a,b=.73,1
            elif source.name=='Captain band':part,side='Arm','near';a,b=.19,.36
            else:raise AssertionError(source.name)
            start=('ATTACH_Shoulder_' if part=='Arm' else 'ATTACH_Hip_')+side
            bend=('CTRL_Elbow_' if part=='Arm' else 'CTRL_Knee_')+side
            end=('CTRL_Hand_' if part=='Arm' else 'CTRL_Foot_')+side
            count=65
            z=spline.bezier_points[0].co.z
            add_stroke(obj,[(0,0,z)]*count,source.data.materials[0],radius=source.data.bevel_depth)
            for i in range(count):
                t=a+(b-a)*i/(count-1)
                w0=(1-t)**3+.3*(1-t)**2*t
                w1=2.7*((1-t)**2*t+(1-t)*t*t)
                w2=.3*(1-t)*t*t+t**3
                for axis in range(2):
                    transform_driver(data,i,axis,[('s',start),('b',bend),('e',end)],
                        f'{w0:.15g}*s+{w1:.15g}*b+{w2:.15g}*e')
            limb_tests.append((source.name,obj.name,a,b))

# Facial point animation lives in the GP datablocks; rigid artwork follows the same parents.
for frame in range(1,241):
    scene.frame_set(frame);bpy.context.view_layer.update()
    for source_name,gp_name in animated_polys:
        source=bpy.data.objects[source_name];data=bpy.data.objects[gp_name].data
        positions=data.layers[0].frames[0].drawing.attributes['position'].data
        for i,p in enumerate(source.data.splines[0].points):
            positions[i].vector=p.co[:3]
            for axis in range(2):data.keyframe_insert(data_path=point_path(i),index=axis,frame=frame)

# Keep the input artwork as an explicitly hidden archive, with no GP driver dependency on it.
archive=bpy.data.collections.new('Curve mesh comparison archive')
scene.collection.children.link(archive);archive.hide_render=archive.hide_viewport=True
for source in sources:
    for collection in list(source.users_collection):collection.objects.unlink(source)
    archive.objects.link(source)
scene.frame_set(1)
scene['Character construction']='Native Grease Pencil strokes/fills. Direct point drivers from the original controls. Native GP facial F-curves. No body-frame bake or Python playback handler.'
scene['Review status']='Small native GP comparison candidate; awaiting visual playback review.'
scene.render.resolution_percentage=50
scene.eevee.taa_render_samples=16
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'cartoon-skin.blend'))
build_seconds=time.monotonic()-started
bpy.ops.wm.open_mainfile(filepath=str(OUT/'cartoon-skin.blend'))
scene=bpy.context.scene
assert controllers()[1]==baseline

# Compare GP centreline samples to the independently evaluated original Bezier curves.
max_gap=0
max_contact=0
for frame in range(1,241):
    scene.frame_set(frame);bpy.context.view_layer.update()
    graph=bpy.context.evaluated_depsgraph_get()
    for source_name,gp_name,a,b in limb_tests:
        source=bpy.data.objects[source_name]
        controls=source.data.splines[0].bezier_points
        cp=[controls[0].co,controls[0].handle_right,controls[1].handle_left,controls[1].co]
        obj=bpy.data.objects[gp_name];evaluated=obj.evaluated_get(graph)
        points=evaluated.data.layers[0].current_frame().drawing.strokes[0].points
        for i,p in enumerate(points):
            t=i/(len(points)-1)
            expected=sum((co*w for co,w in zip(cp,((1-t)**3,3*(1-t)**2*t,3*(1-t)*t*t,t**3))),Vector())
            error=math.dist((source.matrix_world@expected)[:2],(obj.matrix_world@p.position)[:2])
            max_gap=max(max_gap,error)
            assert error<1e-5,(frame,source_name,i,error)
        assert all(fc.driver.is_valid for fc in obj.data.animation_data.drivers)
    for source_name in ('Mitten_far','Mitten_near','Shoe_far','Shoe_near'):
        source=bpy.data.objects[source_name];obj=bpy.data.objects[mapping[source_name]]
        points=obj.evaluated_get(graph).data.layers[0].current_frame().drawing.strokes[0].points
        assert len(points)==len(source.data.vertices)
        for p,v in zip(points,source.data.vertices):
            error=math.dist((obj.matrix_world@p.position)[:2],(source.matrix_world@v.co)[:2])
            max_contact=max(max_contact,error);assert error<1e-6

# A real off-key edit in the reopened scene must move GP sleeve and mitten together.
scene.frame_set(110)
hand=bpy.data.objects['CTRL_Hand_near'];original=hand.location.copy();hand.location.x+=.2
bpy.context.view_layer.update()
obj=bpy.data.objects[mapping['Arm_near fill']]
tip=obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.layers[0].current_frame().drawing.strokes[0].points[-1].position
assert math.dist((obj.matrix_world@tip)[:2],hand.matrix_world.translation[:2])<1e-5
assert bpy.data.objects[mapping['Mitten_near']].parent==hand
hand.location=original;scene.frame_set(1)
assert digest(SOURCE)==source_hash
assert all(bpy.data.objects[name].type=='GREASEPENCIL' for name in mapping.values())
for name in mapping.values():
    data=bpy.data.objects[name].data
    if data.animation_data:
        for fc in data.animation_data.drivers:
            assert all(v.targets[0].id.type=='EMPTY' for v in fc.driver.variables)
checks={'status':'passed','blender':bpy.app.version_string,'frames':240,'controllers':12,
    'original_control_frames_identical':True,'native_gp_character_objects':len(mapping),
    'max_centreline_sample_gap':max_gap,'max_projected_hand_shoe_gap':max_contact,
    'saved_project_hand_edit':'passed','gp_drivers_reference_only_controls':True,
    'body_motion_baked':False,'python_playback_handlers_added':False,
    'source_unchanged':True,'build_seconds':build_seconds,'part_mapping':mapping,
    'limits':'Same view and source design. Curve sampling, cap shapes, antialiasing and draw ordering still require visual comparison. The shared waist compositor remains in use.'}
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
for frame in (1,54,104,118,138,154,158,162,167,170,179,220):
    scene.frame_set(frame);scene.render.filepath=str(OUT/f'pose-{frame:03}.png');bpy.ops.render.render(write_still=True)
append_event(ROOT,stage='gp-native-checks',status='passed',intent='Verify native GP motion and saved editability',
    method='240-frame control/centreline/contact comparison and a temporary hand edit after reopening',
    outputs=[str((OUT/n).relative_to(ROOT)) for n in ('cartoon-skin.blend','checks.json')],
    result='All visible character parts are native GP. Original control motion and contact contours match within stated tolerance. No GP driver refers to source artwork. Pose renders await visual inspection.')
print('GP_BUILD_COMPLETE',json.dumps({k:v for k,v in checks.items() if k!='part_mapping'}),flush=True)
