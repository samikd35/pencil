"""Finish and verify the two picture-identical sound auditions."""
from pathlib import Path
import subprocess,json,re,argparse
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--revision',default='voices-v001');p.add_argument('--variants',nargs='+',default=['1','2'])
args=p.parse_args()
if not re.fullmatch(r'voices-v\d{3}',args.revision) or not all(re.fullmatch(r'[a-z0-9-]+',v) for v in args.variants):p.error('Invalid revision or variant name')
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts'/args.revision;ff='/opt/homebrew/bin/ffmpeg';probe='/opt/homebrew/bin/ffprobe'
def run(cmd):return subprocess.run(cmd,capture_output=True,text=True,check=True)
def measure(path):
 r=run([ff,'-hide_banner','-i',str(path),'-vn','-af','loudnorm=I=-20:TP=-2:LRA=11:print_format=json','-f','null','-']);return json.loads(re.findall(r'\{[^{}]+\}',r.stderr)[-1])
report={}
for v in args.variants:
 src=OUT/f'mix-{v}/mix-premaster.wav';m=measure(src)
 filt=f'loudnorm=I=-20:TP=-2:LRA=11:measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true:print_format=json'
 wav=OUT/f'audition-{v}.wav';run([ff,'-v','error','-i',str(src),'-af',filt,'-ar','48000','-c:a','pcm_s24le',str(wav)])
 for ext,ac in [('mp4','aac'),('webm','libopus')]:
  video=ROOT/f'artifacts/staging-v008/action-review-v001.{ext}';target=OUT/f'audition-{v}.{ext}'
  run([ff,'-v','error','-i',str(video),'-i',str(wav),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a',ac,'-b:a','192k','-t','32',*(['-movflags','+faststart'] if ext=='mp4' else []),str(target)])
  run([ff,'-v','error','-i',str(target),'-f','null','-'])
  d=json.loads(run([probe,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(target)]).stdout);vs=next(s for s in d['streams'] if s['codec_type']=='video');a=next(s for s in d['streams'] if s['codec_type']=='audio')
  assert int(vs['nb_read_frames'])==768 and a['channels']==2 and a['sample_rate']=='48000' and abs(float(d['format']['duration'])-32)<.03
  level=measure(target);assert -22<float(level['input_i'])<-18 and float(level['input_tp'])<-1
  report[f'{v}-{ext}']={'frames':768,'duration_seconds':d['format']['duration'],'audio':'stereo 48kHz','full_decode':'passed','loudness':level}
  print(v,ext,level['input_i'],level['input_tp'],flush=True)
(OUT/'export-checks.json').write_text(json.dumps(report,indent=2)+'\n')
