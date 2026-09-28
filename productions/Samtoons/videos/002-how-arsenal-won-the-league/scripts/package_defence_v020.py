"""Assemble and check the actual batch encode and cumulative review."""
import json,subprocess,hashlib
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/defence-v020';FF='/opt/homebrew/bin/ffmpeg';FP='/opt/homebrew/bin/ffprobe';rows=json.loads((O/'edit.json').read_text())
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True)
def info(p):return json.loads(run([FP,'-v','error','-show_streams','-show_format','-of','json',str(p)]).stdout)
for r in rows:
 p=O/'clips'/(r['id']+'.mp4');i=info(p);v=next(s for s in i['streams'] if s['codec_type']=='video');assert int(v['nb_frames'])==r['frames'],(r['id'],v.get('nb_frames'),r['frames'])
(O/'picture-list.txt').write_text(''.join("file '"+str(O/'clips'/(r['id']+'.mp4'))+"'\n" for r in rows))
run([FF,'-v','error','-y','-f','concat','-safe','0','-i',str(O/'picture-list.txt'),'-c','copy',str(O/'picture.mp4')])
# Match the approved prefix's finishing target without changing performance timing.
measurement=run([FF,'-hide_banner','-i',str(O/'mix/mix-premaster.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']).stderr;a=measurement.rfind('{');stats=json.JSONDecoder().raw_decode(measurement[a:])[0];af='loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}:linear=true'.format(**stats)
out=O/'batch02-review-v020.mp4';run([FF,'-v','error','-y','-i',str(O/'picture.mp4'),'-i',str(O/'mix/mix-premaster.wav'),'-vf','ass='+str(O/'subtitles.ass'),'-af',af,'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-t',str(1047/24),str(out)])
prefix=V/'artifacts/dialogue-v018/batches01-02-review-v018.mp4';(O/'combined-list.txt').write_text("file '"+str(prefix)+"'\nfile '"+str(out)+"'\n")
combined=O/'opening-through-defence-v020.mp4';run([FF,'-v','error','-y','-f','concat','-safe','0','-i',str(O/'combined-list.txt'),'-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(combined)])
checks=[]
for p,n in [(out,1047),(combined,2716)]:
 i=info(p);v=next(s for s in i['streams'] if s['codec_type']=='video');au=next(s for s in i['streams'] if s['codec_type']=='audio');assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1280,720,'24/1',n);assert int(au['sample_rate'])==48000 and au['channels']==2
 run([FF,'-v','error','-i',str(p),'-f','null','-']);checks.append(dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),frames=n,video_seconds=float(v['duration']),audio_seconds=float(au['duration']),resolution=[1280,720],fps=24,decoded=True))
(O/'encode-checks.json').write_text(json.dumps(dict(outputs=checks,premaster_loudness=stats,listening='Not performed by agent; user playback review pending',visual_review='See README for exact inspected frames and limits'),indent=2));print(json.dumps(checks,indent=2))
