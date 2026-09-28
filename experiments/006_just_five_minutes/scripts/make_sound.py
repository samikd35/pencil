"""Original sparse comic Foley and a small instrumental scrolling loop; no speech."""
from pathlib import Path
import ast, json, math, re, subprocess, wave
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v001/audio';OUT.mkdir(exist_ok=True)
SR=48000;DURATION=30;COUNT=SR*DURATION;rng=np.random.default_rng(20260911)
stems={n:np.zeros((COUNT,2),dtype=np.float64) for n in ('music','foley')}
for path,names in [(ROOT.parent/'001_heavy_box/scripts/sound_finish_v001.py',{'noise','voice','synth'}),(ROOT.parent/'003_alisson_winner/scripts/make_sound.py',{'add','note'})]:
    nodes=[n for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert len(nodes)==len(names)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),globals())
cues=[]
def cue(kind,t,d=.13,g=.16,p=0):
    data=dict(kind=kind,duration=d,gain=g,pan=p);_,sound=synth(data);add('foley',t,sound)
    cues.append(dict(data,seconds=t,frame=round(t*30)+1))
cue('tap',.25,.10,.13)
for t in (3.08,3.36):
    tt=np.arange(round(.18*SR))/SR
    buzz=(np.sin(2*np.pi*145*tt)+.25*noise(len(tt),650,500))*np.sin(np.pi*tt/.18)**2
    add('foley',t,buzz,.15,.12)
    cues.append(dict(kind='phone buzz',seconds=t,frame=round(t*30)+1))
cue('tap',4.40,.10,.12,-.2)
cue('whoosh',6,.45,.10,-.7);cue('whoosh',8.9,.55,.08,-.7)
for i in range(15):
    t=10.15+i*.48
    if t<17.35:add('music',t,note([60,64,67,64,62,65,69,65][i%8],.34),-.2 if i%2 else .2,.035)
for t in np.arange(10.3,17.5,.69):cue('tap',float(t),.045,.055,-.25)
for t in (10.8,11.6,12.3,12.9,13.4,13.8,14.1,14.35,14.55,14.72,14.86):cue('tap',t,.05,.075,.45)
cue('tap',15,.17,.28,.4)
cue('creak',21.6,.48,.075,-.2)
cue('tap',24.10,.1,.17,.2)
cue('tap',24.9,.08,.10,.3)
for i,t in enumerate((27.08,27.26,27.42,27.56,27.69,27.80,27.90,28.00)):
    cue('step',t,.075,.13*(1-i/10),-.3+i*.04)
cue('whoosh',27.25,.7,.075);cue('tap',28.22,.15,.08);cue('whoosh',28.22,.27,.10)
mix=sum(stems.values());gain=min(1,.8/max(np.max(np.abs(mix)),1e-9))
def write(name,x):
    assert x.shape==(COUNT,2) and np.isfinite(x).all() and np.max(np.abs(x))<1
    with wave.open(str(OUT/name),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.round(x*32767).astype('<i2').tobytes())
for name,x in stems.items():write(name+'.wav',x*gain)
write('mix-original.wav',mix*gain)
ff='/opt/homebrew/bin/ffmpeg'
r=subprocess.run([ff,'-hide_banner','-i',str(OUT/'mix-original.wav'),'-af','loudnorm=I=-18:TP=-2:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
levels=json.loads(re.findall(r'\{[^{}]+\}',r.stderr)[-1])
filt=f"loudnorm=I=-18:TP=-2:LRA=9:measured_I={levels['input_i']}:measured_TP={levels['input_tp']}:measured_LRA={levels['input_lra']}:measured_thresh={levels['input_thresh']}:offset={levels['target_offset']}:linear=true:print_format=json"
r=subprocess.run([ff,'-hide_banner','-y','-i',str(OUT/'mix-original.wav'),'-af',filt,'-ar','48000','-c:a','pcm_s16le',str(OUT/'soundtrack.wav')],capture_output=True,text=True,check=True)
(OUT/'normalization.log').write_text(r.stderr)
(OUT/'sound-design.json').write_text(json.dumps(dict(origin='Original synthesis using existing Pencil Foley helpers; no speech or source-video audio.',seconds=30,sample_rate=SR,cues=cues),indent=2)+'\n')
print('SOUND_COMPLETE',len(cues),'cues')
