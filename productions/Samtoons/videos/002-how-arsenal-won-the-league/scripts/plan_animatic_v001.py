from pathlib import Path
import json,math,shutil,hashlib,sys,subprocess
from fractions import Fraction
import numpy as np,soundfile as sf
V=Path(__file__).resolve().parents[1];ROOT=V.parents[3];O=V/'artifacts/animatic-v001';S=V/'artifacts/sound-direction-v001';OLD=V.parent/'001-manchester-derby-2026-09-13';SR=48000
sys.path.insert(0,str(ROOT/'pipeline'));import audio
FF='/opt/homebrew/bin/ffmpeg'
def run(args):
 p=subprocess.run([str(a) for a in args],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-2000:])
 return p
# Shot name, chapter sheet, panel (0 based), seconds, dialogue IDs, opening speech delay.
# Durations budget concrete entrances, reactions, visual reveals, contacts, and recovery.
spec=[
('N01',1,0,8,[1],2),('OP01_enter',1,1,8,[2],1),('OP01_offer',1,2,4,[3],.7),('OP02',1,3,6,[4,5],.6),('OP03_close',1,4,1.5,[],0),('OP03_phone',1,5,3.5,[6],.6),
('TR01',2,0,8,[7],1),('TR02_flag',2,1,4,[],0),('TR02_reaction',2,2,6,[8,9],.5),('TR03_warning',2,3,4,[10],.3),('TR03_kick',2,4,3,[],0),('TR03_praise',2,5,3.5,[11],.4),('TR04',3,0,2,[],0),
('CD01_cross',3,0,8,[12],.3),('CD01_header',3,1,3,[],0),('CD02',3,2,5,[13],.2),('CD03',3,3,5,[],0),('CD04',3,4,5,[14],.5),('CD05',3,5,6,[15,16],.3),('N02',1,0,2,[],0),('CD05_proud',3,2,3.5,[17],.2),('CD05_ping',3,2,2.5,[18],.7),
('CP01',4,0,9,[19],.7),('CP02_far',4,1,5,[20],.7),('CP02_near',4,2,3,[],0),('CP03_panic',4,3,3.5,[21],.6),('CP03_pep',4,2,4,[22],.7),('CP04_forward',4,3,4,[23],.4),('CP04_courier',4,4,6,[24,25],.5),('CP05',4,5,5,[26],1.6),
('VH01',5,0,5,[27],1.8),('VH02',5,1,6,[28],.6),('VH03',5,2,2,[],0),('VH03_answer',5,3,4,[29],.6),('VH04_mikel',5,4,4,[30],.7),('VH04_operator',5,3,4.5,[31],.5),('VH04_two',5,4,2.5,[32],.4),('VH04_button',5,5,2,[],0),('VH05',7,1,6.5,[33,34],.4),('VH05_wait',7,1,3,[],0),
('FR01',6,0,8,[35],1),('FR02',6,1,6,[36,37],.5),('N03',1,0,3.5,[38],.6),('FR03_cross',6,2,3,[],0),('FR03_complain',6,1,4,[39],.6),('FR03_bonk',6,3,1,[],0),('FR03_goal',6,4,3,[],0),('FR04',6,5,6,[40,41],.6),('FR05',7,0,6,[42,43],.6),('VH06',7,1,7,[44,45],.5),
('N04_trophy',7,2,5,[],0),('N04_dark',7,3,4,[],0),('N04_reveal',7,4,1.5,[],0),('N04_meltdown',7,5,7,[46,47],.1),('N04_tap',7,5,2.5,[],0)]
takes={int(x['id'][1:]):x for x in json.loads((O/'voices/takes.json').read_text())}
assets={};cues=[];shots=[];edit=[];cursor=1;subtitles=[]
def register(k,p,source,license,attribution=''):
 assets[k]=dict(path=str(p.relative_to(V)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),source=source,license=license,attribution=attribution)
def duration(k):return audio.probe(V/assets[k]['path'])['duration']
# Adopt exact selected A source files locally by copy; their hashes remain unchanged.
for k,a in json.loads((S/'plan-A.json').read_text())['assets'].items():
 src=(S/a['path']).resolve();dest=O/'sounds'/src.name;dest.parent.mkdir(exist_ok=True);shutil.copy2(src,dest);register(k,dest,a['source'],a['license'],a['attribution'])
