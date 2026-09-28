"""Mux the picture and original sound, verify the actual export, save review frames."""
from pathlib import Path
import json,re,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v001'
ff='/opt/homebrew/bin/ffmpeg';probe='/opt/homebrew/bin/ffprobe'
assert json.loads((OUT/'picture-master-checks.json').read_text())['frames']==720
assert json.loads((OUT/'project-checks.json').read_text())['embedded_soundtrack']
final=OUT/'three-goals-one-heartbreak.mp4'
with (OUT/'finish.log').open('w') as log:
    subprocess.run([ff,'-hide_banner','-y','-i',str(OUT/'picture-master.mp4'),'-i',str(OUT/'audio/soundtrack.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','-metadata','title=Three Goals. One Heartbreak.','-metadata','comment=Original stylized dramatization of the 2022 World Cup final, 18 December 2022. Simplified player characters. Original score, atmosphere and Foley; no narration or dialogue.',str(final)],stdout=log,stderr=log,check=True)
data=json.loads(subprocess.check_output([probe,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(final)]))
v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==(1080,1920,'24/1',720)
assert abs(float(data['format']['duration'])-30)<.05 and a['channels']==2 and a['sample_rate']=='48000'
subprocess.run([ff,'-v','error','-i',str(final),'-f','null','-'],check=True)
r=subprocess.run([ff,'-hide_banner','-i',str(final),'-vn','-af','loudnorm=I=-16:TP=-1.8:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
levels=json.loads(re.findall(r'\{[^{}]+\}',r.stderr)[-1]);assert -17<float(levels['input_i'])<-15 and float(levels['input_tp'])<-1
(OUT/'video-checks.json').write_text(json.dumps(data,indent=2)+'\n');(OUT/'audio/export-checks.json').write_text(json.dumps(levels,indent=2)+'\n')
for t in [0,1.5,2.7,3,3.6,4.8,6.6,7.5,8.1,9,10.65,12.1,13.8,15.25,16,17.1,18.625,19.4,21.25,22,23.8,25.7,27.4,28.8,29.8]:
    subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(final),'-frames:v','1',str(OUT/f'stills/final-{round(t*24)+1:04}.png')],check=True)
print(json.dumps({'video':str(final),'frames':720,'seconds':30,'integrated_lufs':levels['input_i'],'true_peak_dbtp':levels['input_tp']},indent=2),flush=True)
