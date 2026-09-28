"""Reopen and check actual revised anchors, drawing visibility and stationary feet."""
from pathlib import Path
import bpy, json, math
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/staging-v002'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'s01-neck-motion-v003.blend'));s=bpy.context.scene
worst_neck=worst_arm=worst_grip=0.;feet={};foot_drift=0.
for f in range(1,193):
    s.frame_set(f);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
    for name in ('Haaland','Maresca'):
        neck=bpy.data.objects[name+' / deforming neck'].evaluated_get(dg)
        for i,label in [(0,'L collar'),(3,'L skull'),(4,'R skull'),(7,'R collar')]:
            a=bpy.data.objects[name+' / neck '+label+' attachment'].matrix_world.translation
            worst_neck=max(worst_neck,(neck.data.vertices[i].co.xy-a.xy).length)
        faces=[bpy.data.objects[name+f' / registered drawing {i}'] for i in range(4)]
        assert sum(not o.hide_render for o in faces)==1,(f,name)
        for side in (-1,1):
            hand=bpy.data.objects[name+f' / HAND {side}'].matrix_world.translation
            curve=bpy.data.objects[name+f' / arm {side} fill'].evaluated_get(dg)
            tip=curve.matrix_world@curve.data.splines[0].bezier_points[-1].co
            worst_arm=max(worst_arm,(tip.xy-hand.xy).length)
            foot=bpy.data.objects[name+f' / foot {side}'].matrix_world.translation.copy();k=(name,side)
            if f==1:feet[k]=foot
            foot_drift=max(foot_drift,(feet[k]-foot).length)
            if name=='Maresca':
                grip=bpy.data.objects['Maresca / badge grip '+str(side)].matrix_world.translation
                worst_grip=max(worst_grip,(grip.xy-hand.xy).length)
assert max(worst_neck,worst_arm,worst_grip,foot_drift)<1e-5
assert bpy.data.objects['Badge / cord'].hide_render
assert all(i.packed_file for i in bpy.data.images if i.name=='head-expressions.png')
assert all(st.mute==not_selected for st,not_selected in [(st,not st.name.startswith('B ')) for st in s.sequence_editor.strips])
report={'scope':'Reopened exact native revision; all 192 frames','neck_max_gap':worst_neck,'arm_max_gap':worst_arm,'badge_grip_max_gap':worst_grip,'foot_drift':foot_drift,'one_visible_drawing_per_character_per_frame':True,'new_art_packed':True,'badge_cord_hidden':True,'sound':'B active; A muted','creative_review':'These checks do not establish natural acting or smoothness to the viewer.'}
(OUT/'reopen-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
