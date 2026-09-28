"""Assemble the corrected native render, original score, and verification records."""
from pathlib import Path
import json
import re
import subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v001'
ff='/opt/homebrew/bin/ffmpeg';probe='/opt/homebrew/bin/ffprobe'
assert json.loads((OUT/'render-checks.json').read_text())['rendered_frames']==960
assert json.loads((OUT/'render-patch.json').read_text())['rendered_frames']==120
final=OUT/'the-goalkeeper-who-scored-the-winner.mp4'
graph='[0:v]split=2[before][after];[before]trim=end_frame=576,setpts=PTS-STARTPTS[v0];[1:v]setpts=PTS-STARTPTS[v1];[after]trim=start_frame=696,setpts=PTS-STARTPTS[v2];[v0][v1][v2]concat=n=3:v=1:a=0[v]'
with (OUT/'finish.log').open('w') as log:
    subprocess.run([ff,'-hide_banner','-y','-i',str(OUT/'picture-master.mp4'),'-i',str(OUT/'net-correction.mp4'),'-i',str(OUT/'audio/soundtrack.wav'),'-filter_complex',graph,'-map','[v]','-map','2:a:0','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','256k','-ar','48000','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart','-metadata','title=The Goalkeeper Who Scored the Winner','-metadata','comment=Original stick-figure reconstruction. West Brom 1-2 Liverpool, 16 May 2021. Original instrumental music and Foley; no narration.',str(final)],stdout=log,stderr=log,check=True)
data=json.loads(subprocess.check_output([probe,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(final)]))
v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==(1080,1920,'24/1',960)
assert abs(float(data['format']['duration'])-40)<.05
assert a['sample_rate']=='48000' and a['channels']==2
subprocess.run([ff,'-v','error','-i',str(final),'-f','null','-'],check=True)
measure=subprocess.run([ff,'-hide_banner','-i',str(final),'-vn','-af','loudnorm=I=-16:TP=-1.8:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
levels=json.loads(re.findall(r'\{[^{}]+\}',measure.stderr)[-1])
assert -17<float(levels['input_i'])<-15
assert float(levels['input_tp'])<-1
(OUT/'audio/exported-audio-check.json').write_text(json.dumps(levels,indent=2)+'\n')
(OUT/'video-checks.json').write_text(json.dumps(data,indent=2)+'\n')
for at in [0,2,5,9,11,15,17,20,21.875,22.5,22.8,24,24.5,25,28,30,33,37,39.5]:
    frame=round(at*24)+1
    subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-ss',str(at),'-i',str(final),'-frames:v','1',str(OUT/f'stills/final-{frame:04}.png')],check=True)
print(json.dumps({'video':str(final),'frames':v['nb_read_frames'],'seconds':data['format']['duration'],'integrated_lufs':levels['input_i'],'true_peak_dbtp':levels['input_tp']},indent=2))
