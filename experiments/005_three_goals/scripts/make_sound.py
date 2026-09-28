"""Original action/puzzle score and Foley, then a measured stereo normalization."""
from pathlib import Path
import ast, math, json, re, subprocess, wave
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v001/audio';OUT.mkdir(parents=True,exist_ok=True)
SR=48000;DURATION=30;COUNT=SR*DURATION;rng=np.random.default_rng(20221218)
stems={n:np.zeros((COUNT,2),dtype=np.float64) for n in ('music','foley','atmosphere')};cues=[]
for file,names in [(ROOT.parent/'001_heavy_box/scripts/sound_finish_v001.py',{'noise','voice','synth'}),(ROOT.parent/'003_alisson_winner/scripts/make_sound.py',{'add','note'})]:
    nodes=[n for n in ast.parse(file.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(nodes)==len(names)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(file),'exec'),globals())

def cue(kind,at,duration,gain,pan=0):
    d={'kind':kind,'duration':duration,'gain':gain,'pan':pan};_,x=synth(d);add('foley',at,x);cues.append(dict(d,seconds=at,frame=round(at*24)+1))
def pad(at,chord,duration,gain):
    for i,n in enumerate(chord):add('music',at,note(n,duration,'pad'),(i-(len(chord)-1)/2)*.35,gain)
def pulse(at,n,gain=.06):
    add('music',at,note(n,.7,'pluck'),-.20 if int(at*10)%2 else .20,gain)
def sub(at,duration=.40,gain=.22):
    t=np.arange(round(duration*SR))/SR;x=np.sin(2*np.pi*(62*t-32*t*t))*np.exp(-t*13)*np.minimum(1,t/.003);add('music',at,x,0,gain)

# Minor pulse; two hopeful returns, then an unresolved ending.
pad(0,[38,45,53],3.3,.043)
for at in (0,.8,1.6,2.25):sub(at,gain=.14)
for i,at in enumerate(np.arange(3.1,6,.32)):pulse(float(at),[62,65,69,65][i%4],.05)
pad(3.2,[38,45,53],3.0,.055)
pad(6.2,[41,48,57,64],3.75,.055)
for at,n in [(7.9,69),(8.25,72),(8.65,76),(9.1,74),(9.5,72)]:add('music',at,note(n,.95,'bell'),.12,.105)
pad(10.05,[33,40,46],1.0,.025)
pad(12.35,[38,45,53],2.9,.038)
for at in (13.2,13.95,14.6):sub(at,gain=.16)
pad(15.7,[41,48,57,64],2.25,.075)
for at,n in [(15.75,69),(16.1,72),(16.45,76),(16.85,79),(17.3,76)]:add('music',at,note(n,.95,'bell'),-.12,.12)
pad(18,[38,45,52],3.7,.05)
for i,at in enumerate(np.arange(18.2,21.3,.38)):pulse(float(at),[62,64,65,64][i%4],.036);sub(float(at),gain=.10)
# No triumphant resolution over the opponent's celebration.
pad(23.25,[50,57,63],6.1,.022)
add('music',27.05,note(62,2.7,'pad'),0,.065)
# Ball contacts are frame-aligned. Timed noise breaths are original sound design.
for at in (3,7.5,10.25,15.25,18.625,21.25):
    cue('tap',at,.15,.45,.05);cue('whoosh',at+.035,.40,.10,.25)
    cue('scrape',at+.45,.26,.17,.5)
for at in (2.50,2.72,6.35,6.65,7.03,7.85,14.82,15.02,18.15,18.40,20.60,20.86,21.06):cue('step',at,.10,.17,-.2)
for at,dur,gain in [(0.6,.80,.08),(1.75,.65,.09),(11.3,.48,.14),(12.0,.48,.13),(13.1,.45,.14),(13.75,.5,.13),(14.4,.40,.14),(23.8,.7,.10),(27.2,.62,.12),(28.15,.85,.12)]:cue('breath',at,dur,gain,0)
cue('whoosh',10,.22,.13,0);cue('whoosh',20.2,.25,.08,0)
for at in np.arange(23.1,24.8,.22):cue('step',float(at),.10,.07,.5)
# Layered filtered noise approximates stadium energy without words or source recordings.
for start in (0,6,12,18,24):
    dur=6;t=np.arange(dur*SR)/SR;x=noise(len(t),600,520)*(.75+.1*np.sin(t*3))*np.minimum(1,t/.25)*np.minimum(1,(dur-t)/.3)
    add('atmosphere',start,x,0,.015 if start<24 else .006)
for at,dur,gain in [(3.43,2.2,.07),(7.92,2.1,.10),(10.60,.55,.055),(15.67,2.3,.13),(19.05,1.0,.05),(21.70,2.0,.13),(25,2,.035)]:
    tt=np.arange(round(dur*SR))/SR;x=noise(len(tt),1150,1000)*np.minimum(1,tt/.18)*np.minimum(1,(dur-tt)/.55)
    add('atmosphere',at,x,.12,gain)
times=np.arange(COUNT)/SR
# Hard musical stops with a 15ms edge avoid clicks.
duck=np.ones(COUNT)
for at,end in [(10,11.2),(21.70,23.2)]:
    m=(times>=at-.015)&(times<at);duck[m]=np.minimum(duck[m],(at-times[m])/.015)
    duck[(times>=at)&(times<end)]=0
for at in (3,15.25):
    m=(times>at-.20)&(times<at);duck[m]*=.15
stems['music']*=duck[:,None]
envelope=np.minimum(1,times/.03)*np.minimum(1,(DURATION-times)/.8)
for name in stems:stems[name]*=envelope[:,None]
mix=sum(stems.values());gain=min(1,.87/np.max(np.abs(mix)))
def write(name,x):
    assert x.shape==(COUNT,2) and np.isfinite(x).all() and np.max(np.abs(x))<1
    with wave.open(str(OUT/name),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.round(x*32767).astype('<i2').tobytes())
for name,x in stems.items():write(name+'.wav',x*gain)
write('mix-original.wav',mix*gain)
ff='/opt/homebrew/bin/ffmpeg'
cmd=[ff,'-hide_banner','-i',str(OUT/'mix-original.wav'),'-af','loudnorm=I=-16:TP=-1.8:LRA=9:print_format=json','-f','null','-']
r=subprocess.run(cmd,capture_output=True,text=True,check=True);(OUT/'loudness-pass1.log').write_text(r.stderr)
levels=json.loads(re.findall(r'\{[^{}]+\}',r.stderr)[-1])
filt=f"loudnorm=I=-16:TP=-1.8:LRA=9:measured_I={levels['input_i']}:measured_TP={levels['input_tp']}:measured_LRA={levels['input_lra']}:measured_thresh={levels['input_thresh']}:offset={levels['target_offset']}:linear=true:print_format=json"
r=subprocess.run([ff,'-hide_banner','-y','-i',str(OUT/'mix-original.wav'),'-af',filt,'-ar','48000','-c:a','pcm_s16le',str(OUT/'soundtrack.wav')],capture_output=True,text=True,check=True);(OUT/'loudness-pass2.log').write_text(r.stderr)
(OUT/'sound-design.json').write_text(json.dumps({'origin':'Original instrumental synthesis, designed atmosphere and Foley. No narration, speech synthesis, voice clone or source audio.','sample_rate':SR,'duration':DURATION,'cue_count':len(cues),'cues':cues,'seed':20221218},indent=2)+'\n')
print('SOUND_READY',len(cues),'cues',flush=True)
