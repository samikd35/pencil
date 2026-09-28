"""Four contextual sound sketches, shared audio pipeline, scored/sparse comparison."""
from pathlib import Path
import json,math,hashlib,shutil,subprocess,sys
from fractions import Fraction
import numpy as np
import soundfile as sf
V=Path(__file__).resolve().parents[1]; ROOT=V.parents[3]; O=V/'artifacts/sound-direction-v001'; SR=48000
sys.path.insert(0,str(ROOT/'pipeline'));import audio
OLD=V.parent/'001-manchester-derby-2026-09-13'
FF='/opt/homebrew/bin/ffmpeg'
def run(args):
    p=subprocess.run([str(a) for a in args],capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-3000:])
    return p
assets={}
def register(name,path,source='Original production synthesis in build_sound_audition_v001.py',license='Original production composition/synthesis',credit=''):
    assets[name]=dict(path=str(path.relative_to(V)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),source=source,license=license,attribution=credit)
def write(name,data):
    assert np.isfinite(data).all() and np.max(np.abs(data))<1
    p=O/(name+'.wav');sf.write(p,data,SR,subtype='PCM_24');register(name,p);return p
# Preserve breath and performance dynamics; only trim outer silence and apply constant level.
for name in ['narrator','arteta','pep','hold','ref','meltdown']:
    raw=O/(name+'-raw.wav');p=O/(name+'.wav')
    filt='silenceremove=start_periods=1:start_duration=0.015:start_threshold=-48dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_duration=0.015:start_threshold=-48dB:start_silence=0.15,areverse,highpass=f=65'
    run([FF,'-v','error','-y','-i',raw,'-af',filt,'-ar',SR,'-ac',1,'-c:a','pcm_s24le',p])
    a,s=sf.read(p);rms=np.sqrt(np.mean(a*a));target=10**((-18 if name=='meltdown' else -21)/20)
    gain=min(target/max(rms,1e-9),.78/max(abs(a)));sf.write(p,a*gain,s,subtype='PCM_24')
    register(name,p,'Local Qwen VoiceDesign; exact text, direction, seed, model provenance in '+name+'-raw.json','Qwen model Apache-2.0; generated candidate')
# Plot sounds, intentionally short and distinct; no synthetic crowd bed.
def pluck(freq,dur,amp=.22):
    t=np.arange(round(dur*SR))/SR
    return amp*(np.sin(2*np.pi*freq*t)+.3*np.sin(2*np.pi*freq*2*t)+.12*np.sin(2*np.pi*freq*3*t))*np.exp(-t*5)*np.minimum(t/.003,1)
def music(notes,duration):
    x=np.zeros(round(duration*SR))
    for time,freq,length,amp in notes:
        a=pluck(freq,length,amp);i=round(time*SR);x[i:i+len(a)]+=a
    return x
write('question-motif',music([(0,146.83,.7,.24),(.75,155.56,.8,.22)],1.6))
write('answer-note',pluck(196,1.1,.22))
write('city-ping',music([(0,880,.22,.14),(.12,1174.66,.35,.12)],.5))
rng=np.random.default_rng(902);t=np.arange(round(.09*SR))/SR
write('switch',rng.normal(0,.11,len(t))*np.exp(-t*100)*np.minimum(t/.001,1))
write('tiny-tap',pluck(430,.14,.045))
notes=[]
for i,midi in enumerate([72,76,79,76,74,77,81,77,72,76,79,84,79,76,74,72]):
    notes.append((i*.34,440*2**((midi-69)/12),.3,.075))
write('hold-tune',music(notes,5.5))
run([FF,'-v','error','-y','-i',O/'hold-tune.wav','-af','highpass=f=380,lowpass=f=2800','-c:a','pcm_s24le',O/'hold-phone.wav'])
register('hold-phone',O/'hold-phone.wav')
run([FF,'-v','error','-y','-i',O/'hold.wav','-af','highpass=f=350,lowpass=f=3200','-c:a','pcm_s24le',O/'hold.wav.tmp.wav'])
(O/'hold.wav.tmp.wav').replace(O/'hold.wav');register('hold',O/'hold.wav','Local Qwen; original menu performance with telephone-band processing','Qwen model Apache-2.0; generated candidate')
p=O/'chase-score.mp3';shutil.copy2(OLD/'assets/music-v001/Scheming Weasel faster.mp3',p)
register('chase-score',p,'https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1100085','CC BY 4.0','Scheming Weasel (faster version) by Kevin MacLeod (incompetech.com), CC BY 4.0 https://creativecommons.org/licenses/by/4.0/ . Excerpted and faded.')
# Conservative short foot accents; full film must bind each to its actual contact.
p=O/'boot.wav';shutil.copy2(OLD/'assets/door-v003/boot-step.wav',p);register('boot',p,'Original episode 001 seeded boot-contact synthesis, prepare_revision_audio.py','Original production synthesis')
p=O/'paper.wav';shutil.copy2(OLD/'assets/audio-v003/paper-crumple.wav',p)
register('paper',p,'https://freesound.org/people/Ezcah/sounds/248178/','CC0','Paper by Ezcah, Freesound 248178; processed excerpt.')
D={k:sf.info(V/a['path']).duration for k,a in assets.items() if a['path'].endswith('.wav')}
# Excerpts use performed duration. Silence after replies is deliberately retained.
narr_end=2+D['narrator']; chase_start=math.ceil((narr_end+.8)*24)/24
pep_start=chase_start+.5+D['arteta']+.55
hold_start=math.ceil((pep_start+D['pep']+1)*24)/24
ref_start=hold_start+.5+D['hold']+.55
reveal_start=math.ceil((ref_start+D['ref']+1.3)*24)/24
lamp=reveal_start+1.7;shout=lamp+1.2;end=math.ceil((shout+D['meltdown']+1.6)*24)/24
plan=dict(version=1,scope='Sound-direction four-excerpt review only',timeline=dict(fps='24',start_frame=1,frames=round(end*24),sample_rate=SR),shots=[dict(id='audition',start_frame=1,events={})],assets=assets,cues=[],mix_gain_db=-2)
def cue(name,time,stem='foley',gain=0,dur=None,intent=None):
    cid=name+'-'+str(len(plan['cues']));plan['shots'][0]['events'][cid]=time*24
    plan['cues'].append(dict(id=cid,shot='audition',event=cid,asset=name,stem=stem,intent=intent or name,duration_seconds=str(Fraction(round((dur if dur else D[name])*SR),SR)),gain_db=gain,fade_in_seconds=.005,fade_out_seconds=.03))
