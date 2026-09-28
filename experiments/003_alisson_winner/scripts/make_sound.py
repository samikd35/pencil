"""Compose an original instrumental score and synthesize football Foley; no recordings."""
from pathlib import Path
import ast
import json
import math
import subprocess
import wave
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v001/audio';OUT.mkdir(exist_ok=True)
SR=48000;DURATION=40;COUNT=SR*DURATION
rng=np.random.default_rng(20210516)
stems={n:np.zeros((COUNT,2),dtype=np.float64) for n in ('music','foley','atmosphere')}
# Reuse the proven Foley synthesizer without running its old experiment's top-level build.
source=ROOT.parent/'001_heavy_box/scripts/sound_finish_v001.py'
nodes=[n for n in ast.parse(source.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in ('noise','voice','synth')]
assert len(nodes)==3
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),globals())
cues=[]
def add(stem,at,sound,pan=0,gain=1):
    start=round(at*SR)
    if sound.ndim==1:
        a=(pan+1)*np.pi/4;sound=np.column_stack((sound*np.cos(a),sound*np.sin(a)))
    end=min(COUNT,start+len(sound));assert start>=0 and end>start
    stems[stem][start:end]+=sound[:end-start]*gain

def note(midi,duration,style='pluck'):
    t=np.arange(round(duration*SR))/SR;f=440*2**((midi-69)/12)
    if style=='pad':
        x=sum(np.sin(2*np.pi*f*(h+detune)*t)/(h*h) for h,detune in [(1,0),(2,.002),(3,-.002)])
        env=np.minimum(1,t/.35)*np.minimum(1,(duration-t)/.70)
    elif style=='bell':
        x=np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*f*2.01*t)+.1*np.sin(2*np.pi*f*3.98*t)
        env=np.minimum(1,t/.006)*np.exp(-t*3)
    else:
        x=sum(np.sin(2*np.pi*f*h*t)/h for h in range(1,7))
        env=np.minimum(1,t/.008)*np.exp(-t*9)
    return x*env

# D minor pulse. The melody and arrangement are authored for this 40-second film.
for begin,chord in [(0,[38,45,53]),(4,[38,45,53]),(8,[34,41,50]),(12,[36,43,52]),(16,[33,40,49]),(19,[33,40,52])]:
    for j,midi in enumerate(chord):add('music',begin,note(midi,4.4 if begin<19 else 3.35,'pad'),(j-1)*.55,.055)
pattern=[62,69,65,69,62,69,65,72]
for i,at in enumerate(np.arange(3.8,21.4,.30)):
    gain=.028+.025*min(1,(at-3.8)/14)
    add('music',float(at),note(pattern[i%8],.65),-.4 if i%2 else .4,gain)
# Resolve into a warmer major harmony when the goal reaches the net.
for begin,chord in [(24,[38,45,54,62]),(28,[35,42,54,59]),(32,[31,43,55,62]),(36,[38,45,54,62])]:
    for j,midi in enumerate(chord):add('music',begin,note(midi,4 if begin==36 else 4.5,'pad'),(j-1.5)*.38,.085)
melody=[(24,74),(24.6,73),(25.2,69),(26.1,66),(27,69),(28.2,71),(29.1,69),(30,66),(31,64),(32.1,67),(33,69),(34.2,74),(35.3,73),(36.1,74)]
for at,midi in melody:add('music',at,note(midi,1.3,'bell'),.05,.12)
for at in np.arange(24,36,.6):
    t=np.arange(round(.30*SR))/SR
    x=np.sin(2*np.pi*(68*t-45*t*t))*np.exp(-t*16)
    add('music',float(at),x,0,.075)

# Wind texture and a pause immediately before contact focus attention on the header.
for start in (0,8,16,24,32):
    n=8*SR;t=np.arange(n)/SR
    x=noise(n,380,330)*(.45+.15*np.sin(t*1.3))*np.minimum(1,t/.5)*np.minimum(1,(8-t)/.5)
    add('atmosphere',start,x,-.30,.026)

def cue(kind,at,dur,gain,pan=0):
    data={'kind':kind,'duration':dur,'gain':gain,'pan':pan}
    _,x=synth(data);add('foley',at,x);cues.append(dict(data,seconds=at,frame=round(at*24)+1))
for at in (1,2,3):cue('tap',at,.065,.10,0)
period=2.56*1.04/3.20
for i,at in enumerate(np.arange(4,10,period/2)):cue('step',float(at),.10,.16,(-1 if i%2 else 1)*.12)
for i,at in enumerate((10.10,10.42,10.79,11.25,11.76)):cue('step',at,.10,.115,-.25+i*.08)
cue('whoosh',4,.55,.11,-.25)
cue('step',16.40,.13,.18,-.15)
cue('whoosh',16.73,.38,.22,-.10)
cue('tap',17,.18,.46,.2)
cue('whoosh',17.12,1.2,.10,.4)
cue('step',21.83,.16,.14,-.2)
cue('whoosh',22.08,.34,.14,-.1)
cue('tap',22.5,.17,.46,0)
cue('whoosh',22.57,1.23,.14,.5)
cue('step',23.15,.16,.23,-.1)
cue('scrape',24,.32,.23,.60)
cue('tap',24.84,.12,.16,.50)
for at,pan in [(29.1,-.8),(29.4,.8),(29.65,-.6),(29.95,.6),(30.2,-.4),(30.5,.4),(30.83,-.2),(31.2,.2)]:cue('step',at,.11,.11,pan)
cue('whoosh',36,.7,.08,0)
# Explicitly duck suspense before the decisive touch, keeping the moment's Foley clear.
timebase=np.arange(COUNT)/SR
duck=np.ones(COUNT)
mask=(timebase>21.9)&(timebase<22.5);duck[mask]=np.interp(timebase[mask],[21.9,22.28,22.5],[1,.08,.08])
mask=(timebase>=22.5)&(timebase<23.3);duck[mask]=np.interp(timebase[mask],[22.5,23.3],[.08,.7])
stems['music']*=duck[:,None]
fade=np.minimum(1,timebase/.10)*np.minimum(1,(DURATION-timebase)/1.20)
for name in stems:stems[name]*=fade[:,None]
mix=sum(stems.values());factor=min(1,.88/np.max(np.abs(mix)))
def write(path,x):
    assert x.shape==(COUNT,2) and np.isfinite(x).all() and np.max(np.abs(x))<1
    with wave.open(str(path),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.round(x*32767).astype('<i2').tobytes())
for name,x in stems.items():write(OUT/(name+'.wav'),x*factor)
write(OUT/'mix-original.wav',mix*factor)
report={'sample_rate':SR,'duration':DURATION,'samples':COUNT,'seed':20210516,'origin':'Original synthesized instrumental composition, filtered wind and Foley. No speech, voice clone, source recording or broadcast audio. Foley functions reused from Heavy Box.','cue_count':len(cues),'cues':cues,'raw_peak':float(np.max(np.abs(mix*factor))),'shared_stem_gain':factor}
(OUT/'sound-design.json').write_text(json.dumps(report,indent=2)+'\n')
print('SOUND_READY',len(cues),'cues',flush=True)
