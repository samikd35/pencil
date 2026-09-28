"""Native style artwork on the saved Heavy Box controls; no image planes or armature deformation.

This is a benchmark adapter, not a universal scene importer. Reuse apply_style only
with the named controls/collections described in construction.md, or adapt those bindings.
"""
import argparse
import ast
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OLD = ROOT / 'experiments/008_cartoon_skin'
SOURCE = OLD / 'artifacts/coherent-proof-v003/cartoon-skin.blend'

# Existing film scripts have top-level builds. Load their small, inspected helpers only.
for file, names in [
    (OLD/'build_skin.py', {'digest','controllers','contact_geometry','material','polygon','oval','verify'}),
    (OLD/'build_ronny.py', {'assign','curve_section'}),
    (OLD/'build_coherent.py', {'anchor','line','live_line'}),
    (ROOT/'experiments/001_heavy_box/scripts/build_v005.py', {'smooth_closed','driver'}),
]:
    nodes = [n for n in ast.parse(file.read_text()).body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert len(nodes) == len(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(file), 'exec'))


def patterned(mat, finish):
    """Original procedural paper/print: no downloaded textures or hidden image dependencies."""
    nodes = mat.node_tree.nodes; links = mat.node_tree.links
    emission = next(n for n in nodes if n.type == 'EMISSION')
    color = tuple(emission.inputs['Color'].default_value)
    coords = nodes.new('ShaderNodeTexCoord')
    texture = nodes.new('ShaderNodeTexWave' if finish == 'collage' else 'ShaderNodeTexNoise')
    texture.inputs['Scale'].default_value = 12 if finish == 'collage' else 45
    if finish == 'collage':
        texture.bands_direction = 'DIAGONAL'
        texture.inputs['Distortion'].default_value = 0
    else:
        texture.inputs['Detail'].default_value = 2
    links.new(coords.outputs['Generated'], texture.inputs['Vector'])
    ramp = nodes.new('ShaderNodeValToRGB')
    amount = .42 if finish == 'collage' else .78
    ramp.color_ramp.elements[0].color = tuple(c*amount for c in color[:3])+(1,)
    ramp.color_ramp.elements[1].color = color
    links.new(texture.outputs['Fac'], ramp.inputs[0]); links.new(ramp.outputs[0], emission.inputs['Color'])


def text_art(name, words, x, y, z, size, mat, parent=None):
    data = bpy.data.curves.new(name, 'FONT'); data.body = words
    data.size = size; data.align_x = 'CENTER'; data.materials.append(mat)
    obj = bpy.data.objects.new(name, data); skin.objects.link(obj)
    obj.parent = parent; obj.location = (x,y,z)
    return obj


