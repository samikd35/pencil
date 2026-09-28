"""Resolve the approved revision from actual cached take durations."""
from pathlib import Path
from fractions import Fraction
import json,math,hashlib,shutil,soundfile as sf
V=Path(__file__).resolve().parents[1];O=V/'artifacts/clarity-v024';OLD=V/'artifacts/final-batch-v023';prior=json.loads((OLD/'audio-plan.json').read_text());oldrows={r['id']:r for r in json.loads((OLD/'edit.json').read_text())};lines=json.loads((O/'lines.json').read_text());new={l['id']:l for l in lines}
# Minimum durations protect action/reaction; dialogue determines any needed extension.
layout=[('CP00',36,['C00']),('CP01',168,['C19']),('CP02_far',75,['L20']),('CP02_near',36,[]),('CP03_panic',60,['C21']),('CP03_pep',60,['C22']),('CP04_courier',120,['C24']),('CP04_reply',48,['C25']),('CP05',48,['L26']),('VH01',156,['C27']),('VH02',80,['L28']),('VH03',30,[]),('VH03_answer',60,['C29']),('VH04_mikel',60,['C30']),('VH04_operator',60,['C31']),('VH04_two',48,['C32']),('VH04_button',30,[]),('VH05',108,['C33','C34','C34b']),('FR01',144,['C35']),('FR02',120,['L36','L37']),('N03',84,['C38']),('FR03_complain',96,['C39']),('FR03_cross',120,[]),('FR04',120,['C40','L41']),('FR05',144,['C42','C43']),('N04_trophy',144,['C48']),('N04_dark',72,[]),('N04_reveal',36,[]),('N04_meltdown',180,['C46']),('N04_tap',60,[])]
rows=[];caps=[];cursor=1
for sid,minimum,ids in layout:
 f=46 if sid=='VH01' else 23 if sid=='CP00' else 16 if sid in ['CP01','FR01','N04_trophy'] else 7
 if sid=='N04_meltdown':f=3
 entries=[]
 for ident in ids:
  p=O/'voices'/f'{ident}-mix.wav'
  if ident.startswith('L'):
   for suffix in ['.wav','-mix.wav','.json']:
    src=OLD/'voices'/(ident+suffix)
    if src.exists():shutil.copy2(src,O/'voices'/src.name)
  meta=json.loads((O/'voices'/f'{ident}.json').read_text());info=sf.info(p);dur=info.duration;entries.append(dict(id=ident,frame=f,seconds=dur,role=meta['role'],text=meta['text']));f+=math.ceil(dur*24)+7
 frames=max(minimum,f+5)
 # The complaint is interrupted at the next kick; no ball hangs in the air for it.
 rows.append(dict(id=sid,start_frame=cursor,frames=frames,local_start=1,scene='S002_clarity_v024_'+sid,dialogue=entries,source_scene='S002_final_v023_'+('VH04_mikel' if sid=='CP00' else 'CP04_forward' if sid=='CP04_reply' else sid)))
 for e in entries:caps.append(dict(id=e['id'],shot=sid,speaker=e['role'],text=e['text'],local_frame=e['frame'],start=(cursor+e['frame']-2)/24,end=(cursor+e['frame']-2)/24+e['seconds']))
 cursor+=frames
plan={k:v for k,v in prior.items() if k not in ['shots','cues','assets']};plan['timeline']['frames']=cursor-1;plan['scope']='Approved clarity revision, City notification through final reveal';plan['assets']=dict(prior['assets']);plan['cues']=[];plan['shots']=[dict(id=r['id'],start_frame=r['start_frame'],events={}) for r in rows];shots={s['id']:s for s in plan['shots']}
def add(asset,sid,f,stem,gain=0,duration=None,intent=None):
 cid=f'{sid}_{asset}_{len(plan["cues"])}';shots[sid]['events'][cid]=f-1;inf=sf.info(plan['assets'][asset]['path']);dur=Fraction(inf.frames,inf.samplerate) if duration is None else Fraction(str(duration));plan['cues'].append(dict(id=cid,shot=sid,event=cid,asset=asset,stem=stem,intent=intent or asset,duration_seconds=str(dur),gain_db=gain,fade_in_seconds=.004,fade_out_seconds=.04,allow_boundary_trim=True))
for r in rows:
 for e in r['dialogue']:
  p=O/'voices'/f'{e["id"]}-mix.wav';plan['assets'][e['id']]=dict(path=str(p.resolve()),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),source='Qwen reference-conditioned local voice; existing voice identity',license='Generated performance, local model unchanged',attribution='Samtoons — original generated dialogue, conditioned on selected character take');add(e['id'],r['id'],e['frame'],'dialogue')
# Preserve the selected music/crowd atmosphere and motif; drop old dialogue/hold callbacks.
valid=set(shots);skip=['boot','paper','confirmation','ball-strike','dry-impact','goal-cheer','meltdown','ref-whistle','approval-choir','fortress-swell']
for c in prior['cues']:
 if c['shot'] not in valid or c['stem']=='dialogue' or c['asset'] in skip or c['id'].startswith('final23-'):continue
 if c['shot'] in ['VH05','VH03_answer','VH04_operator'] and ('hold' in c['asset'] or 'hold' in c.get('intent','').lower()):continue
 oldshot=next(s for s in prior['shots'] if s['id']==c['shot']);f=oldshot['events'][c['event']]+1
 if f>next(r['frames'] for r in rows if r['id']==c['shot']):continue
 add(c['asset'],c['shot'],f,c['stem'],c.get('gain_db',0),float(Fraction(c['duration_seconds'])),c.get('intent'))
for r in rows:
 if r['id'].startswith('CP') and r['id'] not in ['CP00','CP04_courier']:
  for f in range(1,r['frames']+1,14 if r['id']=='CP03_pep' else 8):add('boot',r['id'],f,'foley',-17 if r['id']=='CP03_pep' else -22)
add('ref-whistle','VH01',42,'plot-effects',-8);add('confirmation','VH04_button',9,'plot-effects',-15);add('ball-strike','FR03_cross',29,'foley',-5);add('dry-impact','FR03_cross',64,'plot-effects',-3);add('goal-cheer','FR03_cross',85,'crowd',-5);add('fortress-swell','FR03_cross',1,'music',-18);add('approval-choir','N04_trophy',16,'music',-14)
used={c['asset'] for c in plan['cues']};plan['assets']={k:v for k,v in plan['assets'].items() if k in used};plan['status']='review candidate; subjective listening pending'
for name,data in [('edit.json',rows),('captions.json',caps),('audio-plan.json',plan),('word-analysis.json',{c['id']:{'segments':[]} for c in caps})]:(O/name).write_text(json.dumps(data,indent=2))
print('remaining',cursor-1,'frames;',round((cursor-1+2992)/24,2),'seconds complete')
assert cursor-1+2992<=7200,'Revise actual editorial timing if longer than five minutes'
assert not any(r['id'] in ['VH06','VH05_wait','FR03_bonk','FR03_goal'] for r in rows)
