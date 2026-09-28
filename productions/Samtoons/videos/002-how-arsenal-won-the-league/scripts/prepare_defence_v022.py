"""Selected voice conditioning, timing and scoped original sound design."""
from pathlib import Path
import json,subprocess,sys,hashlib,dataclasses,math
from fractions import Fraction
import numpy as np,soundfile as sf
from scipy.signal import butter,sosfilt
V=Path(__file__).resolve().parents[1];O=V/'artifacts/defence-v022';FF='/opt/homebrew/bin/ffmpeg';SR=48000
for k in ['L18b','L18c']:
 p=O/'voices'/f'{k}.wav';d=O/'voices'/f'{k}-mix.wav';subprocess.run([FF,'-v','error','-y','-i',str(p),'-af','highpass=f=65','-ar','48000','-ac','1','-c:a','pcm_s24le',str(d)],check=True)
 a,sr=sf.read(d);g=min(10**(-21/20)/max(np.sqrt(np.mean(a*a)),1e-9),.78/max(abs(a)));sf.write(d,a*g,sr,subtype='PCM_24')
from mlx_audio.stt import load
m=load('mlx-community/whisper-tiny-asr-fp16');words={}
for k in ['L18b','L18c']:
 r=m.generate(str(O/'voices'/f'{k}-mix.wav'),language='en',word_timestamps=True,temperature=0);words[k]=dataclasses.asdict(r);print(k,words[k].get('text'),flush=True)
(O/'word-analysis.json').write_text(json.dumps(words,indent=2))
