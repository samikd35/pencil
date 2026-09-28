"""Render the bounded first-batch review directly from its saved native scenes."""
import bpy,json,subprocess,math
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/batch01-v010';rows=json.loads((O/'edit.json').read_text());ff='/opt/homebrew/bin/ffmpeg'
# The manifest contains timing and native scene references, not storyboard movie sources.
rows=[{k:r[k] for k in ['id','start_frame','frames','scene','local_start']} for r in rows]
(O/'edit.json').write_text(json.dumps(rows,indent=2)+'\n')
assert sum(r['frames'] for r in rows)==1021
checks={'native_character_surfaces':True,'connected_garments':{},'support_drift_m':{},'mouth_exposure':{},'frames':1021,'fps':24,'width':1280,'height':720,'status':'Technical checks do not establish user acceptance of likeness or performance.'}
for actor,scene in [('opening Arteta','opening'),('banner worker','opening'),('delivery driver','opening'),('unveiling Gyokeres','unveiling'),('unveiling Arteta','unveiling')]:
 p='B01 / '+actor+' / ';col=bpy.data.collections['B01 / '+actor]
 assert all(node.type!='TEX_IMAGE' for o in col.objects if o.type in ['MESH','CURVE'] for m in o.data.materials if m and m.use_nodes for node in m.node_tree.nodes)
 body=bpy.data.objects[p+'connected upper body'];adj={v.index:set() for v in body.data.vertices}
 for edge in body.data.edges:
  a,b=edge.vertices;adj[a].add(b);adj[b].add(a)
 seen=set();todo=[0]
 while todo:
  v=todo.pop()
  if v not in seen:seen.add(v);todo.extend(adj[v]-seen)
 assert len(seen)==len(adj),(actor,'garment disconnected');checks['connected_garments'][actor]=True
 s=bpy.data.scenes['S002_B01_v010_'+scene];bpy.context.window.scene=s;used=set();max_drift=0;anchors={}
 for f in range(1,s.frame_end+1):
  s.frame_set(f);bpy.context.view_layer.update()
  active=[]
  for label in ['rest','MBP','A','E','O','U','FV','L']:
   g=bpy.data.objects[p+'CTRL mouth '+label]
   if any(not ob.hide_render for ob in g.children_recursive if ob.type in ['MESH','CURVE']):active.append(label)
  assert len(active)==1,(actor,f,active);used.update(active)
  # Relative to the character root: truck carries its seated driver; worker has an exposure cut.
  root=bpy.data.objects[p+'CTRL character']
  if max(abs(v) for v in root.matrix_world.to_scale())<1e-8:continue
  inv=root.matrix_world.inverted()
  for side in ['L','R']:
   planted=True;phase=0
   if actor=='unveiling Gyokeres':
    first,last=(53,76) if side=='R' else (82,105);planted=f<=first or f>=last;phase=0 if f<=first else 1
   if planted:
    point=inv@bpy.data.objects[p+'CTRL '+side+' boot'].matrix_world.translation;k=(side,phase)
    if k not in anchors:anchors[k]=point
    max_drift=max(max_drift,(point-anchors[k]).length)
 assert max_drift<.002,(actor,max_drift)
 checks['support_drift_m'][actor]=max_drift*abs(root.scale.x);checks['mouth_exposure'][actor]=sorted(used)
(O/'native-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
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
subprocess.run([ff,'-v','error','-y','-i',str(O/'picture.mp4'),'-i',str(V/'artifacts/opening-v002/mix-premaster.wav'),'-filter_complex','[1:a]atrim=start_sample=0:end_sample=2042000,asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(O/'batch01-review-v010.mp4')],check=True)
print('BATCH01_REVIEW_COMPLETE',flush=True)
