from pathlib import Path
import sys,json,time,hashlib,re,shutil
V=Path(__file__).resolve().parents[1];ROOT=V.parents[3];O=V/'artifacts/animatic-v001';A=O/'voices';A.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT/'pipeline'));import qwen_voice as q
records=json.loads((V/'artifacts/preproduction-v001/timing/timing-report.json').read_text())['lines']
base={
'NARRATOR':('An elderly man, low weathered gravelly voice, restrained Scottish English accent. Original theatrical cartoon football manager voice.',42),
'FERGUSON':('An elderly man, low weathered gravelly voice, restrained Scottish English accent. Original theatrical cartoon football manager voice.',42),
'ARTETA':('Adult man with a bright tight mid-register voice and light Spanish English accent. Comic football manager, clear English.',43),
'PEP':('Middle-aged man with a low soft resonant voice, light Catalan Spanish accent speaking clear English. Completely relaxed and unhurried, almost kindly.',44),
'RECORDED VOICE':('Adult female telephone customer-service voice. Bright polished British English. An absurdly cheerful automatic announcement, oblivious to the callers despair.',45),
'REFEREE':('Adult British male football referee, mid-register voice.',46),
'GYÖKERES':('Young adult man with a warm mid-low baritone and light Swedish accent speaking clear English. Footballer bewildered by his manager. Dry, understated comic reactions.',47),
'COURIER':('Adult British man with a light nasal tenor, crisply cheerful delivery-driver manner. Smiling efficiency, oblivious to how insulting his words are.',48),
'OPERATOR':('Adult British man, smooth warm customer-service baritone. Unctuous professional courtesy, delighted to help his favourite customer.',49)}
acting={
'L01':'Quiet smug certainty. Pause after Relax; dry dismissive finality.',
'L02':'Dry matter-of-fact sarcasm, let runners-up land.',
'L04':'Incredulous objection, stress HAVEN’T.',
'L05':'Brisk cheerful punchline. Exactly. A beat, then Beat the rush.',
'L06':'Clipped determined instruction into the phone.',
'L08':'Genuine wounded confusion, stress WHY.',
'L09':'Entirely sincere tactical instruction, no irony.',
'L10':'Frantic projected warning across the training ground. Sharp urgent commands, stress NOT and OFF.',
'L11':'Delighted, self-satisfied certainty.',
'L13':'Loud decisive order interrupting celebration. Full projected voice on ONE NIL and EVERYBODY BACK.',
'L15':'Calling loudly across a whole pitch, baffled and exasperated; genuine vocal effort.',
'L16':'Call back firmly across the pitch, perfectly sincere.',
'L18':'A tiny shocked question, confidence suddenly gone.',
'L20':'Breathless forced reassurance to yourself while running.',
'L21':'Desperate projected shout through gasping effort. WHY explodes; panic, not conversation.',
'L23':'Urgent shouted directions while running, breath pressure.',
'L25':'Explosive irritated shouted interruption.',
'L26':'Shout as the podium slips, urgent warning.',
'L27':'Confident professional announcement before speaking into headset.',
'L29':'Suddenly delighted warmth for a privileged caller.',
'L30':'Casual quiet request into a shielded phone.',
'L31':'Eager service, like offering fries at a drive-through.',
'L32':'Calm efficient order, no concern.',
'L33':'Small hopeful Hello, then hurt disbelief; stress STILL.',
'L35':'Straining to contain irritation. Stress bloody corner, controlled bitter edge.',
'L36':'Hopeful frustrated appeal, stress FINALLY.',
'L37':'Curt instruction, utterly confident, no shouting.',
'L38':'Clinging desperately to hope, almost whispered.',
'L39':'Exasperated argument abruptly interrupted mid-word; do not complete striker.',
'L40':'Small incredulous question, stunned surprise.',
'L41':'Utterly sincere, smug tactical certainty.',
'L42':'Cheerful professional confusion. Short hesitation after So.',
'L43':'Dry dismissive correction.',
'L44':'Sudden bright hope after exhausting wait.',
'L45':'Polished cheerful automation, terrible news delivered pleasantly.',
'L46':'Full-throated furious comic outrage toward television. Strong breath pressure and cracked raspy attack, stress RETIRED.',
'L47':'Desperate full-throated appeal to ceiling. Outrage tips into helplessness, stress STOP and COME BACK.'}
# Cache exact accepted standalone takes when words match, without regenerating their performances.
accepted={'L01':'narrator','L22':'pep','L33':'ref'}
model=None
for row in records:
    name=row['id'];path=A/(name+'.wav');role=row['role_and_direction'].split(' —')[0].strip();identity,seed=base[role]
    direction=identity+' '+acting.get(name,'Natural clear character delivery; make the sentence a thought, not a reading.')+' Clean dry microphone, no music or extra words.'
    row.update(role=role,direction=direction,seed=seed,heard_by_agent=False,selected_for_final=False)
    if name in accepted:
        source=V/'artifacts/sound-direction-v001'/(accepted[name]+'.wav');shutil.copy2(source,path);row['source']='Accepted A standalone performance: '+str(source.relative_to(V))
    elif not path.exists():
        if model is None:model=q.load_model(str(q.RUNTIME/'model'))
        q.mx.random.seed(seed);start=time.monotonic();chunks=list(model.generate_voice_design(text=row['text'],language='English',instruct=direction,max_tokens=512))
        sr=chunks[0].sample_rate;a=q.np.concatenate([q.np.asarray(c.audio).reshape(-1) for c in chunks]);assert q.np.isfinite(a).all() and .001<float(q.np.max(abs(a)))<=1.01
        q.sf.write(path,a,sr,subtype='PCM_24');row['generation_seconds']=time.monotonic()-start
    info=q.sf.info(path);row.update(path=str(path.relative_to(V)),seconds=info.duration,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    path.with_suffix('.json').write_text(json.dumps(row,indent=2,ensure_ascii=False))
    print(name,role,round(info.duration,2),flush=True)
(A/'takes.json').write_text(json.dumps(records,indent=2,ensure_ascii=False));(A/'model-source.json').write_bytes((q.RUNTIME/'model-source.json').read_bytes())
