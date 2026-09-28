from pathlib import Path
import json,subprocess,hashlib,sys,textwrap
V=Path(__file__).resolve().parents[1];ROOT=V.parents[3];O=V/'artifacts/animatic-v001';FF='/opt/homebrew/bin/ffmpeg';E=json.loads((O/'edit.json').read_text());S=json.loads((O/'subtitles.json').read_text());total=sum(x['frames'] for x in E)
sys.path.insert(0,str(ROOT/'pipeline'));from checkpoints import require_checkpoint
require_checkpoint(V,'sound-direction-v001','sound');require_checkpoint(V,'chase-v002','staging')
def run(args):
 p=subprocess.run([str(x) for x in args],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-2500:])
 return p
(O/'picture-concat.txt').write_text(''.join("file '"+str(O/'clips'/(x['id']+'.mp4'))+"'\n" for x in E))
def ts(t):
 return f'{int(t//3600)}:{int(t//60)%60:02}:{t%60:05.2f}'
header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Dialogue,Arial,29,&H00FFFFFF,&H00FFFFFF,&H00181818,&H90000000,0,0,0,0,100,100,0,0,3,1,0,2,55,55,30,1
Style: Result,Arial,40,&H00FFFFFF,&H00FFFFFF,&H00202020,&H90000000,1,0,0,0,100,100,0,0,3,1,0,8,55,55,30,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
for row in S:header+=f'Dialogue: 0,{ts(row["start"])},{ts(row["end"])},Dialogue,,0,0,0,,'+r'\N'.join(textwrap.wrap(row['text'],67))+'\n'
for row in E:
 if row['id'] in ['CD05_ping','CP02_near']:
  start=(row['start_frame']-1)/24;header+=f'Dialogue: 1,{ts(start)},{ts(start+row["frames"]/24)},Result,,0,0,0,,CITY WIN\n'
(O/'captions.ass').write_text(header)
movie=O/'arsenal-animatic-v001.mp4';assert not movie.exists()
run([FF,'-v','error','-f','concat','-safe','0','-i',O/'picture-concat.txt','-i',O/'mix-premaster.wav','-vf',f'ass={O/"captions.ass"}','-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-frames:v',str(total),'-t',str(total/24),'-movflags','+faststart',movie])
run([FF,'-v','error','-xerror','-i',movie,'-f','null','-'])
meta=json.loads(run(['/opt/homebrew/bin/ffprobe','-v','error','-show_streams','-show_format','-of','json',movie]).stdout);video=next(s for s in meta['streams'] if s['codec_type']=='video');sound=next(s for s in meta['streams'] if s['codec_type']=='audio')
assert int(video['nb_frames'])==total and video['r_frame_rate']=='24/1';assert video['width']==1280 and video['height']==720;assert sound['channels']==2
measure=run([FF,'-hide_banner','-i',movie,'-af','loudnorm=print_format=json','-f','null','-']).stderr;level=json.JSONDecoder().raw_decode(measure[measure.rfind('{'):])[0];assert float(level['input_tp'])<-1
# Check all47script lines represented exactly, every cut contiguous and every movie complete.
assert sorted(n for r in E for n in r['lines'])==list(range(1,48))
assert all(E[i]['start_frame']+E[i]['frames']==E[i+1]['start_frame'] for i in range(len(E)-1))
checks=dict(duration_seconds=total/24,frames=total,fps='24',resolution=[1280,720],audio='48kHz stereo AAC192k',full_decode='passed',script_lines=47,shots=len(E),measured_loudness={k:v for k,v in level.items() if k.startswith('input_')},sha256=hashlib.sha256(movie.read_bytes()).hexdigest(),agent_listening=False,motion_quality='Storyboard exposures only, not full character animation')
(O/'encoding-checks.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks),flush=True)
# Visual contact sheet covers every cut and samples captions; compact evidence only.
run([FF,'-v','error','-y','-i',movie,'-vf','fps=1/5,scale=320:180,tile=5x11','-frames:v','1',O/'edit-contact.jpg'])
for name in ['CD03','CP01','VH01','FR05','N04_reveal']:
 r=next(x for x in E if x['id']==name);run([FF,'-v','error','-y','-ss',str((r['start_frame']+12)/24),'-i',movie,'-frames:v','1',O/(name+'-review.jpg')])
