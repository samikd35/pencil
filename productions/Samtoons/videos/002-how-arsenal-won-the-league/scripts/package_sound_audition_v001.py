"""Contextual still-board / existing-footage edit. Does not render new animation."""
from pathlib import Path
import json,subprocess,math
V=Path(__file__).resolve().parents[1];O=V/'artifacts/sound-direction-v001';T=json.loads((O/'timing.json').read_text());FF='/opt/homebrew/bin/ffmpeg'
def run(args):
    p=subprocess.run([str(a) for a in args],capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-2000:])
    return p
board=V/'artifacts/preproduction-v001/boards'
segments=[(board/'01-shadow.png',0,T['chase_start'],True),
(V/'artifacts/chase-v002/chase-v002.mp4',T['chase_start'],T['hold_start'],False),
(board/'06-hotline.png',T['hold_start'],T['reveal_start'],True),
(board/'01-shadow.png',T['reveal_start'],T['lamp'],True),
(V/'artifacts/ferguson-design-v001/reveal-proposal.png',T['lamp'],T['end'],True)]
# Frame boundaries are rounded once, so concatenation cannot accumulate duration error.
frames=[]
for i,(source,start,end,still) in enumerate(segments):
    n=round(end*24)-round(start*24);frames.append(n)
    args=[FF,'-v','error','-y']+(['-loop','1','-framerate','24'] if still else [])+['-i',source,'-an','-vf','scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps=24','-frames:v',n,'-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p',O/f'picture-{i}.mp4']
    run(args)
assert sum(frames)==round(T['end']*24)
(O/'concat.txt').write_text(''.join("file 'picture-%d.mp4'\n"%i for i in range(len(segments))))
run([FF,'-v','error','-y','-f','concat','-safe','0','-i',O/'concat.txt','-c','copy',O/'picture.mp4'])
def stamp(t):
    h=int(t//3600);m=int(t//60)%60;s=t%60;return f'{h}:{m:02}:{s:05.2f}'
header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Dialogue,Arial,29,&H00FFFFFF,&H00FFFFFF,&H00181818,&H90000000,0,0,0,0,100,100,0,0,3,1,0,2,55,55,30,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
lines=[(2,T['narr_end'],'Relax. It’s Arsenal. We all know how this ends.'),
(T['chase_start']+.5,T['pep_start']-.3,'He’s only walking. We’re fine. WHY IS HE WALKING?'),
(T['pep_start'],T['hold_start']-.4,'Long season, Mikel.'),
(T['hold_start']+.5,T['ref_start']-.3,'For a penalty against Arsenal, please hold.\\NYour call is very important to us.'),
(T['ref_start'],T['reveal_start']-.6,'Hello? I’m still here.'),
(T['shout'],T['end']-1.4,'I SAID I WAS RETIRED!\\NSTOP GIVING ME REASONS TO COME BACK!')]
(O/'captions.ass').write_text(header+''.join(f'Dialogue: 0,{stamp(a)},{stamp(b)},Dialogue,,0,0,0,,{s}\n' for a,b,s in lines))
checks={}
for variant in ['A','B']:
    path=O/f'audition-{variant}.mp4'
    run([FF,'-v','error','-y','-i',O/'picture.mp4','-i',O/f'audition-{variant}.wav','-vf',f"ass={O/'captions.ass'}",'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-t',str(T['end']),path])
    run([FF,'-v','error','-i',path,'-f','null','-'])
    p=run(['/opt/homebrew/bin/ffprobe','-v','error','-show_streams','-show_format','-of','json',path]); info=json.loads(p.stdout)
    assert info['streams'][0]['nb_frames']==str(sum(frames))
    assert info['streams'][1]['codec_type']=='audio'
    measure=run([FF,'-hide_banner','-i',path,'-af','loudnorm=I=-18:TP=-1:LRA=11:print_format=json','-f','null','-']).stderr
    level=json.JSONDecoder().raw_decode(measure[measure.rfind('{'):])[0];checks[variant]=dict(duration=info['format']['duration'],frames=sum(frames),decode='passed',loudness=level)
    assert float(level['input_tp'])<-1
assert abs(float(checks['A']['loudness']['input_i'])-float(checks['B']['loudness']['input_i']))<1
(O/'encoding-checks.json').write_text(json.dumps(checks,indent=2))
run([FF,'-v','error','-y','-ss',str(T['lamp']+.5),'-i',O/'audition-A.mp4','-frames:v','1',O/'review-frame.jpg'])
print(json.dumps(checks),flush=True)
