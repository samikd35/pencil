"""Cache remaining directed lines, loading the existing local model once."""
from pathlib import Path
import sys,json,time,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT.parents[3]
sys.path.insert(0,str(WORK/'pipeline'))
from qwen_voice import mx,np,sf,load_model,RUNTIME
OUT=ROOT/'assets/film-voices-v001'
# Same actor description and seed across a character's new lines; VoiceDesign
# timbre consistency still needs listening review, it is not an identity guarantee.
CAST={
'Haaland':('Young adult male, bright medium-low resonant voice, light Scandinavian English accent, clipped playful robot rhythm, clear consonants.',81),
'Foden':('Young adult male, youthful light Manchester English accent, slightly nasal forward voice, cheeky and impatient.',47),
'Bruno':('Adult male, medium pitch slightly rough forward voice, light Portuguese English accent, expressive urgent football captain.',8),
'Post':('Deep rich British male baritone with confident theatrical diction, smug experienced professional.',44),
'VAR':('Middle-aged British man, dry clipped bureaucratic diction, thin precise voice.',54),
'Martinez':('Young adult man, light Argentine English accent, rough mid-low voice with urgent force.',6),
'Lammens':('Young adult male, light Belgian English accent, clear warm medium voice.',31),
'Maresca':('Middle-aged man, slightly gravelly low voice, light Italian English accent, forceful clipped articulation.',17)}
ROWS=[
('morning','Haaland','Morning, Pep.','Bright sincere greeting with a smile. Brief pause before PEP, warmly pleased.'),
('and-him','Foden','And HIM?!','An indignant shouted accusation. Hit HIM hard with rising disbelief, breath pressure, not a polite question.'),
('fishing','Foden',"Fine. I'm going fishing.",'Tight sulky FINE, then a short breath and defiant quick dismissal.'),
('less-problem','Bruno','One less problem.','Smug satisfied relief, compact pleased finish, falsely confident.'),
('contract','Post','Two saves. I want a new contract.','Self-satisfied demand. Strong TWO, admiring pause, brisk decisive CONTRACT.'),
('var','VAR','Onside. No touch. Goal.','Overconfident administrative finality. Three separate clipped decisions.'),
('him','Martinez','What about HIM?','Urgent shouted interruption. Stress HIM angrily, do not trail off.'),
('yes','Haaland','YEEEES!','Explosive joyful sustained victory yell, powerful attack, jubilant raised voice and satisfied release. Really shout.'),
('ours','Lammens','Ours works too!','Surprised relief turns into smiling discovery. Lift OURS and TOO.'),
('surely','Bruno','Surely now...','Breath held in hope, quiet tense SURELY, suspended expectation on NOW.'),
('wolf','Haaland','Good wolf.','Low affectionate approval with a small pleased smile, reassuring.'),
('thanks','Haaland','Thanks, Pep.','Cheerful sincere gratitude, smiling, upbeat PEP.'),
('enzo','Maresca','ENZO!','Sudden fed-up corrective shout, explosive name, exasperated force. Loud projected bark, not a neutral read.'),
('pep-two','Haaland','Pep two point oh.','Thinking pause before speaking, then proudly pleased confident solution, oblivious to the mistake.'),
('biting','Foden',"Keep going, ref. They're biting.",'Relaxed delighted cheeky aside. Encourage KEEP GOING, then smile about the fish.')]
def main():
 OUT.mkdir(exist_ok=True);start=time.monotonic();model=None;records=[]
 for slug,person,words,acting in ROWS:
  raw=OUT/(slug+'-raw.wav');out=OUT/(slug+'.wav');meta=raw.with_suffix('.json')
  voice,seed=CAST[person];direction=voice+' '+acting
  if not raw.exists():
   if model is None:
    model=load_model(str(RUNTIME/'model'));print('MODEL_LOADED',round(time.monotonic()-start,1),flush=True)
   mx.random.seed(seed);t=time.monotonic();chunks=list(model.generate_voice_design(text=words,language='English',instruct=direction,max_tokens=256))
   assert chunks;sr=chunks[0].sample_rate;audio=np.concatenate([np.asarray(c.audio).reshape(-1) for c in chunks]);assert np.isfinite(audio).all() and len(audio)>sr*.1
   sf.write(raw,audio,sr,subtype='PCM_24');meta.write_text(json.dumps(dict(character=person,text=words,direction=direction,seed=seed,generation_seconds=time.monotonic()-t,sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),model_source=json.loads((RUNTIME/'model-source.json').read_text()),heard_by_agent=False),indent=2)+'\n')
  assert hashlib.sha256(raw.read_bytes()).hexdigest()==json.loads(meta.read_text())['sha256']
  if not out.exists():
   level=-18 if slug in ('and-him','him','yes','enzo') else -21
   filters='silenceremove=start_periods=1:start_duration=0.015:start_threshold=-45dB:start_silence=0.025,areverse,silenceremove=start_periods=1:start_duration=0.015:start_threshold=-45dB:start_silence=0.08,areverse,highpass=f=65,loudnorm=I='+str(level)+':TP=-3:LRA=12,afade=t=in:d=0.005'
   subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-i',str(raw),'-af',filters,'-ar','48000','-ac','1','-c:a','pcm_s24le',str(out)],check=True)
  info=sf.info(out);assert .1<info.duration<10,(slug,info.duration)
  records.append(dict(id=slug,character=person,text=words,direction=direction,path=str(out.relative_to(ROOT)),duration=info.duration,frames=info.frames,sample_rate=info.samplerate,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),review='pending combined animatic'))
  print('VOICE_READY',slug,round(info.duration,3),flush=True)
 (OUT/'takes.json').write_text(json.dumps(records,indent=2)+'\n')
 print('COMPLETE',len(records),flush=True)
if __name__=='__main__':main()
