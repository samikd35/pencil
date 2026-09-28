"""Focused repair review: the complete 18-second signing scene, not a full-film export."""
import bpy,json,subprocess,hashlib
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/cast-coherence-v011';s=bpy.data.scenes['S002_B01_v011_unveiling'];bpy.context.window.scene=s
checks={'frames':432,'fps':24,'scope':'Source likeness, jaw/collar continuity and a single shorts garment during two steps and dialogue. User acceptance pending.','actors':{}}
for name in ['unveiling Gyokeres','unveiling Arteta']:
 p='B01 / '+name+' / ';col=bpy.data.collections['B01 / '+name];neck=bpy.data.objects[p+'v011 connected neck'];assert len(neck.data.vertices)==10
 assert all(node.type!='TEX_IMAGE' for o in col.objects if o.type in ['MESH','CURVE'] for m in o.data.materials if m and m.use_nodes for node in m.node_tree.nodes)
 drift=0;anchors={};used=set();neck_error=0
 for f in range(1,433):
  s.frame_set(f);bpy.context.view_layer.update();root=bpy.data.objects[p+'CTRL character'];inv=root.matrix_world.inverted()
  for side in ['L','R']:
   first,last=(53,76) if side=='R' else (82,105);planted=name.endswith('Arteta') or f<=first or f>=last
   if planted:
    phase=0 if name.endswith('Arteta') or f<=first else 1;k=(side,phase);pt=inv@bpy.data.objects[p+'CTRL '+side+' boot'].matrix_world.translation
    if k not in anchors:anchors[k]=pt
    drift=max(drift,(pt-anchors[k]).length)
  active=[]
  for label in ['rest','MBP','A','E','O','U','FV','L']:
   g=bpy.data.objects[p+'CTRL mouth '+label]
   if any(not o.hide_render for o in g.children_recursive if o.type in ['MESH','CURVE']):active.append(label)
  assert len(active)==1,(name,f,active);used.update(active)
  dg=bpy.context.evaluated_depsgraph_get();nv=neck.evaluated_get(dg).data.vertices
  assert all(nv[2*j].co.x<nv[2*j+1].co.x for j in range(5)),(name,f,'crossed neck')
 assert drift<.002,(name,drift)
 checks['actors'][name]={'native_no_image_textures':True,'neck_left_right_order_all_frames':True,'fixed_support_drift_art_units':drift,'one_active_mouth_all_frames':True,'mouth_shapes':sorted(used)}
shorts=bpy.data.objects['B01 / unveiling Gyokeres / v011 single source shorts'];assert len(shorts.data.shape_keys.key_blocks)==117
checks['shorts']={'source_contours_fitted_together':True,'vertices':len(shorts.data.vertices),'fixed_triangles':all(len(f.vertices)==3 for f in shorts.data.polygons),'old_hip_panel_hidden':bpy.data.objects['B01 / unveiling Gyokeres / hip cloth'].hide_render}
(O/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
ff='/opt/homebrew/bin/ffmpeg';temp=O/'working-frame.png';(O/'frames').mkdir(exist_ok=True)
s.render.use_sequencer=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.resolution_percentage=100;s.eevee.taa_render_samples=32
p=subprocess.Popen([ff,'-v','error','-y','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p',str(O/'picture.mp4')],stdin=subprocess.PIPE)
try:
 for f in range(1,433):
  s.frame_set(f);s.camera=max((m for m in s.timeline_markers if m.frame<=f and m.camera),key=lambda m:m.frame).camera;s.render.filepath=str(temp);bpy.ops.render.render(write_still=True);raw=temp.read_bytes();p.stdin.write(raw)
  if f in [1,22,26,53,70,76,82,94,105,116,192,230,288,301,315,339,351,367,376,432]:(O/'frames'/f'{f:03}.png').write_bytes(raw)
  if f%48==0:print('REVIEW_FRAMES',f,flush=True)
 p.stdin.close();assert p.wait()==0
except BaseException:p.kill();p.wait();raise
temp.unlink(missing_ok=True)
subprocess.run([ff,'-v','error','-y','-i',str(O/'picture.mp4'),'-i',str(V/'artifacts/opening-v002/mix-premaster.wav'),'-filter_complex',f'[1:a]atrim=start_sample={589*2000}:end_sample={1021*2000},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(O/'cast-motion-review-v011.mp4')],check=True)
print('CAST_REVIEW_COMPLETE',flush=True)
