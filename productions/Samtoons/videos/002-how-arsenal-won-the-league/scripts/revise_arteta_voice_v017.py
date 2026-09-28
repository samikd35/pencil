from pathlib import Path
import sys,json,hashlib,time
V=Path(__file__).resolve().parents[1];sys.path.insert(0,str(V.parents[3]/'pipeline'));import qwen_voice as q
O=V/'artifacts/batch02-v017/voices';model=q.load_model(str(q.RUNTIME/'model'))
identity='Adult male football manager, clear English with a light Spanish accent. Calm low-mid register, grounded chest resonance, measured authoritative delivery. Firm descending sentence endings. No whining, no falsetto, no excited squeak. Dry clean microphone.'
for key,text,acting in [('L07b','Meet our real striker.','Introduce your most trusted tactical weapon with absolute certainty. Stress REAL, short deliberate pause before striker.'),('L09','Win us a corner.','A short firm instruction to a subordinate. Understated, decisive. Stress CORNER.'),('L11','Now we are dangerous.','Quiet satisfaction. He believes the plan is working. Low composed confidence.'),('L10','Not the goal! Off him!','A firm projected correction across a football pitch. Clear commanding attack, stress NOT and HIM. Controlled urgency rather than hysteria.')]:
 p=O/(key+'.wav')
 if p.exists():continue
 q.mx.random.seed(43);start=time.monotonic();chunks=list(model.generate_voice_design(text=text,language='English',instruct=identity+' '+acting,max_tokens=256));a=q.np.concatenate([q.np.asarray(c.audio).reshape(-1) for c in chunks]);q.sf.write(p,a,chunks[0].sample_rate,subtype='PCM_24');p.with_suffix('.json').write_text(json.dumps({'text':text,'direction':identity+' '+acting,'seed':43,'seconds':len(a)/chunks[0].sample_rate,'heard_by_agent':False,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2));print(key,len(a)/chunks[0].sample_rate,time.monotonic()-start,flush=True)
