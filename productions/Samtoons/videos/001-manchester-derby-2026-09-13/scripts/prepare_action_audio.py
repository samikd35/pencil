"""Cached original comic Foley candidates for the 28-second staging review.
No crowd replacement, generated speech, or claim of final performance.
"""
from pathlib import Path
import ast, json, math, random, struct, wave, hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'assets/audio-v002';OUT=ROOT/'artifacts/staging-v003'
A.mkdir(exist_ok=True)
# Reuse the existing bounded WAV writer without executing its old plan rewrite.
p=ROOT/'scripts/prepare_staging.py';tree=ast.parse(p.read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='tone'],type_ignores=[]),str(p),'exec'))
tau=math.tau
tone(A/'dry-impact.wav',.20,lambda t:.42*math.sin(tau*(110*t-80*t*t))*math.exp(-t*28)*min(1,t/.002)+.12*math.sin(tau*790*t)*math.exp(-t*90)*min(1,t/.001))
tone(A/'glove-catch.wav',.28,lambda t:.34*math.sin(tau*86*t)*math.exp(-t*20)*min(1,t/.003)+.11*math.sin(tau*640*t)*math.exp(-t*50)*min(1,t/.003))
tone(A/'ref-whistle.wav',.42,lambda t:.23*(math.sin(tau*2640*t+.8*math.sin(tau*35*t))+.3*math.sin(tau*3210*t))*min(1,t/.016)*min(1,(.42-t)/.045))
tone(A/'float-plop.wav',.40,lambda t:.40*math.sin(tau*(440*t+39*(1-math.exp(-t*12))))*math.exp(-t*13)*min(1,t/.004))
tone(A/'whistle-squeak.wav',.18,lambda t:.18*math.sin(tau*(1900*t+1800*t*t))*math.sin(math.pi*t/.18)**2)
rng=random.Random(10)
drops=[(i*.10+rng.uniform(0,.03),rng.uniform(450,1200),rng.uniform(.035,.075)) for i in range(22)]
def fountain(t):
    value=0.
    for onset,freq,amp in drops:
        d=t-onset
        if 0<d<.25:value+=amp*math.sin(tau*(freq*d+50*(1-math.exp(-d*18))))*math.exp(-d*25)*min(1,d/.003)
    return value
tone(A/'comic-fountain.wav',2.5,fountain)
durations={'dry-impact':.2,'glove-catch':.28,'ref-whistle':.42,'float-plop':.4,'whistle-squeak':.18,'comic-fountain':2.5}
assets={}
for name in durations:
    path=A/(name+'.wav');assets[name]={'path':'../../assets/audio-v002/'+path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source':'Original analytic synthesis in scripts/prepare_action_audio.py; comic Foley audition, not authentic match recording.','license':'Original production synthesis','attribution':''}
original=json.loads((ROOT/'production.json').read_text())['assets']['badge'].copy();original['path']='../../'+original['path'];assets['badge']=original;durations['badge']=.22
native=json.loads((OUT/'native-checks.json').read_text());shots=[];start=1
for shot,data in zip(['S02a','S02b','S08','S10'],native['scenes']):
    shots.append({'id':shot,'start_frame':start,'events':{event:frame-1 for event,frame in data['events'].items()}});start+=data['frames']
shots[-1]['events']['tail']=664-336
cues=[]
for shot,event,asset,gain,pan,intent in [
 ('S02a','kick_out','dry-impact',-5,-.2,'Small blunt contact at the kick-out; no heightened injury sound.'),
 ('S02b','red_card','ref-whistle',-4,0,'Referee decision punctuates the complaint.'),
 ('S02b','stamp','badge',-2,0,'Comic administrative stamp reuses the approved graphic-pop source.'),
 ('S02b','fishing_prop','badge',-7,.4,'Tiny accent establishes the rod for the final callback.'),
 ('S08','kick','dry-impact',-2,-.3,'Strike leaves Mbeumo’s boot.'),
 ('S08','save','glove-catch',0,.2,'Soft low thump as the gloves arrest the ball.'),
 ('S10','tears','comic-fountain',3,-.2,'Deliberately comic water burble, not a crying voice. Leave Carrick’s line quiet.'),
 ('S10','umbrella','badge',0,.2,'Pop accent when the umbrella canopy opens.'),
 ('S10','float_dip','float-plop',0,.45,'Fishing float gives the final callback its small payoff.'),
 ('S10','tail','whistle-squeak',-3,-.2,'Brief whistle hiccup ends the excerpt with a clean tail.')]:
    cues.append({'id':shot+'-'+event,'shot':shot,'event':event,'asset':asset,'stem':'foley','intent':intent,'duration_seconds':durations[asset],'gain_db':gain,'pan':pan})
plan={'version':1,'title':'Action staging Foley audition','timeline':{'fps':'24','start_frame':1,'frames':672,'sample_rate':48000},'shots':shots,'assets':assets,'cues':cues,'mix_gain_db':3,'status':'New sound candidates for user audition; no final dialogue. Existing B choice unchanged.'}
assert start==673 and len(cues)==10
(OUT/'audio-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
print('Cached six original Foley candidates; ten named event cues; 28-second staging only.')
