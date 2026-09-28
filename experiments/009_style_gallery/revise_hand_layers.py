"""Apply the shared occlusion fix to the existing chibi box proof without reauthoring motion."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import bpy

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'pipeline/styles'))
from build_samples import controllers, contact_geometry, verify
from character_layers import separate_front_arm


def arm_geometry():
    result=[]
    names=['Arm_'+side+suffix for side in ('far','near') for suffix in ('',' fill')]+['STYLE sleeve far','STYLE sleeve near']
    for frame in range(1,241):
        bpy.context.scene.frame_set(frame);graph=bpy.context.evaluated_depsgraph_get();values=[]
        for name in names:
            obj=bpy.data.objects[name].evaluated_get(graph)
            values.append([name,[[list(obj.matrix_world@getattr(p,k)) for k in ('co','handle_left','handle_right')] for p in obj.data.splines[0].bezier_points]])
        result.append(hashlib.sha256(json.dumps(values).encode()).hexdigest())
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);parser.add_argument('--render',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);out=args.out.resolve()
    if args.render:
        bpy.ops.wm.open_mainfile(filepath=str(out/'character.blend'))
        scene=bpy.context.scene;scene.render.resolution_x=640;scene.render.resolution_y=360;scene.render.resolution_percentage=100
        scene.eevee.taa_render_samples=16
        scene.render.image_settings.media_type='VIDEO';scene.render.image_settings.file_format='FFMPEG'
        scene.render.ffmpeg.format='MPEG4';scene.render.ffmpeg.codec='H264';scene.render.ffmpeg.constant_rate_factor='HIGH';scene.render.ffmpeg.audio_codec='NONE'
        if (out/'motion-picture.mp4').exists():raise ValueError('Preserve existing output')
        scene.render.filepath=str(out/'motion-picture.mp4');bpy.ops.render.render(animation=True)
        return
    source=HERE/'proofs/workflow-v001/chibi/animatic-v001/character.blend'
    source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
    out.mkdir(parents=True,exist_ok=False)
    bpy.ops.wm.open_mainfile(filepath=str(source))
    original_layer=bpy.context.window.view_layer
    before_layer=bpy.context.scene.view_layers.new('Before geometry check');before_layer.use=False
    bpy.context.window.view_layer=before_layer
    _,baseline=controllers();contacts=contact_geometry();source_geometry=arm_geometry()
    for side in ('far','near'):
        bpy.data.objects['ATTACH_Shoulder_'+side].location.x *= -1
    geometry=arm_geometry()
    assert geometry!=source_geometry,'Shoulder-side correction was not applied'
    bpy.context.window.view_layer=original_layer;bpy.context.scene.view_layers.remove(before_layer)
    front,hand=separate_front_arm()
    scene=bpy.context.scene;scene.frame_set(1)
    scene['Review status']='User-requested front-arm layering proof; unchanged motion and original audio; review candidate.'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'character.blend'))
    bpy.ops.wm.open_mainfile(filepath=str(out/'character.blend'))
    checks=verify(baseline)
    assert contact_geometry()==contacts
    assert arm_geometry()==geometry,'Layer change altered arm or sleeve paths'
    assert source_hash==hashlib.sha256(source.read_bytes()).hexdigest()
    checks.pop('identical_controller_frame_hashes')
    checks.update(source_sha256=source_hash,all_arm_and_sleeve_curves_240_frames='Identical before/after layering; shoulder-side correction changes upper-arm geometry relative to source',all_hand_and_foot_meshes_240_frames='identical',original_control_tracks='identical, including original elbow controls',shoulder_correction='Near shoulder screen-left; far shoulder screen-right. Derived bends follow attachments; hand paths unchanged.',front_arm=front,front_hand=hand)
    scene=bpy.context.scene
    assert all(scene.view_layers['Unified body'].layer_collection.children[c].exclude for c in ('Foreground arm artwork','Foreground hand artwork'))
    assert not scene.view_layers['Front hand'].layer_collection.children['Foreground hand artwork'].exclude
    # Exercise both draw-order states without changing the control motion.
    scene['front_arm_over_face']=0.0;scene.frame_set(162);bpy.context.view_layer.update()
    assert all(fc.driver.is_valid for fc in scene.compositing_node_group.animation_data.drivers)
    scene['front_arm_over_face']=1.0
    (out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    (out/'revise_hand_layers.py').write_bytes(Path(__file__).read_bytes())
    (out/'character_layers.py').write_bytes((ROOT/'pipeline/character_layers.py').read_bytes())
    for frame in (1,41,104,138,162,170,220):
        scene.frame_set(frame);scene.render.filepath=str(out/f'pose-{frame:03}.png');bpy.ops.render.render(write_still=True)
    scene.frame_set(1);scene.camera.animation_data_clear();scene.camera.location=(-4.55,2.35,30);scene.camera.data.ortho_scale=5.4
    scene.render.resolution_x=600;scene.render.resolution_y=720;scene.render.resolution_percentage=100
    scene.render.filepath=str(out/'resting-pose.png');bpy.ops.render.render(write_still=True)
    print('PASS: same 240 original control poses and hand/foot geometry; corrected shoulder sides; layering preserves corrected arm curves')


if __name__=='__main__':main()
