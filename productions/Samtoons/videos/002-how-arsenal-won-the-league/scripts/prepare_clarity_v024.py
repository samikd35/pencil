"""Selected clarity revision; same cached voice model and character references."""
from pathlib import Path
import json,hashlib,subprocess,sys
V=Path(__file__).resolve().parents[1];O=V/'artifacts/clarity-v024';OLD=V/'artifacts/final-batch-v023'
LINES=[
('C00','CP00','ARTETA','City won again. They are right behind us! We are NOT handing Pep first place this year!','L21'),
('C19','CP01','NARRATOR','Arsenal were leading the league. Unfortunately, they had seen what happens when Pep starts following them.','L19'),
('C21','CP03_panic','ARTETA','We are sprinting! How is he getting closer?','L21'),
('C22','CP03_pep','PEP','You always get tired around this part, Mikel.','L22'),
('C24','CP04_courier','COURIER','Your annual second-place delivery! Same shelf as last time?','L24'),
('C25','CP04_courier','ARTETA','Cancel the subscription! We are winning it this year!','L21'),
('C27','VH01','REFEREE','He has pulled him down inside the box. Penalty against Arsenal!','L27'),
('C29','VH03_answer','OPERATOR','Mikel! Our priority customer. What can we cancel today?','L29'),
('C30','VH04_mikel','ARTETA','That penalty against us. Make it disappear. Same service as the rest of the season.','B02'),
('C31','VH04_operator','OPERATOR','Penalty cancelled. Would you like an Arsenal corner as a complimentary extra?','L29'),
('C32','VH04_two','ARTETA','Now that is customer service.','B02'),
('C33','VH05','OPERATOR','Decision: no penalty. Corner to Arsenal.','L29'),
('C34','VH05','REFEREE','But Arsenal committed the foul!','L27'),
('C34b','VH05','OPERATOR','And Arsenal will take the corner.','L29'),
('C35','FR01','NARRATOR','One goal would make Arsenal champions. Their entire season had come down to another corner.','L19'),
('C38','N03','NARRATOR','Come on. There is still time for Arsenal to bottle this.','L19'),
('C39','FR03_complain','GYÖKERES','You signed a striker, Mikel! When do I actually get to shoot?','L39'),
('C40','FR04','GYÖKERES','My first title-winning goal, and I did not even face the goal?','L40'),
('C42','FR05','COURIER','Then where am I taking all these second-place medals?','L24'),
('C43','FR05','ARTETA','Etihad Pharmacy. Ask for Pep. He will need something for the pain.','B02'),
('C48','N04_trophy','ARTETA','Nobody deserves this more than you.','B02'),
('C46','N04_meltdown','FERGUSON','I SAID I WAS RETIRED! Now Arsenal have won the league with a CORNER FLAG and a BACKSIDE! STOP GIVING ME REASONS TO COME BACK!','meltdown')]
(O/'lines.json').write_text(json.dumps([dict(id=i,shot=s,role=r,text=t,reference=ref) for i,s,r,t,ref in LINES],indent=2))
if __name__=='__main__':
 import mlx.core as mx,numpy as np,soundfile as sf
 from mlx_audio.tts.utils import load_model
 model=load_model(str(Path.home()/'Models/qwen-voice/base-model'))
 for idx,(ident,sid,role,words,refid) in enumerate(LINES):
  out=O/'voices'/f'{ident}.wav'
  if out.exists():continue
  if refid=='B02':ref=V/'artifacts/opening-v002/voices/B02.wav';reftext=json.loads(ref.with_suffix('.json').read_text())['text']
  elif refid=='meltdown':ref=Path(json.loads((OLD/'audio-plan.json').read_text())['assets']['meltdown']['path']);reftext='I SAID I WAS RETIRED! STOP GIVING ME REASONS TO COME BACK!'
  else:ref=OLD/'voices'/f'{refid}.wav';reftext=json.loads(ref.with_suffix('.json').read_text())['text']
  mx.random.seed(143+idx);chunks=list(model.generate(text=words,lang_code='English',ref_audio=str(ref),ref_text=reftext,temperature=.60,max_tokens=520));a=np.concatenate([np.asarray(c.audio).reshape(-1) for c in chunks]);sr=chunks[0].sample_rate;sf.write(out,a,sr,subtype='PCM_24')
  mix=out.with_name(ident+'-mix.wav');subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-y','-i',str(out),'-af','highpass=f=65','-ar','48000','-ac','1','-c:a','pcm_s24le',str(mix)],check=True);a,sr=sf.read(mix);gain=min(10**((-18 if role=='FERGUSON' else -21)/20)/max(np.sqrt(np.mean(a*a)),1e-9),.78/max(abs(a)));sf.write(mix,a*gain,sr,subtype='PCM_24')
  out.with_suffix('.json').write_text(json.dumps(dict(id=ident,shot=sid,role=role,text=words,reference=str(ref),reference_sha256=hashlib.sha256(ref.read_bytes()).hexdigest(),seconds=len(a)/sr,heard_by_agent=False),indent=2));print(ident,role,round(len(a)/sr,2),flush=True)
