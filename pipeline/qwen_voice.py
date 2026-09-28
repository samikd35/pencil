"""Generate an explicitly directed local performance using the installed MLX Qwen model."""
from pathlib import Path
import argparse, os, sys, json, time, hashlib

RUNTIME = Path.home()/'Models/qwen-voice'
PYTHON = RUNTIME/'.venv/bin/python'
if Path(sys.prefix).resolve() != (RUNTIME/'.venv').resolve():
    if not PYTHON.exists(): raise SystemExit(f'Qwen runtime is missing at {RUNTIME}; see pipeline/qwen-voice/README.md')
    os.execv(str(PYTHON),[str(PYTHON),str(Path(__file__).resolve()),*sys.argv[1:]])

import mlx.core as mx
import numpy as np
import soundfile as sf
from mlx_audio.tts.utils import load_model


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--text',required=True);p.add_argument('--direction',default='')
    p.add_argument('--reference-wav',type=Path);p.add_argument('--reference-text',default='')
    p.add_argument('--out',required=True,type=Path);p.add_argument('--seed',type=int,default=42)
    a=p.parse_args()
    if not a.text.strip() or len(a.text)>200:p.error('Provide one line of 1–200 characters.')
    if a.reference_wav:
        if not a.reference_wav.is_file() or not a.reference_text.strip():p.error('Reference conditioning requires an existing WAV and its exact transcript.')
    elif a.reference_text or not a.direction.strip():p.error('Provide an acting direction, or a reference WAV and transcript.')
    if a.out.suffix.lower()!='.wav' or a.out.exists() or a.out.with_suffix('.json').exists():p.error('Use a new WAV path.')
    if not 0<=a.seed<2**32:p.error('Seed must be an unsigned 32-bit integer.')
    model_path=RUNTIME/('base-model' if a.reference_wav else 'model')
    if not (model_path/'model.safetensors').exists():p.error('Download the pinned model before generating.')
    mx.random.seed(a.seed)
    start=time.monotonic();model=load_model(str(model_path))
    loaded=time.monotonic()
    if a.reference_wav:
        chunks=list(model.generate(text=a.text,lang_code='English',ref_audio=str(a.reference_wav),ref_text=a.reference_text,temperature=.65,max_tokens=320))
    else:
        chunks=list(model.generate_voice_design(text=a.text,language='English',instruct=a.direction,max_tokens=256))
    if not chunks:raise RuntimeError('Model returned no audio.')
    sr=chunks[0].sample_rate
    assert all(c.sample_rate==sr for c in chunks)
    audio=np.concatenate([np.asarray(c.audio).reshape(-1) for c in chunks])
    assert len(audio)>sr*.1 and np.isfinite(audio).all() and .001<float(np.max(np.abs(audio)))<=1.01
    a.out.parent.mkdir(parents=True,exist_ok=True);sf.write(a.out,audio,sr,subtype='PCM_24')
    data=dict(text=a.text,direction=a.direction,seed=a.seed,sample_rate=sr,duration_seconds=len(audio)/sr,
              load_seconds=loaded-start,generation_seconds=time.monotonic()-loaded,peak_memory_bytes=mx.get_peak_memory(),
              model_source=json.loads((RUNTIME/('base-model-source.json' if a.reference_wav else 'model-source.json')).read_text()),sha256=hashlib.sha256(a.out.read_bytes()).hexdigest(),
              heard_by_agent=False,processing='Unprocessed local model output; no gain or pitch change')
    if a.reference_wav:
        data.update(reference_wav=str(a.reference_wav.resolve()),reference_text=a.reference_text,reference_sha256=hashlib.sha256(a.reference_wav.read_bytes()).hexdigest(),direction_applied=False)
    a.out.with_suffix('.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k not in ('model_source','direction')}),flush=True)


if __name__=='__main__':main()
