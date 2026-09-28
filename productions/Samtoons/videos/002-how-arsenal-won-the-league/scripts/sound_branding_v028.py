"""Original three-note sonic logo, sparse outro arrangement, existing production Foley."""
from pathlib import Path
import sys,math,wave,struct,random,json,hashlib,shutil
V=Path(__file__).resolve().parents[1];ROOT=V.parents[3];O=V/'artifacts/branding-v028';A=O/'sounds';A.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT));from pipeline.audio import build
SR=48000
def write(name,duration,notes,groove=False):
 a=[0.0]*round(duration*SR)
 for start,midi,amp,length in notes:
  hz=440*2**((midi-69)/12)
  for k in range(round(length*SR)):
   j=round(start*SR)+k
   if j>=len(a):break
   t=k/SR;env=min(1,t/.006)*math.exp(-t*5/length)*min(1,(length-t)/.04)
   sig=(math.sin(math.tau*hz*t)+.36*math.sin(math.tau*hz*2*t)*math.exp(-t*12)+.18*math.sin(math.tau*hz*3.99*t)*math.exp(-t*20))
   a[j]+=sig*env*amp
 if groove:
  rng=random.Random(28)
  for beat in range(20):
   start=.5+beat*.5
   for k in range(1800):
    j=round(start*SR)+k
    if j>=len(a):break
    t=k/SR;a[j]+=(.016*rng.uniform(-1,1)*math.exp(-t*100) if beat%2 else .075*math.sin(math.tau*(80*t-400*t*t))*math.exp(-t*85))
 with wave.open(str(A/name),'wb') as w:w.setparams((2,2,SR,0,'NONE','not compressed'));w.writeframes(b''.join(struct.pack('<hh',int(max(-.95,min(.95,x))*32767),int(max(-.95,min(.95,x))*32767)) for x in a))
write('three-note-signature.wav',1.55,[(0,72,.23,.5),(.18,76,.22,.5),(.43,81,.22,1.05)])
notes=[]
for bar in range(5):
 start=bar*2
 notes.extend([(start,48 if bar%2==0 else 53,.13,.4),(start+.75,60 if bar%2==0 else 65,.09,.32),(start+1.5,67 if bar%2==0 else 69,.085,.42)])
write('outro-groove.wav',10.5,notes,True)
source1=V.parent/'001-manchester-derby-2026-09-13'
for src,dst in [(source1/'assets/audio-v002/dry-impact.wav','ball-impact.wav'),(source1/'assets/audio-v002/ref-whistle.wav','whistle.wav'),(source1/'assets/audio-v003/paper-handoff.wav','paper-handoff.wav'),(source1/'assets/audio-v003/paper-crumple.wav','paper-crumple.wav')]:shutil.copy2(src,A/dst)
assets={}
for p in A.glob('*.wav'):
 paper=p.name.startswith('paper');assets[p.stem]={'path':'sounds/'+p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source':'https://freesound.org/people/Ezcah/sounds/248178/' if paper else ('Original synthesis in sound_branding_v028.py' if p.name in ['three-note-signature.wav','outro-groove.wav'] else 'Original production synthesis reused from Samtoons001/scripts/prepare_action_audio.py'),'license':'CC0' if paper else 'Original production synthesis','attribution':'Paper by Ezcah, CC0, excerpted and processed.' if paper else ''}
def cue(name,event,asset,stem,duration,gain=0):return {'id':name,'shot':'brand','event':event,'intent':name.replace('-',' '),'asset':asset,'stem':stem,'duration_seconds':duration,'gain_db':gain,'fade_in_seconds':.004,'fade_out_seconds':.025}
for stem,frames,events,cues in [('intro',72,{'impact':12,'whistle':21,'signature':30},[cue('ball-contact','impact','ball-impact','foley',.2,-2),cue('referee-offscreen','whistle','whistle','foley',.42,-8),cue('wordmark-signature','signature','three-note-signature','music',1.55,-1)]),('outro',288,{'paper-arrive':0,'paper-shake':17,'signature':37,'groove':36},[cue('paper-flight','paper-arrive','paper-handoff','foley',.55,-1),cue('paper-shake-off','paper-shake','paper-crumple','foley',1,-5),cue('mascot-grin','signature','three-note-signature','music',1.55,-2),cue('endcard-groove','groove','outro-groove','music',10.5,-4)])]:
 plan={'version':1,'timeline':{'fps':24,'start_frame':1,'frames':frames,'sample_rate':SR},'shots':[{'id':'brand','start_frame':1,'events':events}],'assets':assets,'cues':cues,'mix_gain_db':-1};path=O/(stem+'-sound-plan.json');path.write_text(json.dumps(plan,indent=2));build(path,O/(stem+'-audio'))
print('Sound candidates built; listening approval remains pending.')
