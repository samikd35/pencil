"""Finish the authoritative mix, mux and check the encoded movie."""
from pathlib import Path
import os
import json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts'/os.environ.get('PENCIL_REVISION','film-v001');AUDIO=OUT/'audio-v002'
ff='/opt/homebrew/bin/ffmpeg';probe='/opt/homebrew/bin/ffprobe'
def run(args):return subprocess.run(args,capture_output=True,text=True,check=True)
def levels(path):
    r=run([ff,'-hide_banner','-i',str(path),'-vn','-af','loudnorm=I=-18:TP=-2:LRA=11:print_format=json','-f','null','-'])
    return json.loads(re.findall(r'\{[^{}]+\}',r.stderr)[-1])
mix=AUDIO/'soundtrack.wav'
if not mix.exists():
    m=levels(AUDIO/'mix-premaster.wav')
    filt=f"loudnorm=I=-18:TP=-2:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json"
    r=run([ff,'-hide_banner','-i',str(AUDIO/'mix-premaster.wav'),'-af',filt,'-ar','48000','-c:a','pcm_s24le',str(mix)])
    (AUDIO/'normalization.log').write_text(r.stderr)
if '--audio-only' in sys.argv:print('MIX_READY');sys.exit(0)
preview='--preview' in sys.argv
picture=OUT/('motion-preview.mp4' if preview else 'picture-master.mp4')
final=OUT/('preview-with-sound.mp4' if preview else 'barcelona-wasnt-ready-trent-was.mp4')
r=run([ff,'-hide_banner','-y','-i',str(picture),'-i',str(mix),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','-metadata',"title=Barcelona wasn't ready. Trent was.",'-metadata','comment=Original animated reconstruction of Liverpool v Barcelona, 7 May 2019. Simplified positions; reconstructed sound; no archival material.',str(final)])
(OUT/('preview-finish.log' if preview else 'finish.log')).write_text(r.stderr)
data=json.loads(subprocess.check_output([probe,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(final)]))
v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==((540 if preview else 1080),(960 if preview else 1920),'24/1',864)
assert abs(float(data['format']['duration'])-36)<.05 and a['channels']==2 and a['sample_rate']=='48000'
run([ff,'-v','error','-i',str(final),'-f','null','-'])
m=levels(final);assert -19<=float(m['input_i'])<=-17 and float(m['input_tp'])<=-1,m
(OUT/('preview-checks.json' if preview else 'video-checks.json')).write_text(json.dumps({'probe':data,'loudness':m,'full_decode':True,'audience_comprehension':'unknown','human_listening':'not performed'},indent=2)+'\n')
print(json.dumps({'video':str(final),'frames':864,'seconds':36,'integrated_lufs':m['input_i'],'true_peak_dbtp':m['input_tp']},indent=2))
