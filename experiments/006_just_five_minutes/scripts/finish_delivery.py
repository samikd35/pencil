"""Mux the picture and original sound, verify the actual export, save review frames."""
from pathlib import Path
import json,re,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v001'
ff='/opt/homebrew/bin/ffmpeg';probe='/opt/homebrew/bin/ffprobe'
assert json.loads((OUT/'picture-master-checks.json').read_text())['frames']==900
assert json.loads((OUT/'project-checks.json').read_text())['embedded_soundtrack']
final=OUT/'just-five-minutes.mp4'
with (OUT/'finish.log').open('w') as log:
    subprocess.run([ff,'-hide_banner','-y','-i',str(OUT/'picture-master.mp4'),'-i',str(OUT/'audio/soundtrack.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','-metadata','title=Just Five Minutes','-metadata','comment=Original fictional 30-second story. Editable notebook animation reconstructed against the user-supplied Meesha reference. Original Foley; no narration or dialogue.',str(final)],stdout=log,stderr=log,check=True)
data=json.loads(subprocess.check_output([probe,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(final)]))
v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==(1920,1080,'30/1',900)
assert abs(float(data['format']['duration'])-30)<.05 and a['channels']==2 and a['sample_rate']=='48000'
subprocess.run([ff,'-v','error','-i',str(final),'-f','null','-'],check=True)
r=subprocess.run([ff,'-hide_banner','-i',str(final),'-vn','-af','loudnorm=I=-18:TP=-2:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
levels=json.loads(re.findall(r'\{[^{}]+\}',r.stderr)[-1]);assert -19<float(levels['input_i'])<-17 and float(levels['input_tp'])<-1
(OUT/'video-checks.json').write_text(json.dumps(data,indent=2)+'\n');(OUT/'audio/export-checks.json').write_text(json.dumps(levels,indent=2)+'\n')
for t in [0,1,3.15,4.1,4.4,4.8,5.5,6.2,7.2,8.6,9.4,10.5,12.5,15.2,17.4,18.2,19.5,20.5,21.8,23.5,24.1,25.3,27.2,27.8,28.35,29.5]:
    subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(final),'-frames:v','1',str(OUT/f'stills/final-{round(t*30)+1:04}.png')],check=True)
print(json.dumps({'video':str(final),'frames':900,'seconds':30,'integrated_lufs':levels['input_i'],'true_peak_dbtp':levels['input_tp']},indent=2),flush=True)
