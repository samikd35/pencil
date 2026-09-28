"""A flat native character and one live torso/shorts silhouette on the proven controls."""
import argparse
import ast
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'artifacts/proof-v002/cartoon-skin.blend'
sys.path.insert(0, str(ROOT.parent / '001_heavy_box'))
from journal import append_event

parser = argparse.ArgumentParser()
parser.add_argument('--out', required=True)
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
assert Path(args.out).name == args.out
OUT = ROOT / 'artifacts' / args.out
OUT.mkdir(parents=True, exist_ok=False)
(OUT/'source-build_coherent.py').write_bytes(Path(__file__).read_bytes())

# Import only known helper definitions, without executing the historical build scripts.
for file, names in [
    (ROOT/'build_skin.py', {'digest','controllers','contact_geometry','material','polygon','oval','verify'}),
    (ROOT/'build_ronny.py', {'assign','curve_section'}),
    (ROOT.parent/'001_heavy_box/scripts/build_v005.py', {'sample','smooth_closed','driver','points_key'}),
]:
    definitions = [n for n in ast.parse(file.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert len(definitions)==len(names)
    exec(compile(ast.Module(body=definitions,type_ignores=[]),str(file),'exec'))

append_event(ROOT,stage='coherent-character-build',status='started',
    intent='Implement the user-authorized simplified whole-character design and seamless waist test',
    method='Native face shapes, existing live curve controls, one composited body silhouette',
    inputs=['build_coherent.py','build_skin.py','build_ronny.py','assets/ronny-v001/reference.jpg'],
    result='User said Ok Do it after the research recommendation. Small pose/motion proof with existing sound; no new final-quality film authorization inferred.')
source_hash = digest(SOURCE)
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene = bpy.context.scene
_, baseline = controllers()
baseline_contacts = contact_geometry()
section_specs = []
ink = material('Unified ink','#25394c')
white = material('Unified kit','#f6f5ed')
skin_color = material('Flat skin','#e8aa7d')
hair_color = material('Flat hair','#202c34')
red = material('Badge red','#ba4550')
green = material('Badge green','#337a65')
navy = material('Band navy','#253e58')
body = bpy.data.objects['CTRL_Body']
head = bpy.data.objects['CTRL_Head']
controls = bpy.data.collections['Pose controls • keyed and editable']
body_art = bpy.data.collections.new('Unified body fills')
face_art = bpy.data.collections.new('Flat native face')
scene.collection.children.link(body_art)
scene.collection.children.link(face_art)


def anchor(name,parent,location):
    obj = bpy.data.objects.new(name,None)
    controls.objects.link(obj)
    obj.parent = parent
    obj.location = location
    return obj


def line(name,points,z,mat,parent=None,width=.026):
    data = bpy.data.curves.new(name,'CURVE')
    data.dimensions = '3D'
    data.bevel_depth = width/2
    data.bevel_resolution = 3
    spline = data.splines.new('POLY')
    spline.points.add(len(points)-1)
    for point,xy in zip(spline.points,points):
        point.co = (*xy,z,1)
    data.materials.append(mat)
    obj = bpy.data.objects.new(name,data)
    skin.objects.link(obj)
    obj.parent = parent
    return obj


def live_line(name,start,end,z,width,mat):
    obj = line(name,[(0,0),(0,0)],z,mat,width=width)
    for i,target in enumerate((start,end)):
        for axis,letter in enumerate('XY'):
            driver(obj.data,f'splines[0].points[{i}].co',axis,[('a',target,letter)],'a')
    return obj


# Remove the previous visible construction; keep its controllers and source artwork archived.
for obj in bpy.data.objects:
    if obj.parent==head or obj.name in ('Bean torso','Full shirt','Full shirt outline',
            'Trouser waist','Trouser waist outline','Collar','Collar outline','Chest patch'):
        obj.hide_render = obj.hide_viewport = True

# Derived attachment widths need no new animation tracks. Hand/foot targets remain unchanged.
for side,sign in (('far',-1),('near',1)):
    hip = anchor('ATTACH_Hip_'+side,body,(sign*.14,-.13,0))
    shoulder = anchor('ATTACH_Shoulder_'+side,body,(sign*.15,.74,0))
    for part,target,radius,mat in (('Leg',hip,.105,skin_color),('Arm',shoulder,.085,white)):
        for suffix in ('',' fill'):
            obj = bpy.data.objects[part+'_'+side+suffix]
            obj.data.bevel_depth = radius+(.018 if not suffix else 0)
            assign(obj.name,ink if not suffix else mat)
            for fc in obj.data.animation_data.drivers:
                if 'bezier_points[0]' in fc.data_path:
                    for v in fc.driver.variables:
                        if v.name=='a':
                            v.targets[0].id = target
    assign('Mitten_'+side,skin_color)
    assign('Shoe_'+side,hair_color)

# All torso/hip/shorts fills are composited together before their external border is drawn.
# No part-level waist rectangle, shorts-top cap or horizontal shirt outline is visible.
skin = body_art
torso_points = smooth_closed([(-.10,.91),(.10,.91),(.23,.74),(.27,.40),
    (.28,-.11),(.23,-.27),(0,-.32),(-.23,-.27),(-.28,-.11),(-.26,.40),(-.23,.74)])
polygon('Torso and hip fill',torso_points,.50,white,body,False)
for side in ('far','near'):
    curve_section('Shorts fill '+side,bpy.data.objects['Leg_'+side],0,.34,.14,white,.045)
lower_neck = anchor('ATTACH_Neck_body',body,(0,.82,0))
upper_neck = anchor('ATTACH_Neck_head',head,(0,-.48,0))
live_line('Neck fill',lower_neck,upper_neck,.44,.20,skin_color)
polygon('Dark collar',[(-.11,.88),(.11,.88),(.08,.77),(-.02,.73),(-.09,.80)],.54,ink,body,False)
font = bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf')
data = bpy.data.curves.new('Number 7','FONT')
data.body='7';data.font=font;data.size=.44;data.align_x='CENTER';data.align_y='CENTER'
data.materials.append(ink)
obj=bpy.data.objects.new('Number 7',data);body_art.objects.link(obj);obj.parent=body
obj.location=(0,.35,.57)
polygon('Small kit badge',[(.12,.68),(.22,.68),(.22,.59),(.17,.55),(.12,.59)],.56,red,body,False)
polygon('Badge stripe',[(.145,.66),(.19,.66),(.19,.59),(.145,.59)],.57,green,body,False)

# Socks and arm band keep the same live curve-section method, outside the unified waist pass.
skin = bpy.data.collections['Cartoon surface / same stickman controls']
for side in ('far','near'):
    curve_section('White socks '+side,bpy.data.objects['Leg_'+side],.73,1,.105,white,.055)
curve_section('Captain band',bpy.data.objects['Arm_near'],.19,.36,.090,navy,.05)

# One modest native cartoon head: solid hair, angular jaw, brows, eyes and a simple nose.
skin = face_art
polygon('Left ear',oval(-.37,-.055,.13,.18),.78,skin_color,head)
polygon('Right ear',oval(.39,-.035,.075,.145),.78,skin_color,head)
face_points = smooth_closed([(-.37,.30),(-.29,.48),(-.06,.55),(.24,.50),(.38,.31),
    (.39,.04),(.37,-.29),(.24,-.48),(.02,-.56),(-.22,-.49),(-.34,-.27)])
polygon('Flat face',face_points,.80,skin_color,head)
hair_points = smooth_closed([(-.36,.17),(-.40,.37),(-.30,.55),(-.07,.64),(.22,.59),
    (.34,.46),(.36,.31),(.23,.37),(.06,.41),(-.14,.39),(-.26,.28),(-.30,.09)])
polygon('Hair silhouette',hair_points,.84,hair_color,head)
line('Ear accent',[(-.43,.01),(-.46,.035),(-.46,-.075),(-.40,-.10)],.83,ink,head,width=.018)
line('Simple nose',[(.115,.05),(.10,-.105),(.225,-.15),(.265,-.105)],.855,ink,head,width=.024)
eyes=[];pupils=[];brows=[]
for i,x in enumerate((-.13,.245)):
    eye=polygon('Eye white '+str(i),oval(0,0,.09,.071),.851,white,head,False)
    eye.location=(x,.075,0);eyes.append(eye)
    pupil=polygon('Pupil '+str(i),oval(0,0,.032,.050),.859,ink,head,False)
    pupil.location=(x+.020,.072,0);pupils.append(pupil)
    brows.append(line('Brow '+str(i),[(0,0)]*9,.865,ink,head,width=.050))
mouth=line('Expressive mouth',[(0,0)]*17,.865,ink,head,width=.026)
teeth=polygon('Effort mouth',smooth_closed([(-.075,-.30),(.18,-.28),(.22,-.38),(-.07,-.40)]),.868,white,head)
teeth_line=line('Teeth line',[(-.05,-.35),(.19,-.34)],.89,ink,head,width=.018)
open_mouth=polygon('Surprised mouth',oval(.085,-.34,.081,.115),.868,ink,head,False)
for obj in face_art.objects:
    if obj.type=='CURVE' and obj.name.endswith(' outline'):
        obj.data.bevel_depth=.012
shot=json.loads((ROOT.parent/'001_heavy_box/shot-v005.json').read_text())
for f in range(1,241):
    squint,effort,surprise,suspicious=sample(shot['face'],f)
    for i,(eye,pupil,brow) in enumerate(zip(eyes,pupils,brows)):
        blink=max(0,1-abs(f-207)/2) if 205<=f<=209 else 0
        sy=max(.12,(1-.66*squint)*(1-.90*blink))
        eye.scale.y=pupil.scale.y=sy
        eye.keyframe_insert(data_path='scale',frame=f);pupil.keyframe_insert(data_path='scale',frame=f)
        x=(-.22,.155)[i]
        points=[]
        for j in range(9):
            t=j/8
            y=.235+.03*math.sin(math.pi*t)+surprise*.075
            y+=effort*.060*((1-2*t) if i==0 else (2*t-1))
            y+=suspicious*(.07 if i==0 else -.045)
            points.append((x+.18*t,y))
        points_key(brow,points,f)
    points_key(mouth,[(-.05+.27*j/16,-.34-.035*math.sin(math.pi*j/16)*(1-2*effort)+suspicious*.055*j/16) for j in range(17)],f)
    for obj,on in ((mouth,surprise<.5 and effort<.5),(teeth,effort>=.5 and surprise<.5),
                   (teeth_line,effort>=.5 and surprise<.5),(open_mouth,surprise>=.5)):
        obj.hide_render=obj.hide_viewport=not on
        obj.keyframe_insert(data_path='hide_render',frame=f)
        obj.keyframe_insert(data_path='hide_viewport',frame=f)

# Native compositor unions the body alpha live. Internal overlap never becomes an ink seam.
# ponytail: fixed-view body grouping; changing arm/body depth order needs a separate occlusion review.
scene.render.film_transparent=True
base_layer=scene.view_layers[0];base_layer.name='Stage and limbs'
body_layer=scene.view_layers.new('Unified body')
face_layer=scene.view_layers.new('Face')
for layer,allowed in ((base_layer,None),(body_layer,{body_art.name,controls.name}),(face_layer,{face_art.name,controls.name})):
    for child in layer.layer_collection.children:
        child.exclude=(child.name in {body_art.name,face_art.name}) if allowed is None else child.name not in allowed
tree=bpy.data.node_groups.new('Coherent character compositor','CompositorNodeTree')
scene.compositing_node_group=tree
tree.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
n=tree.nodes;links=tree.links
renders={}
for layer in (base_layer,body_layer,face_layer):
    node=n.new('CompositorNodeRLayers');node.layer=layer.name;renders[layer.name]=node
dilate=n.new('CompositorNodeDilateErode');dilate.inputs['Size'].default_value=1
links.new(renders['Unified body'].outputs['Alpha'],dilate.inputs[0])
border=n.new('CompositorNodeSetAlpha');border.inputs[0].default_value=ink.diffuse_color
links.new(dilate.outputs[0],border.inputs[1])
def over(background,foreground):
    node=n.new('CompositorNodeAlphaOver')
    links.new(background,node.inputs['Background']);links.new(foreground,node.inputs['Foreground']);return node.outputs[0]
combined=over(renders['Stage and limbs'].outputs['Image'],border.outputs[0])
combined=over(combined,renders['Unified body'].outputs['Image'])
combined=over(combined,renders['Face'].outputs['Image'])
glare=n.new('CompositorNodeGlare');glare.inputs['Type'].default_value='Fog Glow'
glare.inputs['Threshold'].default_value=1.3;glare.inputs['Strength'].default_value=.55;glare.inputs['Size'].default_value=.18
links.new(combined,glare.inputs['Image'])
output=n.new('NodeGroupOutput');links.new(glare.outputs['Image'],output.inputs['Image'])
scene.render.use_compositing=True
scene['Character construction']='Native flat face; derived shoulders/hips; live unioned torso/shorts alpha and one external border.'
scene['Review status']='Small user-authorized pose/motion proof, awaiting creative playback review.'
scene['Fiction']='Reference-inspired character moving a box; not a historical football event.'
scene.render.resolution_percentage=50
scene.eevee.taa_render_samples=16
scene.frame_set(1)
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'cartoon-skin.blend'))
bpy.ops.wm.open_mainfile(filepath=str(OUT/'cartoon-skin.blend'))
scene=bpy.context.scene
checks=verify(baseline)
assert contact_geometry()==baseline_contacts
assert digest(SOURCE)==source_hash
checks.update(source_preserved=True,projected_hand_shoe_geometry='identical on all 240 frames',
    head_artwork='native meshes and curves; no face image',
    waist='one live combined-fill silhouette, no separately outlined waist parts',
    limits='All original control motion and contacts checked. Attachment offsets and silhouette treatment are new and require visual review.')
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
for f in (1,54,104,118,138,154,158,162,167,170,179,220):
    scene.frame_set(f);scene.render.filepath=str(OUT/f'pose-{f:03}.png');bpy.ops.render.render(write_still=True)
append_event(ROOT,stage='coherent-native-checks',status='passed',intent='Validate the saved simplified character and unchanged action controls',
    method='Saved/reopened control, endpoint and projected hand/foot comparison',
    outputs=[str((OUT/name).relative_to(ROOT)) for name in ('cartoon-skin.blend','checks.json')],
    result='All original controller frames and contact geometry retained. Native pose samples rendered for independent visual inspection; no user acceptance claimed.')
print('COHERENT_BUILD_COMPLETE',OUT,flush=True)
