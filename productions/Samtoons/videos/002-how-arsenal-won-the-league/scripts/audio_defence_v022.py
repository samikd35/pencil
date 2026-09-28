"""New scored comic beats and City setup; retained dialogue stays byte-identical."""
from pathlib import Path
import json,subprocess,hashlib,sys,math
from fractions import Fraction
import numpy as np,soundfile as sf
from scipy.signal import butter,sosfilt
V=Path(__file__).resolve().parents[1];O=V/'artifacts/defence-v022';S=O/'sounds';S.mkdir(exist_ok=True);SR=48000;rng=np.random.default_rng(220919)
plan=json.loads((V/'artifacts/defence-v019/audio-plan.json').read_text());edit=json.loads((O/'edit.json').read_text());plan['timeline']['frames']=sum(r['frames'] for r in edit);plan['scope']='Second batch: coach reactions, City pursuit setup and intentional sound accents';plan['status']='v022 review candidate; listening not claimed';shots={s['id']:s for s in plan['shots']}
for r in edit:shots[r['id']]['start_frame']=r['start_frame']
plan['cues']=[c for c in plan['cues'] if c['asset']!='L18'];plan['assets'].pop('L18',None)
def register(name,p,source='Original production sound design in audio_defence_v022.py'):
 plan['assets'][name]=dict(path=str(p.resolve()),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),source=source,license='Original production composition/synthesis' if name not in ['L18b','L18c'] else 'Generated synthetic character voice',attribution='')
def write(name,x):
 assert np.isfinite(x).all();x=x/max(1,np.max(abs(x))/.72);p=S/(name+'.wav');sf.write(p,x,SR,subtype='PCM_24');register(name,p)
def env(t,d,attack=.03,release=.2):return np.minimum(t/attack,1)*np.minimum((d-t)/release,1)
def band(x,lo,hi):return sosfilt(butter(2,[lo,hi],btype='bandpass',fs=SR,output='sos'),x)
# Short orchestral-style rise: harmonic brass chord with breath, not a constant music bed.
d=1.5;t=np.arange(round(d*SR))/SR;x=np.zeros(len(t))
for freq in [146.83,220,293.66,369.99,440]:
 voice=sum(np.sin(2*np.pi*freq*h*t+.003*h*np.sin(2*np.pi*4.4*t))/h**1.25 for h in range(1,9));x+=voice*.052
x=band(x,120,3800)*env(t,d,.28,.32);write('fortress-swell',x)
# Small synthetic choral "ah" chord: several detuned voices and vocal formant weighting.
d=1.85;t=np.arange(round(d*SR))/SR;x=np.zeros(len(t))
for freq in [220,277.18,329.63,440]:
 for detune in [-.0025,.0025]:
  for h in range(1,13):
   f=freq*(1+detune)*h;w=(math.exp(-((f-800)/240)**2)+.45*math.exp(-((f-1200)/330)**2)+.12)/h
   x+=w*.07*np.sin(2*np.pi*f*t+.15*np.sin(2*np.pi*5.1*t))
x*=env(t,d,.13,.55);write('approval-choir',x)
# Air accents track the direction of each edge entrance.
d=.30;t=np.arange(round(d*SR))/SR;x=band(rng.normal(0,1,len(t)),450,4200)*np.sin(np.pi*t/d)**2*.13;write('peek-whoosh',x)
# Graphite texture in five brief writing bursts, matching the moving wrist rather than a continuous hiss.
d=1.8;t=np.arange(round(d*SR))/SR;x=band(rng.normal(0,1,len(t)),900,6500);mask=np.zeros(len(t))
for st in [.02,.25,.52,.78,1.07,1.34]:
 u=np.clip((t-st)/.16,0,1);mask+=np.sin(np.pi*u)**2
write('pencil-scribble',x*mask*.12*env(t,d,.008,.08))
d=.65;t=np.arange(round(d*SR))/SR;write('notebook-sparkle',(.18*np.sin(2*np.pi*1174.66*t)+.08*np.sin(2*np.pi*2349.32*t))*np.exp(-t*7)*env(t,d,.002,.16))
d=8.7;t=np.arange(round(d*SR))/SR;x=np.zeros(len(t))
for st in np.arange(.0,d,.72):
 dt=np.maximum(t-st,0);mask=(t>=st)*np.exp(-dt*9)*np.minimum(dt/.016,1)
 x+=.18*(np.sin(2*np.pi*73.416*t)+.23*np.sin(2*np.pi*103.826*t))*mask
write('city-tension',x*env(t,d,.25,.45))

def cue(name,shot,frame,stem,gain,dur=None,pan=0,intent=None):
 p=Path(plan['assets'][name]['path']);length=sf.info(p).duration if dur is None else dur;cid='v022-'+name+'-'+str(len(plan['cues']));shots[shot]['events'][cid]=frame-1
 plan['cues'].append(dict(id=cid,shot=shot,event=cid,asset=name,stem=stem,intent=intent or name,duration_seconds=str(Fraction(round(length*SR),SR)),gain_db=gain,pan=pan,fade_in_seconds=.006,fade_out_seconds=.05))
for k,f in [('L18b',18),('L18c',156)]:register(k,O/'voices'/(k+'-mix.wav'),'Reference-conditioned local Qwen Base using the established synthetic voice; reference and transcript in voices/'+k+'.json');cue(k,'CD05_ping',f,'dialogue',0,intent='Arteta loses confidence' if k=='L18b' else 'Narrator motivates next Pep pursuit')
cue('fortress-swell','CD03',97,'score',-11,intent='Wall locks into an absurdly heroic fortress')
cue('approval-choir','CD04',186,'score',-5,intent='Reverent admiration becomes the joke')
for f,p in [(174,-.75),(199,.75),(225,0)]:cue('peek-whoosh','CD04',f,'foley',-10,pan=p,intent='Coach enters from the corresponding frame edge')
cue('pencil-scribble','CD04',219,'foley',-6,pan=.65,intent='Simeone urgently copies the tactic')
cue('paper','CD04',240,'foley',-19,dur=.35,intent='Conte raises his notebook')
cue('notebook-sparkle','CD04',248,'plot-effects',-11,intent='Arteta Masterclass notebook punchline')
cue('city-tension','CD05_ping',26,'score',-14,intent='After the isolated notification, introduce the approaching threat')
for i,f in enumerate([171,183,195,207,219,231]):cue('boot','CD05_ping',f,'foley',-22+i*1.8,pan=.6-i*.08,intent='Offscreen Pep footsteps approach under the setup line')
plan['mix_gain_db']=-2
(O/'audio-plan.json').write_text(json.dumps(plan,indent=2));subprocess.run([sys.executable,str(V.parents[3]/'pipeline/audio.py'),'build',str(O/'audio-plan.json'),'--out',str(O/'mix')],check=True)
old=json.loads((V/'artifacts/defence-v019/captions.json').read_text());captions=[]
for c in old:
 if c['id']=='L18':continue
 if c['start']>=711/24:c['start']+=4;c['end']+=4
 captions.append(c)
for k,f,sp in [('L18b',18,'ARTETA'),('L18c',156,'NARRATOR')]:
 p=O/'voices'/(k+'-mix.wav');m=json.loads((O/'voices'/(k+'.json')).read_text());t=(shots['CD05_ping']['start_frame']+f-2)/24;captions.append(dict(id=k,speaker=sp,text=m['text'],start=t,end=t+sf.info(p).duration,shot='CD05_ping'))
(O/'captions.json').write_text(json.dumps(captions,indent=2));print('v022 AUDIO READY',flush=True)
