from pathlib import Path
import json,time,hashlib
import mlx.core as mx
import numpy as np,soundfile as sf
from mlx_audio.tts.utils import load_model
V=Path(__file__).resolve().parents[1];O=V/'artifacts/defence-v019';R=V.parents[3]/'.runtime/qwen-voice';model=load_model(str(R/'base-model'))
lines=[('L13','ARTETA',"One nil! That's enough football. Everybody back!"),('L16','ARTETA','Win another corner!'),('L17','ARTETA','Nobody is getting past us.'),('L18','ARTETA','Again?'),('L15','GYÖKERES','What am I supposed to do?')]
for key,speaker,text in lines:
 p=O/'voices'/f'{key}.wav'
 if p.exists():continue
 ref=V/('artifacts/opening-v002/voices/B02.wav' if speaker=='ARTETA' else 'artifacts/animatic-v001/voices/L08.wav');meta=json.loads(ref.with_suffix('.json').read_text());mx.random.seed(43 if speaker=='ARTETA' else 44);start=time.monotonic();chunks=list(model.generate(text=text,lang_code='English',ref_audio=str(ref),ref_text=meta['text'],temperature=.65,max_tokens=280));a=np.concatenate([np.asarray(c.audio).reshape(-1) for c in chunks]);sf.write(p,a,chunks[0].sample_rate,subtype='PCM_24');p.with_suffix('.json').write_text(json.dumps(dict(id=key,text=text,speaker=speaker,reference=str(ref),reference_text=meta['text'],reference_sha256=hashlib.sha256(ref.read_bytes()).hexdigest(),seconds=len(a)/chunks[0].sample_rate,elapsed_seconds=time.monotonic()-start,heard_by_agent=False),indent=2));print(key,len(a)/chunks[0].sample_rate,flush=True)
