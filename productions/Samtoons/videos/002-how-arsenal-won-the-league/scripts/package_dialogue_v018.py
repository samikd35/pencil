from pathlib import Path
import json,subprocess
V=Path(__file__).resolve().parents[1];O=V/'artifacts/dialogue-v018';FF='/opt/homebrew/bin/ffmpeg';FP='/opt/homebrew/bin/ffprobe';rows=json.loads((O/'edit.json').read_text());total=sum(r['frames'] for r in rows)
for r in rows:
 p=O/'clips'/(r['id']+'.mp4');q=json.loads(subprocess.check_output([FP,'-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames','-of','json',str(p)]));assert int(q['streams'][0]['nb_read_frames'])==r['frames'],r['id']
(O/'concat.txt').write_text(''.join("file 'clips/"+r['id']+".mp4'\n" for r in rows))
out=O/'batches01-02-review-v018.mp4'
subprocess.run([FF,'-v','error','-y','-f','concat','-safe','0','-i',str(O/'concat.txt'),'-i',str(O/'mix/mix-premaster.wav'),'-vf',f'ass={O}/subtitles.ass','-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(out)],check=True)
probe=json.loads(subprocess.check_output([FP,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(out)]));video=next(s for s in probe['streams'] if s['codec_type']=='video');audio=next(s for s in probe['streams'] if s['codec_type']=='audio');assert int(video['nb_read_frames'])==total and video['avg_frame_rate']=='24/1';assert int(audio['sample_rate'])==48000 and audio['channels']==2
subprocess.run([FF,'-v','error','-i',str(out),'-f','null','-'],check=True)
checks=dict(frames=total,seconds=total/24,dimensions=[video['width'],video['height']],fps=video['avg_frame_rate'],audio_sample_rate=audio['sample_rate'],audio_channels=audio['channels'],full_decode='passed',subtitles='burned in, ASS and SRT provided',listening_by_agent=False,user_review='pending',motion_changes='speaking holds only; walk, kick, physical-action shots retained at original speed')
(O/'delivery-checks.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks))
# Real encoded frame samples, including captions and key story beats.
for name,seconds in [('title',2.0),('promise',13),('bottles',22),('driver',27.5),('phone',33),('flag',46),('corners',53),('training',58),('praise',66)]:
 subprocess.run([FF,'-v','error','-y','-ss',str(seconds),'-i',str(out),'-frames:v','1',str(O/'review-frames'/f'encoded-{name}.png')],check=True)
