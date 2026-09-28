"""Deterministic original cartoon Foley and nonverbal vocal-like synthesis; no recordings."""
import json
from pathlib import Path
import wave
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/finish-v001/audio'
CFG=json.loads((ROOT/'finish-v001.json').read_text())
SR=CFG['sample_rate']
COUNT=round(CFG['frames']/CFG['fps']*SR)
STEMS={name:np.zeros((COUNT,2),dtype=np.float64) for name in ('footsteps','foley','character','electric')}
rng=np.random.default_rng(CFG['seed'])

def noise(n,center,width):
    bins=np.fft.rfftfreq(n,1/SR)
    values=np.fft.irfft(np.fft.rfft(rng.normal(0,1,n))*np.exp(-.5*((bins-center)/width)**2),n)
    return values/max(np.max(np.abs(values)),1e-9)

def voice(t,frequencies,formants):
    f=np.interp(t,[0,t[-1]*.25,t[-1]*.65,t[-1]],frequencies)
    f*=1+.009*np.sin(2*np.pi*5*t)
    phase=2*np.pi*np.cumsum(f)/SR
    signal=np.zeros_like(t)
    for harmonic in range(1,34):
        weight=.08/harmonic+sum(gain*np.exp(-.5*((harmonic*f-center)/width)**2) for center,width,gain in formants)
        signal+=weight*np.sin(harmonic*phase)/np.sqrt(harmonic)
    return signal/max(np.max(np.abs(signal)),1e-9)

def synth(cue):
    n=round(cue['duration']*SR)
    t=np.arange(n)/SR
    u=t/cue['duration']
    kind=cue['kind']
    envelope=np.sin(np.pi*u)**.8
    if kind in ('step','tap'):
        x=(.7*np.sin(2*np.pi*(150*t-170*t*t))+.3*noise(n,900,750))*np.exp(-t*35)
        stem='footsteps' if kind=='step' else 'foley'
    elif kind in ('breath','whoosh','scrape'):
        center={'breath':1600,'whoosh':850,'scrape':1250}[kind]
        x=noise(n,center,center*.65)*envelope
        if kind=='scrape':
            x*=.7+.3*np.sin(2*np.pi*37*t)
            x+=.12*np.sin(2*np.pi*175*t)*envelope
        stem='character' if kind=='breath' else 'foley'
    elif kind=='creak':
        phase=2*np.pi*np.cumsum(230+60*np.sin(np.pi*u)+12*np.sin(2*np.pi*15*t))/SR
        x=(np.sin(phase)+.25*np.sin(2.013*phase))*envelope
        stem='foley'
    elif kind=='electric':
        phase=2*np.pi*np.cumsum(410+530*u)/SR
        x=(.4*np.sin(phase+2*np.sin(2*np.pi*49*t))+.3*noise(n,2800,1200))*envelope
        stem='electric'
    else:
        if kind=='effort':
            x=voice(t,[140,117,105,88],[(560,150,1),(1120,240,.5),(2300,300,.1)])
            x*=envelope*(.9+.1*np.sin(2*np.pi*11*t))
        elif kind=='gasp':
            x=.75*voice(t,[190,300,265,210],[(780,180,1),(1400,260,.45)])+.25*noise(n,2600,1200)
            x*=envelope
        elif kind=='hum':
            x=voice(t,[170,200,245,190],[(250,130,1),(900,200,.25)])*envelope
        else:
            raise ValueError(kind)
        stem='character'
    fade=np.minimum(1,t/.008)*np.minimum(1,(cue['duration']-t)/.016)
    x=x*fade
    x=x/max(np.max(np.abs(x)),1e-9)*cue['gain']
    pan=(cue['pan']+1)*np.pi/4
    return stem,np.column_stack((x*np.cos(pan),x*np.sin(pan)))

def write(name,x):
    assert np.isfinite(x).all() and np.max(np.abs(x))<1
    with wave.open(str(OUT/name),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
        w.writeframes(np.round(x*32767).astype('<i2').tobytes())

events=[]
for cue in CFG['cues']:
    start=round((cue['frame']-1)/CFG['fps']*SR)
    stem,x=synth(cue)
    assert 0<=start and start+len(x)<=COUNT
    STEMS[stem][start:start+len(x)]+=x
    events.append(dict(cue,start_sample=start,stem=stem))
mix=sum(STEMS.values())
assert len(mix)==480000 and np.max(np.abs(mix))<.95
for name,x in STEMS.items():
    write(name+'.wav',x)
write('mix-original.wav',mix)
(OUT/'synthesis-report.json').write_text(json.dumps({'sample_rate':SR,'samples':COUNT,
    'seconds':COUNT/SR,'raw_peak':float(np.max(np.abs(mix))),'seed':CFG['seed'],
    'origin':'Procedural oscillators, filtered noise and harmonic formants. No recordings, speech model, voice clone or third-party samples.',
    'cues':events},indent=2)+'\n')
print(f'Synthesized {len(events)} cues, four stereo stems, {COUNT/SR:.1f} seconds.')
