"""Finish the authoritative review mix, encode the movie and verify the exact export."""
from pathlib import Path
import json,subprocess,hashlib,time,sys,shutil
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/animatic-v001';FF='/opt/homebrew/bin/ffmpeg';FP='/opt/homebrew/bin/ffprobe'
if '--repair-v002' in sys.argv:OUT=ROOT/'artifacts/animatic-v002'
if '--revision-v003' in sys.argv:OUT=ROOT/'artifacts/animatic-v003'
if '--revision-v004' in sys.argv:OUT=ROOT/'artifacts/animatic-v004'
FINAL='--final-v001' in sys.argv
if FINAL:OUT=ROOT/'artifacts/delivery-v001'
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True)
def assemble():
 deadline=time.monotonic()+900
 while 'ENDING_COMPLETE' not in (OUT/'render-tail.log').read_text():
  if time.monotonic()>deadline:raise TimeoutError('Corrected tail did not finish within fifteen minutes.')
  time.sleep(2)
 edit=json.loads((OUT/'edit.json').read_text());records=[];lines=[]
 for i,row in enumerate(edit):
  folder='picture-selected' if i<13 else 'tail-selected';path=OUT/folder/f'picture-{i:02}.mp4'
  probe=json.loads(run([FP,'-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate,width,height','-of','json',str(path)]).stdout)['streams'][0]
  assert int(probe['nb_frames'])==row['frames'] and probe['r_frame_rate']=='24/1' and probe['width']==960
  records.append(dict(scene=row['scene'],path=str(path.relative_to(OUT)),frames=row['frames'],sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
  lines.append("file '"+str(path.relative_to(OUT))+"'\n")
 (OUT/'concat-selected.txt').write_text(''.join(lines))
 if not (OUT/'picture-selected.mp4').exists():run([FF,'-v','error','-f','concat','-safe','0','-i',str(OUT/'concat-selected.txt'),'-c','copy','-movflags','+faststart',str(OUT/'picture-selected.mp4')])
 for p in OUT.glob('repair-frame-*.png'):shutil.copy2(p,OUT/p.name.removeprefix('repair-'))
 (OUT/'render-checks.json').write_text(json.dumps(dict(frames=sum(r['frames'] for r in records),fps=24,seconds=150,resolution=[1920,1080] if FINAL else [960,540],shots=records,native='combined-animatic-v006.blend',quality='Complete review animatic; not final delivery',selection='First thirteen complete clips plus independently rebuilt final three; isolated scratch paths'),indent=2)+'\n')
 print('ASSEMBLED',flush=True)

def main():
 frames=sum(r['frames'] for r in json.loads((OUT/'edit.json').read_text()));seconds=frames/24
 if '--assemble' in sys.argv:assemble()
 mix=OUT/'mix/mix-premaster.wav';wav=OUT/'mix-review.wav'
 if not wav.exists():
  scan=run([FF,'-hide_banner','-i',str(mix),'-af','loudnorm=I=-19:TP=-2:LRA=12:print_format=json','-f','null','-']).stderr
  measured=json.loads(scan[scan.rfind('{'):scan.rfind('}')+1]);f='loudnorm=I=-19:TP=-2:LRA=12:linear=true:'+':'.join(k+'='+measured[v] for k,v in [('measured_I','input_i'),('measured_TP','input_tp'),('measured_LRA','input_lra'),('measured_thresh','input_thresh'),('offset','target_offset')])
  run([FF,'-v','error','-i',str(mix),'-af',f,'-ar','48000','-ac','2','-c:a','pcm_s24le',str(wav)])
  (OUT/'mix-finish.json').write_text(json.dumps(dict(target_lufs=-19,true_peak_limit=-2,measured=measured,filter=f,source_sha256=hashlib.sha256(mix.read_bytes()).hexdigest()),indent=2)+'\n')
 if not (OUT/'picture-selected.mp4').exists():print('MIX_READY; picture rendering');return
 movie=OUT/('samtoons-final-1080p.mp4' if FINAL else 'animatic.mp4')
 if not movie.exists():run([FF,'-v','error','-i',str(OUT/'picture-selected.mp4'),'-i',str(wav),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','320k' if FINAL else '192k','-movflags','+faststart',str(movie)])
 webm=OUT/('samtoons-final-1080p.webm' if FINAL else 'animatic.webm')
 if not webm.exists():run([FF,'-v','error','-i',str(movie),'-c:v','libvpx-vp9','-crf','24' if FINAL else '34','-b:v','0','-row-mt','1','-threads','4','-c:a','libopus','-b:a','128k',str(webm)])
 probe=json.loads(run([FP,'-v','error','-show_streams','-show_format','-of','json',str(movie)]).stdout)
 video=next(s for s in probe['streams'] if s['codec_type']=='video');audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
 assert video['r_frame_rate']=='24/1' and int(video['nb_frames'])==frames and video['width']==(1920 if FINAL else 960) and video['height']==(1080 if FINAL else 540)
 assert abs(float(probe['format']['duration'])-seconds)<.05 and audio['sample_rate']=='48000' and audio['channels']==2
 run([FF,'-v','error','-i',str(movie),'-f','null','-']);run([FF,'-v','error','-i',str(webm),'-f','null','-'])
 stats=run([FF,'-hide_banner','-i',str(movie),'-af','loudnorm=I=-19:TP=-2:LRA=12:print_format=json','-f','null','-']).stderr;stats=json.loads(stats[stats.rfind('{'):stats.rfind('}')+1]);assert float(stats['input_tp'])<=-.8
 checks=dict(frames=frames,seconds=seconds,fps=24,resolution=[1920,1080] if FINAL else [960,540],audio_sample_rate=48000,channels=2,full_decode='passed MP4 and WebM',encoded_loudness=stats,movie_sha256=hashlib.sha256(movie.read_bytes()).hexdigest(),listening='Combined mix awaits user review; cached performances retained',mouths='Jaw effort and pause synchronization; phoneme-level polish not claimed')
 (OUT/'export-checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks))
if __name__=='__main__':main()
