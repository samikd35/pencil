"""Verify the exact preview and extract its high-risk regions for visual review."""
from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
O=Path(__file__).resolve().parent;V=O.parents[2];ff='/opt/homebrew/bin/ffmpeg';movie=O/'membership-review.mp4'
p=json.loads(subprocess.check_output(['/opt/homebrew/bin/ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)]))
v=next(s for s in p['streams'] if s['codec_type']=='video');a=next(s for s in p['streams'] if s['codec_type']=='audio')
assert (int(v['nb_frames']),v['avg_frame_rate'],v['width'],v['height'])==(312,'24/1',1280,720)
assert a['sample_rate']=='48000' and abs(float(p['format']['duration'])-13)<.05
subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],check=True)
for rel,sha in json.loads((O/'render-inputs.json').read_text()).items():assert hashlib.sha256((V/rel).read_bytes()).hexdigest()==sha,rel
out=O/'encoded-review';out.mkdir(exist_ok=True)
frames=[1,20,25,31,35,43,69,89,99,108,116,118,124,131,138,146,210,211,222,230,275,291,312]
for f in frames:
 subprocess.run([ff,'-v','error','-y','-i',str(movie),'-vf',f'select=eq(n\\,{f-1})','-frames:v','1',str(out/f'{f:03}.png')],check=True)
risk=[20,31,43,99,108,118,124,138]
sheet=Image.new('RGB',(4*350,2*350),'#1b2430');d=ImageDraw.Draw(sheet)
for i,f in enumerate(risk):
 im=Image.open(out/f'{f:03}.png')
 box=(310,310,695,695) if f==20 else (610,295,895,580) if f==31 else (755,300,955,500) if f==43 else (385,445,610,630)
 crop=im.crop(box).resize((300,300));x=(i%4)*350;y=(i//4)*350;sheet.paste(crop,(x+25,y+32));d.text((x+25,y+10),f'Frame {f} / moving grip and wrist',fill='white')
sheet.save(O/'grip-review.jpg',quality=93)
sheet=Image.new('RGB',(1280,1080),'#1b2430')
for i,f in enumerate([1,69,118,146,230,312]):
 im=Image.open(out/f'{f:03}.png').resize((640,360));sheet.paste(im,((i%2)*640,(i//2)*360))
sheet.save(O/'scene-review.jpg',quality=93)
(O/'verification.json').write_text(json.dumps({'frames':312,'fps':24,'size':[1280,720],'duration_seconds':13,'audio_sample_rate':48000,'full_decode':'passed','render_input_hashes':'matched','extracted_encoded_frames':frames,'visual_review':'Pending inspection of extracted crops','normal_speed_playback_review':'User checkpoint pending','audio_listened_by_agent':False},indent=2)+'\n')
print('Verified 312 frames and audio stream; extracted exact encoded review frames.')
