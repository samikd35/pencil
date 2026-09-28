"""Revised Bottle FC storyboard opening; reuse all later selected picture/audio."""
from pathlib import Path
import json,sys,math,subprocess,hashlib,textwrap
import numpy as np,soundfile as sf
from fractions import Fraction
V=Path(__file__).resolve().parents[1];R=V.parents[3];O=V/'artifacts/opening-v002';OLD=V/'artifacts/animatic-v001';FF='/opt/homebrew/bin/ffmpeg';SR=48000
sys.path.insert(0,str(R/'pipeline'));import audio

def run(args):
 p=subprocess.run([str(x) for x in args],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-3000:])
 return p

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
oldplan=json.loads((OLD/'audio-plan.json').read_text());oldedit=json.loads((OLD/'edit.json').read_text());oldsub=json.loads((OLD/'subtitles.json').read_text());takes={r['id']:r for r in json.loads((O/'voices/takes.json').read_text())}
assets={};cues=[];shots=[];edit=[];subs=[];cursor=1
for k in ['switch','question-motif','paper-handoff']:
 a=dict(oldplan['assets'][k]);a['path']=str((OLD/a['path']).resolve());assets[k]=a
for k,r in takes.items():
 src=O/'voices'/(k+'.wav');dst=O/'voices'/(k+'-mix.wav')
 run([FF,'-v','error','-y','-i',src,'-af','highpass=f=65','-ar',SR,'-ac',1,'-c:a','pcm_s24le',dst])
 a,sr=sf.read(dst);gain=min(10**(-21/20)/max(np.sqrt(np.mean(a*a)),1e-9),.78/max(abs(a)));sf.write(dst,a*gain,SR,subtype='PCM_24')
 assets[k]=dict(path=str(dst),sha256=sha(dst),source=r['source']+'; highpass65Hz and RMS level matching existing takes',license='Qwen model Apache-2.0; generated performance',attribution='')
# Original reversing alert: two soft beeps, stops before dialogue.
t=np.arange(int(SR*1.2))/SR;wave=np.zeros(len(t))
for start in [0,.65]:
 local=t-start;mask=(local>=0)&(local<.23);env=np.minimum(np.clip(local/.012,0,1),np.clip((.23-local)/.025,0,1));wave+=.11*np.sin(2*np.pi*850*local)*env*mask
sf.write(O/'reverse.wav',wave,SR,subtype='PCM_24');assets['reverse']=dict(path=str(O/'reverse.wav'),sha256=sha(O/'reverse.wav'),source='Original two-beep reversing alert synthesized for truck arrival; no engine bed',license='Original production sound',attribution='')
spec=[('N01',None,7.5,'B01',1.3),('OP01_banner',0,2.0,None,0),('OP01_year',1,4.2,'B02',.75),('OP02_truck',2,2.3,None,0),('OP02_arteta',3,2.5,'B03',.3),('OP02_driver',4,3.0,'B04',.25),('OP03_phone',5,3.0,'B05',.35)]
def cue(shot,key,at,stem='foley',gain=0,duration=None):
 cid=shot['id']+'_'+key;shot['events'][cid]=round(at*24);dur=float(Fraction(audio.probe(assets[key]['path'])['duration']));dur=min(dur,duration) if duration else dur
 cues.append(dict(id=cid,shot=shot['id'],event=cid,asset=key,stem=stem,intent={'reverse':'Announce bottle truck interruption','paper-handoff':'Small paper detail on changed banner year'}.get(key,key),duration_seconds=str(dur),gain_db=gain,fade_in_seconds=.005,fade_out_seconds=.04))
for name,panel,seconds,line,lead in spec:
 frames=math.ceil(max(seconds,lead+(takes[line]['duration'] if line else 0)+.5)*24);shot=dict(id=name,start_frame=cursor,events={});shots.append(shot)
 edit.append(dict(id=name,start_frame=cursor,frames=frames,panel=panel,source=str(O/'boards.png') if panel is not None else str(OLD/'clips/N01.mp4'),line=line))
 if line:
  cue(shot,line,lead,'dialogue');subs.append(dict(start=(cursor-1)/24+lead,end=(cursor-1)/24+lead+takes[line]['duration'],text=takes[line]['text']))
 if name=='N01':cue(shot,'switch',0);cue(shot,'question-motif',.15,'music',-2)
 if name=='OP01_year':cue(shot,'paper-handoff',.05,'foley',-15,.45)
 if name=='OP02_truck':cue(shot,'reverse',0,'plot-effects',-6)
 if name=='OP03_phone':cue(shot,'switch',frames/24-.15,'foley',-7,.12)
 cursor+=frames
introframes=cursor-1;shift=introframes-744
plan=dict(version=1,timeline=dict(fps='24',start_frame=1,frames=introframes,sample_rate=SR),shots=shots,assets=assets,cues=cues,mix_gain_db=oldplan['mix_gain_db'])
(O/'audio-plan.json').write_text(json.dumps(plan,indent=2))
if not (O/'mix/mix-premaster.wav').exists():run([sys.executable,R/'pipeline/audio.py','build',O/'audio-plan.json','--out',O/'mix'])
C=O/'clips';C.mkdir(exist_ok=True)
# Locate actual sheet dividers, not assumed equal panel heights.
meta=json.loads(run(['/opt/homebrew/bin/ffprobe','-v','error','-show_entries','stream=width,height','-of','json',O/'boards.png']).stdout)['streams'][0];W,H=meta['width'],meta['height']
b=subprocess.check_output([FF,'-v','error','-i',str(O/'boards.png'),'-f','rawvideo','-pix_fmt','gray','-frames:v','1','-']);im=np.frombuffer(b,np.uint8).reshape(H,W)
def divider(scores,expected):
 lo=round(expected)-85;hi=round(expected)+86;return lo+int(np.argmin(scores[lo:hi]))
