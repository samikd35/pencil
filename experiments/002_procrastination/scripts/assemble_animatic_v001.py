"""Assemble the authored panels with original synthesized music and Foley."""
import json
import math
from pathlib import Path
import subprocess
import wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/animatic-v001'
STORY=json.loads((OUT/'story.json').read_text())
PANELS=STORY['panels']
SR=24000
DURATION=STORY['frames']/STORY['fps']
N=round(DURATION*SR)
rng=np.random.default_rng(917)
music=np.zeros((N,2),dtype=np.float32)
foley=np.zeros_like(music)
cues=[]

def add(dest,when,signal,gain=.1,pan=0):
    start=round(when*SR)
    if start>=N:return
    signal=signal[:N-start]*gain
    theta=(max(-1,min(1,pan))+1)*math.pi/4
    dest[start:start+len(signal),0]+=signal*math.cos(theta)
    dest[start:start+len(signal),1]+=signal*math.sin(theta)

def pluck(midi,duration=.6):
    t=np.arange(round(duration*SR))/SR
    f=440*2**((midi-69)/12)
    x=(np.sin(2*np.pi*f*t)+.27*np.sin(2*np.pi*2*f*t)+.10*np.sin(2*np.pi*3*f*t))*np.exp(-t*7)
    return x*np.minimum(t/.006,1)*np.minimum((duration-t)/.035,1)

def effect(kind):
    duration={'step':.17,'tap':.12,'lift':.40,'pop':.20,'tick':.09,'thud':.32,
              'scribble':.70,'paper':.27,'unroll':.85,'pin':.12,'click':.15}[kind]
    t=np.arange(round(duration*SR))/SR
    noise=rng.normal(0,1,len(t))
    if kind in ('step','tap','tick','thud','pin','click'):
        f={'step':130,'tap':380,'tick':1350,'thud':75,'pin':750,'click':520}[kind]
        x=(.72*np.sin(2*np.pi*f*t)+.20*noise)*np.exp(-t*38)
    elif kind=='pop':
        x=np.sin(2*np.pi*(620*t-850*t*t))*np.exp(-t*18)
    elif kind=='lift':
        x=.6*np.sin(2*np.pi*(230*t+250*t*t))*np.sin(np.pi*t/duration)**2
    else:
        smooth=np.convolve(noise,np.ones(5)/5,mode='same')
        x=(noise-smooth)*np.sin(np.pi*t/duration)
        if kind=='scribble':x*=.25+.75*np.sin(2*np.pi*5*t)**2
        if kind=='unroll':x=.6*x+.2*np.sin(2*np.pi*110*t)
    x*=np.minimum(t/.005,1)*np.minimum((duration-t)/.02,1)
    return x/max(np.max(np.abs(x)),1e-9)

# A small original plucked motif gathers complexity with the preparations.
# It falls silent for the realization and resolves when the picture is hung.
quiet=next(p['start_seconds'] for p in PANELS if p['beat']=='A quiet realization')
action=next(p['start_seconds'] for p in PANELS if p['beat']=='Just do the thing')
ending=next(p['start_seconds'] for p in PANELS if p['beat']=='Done')
for start in np.arange(.65,quiet-1,6.0):
    phase=0 if start<40.8 else 1 if start<72.2 else 2
    notes=[60,64,67,64] if phase==0 else [60,64,67,71,67,64] if phase==1 else [60,64,67,71,74,71,67,64]
    spacing=[.50,.39,.27][phase]
    for j,note in enumerate(notes):
        add(music,float(start+j*spacing),pluck(note),.052,math.sin(j)*.25)
    add(music,float(start),pluck(36,1.0),.045,-.1)
for start in np.arange(action+.5,ending,6.5):
    for j,note in enumerate([60,64,67]):add(music,float(start+j*.65),pluck(note,.8),.045)
for j,note in enumerate([60,64,67,72]):
    add(music,ending+.3+j*.6,pluck(note,1.1),.062,j*.12-.18)
