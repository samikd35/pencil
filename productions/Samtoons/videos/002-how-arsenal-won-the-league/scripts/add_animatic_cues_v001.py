from pathlib import Path
import urllib.request,json,hashlib,subprocess
import numpy as np,soundfile as sf
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animatic-v001';P=O/'audio-plan.json';d=json.loads(P.read_text());E={r['id']:r for r in json.loads((O/'edit.json').read_text())};shots={r['id']:r for r in d['shots']};SR=48000
url='https://cdn.freesound.org/previews/462/462362_9159316-hq.mp3';src=O/'sounds/applause-source.mp3'
if not src.exists():src.write_bytes(urllib.request.urlopen(url,timeout=30).read())
subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-y','-i',str(src),'-t','5','-ar','48000','-af','highpass=f=100,loudnorm=I=-23:TP=-4:LRA=10','-c:a','pcm_s24le',str(O/'sounds/applause.wav')],check=True)
def reg(k,source,license,credit=''):
 p=O/'sounds'/(k+'.wav');d['assets'][k]=dict(path='../../'+str(p.relative_to(V)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),source=source,license=license,attribution=credit)
reg('applause','https://freesound.org/people/Breviceps/sounds/462362/ ; HQ public preview, first5seconds, filtered and levelled','CC0 1.0; saved source page','Small applause by Breviceps, Freesound462362 (voluntary credit)')
for name,seconds in [('trolley',.45),('telephone',.85),('medal',.55),('confirmation',.3)]:
 t=np.arange(round(seconds*SR))/SR
 if name=='trolley':a=.09*np.sin(2*np.pi*(900*t-450*t*t))*(.7+.3*np.sin(2*np.pi*31*t))*np.sin(np.pi*t/seconds)**2
 elif name=='telephone':a=.08*(np.sin(2*np.pi*440*t)+np.sin(2*np.pi*480*t))*np.minimum(1,t/.008)*np.minimum(1,(seconds-t)/.02)
 elif name=='medal':a=.10*(np.sin(2*np.pi*2100*t)+.3*np.sin(2*np.pi*3381*t))*np.exp(-t*11)*np.minimum(1,t/.001)
 else:a=.13*np.sin(2*np.pi*1250*t)*np.exp(-t*15)*np.minimum(1,t/.001)
 sf.write(O/'sounds'/(name+'.wav'),a,SR,subtype='PCM_24');reg(name,'Original graphic accent synthesis in add_animatic_cues_v001.py','Original production synthesis')
def cue(sh,key,at,dur,gain=-4,stem='foley'):
 cid=sh+'_'+key+'_additional';assert cid not in [x['id'] for x in d['cues']]
 shots[sh]['events'][cid]=round(at*24);d['cues'].append(dict(id=cid,shot=sh,event=cid,asset=key,stem=stem,intent={'applause':'Applause chooses the flag, cuts dead at Gyokeres reaction','trolley':'Recognisable courier callback','telephone':'Privileged gold line answered promptly','medal':'Unused runners-up medal callback','confirmation':'Official play-on response'}[key],duration_seconds=dur,gain_db=gain,fade_in_seconds=.005,fade_out_seconds=.015))
cue('TR02_flag','applause',0,3.95,-2,'crowd')
for sh,at in [('OP01_enter',.1),('OP01_enter',1.1),('CP04_courier',.1),('FR05',E['FR05']['frames']/24-.48)]:
 # Duplicate repeated cue handled with explicit ordinal; fixed variations, no random reselect.
 if sh=='OP01_enter' and at>1:continue
 cue(sh,'trolley',at,.45,-4)
cue('VH03','telephone',.1,.85,-7);cue('FR05','medal',E['FR05']['frames']/24-1.1,.55,-3)
# Remove City result ping wrongly repurposed for a different dramatic job.
d['cues']=[x for x in d['cues'] if not (x['shot']=='VH04_button' and x['asset']=='city-ping')]
cue('VH04_button','confirmation',.25,.3,-4)
P.write_text(json.dumps(d,indent=2));prod=json.loads((V/'production.json').read_text());prod.update(shots=d['shots'],cues=d['cues'],assets={k:{**a,'path':str((O/a['path']).resolve().relative_to(V))} for k,a in d['assets'].items()});(V/'production.json').write_text(json.dumps(prod,indent=2))
p=V/'scripts/mix_animatic_sections_v001.py';s=p.read_text();s=s.replace("('-scorev2' if i//7 in [2,3,4] else '')","('-cuesv3' if i//7 in [0,1,3,4,5,6] else '-scorev2' if i//7==2 else '')");p.write_text(s)
print('Added flag applause, courier squeak, gold-line ring, medal callback, distinct confirmation.')
