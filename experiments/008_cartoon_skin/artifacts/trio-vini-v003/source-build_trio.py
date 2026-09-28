"""Three reference caricatures on the saved curve/mesh box-action controls."""
import argparse
import ast
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

import bpy

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT/'artifacts/coherent-proof-v003/cartoon-skin.blend'
ASSETS = ROOT/'assets/trio-v003'
parser = argparse.ArgumentParser()
parser.add_argument('--character', choices=['jude', 'mbappe', 'vini'], required=True)
parser.add_argument('--out', required=True)
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
assert Path(args.out).name == args.out
OUT = ROOT/'artifacts'/args.out
OUT.mkdir(exist_ok=False)
(OUT/'source-build_trio.py').write_bytes(Path(__file__).read_bytes())
cfg = json.loads((ASSETS/'characters.json').read_text())[args.character]
sys.path.insert(0, str(ROOT.parent/'001_heavy_box'))
from journal import append_event

for file, names in [
    (ROOT/'build_skin.py', {'digest','controllers','contact_geometry','material','polygon','oval','verify'}),
    (ROOT/'build_ronny.py', {'assign','curve_section'}),
    (ROOT/'build_coherent.py', {'anchor','line','live_line'}),
    (ROOT.parent/'001_heavy_box/scripts/build_v005.py', {'smooth_closed','driver'}),
]:
    definitions = [n for n in ast.parse(file.read_text()).body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert len(definitions) == len(names)
    exec(compile(ast.Module(body=definitions, type_ignores=[]), str(file), 'exec'))


def svg_splines(data, transform, convert):
    """Read the absolute M/C/L/Z subset emitted by this VTracer invocation."""
    tokens = re.findall(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?', data)
    assert set(t for t in tokens if t.isalpha()) <= {'M','C','L','Z'}
    numbers = re.findall(r'[-+]?(?:\d*\.\d+|\d+)', transform)
    assert transform.startswith('translate(') and len(numbers) == 2
    tx, ty = map(float, numbers)
    i = 0
    paths = []
    points = []
    def xy():
        nonlocal i
        x,y = map(float, tokens[i:i+2]); i += 2
        return convert(x+tx, y+ty)
    while i < len(tokens):
        command = tokens[i]; i += 1
        if command == 'M':
            assert not points
            p = xy(); points = [[p,p,p]]
        elif command == 'C':
            a,b,p = xy(),xy(),xy()
            points[-1][2] = a
            points.append([p,b,p])
        elif command == 'L':
            p = xy(); points.append([p,p,p])
        else:
            assert command == 'Z' and len(points) >= 3
            if math.dist(points[-1][0], points[0][0]) < 1e-7:
                points[0][1] = points.pop()[1]
            paths.append(points); points = []
    assert not points and paths
    return paths


# Small runnable parser check also covers multi-contour paths and a closing cubic.
probe = svg_splines('M0 0 L1 0 C1 1 0 1 0 0 Z M2 2 L3 2 L2 3 Z',
                    'translate(4,5)', lambda x,y:(x,y,0))
assert len(probe)==2 and probe[0][0][1]==(4.,6.,0) and len(probe[0])==2

source_hash = digest(SOURCE)
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene = bpy.context.scene
_, baseline = controllers()
contact_baseline = contact_geometry()
controls = bpy.data.collections['Pose controls • keyed and editable']
body_art = bpy.data.collections['Unified body fills']
face_art = bpy.data.collections['Flat native face']
surface = bpy.data.collections['Cartoon surface / same stickman controls']
for collection in (body_art, face_art):
    for obj in list(collection.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
bpy.data.objects.remove(bpy.data.objects['Captain band'], do_unlink=True)
ink = material('Trio / warm ink', '#3b1917')
white = material('Trio / white kit', '#fcfefd')
skin_color = material('Trio / skin', '#b77d62' if args.character=='jude' else cfg['skin'])
green = material('Trio / collar', '#327e68')
red = material('Trio / stripes', '#cc4559')
gold = material('Trio / gold', '#edbb43')
blue = material('Trio / badge', '#214572')
boot = material('Trio / boots', cfg['boot'])
section_specs = []

# Retarget artwork proportions through derived controls; source animation stays intact.
source_body = bpy.data.objects['CTRL_Body']
body = anchor('ATTACH_CharacterBody', None, (0,0,0))
for axis,letter in enumerate('XY'):
    targets=[('a',source_body,letter)]
    expression='a' if axis==0 else f'a*{cfg["hip_y"]}'
    if axis==1 and args.character=='vini':
        targets += [('f',bpy.data.objects['CTRL_Foot_far'],'Y'),('g',bpy.data.objects['CTRL_Foot_near'],'Y')]
        # Keep the compact pelvis above both feet when the original action leans or hops.
        expression=f'max(a*{cfg["hip_y"]},max(f,g)+0.72)'
    driver(body,'location',axis,targets,expression)
rotation = body.constraints.new('COPY_ROTATION'); rotation.target = source_body
h,w = cfg['torso_height'], cfg['body_width']
head_base = anchor('ATTACH_JawPosition', body, (0,h+cfg['neck'],0))
head = anchor('ATTACH_CharacterHead', None, (0,0,0))
location = head.constraints.new('COPY_LOCATION'); location.target = head_base
rotation = head.constraints.new('COPY_ROTATION'); rotation.target = bpy.data.objects['CTRL_Head']
arm_radius = {'jude':.066,'mbappe':.082,'vini':.103}[args.character]
leg_radius = {'jude':.083,'mbappe':.095,'vini':.116}[args.character]
for side,sign in (('far',-1),('near',1)):
    hip = bpy.data.objects['ATTACH_Hip_'+side]
    hip.parent = body; hip.location = (sign*w*.58,-.11,0)
    shoulder = bpy.data.objects['ATTACH_Shoulder_'+side]
    shoulder.parent = body; shoulder.location = (sign*w*.72,h-.13,0)
    for part,target,old_start,bend_name,radius in (
        ('Arm',shoulder,bpy.data.objects['ANCHOR_Shoulder'],'Elbow',arm_radius),
        ('Leg',hip,source_body,'Knee',leg_radius),
    ):
        bend = anchor('ATTACH_'+bend_name+'_'+side,None,(0,0,0))
        for axis,letter in enumerate('XY'):
            driver(bend,'location',axis,[('a',bpy.data.objects['CTRL_'+bend_name+'_'+side],letter),
                ('b',target,letter),('c',old_start,letter)], 'a+(b-c)*0.5')
        for suffix in ('',' fill'):
            obj = bpy.data.objects[part+'_'+side+suffix]
            obj.data.bevel_depth = radius+(.016 if not suffix else 0)
            assign(obj.name,ink if not suffix else skin_color)
            for fc in obj.data.animation_data.drivers:
                for variable in fc.driver.variables:
                    if variable.name=='b': variable.targets[0].id = bend
    assign('Mitten_'+side,skin_color)
    assign('Mitten_'+side+'_outline',ink)
    assign('Shoe_'+side,boot)
    assign('Shoe_'+side+'_outline',ink)
    bpy.data.objects['White socks '+side].data.bevel_depth = leg_radius+.005
    assign('White socks '+side,white)

skin = body_art
polygon('Continuous shirt and hips',smooth_closed([
    (-w*.32,h), (w*.32,h), (w*.78,h-.13), (w,h*.55),
    (w,-.09),(w*.68,-.27),(0,-.31),(-w*.68,-.27),(-w,-.09),(-w,h*.55),(-w*.78,h-.13)
]),.50,white,body,False)
for side in ('far','near'):
    curve_section('Continuous shorts '+side,bpy.data.objects['Leg_'+side],0,.34,
                  leg_radius+.044,white,.045)
    curve_section('Short sleeve '+side,bpy.data.objects['Arm_'+side],0,.38,
                  arm_radius+.028,white,.045)
lower = anchor('ATTACH_NewNeckBase',body,(0,h-.05,0))
upper = anchor('ATTACH_NewNeckTop',head,(0,.25 if args.character=='jude' else .12,0))
neck_width = {'jude':.27,'mbappe':.55,'vini':.31}[args.character]
live_line('Continuous neck',lower,upper,.18,neck_width,skin_color)
polygon('Green collar',smooth_closed([(-neck_width*.62,h+.025),(neck_width*.62,h+.025),
    (neck_width*.56,h-.10),(0,h-.14),(-neck_width*.56,h-.10)]),.55,green,body,False)
for side in (-1,1):
    for stripe in range(3):
        x=side*(w*.44+stripe*.055)
        line(f'Shoulder stripe {side} {stripe}',[(x,h-.07),(x+side*.07,h-.18),(x+side*.08,h-.30)],
             .565,red,body,width=.019)
polygon('Crest rim',oval(w*.44,h*.53,.073,.094),.57,gold,body,False)
polygon('Crest center',oval(w*.44,h*.53,.047,.066),.575,blue,body,False)
line('Crest slash',[(w*.44-.03,h*.53-.045),(w*.44+.03,h*.53+.045)],.58,white,body,width=.020)
polygon('Crest crown',[(w*.44-.06,h*.53+.09),(w*.44-.07,h*.53+.13),
    (w*.44-.02,h*.53+.12),(w*.44,h*.53+.15),(w*.44+.02,h*.53+.12),
    (w*.44+.07,h*.53+.13),(w*.44+.06,h*.53+.09)],.58,gold,body,False)
for j in range(3):
    x=-w*.52+j*.035
    line('Chest mark '+str(j),[(x,h*.49),(x-.045,h*.51+j*.03)],.57,green,body,width=.022)
font=bpy.data.curves.new('Sponsor lettering','FONT');font.body='Emirates\nFLY BETTER'
font.size=.105 if args.character=='jude' else .13;font.align_x='CENTER';font.space_line=.85
font.materials.append(green)
obj=bpy.data.objects.new('Sponsor lettering',font);body_art.objects.link(obj);obj.parent=body
obj.location=(0,h*.30,.57)
if args.character=='mbappe':
    purple=material('Trio / ceremonial sash','#6c538e')
    polygon('Reference ceremonial sash',[(-w*.83,.04),(-w*.55,-.05),(w*.80,h-.2),(w*.58,h-.1)],.59,purple,body,False)
    for j in range(3):
        x=-.10+j*.1; y=h*.65
        polygon('Medal ribbon '+str(j),[(x-.025,y),(x+.025,y),(x+.025,y-.08),(x-.025,y-.08)],.60,red,body,False)
        polygon('Medal '+str(j),oval(x,y-.10,.034,.038),.605,gold,body,False)

# Native filled Bezier regions share the drawing's color/outline language with the body.
skin=face_art
def reference_point(x,y):
    return ((x-cfg['anchor'][0])/cfg['pixels_per_unit'],
            -(y-cfg['anchor'][1])/cfg['pixels_per_unit'],0)
def svg_point(x,y):
    return reference_point(x/3+cfg['crop'][0],y/3+cfg['crop'][1])
paths=list(ET.parse(ASSETS/(args.character+'.svg')).getroot())
for index,path in enumerate(paths):
    name=f'{cfg["label"]} / face region {index:02}'
    data=bpy.data.curves.new(name,'CURVE');data.dimensions='2D';data.fill_mode='BOTH';data.resolution_u=5
    for points in svg_splines(path.get('d'),path.get('transform'),svg_point):
        spline=data.splines.new('BEZIER');spline.bezier_points.add(len(points)-1);spline.use_cyclic_u=True
        for bp,(p,a,b) in zip(spline.bezier_points,points):
            bp.handle_left_type=bp.handle_right_type='FREE';bp.co=p;bp.handle_left=a;bp.handle_right=b
    data.materials.append(material(name,path.get('fill')))
    obj=bpy.data.objects.new(name,data);face_art.objects.link(obj);obj.parent=head;obj.location.z=.82+index*.0005

# ponytail: reference-angle heads; authored turn drawings are needed before head rotation in 3D.
for layer in scene.view_layers:
    for child in layer.layer_collection.children:
        if child.name in (body_art.name,face_art.name):
            child.exclude=child.name != {'Unified body':body_art.name,'Face':face_art.name}.get(layer.name)
for node in scene.compositing_node_group.nodes:
    if node.type=='SETALPHA': node.inputs[0].default_value=ink.diffuse_color
scene['Character']=cfg['label']
scene['Reference']='User-supplied three-player cartoon; user supplied identities. Native vector reconstruction.'
scene['Construction']='Curve/mesh body, continuous limbs and unioned waist, native filled Bezier face regions. No head image texture.'
scene['Review status']='Short fictional box-action experiment awaiting user review; not a canonical character approval.'
scene.render.resolution_percentage=50
scene.eevee.taa_render_samples=16
scene.frame_set(1)
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'cartoon-skin.blend'))
bpy.ops.wm.open_mainfile(filepath=str(OUT/'cartoon-skin.blend'))
scene=bpy.context.scene
checks=verify(baseline)
assert contact_geometry()==contact_baseline
assert digest(SOURCE)==source_hash
checks.update(character=cfg['label'],source_preserved=True,source_sha256=source_hash,
    projected_hand_foot_geometry='Identical across all 240 frames',native_face_regions=len(paths),
    limits='Reference-view head moves as a unit. Expression swaps and turns are not implemented. Numerical checks do not establish likeness or all overlaps.')
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
for frame in (1,54,118,138,154,162,170,179,220):
    scene.frame_set(frame);scene.render.filepath=str(OUT/f'pose-{frame:03}.png')
    bpy.ops.render.render(write_still=True)
append_event(ROOT,stage='trio-native-motion-check',status='passed',intent='Test '+cfg['label']+' in the current curve/mesh workflow',
    method='Saved/reopened all-frame control and contact checks, live hand edit, sampled pose renders',
    inputs=['build_trio.py','assets/trio-v003/characters.json'],
    outputs=[str((OUT/n).relative_to(ROOT)) for n in ('cartoon-skin.blend','checks.json','pose-001.png','pose-118.png','pose-162.png')],
    result='240 original control frames and projected hand/foot contours match. Native face and altered body proportions built; creative motion review remains pending.')
print('TRIO_BUILD_COMPLETE',OUT,flush=True)