for note in (48,60,64,67):add(music,176,pluck(note,2),.035)
for p in PANELS:
    if p['cue']:
        when=p['start_seconds']+.08
        gain=.15 if p['cue'] in ('thud','step','click') else .095
        add(foley,when,effect(p['cue']),gain,max(-.7,min(.7,p['x']/7)))
        cues.append({'seconds':when,'kind':p['cue'],'panel':p['index']})
    if p['beat']=='The system takes over':
        for t in np.arange(p['start_seconds']+.6,p['start_seconds']+p['seconds'],1):
            add(foley,float(t),effect('tick'),.023,-.6)
mix=music+foley
assert np.isfinite(mix).all() and len(mix)==4320000
peak=float(np.max(np.abs(mix)))
assert 0<peak<1,peak
with wave.open(str(OUT/'soundtrack.wav'),'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
    w.writeframes(np.round(mix*32767).astype('<i2').tobytes())
(OUT/'audio-report.json').write_text(json.dumps({'seconds':DURATION,'sample_rate':SR,
    'samples':N,'peak_before_master':peak,'origin':'Original deterministic oscillator/noise synthesis; no recordings, narration, voice model or third-party music.',
    'seed':917,'quiet_section':[quiet,action],'foley_cues':cues},indent=2)+'\n')

manifest=['ffconcat version 1.0']
for p in PANELS:
    path=OUT/p['image']
    assert path.is_file(),path
    with Image.open(path) as im:assert im.size==(1280,720)
    manifest.extend([f"file '{path.as_posix()}'",'option framerate 24',f"duration {p['frames']/24:.9f}"])
manifest.extend([f"file '{(OUT/PANELS[-1]['image']).as_posix()}'",'option framerate 24'])
(OUT/'edit.ffconcat').write_text('\n'.join(manifest)+'\n')
cmd=['/opt/homebrew/bin/ffmpeg','-y','-v','warning','-safe','0','-i',str(OUT/'edit.ffconcat'),
     '-i',str(OUT/'soundtrack.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast',
     '-crf','20','-pix_fmt','yuv420p','-vf','fps=24,trim=end_frame=4320,setpts=N/(24*TB)','-t','180',
     '-af','loudnorm=I=-20:TP=-2:LRA=8','-c:a','aac','-b:a','160k','-ar','48000',
     '-movflags','+faststart',str(OUT/'just-one-thing-animatic.mp4')]
subprocess.run(cmd,check=True)
probe=json.loads(subprocess.check_output(['/opt/homebrew/bin/ffprobe','-v','error','-show_format','-show_streams','-of','json',str(OUT/'just-one-thing-animatic.mp4')]))
video=next(s for s in probe['streams'] if s['codec_type']=='video')
audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert int(video['nb_frames'])==4320 and video['width']==1280 and video['height']==720
assert abs(float(video['duration'])-180)<.001 and abs(float(audio['duration'])-180)<.1
assert audio['channels']==2
(OUT/'video-checks.json').write_text(json.dumps({'status':'passed','duration_seconds':float(video['duration']),
    'frames':int(video['nb_frames']),'resolution':[video['width'],video['height']],
    'fps':video['avg_frame_rate'],'audio_channels':audio['channels'],'panel_count':len(PANELS),
    'bytes':int(probe['format']['size']),'scope':'Encoded video timing, frame count, dimensions, stereo audio and panel presence.'},indent=2)+'\n')

try:font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',17)
except OSError:font=ImageFont.load_default()
for page in range(math.ceil(len(PANELS)/16)):
    subset=PANELS[page*16:(page+1)*16]
    sheet=Image.new('RGB',(1280,824),'#e8dfd0');draw=ImageDraw.Draw(sheet)
    for j,p in enumerate(subset):
        im=Image.open(OUT/p['image']).resize((320,180))
        x=j%4*320;y=j//4*206;sheet.paste(im,(x,y))
        t=p['start_seconds']
        draw.text((x+7,y+183),f"{p['index']:02} / {int(t)//60:02}:{int(t)%60:02} / {p['pose']}",fill='#25394c',font=font)
    sheet.save(OUT/f'contact-sheet-{page+1:02}.jpg',quality=90)
print(json.dumps({'video':str(OUT/'just-one-thing-animatic.mp4'),'panels':len(PANELS),'seconds':DURATION,'checks':'passed'}))
