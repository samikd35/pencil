"""Mux the picture and original sound, verify the actual export, save review frames."""
from pathlib import Path
import json,re,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v001'
ff='/opt/homebrew/bin/ffmpeg';probe='/opt/homebrew/bin/ffprobe'
assert json.loads((OUT/'picture-master-checks.json').read_text())['frames']==768
assert json.loads((OUT/'project-checks.json').read_text())['embedded_soundtrack']
final=OUT/'how-was-this-ball-still-in.mp4'
with (OUT/'finish.log').open('w') as log:
    subprocess.run([ff,'-hide_banner','-y','-i',str(OUT/'picture-master.mp4'),'-i',str(OUT/'audio/soundtrack.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','-metadata','title=How Was This Ball Still In?','-metadata','comment=Original stick-figure reconstruction of Japan v Spain, 1 December 2022. Illustrative Law 9 geometry, not a measured reconstruction. Original score and Foley, no narration.',str(final)],stdout=log,stderr=log,check=True)
data=json.loads(subprocess.check_output([probe,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(final)]))
v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==(1080,1920,'24/1',768)
assert abs(float(data['format']['duration'])-32)<.05 and a['channels']==2 and a['sample_rate']=='48000'
subprocess.run([ff,'-v','error','-i',str(final),'-f','null','-'],check=True)
r=subprocess.run([ff,'-hide_banner','-i',str(final),'-vn','-af','loudnorm=I=-16:TP=-1.8:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
levels=json.loads(re.findall(r'\{[^{}]+\}',r.stderr)[-1]);assert -17<float(levels['input_i'])<-15 and float(levels['input_tp'])<-1
(OUT/'video-checks.json').write_text(json.dumps(data,indent=2)+'\n');(OUT/'audio/export-checks.json').write_text(json.dumps(levels,indent=2)+'\n')
for t in [0,.7,1.8,2.625,3.5,4.7,6.5,8,9.8,11.5,14.5,16,18.3,20,21.5,23.5,25.375,26.3,28,30.5]:
    subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(final),'-frames:v','1',str(OUT/f'stills/final-{round(t*24)+1:04}.png')],check=True)
print(json.dumps({'video':str(final),'frames':768,'seconds':32,'integrated_lufs':levels['input_i'],'true_peak_dbtp':levels['input_tp']},indent=2),flush=True)
