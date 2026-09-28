"""Record new dialogue against selected synthetic voices, never redesign each line's speaker."""
from pathlib import Path
import json,time,hashlib
import mlx.core as mx
import numpy as np,soundfile as sf
from mlx_audio.tts.utils import load_model
V=Path(__file__).resolve().parents[1];O=V/'artifacts/dialogue-v018';R=Path.home()/'Models/qwen-voice';old=V/'artifacts/opening-v002/voices'
lines=[
('B02','ARTETA',"This year, no excuses. I'm lifting that trophy, not applauding somebody else!"),
('B03','ARTETA',"Bottles? Three years finishing second, and you've made us a subscription?"),
('B04','DRIVER',"Automatic renewal, boss. Cancel any time. Preferably before April."),
('B05','ARTETA',"Hello, board? Buy me Gyokeres. A proper striker. Someone who finishes!"),
('L07b','ARTETA','Meet our real striker.'),
('L09','ARTETA',"Win us corners. That's where we score."),
('L10','ARTETA',"Don't shoot! Hit the defender. Off him, out for a corner!"),
('L11','ARTETA',"Perfect. A corner! Now we can actually score.")]
(O/'dialogue.json').write_text(json.dumps([dict(id=k,speaker=s,text=t) for k,s,t in lines],indent=2))
model=load_model(str(R/'base-model'))
for key,speaker,text in lines:
 p=O/'voices'/f'{key}.wav'
 if p.exists():continue
 ref=old/('B04.wav' if speaker=='DRIVER' else 'B02.wav');meta=json.loads(ref.with_suffix('.json').read_text());mx.random.seed(43 if speaker=='ARTETA' else 51);start=time.monotonic()
 chunks=list(model.generate(text=text,lang_code='English',ref_audio=str(ref),ref_text=meta['text'],temperature=.65,max_tokens=320))
 a=np.concatenate([np.asarray(c.audio).reshape(-1) for c in chunks]);sr=chunks[0].sample_rate
 assert len(a)>sr*.3 and np.isfinite(a).all()
 sf.write(p,a,sr,subtype='PCM_24');p.with_suffix('.json').write_text(json.dumps(dict(id=key,text=text,speaker=speaker,reference=str(ref),reference_text=meta['text'],reference_sha256=hashlib.sha256(ref.read_bytes()).hexdigest(),model='mlx-community/Qwen3-TTS-12Hz-0.6B-Base-4bit',revision='0d6bb6fe33f92d47a507e23b9148940e8366ab5b',seconds=len(a)/sr,elapsed_seconds=time.monotonic()-start,heard_by_agent=False),indent=2));print(key,len(a)/sr,time.monotonic()-start,flush=True)
