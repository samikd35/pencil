"""Render the complete review animatic at 960x540/24fps; not full-quality delivery."""
from pathlib import Path
import bpy,json,subprocess,time,shutil,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/animatic-v001'
FINAL='--final-v001' in sys.argv
if FINAL:
 sys.path.insert(0,str(ROOT.parents[3]))
 from pipeline.checkpoints import require_checkpoint
 for stage in ('staging','sound','animatic'):require_checkpoint(ROOT,'animatic-v004',stage)
VAR_LINE='--revision-v004' in sys.argv
REVISION='--revision-v003' in sys.argv or VAR_LINE
PREVIOUS='animatic-v003' if VAR_LINE else 'animatic-v002'
REPAIR='--repair-v002' in sys.argv
if REPAIR:OUT=ROOT/'artifacts/animatic-v002'
if REVISION:OUT=ROOT/('artifacts/animatic-v004' if VAR_LINE else 'artifacts/animatic-v003')
if FINAL:OUT=ROOT/'artifacts/delivery-v001'
ONLY='--ending-only' in sys.argv or '--repair-tail' in sys.argv
SELECTED=(13,14,15) if '--repair-tail' in sys.argv else (15,)
REDO=set(map(int,sys.argv[sys.argv.index('--shots')+1].split(','))) if '--shots' in sys.argv else set()
CLIPS='tail-selected' if ONLY else 'picture-selected'
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'artifacts/animatic-v004/combined-animatic-v004.blend' if FINAL else OUT/('combined-animatic-v004.blend' if VAR_LINE else 'combined-animatic-v003.blend' if REVISION else 'combined-animatic-v002.blend' if REPAIR else 'combined-animatic-v006.blend')))
if FINAL:
 for scene in bpy.data.scenes:
  scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=100;scene.eevee.taa_render_samples=64
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'samtoons-final.blend'))
(OUT/CLIPS).mkdir(exist_ok=True)
edit=json.loads((OUT/'edit.json').read_text());start=time.monotonic();done=[]
total_frames=sum(r['frames'] for r in edit)
windows={0:(100,133),4:(14,65),5:(95,135),7:(14,73),8:(14,79),9:(45,100),12:(45,102),13:(101,130),15:(180,254)}
if REPAIR or REVISION:(OUT/'inspection-frames').mkdir(exist_ok=True)
if REVISION:
 windows={6:(40,180)} if VAR_LINE else {15:(25,144),16:(198,312)}
 previous=json.loads((ROOT/'artifacts'/PREVIOUS/'edit.json').read_text())
 changed=json.loads((OUT/'changed-scenes.json').read_text())
for i,row in enumerate(edit):
 if ONLY and i not in SELECTED:continue
 if REDO and i not in REDO:done.append(row);continue
 s=bpy.data.scenes[row['scene']];bpy.context.window.scene=s;s.render.use_sequencer=False;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=75;s.eevee.taa_render_samples=8
 if FINAL:s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100;s.eevee.taa_render_samples=64
 assert s.render.fps==24 and s.render.fps_base==1 and s.frame_end==row['frames']
 target=OUT/CLIPS/f'picture-{i:02}.mp4';tmp=OUT/CLIPS/'working-frame.png'
 if REVISION and row['scene'] not in changed:
  oldi=next(j for j,x in enumerate(previous) if x['scene']==row['scene'])
  shutil.copy2(ROOT/'artifacts'/PREVIOUS/'picture-selected'/f'picture-{oldi:02}.mp4',target);done.append(row);continue
 if REPAIR and i in (1,2,6,10,11,14):
  folder='tail-selected' if i==14 else 'picture-selected'
  source=ROOT/'artifacts/animatic-v001'/folder/f'picture-{i:02}.mp4'
  shutil.copy2(source,target);done.append(row);continue
 if REPAIR and i==3:
  shutil.copy2(ROOT/'artifacts/repair-v002/picture.mp4',target);done.append(row);continue
 if i==1 and not FINAL:
  shutil.copy2(OUT/'picture-01.mp4',target);done.append(row);continue
 if REDO and target.exists():target.replace(target.with_suffix('.before-qa.mp4'))
 assert not target.exists(),target
 with (OUT/f'encode-{i:02}.log').open('w') as log:
  enc=subprocess.Popen(['/opt/homebrew/bin/ffmpeg','-v','error','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','14' if FINAL else '19','-pix_fmt','yuv420p','-movflags','+faststart',str(target)],stdin=subprocess.PIPE,stderr=log)
  try:
   for f in range(1,s.frame_end+1):
    s.frame_set(f);s.render.filepath=str(tmp);bpy.ops.render.render(write_still=True);enc.stdin.write(tmp.read_bytes())
    if f in (1,57,77,84,110,120,154,221,s.frame_end):(OUT/(('repair-' if ONLY else '')+f'frame-{i:02}-{f:03}.png')).write_bytes(tmp.read_bytes())
    if (REPAIR or REVISION) and i in windows and windows[i][0]<=f<=windows[i][1]:(OUT/'inspection-frames'/f'{i:02}-{f:03}.png').write_bytes(tmp.read_bytes())
    if f%48==0:
     (OUT/('progress-ending.json' if ONLY else 'progress.json')).write_text(json.dumps(dict(scene=i+1,scenes=len(edit),frame=f,scene_frames=s.frame_end,total_completed=sum(x['frames'] for x in done)+f,total_frames=total_frames,elapsed_seconds=time.monotonic()-start)))
   enc.stdin.close();assert enc.wait()==0
  except BaseException:enc.kill();enc.wait();raise
 done.append(row);print('SHOT_COMPLETE',i,row['scene'],flush=True)
 tmp.unlink(missing_ok=True)
if ONLY:print('ENDING_COMPLETE',flush=True);sys.exit(0)
if REDO and (OUT/'picture-selected.mp4').exists():(OUT/'picture-selected.mp4').replace(OUT/'picture-before-qa.mp4')
(OUT/'concat.txt').write_text(''.join(f"file 'picture-selected/picture-{i:02}.mp4'\n" for i in range(len(edit))))
subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-c','copy','-movflags','+faststart',str(OUT/'picture-selected.mp4')],check=True)
(OUT/'render-checks.json').write_text(json.dumps(dict(frames=total_frames,fps=24,seconds=total_frames/24,resolution=[1920,1080] if FINAL else [960,540],shots=len(edit),native_reopened=True,elapsed_seconds=time.monotonic()-start,quality='Full-resolution render of approved animatic-v004' if FINAL else 'Combined animatic, not final delivery'),indent=2)+'\n')
print('COMPLETE',flush=True)
