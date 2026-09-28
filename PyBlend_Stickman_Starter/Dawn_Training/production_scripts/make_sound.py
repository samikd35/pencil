"""Original, quiet synthesized atmosphere and action effects. No external recordings."""
from pathlib import Path
import json,wave
import numpy as np
OUT=Path(__file__).resolve().parents[2]/'artifacts/dawn_training'
RATE=48000;N=30*RATE;rng=np.random.default_rng(734)
t=np.arange(N)/RATE
noise=rng.normal(0,1,N)
wind=np.convolve(noise,np.ones(160)/160,mode='same')*.08
wind*=.55+.35*np.sin(t*.45)**2
bed=np.zeros(N)
for f in [146.8324,174.6141,220.,293.6648]:
 bed+=.007*np.sin(2*np.pi*f*t+.2*np.sin(t*.22))*(.65+.35*np.sin(t*.18+f)**2)
master=np.stack([wind+bed,np.roll(wind,630)+bed],axis=1)
events=[]
def add(start,duration,kind,gain=1,pan=0):
 n=int(duration*RATE);tt=np.arange(n)/RATE
 if kind=='step':
  env=np.exp(-tt*35);s=(rng.normal(0,.13,n)+np.sin(2*np.pi*80*tt)*.17)*env
 elif kind=='charge':
  env=np.sin(np.pi*np.clip(tt/duration,0,1))**.5
  phase=2*np.pi*(130*tt+250/duration*tt**2)
  s=(np.sin(phase)*.04+np.sin(phase*1.505)*.012+np.convolve(rng.normal(0,.1,n),np.ones(8)/8,mode='same'))*env
 elif kind=='blast':
  env=(1-np.exp(-tt*80))*np.exp(-tt*2.6)
  s=(np.convolve(rng.normal(0,.45,n),np.ones(12)/12,mode='same')+np.sin(2*np.pi*(90*tt+30*np.sqrt(tt)))*.11)*env
 elif kind=='impact':
  env=np.exp(-tt*7);s=(np.convolve(rng.normal(0,.75,n),np.ones(6)/6,mode='same')+np.sin(2*np.pi*54*tt)*.22)*env
 else:
  env=np.sin(np.pi*tt/duration)**2;s=np.convolve(rng.normal(0,.25,n),np.ones(18)/18,mode='same')*env
 s*=gain
 i=int(start*RATE);n=min(n,N-i)
 master[i:i+n,0]+=s[:n]*np.sqrt((1-pan)/2);master[i:i+n,1]+=s[:n]*np.sqrt((1+pan)/2)
 events.append(dict(start=start,duration=duration,kind=kind,gain=gain,pan=pan))
add(6.7,3.1,'charge',.6)
for tt in np.arange(10.02,15,.333333):add(float(tt),.14,'step',.7,pan=float((tt-12.5)/3.))
add(14.8,.8,'whoosh',1)
add(15.65,4.3,'charge',1)
add(20.5,1.1,'charge',1.2,-.5)
add(21.5,2.2,'blast',1.15,-.1)
add(21.9,1.2,'impact',1,.7)
add(25.05,.5,'whoosh',.8)
add(25.42,1.2,'impact',.9,.1)
master*=np.clip(t/.5,0,1)[:,None]*np.clip((30-t)/.8,0,1)[:,None]
master=np.tanh(master*1.8)*.78
with wave.open(str(OUT/'Dawn_Training_Sound.wav'),'wb') as w:
 w.setnchannels(2);w.setsampwidth(2);w.setframerate(RATE);w.writeframes((master*32767).astype('<i2').tobytes())
(OUT/'sound_cues.json').write_text(json.dumps({'sample_rate':RATE,'duration':30,'source':'Original procedural synthesis; no sampled recordings','events':events},indent=2))
print('Audio written, peak',round(float(np.abs(master).max()),4))
