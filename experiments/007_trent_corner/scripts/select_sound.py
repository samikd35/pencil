"""Cache original sound selections; cue timing comes from Blender's production.json events."""
from pathlib import Path
import ast, hashlib, json, math, wave
import numpy as np
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'assets/audio-v001';SR=48000
source=ROOT.parent/'001_heavy_box/scripts/sound_finish_v001.py'
names={'noise','voice','synth'}
nodes=[n for n in ast.parse(source.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names]
assert len(nodes)==len(names)
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),globals())
plan=json.loads((ROOT/'production.json').read_text());assets={}
def save(name,x,description):
    if x.ndim==1:x=np.column_stack((x,x))
    assert x.shape[1]==2 and np.isfinite(x).all() and len(x)>0
    x=x/max(np.max(np.abs(x)),1e-8)*.72
    path=ASSETS/(name+'.wav')
    if not path.exists():
        with wave.open(str(path),'wb') as w:
            w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.round(x*32767).astype('<i2').tobytes())
    assets[name]={'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source':'Original deterministic NumPy synthesis in scripts/select_sound.py; '+description,'license':'Original generated production audio; no external samples. Available for this production and its revisions.','attribution':'','notes':'Selected final synthesis, not archival match audio.'}
def env(t,d):return np.minimum(1,t/.008)*np.minimum(1,(d-t)/.035)
for name,kind,d,seed in [('turf','step',.16,11),('freeze','tap',.22,22),('net','scrape',.48,33),('release','whoosh',.36,44)]:
    rng=np.random.default_rng(seed);_,x=synth({'kind':kind,'duration':d,'gain':.7,'pan':0})
    if name=='net':x*=np.exp(-np.arange(len(x))[:,None]/SR*4)
    save(name,x,f'Pencil {kind}, seed {seed}, {d} s')
for name,d,freq,seed in [('corner',.32,108,55),('finish',.42,145,66)]:
    rng=np.random.default_rng(seed);t=np.arange(round(d*SR))/SR
    x=(.78*np.sin(math.tau*(freq*t-65*t*t))+.35*noise(len(t),1300,1000))*np.exp(-t*22)*env(t,d)
    save(name,x,f'Boot/ball impact, {freq} Hz falling membrane and filtered contact noise, seed {seed}')
for name,d,seed in [('stadium',9,77),('cheer',9,88),('hush',7,99)]:
    rng=np.random.default_rng(seed);t=np.arange(round(d*SR))/SR;channels=[]
    for channel in range(2):
        x=noise(len(t),600 if name=='hush' else 1050,500 if name=='hush' else 1050)
        x*=.65+.12*np.sin(math.tau*.47*t+channel)+.12*np.sin(math.tau*1.39*t+channel*2)
        # Massed nonverbal vowel-like resonances; intentionally synthetic, no words/recording.
        if name=='cheer':
            for j in range(9):x+=.08*np.sin(math.tau*(130+j*19)*t+3*np.sin(t*(2+j*.11)))*(.5+.5*np.sin(t*(3+j*.07)))
        x*=np.minimum(1,t/(.45 if name=='cheer' else .12))*np.minimum(1,(d-t)/1.0)
        channels.append(x)
    save(name,np.column_stack(channels),f'Stereo filtered stadium texture, seed {seed}, {d} s; nonverbal synthesis')
for name,notes,d,seed in [('notice',[67,74],2.1,111),('tension',[50,57,62],7,122),('resolve',[55,59,62,67],7,133)]:
    rng=np.random.default_rng(seed);t=np.arange(round(d*SR))/SR;x=np.zeros_like(t)
    for i,note in enumerate(notes):
        at=i*.22 if name=='notice' else i*.08;tt=np.maximum(0,t-at);f=440*2**((note-69)/12)
        tone=(np.sin(math.tau*f*tt)+.21*np.sin(math.tau*f*2.004*tt))
        tone*=np.minimum(1,tt/.025)*np.exp(-tt*(1.7 if name=='notice' else .60))*(t>=at)
        x+=tone/len(notes)
    if name=='tension':x*=.64+.36*np.cos(t*math.tau*1.3)**2
    x*=np.minimum(1,(d-t)/.7)
    save(name,x,'Original instrumental sine partials; MIDI notes '+str(notes))
plan['assets']=assets;plan['cues']=[]
def cue(id,shot,event,asset,stem,duration,gain=-12,offset=0,pan=0,onset=0,fade=.02):
    assert asset in assets
    plan['cues'].append({'id':id,'shot':shot,'event':event,'intent':id.replace('-',' '),'asset':asset,'stem':stem,'in_seconds':0,'duration_seconds':duration,'onset_seconds':onset,'offset_frames':offset,'gain_db':gain,'pan':pan,'fade_in_seconds':.004,'fade_out_seconds':fade})
cue('establish-stadium','setup','start','stadium','atmosphere',2,-15,fade=.2)
cue('stop-time','freeze','hold','freeze','editorial',.22,-17)
cue('held-perspective','freeze','hold','hush','atmosphere',5,-25,fade=.3)
cue('swap-stadium','swap','resume','stadium','atmosphere',3,-19,fade=.3)
for i,event in enumerate(('step_a','step_b')):cue('swap-foot-'+str(i),'swap',event,'turf','foley',.16,-18,pan=.65)
cue('notice-motif','opening','notice','notice','music',2.1,-14)
cue('opportunity-hush','opening','notice','hush','atmosphere',4,-27,fade=.3)
cue('anticipation','swap','resume','tension','music',7,-23,fade=.3)
cue('return-plant','action','plant','turf','foley',.16,-19,pan=.65)
cue('time-resumes','action','resume','release','editorial',.36,-21)
cue('action-atmosphere','action','resume','stadium','atmosphere',2.7,-19,fade=.2)
for shot in ('action','replay'):
    gain=0 if shot=='action' else -6
    cue(shot+'-corner',''+shot,'corner_contact','corner','foley',.32,-6+gain,pan=.55,onset=.008)
    cue(shot+'-finish',shot,'origi_contact','finish','foley',.42,-3+gain,pan=-.15,onset=.008)
    cue(shot+'-net',shot,'net_contact','net','foley',.48,-10+gain,pan=-.55,onset=.008)
cue('goal-cheer','action','cheer','cheer','atmosphere',6.333333,-8,fade=.65)
cue('goal-resolution','action','net_contact','resolve','music',6.5,-14,fade=.8)
cue('replay-perspective','replay','start','hush','atmosphere',6,-23,fade=.3)
cue('replay-observation','replay','start','notice','music',2.1,-23)
cue('final-cheer','payoff','title','cheer','atmosphere',6.6,-14,fade=1.4)
cue('final-resolution','payoff','title','resolve','music',6.6,-17,fade=1.4)
plan['mix_gain_db']=-3
plan['audio_direction']={'authority':'pipeline/audio.py premaster, then two-pass FFmpeg loudnorm','original_sound':True,'quiet_intervals_seconds':[[2,7],[10,14],[23,29],[35.6,36]],'subjective_listening':'Not performed; actual listening is still required.'}
(ROOT/'production.json').write_text(json.dumps(plan,indent=2)+'\n')
print('SELECTED',len(assets),'assets;',len(plan['cues']),'cues')
