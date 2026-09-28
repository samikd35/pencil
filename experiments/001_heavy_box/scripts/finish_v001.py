"""Add an editable visual finish to the delivered animation without rebuilding its motion."""
import json
import math
from pathlib import Path
import sys
import bpy

ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/'finish-v001.json').read_text())
OUT=ROOT/'artifacts/finish-v001'
bpy.ops.wm.open_mainfile(filepath=str(ROOT/CFG['base']))
scene=bpy.context.scene
effects=bpy.data.collections.new('Finish • lighting, shadows and sparks')
scene.collection.children.link(effects)
P=CFG['palette']

def rgba(value):
    rgb=[int(value[i:i+2],16)/255 for i in (1,3,5)]
    return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb)+(1,)

def emission(name,color,strength=1):
    m=bpy.data.materials.new(name);m.use_nodes=True
    m.diffuse_color=rgba(color)
    n=m.node_tree.nodes;n.clear()
    output=n.new('ShaderNodeOutputMaterial');shader=n.new('ShaderNodeEmission')
    shader.inputs['Color'].default_value=rgba(color)
    shader.inputs['Strength'].default_value=strength
    m.node_tree.links.new(shader.outputs[0],output.inputs['Surface'])
    return m,shader

def assign(name,color):
    obj=bpy.data.objects[name]
    m,_=emission('Finish / '+name,color)
    obj.data.materials.clear();obj.data.materials.append(m)

def polygon(name,points,z,mat,parent=None):
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata([(*p,z) for p in points],[],[list(range(len(points)))])
    mesh.materials.append(mat)
    obj=bpy.data.objects.new(name,mesh);effects.objects.link(obj);obj.parent=parent
    return obj

def line(name,points,z,width,mat,parent=None):
    curve=bpy.data.curves.new(name,'CURVE');curve.dimensions='3D'
    curve.bevel_depth=width/2;curve.bevel_resolution=3
    spline=curve.splines.new('POLY');spline.points.add(len(points)-1)
    for point,xy in zip(spline.points,points):point.co=(*xy,z,1)
    curve.materials.append(mat)
    obj=bpy.data.objects.new(name,curve);effects.objects.link(obj);obj.parent=parent
    return obj

# Recolor the shared ink, then assign isolated fills.
for mat in list(bpy.data.materials):
    if mat.name=='#20252c':
        mat.diffuse_color=rgba(P['ink'])
        for node in mat.node_tree.nodes:
            if node.type=='EMISSION':node.inputs['Color'].default_value=rgba(P['ink'])
for name,color in {'Head':P['paper'],'Mitten_far':P['paper'],'Mitten_near':P['paper'],
    'Shoe_far':P['shoes'],'Shoe_near':P['shoes'],'Box front':P['box'],
    'Box top':P['box_top'],'Box side':P['box_side'],'Tape':P['tape'],'Tape top':P['tape'],'Ground':'#c9b49b'}.items():assign(name,color)

# A broad illustrated spotlight: procedural color falloff, not a physical lamp on emission artwork.
back,shader=emission('Warm spotlight',P['paper'])
n=back.node_tree.nodes;l=back.node_tree.links
position=n.new('ShaderNodeNewGeometry')
distance=n.new('ShaderNodeVectorMath');distance.operation='DISTANCE';distance.inputs[1].default_value=(-1.4,3.1,-2)
l.new(position.outputs['Position'],distance.inputs[0])
divide=n.new('ShaderNodeMath');divide.operation='DIVIDE';divide.inputs[1].default_value=7.5
l.new(distance.outputs['Value'],divide.inputs[0])
mix=n.new('ShaderNodeMixRGB');mix.blend_type='MIX';mix.use_clamp=True
mix.inputs[1].default_value=rgba('#fff9ed');mix.inputs[2].default_value=rgba(P['edge'])
l.new(divide.outputs[0],mix.inputs[0]);l.new(mix.outputs[0],shader.inputs['Color'])
bpy.data.objects['White backdrop'].data.materials[0]=back
floor,_=emission('Warm stage floor',P['floor'])
polygon('Stage floor',[(-20,-10),(20,-10),(20,0),(-20,0)],-1.3,floor)

