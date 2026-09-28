"""Read-only v006 audit; optional single-variable renders are never saved as production.
Run Blender -b <v006/call-performance.blend> --python this_file [-- --ablate].
The assertion deliberately exposes silent hand-orientation overrides, not visual quality.
"""
import ast,hashlib,json,math,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
V=ROOT/'productions/Samtoons/videos/003-barca-emergency-meeting'
source=V/'scripts/build_call_performance_v006.py'
tree=ast.parse(source.read_text())
beats=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='BEATS' for t in n.targets))
# Execute only the actual scalar interpolation helper; importing a builder would mutate state.
tree=ast.parse((V/'scripts/build_call_performance_v002.py').read_text())
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='interp')
ns={};exec(compile(ast.Module(body=[fn],type_ignores=[]),'existing_interp','exec'),ns);interp=ns['interp']
s=bpy.context.scene;assert s.name=='S003_S08_Call_Performance_v006'
assert Path(bpy.data.filepath).resolve()==(V/'artifacts/staging-v001/call-performance-v006/call-performance.blend').resolve()
wrap=lambda a:(a+180)%360-180
report={'source_movie_sha256':hashlib.sha256((V/'artifacts/staging-v001/call-performance-v006/call-review.mp4').read_bytes()).hexdigest(),'actors':{},'scope':'hand direction versus authored target; no visual-quality verdict'}
for who in ['Muller','Perez']:
 rig=s.objects['C3V6 / '+who+' fitted drawing rig'];rows=[];gap=0
 for f in range(1,241):
  s.frame_set(f);bpy.context.view_layer.update();fore=rig.pose.bones['L fore'];hand=rig.pose.bones['L hand'];v=hand.tail-hand.head;u=fore.tail-fore.head
  actual=math.degrees(math.atan2(v.y,v.x));desired=90+interp(f,beats[who]['hand']);relative=math.degrees(math.atan2(u.x*v.y-u.y*v.x,u.x*v.x+u.y*v.y))
  gap=max(gap,(fore.tail-hand.head).length)
  rows.append({'frame':f,'desired_degrees':desired,'actual_degrees':actual,'error_degrees':abs(wrap(actual-desired)),'relative_degrees':relative})
 report['actors'][who]={'max_joint_gap_source_pixels':gap,'frames_at_limit':sum(abs(abs(r['relative_degrees'])-40)<.01 for r in rows),'frames_over_one_degree_error':sum(r['error_degrees']>1 for r in rows),'worst':max(rows,key=lambda r:r['error_degrees']),'frames':rows}
report['assertion_passed']=all(a['worst']['error_degrees']<=1 for a in report['actors'].values())
(HERE/'pose-audit.json').write_text(json.dumps(report,indent=2)+'\n')
if '--ablate' in sys.argv:
 s.render.use_sequencer=False;s.render.image_settings.file_format='PNG';out=HERE/'evidence'
 for who,f in [('Perez',150),('Muller',215)]:
  s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(out/f'{who.lower()}-{f}-native.png');bpy.ops.render.render(write_still=True)
  row=report['actors'][who]['frames'][f-1];rig=s.objects['C3V6 / '+who+' fitted drawing rig'];action=rig.animation_data.action;rig.animation_data.action=None;pb=rig.pose.bones['L hand'];pb.rotation_euler.z+=math.radians(wrap(row['desired_degrees']-row['actual_degrees']));bpy.context.view_layer.update()
  s.render.filepath=str(out/f'{who.lower()}-{f}-without-clamp.png');bpy.ops.render.render(write_still=True)
  assert (out/f'{who.lower()}-{f}-native.png').read_bytes()!=(out/f'{who.lower()}-{f}-without-clamp.png').read_bytes(),'Ablation did not change the render'
  rig.animation_data.action=action
 s.frame_set(150)
for who,a in report['actors'].items():print('POSE_AUDIT',who,'limit_frames',a['frames_at_limit'],'max_error',round(a['worst']['error_degrees'],3),'frame',a['worst']['frame'],flush=True)
assert report['assertion_passed'],'Authored hand direction silently overridden; this is a diagnostic failure, not a disconnected-bone failure.'
