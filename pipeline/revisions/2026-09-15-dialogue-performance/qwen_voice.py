"""Generate an explicitly directed local performance using the installed MLX Qwen model."""
from pathlib import Path
import argparse, os, sys, json, time, hashlib

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT/'.runtime/qwen-voice'
PYTHON = RUNTIME/'.venv/bin/python'
if Path(sys.prefix).resolve() != (RUNTIME/'.venv').resolve():
    if not PYTHON.exists(): raise SystemExit('Qwen runtime is missing; see .runtime/qwen-voice/README.md')
    os.execv(str(PYTHON),[str(PYTHON),str(Path(__file__).resolve()),*sys.argv[1:]])

import mlx.core as mx
import numpy as np
import soundfile as sf
from mlx_audio.tts.utils import load_model


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--text',required=True);p.add_argument('--direction',required=True)
    p.add_argument('--out',required=True,type=Path);p.add_argument('--seed',type=int,default=42)
    a=p.parse_args()
    if not a.text.strip() or len(a.text)>200 or not a.direction.strip():p.error('Provide one line of 1–200 characters and its acting direction.')
    if a.out.suffix.lower()!='.wav' or a.out.exists() or a.out.with_suffix('.json').exists():p.error('Use a new WAV path.')
    if not 0<=a.seed<2**32:p.error('Seed must be an unsigned 32-bit integer.')
    model_path=RUNTIME/'model'
    if not (model_path/'model.safetensors').exists():p.error('Download the pinned model before generating.')
    mx.random.seed(a.seed)
    start=time.monotonic();model=load_model(str(model_path))
    loaded=time.monotonic()
    chunks=list(model.generate_voice_design(text=a.text,language='English',instruct=a.direction,max_tokens=256))
    if not chunks:raise RuntimeError('Model returned no audio.')
    sr=chunks[0].sample_rate
    assert all(c.sample_rate==sr for c in chunks)
    audio=np.concatenate([np.asarray(c.audio).reshape(-1) for c in chunks])
    assert len(audio)>sr*.1 and np.isfinite(audio).all() and .001<float(np.max(np.abs(audio)))<=1.01
    a.out.parent.mkdir(parents=True,exist_ok=True);sf.write(a.out,audio,sr,subtype='PCM_24')
    data=dict(text=a.text,direction=a.direction,seed=a.seed,sample_rate=sr,duration_seconds=len(audio)/sr,
              load_seconds=loaded-start,generation_seconds=time.monotonic()-loaded,peak_memory_bytes=mx.get_peak_memory(),
              model_source=json.loads((RUNTIME/'model-source.json').read_text()),sha256=hashlib.sha256(a.out.read_bytes()).hexdigest(),
              heard_by_agent=False,processing='Unprocessed local model output; no gain or pitch change')
    a.out.with_suffix('.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k not in ('model_source','direction')}),flush=True)


if __name__=='__main__':main()