shadow=bpy.data.materials.new('Soft painted shadows');shadow.use_nodes=True;shadow.surface_render_method='BLENDED'
n=shadow.node_tree.nodes;n.clear();l=shadow.node_tree.links
output=n.new('ShaderNodeOutputMaterial');transparent=n.new('ShaderNodeBsdfTransparent')
shade=n.new('ShaderNodeEmission');shade.inputs['Color'].default_value=rgba('#624b36')
uv=n.new('ShaderNodeTexCoord');offset=n.new('ShaderNodeVectorMath');offset.operation='SUBTRACT';offset.inputs[1].default_value=(.5,.5,0)
l.new(uv.outputs['Generated'],offset.inputs[0])
stretch=n.new('ShaderNodeVectorMath');stretch.operation='MULTIPLY';stretch.inputs[1].default_value=(2,2,0);l.new(offset.outputs[0],stretch.inputs[0])
length=n.new('ShaderNodeVectorMath');length.operation='LENGTH';l.new(stretch.outputs[0],length.inputs[0])
fall=n.new('ShaderNodeMath');fall.operation='SUBTRACT';fall.inputs[0].default_value=1;fall.use_clamp=True;l.new(length.outputs['Value'],fall.inputs[1])
power=n.new('ShaderNodeMath');power.operation='POWER';power.inputs[1].default_value=1.5;l.new(fall.outputs[0],power.inputs[0])
opacity=n.new('ShaderNodeMath');opacity.operation='MULTIPLY';opacity.inputs[1].default_value=.30;l.new(power.outputs[0],opacity.inputs[0])
blend=n.new('ShaderNodeMixShader');l.new(opacity.outputs[0],blend.inputs[0]);l.new(transparent.outputs[0],blend.inputs[1]);l.new(shade.outputs[0],blend.inputs[2]);l.new(blend.outputs[0],output.inputs['Surface'])
shadows={}
for side in ('far','near'):
    shadows[side]=polygon('Foot shadow '+side,[(-1,-1),(1,-1),(1,1),(-1,1)],-.30,shadow)
box_shadow=polygon('Box shadow',[(-1,-1),(1,-1),(1,1),(-1,1)],-.32,shadow,bpy.data.objects['CTRL_Box'])
box_shadow.location=(1,-.035,0);box_shadow.scale=(1.2,.13,1)
highlight,_=emission('Box edge light','#c8eee3')
line('Box highlight',[(.03,2.265),(1.77,2.265)],.045,.018,highlight,bpy.data.objects['CTRL_Box'])

# Small golden zigzags are authored effects, with bloom restricted to their bright cores.
spark,spark_shader=emission('Golden electric accent',P['spark'],0)
bolts=[line('Effort spark left',[(-.92,.12),(-1.06,.34),(-.85,.31),(-.98,.56)],.52,.030,spark),
       line('Effort spark right',[(.78,.18),(.99,.35),(.82,.38),(1.04,.60)],.52,.030,spark)]
start,end=CFG['lightning_frames']
for f in range(1,241):
    scene.frame_set(f)
    for side,obj in shadows.items():
        foot=bpy.data.objects['CTRL_Foot_'+side].matrix_world.translation
        height=max(0,foot.y-.14)
        obj.location=(foot.x+.045,-.035,0)
        obj.scale=(.45+.08*height,.09+.03*height,1)
        obj.keyframe_insert(data_path='location',frame=f);obj.keyframe_insert(data_path='scale',frame=f)
    head=bpy.data.objects['CTRL_Head'].matrix_world.translation
    for i,bolt in enumerate(bolts):
        bolt.location=(head.x,head.y,0)
        on=start<=f<=end
        amount=(.8+.1*math.sin((f-start)*.65+i)) if on else 0
        bolt.scale=(amount,amount,1)
        bolt.keyframe_insert(data_path='location',frame=f);bolt.keyframe_insert(data_path='scale',frame=f)
    # One smooth energy swell, with no repeated full-screen flashes.
    energy=3.0*math.sin(math.pi*(f-start)/(end-start)) if start<=f<=end else 0
    spark_shader.inputs['Strength'].default_value=max(0,energy)
    spark_shader.inputs['Strength'].keyframe_insert(data_path='default_value',frame=f)

tree=bpy.data.node_groups.new('Finish compositor','CompositorNodeTree')
scene.compositing_node_group=tree
tree.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
layers=tree.nodes.new('CompositorNodeRLayers');glare=tree.nodes.new('CompositorNodeGlare')
glare.inputs['Type'].default_value='Fog Glow'
glare.inputs['Threshold'].default_value=1.3
glare.inputs['Strength'].default_value=.55
glare.inputs['Size'].default_value=.18
output=tree.nodes.new('NodeGroupOutput')
tree.links.new(layers.outputs['Image'],glare.inputs['Image']);tree.links.new(glare.outputs['Image'],output.inputs['Image'])
scene.render.use_compositing=True

editor=scene.sequence_editor_create()
sound=editor.strips.new_sound('Original synthesized cartoon soundtrack',str(OUT/'audio/soundtrack.wav'),channel=1,frame_start=1)
sound.sound.filepath='//audio/soundtrack.wav'
scene.render.use_sequencer=False
scene['Finish notes']='Original procedural sound design. Warm illustrated lighting, teal/coral palette, soft shadows, brief golden sparks. Base character motion preserved.'
scene.render.filepath='//frames/frame-'
scene.frame_set(138)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'character-and-effects.blend'))
if '--samples' in sys.argv:
    for f in (1,104,118,138,158,170,220):
        scene.frame_set(f);scene.render.filepath=str(OUT/f'sample-{f:03}.png');bpy.ops.render.render(write_still=True)
if '--render' in sys.argv:
    scene.render.filepath=str(OUT/'frames/frame-');bpy.ops.render.render(animation=True)
