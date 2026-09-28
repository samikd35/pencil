"""Insert approved native1080 branding; original film is decoded, never Blender-rendered."""
import subprocess,json,re,hashlib
from pathlib import Path
V=Path(__file__).resolve().parents[1];O=V/'artifacts/delivery-v029';B=V/'artifacts/branding-v028';D=V/'artifacts/delivery-v027';F='/opt/homebrew/bin/ffmpeg';P='/opt/homebrew/bin/ffprobe'
def run(args):subprocess.run([str(x) for x in args],check=True)
for stem in ['intro','outro']:
 run([F,'-v','error','-y','-i',O/(stem+'-picture.mp4'),'-i',B/(stem+'-audio/mix-premaster.wav'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',O/(stem+'-1080p.mp4')])
# Concise stand-alone review, exactly 15 seconds.
(O/'branding-concat.txt').write_text("file 'intro-1080p.mp4'\nfile 'outro-1080p.mp4'\n")
run([F,'-v','error','-y','-f','concat','-safe','0','-i',O/'branding-concat.txt','-c','copy','-movflags','+faststart',O/'intro-outro-1080p.mp4'])
# 180 opening frames / 72 intro / remaining 6454 film frames / 288 outro.
flt='[0:v]split=2[a][b];[a]trim=start_frame=0:end_frame=180,setpts=PTS-STARTPTS,setsar=1[v0];[b]trim=start_frame=180:end_frame=6634,setpts=PTS-STARTPTS,setsar=1[v2];[1:v]setpts=PTS-STARTPTS,setsar=1[v1];[2:v]setpts=PTS-STARTPTS,setsar=1[v3];[v0][v1][v2][v3]concat=n=4:v=1:a=0[v];[0:a]asplit=2[c][d];[c]atrim=start_sample=0:end_sample=360000,asetpts=PTS-STARTPTS[a0];[d]atrim=start_sample=360000:end_sample=13268000,asetpts=PTS-STARTPTS[a2];[3:a]asetpts=PTS-STARTPTS[a1];[4:a]asetpts=PTS-STARTPTS[a3];[a0][a1][a2][a3]concat=n=4:v=0:a=1[a]'
run([F,'-v','error','-y','-i',D/'samtoons-final-1080p.mp4','-i',O/'intro-picture.mp4','-i',O/'outro-picture.mp4','-i',B/'intro-audio/mix-premaster.wav','-i',B/'outro-audio/mix-premaster.wav','-filter_complex',flt,'-map','[v]','-map','[a]','-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','192k','-movflags','+faststart',O/'samtoons-final-1080p.mp4'])
# Shift external captions without changing a single existing word.
def ms(t):h,m,s,ms=map(int,re.split('[:,]',t));return ((h*60+m)*60+s)*1000+ms
def stamp(n):h,n=divmod(n,3600000);m,n=divmod(n,60000);s,n=divmod(n,1000);return f'{h:02}:{m:02}:{s:02},{n:03}'
subs=[]
for block in (D/'samtoons-final.srt').read_text().strip().split('\n\n'):
 lines=block.splitlines();a,b=lines[1].split(' --> ');a,b=ms(a),ms(b);assert not(a<7500<b),'Caption crosses insertion'
 if a>=7500:a+=3000;b+=3000
 subs.append((a,b,'\n'.join(lines[2:])))
subs.extend([(7500,10500,'[MUSIC: Samtoons signature]'),(279417,291417,'[MUSIC: Samtoons outro]')]);subs.sort()
(O/'samtoons-final.srt').write_text('\n\n'.join(f'{i}\n{stamp(a)} --> {stamp(b)}\n{t}' for i,(a,b,t) in enumerate(subs,1))+'\n')
checks={}
for name,nframes in [('intro-1080p.mp4',72),('outro-1080p.mp4',288),('samtoons-final-1080p.mp4',6994)]:
 p=O/name;data=json.loads(subprocess.check_output([P,'-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio');assert int(v['nb_frames'])==nframes;assert v['r_frame_rate']=='24/1';assert (v['width'],v['height'])==(1920,1080);assert abs(float(v['duration'])-float(a['duration']))<.06
 run([F,'-v','error','-i',p,'-f','null','-'])
 checks[name]={'frames':nframes,'dimensions':[1920,1080],'fps':24,'video_seconds':v['duration'],'audio_seconds':a['duration'],'decode':'passed','sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
checks['source_unchanged']=hashlib.sha256((D/'samtoons-final-1080p.mp4').read_bytes()).hexdigest()=='516025cbe42bd57a68a759d9caac6ee6d1d8f76357995b8aa0501af823b3b924';assert checks['source_unchanged'];checks['agent_listening']='not performed';checks['creative_review']='v028 accepted by user; new1080 export technically checked'
(O/'checks.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
