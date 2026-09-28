from pathlib import Path
import json,textwrap
V=Path(__file__).resolve().parents[1];O=V/'artifacts/defence-v022';cues=json.loads((O/'captions.json').read_text())
# Phrase boundaries checked against the new takes' word timestamps; text stays authoritative.
parts={
'L12':[(0,2.5,'Their attacking philosophy?'),(3.2,4.55,'Win a corner.'),(4.8,7.04,"Somebody’s forehead will do the rest.")],
'L18b':[(0,.9,'Again?'),(1.05,2.45,"We’ve built a fortress…"),(2.7,5.2,'and City are still right behind us.')],
'L13':[(0,1.7,"One nil! That’s enough football."),(1.7,2.88,'Everybody back!')],
'L14':[(0,1.6,'Lovely.'),(2.35,5.8,'A goalkeeper protecting nine defenders.')]
}
rows=[]
for c in cues:
 for a,b,t in parts.get(c['id'],[(0,c['end']-c['start'],c['text'])]):rows.append(dict(start=c['start']+a,end=min(c['start']+b,c['end']),speaker=c['speaker'],text=t))
rows.append(dict(start=951/24,end=951/24+1.6,speaker='MUSIC',text='Two-note mystery motif',music=True));rows.append(dict(start=(511+185)/24,end=(511+185)/24+1.7,speaker='MUSIC',text='Choir of approval',music=True));rows.sort(key=lambda r:r['start'])
def ts(t,ass=False):
 u=round(t*(100 if ass else 1000));base=100 if ass else 1000;h,u=divmod(u,3600*base);m,u=divmod(u,60*base);s,u=divmod(u,base)
 return f'{h}:{m:02}:{s:02}.{u:02}' if ass else f'{h:02}:{m:02}:{s:02},{u:03}'
header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 0
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Speech,Arial,30,&H00FFFFFF,&H00FFFFFF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,3,2,0,2,65,65,10,1
Style: Music,Arial,23,&H00FFFFFF,&H00FFFFFF,&H80000000,&H80000000,0,-1,0,0,100,100,0,0,3,2,0,2,65,65,106,1
Style: Title,Arial,39,&H00FFFFFF,&H00FFFFFF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,3,3,0,8,50,50,45,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
ass=[header];srt=[]
# Diegetic result is expanded for readability at the notification beat.
ass.append('Dialogue: 1,0:00:09.87,0:00:11.20,Title,,0,0,0,,ARSENAL  1–0\\N{\\fs25}ONE CORNER. ONE GOAL.\n')
ass.append('Dialogue: 1,0:00:45.20,0:00:50.85,Title,,0,0,0,,{\\an9\\pos(1215,60)\\fs31}CITY WIN AGAIN\n')

for i,r in enumerate(rows,1):
 text=f"{r['speaker']}: {r['text']}"
 if r.get('music'):text='['+text+']'
 wrapped='\n'.join(textwrap.wrap(text,54));assert len(wrapped.splitlines())<=2 and r['end']>r['start']
 srt.append(f'{i}\n{ts(r["start"])} --> {ts(r["end"])}\n{wrapped}\n')
 styled=wrapped.replace('\n','\\N');label=r['speaker']+':'
 styled=styled.replace(label,'{\\c&H84DBFF&}'+label+'{\\c&HFFFFFF&}',1)
 ass.append(f'Dialogue: 0,{ts(r["start"],True)},{ts(r["end"],True)},{"Music" if r.get("music") else "Speech"},{r["speaker"]},0,0,0,,{styled}\n')
(O/'subtitles.ass').write_text(''.join(ass));(O/'subtitles.srt').write_text('\n'.join(srt));(O/'caption-checks.json').write_text(json.dumps(dict(events=len(rows),speaker_labels=True,narrator_identity_hidden=True,source='selected dialogue, aligned phrase boundaries; meaningful music cue labelled'),indent=2))
print(len(rows),'caption events')
