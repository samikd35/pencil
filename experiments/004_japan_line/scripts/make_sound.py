"""Original action/puzzle score and Foley, then a measured stereo normalization."""
from pathlib import Path
import ast, math, json, re, subprocess, wave
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v001/audio';OUT.mkdir(parents=True,exist_ok=True)
SR=48000;DURATION=32;COUNT=SR*DURATION;rng=np.random.default_rng(20221201)
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

# Urgent opening, suspended question, spacious reveal, then the sporting release.
pad(0,[38,45,53],2.5,.035)
for i,at in enumerate(np.arange(0,2.5,.265)):pulse(float(at),[50,57,62,57][i%4],.060);sub(float(at),gain=.11)
pad(3.6,[45,52,59],5.7,.028)
for i,at in enumerate(np.arange(4.2,9.0,.6)):pulse(float(at),[69,71,76,71][i%4],.025)
pad(9.4,[41,48,57,64],4.3,.056)
for at,n in [(9.45,69),(9.75,72),(10.2,76),(11,72)]:add('music',at,note(n,1.2,'bell'),.15,.09)
pad(13.8,[38,45,53,60],5.4,.030)
for at,n in [(14.2,62),(15.5,60),(17.1,64),(17.8,69)]:pulse(at,n,.034)
pad(19,[41,48,57,64],1.9,.045)
pad(21,[38,45,53],5.3,.045)
for i,at in enumerate(np.arange(21,26,.265)):pulse(float(at),[62,65,69,72][i%4],.052);sub(float(at),gain=.13)
pad(26.25,[38,45,54,62],5.75,.075)
for at,n in [(26.3,74),(26.6,78),(27.0,81),(27.6,78),(28.2,74),(29,73),(29.8,74)]:add('music',at,note(n,1.2,'bell'),-.08,.105)

# Footsteps match the authored sprint's half-cycle contacts.
for i,at in enumerate(np.arange(0,1.45,.53/2)):cue('step',float(at),.10,.19,(-1 if i%2 else 1)*.13)
cue('step',1.46,.12,.23,-.05);cue('whoosh',1.85,.65,.15,.20)
cue('tap',2.60,.09,.13,.25)
cue('whoosh',4.0,.5,.11,0);cue('whoosh',5.1,1.7,.09,-.4)
cue('tap',9.45,.10,.12,-.15);cue('whoosh',14.2,.65,.07,.15)
cue('tap',15.7,.08,.10,.15);cue('whoosh',17.1,.6,.07,-.15);cue('tap',17.85,.09,.11,-.1)
cue('whoosh',19,.35,.10,0)
cue('tap',21,.15,.46,.40);cue('scrape',21.10,.48,.22,.20)
cue('whoosh',21.18,.85,.13,-.35)
cue('step',24.65,.12,.20,.1);cue('tap',25.375,.14,.30,0)
cue('whoosh',25.47,.65,.13,-.45);cue('scrape',26.25,.3,.22,-.6)
for at in [28.3,28.6,28.9,29.15]:cue('step',at,.10,.10,.15)
for start in (0,8,16,24):
    t=np.arange(8*SR)/SR;x=noise(8*SR,650,550)*np.minimum(1,t/.5)*np.minimum(1,(8-t)/.6);add('atmosphere',start,x,0,.007)
# Designed broadband release texture, not a crowd or source recording.
t=np.arange(round(2.8*SR))/SR;x=noise(len(t),1500,900)*np.sin(np.pi*t/2.8)**2;add('atmosphere',26.1,x,0,.042)
times=np.arange(COUNT)/SR;envelope=np.minimum(1,times/.015)*np.minimum(1,(DURATION-times)/.65)
# Allow the freeze and the decisive cutback their own short acoustic space.
duck=np.ones(COUNT);duck[(times>2.60)&(times<3.5)]=.06
for name in stems:stems[name]*=envelope[:,None]
stems['music']*=duck[:,None]
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
(OUT/'sound-design.json').write_text(json.dumps({'origin':'Original instrumental synthesis, designed atmosphere and Foley. No narration, speech synthesis, voice clone or source audio.','sample_rate':SR,'duration':DURATION,'cue_count':len(cues),'cues':cues,'seed':20221201},indent=2)+'\n')
print('SOUND_READY',len(cues),'cues',flush=True)
