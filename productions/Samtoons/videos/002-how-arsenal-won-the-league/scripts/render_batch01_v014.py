"""Check preserved construction, then stream the chronological review at 24fps."""
import bpy,json,math,subprocess,sys
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/batch01-v014';rows=json.loads((O/'edit.json').read_text());ff='/opt/homebrew/bin/ffmpeg'
original=json.loads((V/'artifacts/batch01-v013/protected-motion.json').read_text());maps=json.loads((O/'time-maps.json').read_text());checks={'actors':{},'fps':24,'frames':1021,'scope':'Geometry, retained controls and timing only. User playback acceptance still pending.'}
def area(a,b,c):return (b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x)
for name,times in maps.items():
 prefix='B01 / '+name+' / ';s=bpy.data.scenes['S002_B01_v014_'+('opening' if name.startswith('opening') else 'unveiling')];bpy.context.window.scene=s;skin=bpy.data.objects[prefix+'connected upper body'];s.frame_set(1);bpy.context.view_layer.update();ev=skin.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();ref=[v.co.copy() for v in me.vertices];ev.to_mesh_clear()
 polygons=[tuple(p.vertices) for p in skin.data.polygons if len(p.vertices)==4 and (all(28<=i<80 for i in p.vertices) or all(92<=i<144 for i in p.vertices))]
 flips=[];drift=0;anchors={};worst_matrix=0;checked=0
 for f,source_frame in enumerate(times,1):
  s.frame_set(f);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();ev=skin.evaluated_get(dg);me=ev.to_mesh()
  for poly in polygons:
   for j in range(1,len(poly)-1):
    ix=[poly[0],poly[j],poly[j+1]];aa=area(*(ref[i] for i in ix));bb=area(*(me.vertices[i].co for i in ix))
    if abs(aa)>1e-6 and bb/aa<-.0001:flips.append([f,ix])
  ev.to_mesh_clear()
  if abs(source_frame-round(source_frame))<1e-6:
   expected=original['actors'][name][round(source_frame)-1][1]
   for key,values in zip(original['keys'],expected):
    obj=bpy.data.objects[prefix+'CTRL '+key];got=[v for row in obj.matrix_world for v in row];worst_matrix=max(worst_matrix,max(abs(x-y) for x,y in zip(got,values)))
   checked+=1
  for side,first,last in [('L',43,56),('R',60,73)]:
   if name!='unveiling Gyokeres' or f<=first or f>=last:
    key=(side,0 if name!='unveiling Gyokeres' or f<=first else 1);foot=bpy.data.objects[prefix+'CTRL '+side+' boot'];pos=foot.matrix_world@Vector((0,-22,0))
    if key not in anchors:anchors[key]=pos.copy()
    drift=max(drift,(pos-anchors[key]).length)
 checks['actors'][name]={'sleeve_flipped_triangles':len(flips),'flipped_samples':flips[:6],'retained_pose_frames':checked,'max_control_matrix_difference':worst_matrix,'planted_sole_anchor_drift_m':drift,'source_image_used_for_head_and_clothes':True}
 assert worst_matrix<.00001,(name,'original pose changed',worst_matrix)
 assert drift<.003,(name,'sole sliding',drift)
 assert not flips,(name,'folded sleeve',flips[:5])
(O/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print('CHECKS_PASSED',flush=True)
if '--check-only' in sys.argv:raise SystemExit(0)
(O/'frames').mkdir(exist_ok=True);temp=O/'working-frame.png'
p=subprocess.Popen([ff,'-v','error','-y','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(O/'picture.mp4')],stdin=subprocess.PIPE);count=0
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
subprocess.run([ff,'-v','error','-y','-i',str(O/'picture.mp4'),'-i',str(V/'artifacts/opening-v002/mix-premaster.wav'),'-filter_complex','[1:a]atrim=start_sample=0:end_sample=2042000,asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(O/'batch01-review-v014.mp4')],check=True)
print('BATCH01_REVIEW_COMPLETE',flush=True)
