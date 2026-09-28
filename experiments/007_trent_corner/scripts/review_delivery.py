"""Export overview and successive-frame diagnostics from the final encoded movie."""
from pathlib import Path
import os,subprocess,json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts'/os.environ.get('PENCIL_REVISION','film-v001')
movie=OUT/'barcelona-wasnt-ready-trent-was.mp4';stills=OUT/'stills'
ff='/opt/homebrew/bin/ffmpeg'
def export(name,filter):
    subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-i',str(movie),'-vf',filter,'-frames:v','1',str(stills/name)],check=True)
frames=[0,72,216,276,352,360,372,384,396,456,600,816]
selection='+'.join(f'eq(n,{f})' for f in frames)
export('overview.jpg',f"select='{selection}',scale=270:480,tile=4x3")
for name,a,b in [('corner-contact',354,366),('delivery-and-finish',361,399),('replay-contact',583,595)]:
    export(name+'.jpg',f"select='between(n,{a},{b})',crop=1080:820:0:680,scale=324:246,tile=5x{(b-a+5)//5}")
for t in (3,11.5,15,16,16.5,19,30,34,35.95):
    subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(movie),'-frames:v','1',str(stills/f'final-{round(t*24)+1:04}.png')],check=True)
plan=ROOT/'production.json';resolved=json.loads((OUT/'audio-v002/resolved-cues.json').read_text())
assert hashlib.sha256(plan.read_bytes()).hexdigest()==resolved['plan_sha256']
for cue in resolved['cues']:
    assert cue['start_sample']+cue['onset_samples']==cue['event_sample']
    assert cue['trimmed_start_samples']==cue['trimmed_end_samples']==0
print('REVIEW_FRAMES_READY; exact cue onsets and untrimmed tails pass')
