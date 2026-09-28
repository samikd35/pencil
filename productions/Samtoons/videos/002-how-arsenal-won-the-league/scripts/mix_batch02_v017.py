from pathlib import Path
import json,subprocess,hashlib,sys
import numpy as np,soundfile as sf
from fractions import Fraction
V=Path(__file__).resolve().parents[1];O=V/'artifacts/batch02-v017';FF='/opt/homebrew/bin/ffmpeg';plan=json.loads((V/'artifacts/opening-v002/full-audio-plan.json').read_text());plan['timeline']['frames']=1321;shots=[s for s in plan['shots'] if s['start_frame']<=1321];lookup={s['id']:s for s in shots};plan['shots']=shots;plan['status']='revised candidate; listening approval pending'
for ident in ['L07b','L09','L10','L11']:
 p=O/'voices'/f'{ident}.wav';dest=O/'voices'/f'{ident}-mix.wav';subprocess.run([FF,'-v','error','-y','-i',str(p),'-af','highpass=f=65','-ar','48000','-ac','1','-c:a','pcm_s24le',str(dest)],check=True);a,sr=sf.read(dest);gain=min(10**(-21/20)/max(np.sqrt(np.mean(a*a)),1e-9),.78/max(abs(a)));sf.write(dest,a*gain,sr,subtype='PCM_24');plan['assets'][ident]={'path':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source':'Locally directed Qwen performance, see adjacent take JSON','license':'Qwen Apache-2.0; generated performance','attribution':''}
lookup['TR02_flag']['events']['TR02_flag_setup']=3
plan['cues'].append({'id':'TR02_flag_setup','shot':'TR02_flag','event':'TR02_flag_setup','asset':'L07b','stem':'dialogue','intent':'State premise before revealing corner flag as the real striker','duration_seconds':str(sf.info(O/'voices/L07b-mix.wav').duration),'gain_db':0,'fade_in_seconds':.005,'fade_out_seconds':.03})
# Applause belongs to the shirt reveal, after the spoken premise.
lookup['TR02_flag']['events']['TR02_flag_applause_additional']=70
strike=next(c for c in plan['cues'] if c['shot']=='TR03_kick' and 'ball-strike' in c['id']);lookup['TR03_kick']['events'][strike['event']]=16;lookup['TR03_kick']['events']['TR03_deflection']=27;deflect=dict(strike);deflect.update(id='TR03_deflection',event='TR03_deflection',gain_db=-10,intent='Ball hits practice defender on visible shin contact');plan['cues'].append(deflect)
cues=[]
for c in plan['cues']:
 if c['shot'] not in lookup:continue
 if c['id']=='TR02_flag_applause_additional':c['duration_seconds']=str(26/24)
 if c['asset'] in ['L09','L10','L11']:c['duration_seconds']=str(sf.info(O/'voices'/(c['asset']+'-mix.wav')).duration)
 at=lookup[c['shot']]['start_frame']-1+lookup[c['shot']]['events'][c['event']];remain=(1321-at)/24
 if remain<=0:continue
 if 'duration_seconds' in c:c['duration_seconds']=str(min(float(Fraction(str(c['duration_seconds']))),remain))
 cues.append(c)
plan['cues']=cues;used={c['asset'] for c in cues};plan['assets']={k:v for k,v in plan['assets'].items() if k in used};(O/'audio-plan.json').write_text(json.dumps(plan,indent=2));subprocess.run([sys.executable,str(V.parents[3]/'pipeline/audio.py'),'build',str(O/'audio-plan.json'),'--out',str(O/'mix-corrected')],check=True)
