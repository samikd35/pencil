"""Read the reviewed export; make labelled diagnostic sheets without changing it."""
from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
movie=R/'artifacts/animatic-v001/animatic.mp4'
font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',14)
# Inclusive global one-based frame windows. Every frame in these windows is retained.
windows={'opening':(101,132),'good-kick':(240,271),'rashford-kick':(805,838),'rashford-arm':(874,905),'mainoo-kick':(1093,1126),'goal':(1435,1458),'martinez-arm':(1825,1856),'lammens-save':(2080,2111),'maguire-header':(2268,2291),'good-apology':(3236,3267)}
frames={k:[] for k in windows};overview=[]
p=subprocess.Popen(['/opt/homebrew/bin/ffmpeg','-v','error','-i',str(movie),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
count=0
while True:
 raw=p.stdout.read(960*540*3)
 if not raw:break
 assert len(raw)==960*540*3
 count+=1
 selected=[k for k,(a,b) in windows.items() if a<=count<=b]
 if selected or (count-1)%24==0:
  im=Image.frombytes('RGB',(960,540),raw)
  if (count-1)%24==0:overview.append((count,im.copy()))
  for k in selected:frames[k].append((count,im.copy()))
assert p.wait()==0 and count==3600
files=[]
def sheets(name,items,cols=4,rows=4):
 for page,start in enumerate(range(0,len(items),cols*rows),1):
  canvas=Image.new('RGB',(cols*480,rows*296),'#202630');d=ImageDraw.Draw(canvas)
  for n,(fr,im) in enumerate(items[start:start+cols*rows]):
   x=(n%cols)*480;y=(n//cols)*296
   canvas.paste(im.resize((480,270)),(x,y));d.text((x+5,y+273),f'F{fr:04d}  {(fr-1)/24:07.3f}s',font=font,fill='white')
  path=OUT/f'{name}-{page:02d}.jpg';canvas.save(path,quality=91);files.append(path.name)
sheets('overview',overview,5,5)
for k,items in frames.items():sheets(k,items)
probe=json.loads(subprocess.check_output(['/opt/homebrew/bin/ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time,pkt_duration_time','-of','json',str(movie)]))
pts=[float(x['best_effort_timestamp_time']) for x in probe['frames']]
steps=[b-a for a,b in zip(pts,pts[1:])]
report={'movie':str(movie),'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'decoded_frames':count,'fps':24,'duration_seconds':150,'pts_step_range_seconds':[min(steps),max(steps)],'overview':'every 24th frame (150 frames)','adjacent_windows_inclusive':windows,'adjacent_frame_count':sum(len(x) for x in frames.values()),'sheets':files,'limits':'Sheet generation is not visual review. Review coverage must be recorded separately.'}
(OUT/'extraction.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='sheets'},indent=2))
