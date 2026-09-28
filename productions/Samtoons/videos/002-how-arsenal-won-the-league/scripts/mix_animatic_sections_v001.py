"""Use shared mixer section-by-section; verify exact float WavPack before removing temporary WAVs."""
from pathlib import Path
import json,subprocess,sys,hashlib
V=Path(__file__).resolve().parents[1];ROOT=V.parents[3];O=V/'artifacts/animatic-v001';P=json.loads((O/'audio-plan.json').read_text());E=json.loads((O/'edit.json').read_text());FF='/opt/homebrew/bin/ffmpeg'
def run(a):
 p=subprocess.run([str(x) for x in a],capture_output=True)
 if p.returncode:raise RuntimeError(p.stderr.decode()[-1500:])
 return p.stdout
parts=[];evidence=[]
for i in range(0,len(E),7):
 rows=E[i:i+7];lo=rows[0]['start_frame'];frames=sum(x['frames'] for x in rows);ids={x['id'] for x in rows};tag=f'section-{i//7:02}'+('-cuesv3' if i//7 in [0,1,3,4,5,6] else '-scorev2' if i//7==2 else '')
 plan=json.loads(json.dumps(P));plan['timeline']['frames']=frames
 plan['shots']=[{**x,'start_frame':x['start_frame']-lo+1} for x in P['shots'] if x['id'] in ids];plan['cues']=[x for x in P['cues'] if x['shot'] in ids]
 path=O/(tag+'.json');path.write_text(json.dumps(plan,indent=2));out=O/tag
 if not (out/'checks.json').exists():run([sys.executable,ROOT/'pipeline/audio.py','build',path,'--out',out])
 for wav in [*(out/'stems').glob('*.wav'),out/'mix-premaster.wav']:
  wv=wav.with_suffix('.wv')
  if not wav.exists():continue
  run([FF,'-v','error','-y','-i',wav,'-c:a','wavpack','-sample_fmt','fltp',wv])
  a=run([FF,'-v','error','-i',wav,'-f','f32le','-']);b=run([FF,'-v','error','-i',wv,'-f','f32le','-']);assert a==b,'Lossless roundtrip failed'
  evidence.append(dict(original=str(wav.relative_to(O)),retained=str(wv.relative_to(O)),decoded_pcm_sha256=hashlib.sha256(b).hexdigest(),exact_float_roundtrip=True));wav.unlink()
 parts.append(out/'mix-premaster.wv');print(tag,frames/24,'seconds mixed',flush=True)
(O/'float-compression-checks.json').write_text(json.dumps(evidence,indent=2))
(O/'audio-concat.txt').write_text(''.join("file '"+str(p)+"'\n" for p in parts))
run([FF,'-v','error','-y','-f','concat','-safe','0','-i',O/'audio-concat.txt','-c:a','pcm_f32le',O/'mix-premaster.wav'])
print('Full authoritative float master ready.',flush=True)
