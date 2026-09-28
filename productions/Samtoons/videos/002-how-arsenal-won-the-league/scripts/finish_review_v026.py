"""Scoped caption/league-table finishing; preserve selected voices and all animation timing."""
from pathlib import Path
import json, re, subprocess, textwrap, hashlib

V = Path(__file__).resolve().parents[1]
SOURCE = V / 'artifacts/clarity-v024'
PREVIOUS = V / 'artifacts/hand-repair-v025'
OUT = V / 'artifacts/delivery-review-v026'
FF = '/opt/homebrew/bin/ffmpeg'

def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True)

def seconds(value):
    h, m, s = value.split(':')
    return int(h)*3600 + int(m)*60 + float(s.replace(',', '.'))

def timestamp(t, srt=False):
    base = 1000 if srt else 100
    h, rest = divmod(round(t*base), 3600*base)
    m, rest = divmod(rest, 60*base)
    s, sub = divmod(rest, base)
    return f'{h:02}:{m:02}:{s:02},{sub:03}' if srt else f'{h}:{m:02}:{s:02}.{sub:02}'

# Authored phrase boundaries at the cached word-analysis pauses; no rewritten dialogue.
splits = {'C00': [(0,8),(3.18,17)], 'C19': [(0,5),(2.18,16)],
          'C30': [(0,7),(3.64,15)], 'C31': [(0,2),(1.61,12)],
          'C35': [(0,6),(2.73,15)], 'C46': [(0,5),(2.59,18),(7.13,25)]}
caps = {c['id']: c for c in json.loads((SOURCE/'captions.json').read_text())}
original = (SOURCE/'subtitles.ass').read_text()
header = original.split('[Events]')[0] + '[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
events = [line[10:].split(',',9) for line in original.splitlines() if line.startswith('Dialogue: ')]
for key, parts in splits.items():
    c = caps[key]
    events = [e for e in events if not (e[4] == c['speaker'] and c['start']-.02 <= seconds(e[1]) < c['end']-.02)]
    words = c['text'].split(); cursor = 0
    assert parts[-1][1] == len(words), (key, len(words))
    rebuilt = []
    for i, (offset, endword) in enumerate(parts):
        start = c['start'] + offset
        end = c['start'] + parts[i+1][0] if i+1 < len(parts) else c['end']
        phrase = ' '.join(words[cursor:endword]); rebuilt.extend(words[cursor:endword]); cursor = endword
        lines = textwrap.wrap(c['speaker']+': '+phrase,54)
        assert len(lines) <= 2 and end-start >= 1.0, (key, lines, end-start)
        text = '\\N'.join(lines).replace(c['speaker']+':', '{\\c&H84DBFF&}'+c['speaker']+':{\\c&HFFFFFF&}',1)
        events.append(['0',timestamp(start),timestamp(end),'Speech',c['speaker'],'0','0','0','',text])
    assert rebuilt == words

# The suspense caption ends when the reveal's final note begins.
reveal = next(seconds(e[1]) for e in events if e[3]=='Music' and 'The final note' in e[9])
for e in events:
    if e[3]=='Music' and 'The familiar two notes' in e[9]: e[2] = timestamp(reveal)
events.sort(key=lambda e: seconds(e[1]))
(OUT/'subtitles.ass').write_text(header+''.join('Dialogue: '+','.join(e)+'\n' for e in events))

blocks=[]
for folder, offset in [('dialogue-v018',0),('defence-v022',1669/24)]:
    for b in (V/'artifacts'/folder/'subtitles.srt').read_text().strip().split('\n\n'):
        lines=b.splitlines(); a,z=lines[1].split(' --> ')
        blocks.append((seconds(a)+offset,seconds(z)+offset,'\n'.join(lines[2:])))
for e in events:
    blocks.append((seconds(e[1])+2992/24,seconds(e[2])+2992/24,re.sub(r'\{[^}]*\}','',e[9]).replace('\\N','\n')))
(OUT/'samtoons-complete-v026.srt').write_text('\n\n'.join(f'{i}\n{timestamp(a,True)} --> {timestamp(z,True)}\n{text}' for i,(a,z,text) in enumerate(blocks,1))+'\n')

rows=json.loads((PREVIOUS/'edit.json').read_text()); table=next(r for r in rows if r['id']=='FR04')
start=(table['start_frame']-1)/24; end=start+table['frames']/24
enable=f'gte(t,{start})*lt(t,{end})'
# Editorial graphic on the existing banner; source rig, scene and timing unchanged.
vf=f"drawbox=x=125:y=0:w=801:h=65:color=0x1c283f:t=fill:enable='{enable}',drawtext=fontfile=/System/Library/Fonts/Supplemental/Arial.ttf:text='LEAGUE TABLE    1st ARSENAL    2nd CITY':fontsize=28:fontcolor=0xf7f1df:x=151:y=18:enable='{enable}',ass={OUT/'subtitles.ass'}"
run([FF,'-v','error','-y','-i',str(PREVIOUS/'picture.mp4'),'-vf',vf,'-an','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p',str(OUT/'remainder-picture.mp4')])
prefix=V/'artifacts/defence-v022/opening-through-defence-v022.mp4'
(OUT/'picture-list.txt').write_text(f"file '{prefix}'\nfile '{OUT/'remainder-picture.mp4'}'\n")
run([FF,'-v','error','-y','-f','concat','-safe','0','-i',str(OUT/'picture-list.txt'),'-map','0:v:0','-an','-c:v','copy',str(OUT/'complete-picture.mp4')])
movie=OUT/'samtoons-complete-v026.mp4'
run([FF,'-v','error','-y','-i',str(OUT/'complete-picture.mp4'),'-i',str(PREVIOUS/'samtoons-complete-review-v025.mp4'),'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(movie)])
info=json.loads(run(['/opt/homebrew/bin/ffprobe','-v','error','-show_streams','-of','json',str(movie)]).stdout)
v=next(s for s in info['streams'] if s['codec_type']=='video'); a=next(s for s in info['streams'] if s['codec_type']=='audio')
assert (int(v['nb_frames']),v['width'],v['height'],v['r_frame_rate']) == (6634,1280,720,'24/1')
assert a['sample_rate']=='48000' and a['channels']==2
run([FF,'-v','error','-i',str(movie),'-f','null','-'])
def audio_hash(path):
    return run([FF,'-v','error','-i',str(path),'-map','0:a:0','-c:a','pcm_s24le','-f','hash','-hash','sha256','-']).stdout.strip()
before=audio_hash(PREVIOUS/'samtoons-complete-review-v025.mp4'); after=audio_hash(movie)
assert before == after, 'Audio changed during caption-only finishing'
report=dict(frames=6634,resolution=[1280,720],fps=24,video_seconds=v['duration'],audio_seconds=a['duration'],decoded=True,audio_unchanged=before,sha256=hashlib.sha256(movie.read_bytes()).hexdigest(),caption_fixes=list(splits),listening='Not available to agent; full-film audition required',normal_speed_motion_review='User accepted v025 fixes; current agent pass samples frames and checks timing, not a new playback approval')
(OUT/'checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