for n,r in takes.items():
 src=V/r['path'];dst=O/'voices'/f'L{n:02}-mix.wav'
 if n in [1,22,33]:shutil.copy2(src,dst)
 else:
  run([FF,'-v','error','-y','-i',src,'-af','highpass=f=65','-ar',SR,'-ac',1,'-c:a','pcm_s24le',dst])
  a,sr=sf.read(dst);target=10**(-21/20);gain=min(target/max(np.sqrt(np.mean(a*a)),1e-9),.78/max(abs(a)));sf.write(dst,a*gain,SR,subtype='PCM_24')
 register(f'L{n:02}',dst,'Local directed Qwen take; voice JSON retains text, direction, provenance and hearing limits','Qwen model Apache-2.0; generated performance')
# Preserve the selected combined meltdown, including its breath and transition.
register('meltdown',O/'sounds/meltdown.wav','Exact selected sound-direction A combined meltdown','Qwen model Apache-2.0; generated performance')
def add(shot,key,at,stem='foley',gain=0,seconds=None,intent=''):
 cid=f'{shot["id"]}_{key}_{len(cues)}';shot['events'][cid]=round(at*24)
 dur=Fraction(duration(key));dur=min(dur,Fraction(str(seconds))) if seconds is not None else dur
 cues.append(dict(id=cid,shot=shot['id'],event=cid,asset=key,stem=stem,intent=intent or key,duration_seconds=str(dur),gain_db=gain,fade_in_seconds=.005,fade_out_seconds=.06))
for name,ch,panel,secs,ids,lead in spec:
 shot=dict(id=name,start_frame=cursor,events={});local=lead
 if name=='N04_meltdown':
  add(shot,'meltdown',local,'dialogue');d=float(Fraction(duration('meltdown')));subtitles.append(dict(start=(cursor-1)/24+local,end=(cursor-1)/24+local+d,text=takes[46]['text']+' '+takes[47]['text']))
  local+=d+.4
 else:
  for n in ids:
   key=f'L{n:02}';d=float(Fraction(duration(key)));add(shot,key,local,'dialogue');subtitles.append(dict(start=(cursor-1)/24+local,end=(cursor-1)/24+local+d,text=takes[n]['text']));local+=d+.5
 frames=math.ceil(max(secs,local+.35)*24);edit.append(dict(id=name,chapter=ch,panel=panel,start_frame=cursor,frames=frames,lines=ids,source=f'boards/chapter-{ch}.png',camera='hold'))
 shots.append(shot);cursor+=frames
assert sorted(n for row in edit for n in row['lines'])==list(range(1,48))
by={s['id']:s for s in shots};E={s['id']:s for s in edit}
def cue(shot,key,at=0,stem='foley',gain=0,seconds=None,intent=''):add(by[shot],key,at,stem,gain,seconds,intent)
# Plot motifs and purposeful negative space. Sound leads no unseen football outcomes.
cue('N01','switch');cue('N01','question-motif',.15,'music',-2)
cue('N02','question-motif',0,'music',-4);cue('N02','paper',.85,'foley',-10,1)
cue('CD05_ping','city-ping',.05,'plot-effects',-2);cue('CP02_near','city-ping',.05,'plot-effects',-2)
for sh in ['CP01','CP02_far','CP02_near','CP03_panic','CP04_forward','CP04_courier','CP05']:
 cue(sh,'chase-score',0,'music',-24,E[sh]['frames']/24,'Selected A chase score; absent under Pep reply')
for sh in ['VH02','VH05','VH05_wait']:
 at=4 if sh=='VH02' else 0;remain=E[sh]['frames']/24-at
 if remain>0:cue(sh,'hold-phone',at,'music',-4,min(remain,5.5))
