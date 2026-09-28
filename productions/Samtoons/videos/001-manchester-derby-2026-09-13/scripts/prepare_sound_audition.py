"""Two event-aligned Foley/vocal-reaction auditions on approved v008 picture."""
from pathlib import Path
import json,hashlib,subprocess,ast,math,random,wave
ROOT=Path(__file__).resolve().parents[1];ASSET=ROOT/'assets/audio-v003';OUT=ROOT/'artifacts/sound-v001';OUT.mkdir(exist_ok=True)
FF='/opt/homebrew/bin/ffmpeg';sources={r['name']:r for r in json.loads((ASSET/'provenance.json').read_text())};records={}
def prepare(name,source,start,duration,filters):
 p=ASSET/(name+'.wav');cmd=[FF,'-v','error','-ss',str(start),'-t',str(duration),'-i',str(ASSET/(source+'-decoded.wav')),'-af',filters,'-ar','48000','-ac','1',str(p)]
 if not p.exists():subprocess.run(cmd,check=True)
 row=sources[source];records[name]={'path':'../../assets/audio-v003/'+p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source':row['page'],'license':row['license'][0],'attribution':f'{source} by {row["user"]} — {row["page"]} — {row["license"][0]}; excerpted and processed.','notes':json.dumps({'start':start,'source_seconds':duration,'filters':filters,'download':row['download'],'quality':row['quality']})}
prepare('paper-handoff','paper',.12,.55,'highpass=f=140,afade=t=in:d=0.01,afade=t=out:st=0.45:d=0.1,alimiter=limit=0.5:level=false')
prepare('paper-crumple','paper',.4,1.6,'atempo=1.6,highpass=f=120,afade=t=in:d=0.02,afade=t=out:st=0.85:d=0.15,alimiter=limit=0.55:level=false')
prepare('card-flick','paper',1.60,.16,'highpass=f=800,afade=t=in:d=0.003,afade=t=out:st=0.08:d=0.08')
prepare('shirt-move','cloth',.56,.65,'highpass=f=120,afade=t=in:d=0.02,afade=t=out:st=0.5:d=0.15')
prepare('ball-strike','kick',.32,.55,'highpass=f=55,afade=t=in:d=0.003,afade=t=out:st=0.35:d=0.2')
prepare('glove-parry','kick',.33,.35,'highpass=f=180,lowpass=f=5200,afade=t=in:d=0.003,afade=t=out:st=0.18:d=0.17')
prepare('sob-A','sob',.65,3.35,'highpass=f=100,lowpass=f=8000,afade=t=in:d=0.05,afade=t=out:st=2.95:d=0.4,alimiter=limit=0.65:level=false')
prepare('sob-B','sob',2.05,3.1,'rubberband=pitch=1.12,highpass=f=130,afade=t=in:d=0.05,afade=t=out:st=2.7:d=0.4,alimiter=limit=0.65:level=false')
# Reuse the production's original WAV writer and established synthesized graphic accents.
p=ROOT/'scripts/prepare_staging.py';tree=ast.parse(p.read_text());scope={'wave':wave,'math':math,'random':random};exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='tone'],type_ignores=[]),str(p),'exec'),scope)
import struct
scope['struct']=struct
for name,length,fn in [('innocent-chime',.6,lambda t:.22*(math.sin(math.tau*1320*t)+.3*math.sin(math.tau*2640*t))*math.exp(-t*9)*min(1,t/.004)),('comic-recoil',.28,lambda t:.22*math.sin(math.tau*(240*t-300*t*t))*math.exp(-t*16)*min(1,t/.002))]:
 p=ASSET/(name+'.wav')
 if not p.exists():scope['tone'](p,length,fn)
 records[name]={'path':'../../assets/audio-v003/'+p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source':'Original graphic synthesis in scripts/prepare_sound_audition.py','license':'Original production synthesis','attribution':''}
for name,file in [('dry-impact','dry-impact'),('whistle','ref-whistle')]:
 p=ROOT/'assets/audio-v002'/(file+'.wav');records[name]={'path':'../../assets/audio-v002/'+p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source':'Original synthesis in scripts/prepare_action_audio.py; new audition only','license':'Original production synthesis','attribution':''}
def duration(name):
 with wave.open(str(OUT/records[name]['path'])) as w:return w.getnframes()/w.getframerate()
native=json.loads((ROOT/'artifacts/staging-v008/native-checks.json').read_text());shots=[];start=1
for sid,scene,frames in [('S02','S02 / kick and overreaction',336),('S08','S08 / hope and parry',168),('S10','S10 / tears and umbrella',264)]:
 events={k:v-1 for k,v in native['scene_events'][scene].items()};shots.append({'id':sid,'start_frame':start,'events':events});start+=frames
assert start==769 and shots[0]['events']['red_card']==275 and shots[2]['events']['tears']==118
for variant in ('A','B'):
 cues=[]
 def cue(shot,event,asset,gain,pan,intent,stem='foley',onset=0,offset=0):
  cues.append({'id':f'{shot}-{event}-{asset}','shot':shot,'event':event,'asset':asset,'stem':stem,'intent':intent,'duration_seconds':duration(asset),'gain_db':gain,'pan':pan,'onset_seconds':onset,'offset_frames':offset})
 cue('S02','tussle','shirt-move',-12,-.2,'Clothing friction in the tussle')
 cue('S02','kick_out','dry-impact',-4,-.2,'One contact, followed by exaggerated reaction')
 cue('S02','bruno_ground_contact','dry-impact',-2,-.1,'Soft comic landing')
 cue('S02','bruno_rise','shirt-move',-10,0,'Clothing shuffle on recovery')
 cue('S02','complaint','paper-handoff',-5,0,'Paper interrupts Bruno’s dramatic outrage')
 cue('S02','red_card','card-flick',-4,.25,'Flick on raised card')
 cue('S02','red_card','whistle',-6,.25,'Decision whistle')
 cue('S08','strike','ball-strike',-2,-.3,'Recorded football strike',onset=.03)
 cue('S08','glove_parry','glove-parry',-2,.25,'Short sharp deflection contact; processed ball recording, not a catch',onset=.02)
 cue('S10','letter_handoff','paper-handoff',-5,.1,'Letter changes hands before crying')
 cue('S10','tears','sob-'+variant,-5,-.25,'Recorded male sobbing reaction; final speaking voice remains to cast','vocal-reaction')
 cue('S10','crumple','paper-crumple',-3,.2,'Carrick crumples the apology')
 cue('S10','bin_landing','dry-impact',-20,.15,'Tiny bin landing accent')
 if variant=='B':
  cue('S02','bruno_fall','comic-recoil',-8,0,'Brief graphic recoil accent')
  cue('S02','innocent_halo','innocent-chime',-9,0,'Innocent halo chime; A leaves this quiet','comic-accents')
 plan={'version':1,'title':f'Samtoons sound audition {variant}','timeline':{'fps':'24','start_frame':1,'frames':768,'sample_rate':48000},'shots':shots,'assets':records,'cues':cues,'mix_gain_db':0,'scope':'Effects and recorded nonverbal sobs only. No spoken dialogue or final cast selection. Same approved v008 picture; no new music or crowd.','variant':'Restrained' if variant=='A' else 'Light comic accents and brighter sob take'}
 (OUT/f'plan-{variant}.json').write_text(json.dumps(plan,indent=2)+'\n')
(ASSET/'prepared-assets.json').write_text(json.dumps(records,indent=2)+'\n')
(OUT/'credits.md').write_text('# Sound audition credits\n\n'+ '\n\n'.join(r['attribution'] for k,r in records.items() if k in ('paper-handoff','shirt-move','ball-strike','sob-A'))+'\n\nSynthesis: original Pencil graphic accents. The glove parry is a processed football impact, not an authentic goalkeeper recording. Downloaded MP3 previews are audition sources; source links and processing are retained.\n')
print('Prepared two 32-second event-aligned auditions; spoken dialogue still pending.')