cue('switch',0);cue('question-motif',.15,'music',-2);cue('narrator',2,'dialogue')
cue('arteta',chase_start+.5,'dialogue');cue('city-ping',chase_start+.08,'plot-effects',-3)
cue('chase-score',chase_start,'score',-22,pep_start-chase_start-.15,'Busy Arsenal score gives way to effortless Pep')
cue('pep',pep_start,'dialogue');cue('hold',hold_start+.5,'dialogue')
cue('hold-phone',hold_start+.3+D['hold'],'music',-2,min(5.5,reveal_start-(hold_start+.3+D['hold'])-.15),'Bland courtesy persists as the ignored referee loses confidence')
cue('ref',ref_start,'dialogue');cue('question-motif',reveal_start,'music',-2)
cue('switch',lamp);cue('answer-note',lamp,'music',-2);cue('meltdown',shout,'dialogue')
cue('paper',shout+D['meltdown']+.1,'foley',-8,.8);cue('tiny-tap',shout+D['meltdown']+1,'foley',0)
# Not faking exact foot synchronization against stills. The optional foot source is preserved, unused.
meta=dict(narr_end=narr_end,chase_start=chase_start,pep_start=pep_start,hold_start=hold_start,ref_start=ref_start,reveal_start=reveal_start,lamp=lamp,shout=shout,end=end)
(O/'timing.json').write_text(json.dumps(meta,indent=2))
if not (O/'production-before.json').exists(): (O/'production-before.json').write_bytes((V/'production.json').read_bytes())
existing=json.loads((V/'production.json').read_text());existing.update(plan);existing['status']='pending_review';existing['audio_status']='Sound-direction v001 candidates; no listening acceptance';existing['latest_sound_audition']=dict(path='artifacts/sound-direction-v001',status='pending_review',animation_feedback='Chase-v002 defects retained')
(V/'production.json').write_text(json.dumps(existing,indent=2)+'\n')
# Snapshots use correct relative asset roots; shared executable mixer remains authoritative.
for variant in ['A','B']:
    p=json.loads(json.dumps(plan));p['assets']={k:{**v,'path':'../../'+v['path']} for k,v in assets.items()}
    if variant=='B':p['cues']=[c for c in p['cues'] if c['stem']!='score']
    path=O/('plan-'+variant+'.json');path.write_text(json.dumps(p,indent=2)+'\n')
    run([sys.executable,ROOT/'pipeline/audio.py','build',path,'--out',O/('mix-'+variant)])
# Exact same constant output gain on both versions keeps speech matched for comparison.
for variant in ['A','B']:
    run([FF,'-v','error','-y','-i',O/('mix-'+variant)/'mix-premaster.wav','-ar',48000,'-c:a','pcm_s24le',O/('audition-'+variant+'.wav')])
print(json.dumps(meta),flush=True)
# Standalone meaningful check: output duration and foreground identical, scored section only changes.
a,s=sf.read(O/'audition-A.wav');b,s2=sf.read(O/'audition-B.wav');assert a.shape==b.shape and s==s2==48000
assert len(a)==round(end*SR) and np.isfinite(a).all() and np.max(abs(a))<1
lo=round(chase_start*SR);hi=round(pep_start*SR)
assert np.max(abs(a[:lo]-b[:lo]))<2e-6 and np.max(abs(a[hi:]-b[hi:]))<2e-6
assert np.max(abs(a[lo:hi]-b[lo:hi]))>.0001
(O/'comparison-check.json').write_text(json.dumps(dict(duration=end,peak_A=float(np.max(abs(a))),peak_B=float(np.max(abs(b))),matched_dialogue=True,difference='chase score only',heard_by_agent=False),indent=2))
