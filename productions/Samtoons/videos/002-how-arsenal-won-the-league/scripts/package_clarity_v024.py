"""Assemble and check the actual batch encode and cumulative review."""
import json,subprocess,hashlib
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/clarity-v024';FF='/opt/homebrew/bin/ffmpeg';FP='/opt/homebrew/bin/ffprobe';rows=json.loads((O/'edit.json').read_text())
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True)
def info(p):return json.loads(run([FP,'-v','error','-show_streams','-show_format','-of','json',str(p)]).stdout)
for r in rows:
 p=O/'clips'/(r['id']+'.mp4');i=info(p);v=next(s for s in i['streams'] if s['codec_type']=='video');assert int(v['nb_frames'])==r['frames'],(r['id'],v.get('nb_frames'),r['frames'])
(O/'picture-list.txt').write_text(''.join("file '"+str(O/'clips'/(r['id']+'.mp4'))+"'\n" for r in rows))
run([FF,'-v','error','-y','-f','concat','-safe','0','-i',str(O/'picture-list.txt'),'-c','copy',str(O/'picture.mp4')])
# Match the approved prefix's finishing target without changing performance timing.
measurement=run([FF,'-hide_banner','-i',str(O/'mix/mix-premaster.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']).stderr;a=measurement.rfind('{');stats=json.JSONDecoder().raw_decode(measurement[a:])[0];af='loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}:linear=true'.format(**stats)
out=O/'final-batch-review-v024.mp4';run([FF,'-v','error','-y','-i',str(O/'picture.mp4'),'-i',str(O/'mix/mix-premaster.wav'),'-vf','ass='+str(O/'subtitles.ass'),'-af',af,'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-t',str(sum(r['frames'] for r in rows)/24),str(out)])
prefix=V/'artifacts/defence-v022/opening-through-defence-v022.mp4';(O/'combined-list.txt').write_text("file '"+str(prefix)+"'\nfile '"+str(out)+"'\n")
combined=O/'samtoons-complete-review-v024.mp4';run([FF,'-v','error','-y','-f','concat','-safe','0','-i',str(O/'combined-list.txt'),'-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(combined)])
checks=[]
for p,n in [(out,sum(r['frames'] for r in rows)),(combined,2992+sum(r['frames'] for r in rows))]:
 i=info(p);v=next(s for s in i['streams'] if s['codec_type']=='video');au=next(s for s in i['streams'] if s['codec_type']=='audio');assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1280,720,'24/1',n);assert int(au['sample_rate'])==48000 and au['channels']==2
 run([FF,'-v','error','-i',str(p),'-f','null','-']);checks.append(dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),frames=n,video_seconds=float(v['duration']),audio_seconds=float(au['duration']),resolution=[1280,720],fps=24,decoded=True))
(O/'encode-checks.json').write_text(json.dumps(dict(outputs=checks,premaster_loudness=stats,listening='Not performed by agent; user playback review pending',visual_review='See README for exact inspected frames and limits'),indent=2));print(json.dumps(checks,indent=2))

# External complete speaker subtitles use the same exact frame offsets as the picture.
import re
def parse_time(t):
 h,m,s,ms=map(int,re.split('[:,]',t));return ((h*60+m)*60+s)*1000+ms
def format_time(t):
 h,t=divmod(round(t),3600000);m,t=divmod(t,60000);s,ms=divmod(t,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
blocks=[]
for path,offset in [(V/'artifacts/dialogue-v018/subtitles.srt',0),(V/'artifacts/defence-v022/subtitles.srt',1669*1000/24),(O/'subtitles.srt',2992*1000/24)]:
 for block in path.read_text().strip().split('\n\n'):
  lines=block.splitlines();start,end=lines[1].split(' --> ');blocks.append(f'{len(blocks)+1}\n{format_time(parse_time(start)+offset)} --> {format_time(parse_time(end)+offset)}\n'+ '\n'.join(lines[2:]))
(O/'samtoons-complete-review-v024.srt').write_text('\n\n'.join(blocks)+'\n')
assert sum(1 for x in blocks if 'FERGUSON:' in x)==2
