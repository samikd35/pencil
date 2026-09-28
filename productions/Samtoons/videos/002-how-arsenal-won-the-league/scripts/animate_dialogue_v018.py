"""Visible Blender revision: retain v017 artwork/actions, insert speaking holds and refit lips."""
import bpy,json,math,subprocess,ast
from pathlib import Path
from mathutils import Vector
import numpy as np
V=Path(__file__).resolve().parents[1];O=V/'artifacts/dialogue-v018';n=bpy.app.driver_namespace['batch16'];b17=bpy.app.driver_namespace['b17'];curves=n['curves']
rows=json.loads((O/'edit.json').read_text());ins=json.loads((O/'insertions.json').read_text());plan=json.loads((O/'audio-plan.json').read_text());shots={s['id']:s for s in plan['shots']};words=json.loads((O/'word-analysis.json').read_text());report={}
assert not bpy.app.driver_namespace.get('dialogue18_retimed'),'Do not retime twice; reload the preserved v017 native file first.'
def mapframe(f,items):return f+sum(delta for point,delta in items if f>point)
for name,items in ins.items():
 s=bpy.data.scenes[name];ids={s}
 for ob in s.objects:
  ids.add(ob)
  if ob.data:
   ids.add(ob.data)
   if hasattr(ob.data,'shape_keys') and ob.data.shape_keys:ids.add(ob.data.shape_keys)
 actions=set();count=0
 for ob in ids:
  if not getattr(ob,'animation_data',None) or not ob.animation_data.action:continue
  act=ob.animation_data.action
  if act in actions:continue
  actions.add(act)
  for fc in curves(ob):
   values=[(point,delta,fc.evaluate(point)) for point,delta in items];keys=list(fc.keyframe_points)
   for k in keys:
    dx=mapframe(k.co.x,items)-k.co.x
    k.co.x+=dx;k.handle_left.x+=dx;k.handle_right.x+=dx
   for point,delta,val in values:
    for t in [mapframe(point,items),mapframe(point,items)+delta]:
     k=fc.keyframe_points.insert(t,val,options={'FAST'});k.interpolation='CONSTANT' if fc.data_path in ['hide_render','hide_viewport'] else 'LINEAR'
   fc.update();count+=1
 for m in s.timeline_markers:m.frame=round(mapframe(m.frame,items))
 s.frame_end+=sum(d for p,d in items);report[name]={'curves':count,'frames':s.frame_end}
bpy.app.driver_namespace['dialogue18_retimed']=True
# The same lip builder, with this revision's audio and actual word timing.
source=V/'scripts/continue_batch02_v017.py';tree=ast.parse(source.read_text());node=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='lips');scope=dict(b17);scope['O']=O;exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),scope)
for actor,shotids in [(n['ACTORS']['opening Arteta'],['OP01_year','OP02_arteta','OP03_phone']),(n['ACTORS']['unveiling Arteta'],['TR02_flag','TR02_reaction']),(b17['TRAINCAST']['Arteta'],['TR03_warning','TR03_praise'])]:
 lines=[]
 for row in rows:
  if row['id'] in shotids:
   for cue in plan['cues']:
    if cue['shot']==row['id'] and cue['stem']=='dialogue' and cue['asset']!='L08':lines.append((cue['asset'],row['local_start']+shots[row['id']]['events'][cue['event']]))
 scope['lips'](actor,lines,True)
# Retain original body accents at ordinary speed; one small emphasis nod in extended holds.
a=n['ACTORS']['opening Arteta'];s=a['s'];bpy.context.window.scene=s
for point,delta in ins[s.name]:
 if point==309:continue
 first=round(mapframe(point,ins[s.name]));s.frame_set(first);head=a['C']['head'].location.copy();neck=a['C']['neck'].location.copy()
 for off,ang in [(0,0),(max(1,delta//2-4),0),(delta//2,.038),(delta//2+4,0),(delta,0)]:
  a['C']['head'].location=neck+n['rotate'](head-neck,ang);a['C']['head'].keyframe_insert(data_path='location',frame=first+off)
# Driver has native mouth drawings; select them on the actual take, not a stretched old phrase.
s=bpy.data.scenes['S002_B01_v016_opening'];bpy.context.window.scene=s;row=next(r for r in rows if r['id']=='OP02_driver');start=row['local_start']+6
raw=subprocess.check_output(['/opt/homebrew/bin/ffmpeg','-v','error','-i',str(O/'voices/B04-mix.wav'),'-f','f32le','-ac','1','-ar','48000','-']);a=np.frombuffer(raw,np.float32);env=[float(np.sqrt(np.mean(a[i:i+2000]**2))) for i in range(0,len(a),2000)];limit=max(env)*.10
ww=[w for sg in words['B04']['segments'] for w in sg.get('words',[])];groups={label:bpy.data.objects['B01 / delivery driver / CTRL mouth '+label] for label in ['rest','MBP','A','E','O','U','FV','L']}
for group in groups.values():
 for ob in group.children_recursive:
  if ob.type in ['MESH','CURVE']:ob.animation_data_clear()
for f in range(1,s.frame_end+1):
 j=f-start;word=next((w['word'].strip().lower() for w in ww if w['start']<=max(0,j/24)<w['end']),'');label='rest'
 if 0<=j<len(env) and env[j]>limit:
  label='O' if any(t in word for t in ['boss','renew','before']) else 'E'
  if word.startswith(('m','b','p')) and any(abs(j/24-w['start'])<.045 for w in ww):label='MBP'
 for k,group in groups.items():
  for ob in group.children_recursive:
   if ob.type in ['MESH','CURVE']:
    ob.hide_render=ob.hide_viewport=k!=label;ob.keyframe_insert(data_path='hide_render',frame=f);ob.keyframe_insert(data_path='hide_viewport',frame=f)
# Replace each scene's preview audio so live playback matches this revision.
for name in {r['scene'] for r in rows}:
 s=bpy.data.scenes[name];rr=[r for r in rows if r['scene']==name];first=rr[0]['start_frame']-1;count=sum(r['frames'] for r in rr);path=O/(name.rsplit('_',1)[-1]+'-preview.wav')
 subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-y','-i',str(O/'mix/mix-premaster.wav'),'-af',f'atrim=start_sample={first*2000}:end_sample={(first+count)*2000},asetpts=PTS-STARTPTS','-c:a','pcm_s16le',str(path)],check=True)
 ed=s.sequence_editor_create()
 for strip in list(ed.strips):
  if strip.type=='SOUND':ed.strips.remove(strip)
 ed.strips.new_sound('v018 dialogue and effects',str(path),1,1);s.sync_mode='AUDIO_SYNC';s.render.use_sequencer=False
s=bpy.data.scenes['S002_B01_v016_opening'];bpy.context.window.scene=s;s.frame_set(next(r for r in rows if r['id']=='OP02_arteta')['local_start']+10);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=s.frame_current),key=lambda m:m.frame).camera
bpy.data.libraries.write(str(O/'batches01-02-v018.blend'),{bpy.data.scenes[r['scene']] for r in rows},fake_user=True,compress=True)
(O/'native-checks.json').write_text(json.dumps(report,indent=2));result={'native':str(O/'batches01-02-v018.blend'),'scenes':report}
