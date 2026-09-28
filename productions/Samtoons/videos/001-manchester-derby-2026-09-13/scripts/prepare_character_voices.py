"""Audition distinct stock voices and phrasing; preserve accepted B effects."""
from pathlib import Path
import subprocess,json,hashlib,wave,shutil
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/voices-v001';ART=ROOT/'assets/voices-v001';OUT.mkdir(exist_ok=True);ART.mkdir(exist_ok=True)
# These are performance candidates, not emotion controls supplied by Kokoro.
takes=[
 ('bruno-1','Ref!','am_puck',1.10,'Quick indignant burst, then let the pose carry the outrage.'),
 ('oliver-1',"I'm so... so sorry!",'bm_fable',1.02,'Hesitation before the repeated so, then the selected sob takes over.'),
 ('carrick-1','Any points with that?','bm_george',1.,'British, understated question after the paper lands.'),
 ('bruno-2','Ref! Ref!','bm_lewis',1.12,'Two impatient calls, escalating the same complaint.'),
 ('oliver-2',"I'm... so, so sorry!",'am_eric',1.04,'Hesitates immediately, then rushes to apologize.'),
 ('carrick-2','Any points with that?','bm_daniel',.96,'Alternative British voice with a slightly slower deadpan question.')]
records=[]
for ident,text,voice,speed,intent in takes:
 raw=ART/(ident+'-raw.wav');meta=raw.with_suffix('.json')
 if not raw.exists():
  if ident=='carrick-1':
   shutil.copy2(ROOT/'artifacts/voice-setup-v001/carrick-test.wav',raw);shutil.copy2(ROOT/'artifacts/voice-setup-v001/carrick-test.json',meta)
  else:
   with (OUT/(ident+'-generation.log')).open('w') as log:
    subprocess.run(['python3',str(ROOT/'scripts/kokoro_voice.py'),'--text',text,'--voice',voice,'--speed',str(speed),'--out',str(raw)],stdout=log,stderr=subprocess.STDOUT,check=True)
 info=json.loads(meta.read_text());target=ART/(ident+'.wav')
 # Modest processing gives speech a consistent audition level without pretending to synthesize an emotion.
 filters='highpass=f=85,loudnorm=I=-21:TP=-3:LRA=9,afade=t=in:d=0.008'
 if not target.exists():subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-i',str(raw),'-af',filters,'-ar','48000','-ac','1','-c:a','pcm_s24le',str(target)],check=True)
 with wave.open(str(target)) as w:duration=w.getnframes()/w.getframerate()
 records.append({'id':ident,'text':text,'voice':voice,'speed':speed,'intent':intent,'duration_seconds':duration,'path':str(target.relative_to(ROOT)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'generation':str(meta.relative_to(ROOT)),'processing':filters,'heard_by_agent':False})
 print(ident,round(duration,3),flush=True)
(ART/'takes.json').write_text(json.dumps(records,indent=2)+'\n')
base=json.loads((ROOT/'artifacts/sound-v001/plan-B.json').read_text())
for variant in ('1','2'):
 plan=json.loads(json.dumps(base));plan.update(title='Character cast '+variant+' on selected sound B',scope='Speaking voice audition; original v008 picture, provisional mouth synchronization; selected B effect source files/events/gains preserved.')
 plan.pop('variant',None)
 shot={s['id']:s for s in plan['shots']}
 for person,sid,event,frame,pan in [('bruno','S02','delayed_appeal',154,0),('oliver','S10','spoken_apology',49,-.25),('carrick','S10','deadpan_reply',221,.25)]:
  row=next(r for r in records if r['id']==person+'-'+variant);aid=row['id'];shot[sid]['events'][event]=frame-1
  plan['assets'][aid]={'path':'../../'+row['path'],'sha256':row['sha256'],'source':'Original stock synthetic speech using verified local Kokoro-82M v1.0 FP16; '+row['generation'],'license':'Kokoro model Apache-2.0; kokoro-onnx wrapper MIT; original script, no real-person voice clone','attribution':'Kokoro / hexgrad — https://huggingface.co/hexgrad/Kokoro-82M','notes':row['intent']}
  # Excerpt constraints expose a too-long read instead of silently speeding it up or cutting it off.
  available={'bruno':(214-154)/24,'oliver':(119-49)/24,'carrick':(265-221)/24}[person]
  assert row['duration_seconds']<available,(aid,row['duration_seconds'],available)
  plan['cues'].append({'id':aid,'shot':sid,'event':event,'asset':aid,'stem':'dialogue','intent':row['intent'],'duration_seconds':row['duration_seconds'],'gain_db':0,'pan':pan})
 (OUT/f'plan-{variant}.json').write_text(json.dumps(plan,indent=2)+'\n')
