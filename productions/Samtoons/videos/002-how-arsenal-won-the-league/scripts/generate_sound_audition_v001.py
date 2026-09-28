"""Bounded local acting audition; caches raw takes, no full-film voice casting implied."""
from pathlib import Path
import sys,json,time,hashlib
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'pipeline'))
import qwen_voice as q
OUT=Path(__file__).resolve().parents[1]/'artifacts/sound-direction-v001'
base='An elderly man, low weathered gravelly voice, restrained Scottish English accent. Original theatrical cartoon football manager voice. Close dry microphone, no music. '
takes=[
('narrator','Relax. It’s Arsenal. We all know how this ends.',base+'Quietly reassure yourself with absolute smug certainty. Small pause after Relax. Underplay Arsenal, then dry dismissive finality on ends. Do not shout.',42),
('arteta','He’s only walking. We’re fine. WHY IS HE WALKING?', 'Adult man with a bright tight mid-register voice and light Spanish English accent. A comic manager running in fear. First sentence breathless self-reassurance, second forced confidence. Pause, then break into a desperate projected shout on WHY, with genuine panic and breath effort. Clean dry voice only.',43),
('pep','Long season, Mikel.', 'Middle-aged man with a low soft resonant voice, light Catalan Spanish accent speaking clear English. Completely relaxed and unhurried, almost kindly. A tiny knowing smile; let Mikel fall quietly. No threat, no shout, no laugh. Dry close microphone.',44),
('hold','For a penalty against Arsenal, please hold. Your call is very important to us.', 'Adult female telephone customer-service voice. Bright polished British English. An absurdly cheerful automatic announcement, oblivious to the callers despair. Smiling clear diction, measured artificial courtesy. Clean dry speech without telephone filtering or music.',45),
('ref','Hello? I’m still here.', 'Adult British male football referee, mid-register voice. First Hello is a small hopeful question. Then hurt disbelief and embarrassed frustration, stressing STILL. He is being ignored, not addressing a crowd. Clean dry microphone.',46),
('meltdown','I SAID I WAS RETIRED! STOP GIVING ME REASONS TO COME BACK!',base+'Explode in full-throated furious comic outrage toward a television. Strong breath pressure, cracked raspy attack. Stress RETIRED. Ragged inhalation between sentences, then desperate appeal to the ceiling, stressing STOP and COME BACK. Same elderly character now losing all control. This must be acted yelling, not a calm reading.',42)
]
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'performance-directions.json').write_text(json.dumps(takes,indent=2))
model=q.load_model(str(q.RUNTIME/'model'))
for name,text,direction,seed in takes:
    path=OUT/(name+'-raw.wav')
    if path.exists() and path.with_suffix('.json').exists():continue
    if path.exists():raise RuntimeError('Unrecorded existing take: '+str(path))
    q.mx.random.seed(seed); start=time.monotonic()
    chunks=list(model.generate_voice_design(text=text,language='English',instruct=direction,max_tokens=512))
    assert chunks
    sr=chunks[0].sample_rate; data=q.np.concatenate([q.np.asarray(c.audio).reshape(-1) for c in chunks])
    assert q.np.isfinite(data).all() and len(data)>sr*.2 and .001<float(q.np.max(q.np.abs(data)))<=1.01
    q.sf.write(path,data,sr,subtype='PCM_24')
    info=dict(text=text,direction=direction,seed=seed,sample_rate=sr,duration=len(data)/sr,seconds=time.monotonic()-start,heard_by_agent=False,model_source=json.loads((q.RUNTIME/'model-source.json').read_text()),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    path.with_suffix('.json').write_text(json.dumps(info,indent=2))
    print(name,round(len(data)/sr,2),'seconds generated',flush=True)
