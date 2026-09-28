from pathlib import Path
import json,textwrap
V=Path(__file__).resolve().parents[1];O=V/'artifacts/dialogue-v018';cues=json.loads((O/'captions.json').read_text())
# Phrase boundaries checked against the new takes' word timestamps; text stays authoritative.
parts={
'L07':[(0,2.65,'So they bought a striker.'),(2.7,5.12,'Someone to finish the chances.')],
'B02':[(0,2.6,'This year, no excuses.'),(2.82,4.55,"I'm lifting that trophy,"),(4.62,6.32,'not applauding somebody else!')],
'B03':[(0,.94,'Bottles?'),(1.02,2.67,'Three years finishing second,'),(2.67,4.4,"and you've made us a subscription?")],
'B04':[(0,2.55,'Automatic renewal, boss.'),(2.66,4.28,'Cancel any time.'),(4.34,5.6,'Preferably before April.')],
'B05':[(0,1.2,'Hello, board?'),(1.24,2.7,'Buy me Gyökeres.'),(2.84,4.15,'A proper striker.'),(4.24,5.10,'Someone who finishes!')],
'L09':[(0,1.4,'Win us corners.'),(1.48,2.52,"That's where we score.")],
'L10':[(0,1.05,"Don't shoot!"),(1.1,1.96,'Hit the defender.'),(1.96,3.92,'Off him, out for a corner!')],
'L11':[(0,1.55,'Perfect. A corner!'),(1.64,2.88,'Now we can actually score.')]
}
rows=[]
for c in cues:
 for a,b,t in parts.get(c['id'],[(0,c['end']-c['start'],c['text'])]):rows.append(dict(start=c['start']+a,end=min(c['start']+b,c['end']),speaker=c['speaker'],text=t))
rows.append(dict(start=4/24,end=4/24+1.6,speaker='MUSIC',text='Two-note mystery motif',music=True));rows.sort(key=lambda r:r['start'])
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
ass.append('Dialogue: 1,0:00:00.25,0:00:06.70,Title,,0,0,0,,HOW ARSENAL WON THE LEAGUE\\N{\\fs25\\c&H84DBFF&}A RIVAL FAN NARRATES THE SEASON\n')
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
