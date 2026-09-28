from pathlib import Path
import subprocess,json,hashlib,shutil
root=Path('/Users/samikd/MyProjects/Pencil')
out=root/'experiments/009_style_gallery/artifacts/hand-layer-v006/chibi'
old=root/'experiments/009_style_gallery/proofs/workflow-v001/chibi/animatic-v001/animatic-with-sound.mp4'
movie=out/'animatic-with-sound.mp4'
compare=out/'before-after.mp4'
def run(args):return subprocess.run(args,check=True,capture_output=True).stdout
run(['ffmpeg','-v','error','-n','-i',str(out/'motion-picture.mp4'),'-i',str(old),'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(movie)])
font='/System/Library/Fonts/Supplemental/Arial.ttf'
layout=f'[0:v][1:v]hstack=inputs=2,pad=1280:400:0:40:color=0x263640,drawtext=fontfile={font}:text=Before:x=16:y=10:fontsize=22:fontcolor=white,drawtext=fontfile={font}:text=Corrected - same hand paths:x=656:y=10:fontsize=22:fontcolor=white[v]'
run(['ffmpeg','-v','error','-n','-filter_complex_threads','2','-i',str(old),'-i',str(movie),'-filter_complex',layout,'-map','[v]','-map','1:a:0','-c:v','libx264','-threads','4','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(compare)])
def probe(path):return json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(path)]))
def audio_hash(path,copy):
    flags=['-c:a','copy','-f','adts'] if copy else ['-c:a','pcm_s16le','-f','s16le']
    return hashlib.sha256(run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0',*flags,'-'])).hexdigest()
checks={}
for file in (movie,compare):
    p=probe(file);v=next(s for s in p['streams'] if s['codec_type']=='video');a=next(s for s in p['streams'] if s['codec_type']=='audio')
    assert v['nb_read_frames']=='240' and v['avg_frame_rate']=='24/1'
    assert abs(float(v['duration'])-10)<.001 and a['codec_name']=='aac'
    run(['ffmpeg','-v','error','-i',str(file),'-f','null','-'])
    checks[file.name]={'frames':240,'fps':24,'video_seconds':float(v['duration']),'size':[v['width'],v['height']],'decode':'passed','sha256':hashlib.sha256(file.read_bytes()).hexdigest()}
for copy,label in [(True,'aac_stream_sha256'),(False,'decoded_audio_pcm_sha256')]:
    original=audio_hash(old,copy)
    assert original==audio_hash(movie,copy)==audio_hash(compare,copy)
    checks[label]=original
checks['audio']='Original movie AAC copied unchanged; decoded PCM also identical. No new listening claimed.'
checks['review_status']='Technical checks passed; motion sheets and user playback review remain separate.'
(out/'delivery-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
shutil.copyfile(__file__,out/'package_hand_fix.py')
print(json.dumps(checks,indent=2))
