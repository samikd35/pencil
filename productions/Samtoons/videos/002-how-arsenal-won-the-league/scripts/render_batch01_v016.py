"""Stream ten staged shots, retain contiguous frames for actual motion-detail inspection."""
import bpy,json,subprocess,time,numpy as np
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/batch01-v016';rows=json.loads((O/'edit.json').read_text());cast=json.loads((O/'cast.json').read_text());checks={};st=time.monotonic()
for name,a in cast.items():
 s=bpy.data.scenes[a['scene']];bpy.context.window.scene=s;skin=bpy.data.objects[a['skin']];base=np.array([v.co[:2] for v in skin.data.vertices]);uv={l.vertex_index:skin.data.uv_layers.active.data[l.index].uv[:] for l in skin.data.loops};im=next(n.image for n in skin.data.materials[0].node_tree.nodes if n.type=='TEX_IMAGE');pix=np.empty(1536*1024*4,dtype=np.float32);im.pixels.foreach_get(pix);alpha=pix.reshape(1024,1536,4)[:,:,3]
 def visible(poly):
  p=np.mean([uv[i] for i in poly.vertices],axis=0);return alpha[min(1023,max(0,int(p[1]*1024))),min(1535,max(0,int(p[0]*1536)))]>.95
 tri=np.array([p.vertices[:] for p in skin.data.polygons if visible(p)]);ab=base[tri[:,1]]-base[tri[:,0]];ac=base[tri[:,2]]-base[tri[:,0]];ar=ab[:,0]*ac[:,1]-ab[:,1]*ac[:,0];frames=[]
 for f in range(1,s.frame_end+1):
  s.frame_set(f);bpy.context.view_layer.update();ev=skin.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();pts=np.array([v.co[:2] for v in me.vertices]);ab=pts[tri[:,1]]-pts[tri[:,0]];ac=pts[tri[:,2]]-pts[tri[:,0]];ratio=(ab[:,0]*ac[:,1]-ab[:,1]*ac[:,0])/ar;ev.to_mesh_clear();assert np.isfinite(ratio).all();frames.append({'frame':f,'projected_inversions':int((ratio<=0).sum()),'minimum_area_ratio':float(ratio.min()),'maximum_area_ratio':float(ratio.max())})
 checks[name]={'frames':frames,'worst_projected_inversions':max(r['projected_inversions'] for r in frames),'scope':'Projected triangle changes, including deliberate arm overlap; not creative acceptance. Visually inspect reported frames.'}
(O/'geometry-audit.json').write_text(json.dumps(checks,indent=2));print('AUDIT_COMPLETE', {k:v['worst_projected_inversions'] for k,v in checks.items()},flush=True)
(O/'frames').mkdir(exist_ok=True);out=O/'batch01-review-v016.mp4';assert not out.exists();temp=O/'working-frame.png'
cmd=['/opt/homebrew/bin/ffmpeg','-v','error','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-i',str(V/'artifacts/opening-v002/mix-premaster.wav'),'-map','0:v','-map','1:a','-t',str(1021/24),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)]
with (O/'encode.log').open('w') as log:
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log);count=0
 try:
  for row in rows:
   s=bpy.data.scenes[row['scene']];bpy.context.window.scene=s;s.render.use_sequencer=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.resolution_percentage=100;s.eevee.taa_render_samples=16
   print('SHOT_START',row['id'],flush=True)
   for f in range(row['local_start'],row['local_start']+row['frames']):
    s.frame_set(f)
    if s.timeline_markers:s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=f),key=lambda m:m.frame).camera
    s.render.filepath=str(temp);bpy.ops.render.render(write_still=True);raw=temp.read_bytes();p.stdin.write(raw);count+=1
    focused=(row['id']=='TR01' and (20<=f<=30 or 40<=f<=76)) or (row['id']=='OP03_phone' and 336<=f<=352) or (row['id']=='TR02_reaction' and 300<=f<=320)
    if focused or f in [row['local_start'],row['local_start']+row['frames']//2,row['local_start']+row['frames']-1]:(O/'frames'/f'{row["id"]}-{f:03}.png').write_bytes(raw)
   print('SHOT_DONE',row['id'],count,round(time.monotonic()-st,1),flush=True)
  p.stdin.close();assert p.wait()==0
 except BaseException:p.kill();p.wait();raise
assert count==1021;temp.unlink(missing_ok=True);(O/'render-checks.json').write_text(json.dumps({'frames':count,'fps':24,'seconds':count/24,'source_mix':'artifacts/opening-v002/mix-premaster.wav','status':'Review candidate; no user acceptance inferred','elapsed_seconds':time.monotonic()-st},indent=2));print('BATCH_COMPLETE',flush=True)
