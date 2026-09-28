"""Render and validate the bounded first-batch illustrated-rig review."""
import bpy,json,subprocess,math,sys
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/batch01-v012'
rows=json.loads((O/'edit.json').read_text());registry=json.loads((O/'cast-registry.json').read_text());ff='/opt/homebrew/bin/ffmpeg'
assert sum(r['frames'] for r in rows)==1021
checks={'frames':1021,'fps':24,'actors':{},'scope':'Technical checks and inspected frames; creative playback acceptance remains pending.'}
for name,row in registry.items():
 skin=bpy.data.objects[row['skin']];arm=bpy.data.objects[row['armature']];s=next(s for s in bpy.data.scenes if s.name=='S002_B01_v012_'+('opening' if name.startswith('opening') else 'unveiling'));bpy.context.window.scene=s
 assert skin.modifiers[0].object==arm and not skin.hide_render
 assert all(len(p.vertices)==3 for p in skin.data.polygons)
 assert all(abs(sum(g.weight for g in v.groups)-1)<1e-5 for v in skin.data.vertices)
 assert any(node.type=='TEX_IMAGE' for m in skin.data.materials if m.use_nodes for node in m.node_tree.nodes)
 assert len(skin.data.shape_keys.key_blocks)==2
 sole={side:[] for side in ['L','R']}
 for v in skin.data.vertices:
  if v.co.y<18:sole['L' if v.co.x<0 else 'R'].append(v.index)
 assert all(sole.values())
 anchors={};worst=0;mouths=set();max_neck_scale=0
 for f in range(1,s.frame_end+1):
  s.frame_set(f);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();ev=skin.evaluated_get(dg);me=ev.to_mesh()
  for side,indices in sole.items():
   first,last=(53,76) if side=='R' else (82,105)
   planted=name!='unveiling Gyokeres' or f<=first or f>=last;phase=0 if name!='unveiling Gyokeres' or f<=first else 1
   if planted:
    # Evaluated sole vertices, not just ankle controls, must remain planted.
    points=[ev.matrix_world@me.vertices[i].co for i in indices];k=(side,phase)
    if k not in anchors:anchors[k]=[p.copy() for p in points]
    worst=max(worst,max((p-first).length for p,first in zip(points,anchors[k])))
  ev.to_mesh_clear()
  active=[]
  for label in ['MBP','A','E','O','U','FV','L']:
   group=bpy.data.objects[row['controls']['mouth '+label]]
   if any(not ob.hide_render for ob in group.children_recursive if ob.type in ['MESH','CURVE']):active.append(label)
  assert len(active)<=1,(name,f,active);mouths.update(active or ['rest'])
 assert worst<.002,(name,worst)
 checks['actors'][name]={'continuous_textured_mesh':True,'fitted_bones':len(arm.data.bones),'native_eyelid_shape_key':True,'mouth_shapes':sorted(mouths),'evaluated_planted_sole_max_drift_m':worst,'vertices':len(skin.data.vertices)}
(O/'native-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
if '--check-only' in sys.argv:raise SystemExit(0)
(O/'frames').mkdir(exist_ok=True);temp=O/'working-frame.png'
p=subprocess.Popen([ff,'-v','error','-y','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(O/'picture.mp4')],stdin=subprocess.PIPE)
count=0
try:
 for row in rows:
  s=bpy.data.scenes[row['scene']];bpy.context.window.scene=s;s.render.use_sequencer=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.resolution_percentage=100;s.eevee.taa_render_samples=16
  print('SHOT_START',row['id'],flush=True)
  for f in range(row['local_start'],row['local_start']+row['frames']):
   s.frame_set(f)
   if s.timeline_markers:s.camera=max((m for m in s.timeline_markers if m.frame<=f and m.camera),key=lambda m:m.frame).camera
   s.render.filepath=str(temp);bpy.ops.render.render(write_still=True);raw=temp.read_bytes();p.stdin.write(raw);count+=1
   if f in [row['local_start'],row['local_start']+row['frames']//2,row['local_start']+row['frames']-1]:(O/'frames'/f'{row["id"]}-{f:03}.png').write_bytes(raw)
  print('SHOT_DONE',row['id'],count,flush=True)
 p.stdin.close();assert p.wait()==0
except BaseException:p.kill();p.wait();raise
temp.unlink(missing_ok=True);assert count==1021
subprocess.run([ff,'-v','error','-y','-i',str(O/'picture.mp4'),'-i',str(V/'artifacts/opening-v002/mix-premaster.wav'),'-filter_complex','[1:a]atrim=start_sample=0:end_sample=2042000,asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(O/'batch01-review-v012.mp4')],check=True)
print('BATCH01_REVIEW_COMPLETE',flush=True)
