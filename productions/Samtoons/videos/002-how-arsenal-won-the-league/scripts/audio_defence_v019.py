from pathlib import Path
import json,subprocess,sys,hashlib,dataclasses
from fractions import Fraction
import numpy as np,soundfile as sf
V=Path(__file__).resolve().parents[1];O=V/'artifacts/defence-v019';FF='/opt/homebrew/bin/ffmpeg'
ids=['CD01_cross','CD01_header','CD02','CD03','CD04','CD05','N02','CD05_proud','CD05_ping'];lens=[197,72,122,120,200,144,48,84,60];plan=json.loads((V/'artifacts/dialogue-v018/full-audio-plan-working.json').read_text());plan['shots']=[s for s in plan['shots'] if s['id'] in ids];plan['cues']=[c for c in plan['cues'] if c['shot'] in ids];plan['timeline']['frames']=sum(lens);plan['status']='v019 next chronological batch review';shots={s['id']:s for s in plan['shots']};edit=[];cursor=1
for ident,length in zip(ids,lens):
 shots[ident]['start_frame']=cursor;edit.append(dict(id=ident,frames=length,start_frame=cursor,local_start=1 if ident=='N02' else cursor,scene='S002_narrator_v019' if ident=='N02' else 'S002_defence_v019'));cursor+=length
changes={'CD01_cross_ball-strike_69':167,'CD01_header_ball-strike_71':19,'CD01_header_goal-cheer_72':40}
for s in shots.values():
 for event,val in changes.items():
  if event in s['events']:s['events'][event]=val
captions=[]
for c in plan['cues']:
 if c['stem']!='dialogue':continue
 k=c['asset'];p=O/'voices'/f'{k}.wav'
 if not p.exists():p=Path(plan['assets'][k]['path'])
 dest=O/'voices'/f'{k}-mix.wav';subprocess.run([FF,'-v','error','-y','-i',str(p),'-af','highpass=f=65','-ar','48000','-ac','1','-c:a','pcm_s24le',str(dest)],check=True)
 a,sr=sf.read(dest);g=min(10**(-21/20)/max(np.sqrt(np.mean(a*a)),1e-9),.78/max(abs(a)));sf.write(dest,a*g,sr,subtype='PCM_24');c['duration_seconds']=str(Fraction(len(a),sr));plan['assets'][k]={'path':str(dest),'source':'Selected synthetic narrator or original reference-conditioned character voice','license':'Generated voice','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'attribution':''}
 meta=json.loads(p.with_name(k+'.json').read_text());sp=meta.get('speaker','NARRATOR' if k in ['L12','L14'] else 'ARTETA');start=(shots[c['shot']]['start_frame']-1+shots[c['shot']]['events'][c['event']])/24;captions.append(dict(id=k,speaker=sp,text=meta['text'],start=start,end=start+len(a)/sr,shot=c['shot']))
# Audible contact follows the exact authored foot/header/net events.
for j,frame in enumerate([405,421,438,456,477,489]):
 ident='shuffle-'+str(j);shots['CD03']['events'][ident]=frame-392;plan['cues'].append(dict(id=ident,shot='CD03',event=ident,asset='boot',stem='foley',intent='Short boot shuffle aligned to defensive wall / goalkeeper step',duration_seconds=str(Fraction(sf.info(plan['assets']['boot']['path']).frames,sf.info(plan['assets']['boot']['path']).samplerate)),gain_db=-17,fade_in_seconds=.005,fade_out_seconds=.035))
plan['assets']={k:v for k,v in plan['assets'].items() if k in {c['asset'] for c in plan['cues']}};assert cursor==1048
(O/'edit.json').write_text(json.dumps(edit,indent=2));(O/'audio-plan.json').write_text(json.dumps(plan,indent=2));(O/'captions.json').write_text(json.dumps(captions,indent=2))
subprocess.run([sys.executable,str(V.parents[3]/'pipeline/audio.py'),'build',str(O/'audio-plan.json'),'--out',str(O/'mix')],check=True)
from mlx_audio.stt import load
m=load('mlx-community/whisper-tiny-asr-fp16');words={}
for c in captions:
 k=c['id'];r=m.generate(str(O/'voices'/f'{k}-mix.wav'),language='en',word_timestamps=True,temperature=0);words[k]=dataclasses.asdict(r);print(k,words[k].get('text'),flush=True)
(O/'word-analysis.json').write_text(json.dumps(words,indent=2));print('AUDIO READY',flush=True)
