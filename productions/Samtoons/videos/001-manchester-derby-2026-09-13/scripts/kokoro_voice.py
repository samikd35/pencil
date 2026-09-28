"""Generate a WAV with the existing local Kokoro runtime; no downloads or cloud calls."""
from pathlib import Path
import argparse,os,sys,json,time,hashlib,dataclasses
RUNTIME=Path('/Users/samikd/MyProjects/PyBlend/Episode 1/production/voice_runtime')
if Path(sys.prefix).resolve() != (RUNTIME/'.venv').resolve():
    python=RUNTIME/'.venv/bin/python'
    if not python.exists():raise SystemExit(f'Existing Kokoro runtime missing: {python}')
    os.execv(str(python),[str(python),str(Path(__file__).resolve()),*sys.argv[1:]])
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--text',required=True);p.add_argument('--out',required=True,type=Path)
    p.add_argument('--voice',default='bm_george');p.add_argument('--speed',type=float,default=1.)
    a=p.parse_args()
    if not a.text.strip() or len(a.text)>10000:p.error('Use 1–10000 characters per line.')
    if not .5<=a.speed<=2:p.error('Speed must be between 0.5 and 2.')
    if a.out.suffix.lower()!='.wav':p.error('Output must be a .wav file.')
    meta=a.out.with_suffix('.json')
    if a.out.exists() or meta.exists():p.error('Output exists; choose a new take name.')
    expected={'kokoro-v1.0.fp16.onnx':'f3a290d384fbb27966d462905c71a46cef9e5fd00516b40df32a0b4afe77ac96','voices-v1.0.bin':'bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d'}
    for name,digest in expected.items():
        with (RUNTIME/'models'/name).open('rb') as f:
            if hashlib.file_digest(f,'sha256').hexdigest()!=digest:raise RuntimeError(f'Model changed: {name}')
    started=time.monotonic();k=Kokoro(str(RUNTIME/'models/kokoro-v1.0.fp16.onnx'),str(RUNTIME/'models/voices-v1.0.bin'))
    if a.voice not in k.get_voices():p.error('Unknown voice; available: '+', '.join(k.get_voices()))
    audio,sr,timings=k.create_timed(a.text,voice=a.voice,speed=a.speed,lang='en-gb' if a.voice.startswith('b') else 'en-us',sentence_pause=.10,clause_pause=.12)
    duration=len(audio)/sr
    assert len(audio)>100 and np.isfinite(audio).all() and .001<float(np.max(np.abs(audio)))<1
    assert timings and all(0<=t.start<=t.end<=duration+.02 for t in timings)
    a.out.parent.mkdir(parents=True,exist_ok=True);sf.write(a.out,audio,sr,subtype='PCM_24')
    data={'text':a.text,'voice':a.voice,'speed':a.speed,'sample_rate':sr,'duration_seconds':duration,'load_and_generate_seconds':time.monotonic()-started,'runtime':str(RUNTIME),'model_sha256':expected,'phonemes':[dataclasses.asdict(t) for t in timings],'listening_review':'Not heard by assistant; technical smoke test only.'}
    meta.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k not in ('phonemes','model_sha256')}))
if __name__=='__main__':main()