xx=[0,divider(im.mean(axis=0),W/2),W];yy=[0,divider(im.mean(axis=1),H/3),divider(im.mean(axis=1),2*H/3),H]
for row in edit:
 dst=C/(row['id']+'.mp4');row['clip']=str(dst)
 if dst.exists():continue
 if row['panel'] is None:
  run([FF,'-v','error','-y','-i',row['source'],'-an','-frames:v',row['frames'],'-c:v','libx264','-preset','fast','-crf','20',dst])
 else:
  p=row['panel'];col=p%2;rr=p//2;x=xx[col]+5;y=yy[rr]+5;w=xx[col+1]-x-5;h=yy[rr+1]-y-5;row['crop']=[x,y,w,h]
  vf=f'crop={w}:{h}:{x}:{y},scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1'
  run([FF,'-v','error','-y','-loop','1','-framerate','24','-i',O/'boards.png','-vf',vf,'-an','-frames:v',row['frames'],'-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p',dst])
 print(row['id'],row['frames'],flush=True)
for row in oldedit[6:]:
 r=dict(row);r['start_frame']+=shift;r['clip']=str(OLD/'clips'/(r['id']+'.mp4'));edit.append(r)
for sub in oldsub:
 if sub['start']>=31:subs.append(dict(sub,start=sub['start']+shift/24,end=sub['end']+shift/24))
assert all(a['start_frame']+a['frames']==b['start_frame'] for a,b in zip(edit,edit[1:]));assert len(subs)==len(oldsub)-6+5
(O/'edit.json').write_text(json.dumps(edit,indent=2));(O/'subtitles.json').write_text(json.dumps(subs,indent=2))
# Preserve every sample after old opening: append selected original master from31s.
run([FF,'-v','error','-y','-i',O/'mix/mix-premaster.wav','-i',OLD/'mix-premaster.wav','-filter_complex','[1:a]atrim=start=31,asetpts=PTS-STARTPTS[tail];[0:a][tail]concat=n=2:v=0:a=1[out]','-map','[out]','-c:a','pcm_f32le',O/'mix-premaster.wav'])
# Preserve the native plan for full revised timeline too, with changed starts and asset paths.
fullplan=json.loads(json.dumps(oldplan));fullplan['shots']=[s for s in fullplan['shots'] if s['id'] in {r['id'] for r in oldedit[6:]}]
for sh in fullplan['shots']:sh['start_frame']+=shift
fullplan['shots']=shots+fullplan['shots'];fullplan['cues']=[c for c in fullplan['cues'] if c['shot'] in {r['id'] for r in oldedit[6:]}]+cues
for a in fullplan['assets'].values():a['path']=str((OLD/a['path']).resolve())
fullplan['assets'].update(assets);fullplan['timeline']['frames']=edit[-1]['start_frame']+edit[-1]['frames']-1
(O/'full-audio-plan.json').write_text(json.dumps(fullplan,indent=2))
def ts(t):return f'{int(t//3600)}:{int(t//60)%60:02}:{t%60:05.2f}'
header=(OLD/'captions.ass').read_text().split('[Events]')[0]+'[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
for s in subs:header+=f'Dialogue: 0,{ts(s["start"])},{ts(s["end"])},Dialogue,,0,0,0,,'+r'\N'.join(textwrap.wrap(s['text'],67))+'\n'
for r in edit:
 if r['id'] in ['CD05_ping','CP02_near']:
  st=(r['start_frame']-1)/24;header+=f'Dialogue: 1,{ts(st)},{ts(st+r["frames"]/24)},Result,,0,0,0,,CITY WIN\n'
(O/'captions.ass').write_text(header);(O/'concat.txt').write_text(''.join("file '"+r['clip']+"'\n" for r in edit))
movie=O/'arsenal-animatic-v002.mp4';total=fullplan['timeline']['frames']
if not movie.exists():run([FF,'-v','error','-f','concat','-safe','0','-i',O/'concat.txt','-i',O/'mix-premaster.wav','-vf',f'ass={O/"captions.ass"}','-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar',SR,'-frames:v',total,'-t',total/24,'-movflags','+faststart',movie])
end=next(r for r in edit if r['id']=='TR03_warning')['start_frame']-1
run([FF,'-v','error','-y','-i',movie,'-t',end/24,'-c:v','libx264','-preset','fast','-crf','19','-c:a','aac','-b:a','192k','-movflags','+faststart',O/'bottle-fc-opening-v002.mp4'])
run([FF,'-v','error','-xerror','-i',movie,'-f','null','-'])
probe=json.loads(run(['/opt/homebrew/bin/ffprobe','-v','error','-show_streams','-of','json',movie]).stdout);video=next(s for s in probe['streams'] if s['codec_type']=='video');assert int(video['nb_frames'])==total
level=run([FF,'-hide_banner','-i',movie,'-af','loudnorm=print_format=json','-f','null','-']).stderr;level=json.JSONDecoder().raw_decode(level[level.rfind('{'):])[0];assert float(level['input_tp'])<-1
checks=dict(frames=total,seconds=total/24,opening_seconds=end/24,replaced_opening_seconds=introframes/24,old_opening_seconds=31,timeline_shift_frames=shift,full_decode='passed',loudness=level,sha256=sha(movie),agent_listening=False,scope='Held storyboard drawings, revised sound; not finished body motion or lip-sync')
(O/'checks.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks),flush=True)
run([FF,'-v','error','-y','-i',O/'bottle-fc-opening-v002.mp4','-vf','fps=1/3,scale=384:216,tile=4x4','-frames:v','1',O/'contact.jpg'])
