"""Final combined batch: cached takes, consistent Arteta voice, and event timing."""
from pathlib import Path
import json,sys,subprocess,shutil,hashlib,math
V=Path(__file__).resolve().parents[1];O=V/'artifacts/final-batch-v023'
for name in ['voices','clips','review-frames','sounds']:(O/name).mkdir(parents=True,exist_ok=True)
FF='/opt/homebrew/bin/ffmpeg'
def voices():
 import mlx.core as mx
 import numpy as np,soundfile as sf
 from mlx_audio.tts.utils import load_model
 model=None
 for i in range(19,48):
  ident=f'L{i:02}';src=V/'artifacts/animatic-v001/voices'/f'{ident}.wav';meta=json.loads(src.with_suffix('.json').read_text());dst=O/'voices'/src.name
  if dst.exists():continue
  if meta['role']=='ARTETA':
   if model is None:model=load_model(str(V.parents[3]/'.runtime/qwen-voice/base-model'))
   ref=V/'artifacts/opening-v002/voices/B02.wav';rm=json.loads(ref.with_suffix('.json').read_text());mx.random.seed(43+i)
   chunks=list(model.generate(text=meta['text'],lang_code='English',ref_audio=str(ref),ref_text=rm['text'],temperature=.65,max_tokens=280));a=np.concatenate([np.asarray(c.audio).reshape(-1) for c in chunks]);sf.write(dst,a,chunks[0].sample_rate,subtype='PCM_24');meta.update(reference=str(ref),reference_sha256=hashlib.sha256(ref.read_bytes()).hexdigest(),seconds=len(a)/chunks[0].sample_rate,selected_for_final=False,heard_by_agent=False)
  else:shutil.copy2(src,dst)
  dst.with_suffix('.json').write_text(json.dumps(meta,indent=2));print('VOICE',ident,meta['role'],flush=True)
  mix=dst.with_name(ident+'-mix.wav');subprocess.run([FF,'-v','error','-y','-i',str(dst),'-af','highpass=f=65','-ar','48000','-ac','1','-c:a','pcm_s24le',str(mix)],check=True)
  a,sr=sf.read(mix);g=min(10**(-21/20)/max(np.sqrt(np.mean(a*a)),1e-9),.78/max(abs(a)));sf.write(mix,a*g,sr,subtype='PCM_24')
def plan():
 import soundfile as sf
 old=json.loads((V/'artifacts/opening-v002/full-audio-plan.json').read_text());rows=json.loads((V/'artifacts/animation-v004/edit.json').read_text());rows=rows[next(i for i,r in enumerate(rows) if r['id']=='CP01'):]
 shots={s['id']:s for s in old['shots']};cues=[c for c in old['cues'] if c['shot'] in {r['id'] for r in rows}];captions=[];cursor=1
 # Use the selected story's voice anchors, expanding reaction space if a take needs it.
 for r in rows:
  r={k:v for k,v in r.items() if k not in ['clip','source','stage','panel','camera']};sid=r['id'];end=r['frames']
  for c in [c for c in cues if c['shot']==sid and c['stem']=='dialogue']:
   ident=c['asset'];p=O/'voices'/f'{ident}-mix.wav'
   if p.exists():
    dur=sf.info(p).duration;old['assets'][ident].update(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest());c['duration_seconds']=str(dur);f=shots[sid]['events'][c['event']];end=max(end,f+math.ceil(dur*24)+10)
    meta=json.loads((O/'voices'/f'{ident}.json').read_text());captions.append(dict(id=ident,shot=sid,speaker=meta['role'],text=meta['text'],local_frame=f+1,duration=dur))
  r.update(start_frame=cursor,frames=end,local_start=1);cursor+=end;shots[sid]['start_frame']=r['start_frame'];final.append(r)
 old['shots']=[shots[r['id']] for r in final];old['cues']=cues;old['timeline']['frames']=cursor-1;old['scope']='All remaining shots CP01 through N04_tap, one combined review batch';old['status']='review candidate';old['mix_gain_db']=-2
 for c in captions:c['start']=(shots[c['shot']]['start_frame']+c['local_frame']-2)/24;c['end']=c['start']+c['duration']
 # The selected Ferguson take contains both lines in one asset; retain its authored caption anchors.
 for ident,start,end in [('L46',3,55),('L47',71,130)]:
  meta=json.loads((O/'voices'/f'{ident}.json').read_text());t=(shots['N04_meltdown']['start_frame']+start-2)/24;captions.append(dict(id=ident,shot='N04_meltdown',speaker='FERGUSON',text=meta['text'],local_frame=start,duration=(end-start+1)/24,start=t,end=t+(end-start+1)/24))
 (O/'edit.json').write_text(json.dumps(final,indent=2));(O/'audio-plan.json').write_text(json.dumps(old,indent=2));(O/'captions.json').write_text(json.dumps(captions,indent=2))
 # Empty word lists keep the proven amplitude/vowel mouth control available without claiming phoneme alignment.
 (O/'word-analysis.json').write_text(json.dumps({f'L{i:02}':{'segments':[]} for i in range(19,48)},indent=2));print('PLAN',cursor-1,'frames',cursor/24,'seconds',flush=True)
final=[]
if __name__=='__main__':
 if 'voices' in sys.argv:voices()
 if 'plan' in sys.argv:plan()
