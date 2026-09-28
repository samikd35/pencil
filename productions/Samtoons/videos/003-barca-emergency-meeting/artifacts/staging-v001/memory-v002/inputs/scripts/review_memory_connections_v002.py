"""Verify the exact S10 connection-repair export and prepare joint review crops."""
from pathlib import Path
import hashlib,json,subprocess
from PIL import Image,ImageDraw
V=Path(__file__).resolve().parents[1]
O=V/'artifacts/staging-v001/memory-v002';OLD=O.with_name('memory-v001')
FF='/opt/homebrew/bin/ffmpeg';FP='/opt/homebrew/bin/ffprobe'
movie=O/'memory-review.mp4';out=O/'encoded-review';out.mkdir(exist_ok=True)
def run(args):return subprocess.check_output(args)
probe=json.loads(run([FP,'-v','error','-show_streams','-of','json',str(movie)]))
video=next(s for s in probe['streams'] if s['codec_type']=='video')
audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert int(video['nb_frames'])==264 and video['avg_frame_rate']=='24/1'
assert video['width']==1280 and video['height']==720 and audio['sample_rate']=='48000'
subprocess.run([FF,'-v','error','-i',str(movie),'-f','null','-'],check=True)
inputs=json.loads((O/'render-inputs.json').read_text())
for path,digest in inputs.items():assert hashlib.sha256((V/path).read_bytes()).hexdigest()==digest,path
frames=[1,23,38,42,46,47,48,54,64,76,81,119,138,139,149,164,170,171,172,185,220,264]
for f in frames:
 subprocess.run([FF,'-v','error','-y','-i',str(movie),'-vf',f'select=eq(n\\,{f-1})','-frames:v','1',str(out/f'{f:03}.png')],check=True)
# Same narration and sound, verified from decoded samples in the encoded previews.
def audio_hash(path):return hashlib.sha256(run([FF,'-v','error','-i',str(path),'-map','0:a:0','-f','s16le','-acodec','pcm_s16le','-'])).hexdigest()
same_audio=audio_hash(movie)==audio_hash(OLD/'memory-review.mp4');assert same_audio
sheet=Image.new('RGB',(1000,1180),'#172333');draw=ImageDraw.Draw(sheet)
for row,f in enumerate([119,171]):
 before=out/f'before-{f}.png'
 subprocess.run([FF,'-v','error','-y','-i',str(OLD/'memory-review.mp4'),'-vf',f'select=eq(n\\,{f-1})','-frames:v','1',str(before)],check=True)
 for col,path in enumerate([before,out/f'{f:03}.png']):
  crop=Image.open(path).crop((730,180,975,455)).resize((490,550))
  sheet.paste(crop,(col*500,row*590+30));draw.text((col*500+12,row*590+10),f'{"Before" if col==0 else "Revised"} / {"Lewandowski" if row==0 else "Raphinha"} / frame {f}',fill='white')
sheet.save(O/'joint-comparison.jpg',quality=94)
# Action poses: close framing follows the player as the shot camera moves.
film=Image.new('RGB',(1280,800),'#172333');draw=ImageDraw.Draw(film)
for idx,f in enumerate([23,38,47,54,119,149,164,185]):
 im=Image.open(out/f'{f:03}.png');crop=im.crop((450,170,740,490) if f<54 else (240,185,475,510) if f==54 else (730,165,990,570));crop.thumbnail((310,365))
 x=(idx%4)*320;y=(idx//4)*400;film.paste(crop,(x,y+26));draw.text((x+8,y+8),f'Frame {f}',fill='white')
film.save(O/'motion-joints.jpg',quality=94)
(O/'verification.json').write_text(json.dumps({'frames':264,'fps':24,'size':[1280,720],'audio_sample_rate':48000,'decoded_audio_identical_to_v001':same_audio,'full_decode':'passed','input_hashes':'matched','extracted_review_frames':frames,'visual_review':'Pending actual inspection; numerical checks do not establish motion quality.'},indent=2)+'\n')
print('Verified export and unchanged audio; joint and motion review sheets ready.')
