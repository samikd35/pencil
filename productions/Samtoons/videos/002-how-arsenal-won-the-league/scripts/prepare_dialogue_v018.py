from pathlib import Path
import json,math,hashlib,subprocess,sys
from fractions import Fraction
import numpy as np,soundfile as sf
V=Path(__file__).resolve().parents[1];O=V/'artifacts/dialogue-v018';FF='/opt/homebrew/bin/ffmpeg'
plan=json.loads((V/'artifacts/batch02-v017/audio-plan.json').read_text());edit=json.loads((V/'artifacts/batch02-v017/edit.json').read_text());dialogue=json.loads((O/'dialogue.json').read_text());new={r['id']:r for r in dialogue};shots={s['id']:s for s in plan['shots']}
for key,r in new.items():
 p=O/'voices'/f'{key}.wav';dest=p.with_name(key+'-mix.wav')
 cut={'B05':5.10,'L09':2.52}.get(key)
 cmd=[FF,'-v','error','-y','-i',str(p)]
 if cut:cmd+=['-t',str(cut)]
 subprocess.run(cmd+['-af','highpass=f=65','-ar','48000','-ac','1','-c:a','pcm_s24le',str(dest)],check=True)
 a,sr=sf.read(dest);gain=min(10**(-21/20)/max(np.sqrt(np.mean(a*a)),1e-9),.78/max(abs(a)));sf.write(dest,a*gain,sr,subtype='PCM_24');r['duration']=len(a)/sr
 plan['assets'][key]={'path':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source':'Reference-conditioned original synthetic voice; see adjacent take JSON','license':'Qwen Apache-2.0; generated performance','attribution':''}
 for c in plan['cues']:
  if c['asset']==key:c['duration_seconds']=str(Fraction(len(a),sr))
# Extend only the speaking beat. Physical action durations stay unchanged.
holds={'OP01_year':108,'OP02_arteta':242,'OP02_driver':309,'OP03_phone':376,'TR02_flag':218,'TR02_reaction':409,'TR03_warning':78,'TR03_praise':232}
cursor=1;locals={};insertions={}
for r in edit:
 old_start=r['local_start'];old_frames=r['frames'];length=old_frames
 for c in plan['cues']:
  if c['shot']==r['id'] and c['stem']=='dialogue':length=max(length,shots[r['id']]['events'][c['event']]+math.ceil(float(Fraction(c['duration_seconds']))*24)+12)
 if r['id']=='TR02_flag':length=max(length,old_frames+math.ceil(new['L07b']['duration']*24)-32)
 extra=length-old_frames;r.update(old_local_start=old_start,old_frames=old_frames,frames=length,start_frame=cursor,local_start=locals.get(r['scene'],1),hold_source_frame=holds.get(r['id']))
 if extra:insertions.setdefault(r['scene'],[]).append([holds[r['id']],extra])
 shots[r['id']]['start_frame']=cursor
 if r['id']=='OP03_phone':shots[r['id']]['events']['OP03_phone_switch']=length-4
 if r['id']=='TR02_flag':shots[r['id']]['events']['TR02_flag_applause_additional']=70+extra
 cursor+=length;locals[r['scene']]=r['local_start']+length
plan['timeline']['frames']=cursor-1;plan['status']='v018 spoken clarity and reference-conditioned voice candidate'
(O/'edit.json').write_text(json.dumps(edit,indent=2));(O/'insertions.json').write_text(json.dumps(insertions,indent=2));(O/'audio-plan.json').write_text(json.dumps(plan,indent=2));(O/'dialogue.json').write_text(json.dumps(dialogue,indent=2))
# Caption events derive from the same selected cue times and transcripts as audio.
labels={'B01':'NARRATOR','L07':'NARRATOR','L08':'GYÖKERES'};captions=[]
for c in plan['cues']:
 if c['stem']!='dialogue':continue
 k=c['asset'];p=Path(plan['assets'][k]['path']);meta=new.get(k) or json.loads(p.with_name(k+'.json').read_text());start=(shots[c['shot']]['start_frame']-1+shots[c['shot']]['events'][c['event']])/24
 captions.append(dict(id=k,speaker=meta.get('speaker',labels.get(k,'ARTETA')),text=meta['text'].replace('Gyokeres','Gyökeres'),start=start,end=start+float(Fraction(c['duration_seconds'])),shot=c['shot']))
(O/'captions.json').write_text(json.dumps(sorted(captions,key=lambda r:r['start']),indent=2))
assert all(b['start_frame']==a['start_frame']+a['frames'] for a,b in zip(edit,edit[1:]))
assert next(r for r in edit if r['id']=='TR03_kick')['frames']==72
print('frames',cursor-1,'seconds',(cursor-1)/24,'insertions',insertions)
subprocess.run([sys.executable,str(V.parents[3]/'pipeline/audio.py'),'build',str(O/'audio-plan.json'),'--out',str(O/'mix')],check=True)
