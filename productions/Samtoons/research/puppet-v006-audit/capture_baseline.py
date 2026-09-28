"""Reproduce the exact weak v006 poses from the encoded review, without editing art."""
from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[4]
V=ROOT/'productions/Samtoons/videos/003-barca-emergency-meeting'
OUT=Path(__file__).resolve().parent/'evidence';OUT.mkdir(exist_ok=True)
movie=V/'artifacts/staging-v001/call-performance-v006/call-review.mp4'
frames=[38,146,150,154,206,210,214,215]
for f in frames:
 subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-y','-i',str(movie),'-vf',f'select=eq(n\\,{f-1})','-frames:v','1',str(OUT/f'frame-{f:03}.png')],check=True)
# Actual encoded samples. No regeneration, warping or corrective image editing.
rects={'Muller':(120,220,342,519),'Perez':(781,244,1053,521)}
report=[]
for who,rect in rects.items():
 canvas=Image.new('RGB',(4*292,2*316),'#182633');draw=ImageDraw.Draw(canvas)
 for i,f in enumerate(frames):
  im=Image.open(OUT/f'frame-{f:03}.png');crop=im.crop(rect);x=(i%4)*292;y=(i//4)*316
  canvas.paste(crop,(x,y+25));draw.text((x+6,y+6),f'{who} | v006 frame {f}',fill='white')
 canvas.save(OUT/f'{who.lower()}-weak-poses.png');report.append({'actor':who,'crop':rect,'frames':frames,'source':str(movie.relative_to(ROOT))})
(OUT/'capture.json').write_text(json.dumps(report,indent=2)+'\n')
print('Captured 8 exact encoded frames per actor; visual inspection required, not an automatic quality pass.')
