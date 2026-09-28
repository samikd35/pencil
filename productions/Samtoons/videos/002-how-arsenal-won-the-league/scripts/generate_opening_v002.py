"""Only changed Bottle FC lines; existing performances remain untouched."""
from pathlib import Path
import sys,json,hashlib
V=Path(__file__).resolve().parents[1];R=V.parents[3];O=V/'artifacts/opening-v002/voices';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'pipeline'));import qwen_voice as q
rows=[
('B01','Arsenal. New season. Same bottle.',42,'An elderly man, low weathered gravelly voice, restrained Scottish English accent. Original theatrical cartoon football manager voice. Calm smug certainty. Three dry thoughts, brief pauses, dismissive finality on same bottle.'),
('B02','This year, we finish the job.',43,'Adult man with a bright tight mid-register voice and light Spanish English accent. Comic football manager, clear English. Confident motivational promise to his players. Stress this year and finish.'),
('B03','I ordered a striker.',43,'Adult man with a bright tight mid-register voice and light Spanish English accent. Comic football manager, clear English. Annoyed bewilderment at a delivery error. Stress striker.'),
('B04','Sorry. Force of habit.',51,'Middle-aged British male delivery driver with a warm slightly husky voice. Matter-of-fact apology followed by a dry offhand explanation. No exaggerated joking or laughter.'),
('B05','Get me the striker. Now.',43,'Adult man with a bright tight mid-register voice and light Spanish English accent. Comic football manager, clear English. Clipped urgent order into a phone. Brief pause before an emphatic Now.')]
model=q.load_model(str(q.RUNTIME/'model'))
result=[]
for name,text,seed,direction in rows:
 p=O/(name+'.wav');direction+=' Clean dry microphone, no music or extra words.'
 if not p.exists():
  q.mx.random.seed(seed);chunks=list(model.generate_voice_design(text=text,language='English',instruct=direction,max_tokens=256));a=q.np.concatenate([q.np.asarray(c.audio).reshape(-1) for c in chunks]);assert q.np.isfinite(a).all() and .001<float(q.np.max(abs(a)))<=1.01;q.sf.write(p,a,chunks[0].sample_rate,subtype='PCM_24')
 r=dict(id=name,text=text,seed=seed,direction=direction,duration=q.sf.info(p).duration,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),heard_by_agent=False,source='Pinned local Qwen VoiceDesign; original caricature performance, not a real-person recording')
 p.with_suffix('.json').write_text(json.dumps(r,indent=2));result.append(r);print(name,r['duration'],flush=True)
(O/'takes.json').write_text(json.dumps(result,indent=2));(O/'model-source.json').write_bytes((q.RUNTIME/'model-source.json').read_bytes())