def apply_style(option):
    global skin, ink, controls, section_specs
    scene = bpy.context.scene
    settings = option['settings']; design = settings['design']; finish = settings['finish']; presentation = settings['presentation']
    controls = bpy.data.collections['Pose controls • keyed and editable']
    body_art = bpy.data.collections['Unified body fills']; face_art = bpy.data.collections['Flat native face']
    surface = bpy.data.collections['Cartoon surface / same stickman controls']
    for collection in (body_art, face_art):
        for obj in list(collection.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.objects.remove(bpy.data.objects['Captain band'], do_unlink=True)
    section_specs = []
    colors = dict(ink='#263640', shirt='#4f9997', skin='#efb688', hair='#303644', accent='#eb9067', paper='#fff5df')
    if design == 'hose': colors.update(shirt='#323638', skin='#fff5df', hair='#323638', accent='#d87656')
    if design == 'angular': colors.update(ink='#344953',shirt='#d78762',skin='#e9b583',hair='#364b55',accent='#799996')
    if design == 'fox': colors.update(skin='#d88443',shirt='#699891',hair='#743e28')
    if design in ('toast','emoji'): colors.update(skin='#eabe65',shirt='#eabe65',hair='#925336')
    if finish in ('doodle','whiteboard'): colors.update(shirt='#fff9ee',skin='#fff9ee',hair='#fff9ee',accent='#fff9ee')
    if finish == 'silhouette': colors = {k: '#263440' for k in colors}
    if finish == 'storybook': colors.update(ink='#52616a',shirt='#8daba0',skin='#e8c7a9',hair='#73818a',accent='#cfa696')
    mats = {k: material('Style / '+k,v) for k,v in colors.items()}
    ink = mats['ink']; outfit = mats['shirt']; complexion = mats['skin']; white = material('Style / eye white','#fff9ee')
    if finish in ('storybook','collage','paper'):
        for k in ('shirt','skin','hair','accent'):
            patterned(mats[k], finish)
    body_source = bpy.data.objects['CTRL_Body']
    compact = design in ('chibi','toast','emoji')
    h,w = (.56,.31) if design == 'chibi' else ((.76,.42) if design in ('toast','emoji') else (.94,.29))
    if design == 'angular': h,w = 1.05,.37
    if design == 'stick': w=.035
    body = anchor('STYLE_Body',None,(0,0,0))
    for axis,letter in enumerate('XY'):
        targets=[('a',body_source,letter)]
        expression='a'
        if compact and axis==1:
            targets += [('f',bpy.data.objects['CTRL_Foot_far'],'Y'),('g',bpy.data.objects['CTRL_Foot_near'],'Y')]
            expression='max(a*0.70,max(f,g)+0.78)'
        driver(body,'location',axis,targets,expression)
    body.constraints.new('COPY_ROTATION').target=body_source
    head_base=anchor('STYLE_HeadPosition',body,(0,h+.26,0))
    head=anchor('STYLE_Head',None,(0,0,0))
    head.constraints.new('COPY_LOCATION').target=head_base
    head.constraints.new('COPY_ROTATION').target=bpy.data.objects['CTRL_Head']
    radius=.030 if design=='stick' else (.062 if design in ('hose','geometric','angular') else .083)
    for side,sign in (('far',-1),('near',1)):
        hip=bpy.data.objects['ATTACH_Hip_'+side]; hip.parent=body;hip.location=(sign*w*.58,-.11,0)
        shoulder=bpy.data.objects['ATTACH_Shoulder_'+side];shoulder.parent=body;shoulder.location=(sign*w*.72,h-.13,0)
        for part,target,old_start,bend_name,r in (
            ('Arm',shoulder,bpy.data.objects['ANCHOR_Shoulder'],'Elbow',radius),
            ('Leg',hip,body_source,'Knee',radius+.012)):
            bend=anchor('STYLE_'+bend_name+'_'+side,None,(0,0,0))
            for axis,letter in enumerate('XY'):
                driver(bend,'location',axis,[('a',bpy.data.objects['CTRL_'+bend_name+'_'+side],letter),('b',target,letter),('c',old_start,letter)],'a+(b-c)*0.5')
            for suffix in ('',' fill'):
                obj=bpy.data.objects[part+'_'+side+suffix];obj.data.bevel_depth=r+(.016 if not suffix else 0)
                assign(obj.name,ink if not suffix or design=='stick' else complexion)
                for fc in obj.data.animation_data.drivers:
                    for variable in fc.driver.variables:
                        if variable.name=='b': variable.targets[0].id=bend
        assign('Mitten_'+side,white if design=='hose' else (ink if finish=='silhouette' else complexion))
        assign('Mitten_'+side+'_outline',ink);assign('Shoe_'+side,mats['hair']);assign('Shoe_'+side+'_outline',ink)
        bpy.data.objects['White socks '+side].hide_render=True
    skin=body_art
    if design=='stick':
        polygon('STYLE spine',[(w,h),(-w,h),(-w,-.18),(w,-.18)],.5,ink,body,False)
    else:
        points=[(-w*.35,h),(w*.35,h),(w,h-.16),(w,-.10),(w*.65,-.27),(0,-.30),(-w*.65,-.27),(-w,-.10),(-w,h-.16)]
        if design=='angular':points=[(-w*.8,h),(w*.7,h),(w*1.1,-.16),(-w,-.25)]
        if design=='emoji':points=oval(0,.34,.52,.61)
        if design=='toast':points=[(-.44,-.18),(.44,-.18),(.44,.62),(.52,.77),(.42,.97),(-.42,.97),(-.52,.77),(-.44,.62)]
        polygon('STYLE continuous body',points if design in ('geometric','angular') else smooth_closed(points),.5,outfit,body,False)
        for side in ('far','near'):
            curve_section('STYLE continuous shorts '+side,bpy.data.objects['Leg_'+side],0,.30,radius+.049,outfit,.045)
            curve_section('STYLE sleeve '+side,bpy.data.objects['Arm_'+side],0,.32,radius+.025,outfit,.045)
        if design not in ('toast','emoji'):
            polygon('STYLE collar',[(-.14,h+.01),(.14,h+.01),(.11,h-.10),(0,h-.15),(-.11,h-.10)],.56,mats['accent'],body,False)
            polygon('STYLE pocket',[(.09,.51),(.22,.51),(.20,.33),(.10,.33)],.56,mats['accent'],body,False)
    if design not in ('toast','emoji'):
        lower=anchor('STYLE_NeckBase',body,(0,h-.05,0));upper=anchor('STYLE_NeckTop',head,(0,.12,0))
        live_line('STYLE continuous neck',lower,upper,.16,.09 if design=='stick' else .20,ink if design=='stick' else complexion)
    skin=face_art
    face_parent=head
    cx,cy=0,.38
    rx,ry=(.43,.51)
    if design=='chibi':rx,ry=.70,.66
    if design=='caricature':rx,ry=.52,.68
    if design=='hose':rx,ry=.43,.47
    if design=='stick':rx,ry=.35,.39
    if design in ('toast','emoji'):
        face_parent=body;cy=.42;rx=.36;ry=.34
    else:
        face=oval(0,cy,rx,ry)
        if design in ('caricature','angular'):
            face=[(-rx,cy+.20),(-rx*.80,cy+ry),(.50*rx,cy+ry),(.93*rx,cy+.30),(rx*1.15,cy-.03),(.86*rx,cy-.18),(.62*rx,cy-ry),(-.6*rx,cy-ry)]
        if design=='geometric':face=[(-rx,cy-ry),(rx,cy-ry),(rx,cy+ry),(-rx,cy+ry)]
        polygon('STYLE face',face,.82,complexion,face_parent)
        if design=='fox':
            for sign in (-1,1):
                polygon('STYLE ear '+str(sign),[(sign*.18,cy+.39),(sign*.47,cy+.87),(sign*.46,cy+.24)],.85,complexion,head)
                polygon('STYLE inner ear '+str(sign),[(sign*.26,cy+.41),(sign*.43,cy+.72),(sign*.41,cy+.36)],.88,mats['hair'],head,False)
            polygon('STYLE muzzle',[(0,cy+.01),(.38,cy-.12),(.15,cy-.38),(-.15,cy-.38),(-.38,cy-.12)],.86,white,head)
        elif design not in ('stick','hose','geometric'):
            hair=[(-rx,cy+.18),(-rx*1.05,cy+ry*.78),(-rx*.72,cy+ry*1.05),(-rx*.60,cy+ry*1.20),(-rx*.27,cy+ry*1.13),(.02,cy+ry*1.27),(rx*.34,cy+ry*1.10),(rx*.88,cy+ry*.91),(rx*.84,cy+ry*.60),(-rx*.53,cy+ry*.67),(-rx*.67,cy+.18)]
            polygon('STYLE hair',hair,.86,mats['hair'],head)
    if design=='toast':
        polygon('STYLE toasted center',[(-.33,-.05),(.33,-.05),(.33,.66),(.38,.79),(-.38,.79),(-.33,.66)],.81,material('Toast middle','#f8dfa1'),body,False)
    if finish!='silhouette':
        eye_y=cy+.07;eye_dx=rx*.42;eye_r=.12 if design=='chibi' else .084
        for sign in (-1,1):
            x=sign*eye_dx
            if design!='stick':polygon('STYLE eye '+str(sign),oval(x,eye_y,eye_r,eye_r*1.20),.90,white,face_parent,False)
            polygon('STYLE pupil '+str(sign),oval(x+.014,eye_y,.037 if design!='chibi' else .065,.061 if design!='chibi' else .11),.92,ink,face_parent,False)
            if design=='hose':polygon('STYLE pie eye '+str(sign),[(x+.008,eye_y),(x+.08,eye_y+.07),(x+.08,eye_y)],.935,white,face_parent,False)
            line('STYLE brow '+str(sign),[(x-eye_r,eye_y+.19),(x+eye_r,eye_y+.17)],.94,ink,face_parent,width=.033)
        if design in ('caricature','angular'):
            polygon('STYLE nose',[(.06,cy+.04),(.10,cy-.11),(.29,cy-.12),(.32,cy-.04),(.16,cy+.10)],.95,complexion,face_parent)
        elif design=='fox':polygon('STYLE nose',oval(0,cy-.09,.083,.055),.95,ink,face_parent,False)
        mouth=line('STYLE smile',[(-.14,cy-.18),(-.07,cy-.24),(.07,cy-.25),(.16,cy-.18)],.96,ink,face_parent,width=.027)
        # Two simple live expression states; source action timing belongs to the benchmark.
        for f,sy in ((1,1),(84,1),(104,-.65),(145,-.65),(156,1),(240,1)):
            mouth.scale.y=sy;mouth.location.y=(1-sy)*(cy-.2);mouth.keyframe_insert(data_path='scale',frame=f);mouth.keyframe_insert(data_path='location',frame=f)
    if finish=='doodle':
        for j in range(5):
            line('STYLE sketch hatch '+str(j),[(-.18+j*.045,.20),(-.12+j*.045,.34)],.61,ink,body,width=.009)
        for obj in list(face_art.objects):
            if obj.name.endswith(' outline'):
                echo=obj.copy();echo.data=obj.data.copy();face_art.objects.link(echo)
                echo.name='STYLE pencil echo';echo.location.x=.013;echo.location.y=-.009;echo.data.bevel_depth=.006
    if finish=='paper':
        shadow=material('Style / paper shadow','#bdab99')
        for obj in list(face_art.objects)+list(body_art.objects):
            if obj.type=='MESH':
                echo=obj.copy();echo.data=obj.data.copy();obj.users_collection[0].objects.link(echo)
                echo.name='STYLE paper offset';echo.location.x+=.025;echo.location.y-=.025;echo.location.z-=.06
                echo.data.materials.clear();echo.data.materials.append(shadow)
    for node in scene.compositing_node_group.nodes:
        if node.type=='SETALPHA':node.inputs[0].default_value=ink.diffuse_color
        if node.type=='DILATEERODE':node.inputs['Size'].default_value=1
    # Scene furniture is original native art. Optional presentation geometry lives in the base layer.
    skin=bpy.data.collections['Artwork • native vectors']
    if finish=='whiteboard':
        board=material('Style / white board','#ffffff')
        polygon('STYLE whiteboard',[(-12,-1),(8,-1),(8,9),(-12,9)],-.10,board,None,False)
        text_art('STYLE board title','HOW IT WORKS',-4.55,4.25,2,.20,ink)
        line('STYLE board arrow',[(-3.45,3.30),(-3.12,3.05),(-3.40,2.72)],2,ink,width=.026)
        line('STYLE arrow head',[(-3.20,2.75),(-3.40,2.72),(-3.39,2.94)],2,ink,width=.026)
    if presentation=='parallax' or design=='angular':
        back=material('Style / distant scenery','#b3c7c0');front=material('Style / near scenery','#547975')
        for j,(x,y,size,z,mat,speed) in enumerate([(-5.8,2.6,1.3,-.8,back,.15),(-2.5,3.4,.9,-.7,back,.2),(-6.8,.55,.8,1.5,front,.7)]):
            obj=polygon('STYLE scenery '+str(j),[(x-size,y-size),(x-size*.5,y+size),(x+size,y+size*.35),(x+size*.8,y-size)],z,mat,None,False)
            if presentation=='parallax':
                obj.location.x=-speed/2;obj.keyframe_insert(data_path='location',frame=1)
                obj.location.x=speed/2;obj.keyframe_insert(data_path='location',frame=240)
    if presentation=='comic':
        text_art('STYLE comic caption','ONE BOX.  ZERO HELP.',-4.5,4.35,2,.20,ink)
        text_art('STYLE comic sound','HEAVE!',-2.9,2.85,2,.24,ink)
        line('STYLE comic panel',[(-6.6,-.10),(-6.6,4.8),(-2.5,4.8),(-2.5,-.10),(-6.6,-.10)],2,ink,width=.035)
    scene['visual_style_id']=option['id'];scene['visual_style_settings']=json.dumps(settings)
    scene['Style scope']='Native benchmark adapter; fixed-view head. Per-film recipes govern adaptation.'
    return option


def render_sample(path, option):
    scene=bpy.context.scene;scene.frame_set(1)
    camera=scene.camera
    camera.animation_data_clear();camera.location=(-4.55,2.35,30);camera.data.ortho_scale=5.4
    if option['settings']['design'] in ('toast','emoji'):
        camera.location.y=1.65;camera.data.ortho_scale=3.9
    scene.render.resolution_x=600;scene.render.resolution_y=720;scene.render.resolution_percentage=100
    scene.eevee.taa_render_samples=16
    scene.render.image_settings.media_type='IMAGE';scene.render.image_settings.file_format='PNG'
    scene.render.filepath=str(path)
    if option['settings']['finish']=='pixel':
        # Native low-resolution render, displayed with nearest-neighbour pixels in the gallery.
        scene.render.resolution_x=100;scene.render.resolution_y=120
    bpy.ops.render.render(write_still=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--style');parser.add_argument('--production',type=Path)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--motion',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if bool(args.style)==bool(args.production):parser.error('Use exactly one of --style or --production')
    if args.production:
        import importlib.util
        spec=importlib.util.spec_from_file_location('style_selection',ROOT/'pipeline/styles.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        selected=module.resolve(args.production)
        option=json.loads((args.production.parent/selected['files']['option.json']['path']).read_text())
        plan=json.loads(args.production.read_text())
        if plan['timeline'] != dict(fps='24',start_frame=1,frames=240,sample_rate=48000):
            raise ValueError('This benchmark adapter requires the 240-frame Heavy Box timeline; adapt scene construction for a new film')
    else:
        option=next(o for o in json.loads((HERE/'catalog.json').read_text())['options'] if o['id']==args.style)
    args.out.mkdir(parents=True,exist_ok=False)
    source_hash=digest(SOURCE)
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    _,baseline=controllers();contacts=contact_geometry()
    apply_style(option)
    scene=bpy.context.scene;scene.frame_set(1)
    scene.render.resolution_percentage=50;scene.eevee.taa_render_samples=16
    (args.out/'build_samples.py').write_bytes(Path(__file__).read_bytes())
    (args.out/'option.json').write_text(json.dumps(option,indent=2)+'\n')
    bpy.ops.wm.save_as_mainfile(filepath=str(args.out/'character.blend'))
    bpy.ops.wm.open_mainfile(filepath=str(args.out/'character.blend'))
    checks=verify(baseline);assert contact_geometry()==contacts;assert digest(SOURCE)==source_hash
    checks.pop('identical_controller_frame_hashes')
    checks.update(style=option['id'],source_sha256=source_hash,source_preserved=True,contact_geometry_240_frames='identical',artwork='Native editable curves, flat meshes and procedural materials')
    (args.out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    render_sample(args.out/'sample.png',option)
    if args.motion:
        bpy.ops.wm.open_mainfile(filepath=str(args.out/'character.blend'))
        scene=bpy.context.scene
        scene.render.resolution_x=640;scene.render.resolution_y=360;scene.render.resolution_percentage=100
        scene.eevee.taa_render_samples=16
        if option['settings']['finish']=='pixel':scene.render.resolution_x=160;scene.render.resolution_y=90
        scene.render.image_settings.media_type='VIDEO';scene.render.image_settings.file_format='FFMPEG'
        scene.render.ffmpeg.format='MPEG4';scene.render.ffmpeg.codec='H264';scene.render.ffmpeg.constant_rate_factor='HIGH'
        scene.render.ffmpeg.audio_codec='NONE';scene.render.filepath=str(args.out/'motion-picture.mp4')
        # ponytail: proof-only 10-second export; full film scripts must use existing checkpoint gates.
        bpy.ops.render.render(animation=True)


if __name__=='__main__':main()
