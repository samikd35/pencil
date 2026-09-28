"""Reproducible diagnostic sheets from final encodes; no production edits."""
from pathlib import Path
import subprocess,json,io
from PIL import Image,ImageDraw
V=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
movie=V/'artifacts/delivery-v029/samtoons-final-1080p.mp4';records=json.loads((V/'artifacts/delivery-v027/edit.json').read_text());ledger={}
def frame(t,size=(400,225)):
 b=subprocess.check_output(['/opt/homebrew/bin/ffmpeg','-v','error','-ss',str(t),'-i',str(movie),'-frames:v','1','-vf',f'scale={size[0]}:{size[1]}','-f','image2pipe','-vcodec','png','-']);return Image.open(io.BytesIO(b)).convert('RGB')
def sheet(name,items,cols=3):
 im=Image.new('RGB',(cols*400,((len(items)+cols-1)//cols)*250),(245,242,235));d=ImageDraw.Draw(im)
 for i,(label,t) in enumerate(items):
  x=i%cols*400;y=i//cols*250;im.paste(frame(t),(x,y));d.text((x+6,y+229),f'{t:07.3f}s  {label}',fill='black')
 im.save(O/(name+'.jpg'),quality=88);ledger[name]=items
items=[]
for r in records:
 t=(r['start_frame']-1+r['frames']/2)/24;t+=3 if t>=7.5 else 0;items.append((r['id'],t))
items.insert(1,('brand_intro',9.5));items.append(('brand_outro',285))
for i in range(0,len(items),12):sheet(f'overview-{i//12+1:02}',items[i:i+12])
for name,start,end,step in [('walk',40,44,.25),('corner-delivery',74.5,79,.3),('header',81,83.2,.1),('chase',136,138,.125),('foul',168,170.2,.1),('referee',173.5,176.5,.2),('operator',178.5,181.5,.2),('winner',237.4,238.6,1/24),('trophy',256,259,.2),('meltdown',267,270,.2)]:
 times=[];t=start
 while t<end:times.append((name,round(t,6)));t+=step
 sheet('motion-'+name,times,4)
(O/'coverage.json').write_text(json.dumps({'source':str(movie),'method':'Midpoint of every original shot plus branding; diagnostic motion samples at stated timestamps. Not full normal-speed playback or exhaustive frame-by-frame inspection.','sheets':ledger},indent=2))
print('Diagnostic sheets complete',flush=True)