cue('N03','question-motif',.1,'music',-5);cue('N04_dark','question-motif',2.3,'music',-2)
cue('N04_reveal','switch');cue('N04_reveal','answer-note',0,'music',-2)
cue('N04_tap','paper',0,'foley',-8,1);cue('N04_tap','tiny-tap',.8)
# Recorded material detail: selected cached sources; no synthetic stadium hiss.
prep=json.loads((OLD/'assets/audio-v003/prepared-assets.json').read_text())
for k in ['ball-strike','shirt-move','paper-handoff']:
 a=prep[k];src=(OLD/'artifacts/sound-v003'/a['path']).resolve()
 src=OLD/'assets/audio-v003'/Path(a['path']).name;dst=O/'sounds'/src.name;shutil.copy2(src,dst);register(k,dst,a['source'],a['license'],a['attribution'])
for key in ['ref-whistle','dry-impact']:
 p=OLD/'assets/audio-v002'/(key+'.wav');dst=O/'sounds'/p.name;shutil.copy2(p,dst);register(key,dst,'Original episode001 graphic synthesis','Original production synthesis')
prov=json.loads((OLD/'assets/audio-v001/prior-provenance.json').read_text())['sources']['crowd-goal'];p=ROOT/'experiments/007_trent_corner/assets/audio-v002/crowd-goal.wav';dst=O/'sounds/crowd-goal.wav';shutil.copy2(p,dst);register('goal-cheer',dst,prov['source'],prov['license'],prov['attribution'])
for sh in ['TR03_kick','CD01_cross','FR03_cross']:cue(sh,'ball-strike',.15,'foley',-6)
cue('CD01_header','ball-strike',.1,'foley',-7);cue('CD01_header','goal-cheer',.4,'crowd',-5,2.5)
cue('VH01','shirt-move',.1,'foley',-3);cue('VH01','ref-whistle',1,'foley',-6,.5)
cue('OP03_close','dry-impact',0,'foley',-7,.18);cue('CD03','dry-impact',4,'foley',-7,.18)
cue('VH04_button','city-ping',.25,'plot-effects',-8,.4)
cue('FR03_bonk','dry-impact',.05,'foley',-5,.18)
cue('FR03_goal','goal-cheer',.2,'crowd',-2,2.7)
cue('FR04','ref-whistle',E['FR04']['frames']/24-.65,'foley',-8,.5)
cue('N04_trophy','goal-cheer',0,'crowd',-5,4.9)
cue('FR05','paper-handoff',E['FR05']['frames']/24-.7,'foley',-8,.5)
# Reject boundary truncation in each shot, not just the full movie.
for c in cues:
 sh=by[c['shot']];assert sh['events'][c['event']]/24+float(Fraction(c['duration_seconds']))<=E[c['shot']]['frames']/24+.001,c['id']
plan=dict(version=1,scope='Complete illustrated audiovisual storyboard animatic; no finished body-animation claim',status='pending_review',timeline=dict(fps='24',start_frame=1,frames=cursor-1,sample_rate=SR),shots=shots,assets=assets,cues=cues,mix_gain_db=-2)
(O/'edit.json').write_text(json.dumps(edit,indent=2));(O/'subtitles.json').write_text(json.dumps(subtitles,indent=2,ensure_ascii=False))
# Keep a local reproducible audio snapshot with adjusted paths; preserve prior selected review.
if not (O/'production-before.json').exists():shutil.copy2(V/'production.json',O/'production-before.json')
existing=json.loads((V/'production.json').read_text());existing.update(plan);existing['picture']='artifacts/animatic-v001/arsenal-animatic-v001.mp4';existing['native_scene']='artifacts/animatic-v001/arsenal-animatic-v001.blend';existing['latest_animatic']=dict(status='in_progress',movement='New pose blocking only; continuous gait refinement remains open. No rejected cycle reused.');(V/'production.json').write_text(json.dumps(existing,indent=2))
for a in plan['assets'].values():a['path']='../../'+a['path']
(O/'audio-plan.json').write_text(json.dumps(plan,indent=2))
print('Timeline:',(cursor-1)/24,'seconds;',len(edit),'shots;',len(cues),'cues',flush=True)
run([sys.executable,ROOT/'pipeline/audio.py','build',O/'audio-plan.json','--out',O/'mix'])
