"""Check every held panel in the encoded edit and decode the actual mastered audio."""
import json
from pathlib import Path
import subprocess
import tempfile
import wave
import numpy as np
from PIL import Image

OUT=Path(__file__).resolve().parents[1]/'artifacts/animatic-v001'
story=json.loads((OUT/'story.json').read_text())
panels=story['panels']
video=OUT/'just-one-thing-animatic.mp4'
indices=[p['frame']-1+p['frames']//2 for p in panels]
selection='+'.join(f'eq(n\\,{n})' for n in indices)
errors=[]
with tempfile.TemporaryDirectory(prefix='animatic-review-') as tmp:
    subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-i',str(video),
        '-vf','select='+selection,'-fps_mode','vfr',str(Path(tmp)/'%03d.png')],check=True)
    decoded=sorted(Path(tmp).glob('*.png'))
    assert len(decoded)==len(panels)
    for p,path in zip(panels,decoded):
        source=np.asarray(Image.open(OUT/p['image']).convert('RGB'),dtype=np.float32)
        actual=np.asarray(Image.open(path).convert('RGB'),dtype=np.float32)
        error=float(np.abs(source-actual).mean())
        errors.append(error)
        assert error<3,(p['index'],error)
subprocess.run(['/opt/homebrew/bin/ffmpeg','-y','-v','error','-i',str(video),'-vn',
    '-c:a','pcm_s16le','-ar','24000',str(OUT/'review-mix.wav')],check=True)
with wave.open(str(OUT/'review-mix.wav'),'rb') as w:
    sr=w.getframerate();channels=w.getnchannels();count=w.getnframes()
    audio=np.frombuffer(w.readframes(count),dtype='<i2').astype(np.float32)/32768
assert channels==2 and abs(count/sr-180)<.1
assert .01<float(np.max(np.abs(audio)))<.9
(OUT/'delivery-checks.json').write_text(json.dumps({'status':'passed',
    'encoded_panels_checked':len(panels),'maximum_mean_pixel_error':max(errors),
    'decoded_audio_seconds':count/sr,'decoded_audio_peak':float(np.max(np.abs(audio))),
    'scope':'Each encoded panel midpoint matches its source within compression tolerance. Full decode and mastered audio peak/duration checks. No audience-comprehension claim.'},indent=2)+'\n')
print('Verified all 68 encoded panels and decoded mastered stereo soundtrack.')
