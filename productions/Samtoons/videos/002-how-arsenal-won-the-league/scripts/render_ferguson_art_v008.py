"""Check the native construction, then encode one actual dialogue shot."""
import bpy,json,subprocess,math
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v008';s=bpy.data.scenes['S002_v008_Ferguson_dialogue'];bpy.context.window.scene=s
col=bpy.data.collections['S002 / Ferguson native artwork v008'];room=bpy.data.collections['S002 / Narrator room / shared v005'];assert room in list(s.collection.children)
assert all(node.type!='TEX_IMAGE' for o in col.objects if o.type in ['MESH','CURVE'] for m in o.data.materials if m.use_nodes for node in m.node_tree.nodes)
# Preserve the user's positively reviewed control motion exactly.
old=bpy.data.scenes['S002_v007_Ferguson_dialogue'];controls=[o for o in col.objects if 'CTRL ' in o.name];max_control_delta=0
for f in range(1,169):
 bpy.context.window.scene=old;old.frame_set(f);bpy.context.view_layer.update()
 original={o.name:bpy.data.objects[o.name.replace('F8 /','F7 /')].matrix_world.copy() for o in controls}
 bpy.context.window.scene=s;s.frame_set(f);bpy.context.view_layer.update()
 for o in controls:
  max_control_delta=max(max_control_delta,max(abs(a-b) for ra,rb in zip(o.matrix_world,original[o.name]) for a,b in zip(ra,rb)))
assert max_control_delta<1e-6,max_control_delta
garment=bpy.data.objects['F8 / unified cardigan cloth']
assert len(garment.data.shape_keys.key_blocks)==168
adjacent={v.index:set() for v in garment.data.vertices}
for edge in garment.data.edges:
 a,b=edge.vertices;adjacent[a].add(b);adjacent[b].add(a)
reached=set();pending=[0]
while pending:
 v=pending.pop()
 if v not in reached:reached.add(v);pending.extend(adjacent[v]-reached)
assert len(reached)==len(garment.data.vertices),'Disconnected garment topology'
assert bpy.data.objects['F8 / cardigan body outline'].hide_render
# Fixed support and rigid articulated segments are checked throughout, not just at keys.
origins={};max_drift=0;mouths=set()
for f in range(1,169):
 s.frame_set(f);bpy.context.view_layer.update()
 for side in ['L','R']:
  for i in range(4):
   assert bpy.data.objects[f'F8 / {side} finger tip {i}'].hide_render==bpy.data.objects[f'F8 / {side} hand finger {i}'].hide_render,(f,side,i)
 for side in ['L','R']:
  o=bpy.data.objects['F8 / CTRL '+side+' boot'];p=o.matrix_world.translation.copy()
  if side not in origins:origins[side]=p
  max_drift=max(max_drift,(p-origins[side]).length)
 active=[]
 for label in ['rest','MBP','A','E','O','U','FV','L']:
  group=bpy.data.objects['F8 / CTRL mouth '+label]
  if any(not o.hide_render for o in group.children_recursive if o.type in ['MESH','CURVE']):active.append(label)
 assert len(active)==1,(f,active);mouths.update(active)
assert max_drift<1e-5,max_drift
checks={'native_character_no_image_textures':True,'same_shared_room':True,'one_connected_cardigan_boundary':True,'new_finger_details_follow_hand_exposure':True,'control_world_matrix_max_delta_from_v007':max_control_delta,'foot_control_max_drift_m':max_drift,'one_mouth_per_frame':True,'used_mouth_shapes':sorted(mouths),'review_scope':'Construction and draft dialogue performance. Not approval of appearance, acting or final lip sync.'}
(O/'native-checks.json').write_text(json.dumps(checks,indent=2))
(O/'frames').mkdir(exist_ok=True)
full=bpy.data.scenes['S002_v008_Ferguson_full_body']
for f in [7,43,81,121]:
 bpy.context.window.scene=full;full.frame_set(f);full.render.image_settings.file_format='PNG';full.render.filepath=str(O/'frames'/f'full-body-{f:03}.png');bpy.ops.render.render(write_still=True)
bpy.context.window.scene=s
s.render.use_sequencer=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.resolution_percentage=100;s.eevee.taa_render_samples=16
(O/'frames').mkdir(exist_ok=True);temp=O/'working-frame.png';ff='/opt/homebrew/bin/ffmpeg'
p=subprocess.Popen([ff,'-v','error','-y','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(O/'dialogue-picture.mp4')],stdin=subprocess.PIPE)
try:
 for f in range(1,169):
  s.frame_set(f);s.render.filepath=str(temp);bpy.ops.render.render(write_still=True);raw=temp.read_bytes();p.stdin.write(raw)
  if f in [1,7,15,25,39,43,48,58,66,73,81,93,100,111,121,125,132,156]: (O/'frames'/f'{f:03}.png').write_bytes(raw)
 p.stdin.close();assert p.wait()==0
except BaseException:p.kill();p.wait();raise
temp.unlink(missing_ok=True)
row=next(r for r in json.loads((V/'artifacts/animation-v003/edit.json').read_text()) if r['id']=='N04_meltdown');start=(row['start_frame']-1)*2000
subprocess.run([ff,'-v','error','-y','-i',str(O/'dialogue-picture.mp4'),'-i',str(V/'artifacts/opening-v002/mix-premaster.wav'),'-filter_complex',f'[1:a]atrim=start_sample={start}:end_sample={start+168*2000},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(O/'ferguson-native-dialogue-v008.mp4')],check=True)
print('DIALOGUE_CANDIDATE_COMPLETE',flush=True)
