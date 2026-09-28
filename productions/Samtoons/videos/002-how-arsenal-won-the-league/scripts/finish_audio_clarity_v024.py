"""Resolve the actual final-batch contacts, captions and cached soundtrack."""
from pathlib import Path
from fractions import Fraction
import json,sys,subprocess,textwrap,hashlib
import soundfile as sf
V=Path(__file__).resolve().parents[1];O=V/'artifacts/clarity-v024';plan=json.loads((O/'audio-plan.json').read_text());edit=json.loads((O/'edit.json').read_text());shots={s['id']:s for s in plan['shots']};rows={r['id']:r for r in edit}
captions=json.loads((O/'captions.json').read_text());events=[]
for c in captions:
 words=c['text'].split();chunks=[];chunk=[]
 for w in words:
  if len(' '.join(chunk+[w]))>76 and chunk:chunks.append(' '.join(chunk));chunk=[]
  chunk.append(w)
 if chunk:chunks.append(' '.join(chunk))
 cursor=c['start'];total=sum(len(x.split()) for x in chunks)
 for part in chunks:
  end=cursor+(c['end']-c['start'])*len(part.split())/total;events.append(dict(start=cursor,end=end,speaker='FERGUSON' if c['id'] in ['L46','L47'] else c['speaker'],text=part));cursor=end
for sid,frame,text,dur in [('CP01',1,'The title chase',1.5),('VH02',1,'Telephone hold music',1.5),('N03',3,'Two-note mystery motif',1.4),('N04_dark',56,'The familiar two notes',1.5),('N04_reveal',1,'The final note',1.2)]:
 start=(rows[sid]['start_frame']+frame-2)/24;events.append(dict(start=start,end=start+dur,speaker='MUSIC',text=text,music=True))
events.sort(key=lambda e:e['start'])
header=(V/'artifacts/defence-v022/subtitles.ass').read_text().split('[Events]')[0]+'[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
def ts(t,ass=False):
 base=100 if ass else 1000;u=round(t*base);h,u=divmod(u,3600*base);m,u=divmod(u,60*base);s,u=divmod(u,base);return f'{h}:{m:02}:{s:02}.{u:02}' if ass else f'{h:02}:{m:02}:{s:02},{u:03}'
ass=[header];srt=[]
for i,r in enumerate(events,1):
 text=r['speaker']+': '+r['text'];text='['+text+']' if r.get('music') else text;wrapped='\n'.join(textwrap.wrap(text,54));assert len(wrapped.splitlines())<=2 and r['end']>r['start']
 srt.append(f'{i}\n{ts(r["start"])} --> {ts(r["end"])}\n{wrapped}\n');styled=wrapped.replace('\n','\\N');label=r['speaker']+':';styled=styled.replace(label,'{\\c&H84DBFF&}'+label+'{\\c&HFFFFFF&}',1)
 ass.append(f'Dialogue: 0,{ts(r["start"],True)},{ts(r["end"],True)},{"Music" if r.get("music") else "Speech"},{r["speaker"]},0,0,0,,{styled}\n')
(O/'subtitles.ass').write_text(''.join(ass));(O/'subtitles.srt').write_text('\n'.join(srt));(O/'caption-checks.json').write_text(json.dumps(dict(events=len(events),speaker_labels=True,narrator_name_hidden_until_reveal=True,phrase_timing='Proportional phrase split where long; word-perfect timing not claimed'),indent=2))
if '--captions-only' not in sys.argv:subprocess.run([sys.executable,str(V.parents[3]/'pipeline/audio.py'),'build',str(O/'audio-plan.json'),'--out',str(O/'mix')],check=True)
