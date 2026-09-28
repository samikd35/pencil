"""Verify the reopened Blender artifact, independently of the authoring functions."""
import json
import math
from pathlib import Path
import bpy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'artifacts/rough-v003'
shot = json.loads((ROOT/'shot-v003.json').read_text())
scene = bpy.context.scene
report = {'blender':bpy.app.version_string,'checked_frames':0,'max_hand_contact_error':0,
          'max_planted_foot_drift':0,'max_limb_endpoint_error':0,'min_shoe_height':100,
          'release_hand_step':{},'external_files':[]}
anchors = {}
previous_hands = {}
camera = scene.camera
half_width = camera.data.ortho_scale/2
half_height = half_width*scene.render.resolution_y/scene.render.resolution_x
assert scene.frame_start==1 and scene.frame_end==240 and scene.render.fps==24
for f in range(1,241):
    scene.frame_set(f)
    graph = bpy.context.evaluated_depsgraph_get()
    for side in ('far','near'):
        hand=bpy.data.objects['CTRL_Hand_'+side].evaluated_get(graph)
        wrist=hand.matrix_world.translation
        if f==152:
            report['release_hand_step'][side]=(wrist-previous_hands[side]).length
        previous_hands[side]=wrist.copy()
        if 54<=f<=151:
            mitten=bpy.data.objects['Mitten_'+side].evaluated_get(graph)
            edge=max((mitten.matrix_world@v.co).x for v in mitten.data.vertices)+.019
            box_x=bpy.data.objects['CTRL_Box'].evaluated_get(graph).matrix_world.translation.x
            report['max_hand_contact_error']=max(report['max_hand_contact_error'],abs(edge-box_x))
        shoe=bpy.data.objects['Shoe_'+side].evaluated_get(graph)
        min_y=min((shoe.matrix_world@v.co).y for v in shoe.data.vertices)-.041/2
        report['min_shoe_height']=min(report['min_shoe_height'],min_y)
        foot=bpy.data.objects['CTRL_Foot_'+side].evaluated_get(graph).matrix_world.translation
        for start,end in shot['planted_intervals']['foot_'+side]:
            if f==start:
                anchors[(side,start)]=foot.copy()
            if start<=f<=end:
                report['max_planted_foot_drift']=max(report['max_planted_foot_drift'],(foot-anchors[(side,start)]).length)
        for limb,target in (('Arm',wrist),('Leg',foot)):
            obj=bpy.data.objects[limb+'_'+side].evaluated_get(graph)
            endpoint=obj.data.splines[0].bezier_points[1].co
            report['max_limb_endpoint_error']=max(report['max_limb_endpoint_error'],math.dist(endpoint[:2],target[:2]))
    for obj in bpy.data.collections['Artwork • native vectors'].objects:
        if obj.name in ('White backdrop','Ground'):
            continue
        evaluated=obj.evaluated_get(graph)
        mesh=evaluated.to_mesh()
        for vertex in mesh.vertices:
            x,y,z=evaluated.matrix_world@vertex.co
            assert abs(x-camera.location.x) < half_width-.1, (f,obj.name,'horizontal crop')
            assert abs(y-camera.location.y) < half_height-.1, (f,obj.name,'vertical crop')
        evaluated.to_mesh_clear()
    report['checked_frames']+=1
for image in bpy.data.images:
    if image.source=='FILE' and image.filepath and not image.packed_file:
        report['external_files'].append(image.filepath)
assert not bpy.data.libraries
assert not report['external_files']
assert report['max_hand_contact_error']<1e-5
assert report['max_planted_foot_drift']<1e-5
assert report['max_limb_endpoint_error']<1e-5
assert report['min_shoe_height']>-.001
assert max(report['release_hand_step'].values())<.1
report['status']='passed'
report['scope']='240 evaluated frames in a reopened .blend: hand contour contact, foot plants, limb attachments, release continuity, shoe-ground bounds, framing and external dependencies. Artistic timing remains a human review.'
(OUT/'verified-project.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
