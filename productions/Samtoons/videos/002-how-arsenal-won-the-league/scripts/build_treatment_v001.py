"""Native TR02 composition with separately placed raster character artwork.

Static design proof only: artwork planes are not character rigs.
Run through the live Blender connector; preserve the existing boards.
"""
import bpy
from pathlib import Path

ROOT=Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/002-how-arsenal-won-the-league')
OUT=ROOT/'artifacts/visual-treatment-v001'
# Reuse the current video's drawing helpers without building any rough boards.
exec(compile((ROOT/'scripts/build_boards_v001.py').read_text(),'build_boards_v001.py','exec'))
OUT=ROOT/'artifacts/visual-treatment-v001'
base_material=material

def material(color):
    m=base_material(color)
    if not m.get('samtoons_flat_emission'):
        m.use_nodes=True; n=m.node_tree.nodes; n.clear()
        out=n.new('ShaderNodeOutputMaterial'); e=n.new('ShaderNodeEmission')
        e.inputs[0].default_value=m.diffuse_color
        m.node_tree.links.new(e.outputs[0],out.inputs[0])
        m['samtoons_flat_emission']=True
    return m

s=scene('S002_TR02_treatment_v001','#d9e7ee')
s.render.engine='BLENDER_EEVEE'
s.render.resolution_x=1920; s.render.resolution_y=1080
s.render.image_settings.color_mode='RGB'
s.render.use_sequencer=False

rect('rear_stand',-8,.0,16,3.1,'#b8c0c9',-.85)
for row in range(3):
    y=.6+row*.55
    for i in range(44):
        x=-8+i*.38
        disc('distant_spectator',x,y,.13,'#8c98a6',-.8)
        rect('distant_shoulders',x-.16,y-.21,.32,.22,'#8c98a6',-.8)
rect('stadium_red_fascia',-8,2.7,16,.52,'#a6313d',-.7)
line('roof', [(-8,3.5),(8,3.5)],'#758998',.055,-.6)
for x in range(-8,9,2): line('roof_beam',[(x,3.5),(x+1,4.3)],'#758998',.045,-.6)
rect('pitch',-8,-4.5,16,4.6,'#6d9c58',-.6)
poly('grass_light',[(-8,-4.5),(-4,-4.5),(1,.1),(-2,.1)],'#7fa867',-.55)
poly('grass_light',[(2,-4.5),(6,-4.5),(8,.1),(5,.1)],'#7fa867',-.55)
line('touchline',[(-8,-3.9),(8,-.2)],WHITE,.035,-.5)
poly('carpet',[(-7.9,-4.5),(4.7,-4.5),(6.45,-2.8),(4.65,-2.8)],'#9e2434',-.3)
line('carpet_edge',[(-7.9,-4.46),(4.7,-4.46),(6.45,-2.8)],'#d7ae66',.025,-.2)

# Two UV windows preserve the original pixels while allowing independent staging.
im=bpy.data.images.load(str(OUT/'gyokeres-arteta.png')); im.pack()
m=bpy.data.materials.new('TR02 / character artwork'); m.use_nodes=True
n=m.node_tree.nodes; n.clear(); links=m.node_tree.links
out=n.new('ShaderNodeOutputMaterial'); em=n.new('ShaderNodeEmission')
tex=n.new('ShaderNodeTexImage'); tex.image=im; tex.extension='CLIP'
transparent=n.new('ShaderNodeBsdfTransparent'); mix=n.new('ShaderNodeMixShader')
cutoff=n.new('ShaderNodeMath'); cutoff.operation='GREATER_THAN'; cutoff.inputs[1].default_value=.93
links.new(tex.outputs['Color'],em.inputs[0]); links.new(tex.outputs['Alpha'],cutoff.inputs[0])
links.new(cutoff.outputs[0],mix.inputs[0]); links.new(transparent.outputs[0],mix.inputs[1])
links.new(em.outputs[0],mix.inputs[2]); links.new(mix.outputs[0],out.inputs[0])
m.surface_render_method='DITHERED'

def artwork(name,x0,x1,u0,u1):
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata([(x0,-3.7,2),(x1,-3.7,2),(x1,3.65,2),(x0,3.65,2)],[],[(0,1,2,3)])
    mesh.uv_layers.new()
    for loop,uv in zip(mesh.uv_layers.active.data,[(u0,0),(u1,0),(u1,1),(u0,1)]): loop.uv=uv
    o=bpy.data.objects.new(name,mesh); s.collection.objects.link(o); mesh.materials.append(m)
    o['scope']='Static raster pose; independent position/scale only. No joint or face controls.'
    return o

gy=artwork('TR02 / Gyokeres',-7.2,-1.467,0,.52)
ar=artwork('TR02 / Arteta',-1.65,3.642,.52,1)
# Editable native corner-flag prop, with shirt front facing the viewer.
poly('flag_contact_shadow',[(5.65+.6*math.cos(i*math.tau/40),-3.3+.12*math.sin(i*math.tau/40)) for i in range(40)],'#486d43',-.15)
for name,x,r in [('gyokeres',-4.3,1.65),('arteta',.6,1.45)]:
    poly(name+'_contact_shadow',[(x+r*math.cos(i*math.tau/40),-3.45+.11*math.sin(i*math.tau/40)) for i in range(40)],'#4d643e',-.1)
line('flag_pole',[(5.65,-3.25),(5.65,2.8)],'#e8e4d9',.045,.4)
poly('corner_flag',[(5.65,2.8),(7.08,2.35),(5.65,1.92)],RED,.5)
shirt=[(5.17,1.25),(6.13,1.25),(6.75,.65),(6.3,.2),(6.1,.4),(6.2,-1.35),(5.1,-1.35),(5.2,.4),(5.0,.2),(4.55,.65)]
poly('shirt_fill',shirt,RED,.7); line('shirt_outline',shirt+[shirt[0]],INK,.027,.75)
poly('left_white_sleeve',[(5.17,1.25),(4.55,.65),(5,.2),(5.2,.4),(5.35,.85)],WHITE,.8)
poly('right_white_sleeve',[(6.13,1.25),(6.75,.65),(6.3,.2),(6.1,.4),(5.97,.85)],WHITE,.8)
line('collar',[(5.38,1.23),(5.65,.96),(5.93,1.23)],WHITE,.035,.9)
text('9',5.28,-.87,1.48,WHITE,1)

s['Purpose']='TR02 visual-treatment proposal. Native environment/prop/camera; packed raster poses, not rigs.'
s['Script input']='script-v003.md; 81c206544bb86b2221e88766a48d5cd4e3e4b0d73f706fd02fb98b4c188d15a3'
s['Review scope']='Appearance of Arteta/Gyokeres and scene finish. Approved joke/camera sequence is not reopened.'
s.camera.name='TR02 / wide camera'
cam=bpy.data.cameras.new('TR02 / reaction camera'); cam.type='ORTHO'; cam.ortho_scale=10.6
close=bpy.data.objects.new('TR02 / reaction camera',cam); s.collection.objects.link(close); close.location=(-2,1.0,25)
bpy.context.view_layer.update()
assert im.size[:]==(1536,1024) and gy.data.uv_layers and ar.data.uv_layers
assert s.render.resolution_x*9==s.render.resolution_y*16
assert all(o in s.objects[:] for o in [gy,ar,close])
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'unveiling-treatment-v001.blend'))
result={'file':bpy.data.filepath,'scene':s.name,'limits':'Static artwork design proof; motion and likeness approval pending.'}
